#!/usr/bin/env python
# coding=utf-8

"""
:file: test_journey_start_event_mysql.py
:author: zhiqiang.zhu
:Date: Created on 2017/1/12
:Description: 行驶结束消息，包含position数据和soc数据
"""
import random
import pytest
import allure
import time

from utils.assertions import assert_equal


class TestJourneyStartMsg(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, checker):
        '''如果无初始化值就返回0'''
        sql_result = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])
        return {'original_mileage': sql_result[0]['mileage'] if sql_result else 0}

    @pytest.fixture(scope='function', autouse=False)
    def cleanup(self, vid, checker, request):
        def fin():
            checker.vid = vid
        request.addfinalizer(fin)

    def test_journey_start_event(self, vid, prepare,checker, publish_msg):
        # 构造并上报消息
        mileage = prepare['original_mileage'] + 1
        nextev_message, journey_start_obj = publish_msg('journey_start_event',
                                                        vehicle_status={"mileage": mileage},
                                                        )

        # 校验
        tables =['status_position','status_vehicle', 'status_soc', 'status_btry_packs', 'status_hvac']
        checker.check_mysql_tables(journey_start_obj, tables, event_name='journey_start_event')

    def test_pm25fil_valid(self, vid, checker, prepare, publish_msg_by_kafka, cmdopt):
        """
        在车唤醒后的一小段时间内触发了journey start事件，车机来不及获取pm25_fil数据，就会上报默认值127
        仅mysql做校验值[0, 100]范围的处理，若pm25_fil为默认值127，整个hvac状态表都不更新
        """
        with allure.step("校验 pm25_fil>100 不能更新status_hvac"):
            mileage = prepare['original_mileage'] + 1
            pm25_fil = 101
            old_update_time = checker.mysql.fetch('status_hvac', {"id": vid})[0]["update_time"]
            nextev_message, journey_start_obj = publish_msg_by_kafka('journey_start_event',
                                                                     pm25_fil=pm25_fil,
                                                                     vehicle_status={"mileage": mileage})

            # 校验其他状态表正常更新
            tables = ['status_position', 'status_vehicle', 'status_soc', 'status_btry_packs']
            checker.check_mysql_tables(journey_start_obj, tables, event_name='journey_start_event')
            # 校验status_hvac不更新
            new_update_time = checker.mysql.fetch('status_hvac', {"id": vid})[0]["update_time"]
            assert_equal(old_update_time == new_update_time, True)

        with allure.step("校验 pm25_fil<0 不能更新status_hvac"):
            mileage = prepare['original_mileage'] + 1
            pm25_fil = -1
            old_update_time = checker.mysql.fetch('status_hvac', {"id": vid})[0]["update_time"]
            nextev_message, journey_start_obj = publish_msg_by_kafka('journey_start_event',
                                                                     pm25_fil=pm25_fil,
                                                                     vehicle_status={"mileage": mileage + 1})

            # 校验其他状态表正常更新
            tables = ['status_position', 'status_vehicle', 'status_soc', 'status_btry_packs']
            checker.check_mysql_tables(journey_start_obj, tables, event_name='journey_start_event')
            # 校验status_hvac不更新
            new_update_time = checker.mysql.fetch('status_hvac', {"id": vid})[0]["update_time"]
            assert_equal(old_update_time == new_update_time, True)

    def test_mileage_wont_update(self, vid,checker, prepare, publish_msg):
        # 校验当传入mileage为0，stataus_vehicle表中mileage字段不更新
        mileage = 0
        nextev_message, journey_start_obj = publish_msg('journey_start_event',
                                                        vehicle_status={"mileage": mileage}
                                                        )

        with allure.step("校验当传入mileage为0，stataus_vehicle表中mileage字段不更新"):
            mileage_in_mysql = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])[0]
            assert_equal(mileage_in_mysql['mileage'], prepare['original_mileage'])

    def test_posng_valid_type(self, vid, prepare,checker, publish_msg):
        with allure.step("校验 位置信息标为无效时，只要经纬度不为0或null，status_position仍会保存位置信息"):
            mileage = prepare['original_mileage'] + 1
            nextev_message, obj = publish_msg('journey_start_event',
                                              vehicle_status={"mileage": mileage},
                                              position_status={"posng_valid_type": random.choice([1, 2])}
                                              )
            tables = ['status_position', 'status_vehicle', 'status_soc', 'status_btry_packs', 'status_hvac']
            checker.check_mysql_tables(obj, tables, event_name='journey_start_event')

    def test_latitude_longitude_is_zero(self, vid, prepare,checker, publish_msg):
        with allure.step("校验 当经度或纬度为0时，不管位置信息标识为有效还是无效，status_position都不会保存位置信息"):
            mileage = prepare['original_mileage'] + 1
            original_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]

            position_status = random.choice([{'longitude':110.111111,'latitude':0},{'longitude':0,'latitude':35.333333}])
            nextev_message, obj = publish_msg('journey_start_event',
                                              vehicle_status={ "mileage": mileage},
                                              position_status=position_status,
                                              )

            # Check other tables will update
            tables = ['status_vehicle', 'status_soc', 'status_btry_packs', 'status_hvac']
            checker.check_mysql_tables(obj, tables, event_name='journey_start_event')

            # Check position won't update
            new_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]
            assert_equal(original_position_status_in_mysql, new_position_status_in_mysql)

    def test_latitude_longitude_is_null(self, vid, prepare,checker, publish_msg):
        with allure.step("校验 当经度或纬度为null时，不管位置信息标识为有效还是无效，status_position都不会保存位置信息"):
            mileage = prepare['original_mileage'] + 1
            original_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]

            clear_field = random.choice(['position_status.longitude','position_status.latitude'])
            nextev_message, obj = publish_msg('journey_start_event',
                                              vehicle_status={"mileage": mileage},
                                              clear_fields=[clear_field]
                                              )

            # Check other tables will update
            tables = ['status_vehicle', 'status_soc', 'status_btry_packs', 'status_hvac']
            checker.check_mysql_tables(obj, tables, event_name='journey_start_event')

            # Check position won't update
            new_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]
            assert_equal(original_position_status_in_mysql, new_position_status_in_mysql)

    @pytest.mark.test
    def test_invalid_btry_pak_sn(self, vid, prepare, publish_msg,checker):
        # 校验 soc_status的btry_paks不会存入status_btry_packs表中，如果btry_pak_sn=0

        # 构造并上报消息
        event_name = 'journey_start_event'
        mileage = prepare['original_mileage'] + 1
        nextev_message, obj = publish_msg(event_name,
                                              vehicle_status= {"mileage": mileage},
                                              soc_status={"btry_paks": [{
                                                           'btry_pak_sn': 0
                                                       }]}
                                          )

        # 校验其他表能正常存入数据
        tables = ['status_position', 'status_vehicle', 'status_soc', 'status_hvac']
        checker.check_mysql_tables(obj, tables, event_name=event_name)

        # 校验status_btry_packs表不存入btry_pak_sn为0的数据
        btry_paks_status_in_mysql = checker.mysql.fetch('status_btry_packs',
                                                       {"id": vid, "serial_num": obj['soc_status']['btry_paks'][0]['btry_pak_sn']},
                                                        retry_num=10)
        assert_equal(len(btry_paks_status_in_mysql), 0)

    def test_max_mileage_mysql(self, vid, checker, publish_msg_by_kafka, prepare):
        with allure.step("校验上报大于200万的mileage消息后，消息中的mileage字段不能更新mysql"):
            illegal_mileage = 2000000 + 1
            # 上报不合法的mileage信息
            publish_msg_by_kafka('journey_start_event', vehicle_status={"mileage": illegal_mileage})
            # 校验mysql（只是不更新mileage，其他字段会更新）
            mileage_in_mysql = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])[0]
            assert_equal(mileage_in_mysql['mileage'], prepare['original_mileage'])

    def test_ntester_None_to_False(self, vid, checker, prepare, publish_msg_by_kafka):
        with allure.step("校验上报的ntester为空时，将处理为false"):
            # 构造并上报消息
            mileage = prepare['original_mileage'] + 1
            publish_msg_by_kafka('journey_start_event', vehicle_status={"mileage": mileage}, clear_fields=['vehicle_status.ntester'])
            # 校验ntester 默认值为false
            ntester_in_mysql = checker.mysql.fetch('status_vehicle', {"id": vid}, ['ntester'])[0]
            assert_equal(ntester_in_mysql['ntester'], 0)

    def test_correct_re_encoding(self, prepare, mysql, checker, publish_msg_by_kafka, env, cleanup):
        vid = env['vehicles']['v_statistic_3']['vehicle_id']
        vin = env['vehicles']['v_statistic_3']['vin']
        mileage = prepare['original_mileage'] + 1
        with allure.step("从电池溯源数据库，选取nio_encoding和re_encoding"):
            battery_info = mysql['battery_trace'].fetch('sys_battery_pack_entity',
                                                        where_model={'create_time>': '2021-12-01 00:00:00'},
                                                        suffix='limit 2'
                                                        )
            nio_encoding1 = battery_info[0]['nio_encoding']
            re_encoding1 = battery_info[0]['code']
            nio_encoding2 = battery_info[1]['nio_encoding']
            re_encoding2 = battery_info[1]['code']
        with allure.step("上报形成开始事件，设置上报的国标编码不配对"):
            nextev_message, journey_start_obj = publish_msg_by_kafka('journey_start_event', vin=vin, vid=vid,
                                                                     vehicle_status={"mileage": mileage},
                                                                     battery_package_info={"btry_pak_encoding": [{
                                                                         "btry_pak_sn": 1,
                                                                         "nio_encoding": nio_encoding1,
                                                                         "re_encoding": '001PB018543883BCX2IA8O76'},
                                                                         {"btry_pak_sn": 2,
                                                                          "nio_encoding": nio_encoding2,
                                                                          "re_encoding": '001PB018543883BCX2IA8O76'}]}
                                                                     )

        with allure.step("验证mysql存储的国标编码是否纠正"):
            journey_start_obj['battery_package_info']['btry_pak_encoding'][0]['re_encoding'] = re_encoding1
            journey_start_obj['battery_package_info']['btry_pak_encoding'][1]['re_encoding'] = re_encoding2
            checker.vid = vid
            tables = ['status_btry_packs']
            checker.check_mysql_tables(journey_start_obj, tables, event_name='journey_start_event')

    def test_encoding_update_later(self, vid, prepare, publish_msg, checker, cmdopt):
        """
        https://jira.nioint.com/browse/CVS-16596 soc_status表chg_subsys_encoding字段更新问题
        https://jira.nioint.com/browse/CVS-15756 battery_package_info表电池编码更新
        :param vid:
        :param prepare:
        :param publish_msg:
        :param checker:
        :return:
        """
        with allure.step("先上报一个周期事件"):
            sample_ts = time.time()
            journey_id = round(sample_ts)
            publish_msg('periodical_journey_update', journey_id=str(journey_id))

        with allure.step("再上报行程开始事件"):
            nextev_message, journey_start_obj = publish_msg('journey_start_event',
                                                            sleep_time=2 if 'test' in cmdopt else 30,
                                                            journey_id=str(journey_id),
                                                            sample_ts=round(sample_ts*1000))

        with allure.step("验证电池编码更新"):
            btry_in_mysql = checker.mysql.fetch_one('status_btry_packs', {"id": vid})
            assert journey_start_obj['battery_package_info']['btry_pak_encoding'][0]['re_encoding'] == btry_in_mysql['re_encoding']
            assert journey_start_obj['battery_package_info']['btry_pak_encoding'][0]['nio_encoding'] == btry_in_mysql['nio_encoding']
            soc_in_mysql = checker.mysql.fetch_one('status_soc', {"id": vid})
            assert journey_start_obj['battery_package_info']['btry_pak_encoding'][0]['nio_encoding'] == soc_in_mysql['chg_subsys_encoding']