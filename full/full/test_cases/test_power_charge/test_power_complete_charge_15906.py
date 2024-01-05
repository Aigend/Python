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

from common.charge.utils import check_status_code, deal_receive_data
from common.log import log
from config.settings import BMS_URL, CLOUD_REALTIME_URL, PROXIES, MPC_URL


def check_complete_charge_branch_info(prepare, msg):
    """

    :param prepare:
    :param msg:
    :return:
    """
    branch = prepare["branch"]
    check_points_desc = {f"{branch + 1}802": "CDC 支路工作状态", f"{branch + 1}021": "BMS电池包总电流"}
    for k, v in prepare["charge_points"].items():
        _info_msg = f"[STEP][BMS{branch}]电池仓A{branch - 9}充电状态, 数据ID[{k}], 变量名[{check_points_desc[k]}]"
        log.info(_info_msg)
        data = {
            "resource_id": prepare["station"],
            "site": "oss",
            "keys": [k, ]
        }
        content = ""
        expect_type = prepare["charge_points"][f"{k}"]["type"]
        expect_val = prepare["charge_points"][f"{k}"]["value"]
        actual_type = -1
        actual_val = -1
        for j in range(6):
            log.info(f"[STEP][BMS{branch}][{msg}]check point [{k}] 第{j + 1}次请求CLOUD数据")
            rep = requests.post(CLOUD_REALTIME_URL, json=data, proxies=PROXIES)
            check_status_code(rep.status_code, 200, f"Cloud仿真接口请求异常:{rep.reason}，测试Failed！")
            content = json.loads(rep.content)
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
        log.debug(content)
        with allure.step(_info_msg):
            _info_msg = f"[STEP][BMS{branch}]expect_type:{expect_type}, actual_type:{actual_type},expect_val:{expect_val}, actual_val:{actual_val}"
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
    def prepare(self, charge, charge_start):
        """

        :param charge:
        :param charge_start:
        :return:
        """
        branch = charge["branch"]
        log.info(f"[BEGIN][BMS{branch}]测试开发")
        yield charge
        log.info(f"[END][BMS{branch}]测试结束")

    # @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @allure.story(f"充电开启和结束，检查充电支路工作状态和充电电流")
    def test_complete_charge_15906(self, prepare):
        """

        :param prepare:
        :return:
        """
        branch = prepare["branch"]
        log.info(f"[STEP][BMS{branch}]检查开启充电状态")
        bms_data = deal_receive_data(prepare["bms"], {})
        bms_battery_pack_cap = int(bms_data[f"{branch + 1}012"])
        # 75度的3个月就会进行满充 充电到100%
        branch_work_status = 3 if bms_battery_pack_cap == 8 else 1
        prepare["charge_points"] = {}
        prepare["charge_points"][f"{branch + 1}802"] = {"type": 2, "value": branch_work_status}
        prepare["charge_points"][f"{branch + 1}021"] = {"type": 4, "value": -14}
        check_complete_charge_branch_info(prepare, "开启充电")
        time.sleep(10)
        bms_data = deal_receive_data(prepare["bms"], {})
        bms_battery_pack_cap = int(bms_data[f"{branch + 1}012"])
        # 75度的3个月就会进行满充 充电到100%
        if bms_battery_pack_cap in [8, 1, 3]:
            log.info(f"[STEP][BMS{branch}]UI停止充电")
            rep = requests.post(MPC_URL, json={"branch": branch}, proxies=PROXIES)
            check_status_code(rep.status_code, 200, f"MPC仿真接口请求异常:{rep.reason}，测试Error！")
            branch_work_status = 0  # 0-空闲；1-充电中；2-充电完成；3-满充中；4-放电中；5-放电完成
        else:
            log.info(f"[STEP][BMS{branch}]上报充电完成")
            prepare["bms"] = {
                f"bms{int(branch)}": {
                    f"{int(branch) + 1}521": 3,  # C1# BMSCntctrSts
                    f"{int(branch) + 1}508": 2  # 100度电池上报充电完成
                }
            }
            rep = requests.post(url=BMS_URL, json=prepare["bms"], proxies=PROXIES)
            check_status_code(rep.status_code, 200, f"BMS仿真接口请求异常:{rep.reason}，测试Error！")
            branch_work_status = 2
        time.sleep(20)  # 结束
        log.info(f"[STEP][BMS{branch}]检查结束充电状态")
        prepare["charge_points"][f"{branch + 1}802"] = {"type": 2, "value": branch_work_status}
        prepare["charge_points"].pop(f"{branch + 1}021")
        check_complete_charge_branch_info(prepare, "结束充电")
