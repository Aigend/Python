#!/usr/bin/env python
# coding=utf-8

"""
:Description: ecall事件上报校验
"""
import random
import time
import allure
import pytest

from nio_messages import wti
from utils.assertions import assert_equal
from utils.checker import Checker
from utils.httptool import request


class TestEcallEventMsg(object):
    def test_ecall_event(self, vid, checker, publish_msg_by_kafka):
        time.sleep(62)
        # 上报
        nextev_message, obj = publish_msg_by_kafka('ecall_event', sleep_time=4)

        # 校验
        tables = ['ecall_event']
        checker.check_mysql_tables(obj, tables, event_name='ecall_event', sample_ts=obj['sample_ts'])

    def test_tyre_alarm(self, vid, checker, publish_msg_by_kafka):
        """
        校验ecall_event表中的ecall_data.tyre_alarm会纪录所有tyre报警
        """
        time.sleep(62)
        alarm_singal_list = wti.TYRE_WIT_SIGNAL
        nextev_message, obj = publish_msg_by_kafka('ecall_event', sleep_time=4,
                                                   status={'alarm_signal': {'signal_int': alarm_singal_list}})
        tables = ['ecall_event']
        checker.check_mysql_tables(obj, tables, event_name='ecall_event', sample_ts=obj['sample_ts'])

    def test_interval_is_one_min(self, vid, checker, publish_msg_by_kafka):
        """
        校验第一次上报与第二次上报的间隔在一分钟以内时，上报数据被忽略，mysql不做存储, event_id 代表时间戳（秒计）为判定依据
        交替不同的result reason时，也有一分钟限制。
        urgt_prw_shtdwn从0变为1时，也有一分钟的限制。

        注意，当上报的event_id不以当前时间来取值时（例如取的是昨天的某两个时间点，之间相差一直有1秒），rvs认为它是补发数据，此时没有一分钟的限制。该两条数据都会落库。
        此时kafka的推送也没有一分钟限制
        """
        time.sleep(62)
        with allure.step('第一次上报，数据存储在了mysql.ecall_event中'):
            sample_ts = round(time.time() * 1000)
            nextev_message, obj = publish_msg_by_kafka('ecall_event', sample_ts=sample_ts, event_id=sample_ts, sleep_time=4)
            ecall_event_in_mysql_first =  checker.mysql.fetch('ecall_event', {"vehicle_id": vid, "event_id": obj['event_id'] // 1000})
            assert_equal(len(ecall_event_in_mysql_first), 1)

        with allure.step('第二次上报，距离第一次的时间小于一分钟，数据不存储在了mysql中'):
            sample_ts = sample_ts+3*1000
            # 第二次上报比第一次间隔3秒
            nextev_message, obj = publish_msg_by_kafka('ecall_event',  sample_ts=sample_ts, event_id=sample_ts, sleep_time=4)
            ecall_event_in_mysql_second =  checker.mysql.fetch('ecall_event', {"vehicle_id": vid, "event_id": obj['event_id'] // 1000})
            assert_equal(len(ecall_event_in_mysql_second), 0)

    def test_window_status_rule(self, env, cmdopt, api, publish_msg_by_kafka):
        with allure.step('校验ES6遵循新的车窗状态映射规则'):
            vin = env['vehicles']['v_ES6']['vin']
            vid = env['vehicles']['v_ES6']['vehicle_id']
            status = {
                "window_status": {
                    "sun_roof_positions": {
                        "sun_roof_posn": random.choice([random.randint(0, 102), 127])
                    }
                }
            }
            time.sleep(62)
            # 上报
            nextev_message, obj = publish_msg_by_kafka('ecall_event', vin=vin, vid=vid, sleep_time=4, status=status)

            # 校验
            tables = ['ecall_event']
            checke_ES6 = Checker(vid=vid, vin=vin, cmdopt=cmdopt, env=env, api=api)
            checke_ES6.check_mysql_tables(obj, tables, event_name='ecall_event', sample_ts=obj['sample_ts'])

        with allure.step('校验新款ES8遵循新的车窗状态映射规则'):
            vin = env['vehicles']['v_new_ES8']['vin']
            vid = env['vehicles']['v_new_ES8']['vehicle_id']
            status = {
                "window_status": {
                    "sun_roof_positions": {
                        "sun_roof_posn": random.choice([random.randint(0, 102), 127])
                    }
                }
            }
            time.sleep(62)
            # 上报
            nextev_message, obj = publish_msg_by_kafka('ecall_event', vin=vin, vid=vid, sleep_time=4, status=status)

            # 校验
            tables = ['ecall_event']
            checke_ES8 = Checker(vid=vid, vin=vin, cmdopt=cmdopt, env=env, api=api)
            checke_ES8.check_mysql_tables(obj, tables, event_name='ecall_event', sample_ts=obj['sample_ts'])

        with allure.step('校验EC6遵循新的车窗状态映射规则'):
            vin = env['vehicles']['EC6']['vin']
            vid = env['vehicles']['EC6']['vehicle_id']
            status = {
                "window_status": {
                    "sun_roof_positions": {
                        "sun_roof_posn": random.choice([random.randint(0, 102), 127])
                    }
                }
            }
            time.sleep(62)
            # 上报
            nextev_message, obj = publish_msg_by_kafka('ecall_event', vin=vin, vid=vid, sleep_time=4, status=status)

            # 校验
            tables = ['ecall_event']
            checke_ES6 = Checker(vid=vid, vin=vin, cmdopt=cmdopt, env=env, api=api)
            checke_ES6.check_mysql_tables(obj, tables, event_name='ecall_event', sample_ts=obj['sample_ts'])

    @pytest.mark.marcopolo_skip
    @pytest.mark.skip('manual')
    def test_sms(self,kafka,env):
        """
        SMS流程:  车--(短信)-->移动---->联想--(API)-->MNO--(kafka)-->rvs_server


        API:

            curl -X POST 'https://tsp-test.nioint.com/api/1/in/mno/push/text_message?app_id=80001&timestamp=1592470898&sign=255fa168264d735c053edc66da73ed54' \
            -H 'Content-Type:application/x-www-form-urlencoded' \
            -d 'send_msisdn=0120120123&sms_id=123456&target_msisdn=1234&sms_content=AwABAJco614BAXK0AQAAAMmmyUFAkdxCuAAAAAAAJwCdAQAAVQFlAAAAAAAAAAAA&push_date=2020-06-18 12:23:36'

            DOC：http://showdoc.nevint.com/index.php?s=/mno&page_id=9308
            数据库 mno_test.text_message表存入数据

        kafka:
            mno往topic：swc-cvs-mno-${env}-push里面写入消息，rvs_server解析数据中的sms_content，存入ecall_event表中

        注意：
         sms通道上报数据要写mysql的status_*表，而MQTT通道不用

        """
        vid='9347f56bb63e4af190c1cfe744f8c45e'
        with allure.step('验证往mno的topic里面写入消息，解析数据中的content，存入ecall_event，status_position,status_door,status_window,status_soc,status_vehicle表中'):
            http = {
                "host": 'https://tsp-test.nioint.com',
                "uri": "/api/1/in/mno/push/text_message",
                "method": "POST",
                "headers": {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                "params": {
                    "app_id": '80001',
                },
                "data": {
                    'target_msisdn': '123456',
                    # 其中send_msisdn为车辆的msisdn，通过这个值可以查到车辆的vid等信息。vehicle_profile里可看到该值。
                    'send_msisdn': '484721',
                    'sms_id': '123456',
                    # 注意，content里有个时间戳，每次报的content都要是比上次更新的，可以从prod环境找
                    # http://kibana-prod.csapi.cn:5601/app/kibana#/discover?_g=(refreshInterval:(display:Off,pause:!f,value:0),time:(from:now%2Fd,mode:quick,to:now%2Fd))&_a=(columns:!(_source),index:AW5YesUVodGBP02YGkqJ,interval:auto,query:(query_string:(analyze_wildcard:!t,query:send_msisdn)),sort:!('@timestamp',desc))
                    # https://confluence.nioint.com/display/CVS/Advanced+E-Call?preview=/20712280/362222399/NIO-SRD-SWC-AdvancedECall-v0.4.pdf
                    # 根据ecall文档的描述新增reason code类型EDA，以下便是
                    'sms_content': 'AwABAKrkrWABAShaQAAAAAAAAAAAAAAAAAAAAAAAAAB8IwAAFQB/fwAAAAAAAAAA',
                    'push_date': '2021-05-25 12:23:36',
                },
                "expect": {
                    "data": {

                    },
                    "success": 1,
                    "failure": 0,
                    "result_code": "success",
                }
            }

        response = request(http['method'], url=http['host'] + http['uri'],
                      params=http['params'], data=http['data'], headers=http['headers']).json()

