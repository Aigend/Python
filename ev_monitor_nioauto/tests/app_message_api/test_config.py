#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/07 19:13
@contact: li.liu2@nio.com
@description:
    config_update http://${hostname}/api/1/in/message/config_update
    Config Reload http://${hostname}/api/1/in/message/config_reload
    Config Delete http://${hostname}/api/1/in/message/config_delete

"""

import allure
import pytest

from utils.assertions import assert_equal
from utils.httptool import request as rq


class TestMeesageAPI(object):
    @pytest.fixture(scope='class', autouse=False)
    def prepare(self, env, mysql):
        data = {}

        data['host_app'] = env['host']['app']
        data['host_app_in'] = env['host']['app_in']
        user = 'nmp'
        data['app_id_phone'] = '10002' if user == 'li' else '10001'  # 10001 andriod， 10002 ios
        data['account_id'] = env['vehicles'][user]['account_id']
        data['phone'] = env['vehicles'][user]['phone']
        data['client_id'] = env['vehicles'][user]['client_id']
        data['client_id_app'] = env['vehicles'][user][f'client_id_app_{data["app_id_phone"]}']
        data['authorization'] = env['vehicles'][user][f'token_{data["app_id_phone"]}']
        data['device_id_app'] = env['vehicles'][user]['device_id_app']
        data['vehicle_id'] = env['vehicles'][user]['vehicle_id']
        data['app_version'] = mysql['nmp_app'].fetch('clients', {'client_id': data['client_id_app'], 'app_id': data['app_id_phone']})[0]['app_version']
        # data['app_version'] = '3.10.1' #hognzhenbi
        # data['app_version'] = '3.9.9' #liliu
        return data

    @pytest.mark.skip('manual')
    def test_config(self):
        """
        config_update http://${hostname}/api/1/in/message/config_update
        Config Reload http://${hostname}/api/1/in/message/config_reload
        Config Delete http://${hostname}/api/1/in/message/config_delete

        :return:
        """


def check_response(response, http):
    with allure.step('校验response'):
        response.pop('request_id', '')
        response.pop('server_time', '')
        assert_equal(response, http['expect'])
