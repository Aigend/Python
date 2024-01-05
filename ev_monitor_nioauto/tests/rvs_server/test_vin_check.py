#!/usr/bin/env python
# coding=utf-8

"""
:file: test_vin_check.py
:author: muhan.chen
:Date: Created on 2018/10/8
:Description: 对车辆VIN码进行校验
"""

import string, random, pytest
# from utils.vin_check import *
# from messages import pbjson, charge_start_event
# from utils.kafka_client import *
# # from test.base import message_formator_old, cassandra_formator_old, mysql_formator_old
# # from utils.format_message import *
# import requests

pytest.mark.skip('TODO refactor')
class TestVinCheck(object):
    pass
    # @pytest.fixture(scope='function', autouse=True)
    # def prepare(self):
    #     # vid = ''.join(random.sample(string.ascii_lowercase + string.digits, 32))
    #     vin = check()
    #     params = {
    #         'env': 'test',
    #         'vin': vin,
    #         'types': '["CGW"]'
    #     }
    #     url = 'http://10.110.0.151:8080/api/1/browndragon/vehicle'
    #     response = requests.request("GET", url, params=params).json()
    #     log('INFO', 'response is:\n{0}'.format(response))
    #     vid = response['vid']
    #     return {'vid': vid, 'vin': vin}
    #
    # def test_vin_check(self, prepare, mysql, cmdopt):
    #     ################################
    #     # 构造并上报消息
    #     ################################
    #     log('INFO', 'vid is :\n{0}'.format(prepare['vid']))
    #     log('INFO', 'vin is:\n{0}'.format(prepare['vin']))
    #     charge_start_message = charge_start_event.generate_message(prepare['vin'])[1]
    #     charge_start_obj = pbjson.pb2dict(charge_start_message)
    #     log('INFO', 'charge_start_obj is:\n{0}'.format(show_json(charge_start_obj)))
    #     product('charge_start_event', charge_start_message, prepare['vid'], envir=cmdopt)
    #     time.sleep(5)
    #
    #     #################################
    #     # 查询数据库
    #     #################################
    #     vehicle_profile_in_mysql = mysql['rvs'].fetch('vehicle_profile',
    #                                                   {"id": prepare['vid']
    #                                                    },
    #                                                   )[0]
    #     log('INFO', 'vehicle_profile_in_mysql is:\n{0}'.format(show_json(vehicle_profile_in_mysql)))
    #
    #     ###############################
    #     # 校验profile表
    #     ###############################
    #     with allure.step("1、校验 vehicle_profile 存入 vehicle_profile_in_mysql"):
    #         allure.attach('vehicle_profile_in_mysql', show_json(vehicle_profile_in_mysql))
    #         allure.attach('vehicle_profile_vid', show_json(prepare['vin']))
    #         if not vehicle_profile_in_mysql:
    #             assert 0, "No record in mysql"
    #         else:
    #             assert vehicle_profile_in_mysql['vin'] == prepare['vin']
    #             assert vehicle_profile_in_mysql['iccid'] == 'ICC' + prepare['vin']
    #             assert vehicle_profile_in_mysql['id'] == prepare['vid']


