#!/usr/bin/env python
# coding=utf-8
import json
import time
import allure
import pytest

from utils.logger import logger
from utils.assertions import assert_equal
from utils.httptool import request as req


@pytest.mark.test
class TestRepairEvent(object):
    # @pytest.fixture(scope='class', autouse=True)
    # def prepare(self, cmdopt, request):
    #     with allure.step('使车辆在线'):
    #         params = {
    #             'vid': '46c416a9f7c4458ba7fca9973c168bb5',
    #             'ecu': 'cgw',
    #             'env': cmdopt
    #         }
    #         r = req('POST', url="http://10.110.3.103:5000/vcontrol/mqtt_connect", params=params, timeout=5.0)
    #         response = r.json()["result_code"]
    #         logger.info(f"mqtt connection status is {response}")
    #     def fin():
    #         with allure.step('使车辆离线'):
    #             r = req('POST', url="http://10.110.3.103:5000/vcontrol/mqtt_disconnect", params=params, timeout=5.0)
    #             response = r.json()["result_code"]
    #             logger.info(f"mqtt disconnection status is {response}")
    #
    #     request.addfinalizer(fin)
    # TODO 马克波罗服务暂不支持，先跳过
    @pytest.mark.marcopolo_skip
    @pytest.mark.parametrize("status", [5, 10], ids=['repair start', 'repair end'])
    def test_repair(self, env, cmdopt, kafka, redis, status, mysql):
        """
        Artemis Kafka: http://showdoc.nevint.com/index.php?s=/222&page_id=10010 (密码：artemis)
        """
        # ts = 1552461827
        ts = int(time.time())
        vid = env['vehicles']['vehicle_for_repair']['vehicle_id']

        vehicle_repair_order = json.dumps({
            "owner_phone": "13761473462", "order_status_name": "维修开始" if status == 5 else "维修结束", "som_order_no": "BSHHB00020180720001113",
            "account_id": "1112538414", "receipt_type": "", "booking_order_no": "BSHHB00020180720001113",
            "order_status_code": str(status), "update_at": ts, "ro_no": "BSHHB00020180720001113", "update_by": "用户代表",
            "vehicle_id": vid,
            "order_type": "101210034", "timestamp": ts, "status": status,
            "repair_order_no": "BSHHB00020180720001113"
        })

        kafka['do'].produce(kafka['topics']['repair'], vehicle_repair_order)

        with allure.step("校验当有维修工单时，status=5/10代表维修开始/结束 Redis中SpecialStatus会记录repair，和repair_time"):
            # 等待rvs 处理
            time.sleep(5)
            special_status = json.loads(redis['cluster'].get(f'remote_vehicle_test:vehicle_status:{vid}:SpecialStatus'))

            repaired_in_order = 1 if status == 5 else 0
            assert_equal(special_status['repaired'], repaired_in_order)
            assert_equal(special_status['repair_sample_time'], ts)

    # TODO 马克波罗服务暂不支持，先跳过
    @pytest.mark.marcopolo_skip
    @pytest.mark.parametrize("status", [5, 10], ids=['decorate start', 'decorate end'])
    def test_decorate(self, env, cmdopt, kafka, redis, status, mysql):
        """
        ro_type为20201005 且business_type为21201002 的时候，该服务单是进行美容装潢业务，不需要进维修模式
        但是可以关闭该工单
        """
        ts = int(time.time())
        vid = env['vehicles']['vehicle_for_repair']['vehicle_id']

        vehicle_repair_order = json.dumps({
            "owner_phone": "13761473462", "order_status_name": "维修开始" if status == 5 else "维修结束", "som_order_no": "BSHHB00020180720001113",
            "account_id": "1112538414", "receipt_type": "", "booking_order_no": "BSHHB00020180720001113",
            "order_status_code": str(status), "update_at": ts, "ro_no": "BSHHB00020180720001113", "update_by": "用户代表",

            "ro_type": 20201005, "business_type": 21201002,

            "vehicle_id": vid,
            "order_type": "101210034", "timestamp": ts, "status": status,
            "repair_order_no": "BSHHB00020180720001113"
        })

        kafka['do'].produce(kafka['topics']['repair'], vehicle_repair_order)

        with allure.step("校验当有装潢工单时，不开启维修模式，Redis中SpecialStatus会记录repair，和repair_time"):
            # 等待rvs 处理
            time.sleep(5)
            special_status = json.loads(redis['cluster'].get(f'remote_vehicle_test:vehicle_status:{vid}:SpecialStatus'))

            assert_equal(special_status['repaired'], 0)
            assert_equal(special_status['repair_sample_time'] != ts, True)

    # TODO 马克波罗服务暂不支持，先跳过
    @pytest.mark.marcopolo_skip
    @pytest.mark.parametrize("status", [5, 10], ids=['battery repair start', 'battery repair end'])
    def test_battery_repair(self, env, cmdopt, kafka, redis, status, mysql):
        """
        ro_type为20201005 且business_type为21201002 的时候，该服务单是进行美容装潢业务，不需要进维修模式
        但是可以关闭该工单
        """
        ts = int(time.time())
        vid = env['vehicles']['vehicle_for_repair']['vehicle_id']

        vehicle_repair_order = json.dumps({
            "owner_phone": "13761473462", "order_status_name": "维修开始" if status == 5 else "维修结束", "som_order_no": "BSHHB00020180720001113",
            "account_id": "1112538414", "receipt_type": "", "booking_order_no": "BSHHB00020180720001113",
            "order_status_code": str(status), "update_at": ts, "ro_no": "BSHHB00020180720001113", "update_by": "用户代表",

            "ro_type": 20201009,

            "vehicle_id": vid,
            "order_type": "101210034", "timestamp": ts, "status": status,
            "repair_order_no": "BSHHB00020180720001113"
        })

        kafka['do'].produce(kafka['topics']['repair'], vehicle_repair_order)

        with allure.step("校验当有装潢工单时，不开启维修模式，Redis中SpecialStatus会记录repair，和repair_time"):
            # 等待rvs 处理
            time.sleep(5)
            special_status = json.loads(redis['cluster'].get(f'remote_vehicle_test:vehicle_status:{vid}:SpecialStatus'))

            assert_equal(special_status['repaired'], 0)
            assert_equal(special_status['repair_sample_time'] != ts, True)

