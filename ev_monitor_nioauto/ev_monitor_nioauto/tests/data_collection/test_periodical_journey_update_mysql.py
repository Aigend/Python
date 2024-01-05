#!/usr/bin/env python
# coding=utf-8

"""
:file: test_periodical_journey_update_mysql.py
:author: zhiqiang.zhu
:Date: Created on 2017/1/12 下午8:01
:Description: 周期性充电消息上报，包含position_status数据，driving_data数据，vehicle_status数据，occupant_status数据，soc_status数据，
:alarm数据，driving_motor数据，extremum数据，btry_packs数据，hvac_status数据，signal_status数据，tyre_status数据。
"""
import random
import time

import pytest
import allure

from utils import message_formator
from utils.assertions import assert_equal
from utils.checker import Checker
from utils.time_parse import timestamp_to_utc_strtime


class TestJouneyUpdateMsg(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, checker):
        '''如果无初始化值就返回0'''
        sql_result = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])
        return {'original_mileage': sql_result[0]['mileage'] if sql_result else 0}

    def test_periodical_journey_update(self, vid, checker, publish_msg, prepare):
        # 构造并上报消息
        nextev_message, journey_update_obj = publish_msg('periodical_journey_update',
                                                         sample_points=
                                                         [{
                                                             "vehicle_status": {"mileage": prepare['original_mileage'] + 1}
                                                         }]
                                                         )

        # 校验
        tables = ['status_position', 'status_vehicle', 'status_soc',
                  'status_btry_packs', 'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                  'status_extremum_data', 'status_driving_data', 'status_hvac',
                  'status_tyre']

        for sample_point in journey_update_obj['sample_points']:
            checker.check_mysql_tables(sample_point, tables)

    def test_mileage_wont_update(self, vid, checker, prepare, publish_msg):
        # 校验当传入mileage为0，stataus_vehicle表中mileage字段不更新
        nextev_message, journey_update_obj = publish_msg('periodical_journey_update',
                                                         sample_points=
                                                         [{
                                                             "vehicle_status": {"mileage": 0},
                                                         }])

        with allure.step("校验当传入mileage为0，stataus_vehicle表中mileage字段不更新"):
            mileage_in_mysql = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])[0]
            assert_equal(mileage_in_mysql['mileage'], prepare['original_mileage'])

    @pytest.mark.skip('manual')
    def test_mileage_update_while_null_in_status_vehicle(self):
        """
        校验MySQL数据库中的status_vehicle@remote_vehicle_test表的mileage字段为Null时，mileage的状态更新问题

        该case只能手工运行，因为不能直接将mysql里的mileage字段设置为null，来模拟数据不存在status_vehicle表的情况。
        更新mysql的时候会有缓存和redis检测的操作，如果相应的数据存在的话会用更新语句进行更新，而不是用插入语句。
        例如删除了CDC的F110条目数据，上报后，mysql中只更新了F118和F18C两条纪录，而不插入F110
        """
        """
        pangu系统造车流程
        1、TSP中选择相应环境，选择"造车相关MOCK"，一键造车。记录vid，vin，client_id
        2、Account中选择相应环境，申请手机号。记录手机号、验证码和account_id，登录APP
        3、TSP中选择"人车关系"，输入Vid和account_id进行账号和车辆的绑定
        4、TSP中选择"车辆激活"，输入Vid生成激活二维码，APP扫描该激活码进行激活
        5、TSP中选择"车辆在线_CGW"，输入Vin使车辆在线
        """

        with allure.step("当有效的mileage上报后，data_collection能正确落库该mileage"):
            """
            select * from status_vehicle where id='6e9d6aec3e4a4ef8ab130db1310c83e2' 

            id	                                vehl_sts    chrg_sts    oprtn_mode  speed	    mileage ...
            6e9d6aec3e4a4ef8ab130db1310c83e2	3           254         254         225.89999   [Null]  ...
            
            上报mileage字段为有效正整数（如mileage=1）后：
            
            id	                                vehl_sts    chrg_sts    oprtn_mode  speed	    mileage ...
            6e9d6aec3e4a4ef8ab130db1310c83e2	3           254         254         225.89999   1       ...
            """
            pass

        with allure.step("上报mileage字段的信息为负数，mileage状态不会更新"):
            """
            select * from status_vehicle where id='6e9d6aec3e4a4ef8ab130db1310c83e2' 

            id	                                vehl_sts    chrg_sts    oprtn_mode  speed	    mileage ...
            6e9d6aec3e4a4ef8ab130db1310c83e2	3           254         254         225.89999   [Null]  ...

            上报mileage字段为无效负数（如mileage=-1）后：

            id	                                vehl_sts    chrg_sts    oprtn_mode  speed	    mileage ...
            6e9d6aec3e4a4ef8ab130db1310c83e2	3           254         254         225.89999   [Null]  ...
            """

    @pytest.mark.test
    def test_reissue(self, vid, checker, publish_msg, prepare):

        with allure.step("校验当reissue为True时，mysql数据库仍会更新"):
            # 构造并上报消息
            nextev_message, journey_update_obj = publish_msg('periodical_journey_update',
                                                             reissue=True,
                                                             sample_points=
                                                             [{
                                                                 "vehicle_status": {"mileage": prepare['original_mileage'] + 1}
                                                             }]
                                                             )

            # 校验
            tables = ['status_position', 'status_vehicle', 'status_soc',
                      'status_btry_packs', 'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                      'status_extremum_data', 'status_driving_data', 'status_hvac',
                      'status_tyre']

            for sample_point in journey_update_obj['sample_points']:
                checker.check_mysql_tables(sample_point, tables)

    @pytest.mark.test
    def test_posng_valid_type(self, vid, prepare, checker, publish_msg):
        with allure.step("校验 位置信息标为无效时，只要经纬度不为0或null，status_position仍会保存位置信息"):
            # 上报

            nextev_message, journey_update_obj = publish_msg('periodical_journey_update',
                                                             sample_points=
                                                             [{
                                                                 "vehicle_status": {"mileage": prepare['original_mileage'] + 1},
                                                                 "position_status": {
                                                                     "posng_valid_type": random.choice([1, 2])
                                                                 }
                                                             }]
                                                             )

            # 校验
            tables = ['status_position', 'status_vehicle', 'status_soc',
                      'status_btry_packs', 'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                      'status_extremum_data', 'status_driving_data', 'status_hvac',
                      'status_tyre']

            for sample_point in journey_update_obj['sample_points']:
                checker.check_mysql_tables(sample_point, tables)

    @pytest.mark.test
    def test_latitude_longitude_is_zero(self, vid, prepare, checker, publish_msg):
        with allure.step("校验 当经度或纬度为0时，不管位置信息标识为有效还是无效，status_position都不会保存位置信息"):
            # 上报

            original_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]

            position_status = random.choice([{'longitude': 110.111111, 'latitude': 0}, {'longitude': 0, 'latitude': 35.333333}])

            nextev_message, journey_update_obj = publish_msg('periodical_journey_update',
                                                             sample_points=
                                                             [{
                                                                 "vehicle_status": {
                                                                     "mileage": prepare['original_mileage'] + 1},
                                                                 "position_status": position_status
                                                             }]
                                                             )
            # Check position won't update
            new_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]
            assert_equal(original_position_status_in_mysql, new_position_status_in_mysql)

    def test_latitude_longitude_is_null(self, vid, prepare, checker, publish_msg):
        with allure.step("校验 当经度或纬度为null时，不管位置信息标识为有效还是无效，status_position都不会保存位置信息"):
            original_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]

            clear_field = random.choice(['sample_points[0].position_status.longitude', 'sample_points[0].position_status.latitude'])

            nextev_message, journey_update_obj = publish_msg('periodical_journey_update',
                                                             sample_points=
                                                             [{
                                                                 "vehicle_status": {
                                                                     "mileage": prepare['original_mileage'] + 1},
                                                             }],
                                                             clear_fields=[clear_field]
                                                             )

            # 校验
            # Check other tables will update
            tables = ['status_vehicle', 'status_soc',
                      'status_btry_packs', 'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                      'status_extremum_data', 'status_driving_data', 'status_hvac',
                      'status_tyre']

            for sample_point in journey_update_obj['sample_points']:
                checker.check_mysql_tables(sample_point, tables)

            # Check position won't update
            new_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]
            assert_equal(original_position_status_in_mysql, new_position_status_in_mysql)

    @pytest.mark.test
    def test_invalid_btry_pak_sn(self, vid, publish_msg, checker, prepare):
        # 校验 status_btry_packs表不存入btry_pak_sn为0的整条数据

        # 构造并上报消息
        event_name = 'periodical_journey_update'
        nextev_message, obj = publish_msg(event_name,
                                          sample_points=
                                          [{
                                              "vehicle_status": {"mileage": prepare['original_mileage'] + 1},
                                              "soc_status": {"btry_paks": [{
                                                  'btry_pak_sn': 0
                                              }]}
                                          }],
                                          )

        # 校验其他表能正常存入数据
        tables = ['status_position', 'status_vehicle', 'status_soc',
                  'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                  'status_extremum_data', 'status_driving_data', 'status_hvac',
                  'status_tyre']
        checker.check_mysql_tables(obj['sample_points'][0], tables, event_name=event_name)

        # 校验status_btry_packs表不存入btry_pak_sn为0的数据
        btry_paks_status_in_mysql = checker.mysql.fetch('status_btry_packs',
                                                        {"id": vid, "serial_num": obj['sample_points'][0]['soc_status']['btry_paks'][0]['btry_pak_sn']},
                                                        retry_num=10)
        assert_equal(len(btry_paks_status_in_mysql), 0)

    def test_invalid_extremum_data(self, vid, publish_msg, checker, prepare):
        with allure.step('校验sin_btry_hist_volt 与sin_btry_lwst_volt 的取值范围为[0,100)'):
            event_name = 'periodical_journey_update'

            sin_btry_hist_volt = random.choice([-1, 100])
            sin_btry_lwst_volt = random.choice([-1, 100])
            nextev_message, obj = publish_msg(event_name,
                                              sample_points=[{
                                                  "vehicle_status": {"mileage": prepare['original_mileage'] + 1},
                                                  "extremum_data":
                                                      {"sin_btry_hist_volt": sin_btry_hist_volt,
                                                       "sin_btry_lwst_volt": sin_btry_lwst_volt,
                                                       }
                                              }],
                                              )
            status_extremum_in_mysql_old = checker.mysql.fetch('status_extremum_data', {"id": vid}, exclude_fields=['update_time'])[0]

            formator = message_formator.MessageFormator(vid, obj['sample_points'][0]['sample_ts'])
            status_extremum_in_msg = formator.to_mysql_status_extremum_data(obj['sample_points'][0]['extremum_data'])
            with allure.step('校验除status_extremum_data表外其他表能正常存入数据'):
                tables = ['status_position', 'status_vehicle', 'status_soc',
                          'status_btry_packs', 'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                          'status_driving_data', 'status_hvac',
                          'status_tyre']
                checker.check_mysql_tables(obj['sample_points'][0], tables, event_name=event_name)

            with allure.step('校验status_extremum_data表sin_btry_hist_volt, sin_btry_lwst_volt字段值为上报之前的值'):
                status_extremum_in_mysql_new = checker.mysql.fetch('status_extremum_data', {"id": vid}, exclude_fields=['update_time'])[0]
                assert_equal(status_extremum_in_mysql_old['sin_btry_hist_volt'], status_extremum_in_mysql_new['sin_btry_hist_volt'])
                assert_equal(status_extremum_in_mysql_old['sin_btry_lwst_volt'], status_extremum_in_mysql_new['sin_btry_lwst_volt'])

            with allure.step('校验status_extremum_data表sin_btry_hist_volt, sin_btry_lwst_volt以外的字段照常存入新值'):
                status_extremum_in_mysql_new.pop('sin_btry_hist_volt')
                status_extremum_in_mysql_new.pop('sin_btry_lwst_volt')
                status_extremum_in_msg.pop('sin_btry_hist_volt')
                status_extremum_in_msg.pop('sin_btry_lwst_volt')
                assert_equal(status_extremum_in_mysql_new, status_extremum_in_msg)

    @pytest.mark.test
    def test_sample_ts_update(self, env, publish_msg_by_kafka, mysql):
        """
        因为报未来时间会对其他案例造成影响所以更换一下车辆
        状态表更新规则（适用于所有更新状态表的事件）：
        1、上报的sample_ts <= 服务器当前时间 + 1小时 （现在最多能报未来一个小时的数据了）
        2、上报的sample_ts > 数据库sample_ts
        """
        with allure.step('校验上报的sample_ts在当前时间1小时5分钟之后，不能够更新状态表'):
            tables = ['status_position', 'status_vehicle', 'status_soc',
                      'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                      'status_extremum_data', 'status_driving_data', 'status_hvac',
                      'status_tyre']
            old_update_time = {}
            new_update_time = {}
            vid = env['vehicles']['v_sample_ts']['vehicle_id']
            vin = env['vehicles']['v_sample_ts']['vin']
            original_mileage_in_mysql = mysql['rvs'].fetch('status_vehicle', {"id": vid}, ['mileage'])[0]['mileage']
            # 上报一条1小时5分钟后的数据
            for table in tables:
                old_update_time[table] = mysql['rvs'].fetch(table, {"id": vid})[0]["update_time"]
            publish_msg_by_kafka('periodical_journey_update', vin=vin, vid=vid,
                                 sample_points=[{"vehicle_status": {"mileage": original_mileage_in_mysql + 1}, "sample_ts": int((time.time() + 7200) * 1000)}],
                                 sleep_time=0)
            for table in tables:
                new_update_time[table] = mysql['rvs'].fetch(table, {"id": vid})[0]["update_time"]
            assert_equal(old_update_time, new_update_time)

    def test_sample_ts_null(self, env, publish_msg_by_kafka, mysql, cmdopt, api):
        """
        上报的sample_ts > 服务器当前时间 + 1小时 data_collection会将其置为null
        每0.5秒对消费的数据进行merge操作，校验有sample_ts为null的数据时也能merge成功。

        但是这条sample_ts是未来时间的数据还是会存mongodb的, 导致mongodb中sample_ts之前的数据不会更新。
        所以为了不影响mongodb的case，这里使用单独一辆车做校验。
        """
        vid = env['vehicles']['v_sample_ts']['vehicle_id']
        vin = env['vehicles']['v_sample_ts']['vin']
        original_mileage_in_mysql = mysql['rvs'].fetch('status_vehicle', {"id": vid}, ['mileage'])[0]['mileage']
        with allure.step('校验上报的sample_ts在当前时间1小时5分钟之后，不能够更新状态表'):
            tables = ['status_position', 'status_vehicle', 'status_soc',
                      'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                      'status_extremum_data', 'status_driving_data', 'status_hvac',
                      'status_tyre']
            # 上报一条2小时后的数据
            nextev_message, publish_invalid = publish_msg_by_kafka(
                'periodical_journey_update',
                vin=vin, vid=vid,
                sample_points=[
                    {
                        "vehicle_status": {"mileage": original_mileage_in_mysql + 1},
                        "sample_ts": int((time.time() + 7200) * 1000)
                    }
                ],
                sleep_time=0
            )
            # 上报一条当前的数据
            nextev_message, publish_valid = publish_msg_by_kafka(
                'periodical_journey_update',
                vin=vin, vid=vid,
                sample_points=[
                    {
                        "vehicle_status": {"mileage": original_mileage_in_mysql + 1},
                        "sample_ts": int((time.time()) * 1000)
                    }
                ]
            )
            v_sample_ts_checker = Checker(vin=vin, vid=vid, cmdopt=cmdopt, env=env, api=api)
            v_sample_ts_checker.check_mysql_tables(publish_valid['sample_points'][0], tables, event_name='periodical_journey_update')
            del v_sample_ts_checker

    def test_abnormal_value(self, vid, publish_msg, checker, prepare):
        """
        climb、altitude字段线上超过数据库字段范围的非法值较普遍，易导致报错且不更新mysql。
        对于超过范围的值，设置值为字段范围的临界值climb(±9999.999999)、altitude(±9999.999)。
        该规则适用于所有更新状态表的事件。
        """
        with allure.step('校验上报超过数据库字段范围的非法值，仍然能够更新状态表'):
            nextev_message, obj = publish_msg(
                'periodical_journey_update',
                sample_points=[
                    {
                        "vehicle_status": {"mileage": prepare['original_mileage'] + 1},
                        "position_status": {"climb": 100000, "altitude": 100000}
                    }
                ]
            )
            # 校验状态表能正常存入数据
            tables = ['status_position', 'status_vehicle', 'status_soc',
                      'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                      'status_extremum_data', 'status_driving_data', 'status_hvac',
                      'status_tyre']
            checker.check_mysql_tables(obj['sample_points'][0], tables, event_name='periodical_journey_update')

    def test_parse_can_msg(self, vid, prepare, publish_msg, checker):
        """
        https://jira.nioint.com/browse/CVS-14698
        携带can id为623，信号名为BMSBatteryPackCap的can消息，解析出BMSBatteryPackCap，写入soc_status表的字段battery_pack_cap里
        BMSBatteryPackCap对应的是can_data里的28~31比特位
        http://venus.nioint.com/#/detailWorkflow/wf-20220424145320-l2
        携带can id为537，590解析VCUChrgDispLampReq,VCUChrgDispCrrt,VCUChrgDispVolt,VCUChrgPwr字段，存储到stauts_soc表中
        :param vid:
        :param prepare:
        :param publish_msg:
        :param checker:
        :return:
        """
        with allure.step("上报携带BMSBatteryPackCap的can消息的periodical_journey_update事件"):
            event_name = 'periodical_journey_update'
            mileage = prepare['original_mileage'] + 1
            nextev_message, obj = publish_msg(event_name,
                                              sample_points=[{"vehicle_status": {"mileage": mileage},
                                                             'can_msg': {
                                                                'can_data': [
                                                                    {
                                                                        'msg_id': 623,
                                                                        'value': b'\x00\x02\x14\x86\x23\x10\x11\x02'
                                                                    },
                                                                    {
                                                                        'msg_id': 537,
                                                                        'value': b'\x00\x02\xc4\x86\x23\x10\x11\x00'
                                                                    },
                                                                    {
                                                                        'msg_id': 590,
                                                                        'value': 'ffffffffffffffff'
                                                                    }
                                                                ]
                                                             }
                                              }])

        with allure.step("校验status_soc表的存储"):
            status_soc_in_mysql = checker.mysql.fetch_one('status_soc',
                                                          {"id": vid, "sample_time": timestamp_to_utc_strtime(obj['sample_points'][0]['sample_ts'])},
                                                          exclude_fields=['update_time', 'chg_subsys_len', 'chrg_pwr',
                                                                          'chg_subsys_encoding',
                                                                          'charger_type', 'in_volt_ac',
                                                                          'in_volt_dc', 'in_curnt_ac', 'chrg_disp_crrt',
                                                                          'estimate_chrg_time', 'chrg_disp_volt'])
            formator = message_formator.MessageFormator(vid, obj['sample_points'][0]['sample_ts'])
            soc_status_in_message = formator.to_mysql_status_soc(obj['sample_points'][0]['soc_status'])
            soc_status_in_message['battery_pack_cap'] = 8 # 8代表75度电池
            # soc_status_in_message['chrg_pwr'] = 523.5
            # soc_status_in_message['chrg_disp_crrt'] = 4553.5
            # soc_status_in_message['chrg_disp_volt'] = 1023.5
            soc_status_in_message['chrg_disp_lamp_req'] = 6
            assert_equal(status_soc_in_mysql, soc_status_in_message)

        with allure.step("校验mongo can_msg,电池信息上报10分钟之内在mongo查询，超过10分钟查询mysql"):
            can_msg_in_mongo = checker.mongodb.find("can_msg", {"_id": f"{vid}_623"})[0]
            assert can_msg_in_mongo['timestamp'] == obj['sample_points'][0]['sample_ts']
            assert can_msg_in_mongo['value']['BMSBatteryPackCap'] == 8
