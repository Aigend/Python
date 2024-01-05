# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/1/9 17:56
# @File: acdc_data.py
import json

from utils.log import log

ACDC_BASIC = {
    "sw_version": "82",  # 1# ACDC1模块软件版本号
    "hw_version": "83",  # 1# ACDC1模块硬件版本号
    "serial_number": "84",  # 1# ACDC1模块序列号
}

ACDC_STATE = {
    "work_state": "102000",  # //1-待机状态  2-工作状态
    "fault_state": "102001",  # //0- 正常 1-故障
    "group_type": "102002",  # //0-固定分组； 1-动态分组
    "state_machine": "102003",
    # CHARGE_INIT = 0,CHARGE_IDEL = 1,CHARGE_PRE_RUN =2,CHARGE_SOFTSTART =3,CHARGE_PFC_RUN =4,CHARGE_DCDC_RUN =5,CHARGE_ALARM =6,CHARGE_UPDATA =7
    "work_mode": "102004",  # //0-并网  1-离网
    "volt_mode": "102005",  # //0-低压  1-高压
    "running_mode": "102006",  # //运行模式 0-正常 1-调试
}

# ACDC的报警数据，根据开发的代码，需要保证DI有对应的信号输入，电压值12v 具体DI口参考PUS3.0 PCU使用的硬件资源
ACDC_ALARM = {
    "pfc_a_oc_sw": "721000",  # //A相软件过流
    "pfc_b_oc_sw": "721001",  # //B相软件过流
    "pfc_c_oc_sw": "721002",  # //C相软件过流
    "bus_oc_sw": "721003",  # //母线软件过流
    "bus_ov_sw": "721004",  # //母线软件过压
    "bus_uv_sw": "721005",  # //母线软件欠压
    "out_ov_sw": "721006",  # //输出过压
    "out_ol_sw": "721007",  # //输出过载

    "pre_ac_sw": "721008",  # //交流预充失败
    "pre_dc_sw": "721009",  # //直流预充失败
    "igbt_fault_sw": "721010",  # //igbt软件故障
    "ntc_otp_sw": "721011",  # //过温报护
    "sensor_fault_sw": "721012",  # //传感器校准失败
    "cfg_fault_sw": "721013",  # //参数配置错误
    "pfc_a_oc_hw": "721014",  # //A相硬件过流
    "pfc_b_oc_hw": "721015",  # //B相硬件过流

    "pfc_c_oc_hw": "721016",  # //C相硬件过流
    "pfc_z_oc_hw": "721017",  # //零序硬件过流
    "bus_oc_hw": "721018",  # //母线硬件过流
    "bus_ov_hw": "721019",  # //母线硬件过压
    "driver_fault1_hw": "721020",  # //驱动故障1
    "driver_fault2_hw": "721021",  # //驱动故障2
    "op_fault_hw": "721022",  # //op故障
    "rely_in_sw": "721023",  # //输入继电器故障

    "rely_out_sw": "721024",  # //输出继电器故障
    "leakage_circuit_fault": "721025",  # //泄放电路故障
    "module_irreparable": "721026",  # //模块损坏
    "grid_uv_sw": "721027",  # //电网欠压
    "grid_open_phase": "721028",  # //电网缺相
    "grid_island_sw": "721029",  # //孤岛报护
    "grid_ov_sw": "721030",  # //电网过压
    "grid_of_sw": "721031",  # //电网超频

    "grid_uf_sw": "721032",  # //电网欠频
    "grid_unbalance": "721033",  # //电网不平衡
    "input_broken": "721034",  # //输入掉电故障
    "ac_ov_disconnected": "721035",  # //交流过压脱离
    "short_circuit_shut_down": "721036",  # //模块输出短路锁死
    "dc_ov_shut_down": "721037",  # //直流输出过压锁死
    "dc_uv": "721038",  # //直流输出欠压
    "dc_voltage_unbalance": "721039",  # //直流输出不平衡

    "pfc_unbalance": "721040",  # //PFC输出电压不平衡
    "eeprom_fault": "721041",  # //PFC或DC EEPROM故障
    "fan_fault": "721042",  # //风扇故障
    "sci_is_not_ok": "721043",  # //PFC和DC通讯故障
    "ambient_ut": "721044",  # //环境温度过低
    "get_same_s_nor_addr": "721045",  # //模块系列号或地址号重复
}

