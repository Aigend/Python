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

from common.charge.utils import check_status_code, set_expect_result, deal_receive_data, VALUE_TYPE_MAP, CHARGE_POINT
from common.log import log
from config.settings import BMS_URL, CLOUD_EVENT_URL, PROXIES, MPC_URL

discharge_oss = ""


def set_discharge_point():
    """

    :return:
    """
    points = [str(107000 + i) for i in range(151)]
    points.remove("107006")
    points.remove("107017")
    points.remove("107018")
    points.remove("107021")
    points.remove("107022")
    points.remove("107023")
    points.remove("107024")
    points.remove("107025")
    points.remove("107026")
    points.remove("107027")
    points.remove("107028")
    points.remove("107031")
    points.remove("107032")
    points.remove("107033")
    points.remove("107034")
    points.remove("107035")
    points.remove("107036")
    points.remove("107105")
    points.remove("107106")
    points.remove("107109")
    points.remove("107110")
    return points


@allure.feature("[PTCM-14008]充电结束自放电服务小结上传")
class TestPowerDischargeOss14008:
    """
        检查：充电结束电池自放电检查服务小结
        充电结束类型：电池上报充电完成， 关闭ACDC，PDU, BMS退出
    """

    @pytest.fixture(scope="class", autouse=False)
    def prepare(self, charge, charge_start):
        """

        :param charge:
        :param charge_start:
        :return:
        """
        resource_id = charge["station"]
        event = "800002"
        branch = charge["branch"]
        start_timestamp = charge_start[branch]["start_time"]
        end_timestamp = int(time.time() * 1000)
        data = {
            "resource_id": resource_id,
            "site": "oss",
            "keys": [event],
            "branch_id": branch,
            "timestamp": end_timestamp
        }
        log.info(f"[BEGIN][BMS{branch}]STATION:{resource_id}, BMS{branch}, event{event}, 测试的时间:{end_timestamp}")
        bms_data = deal_receive_data(charge["bms"], {})
        bms_battery_pack_cap = int(bms_data[f"{branch + 1}012"])
        if bms_battery_pack_cap in [8, 1, 3]:  # 0-空闲；1-充电中；2-充电完成；3-满充中；4-放电中；5-放电完成
            log.info(f"[STEP][BMS{branch}]UI停止充电")
            rep = requests.post(MPC_URL, json={"branch": branch}, proxies=PROXIES)
            check_status_code(rep.status_code, 200, f"MPC仿真接口请求异常:{rep.reason}，测试Error！")
            event = 11
        else:
            log.info(f"[STEP][BMS{branch}]上报充电完成")
            charge["bms"] = {
                f"bms{int(branch)}": {
                    f"{int(branch) + 1}521": 3,  # C1# BMSCntctrSts
                    f"{int(branch) + 1}508": 2  # 100度电池上报充电完成
                }
            }
            rep = requests.post(url=BMS_URL, json=charge["bms"], proxies=PROXIES)
            check_status_code(rep.status_code, 200, f"BMS仿真接口请求异常:{rep.reason}，测试Error！")
            event = 4
        set_result = {
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
            "branch_id": int(branch),
            "battery_id": bms_data[f"{int(branch) + 1}001"],
            "battery_gb_pack_id": bms_data[f"{int(branch) + 1}005"],
            "bms_battery_capacity": int(bms_data[f"{int(branch) + 1}012"]),
            "event": 0,
            "start_soc": int(bms_data[f"{int(branch) + 1}023"]),
            "end_soc": int(bms_data[f"{int(branch) + 1}023"]),
            "start_max_temp": int(float(bms_data[f"{int(branch) + 1}036"])),
            "start_max_temp_num": int(bms_data[f"{int(branch) + 1}039"]),
            "end_max_temp": int(float(bms_data[f"{int(branch) + 1}036"])),
            "end_max_temp_num": int(bms_data[f"{int(branch) + 1}039"]),
            "start_voltage": 411,
            "end_voltage": 411,
            "soe_capacity1": 0,
            "soe_electricity1": 0,
            "soe_capacity2": 0,
            "soe_electricity2": 0,
            "soe_capacity3": 0,
            "soe_electricity3": 0,
            "soe_capacity4": 0,
            "soe_electricity4": 0,
            "soe_capacity5": 0,
            "soe_electricity5": 0,
            "soe_capacity6": 0,
            "soe_electricity6": 0,
            "soe_capacity7": 0,
            "soe_electricity7": 0,
            "soe_capacity8": 0,
            "soe_electricity8": 0,
            "soe_capacity9": 0,
            "soe_electricity9": 0,
            "soe_capacity10": 0,
            "soe_electricity10": 0,
            "soe_capacity11": 0,
            "soe_electricity11": 0,
            "soe_capacity12": 0,
            "soe_electricity12": 0,
            "soc_30max_temp": -40,
            "soc_30min_temp": -40,
            "soc_50max_temp": -40,
            "soc_50min_temp": -40,
            "soc_85max_temp": -40,
            "soc_85min_temp": -40,
            "soh_start_soc1": 0,
            "soh_start_current1": 0,
            "soh_maxr_a1": 0,
            "soh_maxr_num_a1": 1,
            "soh_maxr_b1": 0,
            "soh_maxr_num_b1": 1,
            "soh_maxr_c1": 0,
            "soh_maxr_num_c1": 1,
            "soh_minr_a1": 0,
            "soh_minr_num_a1": 1,
            "soh_minr_b1": 0,
            "soh_minr_num_b1": 1,
            "soh_minr_c1": 0,
            "soh_minr_num_c1": 1,
            "soh_avgr1": 0,
            "soh_viff1": 0,
            "soh_start_soc2": 0,
            "soh_start_current2": 0,
            "soh_maxr_a2": 0,
            "soh_maxr_num_a2": 1,
            "soh_maxr_b2": 0,
            "soh_maxr_num_b2": 1,
            "soh_maxr_c2": 0,
            "soh_maxr_num_c2": 1,
            "soh_minr_a2": 0,
            "soh_minr_num_a2": 1,
            "soh_minr_b2": 0,
            "soh_minr_num_b2": 1,
            "soh_minr_c2": 0,
            "soh_minr_num_c2": 1,
            "soh_avgr2": 0,
            "soh_viff2": 0,
            "soh_start_soc3": 0,
            "soh_start_current3": 0,
            "soh_maxr_a3": 0,
            "soh_maxr_num_a3": 1,
            "soh_maxr_b3": 0,
            "soh_maxr_num_b3": 1,
            "soh_maxr_c3": 0,
            "soh_maxr_num_c3": 1,
            "soh_minr_a3": 0,
            "soh_minr_num_a3": 1,
            "soh_minr_b3": 0,
            "soh_minr_num_b3": 1,
            "soh_minr_c3": 0,
            "soh_minr_num_c3": 1,
            "soh_avgr3": 0,
            "soh_viff3": 0,
            "soc_70max_temp": -40,
            "soc_70min_temp": -40,
            "soc_85start_current": 0,
            "charge_service_event": 2,
            "self_discharge_result": 3,
            "self_discharge_check_timestamp": 0,
            "battery_diff_0": 0,
            "battery_diff_1": 0,
            "pressure_drop_rate": 0,
            "degree_of_outlier": 0,
            "soe_capacity13": 0,
            "soe_electricity13": 0,
            "soe_capacity14": 0,
            "soe_electricity14": 0,
            "soe_capacity15": 0,
            "soe_electricity15": 0,
            "soe_capacity16": 0,
            "soe_electricity16": 0,
            "sohmaxr_b_a_1": 0,
            "sohmaxr_num_b_a_1": 1,
            "sohmaxr_b_b_1": 0,
            "sohmaxr_num_b_b_1": 1,
            "sohmaxr_b_c_1": 0,
            "sohmaxr_num_b_c_1": 1,
            "sohminr_b_a_1": 0,
            "sohminr_num_b_a_1": 1,
            "sohminr_b_b_1": 0,
            "sohminr_num_b_b_1": 1,
            "sohminr_b_c_1": 0,
            "sohminr_num_b_c_1": 1,
            "sohmaxr_b_a_2": 0,
            "sohmaxr_num_b_a_2": 1,
            "sohmaxr_b_b_2": 0,
            "sohmaxr_num_b_b_2": 1,
            "sohmaxr_b_c_2": 0,
            "sohmaxr_num_b_c_2": 1,
            "sohminr_b_a_2": 0,
            "sohminr_num_b_a_2": 1,
            "sohminr_b_b_2": 0,
            "sohminr_num_b_b_2": 1,
            "sohminr_b_c_2": 0,
            "sohminr_num_b_c_2": 1,
            "sohmaxr_b_a_3": 0,
            "sohmaxr_num_b_a_3": 1,
            "sohmaxr_b_b_3": 0,
            "sohmaxr_num_b_b_3": 1,
            "sohmaxr_b_c_3": 0,
            "sohmaxr_num_b_c_3": 1,
            "sohminr_b_a_3": 0,
            "sohminr_num_b_a_3": 1,
            "sohminr_b_b_3": 0,
            "sohminr_num_b_b_3": 1,
            "sohminr_b_c_3": 0,
            "sohminr_num_b_c_3": 1,
            "bms_soh": 655,
            "ah_of_overall_charged": -1,
            "ah_of_overall_discharged": -1,
            "ah_of_overall_fastcharged": -1
        }
        set_expect_result(charge, set_result)
        time.sleep(20)
        points = []
        for i in range(6):
            log.info(f"[STEP][BMS{branch}]第{i + 1}次请求CLOUD数据")
            rep = requests.post(CLOUD_EVENT_URL, json=data, proxies=PROXIES)
            check_status_code(rep.status_code, 200, f"Cloud仿真接口请求异常:{rep.reason}，测试Failed！")
            content = json.loads(rep.content)
            points_data = content["data"]["point_data"][0]
            points = points_data.get("data", [])
            if points:
                log.info({"event_id": points_data.get("event_id"), "timestamp": points_data.get("timestamp")})
                log.debug(points)
                break
            time.sleep(10)
        yield charge, event, points
        log.info(f"[END][BMS{branch}]测试结束")

    @pytest.fixture(params=set_discharge_point(), scope="function", autouse=False)
    def check_point(self, request, charge):
        global discharge_oss
        desc = CHARGE_POINT[request.param]["desc"]
        discharge_oss = f"branch:{charge['branch']}, key: {request.param}, desc: {desc}"
        return request.param

    # @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @allure.story(f"PTCM-14008:检查充电结束自放电服务小结: event_id: 800002, {discharge_oss}")
    def test_discharge_oss(self, prepare, check_point):
        """

        :param prepare:
        :param check_point:
        :return:
        """
        prepare, event, points = prepare
        branch = prepare["branch"]
        desc = prepare['charge_points'][f'{check_point}']['desc']
        _info_msg = f"[STEP][BMS{branch}]电池仓A{branch - 9}充电服务小结开始[{event}], 数据ID[{check_point}], 变量名[{desc}]"
        with allure.step(_info_msg):
            expect_type = prepare["charge_points"][f"{check_point}"]["type"]
            expect_val = prepare["charge_points"][f"{check_point}"]["value"]
            for point in points:
                if point["key"] == check_point:
                    actual_type = point['type']
                    actual_val = point[VALUE_TYPE_MAP[point['type']]]
                    if point["key"] in ["107000", "107001"]:
                        _info_msg = f"[STEP][BMS{branch}]expect_type:{expect_type}, actual_type:{actual_type}, expect_val:{expect_val}, actual_val:{actual_val},实际时间戳在期望时间之后，正常"
                        log.info(_info_msg)
                        assert actual_val > expect_val
                        break
                    if isinstance(actual_val, float):
                        actual_val = int(actual_val)
                    _info_msg = f"[STEP][BMS{branch}]expect_type:{expect_type}, actual_type:{actual_type},expect_val:{expect_val}, actual_val:{actual_val}"
                    log.info(_info_msg)
                    assert expect_val == actual_val
                    break
            else:  # 这里前面要加断言，否则为空case pass
                _error_msg = f"[STEP][BMS{branch}]OSS云端未获取到数据:{_info_msg}"
                log.error(_error_msg)
                assert expect_type == ""
                assert expect_val == ""
