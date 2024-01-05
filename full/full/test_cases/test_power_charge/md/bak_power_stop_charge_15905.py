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
import pytest
import requests

from common.charge.utils import check_status_code
from common.log import log
from config.settings import MPC_URL, CLOUD_REALTIME_URL, PROXIES


@allure.feature("[PTCM-15905]手动停止充电")
class TestPowerBeginCharge15905:
    """
        前置条件：
            清除对应模块ACDC，BMS状态
        操作步骤：
            1.设置PLC，BMS，PDU，ACDC状态，配置充电启动
            2.UI点击停止充电
        检查：
            2.检查支路状态和充电电流数据
        备注：
    """

    @pytest.fixture(scope="class", autouse=False)
    def prepare(self, charge, charge_start):
        """

        :param charge:
        :param charge_start:
        :return:
        """
        log.info("[BEGIN]测试开发")
        # 调试使用
        """
        log.info("[STEP]清除acdc数据")
        rep = requests.get(ACDC_CLOSE_URL.format(int(charge["branch"]) - 10))
        check_status_code(rep.status_code, 200, f"ACDC仿真接口请求异常:{rep.reason}，测试Error！")
        log.info("[STEP]清除pdu数据")
        brn = int(charge["branch"]) - 10
        mod = brn // 2  # 0-4
        tmp = brn % 2  # 0, 1
        key_pos_start = 104300 if tmp == 0 else 104308
        key_neg_start = 104301 if tmp == 0 else 104309
        pos = str(key_pos_start + 14 * mod)
        neg = str(key_neg_start + 14 * mod)
        charge["pdu"][pos] = 0
        charge["pdu"][neg] = 0
        rep = requests.post(PDU_URL, json=charge["pdu"])
        check_status_code(rep.status_code, 200, f"PDU仿真接口请求异常:{rep.reason}，测试Error！")   
        log.info("[STEP]发送关闭BMS数据")
        rep = requests.get(url=BMS_CLOSE_URL.format(int(charge["branch"])))
        time.sleep(5)
        check_status_code(rep.status_code, 200, f"BMS仿真接口请求异常:{rep.reason}，测试Error！")
        log.info("[STEP]发送充电PLC数据")
        rep = requests.post(url=PLC_URL, json=charge["plc"], proxies=PROXIES)
        check_status_code(rep.status_code, 200, f"PLC仿真接口请求异常:{rep.reason}，测试Error！")
        time.sleep(15)
        log.info("[STEP]发送充电BMS数据")
        rep = requests.post(url=BMS_URL, json=charge["bms"], proxies=PROXIES)
        check_status_code(rep.status_code, 200, f"BMS仿真接口请求异常:{rep.reason}，测试Error！")
        time.sleep(20)
        log.info("[STEP]发送充电PDU数据")
        rep = requests.post(PDU_URL, json=charge["pdu"], proxies=PROXIES)
        check_status_code(rep.status_code, 200, f"PDU仿真接口请求异常:{rep.reason}，测试Error！")
        addr_start = (int(charge["branch"]) - 10) * 3
        for i in range(3):
            addr = addr_start + i
            log.info(f"[STEP]发送充电ACDC{addr}数据")
            rep = requests.post(url=ACDC_URL, json=charge[f"acdc{addr}"], proxies=PROXIES)
            check_status_code(rep.status_code, 200, f"ACDC仿真接口请求异常:{rep.reason}，测试Error！")
            time.sleep(1)
        time.sleep(60)
        """
        # 断言的数据点
        branch = charge["branch"]
        charge["charge_points"] = {}
        charge["charge_points"][f"{branch + 1}802"] = {"type": 2, "value": 0}
        charge["charge_points"][f"{branch + 1}021"] = {"type": 4, "value": 0}
        log.info("[STEP]UI停止充电")
        rep = requests.post(MPC_URL, json={"branch": branch}, proxies=PROXIES)
        check_status_code(rep.status_code, 200, f"MPC仿真接口请求异常:{rep.reason}，测试Error！")
        log.info("[STEP]UI结束停止充电")
        time.sleep(20)
        yield charge
        # 调试使用
        """
        log.info("[STEP]清除acdc数据")
        rep = requests.get(ACDC_CLOSE_URL.format(int(charge["branch"]) - 10))
        check_status_code(rep.status_code, 200, f"ACDC仿真接口请求异常:{rep.reason}，测试Error！")
        charge["pdu"] = {}
        log.info("[STEP]清除pdu继电器状态数据")
        rep = requests.post(PDU_URL, json=charge["pdu"])
        check_status_code(rep.status_code, 200, f"PDU仿真接口请求异常:{rep.reason}，测试Error！")
        log.info("[STEP]发送关闭BMS数据")
        rep = requests.get(url=BMS_CLOSE_URL.format(int(charge["branch"])))
        check_status_code(rep.status_code, 200, f"BMS仿真接口请求异常:{rep.reason}，测试Error！")
        """
        log.info("[END]测试结束")

    # @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @allure.story(f"PTCM-15905:充电关闭，检查充电支路工作状态和充电电流")
    def test_stop_charge_15905(self, prepare):
        """

        :param prepare:
        :return:
        """
        branch = prepare["branch"]
        # check_points = [f"{branch + 1}802", f"{branch + 1}021"]
        check_points = [f"{branch + 1}802", ]
        check_points_desc = ["CDC 支路工作状态", "BMS电池包总电流"]
        for i in range(len(check_points)):
            _info_msg = f"电池仓A{branch - 9}充电状态, 数据ID[{check_points[i]}], 变量名[{check_points_desc[i]}]"
            log.info(_info_msg)
            data = {
                "resource_id": prepare["station"],
                "site": "oss",
                "keys": [check_points[i]]
            }
            expect_type = prepare["charge_points"][f"{check_points[i]}"]["type"]
            expect_val = prepare["charge_points"][f"{check_points[i]}"]["value"]
            actual_type = -1
            actual_val = -1
            for j in range(10):
                log.info(f"[STEP]check point [{check_points[i]}][{check_points_desc[i]}]第{j + 1}次请求CLOUD数据")
                rep = requests.post(CLOUD_REALTIME_URL, json=data, proxies=PROXIES)
                check_status_code(rep.status_code, 200, f"Cloud仿真接口请求异常:{rep.reason}，测试Failed！")
                content = json.loads(rep.content)
                log.debug(content)
                point = content["data"]["point_data"][-1]
                typ = point.get("type", -1)
                if typ != -1:
                    actual_type = point['type']
                    actual_val = point["value"]
                    if isinstance(actual_val, float):
                        actual_val = int(actual_val)
                    if actual_val == expect_val:
                        break
                time.sleep(10)
            with allure.step(_info_msg):
                _info_msg = f"expect_type:{expect_type}, actual_type:{actual_type},expect_val:{expect_val}, actual_val:{actual_val}"
                log.info(_info_msg)
                assert expect_type == actual_type
                assert expect_val == actual_val
