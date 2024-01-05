"""
@Project: full
@File: check.py
@Author: wenlong.jin
@Time: 2023/10/30 17:24
@version: 1.0.0
@Description:
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
from copy import deepcopy

CHARGE_POINT = {
    '107000': {
        'desc': '开始时间戳',
        'type': 3
    },
    '107001': {
        'desc': '结束时间戳',
        'type': 3
    },
    '107002': {
        'desc': '支路号',
        'type': 2
    },
    '107003': {
        'desc': '电池ID',
        'type': 6
    },
    '107004': {
        'desc': '电池国标ID',
        'type': 6
    },
    '107005': {
        'desc': '电池类型',
        'type': 2
    },
    '107006': {
        'desc': '完成原因',
        'type': 2
    },
    '107007': {
        'desc': '充电开始电量',
        'type': 4
    },
    '107008': {
        'desc': '结束电量',
        'type': 4
    },
    '107009': {
        'desc': '开始最高电芯温度',
        'type': 4
    },
    '107010': {
        'desc': '开始最高电芯温度编号',
        'type': 2
    },
    '107011': {
        'desc': '结束最高电芯温度',
        'type': 4
    },
    '107012': {
        'desc': '结束最高电芯温度编号',
        'type': 2
    },
    '107013': {
        'desc': '充电起始电压（0电流）',
        'type': 4
    },
    '107014': {
        'desc': '充电结束电压（0电流）',
        'type': 4
    },
    '107015': {
        'desc': 'SOE容量1',
        'type': 4
    },
    '107016': {
        'desc': 'SOE电量1',
        'type': 4
    },
    '107017': {
        'desc': 'SOE容量2',
        'type': 4
    },
    '107018': {
        'desc': 'SOE电量2',
        'type': 4
    },
    '107019': {
        'desc': 'SOE容量3',
        'type': 4
    },
    '107020': {
        'desc': 'SOE电量3',
        'type': 4
    },
    '107021': {
        'desc': 'SOE容量4',
        'type': 4
    },
    '107022': {
        'desc': 'SOE电量4',
        'type': 4
    },
    '107023': {
        'desc': 'SOE容量5',
        'type': 4
    },
    '107024': {
        'desc': 'SOE电量5',
        'type': 4
    },
    '107025': {
        'desc': 'SOE容量6',
        'type': 4
    },
    '107026': {
        'desc': 'SOE电量6',
        'type': 4
    },
    '107027': {
        'desc': 'SOE容量7',
        'type': 4
    },
    '107028': {
        'desc': 'SOE电量7',
        'type': 4
    },
    '107029': {
        'desc': 'SOE容量8',
        'type': 4
    },
    '107030': {
        'desc': 'SOE电量8',
        'type': 4
    },
    '107031': {
        'desc': 'SOE容量9',
        'type': 4
    },
    '107032': {
        'desc': 'SOE电量9',
        'type': 4
    },
    '107033': {
        'desc': 'SOE容量10',
        'type': 4
    },
    '107034': {
        'desc': 'SOE电量10',
        'type': 4
    },
    '107035': {
        'desc': 'SOE容量11',
        'type': 4
    },
    '107036': {
        'desc': 'SOE电量11',
        'type': 4
    },
    '107037': {
        'desc': 'SOE容量12',
        'type': 4
    },
    '107038': {
        'desc': 'SOE电量12',
        'type': 4
    },
    '107039': {
        'desc': 'SOC30最高温度',
        'type': 4
    },
    '107040': {
        'desc': 'SOC30最低温度',
        'type': 4
    },
    '107041': {
        'desc': 'SOC50最高温度',
        'type': 4
    },
    '107042': {
        'desc': 'SOC50最低温度',
        'type': 4
    },
    '107043': {
        'desc': 'SOC85最高温度',
        'type': 4
    },
    '107044': {
        'desc': 'SOC85最低温度',
        'type': 4
    },
    '107045': {
        'desc': 'SOH起始SOC_1',
        'type': 4
    },
    '107046': {
        'desc': 'SOH起始电流_1',
        'type': 4
    },
    '107047': {
        'desc': 'SOHMaxR_a_1',
        'type': 4
    },
    '107048': {
        'desc': 'SOHMaxRNum_a_1',
        'type': 2
    },
    '107049': {
        'desc': 'SOHMaxR_b_1',
        'type': 4
    },
    '107050': {
        'desc': 'SOHMaxRNum_b_1',
        'type': 2
    },
    '107051': {
        'desc': 'SOHMaxR_c_1',
        'type': 4
    },
    '107052': {
        'desc': 'SOHMaxRNum_c_1',
        'type': 2
    },
    '107053': {
        'desc': 'SOHMinR_a_1',
        'type': 4
    },
    '107054': {
        'desc': 'SOHMinRNum_a_1',
        'type': 2
    },
    '107055': {
        'desc': 'SOHMinR_b_1',
        'type': 4
    },
    '107056': {
        'desc': 'SOHMinRNum_b_1',
        'type': 2
    },
    '107057': {
        'desc': 'SOHMinR_c_1',
        'type': 4
    },
    '107058': {
        'desc': 'SOHMinRNum_c_1',
        'type': 2
    },
    '107059': {
        'desc': 'SOHAvgR_1',
        'type': 4
    },
    '107060': {
        'desc': 'SOHViff_1',
        'type': 4
    },
    '107061': {
        'desc': 'SOH起始SOC_2',
        'type': 4
    },
    '107062': {
        'desc': 'SOH起始电流_2',
        'type': 4
    },
    '107063': {
        'desc': 'SOHMaxR_a_2',
        'type': 4
    },
    '107064': {
        'desc': 'SOHMaxRNum_a_2',
        'type': 2
    },
    '107065': {
        'desc': 'SOHMaxR_b_2',
        'type': 4
    },
    '107066': {
        'desc': 'SOHMaxRNum_b_2',
        'type': 2
    },
    '107067': {
        'desc': 'SOHMaxR_c_2',
        'type': 4
    },
    '107068': {
        'desc': 'SOHMaxRNum_c_2',
        'type': 2
    },
    '107069': {
        'desc': 'SOHMinR_a_2',
        'type': 4
    },
    '107070': {
        'desc': 'SOHMinRNum_a_2',
        'type': 2
    },
    '107071': {
        'desc': 'SOHMinR_b_2',
        'type': 4
    },
    '107072': {
        'desc': 'SOHMinRNum_b_2',
        'type': 2
    },
    '107073': {
        'desc': 'SOHMinR_c_2',
        'type': 4
    },
    '107074': {
        'desc': 'SOHMinRNum_c_2',
        'type': 2
    },
    '107075': {
        'desc': 'SOHAvgR_2',
        'type': 4
    },
    '107076': {
        'desc': 'SOHViff_2',
        'type': 4
    },
    '107077': {
        'desc': 'SOH起始SOC_3',
        'type': 4
    },
    '107078': {
        'desc': 'SOH起始电流_3',
        'type': 4
    },
    '107079': {
        'desc': 'SOHMaxR_a_3',
        'type': 4
    },
    '107080': {
        'desc': 'SOHMaxRNum_a_3',
        'type': 2
    },
    '107081': {
        'desc': 'SOHMaxR_b_3',
        'type': 4
    },
    '107082': {
        'desc': 'SOHMaxRNum_b_3',
        'type': 2
    },
    '107083': {
        'desc': 'SOHMaxR_c_3',
        'type': 4
    },
    '107084': {
        'desc': 'SOHMaxRNum_c_3',
        'type': 2
    },
    '107085': {
        'desc': 'SOHMinR_a_3',
        'type': 4
    },
    '107086': {
        'desc': 'SOHMinRNum_a_3',
        'type': 2
    },
    '107087': {
        'desc': 'SOHMinR_b_3',
        'type': 4
    },
    '107088': {
        'desc': 'SOHMinRNum_b_3',
        'type': 2
    },
    '107089': {
        'desc': 'SOHMinR_c_3',
        'type': 4
    },
    '107090': {
        'desc': 'SOHMinRNum_c_3',
        'type': 2
    },
    '107091': {
        'desc': 'SOHAvgR_3',
        'type': 4
    },
    '107092': {
        'desc': 'SOHViff_3',
        'type': 4
    },
    '107093': {
        'desc': 'SOC70最高温度',
        'type': 4
    },
    '107094': {
        'desc': 'SOC70最低温度',
        'type': 4
    },
    '107095': {
        'desc': 'SOC85起始电流',
        'type': 4
    },
    '107096': {
        'desc': '充电服务事件',
        'type': 2
    },
    '107097': {
        'desc': '自放电检查结果',
        'type': 2
    },
    '107098': {
        'desc': '自放电检查时间点',
        'type': 3
    },
    '107099': {
        'desc': '电池压差_0',
        'type': 4
    },
    '107100': {
        'desc': '电池压差_1',
        'type': 4
    },
    '107101': {
        'desc': '压降速率',
        'type': 4
    },
    '107102': {
        'desc': '离群程度',
        'type': 4
    },
    '107103': {
        'desc': 'SOE容量13',
        'type': 4
    },
    '107104': {
        'desc': 'SOE电量13',
        'type': 4
    },
    '107105': {
        'desc': 'SOE容量14',
        'type': 4
    },
    '107106': {
        'desc': 'SOE电量14',
        'type': 4
    },
    '107107': {
        'desc': 'SOE容量15',
        'type': 4
    },
    '107108': {
        'desc': 'SOE电量15',
        'type': 4
    },
    '107109': {
        'desc': 'SOE容量16',
        'type': 4
    },
    '107110': {
        'desc': 'SOE电量16',
        'type': 4
    },
    '107111': {
        'desc': 'SOHMaxR_B_a_1',
        'type': 4
    },
    '107112': {
        'desc': 'SOHMaxRNum_B_a_1',
        'type': 2
    },
    '107113': {
        'desc': 'SOHMaxR_B_b_1',
        'type': 4
    },
    '107114': {
        'desc': 'SOHMaxRNum_B_b_1',
        'type': 2
    },
    '107115': {
        'desc': 'SOHMaxR_B_c_1',
        'type': 4
    },
    '107116': {
        'desc': 'SOHMaxRNum_B_c_1',
        'type': 2
    },
    '107117': {
        'desc': 'SOHMinR_B_a_1',
        'type': 4
    },
    '107118': {
        'desc': 'SOHMinRNum_B_a_1',
        'type': 2
    },
    '107119': {
        'desc': 'SOHMinR_B_b_1',
        'type': 4
    },
    '107120': {
        'desc': 'SOHMinRNum_B_b_1',
        'type': 2
    },
    '107121': {
        'desc': 'SOHMinR_B_c_1',
        'type': 4
    },
    '107122': {
        'desc': 'SOHMinRNum_B_c_1',
        'type': 2
    },
    '107123': {
        'desc': 'SOHMaxR_B_a_2',
        'type': 4
    },
    '107124': {
        'desc': 'SOHMaxRNum_B_a_2',
        'type': 2
    },
    '107125': {
        'desc': 'SOHMaxR_B_b_2',
        'type': 4
    },
    '107126': {
        'desc': 'SOHMaxRNum_B_b_2',
        'type': 2
    },
    '107127': {
        'desc': 'SOHMaxR_B_c_2',
        'type': 4
    },
    '107128': {
        'desc': 'SOHMaxRNum_B_c_2',
        'type': 2
    },
    '107129': {
        'desc': 'SOHMinR_B_a_2',
        'type': 4
    },
    '107130': {
        'desc': 'SOHMinRNum_B_a_2',
        'type': 2
    },
    '107131': {
        'desc': 'SOHMinR_B_b_2',
        'type': 4
    },
    '107132': {
        'desc': 'SOHMinRNum_B_b_2',
        'type': 2
    },
    '107133': {
        'desc': 'SOHMinR_B_c_2',
        'type': 4
    },
    '107134': {
        'desc': 'SOHMinRNum_B_c_2',
        'type': 2
    },
    '107135': {
        'desc': 'SOHMaxR_B_a_3',
        'type': 4
    },
    '107136': {
        'desc': 'SOHMaxRNum_B_a_3',
        'type': 2
    },
    '107137': {
        'desc': 'SOHMaxR_B_b_3',
        'type': 4
    },
    '107138': {
        'desc': 'SOHMaxRNum_B_b_3',
        'type': 2
    },
    '107139': {
        'desc': 'SOHMaxR_B_c_3',
        'type': 4
    },
    '107140': {
        'desc': 'SOHMaxRNum_B_c_3',
        'type': 2
    },
    '107141': {
        'desc': 'SOHMinR_B_a_3',
        'type': 4
    },
    '107142': {
        'desc': 'SOHMinRNum_B_a_3',
        'type': 2
    },
    '107143': {
        'desc': 'SOHMinR_B_b_3',
        'type': 4
    },
    '107144': {
        'desc': 'SOHMinRNum_B_b_3',
        'type': 2
    },
    '107145': {
        'desc': 'SOHMinR_B_c_3',
        'type': 4
    },
    '107146': {
        'desc': 'SOHMinRNum_B_c_3',
        'type': 2
    },
    '107147': {
        'desc': '电池健康度',
        'type': 4
    },
    '107148': {
        'desc': '总充电安时数',
        'type': 2
    },
    '107149': {
        'desc': '总放电安时数',
        'type': 2
    },
    '107150': {
        'desc': '总快充安时数',
        'type': 2
    }
}

# BMS_KEY_MAP = {
#     "battery_pack_id": "1001",
#     "gb_battery_pack_id": "1005",
#     "bms_battery_pack_cap": "1012"
# }


VALUE_TYPE_MAP = {
    2: "value_int",
    3: "value_long",
    4: "value_float",
    6: "value_string",
}


def connect_mqtt():
    pass


def check_status_code(rep_status, exp_status, msg):
    if rep_status != exp_status:
        raise Exception(msg)


def deal_receive_data(rec_json, rep_json):
    if isinstance(rec_json, dict):
        for name, val in rec_json.items():
            if isinstance(val, dict):
                deal_receive_data(val, rep_json)
            else:
                rep_json[name] = val
    return rep_json


def set_expect_result(charge, set_result):
    charge_points = deepcopy(CHARGE_POINT)
    charge_points["107000"]["value"] = set_result["start_timestamp"]
    charge_points["107001"]["value"] = set_result["end_timestamp"]
    charge_points["107002"]["value"] = set_result["branch_id"]
    charge_points["107003"]["value"] = set_result["battery_id"]
    charge_points["107004"]["value"] = set_result["battery_gb_pack_id"]
    charge_points["107005"]["value"] = set_result["bms_battery_capacity"]
    charge_points["107006"]["value"] = set_result["event"]
    charge_points["107007"]["value"] = set_result["start_soc"]
    charge_points["107008"]["value"] = set_result["end_soc"]
    charge_points["107009"]["value"] = set_result["start_max_temp"]
    charge_points["107010"]["value"] = set_result["start_max_temp_num"]
    charge_points["107011"]["value"] = set_result["end_max_temp"]
    charge_points["107012"]["value"] = set_result["end_max_temp_num"]
    charge_points["107013"]["value"] = set_result["start_voltage"]
    charge_points["107014"]["value"] = set_result["end_voltage"]
    charge_points["107015"]["value"] = set_result["soe_capacity1"]
    charge_points["107016"]["value"] = set_result["soe_electricity1"]
    charge_points["107017"]["value"] = set_result["soe_capacity2"]
    charge_points["107018"]["value"] = set_result["soe_electricity2"]
    charge_points["107019"]["value"] = set_result["soe_capacity3"]
    charge_points["107020"]["value"] = set_result["soe_electricity3"]
    charge_points["107021"]["value"] = set_result["soe_capacity4"]
    charge_points["107022"]["value"] = set_result["soe_electricity4"]
    charge_points["107023"]["value"] = set_result["soe_capacity5"]
    charge_points["107024"]["value"] = set_result["soe_electricity5"]
    charge_points["107025"]["value"] = set_result["soe_capacity6"]
    charge_points["107026"]["value"] = set_result["soe_electricity6"]
    charge_points["107027"]["value"] = set_result["soe_capacity7"]
    charge_points["107028"]["value"] = set_result["soe_electricity7"]
    charge_points["107029"]["value"] = set_result["soe_capacity8"]
    charge_points["107030"]["value"] = set_result["soe_electricity8"]
    charge_points["107031"]["value"] = set_result["soe_capacity9"]
    charge_points["107032"]["value"] = set_result["soe_electricity9"]
    charge_points["107033"]["value"] = set_result["soe_capacity10"]
    charge_points["107034"]["value"] = set_result["soe_electricity10"]
    charge_points["107035"]["value"] = set_result["soe_capacity11"]
    charge_points["107036"]["value"] = set_result["soe_electricity11"]
    charge_points["107037"]["value"] = set_result["soe_capacity12"]
    charge_points["107038"]["value"] = set_result["soe_electricity12"]
    charge_points["107039"]["value"] = set_result["soc_30max_temp"]
    charge_points["107040"]["value"] = set_result["soc_30min_temp"]
    charge_points["107041"]["value"] = set_result["soc_50max_temp"]
    charge_points["107042"]["value"] = set_result["soc_50min_temp"]
    charge_points["107043"]["value"] = set_result["soc_85max_temp"]
    charge_points["107044"]["value"] = set_result["soc_85min_temp"]
    charge_points["107045"]["value"] = set_result["soh_start_soc1"]
    charge_points["107046"]["value"] = set_result["soh_start_current1"]
    charge_points["107047"]["value"] = set_result["soh_maxr_a1"]
    charge_points["107048"]["value"] = set_result["soh_maxr_num_a1"]
    charge_points["107049"]["value"] = set_result["soh_maxr_b1"]
    charge_points["107050"]["value"] = set_result["soh_maxr_num_b1"]
    charge_points["107051"]["value"] = set_result["soh_maxr_c1"]
    charge_points["107052"]["value"] = set_result["soh_maxr_num_c1"]
    charge_points["107053"]["value"] = set_result["soh_minr_a1"]
    charge_points["107054"]["value"] = set_result["soh_minr_num_a1"]
    charge_points["107055"]["value"] = set_result["soh_minr_b1"]
    charge_points["107056"]["value"] = set_result["soh_minr_num_b1"]
    charge_points["107057"]["value"] = set_result["soh_minr_c1"]
    charge_points["107058"]["value"] = set_result["soh_minr_num_c1"]
    charge_points["107059"]["value"] = set_result["soh_avgr1"]
    charge_points["107060"]["value"] = set_result["soh_viff1"]
    charge_points["107061"]["value"] = set_result["soh_start_soc2"]
    charge_points["107062"]["value"] = set_result["soh_start_current2"]
    charge_points["107063"]["value"] = set_result["soh_maxr_a2"]
    charge_points["107064"]["value"] = set_result["soh_maxr_num_a2"]
    charge_points["107065"]["value"] = set_result["soh_maxr_b2"]
    charge_points["107066"]["value"] = set_result["soh_maxr_num_b2"]
    charge_points["107067"]["value"] = set_result["soh_maxr_c2"]
    charge_points["107068"]["value"] = set_result["soh_maxr_num_c2"]
    charge_points["107069"]["value"] = set_result["soh_minr_a2"]
    charge_points["107070"]["value"] = set_result["soh_minr_num_a2"]
    charge_points["107071"]["value"] = set_result["soh_minr_b2"]
    charge_points["107072"]["value"] = set_result["soh_minr_num_b2"]
    charge_points["107073"]["value"] = set_result["soh_minr_c2"]
    charge_points["107074"]["value"] = set_result["soh_minr_num_c2"]
    charge_points["107075"]["value"] = set_result["soh_avgr2"]
    charge_points["107076"]["value"] = set_result["soh_viff2"]
    charge_points["107077"]["value"] = set_result["soh_start_soc3"]
    charge_points["107078"]["value"] = set_result["soh_start_current3"]
    charge_points["107079"]["value"] = set_result["soh_maxr_a3"]
    charge_points["107080"]["value"] = set_result["soh_maxr_num_a3"]
    charge_points["107081"]["value"] = set_result["soh_maxr_b3"]
    charge_points["107082"]["value"] = set_result["soh_maxr_num_b3"]
    charge_points["107083"]["value"] = set_result["soh_maxr_c3"]
    charge_points["107084"]["value"] = set_result["soh_maxr_num_c3"]
    charge_points["107085"]["value"] = set_result["soh_minr_a3"]
    charge_points["107086"]["value"] = set_result["soh_minr_num_a3"]
    charge_points["107087"]["value"] = set_result["soh_minr_b3"]
    charge_points["107088"]["value"] = set_result["soh_minr_num_b3"]
    charge_points["107089"]["value"] = set_result["soh_minr_c3"]
    charge_points["107090"]["value"] = set_result["soh_minr_num_c3"]
    charge_points["107091"]["value"] = set_result["soh_avgr3"]
    charge_points["107092"]["value"] = set_result["soh_viff3"]
    charge_points["107093"]["value"] = set_result["soc_70max_temp"]
    charge_points["107094"]["value"] = set_result["soc_70min_temp"]
    charge_points["107095"]["value"] = set_result["soc_85start_current"]
    charge_points["107096"]["value"] = set_result["charge_service_event"]
    charge_points["107097"]["value"] = set_result["self_discharge_result"]
    charge_points["107098"]["value"] = set_result["self_discharge_check_timestamp"]
    charge_points["107099"]["value"] = set_result["battery_diff_0"]
    charge_points["107100"]["value"] = set_result["battery_diff_1"]
    charge_points["107101"]["value"] = set_result["pressure_drop_rate"]
    charge_points["107102"]["value"] = set_result["degree_of_outlier"]
    charge_points["107103"]["value"] = set_result["soe_capacity13"]
    charge_points["107104"]["value"] = set_result["soe_electricity13"]
    charge_points["107105"]["value"] = set_result["soe_capacity14"]
    charge_points["107106"]["value"] = set_result["soe_electricity14"]
    charge_points["107107"]["value"] = set_result["soe_capacity15"]
    charge_points["107108"]["value"] = set_result["soe_electricity15"]
    charge_points["107109"]["value"] = set_result["soe_capacity16"]
    charge_points["107110"]["value"] = set_result["soe_electricity16"]
    charge_points["107111"]["value"] = set_result["sohmaxr_b_a_1"]
    charge_points["107112"]["value"] = set_result["sohmaxr_num_b_a_1"]
    charge_points["107113"]["value"] = set_result["sohmaxr_b_b_1"]
    charge_points["107114"]["value"] = set_result["sohmaxr_num_b_b_1"]
    charge_points["107115"]["value"] = set_result["sohmaxr_b_c_1"]
    charge_points["107116"]["value"] = set_result["sohmaxr_num_b_c_1"]
    charge_points["107117"]["value"] = set_result["sohminr_b_a_1"]
    charge_points["107118"]["value"] = set_result["sohminr_num_b_a_1"]
    charge_points["107119"]["value"] = set_result["sohminr_b_b_1"]
    charge_points["107120"]["value"] = set_result["sohminr_num_b_b_1"]
    charge_points["107121"]["value"] = set_result["sohminr_b_c_1"]
    charge_points["107122"]["value"] = set_result["sohminr_num_b_c_1"]
    charge_points["107123"]["value"] = set_result["sohmaxr_b_a_2"]
    charge_points["107124"]["value"] = set_result["sohmaxr_num_b_a_2"]
    charge_points["107125"]["value"] = set_result["sohmaxr_b_b_2"]
    charge_points["107126"]["value"] = set_result["sohmaxr_num_b_b_2"]
    charge_points["107127"]["value"] = set_result["sohmaxr_b_c_2"]
    charge_points["107128"]["value"] = set_result["sohmaxr_num_b_c_2"]
    charge_points["107129"]["value"] = set_result["sohminr_b_a_2"]
    charge_points["107130"]["value"] = set_result["sohminr_num_b_a_2"]
    charge_points["107131"]["value"] = set_result["sohminr_b_b_2"]
    charge_points["107132"]["value"] = set_result["sohminr_num_b_b_2"]
    charge_points["107133"]["value"] = set_result["sohminr_b_c_2"]
    charge_points["107134"]["value"] = set_result["sohminr_num_b_c_2"]
    charge_points["107135"]["value"] = set_result["sohmaxr_b_a_3"]
    charge_points["107136"]["value"] = set_result["sohmaxr_num_b_a_3"]
    charge_points["107137"]["value"] = set_result["sohmaxr_b_b_3"]
    charge_points["107138"]["value"] = set_result["sohmaxr_num_b_b_3"]
    charge_points["107139"]["value"] = set_result["sohmaxr_b_c_3"]
    charge_points["107140"]["value"] = set_result["sohmaxr_num_b_c_3"]
    charge_points["107141"]["value"] = set_result["sohminr_b_a_3"]
    charge_points["107142"]["value"] = set_result["sohminr_num_b_a_3"]
    charge_points["107143"]["value"] = set_result["sohminr_b_b_3"]
    charge_points["107144"]["value"] = set_result["sohminr_num_b_b_3"]
    charge_points["107145"]["value"] = set_result["sohminr_b_c_3"]
    charge_points["107146"]["value"] = set_result["sohminr_num_b_c_3"]
    charge_points["107147"]["value"] = set_result["bms_soh"]
    charge_points["107148"]["value"] = set_result["ah_of_overall_charged"]
    charge_points["107149"]["value"] = set_result["ah_of_overall_discharged"]
    charge_points["107150"]["value"] = set_result["ah_of_overall_fastcharged"]
    charge["charge_points"] = charge_points
