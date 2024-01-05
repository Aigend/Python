"""
@Author: wenlong.jin
@File: test_charge.py
@Project: full
@Time: 2023/10/25 15:02
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
import allure
import requests
import pytest

from common.log import log
from common.charge.utils import check_status_code
from config.settings import PLC_URL, BMS_URL, BMS_CLOSE_URL, ACDC_URL, ACDC_CLOSE_URL, PDU_URL, CLOUD_REALTIME_URL, PROXIES


@allure.feature("[PTCM-15908]不同类型电池柔性充电")
class TestPowerFlexibleCharge15908:
    """
        检查：充电开始服务小结云端上传
        充电结束类型：关闭ACDC，PDU异常退出
    """
    @pytest.fixture(scope="class", autouse=False)
    def prepare(self, charge):
        """

        :param charge:
        :return:
        """
        log.info("[BEGIN]测试开发")
        timestamp = int(time.time() * 1000)
        log.info(f"测试的时间:{timestamp}")
        log.info("[STEP]发送关闭BMS数据")
        rep = requests.get(url=BMS_CLOSE_URL.format(int(charge["branch"])))
        time.sleep(20)
        check_status_code(rep.status_code, 200, f"BMS仿真接口请求异常:{rep.reason}，测试Error！")
        log.info("[STEP]发送充电PLC数据")
        rep = requests.post(url=PLC_URL, json=charge["plc"], proxies=PROXIES)
        check_status_code(rep.status_code, 200, f"PLC仿真接口请求异常:{rep.reason}，测试Error！")
        time.sleep(5)
        log.info("[STEP]发送充电BMS数据")
        rep = requests.post(url=BMS_URL, json=charge["bms"], proxies=PROXIES)
        check_status_code(rep.status_code, 200, f"BMS仿真接口请求异常:{rep.reason}，测试Error！")
        time.sleep(5)
        log.info("[STEP]发送充电PDU数据")
        charge["pdu"]["104348"] = 1
        charge["pdu"]["104349"] = 1
        rep = requests.post(PDU_URL, json=charge["pdu"], proxies=PROXIES)
        check_status_code(rep.status_code, 200, f"PDU仿真接口请求异常:{rep.reason}，测试Error！")
        addr_start = (int(charge["branch"]) - 10) * 3
        for i in range(6):
            addr = addr_start + i
            log.info(f"[STEP]发送充电ACDC{addr}数据")
            rep = requests.post(url=ACDC_URL, json=charge[f"acdc{addr}"], proxies=PROXIES)
            check_status_code(rep.status_code, 200, f"ACDC仿真接口请求异常:{rep.reason}，测试Error！")
            time.sleep(1)
        time.sleep(20)
        # 断言的数据点
        branch = charge["branch"]
        charge["charge_points"] = {}
        charge["charge_points"][f"{branch + 1}802"] = {"type": 2, "value": 1}
        charge["charge_points"][f"{branch + 1}021"] = {"type": 4, "value": -14}
        for i in range(600):
            time.sleep(1)
            print(f"debug {i}")
        yield charge
        log.info("[STEP]清除acdc数据")
        rep = requests.get(ACDC_CLOSE_URL.format(int(charge["branch"]) - 10))
        check_status_code(rep.status_code, 200, f"ACDC仿真接口请求异常:{rep.reason}，测试Error！")
        charge["pdu"] = {}
        log.info("[STEP]清除pdu继电器状态数据")
        rep = requests.post(PDU_URL, json=charge["pdu"])
        check_status_code(rep.status_code, 200, f"PDU仿真接口请求异常:{rep.reason}，测试Error！")
        log.info("[END]测试结束")

    # @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_flexible_charge(self, prepare):
        """

        :param prepare:
        :return:
        """
        pass
        # branch = prepare["branch"]
        # check_points = [f"{branch + 1}802", f"{branch + 1}021"]
        # check_points_desc = ["CDC 支路工作状态", "BMS电池包总电流"]
        # for i in range(len(check_points)):
        #     _info_msg = f"电池仓A{branch - 9}充电状态, 数据ID[{check_points[i]}], 变量名[{check_points_desc[i]}]"
        #     log.info(_info_msg)
        #     data = {
        #         "resource_id": prepare["station"],
        #         "site": "oss",
        #         "keys": [check_points[i]]
        #     }
        #     point = {
        #         "key": check_points[i],
        #         'type': -1,
        #         'value': -1
        #     }
        #     for j in range(3):
        #         log.info(f"[STEP]check point [{check_points[i]}] 第{j + 1}次请求CLOUD数据")
        #         rep = requests.post(CLOUD_REALTIME_URL, json=data, proxies=PROXIES)
        #         check_status_code(rep.status_code, 200, f"Cloud仿真接口请求异常:{rep.reason}，测试Failed！")
        #         content = json.loads(rep.content)
        #         log.debug(content)
        #         point = content["data"]["point_data"][-1]
        #         typ = point.get("type", -1)
        #         if typ != -1:
        #             break
        #         time.sleep(15)
        #     with allure.step(_info_msg):
        #         expect_type = prepare["charge_points"][f"{check_points[i]}"]["type"]
        #         expect_val = prepare["charge_points"][f"{check_points[i]}"]["value"]
        #         actual_type = point['type']
        #         actual_val = point["value"]
        #         assert expect_type == actual_type
        #         if isinstance(actual_val, float):
        #             actual_val = int(actual_val)
        #         _info_msg = f"expect_type:{expect_type}, actual_type:{actual_type},expect_val:{expect_val}, actual_val:{actual_val}"
        #         log.info(_info_msg)
        #         assert expect_val == actual_val
