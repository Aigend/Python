""" 
@author:dun.yuan
@time: 2022/5/18 11:30 AM
@contact: dun.yuan@nio.com
@description: 激活和反激活时打快照
@showdoc：http://showdoc.nevint.com/index.php?s=/poseidon&page_id=17284
"""
import time
import json
import allure
import pytest

from utils.time_parse import timestamp_to_utc_strtime


@pytest.mark.test
class TestActiveCarSnapShot(object):
    def test_active_car_snapshot(self, env, kafka, checker):
        with allure.step("推送车辆激活信息"):
            data = {
                "msg_id": "abc",
                "type": "activation",
                "vehicle_id": env['vehicles']['v_expired']['vehicle_id'],
                "account_id": "100001",
                "car_order_no": "80000",
                "vin": env['vehicles']['v_expired']['vin'],
                "timestamp": round(time.time()),
                "baas_code": 0,
                "order_type": "1",
                "first_activation_time": 1520998380
            }
            kafka['comn'].produce(kafka['topics']['admin_change'], json.dumps(data))

        with allure.step("验证生成快照信息存库"):
            snap = checker.mysql_rvs_data.fetch_one('vehicle_snapshot',
                                                    {'vehicle_id': data['vehicle_id'],
                                                     'create_time>=': timestamp_to_utc_strtime((data['timestamp']-1)*1000)})
            assert snap['scenario'] == 'activation'
            assert snap['app_id'] == 80001

        with allure.step("推送车辆反激活信息"):
            time.sleep(2)
            data = {
                "msg_id": "abc",
                "type": "deactivation",
                "vehicle_id": env['vehicles']['v_expired']['vehicle_id'],
                "account_id": "100001",
                "car_order_no": "80000",
                "vin": env['vehicles']['v_expired']['vin'],
                "timestamp": round(time.time()),
            }
            kafka['comn'].produce(kafka['topics']['admin_change'], json.dumps(data))

        with allure.step("验证生成快照信息存库"):
            snap = checker.mysql_rvs_data.fetch_one('vehicle_snapshot',
                                                    {'vehicle_id': data['vehicle_id'],
                                                     'create_time>=': timestamp_to_utc_strtime((data['timestamp']-1)*1000)})
            assert snap['scenario'] == 'deactivation'
            assert snap['app_id'] == 80001

