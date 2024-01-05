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
from config.settings import CLOUD_REALTIME_URL, PROXIES


@allure.feature("[PTCM-15904]手动开启充电")
class TestPowerBeginCharge15904:
    """
        检查：启动充电
        充电结束类型：一直充电未停止
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
        bms_data = deal_receive_data(charge["bms"], {})
        bms_battery_pack_cap = int(bms_data[f"{branch + 1}012"])
        # 75度的3个月就会进行满充 充电到100%
        branch_work_status = 3 if bms_battery_pack_cap == 8 else 1
        charge["charge_points"] = {}
        charge["charge_points"][f"{branch + 1}802"] = {"type": 2, "value": branch_work_status}
        charge["charge_points"][f"{branch + 1}021"] = {"type": 4, "value": -14}
        yield charge
        log.info(f"[END][BMS{branch}]测试结束")

    # @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @allure.story(f"PTCM-15904:充电开启，检查充电支路工作状态和充电电流")
    def test_begin_charge_15904(self, prepare):
        """

        :param prepare:
        :return:
        """
        branch = prepare["branch"]
        check_points = [f"{branch + 1}802", f"{branch + 1}021"]
        check_points_desc = ["CDC 支路工作状态", "BMS电池包总电流"]
        for i in range(len(check_points)):
            _info_msg = f"[STEP][BMS{branch}]电池仓A{branch - 9}充电状态, 数据ID[{check_points[i]}], 变量名[{check_points_desc[i]}]"
            log.info(_info_msg)
            data = {
                "resource_id": prepare["station"],
                "site": "oss",
                "keys": [check_points[i]]
            }
            content = ""
            expect_type = prepare["charge_points"][f"{check_points[i]}"]["type"]
            expect_val = prepare["charge_points"][f"{check_points[i]}"]["value"]
            actual_type = -1
            actual_val = -1
            for j in range(6):
                log.info(f"[STEP][BMS{branch}]check point [{check_points[i]}] 第{j + 1}次请求CLOUD数据")
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