ACDC_REAL = {
    "set_voltage": "100000",  # 模块设定电压 # 调试未生效
    "set_current": "100001",  # 模块设定电流 # 调试未生效
    "bus_volt": "100002",  # //母线电压  分辨率0.1V 范围0-1000
    "output_volt": "100003",  # //输出电压  分辨率0.1V 范围0-1000
    "output_curr": "100004",  # //输出电流  分辨率0.01A 范围-300-300  偏移量300
    "a_phase_in_curr": "100005",  # //a相输入电流 分辨率0.01A 范围-300-300  偏移量300
    "b_phase_in_curr": "100006",  # //b相输入电流 分辨率0.01A 范围-300-300  偏移量300
    "c_phase_in_curr": "100007",  # //c相输入电流 分辨率0.01A 范围-300-300  偏移量300
    "ab_line_volt": "100008",  # //ab线电压    分辨率0.1V 范围0-500
    "bc_line_volt": "100009",  # //bc线电压    分辨率0.1V 范围0-500
    "grid_freq": "100010",  # //电网频率    分辨率0.01Hz  范围0~70
    "active_power": "100011",  # //有功功率    分辨率0.01KW  范围0~100
    "reactive_power": "100012",  # //无功功率    分辨率0.01KW  范围0~100
    "power_factor": "100013",  # //功率因素    分辨率0.001 范围0~1
    "mdl_efficiency": "100014",  # //模块效率    分辨率0.001 范围0~1
    "air_temp": "100015",  # //空气温度    分别率1℃  范围-55~200 偏移量55
    "water_temp": "100016",  # //水温度      分别率1℃  范围-55~200 偏移量55
    "sic1_temp": "100017",  # //sic1温度    分别率1℃  范围-55~200 偏移量55
    "sic2_temp": "100018",  # //sic1温度    分别率1℃  范围-55~200 偏移量55
    "sic3_temp": "100019",  # //sic1温度    分别率1℃  范围-55~200 偏移量55
    "igbt_temp": "100020",  # //igbt温度    分别率1℃  范围-55~200 偏移量55
    "inductance_temp": "100021",  # //电感温度    分别率1℃  范围-55~200 偏移量55
    "group_num": "100022",  # //当前组号    范围0~255 （0表示未分组）
}


def acdc_key_to_variable(acdc_node, data):
    """
    :param acdc_node:0-29
    :param data:
    :return:
    """
    result = {}
    basic_add = acdc_node * 3  # 基本数据通信点表key值每支路acdc间隔3:82, 85, ......
    real_add = acdc_node * 30  # 实时数据通信点表key值每支路acdc间隔30:100000, 100030, ......
    alarm_add = acdc_node * 64  # 报警数据通信点表key值每支路acdc间隔64:721000, 721064, ......
    state_add = acdc_node * 10  # 状态数据通信点表key值每支路acdc间隔10:102000, 102010, ......
    for var_name, k_value in ACDC_BASIC.items():
        tmp = str(int(k_value) + basic_add)
        if tmp in data:
            result[var_name] = data.get(tmp)
    for var_name, k_value in ACDC_REAL.items():
        tmp = str(int(k_value) + real_add)
        if tmp in data:
            result[var_name] = data.get(tmp)
    for var_name, k_value in ACDC_ALARM.items():
        tmp = str(int(k_value) + alarm_add)
        if tmp in data:
            result[var_name] = data.get(tmp)
    for var_name, k_value in ACDC_STATE.items():
        tmp = str(int(k_value) + state_add)
        if tmp in data:
            result[var_name] = data.get(tmp)
    # log.info(f"<ACDC>:发送的数据转换后的结果:{result}")
    return result


if __name__ == '__main__':
    for i in range(30):
        result = {f"acdc{i}":{}}
        state_add = i * 10
        state = []
        for var_name, k_value in ACDC_STATE.items():
            tmp = int(int(k_value) + state_add)
            state.append(tmp)
        st = sorted(state)
        result[f"acdc{i}"][f"{st[0]}"] = 1
        result[f"acdc{i}"][f"{st[1]}"] = 0
        result[f"acdc{i}"][f"{st[2]}"] = 1
        result[f"acdc{i}"][f"{st[3]}"] = 0
        result[f"acdc{i}"][f"{st[4]}"] = 0
        result[f"acdc{i}"][f"{st[5]}"] = 0
        result[f"acdc{i}"][f"{st[6]}"] = 0

        real_add = i * 30
        state = []
        for var_name, k_value in ACDC_REAL.items():
            tmp = int(int(k_value) + real_add)
            state.append(tmp)
        st = sorted(state)
        result[f"acdc{i}"][f"{st[0]}"] = 0
        result[f"acdc{i}"][f"{st[1]}"] = 0
        result[f"acdc{i}"][f"{st[2]}"] = 859.7
        result[f"acdc{i}"][f"{st[3]}"] = 405.2
        result[f"acdc{i}"][f"{st[4]}"] = 1.64
        result[f"acdc{i}"][f"{st[5]}"] = 0
        result[f"acdc{i}"][f"{st[6]}"] = 0
        result[f"acdc{i}"][f"{st[7]}"] = 0
        result[f"acdc{i}"][f"{st[8]}"] = 407.8
        result[f"acdc{i}"][f"{st[9]}"] = 407.7
        result[f"acdc{i}"][f"{st[10]}"] = 50
        result[f"acdc{i}"][f"{st[11]}"] = 0
        result[f"acdc{i}"][f"{st[12]}"] = 0
        result[f"acdc{i}"][f"{st[13]}"] = 0
        result[f"acdc{i}"][f"{st[14]}"] = 0
        result[f"acdc{i}"][f"{st[15]}"] = 26
        result[f"acdc{i}"][f"{st[16]}"] = 0
        result[f"acdc{i}"][f"{st[17]}"] = 22
        result[f"acdc{i}"][f"{st[18]}"] = 29
        result[f"acdc{i}"][f"{st[19]}"] = 32
        result[f"acdc{i}"][f"{st[20]}"] = 0
        result[f"acdc{i}"][f"{st[21]}"] = 0
        result[f"acdc{i}"][f"{st[22]}"] = i//3 + 1
        with open(f"acdc_{i}.json", "w") as f:
            json.dump(result, f)




