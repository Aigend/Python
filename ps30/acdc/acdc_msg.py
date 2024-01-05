# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/8/15 10:59
# @File:acdc_msg.py
import re

import can

from acdc.acdc_data import acdc_key_to_variable


class AcdcMsg:

    def __init__(self, receive_data, branch):
        """

        :param receive_data: json数据，key为云端的key字符串
        :param branch: 字符串
        """
        self.pf2a = []
        self.pf83 = []
        self.pf83_serial_number = []
        self.pf83_hw_version = []
        self.pf83_sw_version = []
        self.receive_data = receive_data
        self.branch = branch  # 0-29
        self.data = receive_data
        self.addr = self.branch + 0x20
        self.board = [0 for _ in range(44)]
        # self.cmd_map = {
        #     0x01: {},  # 快速开机，绝缘检测阶段使用
        #     0x02: {},
        #     0x03: {},  # 软启开机
        #     0x04: {},
        #     0x05: {},
        #     0x06: {}
        # }
        self.init_msg_data()

    def __repr__(self):
        return str(self.pf2a)

    def init_msg_data(self):
        self.generate_pf2a_msg()
        self.generate_pf83_msg()

    def update_pf2a_msg(self, frame):
        cmd = frame[0] & 0x0F
        if cmd == 0x01:
            self.board[0] = self.board[0] | (2 << 6)
        elif cmd == 0x02:  # # 停止充电
            self.board[0] = self.board[0] | (1 << 6)
        elif cmd == 0x03:
            self.board[0] = self.board[0] | (2 << 6)
        elif cmd == 0x04:
            return
        elif cmd == 0x05:
            return
        elif cmd == 0x06:
            self.board[0] = self.board[0] | (1 << 6)
        self.pf2a = self.pack_long_frame(self.board, [], 0x2A, 0xA0, self.addr)
        return True

    def generate_pf2a_msg(self):
        self.board[0] = self.board[0] | (int(self.data.get("state_machine", 0)) & 0x07)  # 0
        self.board[0] = self.board[0] | (int(self.data.get("group_type", 1)) & 0x01) << 3  # 1
        self.board[0] = self.board[0] | (int(self.data.get('fault_state', 0)) & 0x01) << 4  # 0
        self.board[0] = self.board[0] | (int(self.data.get("work_state", 1)) & 0x03) << 6  # 1 待机，2工作

        self.board[1] = self.board[1] | (int(self.data.get('pfc_a_oc_sw', 0)) & 0x01)  # //A相软件过流
        self.board[1] = self.board[1] | (int(self.data.get('pfc_b_oc_sw', 0)) & 0x01) << 1  # //B相软件过流
        self.board[1] = self.board[1] | (int(self.data.get('pfc_c_oc_sw', 0)) & 0x01) << 2  # C相软件过流
        self.board[1] = self.board[1] | (int(self.data.get('bus_oc_sw', 0)) & 0x01) << 3  # 母线软件过流
        self.board[1] = self.board[1] | (int(self.data.get('bus_ov_sw', 0)) & 0x01) << 4  # 母线软件过压
        self.board[1] = self.board[1] | (int(self.data.get('bus_uv_sw', 0)) & 0x01) << 5  # 母线软件欠压
        self.board[1] = self.board[1] | (int(self.data.get('out_ov_sw', 0)) & 0x01) << 6  # 输出过压
        self.board[1] = self.board[1] | (int(self.data.get('out_ol_sw', 0)) & 0x01) << 7  # 输出过载

        self.board[2] = self.board[2] | (int(self.data.get('pre_ac_sw', 0)) & 0x01)  # //交流预充失败
        self.board[2] = self.board[2] | (int(self.data.get('pre_dc_sw', 0)) & 0x01) << 1  # //直流预充失败
        self.board[2] = self.board[2] | (int(self.data.get('igbt_fault_sw', 0)) & 0x01) << 2  # //igbt软件故障
        self.board[2] = self.board[2] | (int(self.data.get('ntc_otp_sw', 0)) & 0x01) << 3  # //过温报护
        # self.board[2] = self.board[2] | (int(self.data.get('can_lose_sw', 0)) & 0x01) << 4  # CAN通信故障
        self.board[2] = self.board[2] | (int(self.data.get('sensor_fault_sw', 0)) & 0x01) << 5  # //传感器校准失败
        self.board[2] = self.board[2] | (int(self.data.get('cfg_fault_sw', 0)) & 0x01) << 6  # //参数配置错误
        # self.board[2] = self.board[2] | (int(self.data.get('rsvd1', 0)) & 0x01) << 7  # 保留

        self.board[3] = self.board[3] | (int(self.data.get('pfc_a_oc_hw', 0)) & 0x01)  # A相软件过流
        self.board[3] = self.board[3] | (int(self.data.get('pfc_b_oc_hw', 0)) & 0x01) << 1  # B相软件过流
        self.board[3] = self.board[3] | (int(self.data.get('pfc_c_oc_hw', 0)) & 0x01) << 2  # C相软件过流
        self.board[3] = self.board[3] | (int(self.data.get('pfc_z_oc_hw', 0)) & 0x01) << 3  # 零序硬件过流
        self.board[3] = self.board[3] | (int(self.data.get('bus_oc_hw', 0)) & 0x01) << 4  # 母线硬件过流
        self.board[3] = self.board[3] | (int(self.data.get('bus_ov_hw', 0)) & 0x01) << 5  # 母线硬件过压
        self.board[3] = self.board[3] | (int(self.data.get('driver_fault1_hw', 0)) & 0x01) << 6  # 驱动故障1
        self.board[3] = self.board[3] | (int(self.data.get('driver_fault2_hw', 0)) & 0x01) << 7  # 驱动故障2

        self.board[4] = self.board[4] | (int(self.data.get('op_fault_hw', 0)) & 0x01)  # //op故障
        self.board[4] = self.board[4] | (int(self.data.get('rely_in_sw', 0)) & 0x01) << 1
        self.board[4] = self.board[4] | (int(self.data.get('rely_out_sw', 0)) & 0x01) << 2
        self.board[4] = self.board[4] | (int(self.data.get('leakage_circuit_fault', 0)) & 0x01) << 3
        # self.board[4] = self.board[4] | (int(self.data.get('', 0)) & 0x01) << 6  # 保留
        # self.board[4] = self.board[4] | (int(self.data.get('', 0)) & 0x01) << 5  # 保留
        # self.board[4] = self.board[4] | (int(self.data.get('', 0)) & 0x01) << 4  # 保留
        self.board[4] = self.board[4] | (int(self.data.get('module_irreparable', 0)) & 0x01) << 7  # //模块损坏

        self.board[5] = self.board[5] | (int(self.data.get('grid_uv_sw', 0)) & 0x01)  # //电网欠压
        self.board[5] = self.board[5] | (int(self.data.get('grid_open_phase', 0)) & 0x01) << 1
        self.board[5] = self.board[5] | (int(self.data.get('grid_island_sw', 0)) & 0x01) << 2
        self.board[5] = self.board[5] | (int(self.data.get('grid_ov_sw', 0)) & 0x01) << 3
        self.board[5] = self.board[5] | (int(self.data.get('grid_of_sw', 0)) & 0x01) << 4
        self.board[5] = self.board[5] | (int(self.data.get('grid_uf_sw', 0)) & 0x01) << 5
        self.board[5] = self.board[5] | (int(self.data.get('grid_unbalance', 0)) & 0x01) << 6  # //电网不平衡
        # self.board[5] = self.board[5] | (int(self.data.get('rsvd2', 0)) & 0x01) << 7 #

        self.board[6] = self.board[6] | (int(self.data.get('input_broken', 0)) & 0x03)  # //输入掉电故障
        self.board[6] = self.board[6] | (int(self.data.get('ac_ov_disconnected', 0)) & 0x01) << 1  # //交流过压脱离
        self.board[6] = self.board[6] | (int(self.data.get('short_circuit_shut_down', 0)) & 0x01) << 2  # //模块输出短路锁死
        self.board[6] = self.board[6] | (int(self.data.get('dc_ov_shut_down', 0)) & 0x01) << 3  # //直流输出过压锁死
        self.board[6] = self.board[6] | (int(self.data.get('dc_uv', 0)) & 0x01) << 4  # //直流输出欠压
        self.board[6] = self.board[6] | (int(self.data.get('dc_voltage_unbalance', 0)) & 0x01) << 5  # //直流输出不平衡
        self.board[6] = self.board[6] | (int(self.data.get('pfc_unbalance', 0)) & 0x01) << 6  # //PFC输出电压不平衡
        self.board[6] = self.board[6] | (int(self.data.get('eeprom_fault', 0)) & 0x01) << 7  # //PFC或DC EEPROM故障

        self.board[7] = self.board[7] | (int(self.data.get('fan_fault', 0)) & 0x01)
        self.board[7] = self.board[7] | (int(self.data.get('sci_is_not_ok', 0)) & 0x01) << 1
        self.board[7] = self.board[7] | (int(self.data.get('ambient_ut', 0)) & 0x01) << 2
        self.board[7] = self.board[7] | (int(self.data.get('get_same_s_nor_addr', 0)) & 0x01) << 3
        # self.board[7] = self.board[7] | (int(self.data.get('', 0)) & 0x01) << 7 # Reserved（定义国标/欧标故障）
        # self.board[7] = self.board[7] | (int(self.data.get('', 0)) & 0x01) << 6 # Reserved（定义国标/欧标故障）
        # self.board[7] = self.board[7] | (int(self.data.get('', 0)) & 0x01) << 5 # Reserved（定义国标/欧标故障）

        # self.board[8] = 0  # Bit0-Bit7 Reserved（定义国标/欧标故障）

        bus_volt = int(float(self.data.get('bus_volt', 0)) * 10)  # 母线电压 # 859.7
        self.board[9] = bus_volt & 0xFF
        self.board[10] = (bus_volt >> 8) & 0xFF

        output_volt = int(float(self.data.get('output_volt', 0)) * 10)  # 输出电压 # 405.2
        self.board[11] = output_volt & 0xFF
        self.board[12] = (output_volt >> 8) & 0xFF

        bus_volt = int(float(self.data.get('output_curr', 0)) * 100 + 30000)  # 输出电流 # 1.64
        self.board[13] = bus_volt & 0xFF
        self.board[14] = (bus_volt >> 8) & 0xFF

        bus_volt = int(float(self.data.get('a_phase_in_curr', 0)) * 100 + 30000)  # A相输入电流
        self.board[15] = bus_volt & 0xFF
        self.board[16] = (bus_volt >> 8) & 0xFF

        bus_volt = int(float(self.data.get('b_phase_in_curr', 0)) * 100 + 30000)  # B相输入电流
        self.board[17] = bus_volt & 0xFF
        self.board[18] = (bus_volt >> 8) & 0xFF

        bus_volt = int(float(self.data.get('c_phase_in_curr', 0)) * 100 + 30000)  # C相输入电流
        self.board[19] = bus_volt & 0xFF
        self.board[20] = (bus_volt >> 8) & 0xFF

        bus_volt = int(float(self.data.get('ab_line_volt', 0)) * 10)  # AB线电压 # 407.8
        self.board[21] = bus_volt & 0xFF
        self.board[22] = (bus_volt >> 8) & 0xFF

        bus_volt = int(float(self.data.get('bc_line_volt', 0)) * 10)  # BC线电压 # 407.7
        self.board[23] = bus_volt & 0xFF
        self.board[24] = (bus_volt >> 8) & 0xFF

        bus_volt = int(float(self.data.get('grid_freq', 0)) * 100)  # 电网频率 # 50
        self.board[25] = bus_volt & 0xFF
        self.board[26] = (bus_volt >> 8) & 0xFF

        bus_volt = int(float(self.data.get('active_power', 0)) * 100)  # 有功功率
        self.board[27] = bus_volt & 0xFF
        self.board[28] = (bus_volt >> 8) & 0xFF

        bus_volt = int(float(self.data.get('reactive_power', 0)) * 100)  # 无功功率
        self.board[29] = bus_volt & 0xFF
        self.board[30] = (bus_volt >> 8) & 0xFF

        bus_volt = int(float(self.data.get('power_factor', 0)) * 1000)  # 功率因素
        self.board[31] = bus_volt & 0xFF
        self.board[32] = (bus_volt >> 8) & 0xFF

        bus_volt = int(float(self.data.get('mdl_efficiency', 0)) * 1000)  # 模块效率
        self.board[33] = bus_volt & 0xFF
        self.board[34] = (bus_volt >> 8) & 0xFF

        self.board[35] = int(float(self.data.get('air_temp', 0)) + 55)  # 空气温度 # 26

        self.board[36] = int(float(self.data.get('water_temp', 0)) + 55)  # 水温度

        self.board[37] = int(float(self.data.get('sic1_temp', 0)) + 55)  # sic1温度 # 22

        self.board[38] = int(float(self.data.get('sic2_temp', 0)) + 55)  # sic2温度 # 29

        self.board[39] = int(float(self.data.get('sic3_temp', 0)) + 55)  # sic3温度 # 32

        self.board[40] = int(float(self.data.get('igbt_temp', 0)) + 55)  # igbt温度

        self.board[41] = int(float(self.data.get('inductance_temp', 0)) + 55)  # 电感温度

        # ACDC1-3 组号为1......ACDC28-30组号为10, 脚本配置该参数需配置正确
        self.board[42] = int(float(self.data.get('group_num', 0)))  # 当前组号 # 0

        self.board[43] = self.board[43] | (int(self.data.get('work_mode', 0)) & 0x01) << 6  # 工作模式（并离网状态） # 0
        self.board[43] = self.board[43] | (int(self.data.get('volt_mode', 0)) & 0x01) << 7  # 高低压模式  # 0

        # self.board[43] = self.board[43] | int(self.data.get('running_mode', 0))  # 开发代码固定写0, 这里传值不生效

        self.pack_long_frame(self.board, self.pf2a, 0x2A, 0xA0, self.addr)

    def generate_pf83_msg(self):
        self.generate_pf83_serial_number_msg()
        self.generate_pf83_hw_version_msg()
        self.generate_pf83_sw_version_msg()
        self.pf83 = {
            0x03: self.pf83_serial_number,
            0x05: self.pf83_hw_version,
            0x06: self.pf83_sw_version
        }

    def generate_pf83_serial_number_msg(self):
        """
            充电模块向发送功率控制模块定值查询应答令帧：优先级6，PF：0x83
        0x1882A0XX
        :return:
        """
        data = [0 for _ in range(38)]
        # data[0] = 0  # 充电接口标识
        data[1] = 0x04  # 设备类型 0x04 --- 充电模块  0x10 --- 双向ACDC模块
        data[2] = self.addr  # 设备通信地址
        data[3] = 0x03  # 定值序号 低位
        data[4] = 0x00  # 定值序号 高位
        data[5] = 0x01 << 7  # 操作返回 Bit7：成功标识 0x00 --- 失败 0x01 --- 成功
        serial_number = self.data.get("serial_number", "SN:220919001070000026").encode()  # 定值序号
        if len(serial_number) > 32:
            serial_number = serial_number[:32]
        for i in range(len(serial_number)):
            data[i + 6] = serial_number[i]
        self.pack_long_frame(data, self.pf83_serial_number, 0x83, 0xA0, self.addr)

    def generate_pf83_hw_version_msg(self):
        """
            充电模块向发送功率控制模块定值查询应答令帧：优先级6，PF：0x83
        0x1882A0XX
        :return:
        """
        data = [0 for _ in range(8)]
        # data[0] = 0  # 充电接口标识
        data[1] = 0x04  # 设备类型 0x04 --- 充电模块  0x10 --- 双向ACDC模块
        data[2] = self.addr  # 设备通信地址
        data[3] = 0x05  # 定值序号 低位
        data[4] = 0x00  # 定值序号 高位
        data[5] = 0x01 << 7  # 操作返回 Bit7：成功标识 0x00 --- 失败 0x01 --- 成功
        hw_version = self.data.get("hw_version", "V1.00")  # ACDC1模块硬件版本号
        hw_version = re.search("V(\d+\.\d+)", hw_version).group(1) if re.search("V(\d+\.\d+)", hw_version) else "1.00"
        hw_ver = hw_version.split('.')
        data[6] = int(hw_ver[0])
        data[7] = int(hw_ver[1])
        self.pack_long_frame(data, self.pf83_hw_version, 0x83, 0xA0, self.addr)

    def generate_pf83_sw_version_msg(self):
        """
        充电模块向发送功率控制模块定值查询应答令帧：优先级6，PF：0x83
        0x1882A0XX
        :return:
        """
        data = [0 for _ in range(9)]
        # data[0] = 0  # 充电接口标识
        data[1] = 0x04  # 设备类型 0x04 --- 充电模块  0x10 --- 双向ACDC模块
        data[2] = self.addr  # 设备通信地址
        data[3] = 0x06  # 定值序号 低位
        data[4] = 0x00  # 定值序号 高位
        data[5] = 0x01 << 7  # 操作返回 Bit7：成功标识 0x00 --- 失败 0x01 --- 成功
        sw_version = self.data.get("sw_version", "V1.00.00")  # ACDC1模块软件版本号
        sw_version = re.search("V(\d+\.\d+\.\d+)", sw_version).group(1) if re.search("V(\d+\.\d+)",
                                                                                     sw_version) else "1.00.00"
        sw_ver = sw_version.split('.')
        data[6] = int(sw_ver[0])
        data[7] = int(sw_ver[1])
        data[8] = int(sw_ver[2])
        self.pack_long_frame(data, self.pf83_sw_version, 0x83, 0xA0, self.addr)

    def pack_long_frame(self, data, result, pf, ps, sa):
        """
        根据开发代码实现的python 打包多帧
        :param data:  待打包的数据
        :param result: 打包后赋值的实例变量
        :param pf: 发送的优先级
        :param ps: 发送的目的地址
        :param sa: 发送的源地址
        :return:
        """
        data_len = len(data)
        if (data_len + 3 + 2) % 7 == 0:
            send_pkg_num = (data_len + 3 + 2) // 7
        else:
            send_pkg_num = (data_len + 3 + 2) // 7 + 1
        send_data_pack = [0 for _ in range(send_pkg_num * 8)]
        send_data_pack[0] = 1
        send_data_pack[1] = send_pkg_num
        send_data_pack[2] = data_len & 0xFF
        send_data_pack[3] = (data_len >> 8) & 0xFF
        send_data_pack[4:8] = data[0:4]
        sum_check = sum(send_data_pack[1:4])
        for i in range(data_len):
            sum_check += data[i]
        k = 4
        for i in range(8, send_pkg_num * 8):
            if i % 8 == 0:
                send_data_pack[i] = i // 8 + 1
                continue
            if k < data_len:
                send_data_pack[i] = data[k]
                k += 1
        if (data_len + 3) % 7 == 0:  # 校验位在下一帧开头
            send_data_pack[data_len + 3 + send_pkg_num] = sum_check & 0xFF
            send_data_pack[data_len + 4 + send_pkg_num] = (sum_check >> 8) & 0xFF
        elif (data_len + 3) % 7 == 6:  # 校验位跨越两帧
            send_data_pack[data_len + 2 + send_pkg_num] = sum_check & 0xFF
            send_data_pack[data_len + 4 + send_pkg_num] = (sum_check >> 8) & 0xFF
        else:  # 校验位和数据在同一帧
            send_data_pack[data_len + 3 + send_pkg_num] = sum_check & 0xFF
            send_data_pack[data_len + 4 + send_pkg_num] = (sum_check >> 8) & 0xFF
        for i in range(send_pkg_num):
            arbitration_id = (0x06 << 26) | (pf << 16) | (ps << 8) | sa
            msg = can.Message(arbitration_id=arbitration_id,
                              data=send_data_pack[8 * i:8 * i + 8],
                              is_extended_id=True)
            result.append(msg)
        return result


if __name__ == '__main__':
    def deal_acdc_data(rec_json, glob_json):
        """

        :param rec_json:
        :param glob_json:
        :return:
        """
        if isinstance(rec_json, dict):
            for name, val in rec_json.items():
                if isinstance(val, dict):
                    deal_acdc_data(val, glob_json)
                else:
                    glob_json[name] = val
        return glob_json


    data = {"acdc2": {
        "acdc_real": {"100062": "500.0", "100063": "500.0", "100064": "150.0", "100065": "150.0", "100066": "150.0",
                      "100067": "150.0", "100068": "250.0", "100069": "250.0", "100070": "35.0", "100071": "50.0",
                      "100072": "50.0", "100073": "1", "100074": "1", "100075": "100", "100076": "100", "100077": "100",
                      "100078": "100", "100079": "100", "100080": "100", "100081": "100", "100082": "1"},
        "acdc_state": {"102020": "1", "102021": "0", "102022": "0", "102023": "0", "102024": "0", "102025": "0",
                       "102026": "0", "721128": "1"}}}
    branch = 2
    data = deal_acdc_data(data, {})
    data = acdc_key_to_variable(branch, data)
    obj = AcdcMsg(data, branch)
    for msg in obj.pf2a:
        print(msg)
