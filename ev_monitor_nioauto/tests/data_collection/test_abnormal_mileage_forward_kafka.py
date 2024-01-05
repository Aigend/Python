""" 
@author:dun.yuan
@time: 2022/6/22 3:14 PM
@contact: dun.yuan@nio.com
@description: 触发里程跳变/异常的条件：
1. 当里程较上次更新增加大于500km且小于50000km时，将检查其平均每天里程是否超过2000km，即平均每秒的里程增加不超过0.02314815km。
2. 当里程较上次更新增加大于50000km时，将检查其平均每天里程是否超过1200km，即平均每秒的里程增加不超过0.01388889km。
3. 较上次上报的数据时间的间隔小于15s且对应的里程差距>=2时。
4. 上报里程值>=2000000（不会发送最近的正常里程及采样时间）
@showdoc：https://apidoc.nioint.com/project/4970/interface/api/380537
"""
import random

import pytest
import allure
import json
from utils.assertions import assert_equal


class TestAbnormalMileageForwardKafka(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, checker, cmdopt):
        '''如果无初始化值就返回0'''
        sql_result = checker.mysql.fetch_one('status_vehicle', {"id": vid}, ['mileage'])
        sample_ts = checker.redis.hash_hget(f'data_collection_{cmdopt}:{vid}', 'mileage_prefix').split('|')[0]
        return {'original_mileage': sql_result['mileage'] if sql_result else 0, 'sample_ts': int(sample_ts)}

    def test_mileage_more_2000_daily(self, vid, checker, publish_msg, prepare, kafka):
        # 重置offset
        kafka['cvs'].set_offset_to_end(kafka['topics']['mileage_check'])

        with allure.step("模拟描述里条件1的上报，构造期望消息"):
            # 构造并上报消息
            _, obj = publish_msg('periodical_journey_update',
                                 sample_points=[{"vehicle_status": {"mileage": prepare['original_mileage'] + 10000}}])

            expect_msg = {"vehicleId": vid,
                          "latestNormalMileage": prepare['original_mileage'],
                          "latestNormalSampleTs": prepare['sample_ts'],
                          "abnormalMileage": prepare['original_mileage'] + 10000,
                          "abnormalSampleTs": obj['sample_points'][0]['sample_ts'],
                          "processId": obj['journey_id']}

            with allure.step("验证转发里程跳变消息"):
                msg = None
                for data in kafka['cvs'].consume(kafka['topics']['mileage_check'], timeout=30):
                    msg = json.loads(data)
                    if msg['vehicleId'] == vid:
                        break
                msg.pop('timestamp')
                assert_equal(msg, expect_msg)

    @pytest.mark.skip("定期执行自动化，与上条重复，最好是找多天未上报行程的车单次验证")
    def test_mileage_more_1200_daily(self, vid, checker, publish_msg, prepare, kafka):
        # 重置offset
        kafka['cvs'].set_offset_to_end(kafka['topics']['mileage_check'])

        with allure.step("模拟描述里条件2的上报，构造期望消息"):
            # 构造并上报消息
            _, obj = publish_msg('periodical_charge_update',
                                 sample_points=[{"vehicle_status": {"mileage": prepare['original_mileage'] + 50001}}])

            expect_msg = {"vehicleId": vid,
                          "latestNormalMileage": prepare['original_mileage'],
                          "latestNormalSampleTs": prepare['sample_ts'],
                          "abnormalMileage": prepare['original_mileage'] + 50001,
                          "abnormalSampleTs": obj['sample_points'][0]['sample_ts'],
                          "processId": obj['charge_id']}

            with allure.step("验证转发里程跳变消息"):
                msg = None
                for data in kafka['cvs'].consume(kafka['topics']['mileage_check'], timeout=30):
                    msg = json.loads(data)
                    if msg['vehicleId'] == vid:
                        break
                msg.pop('timestamp')
                assert_equal(msg, expect_msg)

    def test_mileage_more_2000000_once(self, vid, checker, publish_msg, prepare, kafka):
        # 重置offset
        kafka['cvs'].set_offset_to_end(kafka['topics']['mileage_check'])

        with allure.step("模拟描述里条件4的上报，构造期望消息"):
            # 构造并上报消息
            _, obj = publish_msg('periodical_journey_update',
                                 sample_points=[{"vehicle_status": {"mileage": prepare['original_mileage'] + 2000000}}])

            expect_msg = {"vehicleId": vid,
                          "abnormalMileage": prepare['original_mileage'] + 2000000,
                          "abnormalSampleTs": obj['sample_points'][0]['sample_ts'],
                          "processId": obj['journey_id']}

            with allure.step("验证转发里程跳变消息"):
                msg = None
                for data in kafka['cvs'].consume(kafka['topics']['mileage_check'], timeout=30):
                    msg = json.loads(data)
                    if msg['vehicleId'] == vid:
                        break
                msg.pop('timestamp')
                assert_equal(msg, expect_msg)

    def test_mileage_more_2_in_15s(self, vid, checker, publish_msg, prepare, kafka, cmdopt):
        # 重置offset
        kafka['cvs'].set_offset_to_end(kafka['topics']['mileage_check'])

        with allure.step("模拟描述里条件3的上报，构造期望消息"):
            # 构造并上报消息
            _, obj1 = publish_msg('periodical_journey_update',
                                  sample_points=[{"vehicle_status": {"mileage": prepare['original_mileage']}}])

            _, obj2 = publish_msg('periodical_journey_update',
                                  sample_points=[{"vehicle_status": {"mileage": prepare['original_mileage'] + random.randint(2, 10)}}])

            expect_msg = {"vehicleId": vid,
                          "latestNormalMileage": prepare['original_mileage'],
                          "latestNormalSampleTs": obj1['sample_points'][0]['sample_ts'],
                          "abnormalMileage": obj2['sample_points'][0]['vehicle_status']['mileage'],
                          "abnormalSampleTs": obj2['sample_points'][0]['sample_ts'],
                          "processId": obj2['journey_id']}

            with allure.step("验证转发里程跳变消息"):
                msg = None
                for data in kafka['cvs'].consume(kafka['topics']['mileage_check'], timeout=30):
                    msg = json.loads(data)
                    if msg['vehicleId'] == vid:
                        break
                msg.pop('timestamp')
                assert_equal(msg, expect_msg)

        with allure.step("验证条件3，仍然落库"):
            tables = ['status_vehicle']

            for sample_point in obj2['sample_points']:
                checker.check_mysql_tables(sample_point, tables)

            mileage = int(checker.redis.hash_hget(f'data_collection_{cmdopt}:{vid}', 'mileage_prefix').split('|')[1])
            assert mileage == obj2['sample_points'][0]['vehicle_status']['mileage']
