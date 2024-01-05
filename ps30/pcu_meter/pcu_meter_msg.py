# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/8/30 17:12
# @File:pcu_meter_msg.py
from binascii import *

import crcmod

from utils.log import log


class PcuMeterMsg:

    def __init__(self):
        self.start_server_flag = False
        self.slave_1_data = ""
        self.slave_2_data = ""
        self.slave_3_data = ""
        self.slave_4_data = ""
        self.slave_1 = [0 for _ in range(228)]
        self.slave_2 = [0 for _ in range(228)]
        self.slave_3 = [0 for _ in range(228)]
        self.slave_4 = [0 for _ in range(228)]
        self.set_pt_value()
        self.set_ct_value()
        self.set_dpt_dct_value()
        self.set_dpq_value()

    def meter_data_init(self):
        slave_1_temp = self.crc16Add([0x01, 0x03, 0xE4, ], self.slave_1)
        slave_2_temp = self.crc16Add([0x02, 0x03, 0xE4, ], self.slave_2)
        slave_3_temp = self.crc16Add([0x03, 0x03, 0xE4, ], self.slave_3)
        slave_4_temp = self.crc16Add([0x04, 0x03, 0xE4, ], self.slave_4)
        self.slave_1_data = self.data_covert(slave_1_temp)
        self.slave_2_data = self.data_covert(slave_2_temp)
        self.slave_3_data = self.data_covert(slave_3_temp)
        self.slave_4_data = self.data_covert(slave_4_temp)

    def crc16Add(self, prefix, tem,):
        prefix.extend(tem)
        res = []
        for p in prefix:
            temp = hex(p).replace("0x", "")
            if len(temp) == 1:
                temp = f"0{temp}"
            res.append(temp)
        read = " ".join(res)
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
        data = read.replace(" ", "")  # 消除空格
        readcrcout = hex(crc16(unhexlify(data))).upper()
        str_list = list(readcrcout)
        if len(str_list) == 5:
            str_list.insert(2, '0')  # 位数不足补0，因为一般最少是5个
        crc_data = "".join(str_list)  # 用""把数组的每一位结合起来  组成新的字符串
        read = read.strip() + ' ' + crc_data[4:] + ' ' + crc_data[2:4]  # 把源代码和crc校验码连接起来
        return read

    def data_covert(self, data):
        t = []
        for val in data.split(" "):
            if val.strip():
                t.append(int(val.strip(), base=16))
        return bytearray(t)

    def data_float_to_int(self, data):
        """
    
        :param data:
        :return:
        """
        try:
            data = int(data)
            return data
        except Exception as e:
            pass
        try:
            data = int(float(data))
            return data
        except Exception as e:
            raise e
    
    def data_float_x1000_to_int(self, data):
        """
        
        :param data: 
        :return: 
        """
        try:
            data = float(data)
            return int(data * 1000)
        except Exception as e:
            raise e

    def set_pt_value(self, pt=0x0001):
        """
        PT变化:[1, 9999]
        :param pt:
        :return:
        """
        self.slave_1[6] = 0x0
        self.slave_1[7] = 0x1
        self.slave_2[6] = 0x0
        self.slave_2[7] = 0x1
        self.slave_3[6] = 0x0
        self.slave_3[7] = 0x1
        self.slave_4[6] = 0x0
        self.slave_4[7] = 0x1

    def set_ct_value(self, ct=0x0001):
        """
        CT变化:[1, 9999]
        :param ct:
        :return:
        """
        self.slave_1[8] = 0x0
        self.slave_1[9] = 0x1
        self.slave_2[8] = 0x0
        self.slave_2[9] = 0x1
        self.slave_3[8] = 0x0
        self.slave_3[9] = 0x1
        self.slave_4[8] = 0x0
        self.slave_4[9] = 0x1

    def set_dpt_dct_value(self, dpt=4, dct=4):
        """
        DPT高字节:[3, 7], DCT低字节:[1, 5]
        :param dpt:
        :param dct:
        :return:
        """
        self.slave_1[70] = 0x4
        self.slave_1[71] = 0x4
        self.slave_2[70] = 0x4
        self.slave_2[71] = 0x4
        self.slave_3[70] = 0x4
        self.slave_3[71] = 0x4
        self.slave_4[70] = 0x4
        self.slave_4[71] = 0x4

    def set_dpq_value(self, pq_h=4, pq_l=0):
        """
            小数点PQ高字节:[4, 10], PQ符号低字节:[0, 1]
        :param pq_h:
        :param pq_l:
        :return:
        """
        self.slave_1[72] = 0x4
        self.slave_1[73] = 0x0
        self.slave_2[72] = 0x4
        self.slave_2[73] = 0x0
        self.slave_3[72] = 0x4
        self.slave_3[73] = 0x0
        self.slave_4[72] = 0x4
        self.slave_4[73] = 0x0

    def set_meter_real_value(self, meter_param):
        """
        handle pcu_meter real_info data
        :return:
        """
        log.debug(f"<PCU_Meter>:<meter_Msg>enter set_meter_real_value func")
        # meter1 real info
        if meter_param.get('meter1_A_phase_voltage', "") != "":
            meter1_A_phase_voltage = self.data_float_to_int(meter_param.get('meter1_A_phase_voltage', 0))
            self.slave_1[74] = (meter1_A_phase_voltage >> 8) & 0xFF
            self.slave_1[75] = meter1_A_phase_voltage & 0xFF
        if meter_param.get('meter1_B_phase_voltage', "") != "":
            meter1_B_phase_voltage = self.data_float_to_int(meter_param.get('meter1_B_phase_voltage', 0))
            self.slave_1[76] = (meter1_B_phase_voltage >> 8) & 0xFF
            self.slave_1[77] = meter1_B_phase_voltage & 0xFF
        if meter_param.get('meter1_C_phase_voltage', "") != "":
            meter1_C_phase_voltage = self.data_float_to_int(meter_param.get('meter1_C_phase_voltage', 0))
            self.slave_1[78] = (meter1_C_phase_voltage >> 8) & 0xFF
            self.slave_1[79] = meter1_C_phase_voltage & 0xFF
        if meter_param.get('meter1_A_line_voltage', "") != "":
            meter1_A_line_voltage = self.data_float_to_int(meter_param.get('meter1_A_line_voltage', 0))
            self.slave_1[80] = (meter1_A_line_voltage >> 8) & 0xFF
            self.slave_1[81] = meter1_A_line_voltage & 0xFF
        if meter_param.get('meter1_B_line_voltage', "") != "":
            meter1_B_line_voltage = self.data_float_to_int(meter_param.get('meter1_B_line_voltage', 0))
            self.slave_1[82] = (meter1_B_line_voltage >> 8) & 0xFF
            self.slave_1[83] = meter1_B_line_voltage & 0xFF
        if meter_param.get('meter1_C_line_voltage', "") != "":
            meter1_C_line_voltage = self.data_float_to_int(meter_param.get('meter1_C_line_voltage', 0))
            self.slave_1[84] = (meter1_C_line_voltage >> 8) & 0xFF
            self.slave_1[85] = meter1_C_line_voltage & 0xFF
        if meter_param.get('meter1_A_phase_current', "") != "":
            meter1_A_phase_current = self.data_float_to_int(meter_param.get('meter1_A_phase_current', 0))
            self.slave_1[86] = (meter1_A_phase_current >> 8) & 0xFF
            self.slave_1[87] = meter1_A_phase_current & 0xFF
        if meter_param.get('meter1_B_phase_current', "") != "":
            meter1_B_phase_current = self.data_float_to_int(meter_param.get('meter1_B_phase_current', 0))
            self.slave_1[88] = (meter1_B_phase_current >> 8) & 0xFF
            self.slave_1[89] = meter1_B_phase_current & 0xFF
        if meter_param.get('meter1_C_phase_current', "") != "":
            meter1_C_phase_current = self.data_float_to_int(meter_param.get('meter1_C_phase_current', 0))
            self.slave_1[90] = (meter1_C_phase_current >> 8) & 0xFF
            self.slave_1[91] = meter1_C_phase_current & 0xFF
        if meter_param.get('meter1_total_power', "") != "":
            meter1_total_power = self.data_float_x1000_to_int(meter_param.get('meter1_total_power', 0))
            self.slave_1[98] = (meter1_total_power >> 8) & 0xFF
            self.slave_1[99] = meter1_total_power & 0xFF
        if meter_param.get('meter1_power_factor', "") != "":
            meter1_power_factor = self.data_float_x1000_to_int(meter_param.get('meter1_power_factor', 0))
            self.slave_1[114] = (meter1_power_factor >> 8) & 0xFF
            self.slave_1[115] = meter1_power_factor & 0xFF
        if meter_param.get('meter1_energy', "") != "":
            meter1_energy = self.data_float_x1000_to_int(meter_param.get('meter1_energy', 0))
            meter1_energy_h = (meter1_energy >> 16) & 0x0000FFFF
            meter1_energy_l = meter1_energy & 0x0000FFFF
            self.slave_1[126] = (meter1_energy_h >> 8) & 0xFF
            self.slave_1[127] = meter1_energy_h & 0xFF
            self.slave_1[128] = (meter1_energy_l >> 8) & 0xFF
            self.slave_1[129] = meter1_energy_l & 0xFF
        if meter_param.get('meter1_sharp_secondary_energy', "") != "":
            # 下面参数的计算是基于PT， CT 变化默认配置为1, 根据开发代码上的计算公式，传输的数据和云端的数据默认为1000倍的差别
            meter1_sharp_secondary_energy = self.data_float_x1000_to_int(meter_param.get('meter1_sharp_secondary_energy',  0))
            meter1_sharp_secondary_energy_h = (meter1_sharp_secondary_energy >> 16) & 0x0000FFFF
            meter1_sharp_secondary_energy_l = meter1_sharp_secondary_energy & 0x0000FFFF
            self.slave_1[168] = (meter1_sharp_secondary_energy_h >> 8) & 0xFF
            self.slave_1[169] = meter1_sharp_secondary_energy_h & 0xFF
            self.slave_1[170] = (meter1_sharp_secondary_energy_l >> 8) & 0xFF
            self.slave_1[171] = meter1_sharp_secondary_energy_l & 0xFF
        if meter_param.get('meter1_peak_secondary_energy', "") != "":
            meter1_peak_secondary_energy = self.data_float_x1000_to_int(meter_param.get('meter1_peak_secondary_energy', 0))
            meter1_peak_secondary_energy_h = (meter1_peak_secondary_energy >> 16) & 0x0000FFFF
            meter1_peak_secondary_energy_l = meter1_peak_secondary_energy & 0x0000FFFF
            self.slave_1[172] = (meter1_peak_secondary_energy_h >> 8) & 0xFF
            self.slave_1[173] = meter1_peak_secondary_energy_h & 0xFF
            self.slave_1[174] = (meter1_peak_secondary_energy_l >> 8) & 0xFF
            self.slave_1[175] = meter1_peak_secondary_energy_l & 0xFF
        if meter_param.get('meter1_flat_secondary_energy', "") != "":
            meter1_flat_secondary_energy = self.data_float_x1000_to_int(meter_param.get('meter1_flat_secondary_energy', 0))
            meter1_flat_secondary_energy_h = (meter1_flat_secondary_energy >> 16) & 0x0000FFFF
            meter1_flat_secondary_energy_l = meter1_flat_secondary_energy & 0x0000FFFF
            self.slave_1[176] = (meter1_flat_secondary_energy_h >> 8) & 0xFF
            self.slave_1[177] = meter1_flat_secondary_energy_h & 0xFF
            self.slave_1[178] = (meter1_flat_secondary_energy_l >> 8) & 0xFF
            self.slave_1[179] = meter1_flat_secondary_energy_l & 0xFF
        if meter_param.get('meter1_valley_secondary_energy', "") != "":
            meter1_valley_secondary_energy = self.data_float_x1000_to_int(meter_param.get('meter1_valley_secondary_energy', 0))
            meter1_valley_secondary_energy_h = (meter1_valley_secondary_energy >> 16) & 0x0000FFFF
            meter1_valley_secondary_energy_l = meter1_valley_secondary_energy & 0x0000FFFF
            self.slave_1[180] = (meter1_valley_secondary_energy_h >> 8) & 0xFF
            self.slave_1[181] = meter1_valley_secondary_energy_h & 0xFF
            self.slave_1[182] = (meter1_valley_secondary_energy_l >> 8) & 0xFF
            self.slave_1[183] = meter1_valley_secondary_energy_l & 0xFF

        # meter2 real info
        if meter_param.get('meter2_A_phase_voltage', "") != "":
            meter2_A_phase_voltage = self.data_float_to_int(meter_param.get('meter2_A_phase_voltage', 0))
            self.slave_2[74] = (meter2_A_phase_voltage >> 8) & 0xFF
            self.slave_2[75] = meter2_A_phase_voltage & 0xFF
        if meter_param.get('meter2_B_phase_voltage', "") != "":
            meter2_B_phase_voltage = self.data_float_to_int(meter_param.get('meter2_B_phase_voltage', 0))
            self.slave_2[76] = (meter2_B_phase_voltage >> 8) & 0xFF
            self.slave_2[77] = meter2_B_phase_voltage & 0xFF
        if meter_param.get('meter2_C_phase_voltage', "") != "":
            meter2_C_phase_voltage = self.data_float_to_int(meter_param.get('meter2_C_phase_voltage', 0))
            self.slave_2[78] = (meter2_C_phase_voltage >> 8) & 0xFF
            self.slave_2[79] = meter2_C_phase_voltage & 0xFF
        if meter_param.get('meter2_A_line_voltage', "") != "":
            meter2_A_line_voltage = self.data_float_to_int(meter_param.get('meter2_A_line_voltage', 0))
            self.slave_2[80] = (meter2_A_line_voltage >> 8) & 0xFF
            self.slave_2[81] = meter2_A_line_voltage & 0xFF
        if meter_param.get('meter2_B_line_voltage', "") != "":
            meter2_B_line_voltage = self.data_float_to_int(meter_param.get('meter2_B_line_voltage', 0))
            self.slave_2[82] = (meter2_B_line_voltage >> 8) & 0xFF
            self.slave_2[83] = meter2_B_line_voltage & 0xFF
        if meter_param.get('meter2_C_line_voltage', "") != "":
            meter2_C_line_voltage = self.data_float_to_int(meter_param.get('meter2_C_line_voltage', 0))
            self.slave_2[84] = (meter2_C_line_voltage >> 8) & 0xFF
            self.slave_2[85] = meter2_C_line_voltage & 0xFF
        if meter_param.get('meter2_A_phase_current', "") != "":
            meter2_A_phase_current = self.data_float_to_int(meter_param.get('meter2_A_phase_current', 0))
            self.slave_2[86] = (meter2_A_phase_current >> 8) & 0xFF
            self.slave_2[87] = meter2_A_phase_current & 0xFF
        if meter_param.get('meter2_B_phase_current', "") != "":
            meter2_B_phase_current = self.data_float_to_int(meter_param.get('meter2_B_phase_current', 0))
            self.slave_2[88] = (meter2_B_phase_current >> 8) & 0xFF
            self.slave_2[89] = meter2_B_phase_current & 0xFF
        if meter_param.get('meter2_C_phase_current', "") != "":
            meter2_C_phase_current = self.data_float_to_int(meter_param.get('meter2_C_phase_current', 0))
            self.slave_2[90] = (meter2_C_phase_current >> 8) & 0xFF
            self.slave_2[91] = meter2_C_phase_current & 0xFF
        if meter_param.get('meter2_total_power', "") != "":
            meter2_total_power = self.data_float_x1000_to_int(meter_param.get('meter2_total_power', 0))
            self.slave_2[98] = (meter2_total_power >> 8) & 0xFF
            self.slave_2[99] = meter2_total_power & 0xFF
        if meter_param.get('meter2_power_factor', "") != "":
            meter2_power_factor = self.data_float_x1000_to_int(meter_param.get('meter2_power_factor', 0))
            self.slave_2[114] = (meter2_power_factor >> 8) & 0xFF
            self.slave_2[115] = meter2_power_factor & 0xFF
        if meter_param.get('meter2_energy') != "":
            meter2_energy = self.data_float_x1000_to_int(meter_param.get('meter2_energy', 0))
            meter2_energy_h = (meter2_energy >> 16) & 0x0000FFFF
            meter2_energy_l = meter2_energy & 0x0000FFFF
            self.slave_2[126] = (meter2_energy_h >> 8) & 0xFF
            self.slave_2[127] = meter2_energy_h & 0xFF
            self.slave_2[128] = (meter2_energy_l >> 8) & 0xFF
            self.slave_2[129] = meter2_energy_l & 0xFF
        if meter_param.get('meter2_sharp_secondary_energy', "") != "":
            meter2_sharp_secondary_energy = self.data_float_x1000_to_int(meter_param.get('meter2_sharp_secondary_energy', 0))
            meter2_sharp_secondary_energy_h = (meter2_sharp_secondary_energy >> 16) & 0x0000FFFF
            meter2_sharp_secondary_energy_l = meter2_sharp_secondary_energy & 0x0000FFFF
            self.slave_2[168] = (meter2_sharp_secondary_energy_h >> 8) & 0xFF
            self.slave_2[169] = meter2_sharp_secondary_energy_h & 0xFF
            self.slave_2[170] = (meter2_sharp_secondary_energy_l >> 8) & 0xFF
            self.slave_2[171] = meter2_sharp_secondary_energy_l & 0xFF
        if meter_param.get('meter2_peak_secondary_energy', "") != "":
            meter2_peak_secondary_energy = self.data_float_x1000_to_int(meter_param.get('meter2_peak_secondary_energy', 0))
            meter2_peak_secondary_energy_h = (meter2_peak_secondary_energy >> 16) & 0x0000FFFF
            meter2_peak_secondary_energy_l = meter2_peak_secondary_energy & 0x0000FFFF
            self.slave_2[172] = (meter2_peak_secondary_energy_h >> 8) & 0xFF
            self.slave_2[173] = meter2_peak_secondary_energy_h & 0xFF
            self.slave_2[174] = (meter2_peak_secondary_energy_l >> 8) & 0xFF
            self.slave_2[175] = meter2_peak_secondary_energy_l & 0xFF
        if meter_param.get('meter2_flat_secondary_energy', "") != "":
            meter2_flat_secondary_energy = self.data_float_x1000_to_int(meter_param.get('meter2_flat_secondary_energy', 0))
            meter2_flat_secondary_energy_h = (meter2_flat_secondary_energy >> 16) & 0x0000FFFF
            meter2_flat_secondary_energy_l = meter2_flat_secondary_energy & 0x0000FFFF
            self.slave_2[176] = (meter2_flat_secondary_energy_h >> 8) & 0xFF
            self.slave_2[177] = meter2_flat_secondary_energy_h & 0xFF
            self.slave_2[178] = (meter2_flat_secondary_energy_l >> 8) & 0xFF
            self.slave_2[179] = meter2_flat_secondary_energy_l & 0xFF
        if meter_param.get('meter2_valley_secondary_energy', "") != "":
            meter2_valley_secondary_energy = self.data_float_x1000_to_int(meter_param.get('meter2_valley_secondary_energy', 0))
            meter2_valley_secondary_energy_h = (meter2_valley_secondary_energy >> 16) & 0x0000FFFF
            meter2_valley_secondary_energy_l = meter2_valley_secondary_energy & 0x0000FFFF
            self.slave_2[180] = (meter2_valley_secondary_energy_h >> 8) & 0xFF
            self.slave_2[181] = meter2_valley_secondary_energy_h & 0xFF
            self.slave_2[182] = (meter2_valley_secondary_energy_l >> 8) & 0xFF
            self.slave_2[183] = meter2_valley_secondary_energy_l & 0xFF

        # meter3 real info
        if meter_param.get('meter3_A_phase_voltage', "") != "":
            meter3_A_phase_voltage = self.data_float_to_int(meter_param.get('meter3_A_phase_voltage', 0))
            self.slave_3[74] = (meter3_A_phase_voltage >> 8) & 0xFF
            self.slave_3[75] = meter3_A_phase_voltage & 0xFF
        if meter_param.get('meter3_B_phase_voltage', "") != "":
            meter3_B_phase_voltage = self.data_float_to_int(meter_param.get('meter3_B_phase_voltage', 0))
            self.slave_3[76] = (meter3_B_phase_voltage >> 8) & 0xFF
            self.slave_3[77] = meter3_B_phase_voltage & 0xFF
        if meter_param.get('meter3_C_phase_voltage', "") != "":
            meter3_C_phase_voltage = self.data_float_to_int(meter_param.get('meter3_C_phase_voltage', 0))
            self.slave_3[78] = (meter3_C_phase_voltage >> 8) & 0xFF
            self.slave_3[79] = meter3_C_phase_voltage & 0xFF
        if meter_param.get('meter3_A_line_voltage', "") != "":
            meter3_A_line_voltage = self.data_float_to_int(meter_param.get('meter3_A_line_voltage', 0))
            self.slave_3[80] = (meter3_A_line_voltage >> 8) & 0xFF
            self.slave_3[81] = meter3_A_line_voltage & 0xFF
        if meter_param.get('meter3_B_line_voltage', "") != "":
            meter3_B_line_voltage = self.data_float_to_int(meter_param.get('meter3_B_line_voltage', 0))
            self.slave_3[82] = (meter3_B_line_voltage >> 8) & 0xFF
            self.slave_3[83] = meter3_B_line_voltage & 0xFF
        if meter_param.get('meter3_C_line_voltage', "") != "":
            meter3_C_line_voltage = self.data_float_to_int(meter_param.get('meter3_C_line_voltage', 0))
            self.slave_3[84] = (meter3_C_line_voltage >> 8) & 0xFF
            self.slave_3[85] = meter3_C_line_voltage & 0xFF
        if meter_param.get('meter3_A_phase_current', "") != "":
            meter3_A_phase_current = self.data_float_to_int(meter_param.get('meter3_A_phase_current', 0))
            self.slave_3[86] = (meter3_A_phase_current >> 8) & 0xFF
            self.slave_3[87] = meter3_A_phase_current & 0xFF
        if meter_param.get('meter3_B_phase_current', "") != "":
            meter3_B_phase_current = self.data_float_to_int(meter_param.get('meter3_B_phase_current', 0))
            self.slave_3[88] = (meter3_B_phase_current >> 8) & 0xFF
            self.slave_3[89] = meter3_B_phase_current & 0xFF
        if meter_param.get('meter3_C_phase_current', "") != "":
            meter3_C_phase_current = self.data_float_to_int(meter_param.get('meter3_C_phase_current', 0))
            self.slave_3[90] = (meter3_C_phase_current >> 8) & 0xFF
            self.slave_3[91] = meter3_C_phase_current & 0xFF
        if meter_param.get('meter3_total_power', "") != "":
            meter3_total_power = self.data_float_x1000_to_int(meter_param.get('meter3_total_power', 0))
            self.slave_3[98] = (meter3_total_power >> 8) & 0xFF
            self.slave_3[99] = meter3_total_power & 0xFF
        if meter_param.get('meter3_power_factor', "") != "":
            meter3_power_factor = self.data_float_x1000_to_int(meter_param.get('meter3_power_factor', 0))
            self.slave_3[114] = (meter3_power_factor >> 8) & 0xFF
            self.slave_3[115] = meter3_power_factor & 0xFF
        if meter_param.get('meter3_energy', 0):
            meter3_energy = self.data_float_x1000_to_int(meter_param.get('meter3_energy', 0))
            meter3_energy_h = (meter3_energy >> 16) & 0x0000FFFF
            meter3_energy_l = meter3_energy & 0x0000FFFF
            self.slave_3[126] = (meter3_energy_h >> 8) & 0xFF
            self.slave_3[127] = meter3_energy_h & 0xFF
            self.slave_3[128] = (meter3_energy_l >> 8) & 0xFF
            self.slave_3[129] = meter3_energy_l & 0xFF
        if meter_param.get('meter3_sharp_secondary_energy', "") != "":
            meter3_sharp_secondary_energy = self.data_float_x1000_to_int(meter_param.get('meter3_sharp_secondary_energy', 0))
            meter3_sharp_secondary_energy_h = (meter3_sharp_secondary_energy >> 16) & 0x0000FFFF
            meter3_sharp_secondary_energy_l = meter3_sharp_secondary_energy & 0x0000FFFF
            self.slave_3[168] = (meter3_sharp_secondary_energy_h >> 8) & 0xFF
            self.slave_3[169] = meter3_sharp_secondary_energy_h & 0xFF
            self.slave_3[170] = (meter3_sharp_secondary_energy_l >> 8) & 0xFF
            self.slave_3[171] = meter3_sharp_secondary_energy_l & 0xFF
        if meter_param.get('meter3_peak_secondary_energy', "") != "":
            meter3_peak_secondary_energy = self.data_float_x1000_to_int(meter_param.get('meter3_peak_secondary_energy', 0))
            meter3_peak_secondary_energy_h = (meter3_peak_secondary_energy >> 16) & 0x0000FFFF
            meter3_peak_secondary_energy_l = meter3_peak_secondary_energy & 0x0000FFFF
            self.slave_3[172] = (meter3_peak_secondary_energy_h >> 8) & 0xFF
            self.slave_3[173] = meter3_peak_secondary_energy_h & 0xFF
            self.slave_3[174] = (meter3_peak_secondary_energy_l >> 8) & 0xFF
            self.slave_3[175] = meter3_peak_secondary_energy_l & 0xFF
        if meter_param.get('meter3_flat_secondary_energy', "") != "":
            meter3_flat_secondary_energy = self.data_float_x1000_to_int(meter_param.get('meter3_flat_secondary_energy', 0))
            meter3_flat_secondary_energy_h = (meter3_flat_secondary_energy >> 16) & 0x0000FFFF
            meter3_flat_secondary_energy_l = meter3_flat_secondary_energy & 0x0000FFFF
            self.slave_3[176] = (meter3_flat_secondary_energy_h >> 8) & 0xFF
            self.slave_3[177] = meter3_flat_secondary_energy_h & 0xFF
            self.slave_3[178] = (meter3_flat_secondary_energy_l >> 8) & 0xFF
            self.slave_3[179] = meter3_flat_secondary_energy_l & 0xFF
        if meter_param.get('meter3_valley_secondary_energy', "") != "":
            meter3_valley_secondary_energy = self.data_float_x1000_to_int(meter_param.get('meter3_valley_secondary_energy', 0))
            meter3_valley_secondary_energy_h = (meter3_valley_secondary_energy >> 16) & 0x0000FFFF
            meter3_valley_secondary_energy_l = meter3_valley_secondary_energy & 0x0000FFFF
            self.slave_3[180] = (meter3_valley_secondary_energy_h >> 8) & 0xFF
            self.slave_3[181] = meter3_valley_secondary_energy_h & 0xFF
            self.slave_3[182] = (meter3_valley_secondary_energy_l >> 8) & 0xFF
            self.slave_3[183] = meter3_valley_secondary_energy_l & 0xFF


        # meter4 real info
        if meter_param.get('meter4_A_phase_voltage', "") != "":
            meter4_A_phase_voltage = self.data_float_to_int(meter_param.get('meter4_A_phase_voltage', 0))
            self.slave_4[74] = (meter4_A_phase_voltage >> 8) & 0xFF
            self.slave_4[75] = meter4_A_phase_voltage & 0xFF
        if meter_param.get('meter4_B_phase_voltage', "") != "":
            meter4_B_phase_voltage = self.data_float_to_int(meter_param.get('meter4_B_phase_voltage', 0))
            self.slave_4[76] = (meter4_B_phase_voltage >> 8) & 0xFF
            self.slave_4[77] = meter4_B_phase_voltage & 0xFF
        if meter_param.get('meter4_C_phase_voltage', "") != "":
            meter4_C_phase_voltage = self.data_float_to_int(meter_param.get('meter4_C_phase_voltage', 0))
            self.slave_4[78] = (meter4_C_phase_voltage >> 8) & 0xFF
            self.slave_4[79] = meter4_C_phase_voltage & 0xFF
        if meter_param.get('meter4_A_line_voltage', "") != "":
            meter4_A_line_voltage = self.data_float_to_int(meter_param.get('meter4_A_line_voltage', 0))
            self.slave_4[80] = (meter4_A_line_voltage >> 8) & 0xFF
            self.slave_4[81] = meter4_A_line_voltage & 0xFF
        if meter_param.get('meter4_B_line_voltage', "") != "":
            meter4_B_line_voltage = self.data_float_to_int(meter_param.get('meter4_B_line_voltage', 0))
            self.slave_4[82] = (meter4_B_line_voltage >> 8) & 0xFF
            self.slave_4[83] = meter4_B_line_voltage & 0xFF
        if meter_param.get('meter4_C_line_voltage', "") != "":
            meter4_C_line_voltage = self.data_float_to_int(meter_param.get('meter4_C_line_voltage', 0))
            self.slave_4[84] = (meter4_C_line_voltage >> 8) & 0xFF
            self.slave_4[85] = meter4_C_line_voltage & 0xFF
        if meter_param.get('meter4_A_phase_current', "") != "":
            meter4_A_phase_current = self.data_float_to_int(meter_param.get('meter4_A_phase_current', 0))
            self.slave_4[86] = (meter4_A_phase_current >> 8) & 0xFF
            self.slave_4[87] = meter4_A_phase_current & 0xFF
        if meter_param.get('meter4_B_phase_current', "") != "":
            meter4_B_phase_current = self.data_float_to_int(meter_param.get('meter4_B_phase_current', 0))
            self.slave_4[88] = (meter4_B_phase_current >> 8) & 0xFF
            self.slave_4[89] = meter4_B_phase_current & 0xFF
        if meter_param.get('meter4_C_phase_current', "") != "":
            meter4_C_phase_current = self.data_float_to_int(meter_param.get('meter4_C_phase_current', 0))
            self.slave_4[90] = (meter4_C_phase_current >> 8) & 0xFF
            self.slave_4[91] = meter4_C_phase_current & 0xFF
        if meter_param.get('meter4_total_power', "") != "":
            meter4_total_power = self.data_float_x1000_to_int(meter_param.get('meter4_total_power', 0))
            self.slave_4[98] = (meter4_total_power >> 8) & 0xFF
            self.slave_4[99] = meter4_total_power & 0xFF
        if meter_param.get('meter4_power_factor', "") != "":
            meter4_power_factor = self.data_float_x1000_to_int(meter_param.get('meter4_power_factor', 0))
            self.slave_4[114] = (meter4_power_factor >> 8) & 0xFF
            self.slave_4[115] = meter4_power_factor & 0xFF
        if meter_param.get('meter4_energy', 0):
            meter4_energy = self.data_float_x1000_to_int(meter_param.get('meter4_energy', 0))
            meter4_energy_h = (meter4_energy >> 16) & 0x0000FFFF
            meter4_energy_l = meter4_energy & 0x0000FFFF
            self.slave_4[126] = (meter4_energy_h >> 8) & 0xFF
            self.slave_4[127] = meter4_energy_h & 0xFF
            self.slave_4[128] = (meter4_energy_l >> 8) & 0xFF
            self.slave_4[129] = meter4_energy_l & 0xFF
        if meter_param.get('meter4_sharp_secondary_energy', "") != "":
            meter4_sharp_secondary_energy = self.data_float_x1000_to_int(meter_param.get('meter4_sharp_secondary_energy', 0))
            meter4_sharp_secondary_energy_h = (meter4_sharp_secondary_energy >> 16) & 0x0000FFFF
            meter4_sharp_secondary_energy_l = meter4_sharp_secondary_energy & 0x0000FFFF
            self.slave_4[168] = (meter4_sharp_secondary_energy_h >> 8) & 0xFF
            self.slave_4[169] = meter4_sharp_secondary_energy_h & 0xFF
            self.slave_4[170] = (meter4_sharp_secondary_energy_l >> 8) & 0xFF
            self.slave_4[171] = meter4_sharp_secondary_energy_l & 0xFF
        if meter_param.get('meter4_peak_secondary_energy', "") != "":
            meter4_peak_secondary_energy = self.data_float_x1000_to_int(meter_param.get('meter4_peak_secondary_energy', 0))
            meter4_peak_secondary_energy_h = (meter4_peak_secondary_energy >> 16) & 0x0000FFFF
            meter4_peak_secondary_energy_l = meter4_peak_secondary_energy & 0x0000FFFF
            self.slave_4[172] = (meter4_peak_secondary_energy_h >> 8) & 0xFF
            self.slave_4[173] = meter4_peak_secondary_energy_h & 0xFF
            self.slave_4[174] = (meter4_peak_secondary_energy_l >> 8) & 0xFF
            self.slave_4[175] = meter4_peak_secondary_energy_l & 0xFF
        if meter_param.get('meter4_flat_secondary_energy', "") != "":
            meter4_flat_secondary_energy = self.data_float_x1000_to_int(meter_param.get('meter4_flat_secondary_energy', 0))
            meter4_flat_secondary_energy_h = (meter4_flat_secondary_energy >> 16) & 0x0000FFFF
            meter4_flat_secondary_energy_l = meter4_flat_secondary_energy & 0x0000FFFF
            self.slave_4[176] = (meter4_flat_secondary_energy_h >> 8) & 0xFF
            self.slave_4[177] = meter4_flat_secondary_energy_h & 0xFF
            self.slave_4[178] = (meter4_flat_secondary_energy_l >> 8) & 0xFF
            self.slave_4[179] = meter4_flat_secondary_energy_l & 0xFF
        if meter_param.get('meter4_valley_secondary_energy', "") != "":
            meter4_valley_secondary_energy = self.data_float_x1000_to_int(meter_param.get('meter4_valley_secondary_energy', 0))
            meter4_valley_secondary_energy_h = (meter4_valley_secondary_energy >> 16) & 0x0000FFFF
            meter4_valley_secondary_energy_l = meter4_valley_secondary_energy & 0x0000FFFF
            self.slave_4[180] = (meter4_valley_secondary_energy_h >> 8) & 0xFF
            self.slave_4[181] = meter4_valley_secondary_energy_h & 0xFF
            self.slave_4[182] = (meter4_valley_secondary_energy_l >> 8) & 0xFF
            self.slave_4[183] = meter4_valley_secondary_energy_l & 0xFF
        # log.debug(f"<PCU_Meter>:<meter_Msg>exit set pcu_meter real value success")
