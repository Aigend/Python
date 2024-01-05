#!/usr/bin/env python
# coding=utf-8

"""
:file: test_charge_start_event_mysql.py
:author: chunming.liu
:Date: Created on 2019/1/11
:Description: 充电开始事件，包含电池数据
"""
import time
import json
import allure
import pytest

from utils import time_parse


@pytest.mark.test
class TestResetLoginSn(object):

    @pytest.mark.parametrize("event_name", ['journey_start_event', 'charge_start_event'])
    def test_reset_login_sn(self, event_name, env, mysql, publish_msg_by_kafka, api, cassandra):
        """
        校验调用evm notify接口后，再次报charge/journey start事件时，平台收到的login_s_n会被重置为1
        """
        vin = env['vehicles']['gb_public']['vin']
        vid = env['vehicles']['gb_public']['vehicle_id']
        attribution = env['vehicles']['gb_public']['attribution']

        with allure.step('第一次上报，获得sh和gb的初始login_s_n'):
            nextev_message, obj = publish_msg_by_kafka(event_name, vin=vin, vid=vid)
            time.sleep(2)
            login_s_n_mock = self.get_mock_login_s_n(obj, vin, attribution, cassandra, mysql)
            # orig_sh_login_s_n =  login_s_n_mock['sh_login_s_n']
            orig_gb_login_s_n = login_s_n_mock['gb_login_s_n']

        with allure.step('第二次上报，验证sh和gb的login_s_n都自增1'):
            nextev_message, obj = publish_msg_by_kafka(event_name, vin=vin, vid=vid)
            time.sleep(2)
            login_s_n_mock = self.get_mock_login_s_n(obj, vin, attribution, cassandra, mysql)
            # assert login_s_n_mock['sh_login_s_n'] == orig_sh_login_s_n + 1
            assert login_s_n_mock['gb_login_s_n'] == orig_gb_login_s_n + 1
        

        # with allure.step('将sh的login_sn重置'):
        #     events= [
        #         {
        #             "type": "reset_login_sn",
        #             "sns": [
        #                 {
        #                     "attribution": attribution,
        #                     "domain": 'private',
        #                     "vin": vin
        #                 }
        #             ]
        #         }
        #     ]
        #     evm_nofify_api(cmdopt=cmdopt, events=events)


        with allure.step('第三次上报，验证sh收到的message 的login_sn重置为1,同时gb收到的message login_s_n自增1'):
            nextev_message, obj = publish_msg_by_kafka(event_name, vin=vin, vid=vid)
            time.sleep(2)
            login_s_n_mock = self.get_mock_login_s_n(obj, vin, attribution, cassandra, mysql)
            # assert login_s_n_mock['sh_login_s_n'] == 1
            assert login_s_n_mock['gb_login_s_n'] == orig_gb_login_s_n + 2


        with allure.step('第四次上报，验证sh收到的message 的login_sn为2,同时gb收到的message login_s_n自增1'):
            nextev_message, obj = publish_msg_by_kafka(event_name, vin=vin, vid=vid)
            time.sleep(2)
            login_s_n_mock = self.get_mock_login_s_n(obj, vin, attribution, cassandra, mysql)
            # assert login_s_n_mock['sh_login_s_n'] == 2
            assert login_s_n_mock['gb_login_s_n'] == orig_gb_login_s_n + 3


    def get_mock_login_s_n(self, obj, vin, attribution, cassandra, mysql):
        insert_date = time_parse.utc_to_local(timestamp=obj['sample_ts'] / 1000.0, offset_hour=8)
        sample_ts = cassandra['datacollection'].fetch('evm_message',
                                                                        {'vin': vin,
                                                                         'insert_date': insert_date,
                                                                         'attribution': attribution
                                                                         },
                                                                        [
                                                                         "blobAsBigint(timestampAsBlob(sample_ts)) as sample_ts",

                                                                         ]
                                                                        )[-1]['sample_ts']//1000
        sh_message_mock_server = mysql['rvs'].fetch('vehicle_data_mock',
                                                    {"vin": vin,
                                                     "sample_time": time_parse.time_sec_to_strtime(sample_ts),
                                                     "attribution": attribution
                                                     }
                                                    )[0]

        gb_message_mock_server = mysql['rvs'].fetch('vehicle_data_mock',
                                                    {"vin": vin,
                                                     "sample_time": time_parse.time_sec_to_strtime(sample_ts),
                                                     "attribution": '156'
                                                     }
                                                    )[0]

        # sh_login_s_n_mock = int(json.loads(sh_message_mock_server['message'])['dataUnit']['loginSN'])
        gb_login_s_n_mock = int(json.loads(gb_message_mock_server['message'])['dataUnit']['loginSN'])

        return {'gb_login_s_n': gb_login_s_n_mock}

