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
from common.charge.utils import check_status_code, deal_receive_data
from config.settings import PLC_URL, BMS_URL, BMS_CLOSE_URL, ACDC_URL, ACDC_CLOSE_URL, PDU_URL, CLOUD_REALTIME_URL, \
    PROXIES, MPC_URL


def check_complete_charge_branch_info(prepare, msg):
    """

    :param prepare:
    :param msg:
    :return:
    """
    branch = prepare["branch"]
    check_points_desc = {f"{branch + 1}802": "CDC 支路工作状态", f"{branch + 1}021": "BMS电池包总电流"}
    for k, v in prepare["charge_points"].items():
        _info_msg = f"电池仓A{branch - 9}充电状态, 数据ID[{k}], 变量名[{check_points_desc[k]}]"
        log.info(_info_msg)
        data = {
            "resource_id": prepare["station"],
            "site": "oss",
            "keys": [k, ]
        }
        expect_type = prepare["charge_points"][f"{k}"]["type"]
        expect_val = prepare["charge_points"][f"{k}"]["value"]
        actual_type = -1
        actual_val = -1
        for j in range(10):
            log.info(f"[STEP][{msg}]check point [{k}] 第{j + 1}次请求CLOUD数据")
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


@allure.feature("不同类型电池完整充电")
class TestPowerCompleteCharge15906:
    """
        检查：不同类型电池完整充电
        充电结束类型：电池上报充满状态
    """

    @pytest.fixture(scope="class", autouse=False)
    def prepare(self, charge):
        """

        :param charge:
        :return:
        """
        log.info("[BEGIN]测试开发")
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
        time.sleep(20)
        yield charge
        log.info("[STEP]清除acdc数据")
        rep = requests.get(ACDC_CLOSE_URL.format(int(charge["branch"]) - 10))
        check_status_code(rep.status_code, 200, f"ACDC仿真接口请求异常:{rep.reason}，测试Error！")
        time.sleep(2)
        charge["pdu"] = {}
        log.info("[STEP]清除pdu继电器状态数据")
        rep = requests.post(PDU_URL, json=charge["pdu"])
        check_status_code(rep.status_code, 200, f"PDU仿真接口请求异常:{rep.reason}，测试Error！")
        time.sleep(2)
        log.info("[END]测试结束")

    # @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @allure.story(f"充电开启和结束，检查充电支路工作状态和充电电流")
    def test_complete_charge_15906(self, prepare):
        """

        :param prepare:
        :return:
        """
        log.info(f"[STEP]检查开启充电状态")
        branch = prepare["branch"]
        prepare["charge_points"] = {}
        prepare["charge_points"][f"{branch + 1}802"] = {"type": 2, "value": 1}
        prepare["charge_points"][f"{branch + 1}021"] = {"type": 4, "value": -14}
        check_complete_charge_branch_info(prepare, "开启充电")
        branch = prepare["branch"]
        bms_data = deal_receive_data(prepare["bms"], {})
        bms_battery_pack_cap = int(bms_data[f"{branch + 1}012"])
        # 75度的3个月就会进行满充 充电到100%
        if bms_battery_pack_cap == 8:
            log.info("[STEP]UI停止充电")
            rep = requests.post(MPC_URL, json={"branch": branch}, proxies=PROXIES)
            check_status_code(rep.status_code, 200, f"MPC仿真接口请求异常:{rep.reason}，测试Error！")
        else:
            log.info(f"[STEP]BMS上报充电完成")
            prepare["bms"] = {
                f"bms{int(branch)}": {
                    f"{int(branch) + 1}508": 2  # 100度电池上报充电完成
                }
            }
            rep = requests.post(url=BMS_URL, json=prepare["bms"], proxies=PROXIES)
            check_status_code(rep.status_code, 200, f"BMS仿真接口请求异常:{rep.reason}，测试Error！")
        time.sleep(20)  # 结束
        log.info(f"[STEP]检查结束充电状态")
        prepare["charge_points"][f"{branch + 1}802"] = {"type": 2, "value": 2}
        prepare["charge_points"].pop(f"{branch + 1}021")
        check_complete_charge_branch_info(prepare, "结束充电")
