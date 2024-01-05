# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/7/21 13:05
# @File:bms_data.py
"""
    1.发送每个支路的bms信息，共1-13支路
    2.每个支路
    3.501156 作用于26F 中的BMSBatteryPackCap和BMSBatteryType
    4.
"""
import re
from utils.log import log


def mem_cpy_replace(list1, list2, num):
    """
    数据处理
    :param list1:
    :param list2:
    :param num:
    :return:
    """
    # 这里加if 判断是为了避免传入的数据长度过长可能引入数据格式问题
    l = len(list2)
    if num == 130 and l > 31:
        list2 = list2[:31]
        l = 31
    elif num == 163 and l > 24:
        list2 = list2[:24]
        l = 24
    elif num == 196 and l > 17:
        list2 = list2[:17]
        l = 17
    elif num == 213 and l > 11:
        list2 = list2[:11]
        l = 11

    for j in list2[0:]:
        list1[num] = j
        num = num + 1


class BmsData:

    def __init__(self, branch_json):
        self.data = branch_json
        self.board = [0 for _ in range(0, 1000)]
        self.battery_type = int(branch_json.get("bms_battery_pack_cap", 6))  # 1008

    def int_data_covert(self, data, key=None):
        """
        该函数对于非int类型的数据强制转成int
        用于对于发送为20,云端为20.0的情况
        对于不要强制转换的，不要调用该函数，直接使用int即可
        :param data:
        :param key:
        :return:
        """
        try:
            data = int(data)
            if self.init_data_check(data, key):
                return data
            raise ValueError(f"<BMS>:{key} 对应的值{data}不在范围内")
        except Exception as e:
            pass
        try:
            data = int(float(data))
            if self.init_data_check(data, key):
                return data
            raise ValueError(f"<BMS>:{key} 对应的值{data}不在范围内")
        except Exception as e:
            raise e

    def float_data_covert(self, data, key=None):
        """
        :param data:
        :param key:
        :return:
        """
        try:
            data = float(data)
            if self.init_data_check(data, key):
                return data
            raise ValueError(f"<BMS>:{key} 对应的值{data}不在范围内")
        except Exception as e:
            raise e

    def volt_float_data_convert(self, data, key=None):
        """
        电压数据的检查
        :param data:
        :param key:
        :return:
        """
        try:
            data = float(data)
            if self.init_data_check(data, key):
                data = data - 1
                data = round(data * 1000)
                return data
            raise ValueError(f"<BMS>:{key} 对应的值{data}不在范围内")
        except Exception as e:
            raise e

    def init_data_check(self, data, key):
        """
        这里进行post数据的检查，如果不符合，直接返回数据范围不对的提示
        :param data:
        :return:
        """
        return True

    def bms_data_init(self):
        """

        :return:
        """
        self.bms_af_data()
        self.bms_ac_data()
        self.bms_ad_data()
        self.bms_ae_data()
        self.bms_267_data()
        self.bms_268_data()
        self.bms_269_data()
        self.bms_26a_data()
        self.bms_26f_data()
        self.bms_270_data()
        self.bms_271_data()
        self.bms_272_data()
        self.bms_273_data()
        self.bms_372_data()
        self.bms_373_data()
        self.bms_68c_data()
        self.cell_volt_data()
        self.cell_temp_data()
        self.bms_274_data()
        self.bms_29a_data()
        self.bms_29b_data()
        self.bms_376_data()
        self.bms_379_data()

    def bms_af_data(self):
        """
        处理 BMS_VCU_AF AF数据
        0-7
        :return:
        """
        data = self.int_data_covert(self.data.get('bms_contactor_states', '0'))
        # BMSCntctrSts 电池内部高压继电器状态
        self.board[0] = (self.board[0] | (data & 0x07)) & 0xFF  # byte0 bit:0-2 range:[0-7] factor:1 offset:0
        data = self.int_data_covert(self.data.get('bms_sts', '0'))  # BMSSSts 电池状态
        self.board[0] = (self.board[0] | ((data << 4) & 0xF0)) & 0xFF
        # byte0 bit:4-7 range:[0-15] factor:1 offset:0
        data = self.int_data_covert(self.data.get('bms_inhibit_cls_reason', '0'))
        self.board[1] = data & 0xFF
        # BMSInhibitClsReason byte1 bit:0-7 range:[0-255] factor:1 offset:0
        data = self.int_data_covert(self.data.get('bms_abort_cls_reason', '0'))
        self.board[2] = data & 0xFF
        # BMSAbortClsReason byte2 bit:0-7 range:[0-255] factor:1 offset:0

    def bms_ac_data(self):
        """
        处理BMS_VCU_AC AC数据
        8-15
        :return:
        """
        data = self.float_data_covert(self.data.get('bms_pack_crrnt', '0'))
        data = int((data + 2000) * 10)  # BMSPackCrrnt 电池包总电流 [-2000, 2000] factor=0.1
        self.board[8] = (data >> 8) & 0xFF
        self.board[9] = data & 0x00FF

        data = self.float_data_covert(self.data.get('bms_pack_voltage', '0'))
        data = int(data * 10)  # BMSPackVoltage 电池包总电压 [0, 600] factor=0.1
        self.board[10] = (self.board[10] | ((data >> 8) & 0x1F)) & 0xFF
        self.board[11] = data & 0x00FF

        data = self.int_data_covert(self.data.get('bms_fault_lvl', '0'))  # BMSFaultLvl 电池故障等级 [0, 7]
        # log.warning(f"bms_fault_lvl:{data}")
        self.board[10] = (self.board[10] | ((data << 5) & 0xE0)) & 0xFF
        # log.warning(f"self.board[10]:{self.board[10]}")
        data = self.float_data_covert(self.data.get('bms_soc', '0'))  # BMSSOC 电池实际SOC [0, 100]
        self.board[12] = int((data * 2)) & 0xFF

        data = self.float_data_covert(self.data.get('bms_customer_usage_soc', '0'))
        # print("bms_customer_usage_soc:", data)
        self.board[13] = int((data * 2)) & 0xFF  # BMSCustomerUsageSOC 电池用户SOC [0, 100] factor=0.5
        # print("self.board[13]:", self.board[13])
        data = self.int_data_covert(self.data.get('bms_charge_available', '0'))
        # print("bms_charge_available", data)
        # BMSChargeAvailable 电池可充电标志/BMS充电允许标志位 [0， 1]
        self.board[14] = (self.board[14] | ((data << 4) & 0x10)) & 0xFF

        data = self.int_data_covert(self.data.get('bms_ac_test_status', '0'))  # BMSACTestStatus 电池AC测试状态 [0, 1]
        self.board[14] = (self.board[14] | ((data << 5) & 0x20)) & 0xFF

        data = self.int_data_covert(self.data.get('hv_batt_soc_low_warn', '0'))  # HVBattSOCLowWarn [0, 1] fact=1
        self.board[14] = (self.board[14] | ((data << 6) & 0x40)) & 0xFF

        data = self.int_data_covert(self.data.get('bms_check_sum_ac', '0'))  # BMS_VCU_AC_CRC [0, 255] fact=1
        self.board[15] = self.board[15] | (data & 0xFF)

    def bms_ad_data(self):
        """
        处理BMS_VCU_AD AD数据
        16-23
        :return:
        """
        data = self.float_data_covert(self.data.get('bms_dischg_crrnt_limit', '0'))
        # BMSDischgCrrntLimit [0, 2000] fact=0.1
        data = int(data * 10)
        self.board[16] = ((data >> 8) & 0xFF)
        self.board[17] = data & 0xFF

        data = self.float_data_covert(self.data.get('bms_voltage_limit_max', '0'))
        # BMSVoltgLimitMax 电池电池包最高允许总电压 [0, 600]
        data = int(data * 10)
        self.board[18] = (self.board[18] | ((data >> 8) & 0X1F)) & 0xFF
        self.board[19] = data & 0xFF

        data = self.int_data_covert(self.data.get('bms_balance_sts', '0'))  # BMSBalanceSts 电池均衡状态 [0,1]
        self.board[18] = (self.board[18] | ((data << 5) & 0x20)) & 0xFF

        data = self.int_data_covert(self.data.get('bms_inter_lock_sts', '0'))  # BMSInterlockSts 电池高压互锁标志 [0, 3]
        self.board[18] = (self.board[18] | ((data << 6) & 0xC0)) & 0xFF
        # print("bms_inter_lock_sts", data, hex(self.board[18]))

        data = self.float_data_covert(self.data.get('bms_voltage_limit_min', '0'))
        # BMSVoltgLimitMin 电池电池包最低允许总电压 [0, 600]
        data = int(data * 10)
        self.board[20] = (self.board[20] | ((data >> 8) & 0X1F)) & 0xFF
        self.board[21] = data & 0xFF

        data = self.int_data_covert(self.data.get('bms_isolation_lvl', '0'))  # BMSIsolationLvl 电池绝缘等级 [0,7]
        self.board[20] = (self.board[20] | ((data << 5) & 0xE0)) & 0xFF

        data = self.int_data_covert(self.data.get('bms_alm_clk_sts', '0'))  # BMSAlarmClockStatus [0, 255] fact=1
        self.board[22] = self.board[22] | (data & 0x03)

        data = self.int_data_covert(self.data.get('bms_dc_chrg_derate_crrnt_sts', '0'))
        # BMSDCChrgDerateCrrntSts [0, 1] fact=1
        self.board[22] = self.board[22] | ((data << 3) & 0x08)

        data = self.int_data_covert(self.data.get('bms_charge_state', '0'))  # BMSChrgState 电池充电状态 [0, 7]
        self.board[22] = (self.board[22] | ((data << 5) & 0xE0)) & 0xFF

        data = self.int_data_covert(self.data.get('bms_fault_cat', '0'))  # BMSFaultCat BMS故障等级位掩码 [0, 255] fact=1
        self.board[23] = data & 0xFF

    def bms_ae_data(self):
        """
        处理BMS_VCU_AE AE数据
        24-31
        :return:
        """
        # 尝试移除变量名的方式
        data = self.int_data_covert(self.data.get('bms_if_bms_soc_set', '0'))  # BMSIfBmsSocSet 电池达到SOC目标值 [0, 3]
        self.board[24] = (self.board[24] | (data & 0x03)) & 0xFF
        data = self.int_data_covert(self.data.get('bms_if_pack_voltage_set', '0'))
        # BMSIfPackVoltageSet 电池达到总电压目标值 [0, 3]
        self.board[24] = (self.board[24] | ((data << 2) & 0x0C)) & 0xFF
        data = self.int_data_covert(self.data.get('bms_if_cell_voltage_set', '0'))
        # BMSIfCellVoltageSet 电池达到单体电压目标值 [0,3]
        self.board[24] = (self.board[24] | ((data << 4) & 0x30)) & 0xFF
        data = self.int_data_covert(self.data.get('bms_hv_isolation', '0'))  # BMSHvIsolation BMS绝缘故障 [0,3]
        # print("bms_hv_isolation", data)
        self.board[24] = (self.board[24] | ((data << 6) & 0xC0)) & 0xFF

        data = self.int_data_covert(self.data.get('bms_connector_over_temp', '0'))
        # BMSConnectorOvertemp BMS高压继电器过温故障 [0,3]
        self.board[25] = (self.board[25] | ((data & 0x03) & 0xFF)) & 0xFF
        data = self.int_data_covert(self.data.get('bms_chrg_conn_over_temp', '0'))
        # BMSChrgConnOvertemp BMS充电连接器过温故障 [0,3]
        self.board[25] = (self.board[25] | ((data << 2) & 0x0C)) & 0xFF
        data = self.int_data_covert(self.data.get('bms_chrg_conn_error', '0'))
        # BMSChrgConnError BMS充电连接器故障 [0,3]
        self.board[25] = (self.board[25] | ((data << 4) & 0x30)) & 0xFF
        data = self.int_data_covert(self.data.get('bms_pack_over_temp', '0'))
        # BMSPackOverTemp BMS电池包温度过高故障 [0,3]
        self.board[25] = (self.board[25] | ((data << 6) & 0xC0)) & 0xFF

        data = self.int_data_covert(self.data.get('bms_hv_conector_error', '0'))
        # BMSHvConectorError BMS高压继电器故障 [0,3]
        self.board[26] = (self.board[26] | ((data & 0x03) & 0xFF)) & 0xFF
        data = self.int_data_covert(self.data.get('bms_other_error', '0'))  # BMSOtherError BMS其它故障 [0,3]
        self.board[26] = (self.board[26] | ((data << 2) & 0x0C)) & 0xFF
        data = self.int_data_covert(self.data.get('bms_over_current', '0'))  # BMSOverCurrent BMS过流故障 [0,3]
        self.board[26] = (self.board[26] | ((data << 4) & 0x30)) & 0xFF
        data = self.int_data_covert(self.data.get('bms_voltg_mismatch', '0'))  # BMSVolMismatch BMS电压不匹配 [0,3]
        self.board[26] = (self.board[26] | ((data << 6) & 0xC0)) & 0xFF

        data = self.float_data_covert(self.data.get('maximum_permit_charge_cell_volt', '0'))
        # MaximumPeimitChargeCellVoltage 电池单体最高允许充电电压 [0, 24]
        data = int(data * 100)
        self.board[27] = (data >> 8) & 0xFF
        self.board[28] = data & 0xFF

        data = self.float_data_covert(self.data.get('bms_high_resl_soc', '0'))
        # BMSHighReslSOC 高实际SOC BMS高分辨率SOC [0, 102.3] fact=0.1
        data = int(data * 10)
        self.board[29] = ((data & 0x3FF) >> 2) & 0xFF
        self.board[30] = self.board[30] | ((data & 0x03) << 6)

        data = self.int_data_covert(self.data.get('bms_cel_slf_dchrg_sts', '0'))
        # BMSCellSelfDischrgSts BMS单体自放电状态 [0, 3] fact =1
        self.board[30] = (self.board[30] | (data & 0x03)) & 0xFF

        data = self.int_data_covert(self.data.get('bms_pack_iso_dec_sts', '0'))
        # BMSPackIsoDecreaseSts BMS电池包绝缘下降状态 [0, 3] fact =1
        self.board[30] = (self.board[30] | ((data << 2) & 0x0C)) & 0xFF

        data = self.int_data_covert(self.data.get('bms_inhibit_chrg_flt', '0'))  # //zl 2022.6.15
        self.board[30] = (self.board[30] | ((data << 4) & 0x30)) & 0xFF

    def bms_267_data(self):
        """
        处理267数据
        :return:
        """
        data = self.float_data_covert(self.data.get('bms_dc_chrg_current_req', '0'))
        data = int((data + 2000) * 10)  # BMSDCChrgCrntReq 电池充电请求电流 [-2000, 4553.5] factor=0.1
        self.board[32] = (data >> 8) & 0xFF
        self.board[33] = data & 0xFF

        data = self.float_data_covert(self.data.get('bms_dc_chrg_voltage_req', '0'))
        data = int(data * 10)  # BMSDCChrgVoltgReq 电池充电请求电压 [0, 600] factor=0.1
        self.board[34] = (data >> 8) & 0xFF
        self.board[35] = data & 0xFF

        data = self.float_data_covert(self.data.get('bms_chrg_current_limit', '0'))
        data = int((data + 2000) * 10)  # BMSChgCrrntLimit 电池充电限流值 [-2000, 0] factot=0.1
        self.board[36] = (data >> 8) & 0xFF
        self.board[37] = data & 0xFF

        data = self.int_data_covert(self.data.get('bms_dc_chrg_mode', '0'))  # BMSDCChrgMode 直流充电模式 [0,3]
        self.board[38] = (self.board[38] | ((data << 2) & 0x0C)) & 0xFF

        data = self.int_data_covert(self.data.get('bms_req_wakeup_obcm', '0'))
        self.board[38] = self.board[38] | ((data << 4) & 0x10)  # BMSReqWakeUpOBCM BMS请求唤醒OBCm

        data = self.int_data_covert(self.data.get('bms_pack_therm_out_of_ctrl_vld', '0'))  # BMS电池包热失控故障有效性 [0, 1] 1
        self.board[38] = self.board[38] | ((data << 5) & 0x20)  # BMSPackThermOutOfCtrlVld

        data = self.int_data_covert(self.data.get('bms_pack_therm_out_of_ctrl_alrm', '0'))
        self.board[38] = self.board[38] | ((data << 6) & 0xC0)  # BMSPackThermOutOfCtrlAlrm BMS_热管理失控告警

        data = self.float_data_covert(self.data.get('bms_pack_energy_available', '0'))
        data = int(data * 10)  # BMSPackEnergyAvailable 电池可用电量 [0, 100] factor=0.1
        self.board[38] = (self.board[38] | ((data >> 8) & 0x03)) & 0xFF
        self.board[39] = data & 0xFF

    def bms_268_data(self):
        """
        处理BMS_VCU_268 268数据
        40-47
        :return:
        """
        data = self.float_data_covert(self.data.get('bms_dischrg_power_limit_st', '0'))
        # BMSDischrgPowerLimitST 电池短时放电功率限值 [0, 1000]
        data = int(data * 10)  # fact=0.1
        self.board[40] = (data >> 8) & 0xFF
        self.board[41] = data & 0xFF
        data = self.float_data_covert(self.data.get('bms_dischrg_power_limit_lt', '0'))
        # BMSDischrgPowerLimitLT 电池长时放电功率限值 [0, 1000]
        data = int(data * 10)
        self.board[42] = (data >> 8) & 0xFF
        self.board[43] = data & 0xFF
        data = self.float_data_covert(self.data.get('bms_dischrg_power_limit_dynamic', '0'))
        # BMSDischrgPowerLimitDynamic 电池动态放电功率限值 [0, 1000]
        data = int(data * 10)
        self.board[44] = (data >> 8) & 0xFF
        self.board[45] = data & 0xFF
        data = self.int_data_covert(self.data.get('bms_insolation_resistance_value', '0'))
        # BMSInsulationResistanceValue 电池绝缘电阻值 [0, 65535] factor=1
        self.board[46] = (data >> 8) & 0xFF
        self.board[47] = data & 0xFF

    def bms_269_data(self):
        """
        处理BMS_VCU_269 269数据
        48-55
        :return:
        """
        data = self.float_data_covert(self.data.get('bms_cell_voltg_max', '0'))
        data = int(data * 1000)  # BMSCellVoltgMax 电池最高单体电压 [0, 5] factor=0.001
        self.board[48] = (data >> 8) & 0xFF
        self.board[49] = data & 0xFF

        data = self.float_data_covert(self.data.get('bms_cell_voltg_min', '0'))  # BMSCellVoltgMin 电池最低单体电压 [0, 5]
        data = int(data * 1000)
        self.board[50] = (data >> 8) & 0xFF
        self.board[51] = data & 0xFF

        data = self.int_data_covert(self.data.get('bms_cell_voltg_average_validity', '0'))
        # BMSCellVoltgAverageValidity
        self.board[52] = self.board[52] | ((data << 4) & 0x10)  # [0, 1] fact=1
        data = self.int_data_covert(self.data.get('bms_cell_voltg_max_validity', '0'))  # BMSCellVoltgMaxValidity
        self.board[52] = self.board[52] | ((data << 5) & 0x20)  # [0, 1] fact=1
        data = self.int_data_covert(self.data.get('bms_cell_voltg_min_validity', '0'))  # BMSCellVoltgMinValidity
        self.board[52] = self.board[52] | ((data << 6) & 0x40)  # [0, 1] fact=1

        data = self.int_data_covert(self.data.get('bms_estimate_chrg_time', '0'))
        # BMSEstimateChrgTime 电池预估剩余充电时间 [0, 1440]
        self.board[52] = (self.board[52] | (data >> 8) & 0x0F) & 0xFF
        self.board[53] = data & 0xFF

        data = self.float_data_covert(self.data.get('bms_cell_voltg_average', '0'))
        # BMSCellVoltgAverage 电池平均单体电压 [0, 5]
        data = int(data * 1000)
        self.board[54] = (data >> 8) & 0xFF
        self.board[55] = data & 0xFF

    def bms_26a_data(self):
        """
        处理BMS_VCU_26A 26A数据
        56-63
        :return:
        """
        data = self.float_data_covert(self.data.get('bms_chrg_power_limit_st', '0'))
        # BMSChrgPowerLimitST 电池短时充电功率极值 [0, 1000]
        data = int(data * 10)
        self.board[56] = (data >> 8) & 0xFF
        self.board[57] = data & 0xFF
        data = self.float_data_covert(self.data.get('bms_chrg_power_limit_lt', '0'))
        # BMSChrgPowerLimitLT 电池长时充电功率极值 [0, 1000]
        data = int(data * 10)
        self.board[58] = (data >> 8) & 0xFF
        self.board[59] = data & 0xFF
        data = self.float_data_covert(self.data.get('bms_chrg_power_limit_dynamic', '0'))
        # BMSChrgPowerLimitDynamic 电池动态充电功率限值 [0， 1000]
        data = int(data * 10)
        self.board[60] = (data >> 8) & 0xFF
        self.board[61] = data & 0xFF

    def bms_26f_data(self):
        """
        处理BMS_VCU_26F 26F数据
        72-79
        :return:
        """
        data = self.data.get('bms_protocal_version', '1.2.3')  # BMSProtocalVersion [0, 16777215]
        vers = data.split(".")
        if len(vers) >= 3 and all([vers[i].isdigit() for i in range(len(vers))]):
            self.board[72] = int(vers[0])
            self.board[73] = int(vers[1])
            self.board[74] = int(vers[2])
        else:
            self.board[72] = 1
            self.board[73] = 2
            self.board[74] = 3

        data = self.int_data_covert(self.data.get('bms_battery_type', '0'))
        # print("bms_battery_type:", self.data.get('bms_battery_type'))
        self.board[75] = self.board[75] | (data & 0x0F)  # BMSBatteryType 电池类型 [0, 15]

        data = self.int_data_covert(self.data.get('bms_battery_pack_cap', '0'))  # BMSBatteryPackCap 电芯类型 [0, 15]
        # print("bms_battery_pack_cap:", self.data.get('bms_battery_pack_cap'))
        self.board[75] = self.board[75] | ((data << 4) & 0xF0)

        data = self.float_data_covert(self.data.get('bms_max_permit_dc_charge_voltage', '0'))
        # BMSMaxPermitDCChargeVoltage 电池最大允许直流充电电压 [0, 6553.5]
        data = int(data * 10)
        self.board[76] = (data >> 8) & 0xFF
        self.board[77] = data & 0xFF

        data = self.float_data_covert(self.data.get('bms_battery_rated_capacity', '0'))
        # BMSBatteryRatedCapacity 电池额定容量 [0, 1000]
        data = int(data * 10)
        self.board[78] = (data >> 8) & 0xFF
        self.board[79] = data & 0xFF

    def bms_270_data(self):
        """
        处理BMS_VCU_270 270数据
        80-87
        :return:
        """
        data = self.float_data_covert(self.data.get('bms_battery_rated_voltage', '0'))
        # BMSBatteryRatedVoltage 电池动力电池额定电压 [0, 1000]
        data = int(data * 10)
        self.board[80] = (data >> 8) & 0xFF
        self.board[81] = data & 0xFF
        data = self.int_data_covert(self.data.get('bms_ready_dc_charging', '0'))
        # print("bms_ready_dc_charging", data)
        # BMSReadyDCCharging 电池直流充电就绪状态 [0, 255] BMS准备就绪:0x00-未准备好; 0xAA-快充准备好; 0xFF-无效
        self.board[83] = data & 0xFF
        data = self.float_data_covert(self.data.get('bms_dc_charging_volt_measure', '0'))
        # 充电电压测量值: Resolution-0.1; 0~1000V; offset: 0;
        data = int(data * 10)  # BMSDCChargingVoltageMeasurement [0, 1000],fact=0.1
        self.board[84] = (data >> 8) & 0xFF
        self.board[85] = data & 0xFF
        data = self.float_data_covert(self.data.get('bms_dc_charging_curr_measure', '0'))
        # 充电电流测量值: Resolution-0.1; -400~0V; offset: -400;
        data = int((data + 400) * 10)  # BMSDCChargingCurrentMeasurement [-400, 6153.5],fact=0.1
        self.board[86] = (data >> 8) & 0xFF
        self.board[87] = data & 0xFF

    def bms_271_data(self):
        """
        处理BMS_VCU_271 271数据
        :return:
        """
        data = self.int_data_covert(self.data.get('bms_maximum_cell_voltage_number', '1'))
        # BMSMaximumCellVoltageNumber 电池最高单体电压单体编号 [1, 256], factor=1
        self.board[88] = (data - 1) & 0xFF
        data = self.int_data_covert(self.data.get('bms_maximum_cell_temp', '0'))
        # BMSMaximumCellTemp 电池最高电芯温度 [-50, 200]
        self.board[89] = (data + 50) & 0xFF
        data = self.int_data_covert(self.data.get('bms_maximum_temp_number', '0'))
        # BMSMaximumTempNumber 电池最高电芯温度编号 [1, 128]
        self.board[90] = (data - 1) & 0xFF
        data = self.int_data_covert(self.data.get('bms_minimum_cell_temp', '0'))
        # BMSMinimumCellTemp 电池最低电芯温度 [-50, 200]
        self.board[91] = (data + 50) & 0xFF
        data = self.int_data_covert(self.data.get('bms_minimum_temp_number', '0'))
        # BMSMinimumTempNumber 电池最低电芯温度编号 [1, 128]
        self.board[92] = (data - 1) & 0xFF
        data = self.int_data_covert(self.data.get('bms_dc_chrg_final_soc', '0'))
        # BMSDCChrgFinalSOC 电池充电截止SOC [0, 100]
        self.board[93] = data & 0xFF

    def bms_272_data(self):
        """
        处理BMS_VCU_272 272数据
        96-103
        :return:
        """
        data = self.int_data_covert(self.data.get('bms_cell_voltage_over_under', '0'))
        self.board[96] = (self.board[96] | (data & 0x03)) & 0xFF  # BMSCellVoltageOverUnder
        data = self.int_data_covert(self.data.get('bms_soc_over_under', '0'))  # BMSSOCOverUnder 电池当前可用soc状态 [0, 3]
        self.board[96] = (self.board[96] | ((data << 2) & 0x0C)) & 0xFF
        data = self.int_data_covert(self.data.get('battery_temp_over', '0'))
        self.board[96] = (self.board[96] | ((data << 6) & 0xC0)) & 0xFF  # BatteryTempOver
        data = self.int_data_covert(self.data.get('bms_dc_chrg_curr_over', '0'))
        self.board[96] = (self.board[96] | ((data << 4) & 0x30)) & 0xFF  # BMSDCChargeCurrentOverUnder
        data = self.int_data_covert(self.data.get('battery_output_connector_state', '0'))
        # BatteryOutputConnectorState 电池输出电连接器状态 [0, 3]
        self.board[97] = (self.board[97] | (data & 0x03)) & 0xFF
        data = self.int_data_covert(self.data.get('dc_charging_permit_status', '0'))
        # print("dc_charging_permit_status", data)
        # DCChargingPermitStatus 电池允许充电状态 [0, 3]
        self.board[97] = (self.board[97] | ((data << 2) & 0x0C)) & 0xFF

        data = self.int_data_covert(self.data.get('battery_abnormal_alarm4', '0'))
        self.board[98] = self.board[98] | (data & 0x03)

        data = self.int_data_covert(self.data.get('battery_abnormal_alarm3', '0'))
        self.board[98] = self.board[98] | ((data << 2) & 0x0C)

        data = self.int_data_covert(self.data.get('battery_abnormal_alarm2', '0'))
        self.board[98] = self.board[98] | ((data << 4) & 0x30)

        data = self.int_data_covert(self.data.get('battery_abnormal_alarm1', '0'))
        self.board[98] = self.board[98] | ((data << 6) & 0xC0)

        data = self.int_data_covert(self.data.get('egy_storg_err8', '0'))
        self.board[99] = self.board[99] | (data & 0x01)  # EgyStorgDevErr8
        data = self.int_data_covert(self.data.get('egy_storg_err7', '0'))
        self.board[99] = self.board[99] | ((data << 1) & 0x02)  # EgyStorgDevErr7
        data = self.int_data_covert(self.data.get('egy_storg_err6', '0'))
        self.board[99] = self.board[99] | ((data << 2) & 0x04)  # EgyStorgDevErr6
        data = self.int_data_covert(self.data.get('egy_storg_err5', '0'))
        self.board[99] = self.board[99] | ((data << 3) & 0x08)  # EgyStorgDevErr5
        data = self.int_data_covert(self.data.get('egy_storg_err4', '0'))
        self.board[99] = self.board[99] | ((data << 4) & 0x10)  # EgyStorgDevErr4
        data = self.int_data_covert(self.data.get('egy_storg_err3', '0'))
        self.board[99] = self.board[99] | ((data << 5) & 0x20)  # EgyStorgDevErr3
        data = self.int_data_covert(self.data.get('egy_storg_err2', '0'))
        self.board[99] = self.board[99] | ((data << 6) & 0x40)  # EgyStorgDevErr2
        data = self.int_data_covert(self.data.get('egy_storg_err1', '0'))
        self.board[99] = self.board[99] | ((data << 7) & 0x80)  # EgyStorgDevErr1
        data = self.int_data_covert(self.data.get('soc_jump_alarm', '0'))
        self.board[100] = self.board[100] | (data & 0x03)  # SOCJumpAlarm
        data = self.int_data_covert(self.data.get('battery_type_dismatch_alarm', '0'))
        self.board[100] = (self.board[100] | ((data << 2) & 0x0C)) & 0xFF  # BatteryTypeDismatchAlram
        data = self.int_data_covert(self.data.get('battery_consistency_alarm', '0'))
        self.board[100] = (self.board[100] | ((data << 4) & 0x30)) & 0xFF  # BatteryConsistencyAlarm
        data = self.int_data_covert(self.data.get('battery_temp_differ_alarm', '0'))
        self.board[100] = (self.board[100] | ((data << 6) & 0xC0)) & 0xFF  # BatteryTempDifferAlarm
        data = self.int_data_covert(self.data.get('battery_pck_volt_over_alarm', '0'))
        self.board[101] = (self.board[101] | (data & 0x03)) & 0xFF  # BatteryPckVoltOverAlarm
        data = self.int_data_covert(self.data.get('battery_pck_volt_under_alarm', '0'))
        self.board[101] = (self.board[101] | ((data << 2) & 0x0C)) & 0xFF  # BatteryPckVoltUnderAlarm
        data = self.int_data_covert(self.data.get('battery_cell_vol_high_alarm', '0'))
        self.board[101] = (self.board[101] | ((data << 4) & 0x30)) & 0xFF  # BatteryCellVolHighAlarm
        data = self.int_data_covert(self.data.get('battery_cell_vol_low_alarm', '0'))
        self.board[101] = (self.board[101] | ((data << 6) & 0xC0)) & 0xFF  # BatteryCellVolLowAlarm
        data = self.int_data_covert(self.data.get('battery_cell_temp_high_alarm', '0'))
        self.board[102] = (self.board[102] | (data & 0x03)) & 0xFF  # BatteryCellTempHighAlarm
        data = self.int_data_covert(self.data.get('battery_cell_temp_low_alarm', '0'))
        self.board[102] = (self.board[102] | ((data << 2) & 0x0C)) & 0xFF  # BatteryCellTempLowAlarm
        data = self.int_data_covert(self.data.get('soc_jump_reason', '0'))  # SocJumpReason 电池SOC跳跃原因 [0, 15]
        self.board[102] = (self.board[102] | ((data << 4) & 0xF0)) & 0xFF
        data = self.int_data_covert(self.data.get('battery_soc_high_alarm', '0'))
        self.board[103] = self.board[103] | ((data << 2) & 0x0C)  # BatterySOCHighAlarm
        data = self.int_data_covert(self.data.get('battery_over_temp_alarm', '0'))
        self.board[103] = self.board[103] | ((data << 4) & 0x30)  # BatteryOverTemprAlarm
        data = self.int_data_covert(self.data.get('bms_hv_isolation_alarm', '0'))
        self.board[103] = (self.board[103] | ((data << 6) & 0xC0)) & 0xFF  # BMSHvIsolationAlarm

    def bms_273_data(self):
        """
        处理BMS_VCU_273 273数据
        104-111
        :return:
        """
        data = self.int_data_covert(self.data.get('bms_minimum_cell_voltage_number', '1'))
        self.board[104] = (data - 1) & 0xFF  # BMSMinimumCellVoltageNumber 电池最低单体电压单体编号 [1, 256]
        data = self.int_data_covert(self.data.get('bms_max_voltage_subsys_number', '1'))
        self.board[105] = (data - 1) & 0xFF  # BMSMaxVoltageSubSysNumber [1-256]
        data = self.int_data_covert(self.data.get('bms_min_voltage_subsys_number', '1'))
        self.board[106] = (data - 1) & 0xFF  # BMSMinVoltageSubSysNumber [1-256]
        data = self.int_data_covert(self.data.get('bms_max_temp_subsys_number', '1'))
        self.board[107] = (data - 1) & 0xFF  # BMSMaxTempSubSysNumber [1-256]
        data = self.int_data_covert(self.data.get('bms_min_temp_subsys_number', '1'))
        self.board[108] = (data - 1) & 0xFF  # BMSMinTempSubSysNumber [1-256]

    def bms_372_data(self):
        """
        处理BMS_VCU_372 372数据
        112-119
        :return:
        """
        data = self.float_data_covert(self.data.get('maximum_charging_current', '0'))
        # MaximumChargingCurrent 电池最大充电电流 [-400, 6153.5]
        data = int((data + 400) * 10)
        self.board[112] = (data >> 8) & 0xFF
        self.board[113] = data & 0xFF
        data = self.float_data_covert(self.data.get('battery_normal_capacity', '0'))
        # BatteryNomalCapacity 电池动力电池标称总能量 [0, 1000]
        data = int(data * 10)
        self.board[114] = (data >> 8) & 0xFF
        self.board[115] = data & 0xFF

        data = self.float_data_covert(self.data.get('maximum_charging_voltage', '0'))
        # MaximumChargingVoltage 电池最大允许直流充电电压 [0, 1000]
        data = int(data * 10)
        self.board[116] = (data >> 8) & 0xFF
        self.board[117] = data & 0xFF

        data = self.int_data_covert(self.data.get('maximum_permit_temp', '0'))
        # MaximumPermitTemp 电池最高允许温度 [-50, 205]
        data = data + 50
        self.board[118] = data & 0xFF

    def bms_373_data(self):
        """
        处理BMS_VCU_373 373数据 电池数据要在指定范围内
        120-127
        :return:
        """
        data = self.float_data_covert(self.data.get('bms_temp_max', '0'))  # BMSTempMax 电池最高电芯温度 [-40, 85]
        data = int((data + 40) * 2)
        self.board[120] = data & 0xFF

        data = self.float_data_covert(self.data.get('bms_temp_min', '0'))  # BMSTempMin 电池最低电芯温度 [-40, 85]
        data = int((data + 40) * 2)
        self.board[121] = data

        data = self.float_data_covert(self.data.get('bms_temp_average', '0'))  # BMSTempAverage 电池平均电芯温度 [-40, 85]
        data = int((data + 40) * 2)
        self.board[122] = data & 0xFF

        data = self.int_data_covert(self.data.get('bms_hv_shutdown_req', '0'))  # BMSHVShutdownReq 电池高压下电请求 [0, 1]
        self.board[123] = (self.board[123] | ((data << 2) & 0x04)) & 0xFF

        data = self.int_data_covert(self.data.get('bms_temp_max_validity', '0'))  # BMSTempMaxValidity [0, 1]
        self.board[123] = self.board[123] | ((data << 3) & 0x08)

        data = self.int_data_covert(self.data.get('bms_temp_min_validity', '0'))  # BMSTempMinValidity [0, 1]
        self.board[123] = self.board[123] | ((data << 4) & 0x10)

        data = self.int_data_covert(self.data.get('bms_temp_average_validity', '0'))  # BMSTempAverageValidity [0, 1]
        self.board[123] = self.board[123] | ((data << 5) & 0x20)

        data = self.int_data_covert(self.data.get('bms_ess_inlet_temp_validity', '0'))  # BMSESSInletTempValidity [0, 1]
        self.board[123] = self.board[123] | ((data << 6) & 0x40)

        data = self.int_data_covert(self.data.get('bms_ess_inlet_temp_mask', '1'))  # BMSESSInletTempMask [0, 1]
        self.board[123] = self.board[123] | ((data << 7) & 0x80)

        data = self.float_data_covert(self.data.get('bms_ess_inlet_temp', '0'))  # BMSESSInletTemp 电池包入水口温度 [-40, 85]
        data = int((data + 40) * 8)
        self.board[123] = (self.board[123] | ((data >> 8) & 0x03)) & 0xFF
        self.board[124] = data & 0xFF

        data = self.int_data_covert(self.data.get('bms_ess_outlet_temp_validity', '0'))  # BMSESSOutletTempValidity
        self.board[125] = self.board[125] | ((data << 6) & 0x40)

        data = self.int_data_covert(self.data.get('bms_ess_outlet_temp_mask', '1'))  # BMSESSOutletTempMask
        self.board[125] = self.board[125] | ((data << 7) & 0x80)

        data = self.float_data_covert(self.data.get('bms_ess_outlet_temp', '0'))  # BMSESSOutletTemp 电池包出水口温度
        data = int((data + 40) * 8)
        self.board[125] = (self.board[125] | ((data >> 4) & 0x3F)) & 0xFF
        self.board[126] = (self.board[126] | ((data & 0x0F) << 4)) & 0xFF

        data = self.int_data_covert(self.data.get('bms_cell_tar_temp_mode_req_A', '0'))
        # BMSCellTarTempModeReq_A BMS单体目标温度请求方式 [0, 3] fact=1
        self.board[126] = self.board[126] | (data & 0x03)

        data = self.int_data_covert(self.data.get('reflash_req', '0'))  # ReflashReq [0, 1] fact=1
        self.board[126] = self.board[126] | ((data << 2) & 0x04)

        data = self.int_data_covert(self.data.get('bms_over_dc_chrg_protect', '0'))
        self.board[126] = self.board[126] | ((data << 3) & 0x08)

        data = self.float_data_covert(self.data.get('bms_cell_tar_temp', '0'))
        # BMSCellTarTemp BMS单体目标温度 [-20, 43.5] fact=0.5
        data = int((data + 20) * 2)
        # data = int(data)
        # print("bms_cell_tar_temp", data)
        self.board[127] = self.board[127] | (data & 0x7F)
        data = self.int_data_covert(self.data.get('bms_cell_tar_temp_validity', '0'))
        # BMSCellTarTempVld BMS单体目标温度有效性 [0, 1] fact=1
        self.board[127] = self.board[127] | ((data << 7) & 0x80)

    def bms_68c_data(self):
        """
        电池基本信息 68C
        battery_bms_pack_id:130-160
        battery_gb_pack_id:163-186
        bms_software_ver:196-212
        bms_hardware_ver:213-223
        :return:
        """
        data = self.data.get('battery_pack_id', "000000000000000000000000000test")
        mem_cpy_replace(self.board, data.encode(), 130)
        data = self.data.get('gb_battery_pack_id', "000000000000000000000000")
        mem_cpy_replace(self.board, data.encode(), 163)
        data = self.data.get('bms_software_ver', "00000000 00")
        mem_cpy_replace(self.board, data.encode(), 196)
        data = self.data.get('bms_hardware_ver', '00000000 00')
        mem_cpy_replace(self.board, data.encode(), 213)

    def cell_volt_data(self):
        """
        通过26C 发送
        每帧构造4个电压数据，共48帧，384个字节
        230-613 230开始， 613截止
        :return:
        """
        self.board[230] = 0x0
        data = self.volt_float_data_convert(self.data.get('N1', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N1
        self.board[231] = (data & 0x0FF0) >> 4
        self.board[232] = self.board[232] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N2', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N2
        self.board[232] = self.board[232] | (data & 0x0F00) >> 8
        self.board[233] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N3', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N3
        self.board[234] = (data & 0x0FF0) >> 4
        self.board[235] = self.board[235] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N4', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N4
        self.board[235] = self.board[235] | (data & 0x0F00) >> 8
        self.board[236] = data & 0x00FF

        self.board[238] = 0x1
        data = self.volt_float_data_convert(self.data.get('N5', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N5
        self.board[239] = (data & 0x0FF0) >> 4
        self.board[240] = self.board[240] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N6', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N6
        self.board[240] = self.board[240] | (data & 0x0F00) >> 8
        self.board[241] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N7', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N7
        self.board[242] = (data & 0x0FF0) >> 4
        self.board[243] = self.board[243] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N8', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N8
        self.board[243] = self.board[243] | (data & 0x0F00) >> 8
        self.board[244] = data & 0x00FF

        self.board[246] = 0x2
        data = self.volt_float_data_convert(self.data.get('N9', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N9
        self.board[247] = (data & 0x0FF0) >> 4
        self.board[248] = self.board[248] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N10', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N10
        self.board[248] = self.board[248] | (data & 0x0F00) >> 8
        self.board[249] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N11', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N11
        self.board[250] = (data & 0x0FF0) >> 4
        self.board[251] = self.board[251] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N12', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N12
        self.board[251] = self.board[251] | (data & 0x0F00) >> 8
        self.board[252] = data & 0x00FF

        self.board[254] = 0x3
        data = self.volt_float_data_convert(self.data.get('N13', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N13
        self.board[255] = (data & 0x0FF0) >> 4
        self.board[256] = self.board[256] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N14', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N14
        self.board[256] = self.board[256] | (data & 0x0F00) >> 8
        self.board[257] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N15', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N15
        self.board[258] = (data & 0x0FF0) >> 4
        self.board[259] = self.board[259] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N16', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N16
        self.board[259] = self.board[259] | (data & 0x0F00) >> 8
        self.board[260] = data & 0x00FF

        self.board[262] = 0x4
        data = self.volt_float_data_convert(self.data.get('N17', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N17
        self.board[263] = (data & 0x0FF0) >> 4
        self.board[264] = self.board[264] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N18', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N18
        self.board[264] = self.board[264] | (data & 0x0F00) >> 8
        self.board[265] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N19', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N19
        self.board[266] = (data & 0x0FF0) >> 4
        self.board[267] = self.board[267] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N20', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N20
        self.board[267] = self.board[267] | (data & 0x0F00) >> 8
        self.board[268] = data & 0x00FF

        self.board[270] = 0x5
        data = self.volt_float_data_convert(self.data.get('N21', 1)) & 0xFFF
        self.board[271] = (data & 0x0FF0) >> 4
        self.board[272] = self.board[272] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N22', 1)) & 0xFFF
        self.board[272] = self.board[272] | (data & 0x0F00) >> 8
        self.board[273] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N23', 1)) & 0xFFF
        self.board[274] = (data & 0x0FF0) >> 4
        self.board[275] = self.board[275] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N24', 1)) & 0xFFF
        self.board[275] = self.board[275] | (data & 0x0F00) >> 8
        self.board[276] = data & 0x00FF

        self.board[278] = 0x6
        data = self.volt_float_data_convert(self.data.get('N25', 1)) & 0xFFF
        self.board[279] = (data & 0x0FF0) >> 4
        self.board[280] = self.board[280] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N26', 1)) & 0xFFF
        self.board[280] = self.board[280] | (data & 0x0F00) >> 8
        self.board[281] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N27', 1)) & 0xFFF
        self.board[282] = (data & 0x0FF0) >> 4
        self.board[283] = self.board[283] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N28', 1)) & 0xFFF
        self.board[283] = self.board[283] | (data & 0x0F00) >> 8
        self.board[284] = data & 0x00FF

        self.board[286] = 0x7
        data = self.volt_float_data_convert(self.data.get('N29', 1)) & 0xFFF
        self.board[287] = (data & 0x0FF0) >> 4
        self.board[288] = self.board[288] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N30', 1)) & 0xFFF
        self.board[288] = self.board[288] | (data & 0x0F00) >> 8
        self.board[289] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N31', 1)) & 0xFFF
        self.board[290] = (data & 0x0FF0) >> 4
        self.board[291] = self.board[291] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N32', 1)) & 0xFFF
        self.board[291] = self.board[291] | (data & 0x0F00) >> 8
        self.board[292] = data & 0x00FF

        self.board[294] = 0x8
        data = self.volt_float_data_convert(self.data.get('N33', 1)) & 0xFFF
        self.board[295] = (data & 0x0FF0) >> 4
        self.board[296] = self.board[296] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N34', 1)) & 0xFFF
        self.board[296] = self.board[296] | (data & 0x0F00) >> 8
        self.board[297] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N35', 1)) & 0xFFF
        self.board[298] = (data & 0x0FF0) >> 4
        self.board[299] = self.board[299] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N36', 1)) & 0xFFF
        self.board[299] = self.board[299] | (data & 0x0F00) >> 8
        self.board[300] = data & 0x00FF

        self.board[302] = 0x9
        data = self.volt_float_data_convert(self.data.get('N37', 1)) & 0xFFF
        self.board[303] = (data & 0x0FF0) >> 4
        self.board[304] = self.board[304] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N38', 1)) & 0xFFF
        self.board[304] = self.board[304] | (data & 0x0F00) >> 8
        self.board[305] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N39', 1)) & 0xFFF
        self.board[306] = (data & 0x0FF0) >> 4
        self.board[307] = self.board[307] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N40', 1)) & 0xFFF
        self.board[307] = self.board[307] | (data & 0x0F00) >> 8
        self.board[308] = data & 0x00FF

        self.board[310] = 0xA
        data = self.volt_float_data_convert(self.data.get('N41', 1)) & 0xFFF
        self.board[311] = (data & 0x0FF0) >> 4
        self.board[312] = self.board[312] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N42', 1)) & 0xFFF
        self.board[312] = self.board[312] | (data & 0x0F00) >> 8
        self.board[313] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N43', 1)) & 0xFFF
        self.board[314] = (data & 0x0FF0) >> 4
        self.board[315] = self.board[315] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N44', 1)) & 0xFFF
        self.board[315] = self.board[315] | (data & 0x0F00) >> 8
        self.board[316] = data & 0x00FF

        self.board[318] = 0xB
        data = self.volt_float_data_convert(self.data.get('N45', 1)) & 0xFFF
        self.board[319] = (data & 0x0FF0) >> 4
        self.board[320] = self.board[320] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N46', 1)) & 0xFFF
        self.board[320] = self.board[320] | (data & 0x0F00) >> 8
        self.board[321] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N47', 1)) & 0xFFF
        self.board[322] = (data & 0x0FF0) >> 4
        self.board[323] = self.board[323] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N48', 1)) & 0xFFF
        self.board[323] = self.board[323] | (data & 0x0F00) >> 8
        self.board[324] = data & 0x00FF

        self.board[326] = 0xC
        data = self.volt_float_data_convert(self.data.get('N49', 1)) & 0xFFF
        self.board[327] = (data & 0x0FF0) >> 4
        self.board[328] = self.board[328] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N50', 1)) & 0xFFF
        self.board[328] = self.board[328] | (data & 0x0F00) >> 8
        self.board[329] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N51', 1)) & 0xFFF
        self.board[330] = (data & 0x0FF0) >> 4
        self.board[331] = self.board[331] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N52', 1)) & 0xFFF
        self.board[331] = self.board[331] | (data & 0x0F00) >> 8
        self.board[332] = data & 0x00FF

        self.board[334] = 0xD
        data = self.volt_float_data_convert(self.data.get('N53', 1)) & 0xFFF
        self.board[335] = (data & 0x0FF0) >> 4
        self.board[336] = self.board[336] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N54', 1)) & 0xFFF
        self.board[336] = self.board[336] | (data & 0x0F00) >> 8
        self.board[337] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N55', 1)) & 0xFFF
        self.board[338] = (data & 0x0FF0) >> 4
        self.board[339] = self.board[339] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N56', 1)) & 0xFFF
        self.board[339] = self.board[339] | (data & 0x0F00) >> 8
        self.board[340] = data & 0x00FF

        self.board[342] = 0xE
        data = self.volt_float_data_convert(self.data.get('N57', 1)) & 0xFFF
        self.board[343] = (data & 0x0FF0) >> 4
        self.board[344] = self.board[344] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N58', 1)) & 0xFFF
        self.board[344] = self.board[344] | (data & 0x0F00) >> 8
        self.board[345] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N59', 1)) & 0xFFF
        self.board[346] = (data & 0x0FF0) >> 4
        self.board[347] = self.board[347] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N60', 1)) & 0xFFF
        self.board[347] = self.board[347] | (data & 0x0F00) >> 8
        self.board[348] = data & 0x00FF

        self.board[350] = 0xF
        data = self.volt_float_data_convert(self.data.get('N61', 1)) & 0xFFF
        self.board[351] = (data & 0x0FF0) >> 4
        self.board[352] = self.board[352] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N62', 1)) & 0xFFF
        self.board[352] = self.board[352] | (data & 0x0F00) >> 8
        self.board[353] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N63', 1)) & 0xFFF
        self.board[354] = (data & 0x0FF0) >> 4
        self.board[355] = self.board[355] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N64', 1)) & 0xFFF
        self.board[355] = self.board[355] | (data & 0x0F00) >> 8
        self.board[356] = data & 0x00FF

        self.board[358] = 0x10
        data = self.volt_float_data_convert(self.data.get('N65', 1)) & 0xFFF
        self.board[359] = (data & 0x0FF0) >> 4
        self.board[360] = self.board[360] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N66', 1)) & 0xFFF
        self.board[360] = self.board[360] | (data & 0x0F00) >> 8
        self.board[361] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N67', 1)) & 0xFFF
        self.board[362] = (data & 0x0FF0) >> 4
        self.board[363] = self.board[363] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N68', 1)) & 0xFFF
        self.board[363] = self.board[363] | (data & 0x0F00) >> 8
        self.board[364] = data & 0x00FF

        self.board[366] = 0x11
        data = self.volt_float_data_convert(self.data.get('N69', 1)) & 0xFFF
        self.board[367] = (data & 0x0FF0) >> 4
        self.board[368] = self.board[368] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N70', 1)) & 0xFFF
        self.board[368] = self.board[368] | (data & 0x0F00) >> 8
        self.board[369] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N71', 1)) & 0xFFF
        self.board[370] = (data & 0x0FF0) >> 4
        self.board[371] = self.board[371] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N72', 1)) & 0xFFF
        self.board[371] = self.board[371] | (data & 0x0F00) >> 8
        self.board[372] = data & 0x00FF

        self.board[374] = 0x12
        data = self.volt_float_data_convert(self.data.get('N73', 1)) & 0xFFF
        self.board[375] = (data & 0x0FF0) >> 4
        self.board[376] = self.board[376] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N74', 1)) & 0xFFF
        self.board[376] = self.board[376] | (data & 0x0F00) >> 8
        self.board[377] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N75', 1)) & 0xFFF
        self.board[378] = (data & 0x0FF0) >> 4
        self.board[379] = self.board[379] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N76', 1)) & 0xFFF
        self.board[379] = self.board[379] | (data & 0x0F00) >> 8
        self.board[380] = data & 0x00FF

        self.board[382] = 0x13
        data = self.volt_float_data_convert(self.data.get('N77', 1)) & 0xFFF
        self.board[383] = (data & 0x0FF0) >> 4
        self.board[384] = self.board[384] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N78', 1)) & 0xFFF
        self.board[384] = self.board[384] | (data & 0x0F00) >> 8
        self.board[385] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N79', 1)) & 0xFFF
        self.board[386] = (data & 0x0FF0) >> 4
        self.board[387] = self.board[387] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N80', 1)) & 0xFFF
        self.board[387] = self.board[387] | (data & 0x0F00) >> 8
        self.board[388] = data & 0x00FF

        self.board[390] = 0x14
        data = self.volt_float_data_convert(self.data.get('N81', 1)) & 0xFFF
        self.board[391] = (data & 0x0FF0) >> 4
        self.board[392] = self.board[392] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N82', 1)) & 0xFFF
        self.board[392] = self.board[392] | (data & 0x0F00) >> 8
        self.board[393] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N83', 1)) & 0xFFF
        self.board[394] = (data & 0x0FF0) >> 4
        self.board[395] = self.board[395] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N84', 1)) & 0xFFF
        self.board[395] = self.board[395] | (data & 0x0F00) >> 8
        self.board[396] = data & 0x00FF

        self.board[398] = 0x15
        data = self.volt_float_data_convert(self.data.get('N85', 1)) & 0xFFF
        self.board[399] = (data & 0x0FF0) >> 4
        self.board[400] = self.board[400] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N86', 1)) & 0xFFF
        self.board[400] = self.board[400] | (data & 0x0F00) >> 8
        self.board[401] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N87', 1)) & 0xFFF
        self.board[402] = (data & 0x0FF0) >> 4
        self.board[403] = self.board[403] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N88', 1)) & 0xFFF
        self.board[403] = self.board[403] | (data & 0x0F00) >> 8
        self.board[404] = data & 0x00FF

        self.board[406] = 0x16
        data = self.volt_float_data_convert(self.data.get('N89', 1)) & 0xFFF
        self.board[407] = (data & 0x0FF0) >> 4
        self.board[408] = self.board[408] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N90', 1)) & 0xFFF
        self.board[408] = self.board[408] | (data & 0x0F00) >> 8
        self.board[409] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N91', 1)) & 0xFFF
        self.board[410] = (data & 0x0FF0) >> 4
        self.board[411] = self.board[411] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N92', 1)) & 0xFFF
        self.board[411] = self.board[411] | (data & 0x0F00) >> 8
        self.board[412] = data & 0x00FF

        self.board[414] = 0x17
        data = self.volt_float_data_convert(self.data.get('N93', 1)) & 0xFFF
        self.board[415] = (data & 0x0FF0) >> 4
        self.board[416] = self.board[416] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N94', 1)) & 0xFFF
        self.board[416] = self.board[416] | (data & 0x0F00) >> 8
        self.board[417] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N95', 1)) & 0xFFF
        self.board[418] = (data & 0x0FF0) >> 4
        self.board[419] = self.board[419] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N96', 1)) & 0xFFF
        self.board[419] = self.board[419] | (data & 0x0F00) >> 8
        self.board[420] = data & 0x00FF

        self.board[422] = 0x18
        data = self.volt_float_data_convert(self.data.get('N97', 1)) & 0xFFF
        self.board[423] = (data & 0x0FF0) >> 4
        self.board[424] = self.board[424] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N98', 1)) & 0xFFF
        self.board[424] = self.board[424] | (data & 0x0F00) >> 8
        self.board[425] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N99', 1)) & 0xFFF
        self.board[426] = (data & 0x0FF0) >> 4
        self.board[427] = self.board[427] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N100', 1)) & 0xFFF
        self.board[427] = self.board[427] | (data & 0x0F00) >> 8
        self.board[428] = data & 0x00FF

        self.board[430] = 0x19
        data = self.volt_float_data_convert(self.data.get('N101', 1)) & 0xFFF
        self.board[431] = (data & 0x0FF0) >> 4
        self.board[432] = self.board[432] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N102', 1)) & 0xFFF
        self.board[432] = self.board[432] | (data & 0x0F00) >> 8
        self.board[433] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N103', 1)) & 0xFFF
        self.board[434] = (data & 0x0FF0) >> 4
        self.board[435] = self.board[435] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N104', 1)) & 0xFFF
        self.board[435] = self.board[435] | (data & 0x0F00) >> 8
        self.board[436] = data & 0x00FF

        self.board[438] = 0x1A
        data = self.volt_float_data_convert(self.data.get('N105', 1)) & 0xFFF
        self.board[439] = (data & 0x0FF0) >> 4
        self.board[440] = self.board[440] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N106', 1)) & 0xFFF
        self.board[440] = self.board[440] | (data & 0x0F00) >> 8
        self.board[441] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N107', 1)) & 0xFFF
        self.board[442] = (data & 0x0FF0) >> 4
        self.board[443] = self.board[443] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N108', 1)) & 0xFFF
        self.board[443] = self.board[443] | (data & 0x0F00) >> 8
        self.board[444] = data & 0x00FF

        self.board[446] = 0x1B
        data = self.volt_float_data_convert(self.data.get('N109', 1)) & 0xFFF
        self.board[447] = (data & 0x0FF0) >> 4
        self.board[448] = self.board[448] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N110', 1)) & 0xFFF
        self.board[448] = self.board[448] | (data & 0x0F00) >> 8
        self.board[449] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N111', 1)) & 0xFFF
        self.board[450] = (data & 0x0FF0) >> 4
        self.board[451] = self.board[451] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N112', 1)) & 0xFFF
        self.board[451] = self.board[451] | (data & 0x0F00) >> 8
        self.board[452] = data & 0x00FF

        self.board[454] = 0x1C
        data = self.volt_float_data_convert(self.data.get('N113', 1)) & 0xFFF
        self.board[455] = (data & 0x0FF0) >> 4
        self.board[456] = self.board[456] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N114', 1)) & 0xFFF
        self.board[456] = self.board[456] | (data & 0x0F00) >> 8
        self.board[457] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N115', 1)) & 0xFFF
        self.board[458] = (data & 0x0FF0) >> 4
        self.board[459] = self.board[459] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N116', 1)) & 0xFFF
        self.board[459] = self.board[459] | (data & 0x0F00) >> 8
        self.board[460] = data & 0x00FF

        self.board[462] = 0x1D
        data = self.volt_float_data_convert(self.data.get('N117', 1)) & 0xFFF
        self.board[463] = (data & 0x0FF0) >> 4
        self.board[464] = self.board[464] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N118', 1)) & 0xFFF
        self.board[464] = self.board[464] | (data & 0x0F00) >> 8
        self.board[465] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N119', 1)) & 0xFFF
        self.board[466] = (data & 0x0FF0) >> 4
        self.board[467] = self.board[467] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N120', 1)) & 0xFFF
        self.board[467] = self.board[467] | (data & 0x0F00) >> 8
        self.board[468] = data & 0x00FF

        self.board[470] = 0x1E
        data = self.volt_float_data_convert(self.data.get('N121', 1)) & 0xFFF
        self.board[471] = (data & 0x0FF0) >> 4
        self.board[472] = self.board[472] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N122', 1)) & 0xFFF
        self.board[472] = self.board[472] | (data & 0x0F00) >> 8
        self.board[473] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N123', 1)) & 0xFFF
        self.board[474] = (data & 0x0FF0) >> 4
        self.board[475] = self.board[475] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N124', 1)) & 0xFFF
        self.board[475] = self.board[475] | (data & 0x0F00) >> 8
        self.board[476] = data & 0x00FF

        self.board[478] = 0x1F
        data = self.volt_float_data_convert(self.data.get('N125', 1)) & 0xFFF
        self.board[479] = (data & 0x0FF0) >> 4
        self.board[480] = self.board[480] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N126', 1)) & 0xFFF
        self.board[480] = self.board[480] | (data & 0x0F00) >> 8
        self.board[481] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N127', 1)) & 0xFFF
        self.board[482] = (data & 0x0FF0) >> 4
        self.board[483] = self.board[483] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N128', 1)) & 0xFFF
        self.board[483] = self.board[483] | (data & 0x0F00) >> 8
        self.board[484] = data & 0x00FF

        self.board[486] = 0x20
        data = self.volt_float_data_convert(self.data.get('N129', 1)) & 0xFFF
        self.board[487] = (data & 0x0FF0) >> 4
        self.board[488] = self.board[488] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N130', 1)) & 0xFFF
        self.board[488] = self.board[488] | (data & 0x0F00) >> 8
        self.board[489] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N131', 1)) & 0xFFF
        self.board[490] = (data & 0x0FF0) >> 4
        self.board[491] = self.board[491] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N132', 1)) & 0xFFF
        self.board[491] = self.board[491] | (data & 0x0F00) >> 8
        self.board[492] = data & 0x00FF

        self.board[494] = 0x21
        data = self.volt_float_data_convert(self.data.get('N133', 1)) & 0xFFF
        self.board[495] = (data & 0x0FF0) >> 4
        self.board[496] = self.board[496] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N134', 1)) & 0xFFF
        self.board[496] = self.board[496] | (data & 0x0F00) >> 8
        self.board[497] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N135', 1)) & 0xFFF
        self.board[498] = (data & 0x0FF0) >> 4
        self.board[499] = self.board[499] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N136', 1)) & 0xFFF
        self.board[499] = self.board[499] | (data & 0x0F00) >> 8
        self.board[500] = data & 0x00FF

        self.board[502] = 0x22
        data = self.volt_float_data_convert(self.data.get('N137', 1)) & 0xFFF
        self.board[503] = (data & 0x0FF0) >> 4
        self.board[504] = self.board[504] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N138', 1)) & 0xFFF
        self.board[504] = self.board[504] | (data & 0x0F00) >> 8
        self.board[505] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N139', 1)) & 0xFFF
        self.board[506] = (data & 0x0FF0) >> 4
        self.board[507] = self.board[507] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N140', 1)) & 0xFFF
        self.board[507] = self.board[507] | (data & 0x0F00) >> 8
        self.board[508] = data & 0x00FF

        self.board[510] = 0x23
        data = self.volt_float_data_convert(self.data.get('N141', 1)) & 0xFFF
        self.board[511] = (data & 0x0FF0) >> 4
        self.board[512] = self.board[512] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N142', 1)) & 0xFFF
        self.board[512] = self.board[512] | (data & 0x0F00) >> 8
        self.board[513] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N143', 1)) & 0xFFF
        self.board[514] = (data & 0x0FF0) >> 4
        self.board[515] = self.board[515] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N144', 1)) & 0xFFF
        self.board[515] = self.board[515] | (data & 0x0F00) >> 8
        self.board[516] = data & 0x00FF

        self.board[518] = 0x24
        data = self.volt_float_data_convert(self.data.get('N145', 1)) & 0xFFF
        self.board[519] = (data & 0x0FF0) >> 4
        self.board[520] = self.board[520] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N146', 1)) & 0xFFF
        self.board[520] = self.board[520] | (data & 0x0F00) >> 8
        self.board[521] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N147', 1)) & 0xFFF
        self.board[522] = (data & 0x0FF0) >> 4
        self.board[523] = self.board[523] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N148', 1)) & 0xFFF
        self.board[523] = self.board[523] | (data & 0x0F00) >> 8
        self.board[524] = data & 0x00FF

        self.board[526] = 0x25
        data = self.volt_float_data_convert(self.data.get('N149', 1)) & 0xFFF
        self.board[527] = (data & 0x0FF0) >> 4
        self.board[528] = self.board[528] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N150', 1)) & 0xFFF
        self.board[528] = self.board[528] | (data & 0x0F00) >> 8
        self.board[529] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N151', 1)) & 0xFFF
        self.board[530] = (data & 0x0FF0) >> 4
        self.board[531] = self.board[531] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N152', 1)) & 0xFFF
        self.board[531] = self.board[531] | (data & 0x0F00) >> 8
        self.board[532] = data & 0x00FF

        self.board[534] = 0x26
        data = self.volt_float_data_convert(self.data.get('N153', 1)) & 0xFFF
        self.board[535] = (data & 0x0FF0) >> 4
        self.board[536] = self.board[536] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N154', 1)) & 0xFFF
        self.board[536] = self.board[536] | (data & 0x0F00) >> 8
        self.board[537] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N155', 1)) & 0xFFF
        self.board[538] = (data & 0x0FF0) >> 4
        self.board[539] = self.board[539] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N156', 1)) & 0xFFF
        self.board[539] = self.board[539] | (data & 0x0F00) >> 8
        self.board[540] = data & 0x00FF

        self.board[542] = 0x27
        data = self.volt_float_data_convert(self.data.get('N157', 1)) & 0xFFF
        self.board[543] = (data & 0x0FF0) >> 4
        self.board[544] = self.board[544] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N158', 1)) & 0xFFF
        self.board[544] = self.board[544] | (data & 0x0F00) >> 8
        self.board[545] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N159', 1)) & 0xFFF
        self.board[546] = (data & 0x0FF0) >> 4
        self.board[547] = self.board[547] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N160', 1)) & 0xFFF
        self.board[547] = self.board[547] | (data & 0x0F00) >> 8
        self.board[548] = data & 0x00FF

        self.board[550] = 0x28
        data = self.volt_float_data_convert(self.data.get('N161', 1)) & 0xFFF
        self.board[551] = (data & 0x0FF0) >> 4
        self.board[552] = self.board[552] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N162', 1)) & 0xFFF
        self.board[552] = self.board[552] | (data & 0x0F00) >> 8
        self.board[553] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N163', 1)) & 0xFFF
        self.board[554] = (data & 0x0FF0) >> 4
        self.board[555] = self.board[555] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N164', 1)) & 0xFFF
        self.board[555] = self.board[555] | (data & 0x0F00) >> 8
        self.board[556] = data & 0x00FF

        self.board[558] = 0x29
        data = self.volt_float_data_convert(self.data.get('N165', 1)) & 0xFFF
        self.board[559] = (data & 0x0FF0) >> 4
        self.board[560] = self.board[560] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N166', 1)) & 0xFFF
        self.board[560] = self.board[560] | (data & 0x0F00) >> 8
        self.board[561] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N167', 1)) & 0xFFF
        self.board[562] = (data & 0x0FF0) >> 4
        self.board[563] = self.board[563] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N168', 1)) & 0xFFF
        self.board[563] = self.board[563] | (data & 0x0F00) >> 8
        self.board[564] = data & 0x00FF

        self.board[566] = 0x2A
        data = self.volt_float_data_convert(self.data.get('N169', 1)) & 0xFFF
        self.board[567] = (data & 0x0FF0) >> 4
        self.board[568] = self.board[568] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N170', 1)) & 0xFFF
        self.board[568] = self.board[568] | (data & 0x0F00) >> 8
        self.board[569] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N171', 1)) & 0xFFF
        self.board[570] = (data & 0x0FF0) >> 4
        self.board[571] = self.board[571] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N172', 1)) & 0xFFF
        self.board[571] = self.board[571] | (data & 0x0F00) >> 8
        self.board[572] = data & 0x00FF

        self.board[574] = 0x2B
        data = self.volt_float_data_convert(self.data.get('N173', 1)) & 0xFFF
        self.board[575] = (data & 0x0FF0) >> 4
        self.board[576] = self.board[576] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N174', 1)) & 0xFFF
        self.board[576] = self.board[576] | (data & 0x0F00) >> 8
        self.board[577] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N175', 1)) & 0xFFF
        self.board[578] = (data & 0x0FF0) >> 4
        self.board[579] = self.board[579] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N176', 1)) & 0xFFF
        self.board[579] = self.board[579] | (data & 0x0F00) >> 8
        self.board[580] = data & 0x00FF

        self.board[582] = 0x2C
        data = self.volt_float_data_convert(self.data.get('N177', 1)) & 0xFFF
        self.board[583] = (data & 0x0FF0) >> 4
        self.board[584] = self.board[584] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N178', 1)) & 0xFFF
        self.board[584] = self.board[584] | (data & 0x0F00) >> 8
        self.board[585] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N179', 1)) & 0xFFF
        self.board[586] = (data & 0x0FF0) >> 4
        self.board[587] = self.board[587] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N180', 1)) & 0xFFF
        self.board[587] = self.board[587] | (data & 0x0F00) >> 8
        self.board[588] = data & 0x00FF

        self.board[590] = 0x2D
        data = self.volt_float_data_convert(self.data.get('N181', 1)) & 0xFFF
        self.board[591] = (data & 0x0FF0) >> 4
        self.board[592] = self.board[592] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N182', 1)) & 0xFFF
        self.board[592] = self.board[592] | (data & 0x0F00) >> 8
        self.board[593] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N183', 1)) & 0xFFF
        self.board[594] = (data & 0x0FF0) >> 4
        self.board[595] = self.board[595] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N184', 1)) & 0xFFF
        self.board[595] = self.board[595] | (data & 0x0F00) >> 8
        self.board[596] = data & 0x00FF

        self.board[598] = 0x2E
        data = self.volt_float_data_convert(self.data.get('N185', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N185
        self.board[599] = (data & 0x0FF0) >> 4
        self.board[600] = self.board[600] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N186', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N186
        self.board[600] = self.board[600] | (data & 0x0F00) >> 8
        self.board[601] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N187', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N187
        self.board[602] = (data & 0x0FF0) >> 4
        self.board[603] = self.board[603] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N188', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N188
        self.board[603] = self.board[603] | (data & 0x0F00) >> 8
        self.board[604] = data & 0x00FF

        self.board[606] = 0x2F
        data = self.volt_float_data_convert(self.data.get('N189', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N189
        self.board[607] = (data & 0x0FF0) >> 4
        self.board[608] = self.board[608] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N190', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N190
        self.board[608] = self.board[608] | (data & 0x0F00) >> 8
        self.board[609] = data & 0x00FF
        data = self.volt_float_data_convert(self.data.get('N191', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N191
        self.board[610] = (data & 0x0FF0) >> 4
        self.board[611] = self.board[611] | (data & 0x000F) << 4
        data = self.volt_float_data_convert(self.data.get('N192', 1)) & 0xFFF  # [1, 5] 电池包电芯电压Cell_N192
        self.board[611] = self.board[611] | (data & 0x0F00) >> 8
        self.board[612] = data & 0x00FF

    def cell_temp_data(self):
        """
        通过26F 最多发送 128个字节，不同电池类型有差异
        614-741
        0，P50 50Ah；#50度电池，已经去掉了
        1，P70 102Ah；#70度电池
        2，P84；#84度电池，已淘汰
        3，P70 102Ah X；#70度电池，材料差异
        4，P84锁电；84度锁成70度，换电调度
        5，P70 LFP； 70度，材料不同，现在未使用
        6， P100 NCM； 100度电池，NCM材料
        7，P100 锁电70；100度锁70
        8，P75；75度
        9，P100 锁电84；已淘汰
        10，P150；现在没有
        11，P100 锁电75；当75度使用
        12～16，预留
        :return:
        """
        if self.battery_type in [6, 7, 9, 11, 13, 14]:
            # battery_module_type = CAP_280AH; 12帧, 48个数据
            # print("cell_12_4_temp_data")
            self.cell_12_4_temp_data()
            self.board[998] = 24
        elif self.battery_type in [1, 3, ]:
            # battery_module_type = CAP_102AH; 16帧, 64个数据
            self.cell_16_4_temp_data()
            self.board[998] = 48
        elif self.battery_type in [2, 4]:
            # battery_module_type = CAP_120AH
            self.cell_16_6_temp_data()  #
            self.board[998] = 48
        # elif self.battery_type in [0, ]:  # 50, 电池处理
        #     # battery_module_type = CAP_50AH;
        #     self.cell_96_temp_data()
        #     self.board[998] = 48
        elif self.battery_type in [8, ]:
            # battery_module_type = CAP_75KWH; 8帧, 48个数据
            self.cell_8_6_temp_data()
            self.board[998] = 30

    def cell_12_4_temp_data(self):
        """
        发送12帧数据，每帧4个值
        614:709
        :return:
        """
        self.board[999] = 12
        self.board[614] = 0x0
        data = self.int_data_covert(self.data.get('T1_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T1_A1
        self.board[615] = data & 0xFF
        data = self.int_data_covert(self.data.get('T1_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T1_A2
        self.board[616] = data & 0xFF
        data = self.int_data_covert(self.data.get('T1_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T1_B1
        self.board[618] = data & 0xFF
        data = self.int_data_covert(self.data.get('T1_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T1_B2
        self.board[619] = data & 0xFF

        self.board[622] = 0x1
        data = self.int_data_covert(self.data.get('T2_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T2_A1
        self.board[623] = data & 0xFF
        data = self.int_data_covert(self.data.get('T2_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T2_A2
        self.board[624] = data & 0xFF
        data = self.int_data_covert(self.data.get('T2_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T2_B1
        self.board[626] = data & 0xFF
        data = self.int_data_covert(self.data.get('T2_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T2_B2
        self.board[627] = data & 0xFF

        self.board[630] = 0x2
        data = self.int_data_covert(self.data.get('T3_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T3_A1
        self.board[631] = data & 0xFF
        data = self.int_data_covert(self.data.get('T3_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T3_A2
        self.board[632] = data & 0xFF
        data = self.int_data_covert(self.data.get('T3_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T3_B1
        self.board[634] = data & 0xFF
        data = self.int_data_covert(self.data.get('T3_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T3_B2
        self.board[635] = data & 0xFF

        self.board[638] = 0x3
        data = self.int_data_covert(self.data.get('T4_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T4_A1
        self.board[639] = data & 0xFF
        data = self.int_data_covert(self.data.get('T4_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T4_A2
        self.board[640] = data & 0xFF
        data = self.int_data_covert(self.data.get('T4_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T4_B1
        self.board[642] = data & 0xFF
        data = self.int_data_covert(self.data.get('T4_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T4_B2
        self.board[643] = data & 0xFF

        self.board[646] = 0x4
        data = self.int_data_covert(self.data.get('T5_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T5_A1
        self.board[647] = data & 0xFF
        data = self.int_data_covert(self.data.get('T5_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T5_A2
        self.board[648] = data & 0xFF
        data = self.int_data_covert(self.data.get('T5_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T5_B1
        self.board[650] = data & 0xFF
        data = self.int_data_covert(self.data.get('T5_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T5_B2
        self.board[651] = data & 0xFF

        self.board[654] = 0x5
        data = self.int_data_covert(self.data.get('T6_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T6_A1
        self.board[655] = data & 0xFF
        data = self.int_data_covert(self.data.get('T6_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T6_A2
        self.board[656] = data & 0xFF
        data = self.int_data_covert(self.data.get('T6_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T6_B1
        self.board[658] = data & 0xFF
        data = self.int_data_covert(self.data.get('T6_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T6_B2
        self.board[659] = data & 0xFF

        self.board[662] = 0x6
        data = self.int_data_covert(self.data.get('T7_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T7_A1
        self.board[663] = data & 0xFF
        data = self.int_data_covert(self.data.get('T7_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T7_A2
        self.board[664] = data & 0xFF
        data = self.int_data_covert(self.data.get('T7_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T7_B1
        self.board[666] = data & 0xFF
        data = self.int_data_covert(self.data.get('T7_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T7_B2
        self.board[667] = data & 0xFF

        self.board[670] = 0x7
        data = self.int_data_covert(self.data.get('T8_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T8_A1
        self.board[671] = data & 0xFF
        data = self.int_data_covert(self.data.get('T8_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T8_A2
        self.board[672] = data & 0xFF
        data = self.int_data_covert(self.data.get('T8_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T8_B1
        self.board[674] = data & 0xFF
        data = self.int_data_covert(self.data.get('T8_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T8_B2
        self.board[675] = data & 0xFF

        self.board[678] = 0x8
        data = self.int_data_covert(self.data.get('T9_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T9_A1
        self.board[679] = data & 0xFF
        data = self.int_data_covert(self.data.get('T9_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T9_A2
        self.board[680] = data & 0xFF
        data = self.int_data_covert(self.data.get('T9_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T9_B1
        self.board[682] = data & 0xFF
        data = self.int_data_covert(self.data.get('T9_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T9_B2
        self.board[683] = data & 0xFF

        self.board[686] = 0x9
        data = self.int_data_covert(self.data.get('T10_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T10_A1
        self.board[687] = data & 0xFF
        data = self.int_data_covert(self.data.get('T10_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T10_A2
        self.board[688] = data & 0xFF
        data = self.int_data_covert(self.data.get('T10_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T10_B1
        self.board[690] = data & 0xFF
        data = self.int_data_covert(self.data.get('T10_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T10_B2
        self.board[691] = data & 0xFF

        self.board[694] = 0xA
        data = self.int_data_covert(self.data.get('T11_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T11_A1
        self.board[695] = data & 0xFF
        data = self.int_data_covert(self.data.get('T11_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T11_A2
        self.board[696] = data & 0xFF
        data = self.int_data_covert(self.data.get('T11_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T11_B1
        self.board[698] = data & 0xFF
        data = self.int_data_covert(self.data.get('T11_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T11_B2
        self.board[699] = data & 0xFF

        self.board[702] = 0xB
        data = self.int_data_covert(self.data.get('T12_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T12_A1
        self.board[703] = data & 0xFF
        data = self.int_data_covert(self.data.get('T12_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T12_A2
        self.board[704] = data & 0xFF
        data = self.int_data_covert(self.data.get('T12_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T12_B1
        self.board[706] = data & 0xFF
        data = self.int_data_covert(self.data.get('T12_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T12_B2
        self.board[707] = data & 0xFF

    def cell_8_6_temp_data(self):
        """
        614开始, 678截止 发送8帧数据，每帧6个值
        :return:
        """
        self.board[999] = 8
        self.board[614] = 0x0
        data = self.int_data_covert(self.data.get('T1_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T1_A1
        self.board[615] = data & 0xFF
        data = self.int_data_covert(self.data.get('T1_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T1_A2
        self.board[616] = data & 0xFF
        data = self.int_data_covert(self.data.get('T1_A3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T1_A3
        self.board[617] = data & 0xFF
        data = self.int_data_covert(self.data.get('T1_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T1_B1
        self.board[618] = data & 0xFF
        data = self.int_data_covert(self.data.get('T1_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T1_B2
        self.board[619] = data & 0xFF
        data = self.int_data_covert(self.data.get('T1_B3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T1_B3
        self.board[620] = data & 0xFF

        self.board[622] = 0x1
        data = self.int_data_covert(self.data.get('T2_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T2_A1
        self.board[623] = data & 0xFF
        data = self.int_data_covert(self.data.get('T2_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T2_A2
        self.board[624] = data & 0xFF
        data = self.int_data_covert(self.data.get('T2_A3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T2_A3
        self.board[625] = data & 0xFF
        data = self.int_data_covert(self.data.get('T2_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T2_B1
        self.board[626] = data & 0xFF
        data = self.int_data_covert(self.data.get('T2_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T2_B2
        self.board[627] = data & 0xFF
        data = self.int_data_covert(self.data.get('T2_B3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T2_B3
        self.board[628] = data & 0xFF

        self.board[630] = 0x2
        data = self.int_data_covert(self.data.get('T3_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T3_A1
        self.board[631] = data & 0xFF
        data = self.int_data_covert(self.data.get('T3_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T3_A2
        self.board[632] = data & 0xFF
        data = self.int_data_covert(self.data.get('T3_A3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T3_A3
        self.board[633] = data & 0xFF
        data = self.int_data_covert(self.data.get('T3_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T3_B1
        self.board[634] = data & 0xFF
        data = self.int_data_covert(self.data.get('T3_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T3_B2
        self.board[635] = data & 0xFF
        data = self.int_data_covert(self.data.get('T3_B3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T3_B3
        self.board[636] = data & 0xFF

        self.board[638] = 0x3
        data = self.int_data_covert(self.data.get('T4_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T4_A1
        self.board[639] = data & 0xFF
        data = self.int_data_covert(self.data.get('T4_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T4_A2
        self.board[640] = data & 0xFF
        data = self.int_data_covert(self.data.get('T4_A3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T4_A3
        self.board[641] = data & 0xFF
        data = self.int_data_covert(self.data.get('T4_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T4_B1
        self.board[642] = data & 0xFF
        data = self.int_data_covert(self.data.get('T4_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T4_B2
        self.board[643] = data & 0xFF
        data = self.int_data_covert(self.data.get('T4_B3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T4_B3
        self.board[644] = data & 0xFF

        self.board[646] = 0x4
        data = self.int_data_covert(self.data.get('T5_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T5_A1
        self.board[647] = data & 0xFF
        data = self.int_data_covert(self.data.get('T5_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T5_A2
        self.board[648] = data & 0xFF
        data = self.int_data_covert(self.data.get('T5_A3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T5_A3
        self.board[649] = data & 0xFF
        data = self.int_data_covert(self.data.get('T5_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T5_B1
        self.board[650] = data & 0xFF
        data = self.int_data_covert(self.data.get('T5_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T5_B2
        self.board[651] = data & 0xFF
        data = self.int_data_covert(self.data.get('T5_B3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T5_B3
        self.board[652] = data & 0xFF

        self.board[654] = 0x5
        data = self.int_data_covert(self.data.get('T6_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T6_A1
        self.board[655] = data & 0xFF
        data = self.int_data_covert(self.data.get('T6_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T6_A2
        self.board[656] = data & 0xFF
        data = self.int_data_covert(self.data.get('T6_A3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T6_A3
        self.board[657] = data & 0xFF
        data = self.int_data_covert(self.data.get('T6_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T6_B1
        self.board[658] = data & 0xFF
        data = self.int_data_covert(self.data.get('T6_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T6_B2
        self.board[659] = data & 0xFF
        data = self.int_data_covert(self.data.get('T6_B3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T6_B3
        self.board[660] = data & 0xFF

        self.board[662] = 0x6
        data = self.int_data_covert(self.data.get('T7_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T7_A1
        self.board[663] = data & 0xFF
        data = self.int_data_covert(self.data.get('T7_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T7_A2
        self.board[664] = data & 0xFF
        data = self.int_data_covert(self.data.get('T7_A3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T7_A3
        self.board[665] = data & 0xFF
        data = self.int_data_covert(self.data.get('T7_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T7_B1
        self.board[666] = data & 0xFF
        data = self.int_data_covert(self.data.get('T7_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T7_B2
        self.board[667] = data & 0xFF
        data = self.int_data_covert(self.data.get('T7_B3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T7_B3
        self.board[668] = data & 0xFF

        self.board[670] = 0x7
        data = self.int_data_covert(self.data.get('T8_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T8_A1
        self.board[671] = data & 0xFF
        data = self.int_data_covert(self.data.get('T8_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T8_A2
        self.board[672] = data & 0xFF
        data = self.int_data_covert(self.data.get('T8_A3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T8_A3
        self.board[673] = data & 0xFF
        data = self.int_data_covert(self.data.get('T8_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T8_B1
        self.board[674] = data & 0xFF
        data = self.int_data_covert(self.data.get('T8_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T8_B2
        self.board[675] = data & 0xFF
        data = self.int_data_covert(self.data.get('T8_B3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T8_B3
        self.board[676] = data & 0xFF

    def cell_16_4_temp_data(self):
        """
        614开始, 741截止 发送16帧数据，每帧4个值
        :return:
        """
        self.board[999] = 16
        self.board[614] = 0x0
        data = self.int_data_covert(self.data.get('T1_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T1_A1
        self.board[615] = data & 0xFF
        data = self.int_data_covert(self.data.get('T1_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T1_A2
        self.board[616] = data & 0xFF
        data = self.int_data_covert(self.data.get('T1_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T1_B1
        self.board[618] = data & 0xFF
        data = self.int_data_covert(self.data.get('T1_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T1_B2
        self.board[619] = data & 0xFF

        self.board[622] = 0x1
        data = self.int_data_covert(self.data.get('T2_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T2_A1
        self.board[623] = data & 0xFF
        data = self.int_data_covert(self.data.get('T2_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T2_A2
        self.board[624] = data & 0xFF
        data = self.int_data_covert(self.data.get('T2_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T2_B1
        self.board[626] = data & 0xFF
        data = self.int_data_covert(self.data.get('T2_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T2_B2
        self.board[627] = data & 0xFF

        self.board[630] = 0x2
        data = self.int_data_covert(self.data.get('T3_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T3_A1
        self.board[631] = data & 0xFF
        data = self.int_data_covert(self.data.get('T3_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T3_A2
        self.board[632] = data & 0xFF
        data = self.int_data_covert(self.data.get('T3_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T3_B1
        self.board[634] = data & 0xFF
        data = self.int_data_covert(self.data.get('T3_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T3_B2
        self.board[635] = data & 0xFF

        self.board[638] = 0x3
        data = self.int_data_covert(self.data.get('T4_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T4_A1
        self.board[639] = data & 0xFF
        data = self.int_data_covert(self.data.get('T4_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T4_A2
        self.board[640] = data & 0xFF
        data = self.int_data_covert(self.data.get('T4_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T4_B1
        self.board[642] = data & 0xFF
        data = self.int_data_covert(self.data.get('T4_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T4_B2
        self.board[643] = data & 0xFF

        self.board[646] = 0x4
        data = self.int_data_covert(self.data.get('T5_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T5_A1
        self.board[647] = data & 0xFF
        data = self.int_data_covert(self.data.get('T5_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T5_A2
        self.board[648] = data & 0xFF
        data = self.int_data_covert(self.data.get('T5_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T5_B1
        self.board[650] = data & 0xFF
        data = self.int_data_covert(self.data.get('T5_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T5_B2
        self.board[651] = data & 0xFF

        self.board[654] = 0x5
        data = self.int_data_covert(self.data.get('T6_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T6_A1
        self.board[655] = data & 0xFF
        data = self.int_data_covert(self.data.get('T6_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T6_A2
        self.board[656] = data & 0xFF
        data = self.int_data_covert(self.data.get('T6_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T6_B1
        self.board[658] = data & 0xFF
        data = self.int_data_covert(self.data.get('T6_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T6_B2
        self.board[659] = data & 0xFF

        self.board[662] = 0x6
        data = self.int_data_covert(self.data.get('T7_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T7_A1
        self.board[663] = data & 0xFF
        data = self.int_data_covert(self.data.get('T7_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T7_A2
        self.board[664] = data & 0xFF
        data = self.int_data_covert(self.data.get('T7_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T7_B1
        self.board[666] = data & 0xFF
        data = self.int_data_covert(self.data.get('T7_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T7_B2
        self.board[667] = data & 0xFF

        self.board[670] = 0x7
        data = self.int_data_covert(self.data.get('T8_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T8_A1
        self.board[671] = data & 0xFF
        data = self.int_data_covert(self.data.get('T8_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T8_A2
        self.board[672] = data & 0xFF
        data = self.int_data_covert(self.data.get('T8_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T8_B1
        self.board[674] = data & 0xFF
        data = self.int_data_covert(self.data.get('T8_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T8_B2
        self.board[675] = data & 0xFF

        self.board[678] = 0x8
        data = self.int_data_covert(self.data.get('T9_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T9_A1
        self.board[679] = data & 0xFF
        data = self.int_data_covert(self.data.get('T9_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T9_A2
        self.board[680] = data & 0xFF
        data = self.int_data_covert(self.data.get('T9_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T9_B1
        self.board[682] = data & 0xFF
        data = self.int_data_covert(self.data.get('T9_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T9_B2
        self.board[683] = data & 0xFF

        self.board[686] = 0x9
        data = self.int_data_covert(self.data.get('T10_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T10_A1
        self.board[687] = data & 0xFF
        data = self.int_data_covert(self.data.get('T10_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T10_A2
        self.board[688] = data & 0xFF
        data = self.int_data_covert(self.data.get('T10_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T10_B1
        self.board[690] = data & 0xFF
        data = self.int_data_covert(self.data.get('T10_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T10_B2
        self.board[691] = data & 0xFF

        self.board[694] = 0xA
        data = self.int_data_covert(self.data.get('T11_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T11_A1
        self.board[695] = data & 0xFF
        data = self.int_data_covert(self.data.get('T11_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T11_A2
        self.board[696] = data & 0xFF
        data = self.int_data_covert(self.data.get('T11_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T11_B1
        self.board[698] = data & 0xFF
        data = self.int_data_covert(self.data.get('T11_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T11_B2
        self.board[699] = data & 0xFF

        self.board[702] = 0xB
        data = self.int_data_covert(self.data.get('T12_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T12_A1
        self.board[703] = data & 0xFF
        data = self.int_data_covert(self.data.get('T12_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T12_A2
        self.board[704] = data & 0xFF
        data = self.int_data_covert(self.data.get('T12_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T12_B1
        self.board[706] = data & 0xFF
        data = self.int_data_covert(self.data.get('T12_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T12_B2
        self.board[707] = data & 0xFF

        self.board[710] = 0xC
        data = self.int_data_covert(self.data.get('T13_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T13_A1
        self.board[711] = data & 0xFF
        data = self.int_data_covert(self.data.get('T13_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T13_A2
        self.board[712] = data & 0xFF
        data = self.int_data_covert(self.data.get('T13_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T13_B1
        self.board[714] = data & 0xFF
        data = self.int_data_covert(self.data.get('T13_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T13_B2
        self.board[715] = data & 0xFF

        self.board[718] = 0xD
        data = self.int_data_covert(self.data.get('T14_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T14_A1
        self.board[719] = data & 0xFF
        data = self.int_data_covert(self.data.get('T14_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T14_A2
        self.board[720] = data & 0xFF
        data = self.int_data_covert(self.data.get('T14_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T14_B1
        self.board[722] = data & 0xFF
        data = self.int_data_covert(self.data.get('T14_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T14_B2
        self.board[723] = data & 0xFF

        self.board[726] = 0xE
        data = self.int_data_covert(self.data.get('T15_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T15_A1
        self.board[727] = data & 0xFF
        data = self.int_data_covert(self.data.get('T15_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T15_A2
        self.board[728] = data & 0xFF
        data = self.int_data_covert(self.data.get('T15_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T15_B1
        self.board[730] = data & 0xFF
        data = self.int_data_covert(self.data.get('T15_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T15_B2
        self.board[731] = data & 0xFF

        self.board[734] = 0xF
        data = self.int_data_covert(self.data.get('T16_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T16_A1
        self.board[735] = data & 0xFF
        data = self.int_data_covert(self.data.get('T16_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T16_A2
        self.board[736] = data & 0xFF
        data = self.int_data_covert(self.data.get('T16_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T16_B1
        self.board[738] = data & 0xFF
        data = self.int_data_covert(self.data.get('T16_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T16_B2
        self.board[739] = data & 0xFF

    def cell_16_6_temp_data(self):
        """
        614开始, 741截止 发送16帧数据，每帧6个值
        :return:
        """
        self.board[999] = 16
        self.board[614] = 0x0
        data = self.int_data_covert(self.data.get('T1_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T1_A1
        self.board[615] = data & 0xFF
        data = self.int_data_covert(self.data.get('T1_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T1_A2
        self.board[616] = data & 0xFF
        data = self.int_data_covert(self.data.get('T1_A3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T1_A3
        self.board[617] = data & 0xFF
        data = self.int_data_covert(self.data.get('T1_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T1_B1
        self.board[618] = data & 0xFF
        data = self.int_data_covert(self.data.get('T1_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T1_B2
        self.board[619] = data & 0xFF
        data = self.int_data_covert(self.data.get('T1_B3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T1_B3
        self.board[620] = data & 0xFF

        self.board[622] = 0x1
        data = self.int_data_covert(self.data.get('T2_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T2_A1
        self.board[623] = data & 0xFF
        data = self.int_data_covert(self.data.get('T2_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T2_A2
        self.board[624] = data & 0xFF
        data = self.int_data_covert(self.data.get('T2_A3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T2_A3
        self.board[625] = data & 0xFF
        data = self.int_data_covert(self.data.get('T2_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T2_B1
        self.board[626] = data & 0xFF
        data = self.int_data_covert(self.data.get('T2_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T2_B2
        self.board[627] = data & 0xFF
        data = self.int_data_covert(self.data.get('T2_B3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T2_B3
        self.board[628] = data & 0xFF

        self.board[630] = 0x2
        data = self.int_data_covert(self.data.get('T3_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T3_A1
        self.board[631] = data & 0xFF
        data = self.int_data_covert(self.data.get('T3_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T3_A2
        self.board[632] = data & 0xFF
        data = self.int_data_covert(self.data.get('T3_A3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T3_A3
        self.board[633] = data & 0xFF
        data = self.int_data_covert(self.data.get('T3_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T3_B1
        self.board[634] = data & 0xFF
        data = self.int_data_covert(self.data.get('T3_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T3_B2
        self.board[635] = data & 0xFF
        data = self.int_data_covert(self.data.get('T3_B3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T3_B3
        self.board[636] = data & 0xFF

        self.board[638] = 0x3
        data = self.int_data_covert(self.data.get('T4_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T4_A1
        self.board[639] = data & 0xFF
        data = self.int_data_covert(self.data.get('T4_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T4_A2
        self.board[640] = data & 0xFF
        data = self.int_data_covert(self.data.get('T4_A3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T4_A3
        self.board[641] = data & 0xFF
        data = self.int_data_covert(self.data.get('T4_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T4_B1
        self.board[642] = data & 0xFF
        data = self.int_data_covert(self.data.get('T4_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T4_B2
        self.board[643] = data & 0xFF
        data = self.int_data_covert(self.data.get('T4_B3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T4_B3
        self.board[644] = data & 0xFF

        self.board[646] = 0x4
        data = self.int_data_covert(self.data.get('T5_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T5_A1
        self.board[647] = data & 0xFF
        data = self.int_data_covert(self.data.get('T5_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T5_A2
        self.board[648] = data & 0xFF
        data = self.int_data_covert(self.data.get('T5_A3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T5_A3
        self.board[649] = data & 0xFF
        data = self.int_data_covert(self.data.get('T5_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T5_B1
        self.board[650] = data & 0xFF
        data = self.int_data_covert(self.data.get('T5_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T5_B2
        self.board[651] = data & 0xFF
        data = self.int_data_covert(self.data.get('T5_B3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T5_B3
        self.board[652] = data & 0xFF

        self.board[654] = 0x5
        data = self.int_data_covert(self.data.get('T6_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T6_A1
        self.board[655] = data & 0xFF
        data = self.int_data_covert(self.data.get('T6_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T6_A2
        self.board[656] = data & 0xFF
        data = self.int_data_covert(self.data.get('T6_A3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T6_A3
        self.board[657] = data & 0xFF
        data = self.int_data_covert(self.data.get('T6_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T6_B1
        self.board[658] = data & 0xFF
        data = self.int_data_covert(self.data.get('T6_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T6_B2
        self.board[659] = data & 0xFF
        data = self.int_data_covert(self.data.get('T6_B3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T6_B3
        self.board[660] = data & 0xFF

        self.board[662] = 0x6
        data = self.int_data_covert(self.data.get('T7_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T7_A1
        self.board[663] = data & 0xFF
        data = self.int_data_covert(self.data.get('T7_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T7_A2
        self.board[664] = data & 0xFF
        data = self.int_data_covert(self.data.get('T7_A3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T7_A3
        self.board[665] = data & 0xFF
        data = self.int_data_covert(self.data.get('T7_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T7_B1
        self.board[666] = data & 0xFF
        data = self.int_data_covert(self.data.get('T7_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T7_B2
        self.board[667] = data & 0xFF
        data = self.int_data_covert(self.data.get('T7_B3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T7_B3
        self.board[668] = data & 0xFF

        self.board[670] = 0x7
        data = self.int_data_covert(self.data.get('T8_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T8_A1
        self.board[671] = data & 0xFF
        data = self.int_data_covert(self.data.get('T8_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T8_A2
        self.board[672] = data & 0xFF
        data = self.int_data_covert(self.data.get('T8_A3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T8_A3
        self.board[673] = data & 0xFF
        data = self.int_data_covert(self.data.get('T8_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T8_B1
        self.board[674] = data & 0xFF
        data = self.int_data_covert(self.data.get('T8_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T8_B2
        self.board[675] = data & 0xFF
        data = self.int_data_covert(self.data.get('T8_B3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T8_B3
        self.board[676] = data & 0xFF

        self.board[678] = 0x8
        data = self.int_data_covert(self.data.get('T9_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T9_A1
        self.board[679] = data & 0xFF
        data = self.int_data_covert(self.data.get('T9_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T9_A2
        self.board[680] = data & 0xFF
        data = self.int_data_covert(self.data.get('T9_A3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T9_A3
        self.board[681] = data & 0xFF
        data = self.int_data_covert(self.data.get('T9_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T9_B1
        self.board[682] = data & 0xFF
        data = self.int_data_covert(self.data.get('T9_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T9_B2
        self.board[683] = data & 0xFF
        data = self.int_data_covert(self.data.get('T9_B3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T9_B3
        self.board[684] = data & 0xFF

        self.board[686] = 0x9
        data = self.int_data_covert(self.data.get('T10_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T10_A1
        self.board[687] = data & 0xFF
        data = self.int_data_covert(self.data.get('T10_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T10_A2
        self.board[688] = data & 0xFF
        data = self.int_data_covert(self.data.get('T10_A3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T10_A3
        self.board[689] = data & 0xFF
        data = self.int_data_covert(self.data.get('T10_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T10_B1
        self.board[690] = data & 0xFF
        data = self.int_data_covert(self.data.get('T10_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T10_B2
        self.board[691] = data & 0xFF
        data = self.int_data_covert(self.data.get('T10_B3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T10_B3
        self.board[692] = data & 0xFF

        self.board[694] = 0xA
        data = self.int_data_covert(self.data.get('T11_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T11_A1
        self.board[695] = data & 0xFF
        data = self.int_data_covert(self.data.get('T11_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T11_A2
        self.board[696] = data & 0xFF
        data = self.int_data_covert(self.data.get('T11_A3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T11_A3
        self.board[697] = data & 0xFF
        data = self.int_data_covert(self.data.get('T11_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T11_B1
        self.board[698] = data & 0xFF
        data = self.int_data_covert(self.data.get('T11_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T11_B2
        self.board[699] = data & 0xFF
        data = self.int_data_covert(self.data.get('T11_B3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T11_B3
        self.board[700] = data & 0xFF

        self.board[702] = 0xB
        data = self.int_data_covert(self.data.get('T12_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T12_A1
        self.board[703] = data & 0xFF
        data = self.int_data_covert(self.data.get('T12_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T12_A2
        self.board[704] = data & 0xFF
        data = self.int_data_covert(self.data.get('T12_A3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T12_A3
        self.board[705] = data & 0xFF
        data = self.int_data_covert(self.data.get('T12_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T12_B1
        self.board[706] = data & 0xFF
        data = self.int_data_covert(self.data.get('T12_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T12_B2
        self.board[707] = data & 0xFF
        data = self.int_data_covert(self.data.get('T12_B3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T12_B3
        self.board[708] = data & 0xFF

        self.board[710] = 0xC
        data = self.int_data_covert(self.data.get('T13_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T13_A1
        self.board[711] = data & 0xFF
        data = self.int_data_covert(self.data.get('T13_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T13_A2
        self.board[712] = data & 0xFF
        data = self.int_data_covert(self.data.get('T13_A3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T13_A3
        self.board[713] = data & 0xFF
        data = self.int_data_covert(self.data.get('T13_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T13_B1
        self.board[714] = data & 0xFF
        data = self.int_data_covert(self.data.get('T13_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T13_B2
        self.board[715] = data & 0xFF
        data = self.int_data_covert(self.data.get('T13_B3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T13_B3
        self.board[716] = data & 0xFF

        self.board[718] = 0xD
        data = self.int_data_covert(self.data.get('T14_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T14_A1
        self.board[719] = data & 0xFF
        data = self.int_data_covert(self.data.get('T14_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T14_A2
        self.board[720] = data & 0xFF
        data = self.int_data_covert(self.data.get('T14_A3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T14_A3
        self.board[721] = data & 0xFF
        data = self.int_data_covert(self.data.get('T14_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T14_B1
        self.board[722] = data & 0xFF
        data = self.int_data_covert(self.data.get('T14_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T14_B2
        self.board[723] = data & 0xFF
        data = self.int_data_covert(self.data.get('T14_B3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T14_B3
        self.board[724] = data & 0xFF

        self.board[726] = 0xE
        data = self.int_data_covert(self.data.get('T15_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T15_A1
        self.board[727] = data & 0xFF
        data = self.int_data_covert(self.data.get('T15_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T15_A2
        self.board[728] = data & 0xFF
        data = self.int_data_covert(self.data.get('T15_A3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T15_A3
        self.board[729] = data & 0xFF
        data = self.int_data_covert(self.data.get('T15_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T15_B1
        self.board[730] = data & 0xFF
        data = self.int_data_covert(self.data.get('T15_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T15_B2
        self.board[731] = data & 0xFF
        data = self.int_data_covert(self.data.get('T15_B3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T15_B3
        self.board[732] = data & 0xFF

        self.board[734] = 0xF
        data = self.int_data_covert(self.data.get('T16_A1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T16_A1
        self.board[735] = data & 0xFF
        data = self.int_data_covert(self.data.get('T16_A2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T16_A2
        self.board[736] = data & 0xFF
        data = self.int_data_covert(self.data.get('T16_A3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T16_A3
        self.board[737] = data & 0xFF
        data = self.int_data_covert(self.data.get('T16_B1', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T16_B1
        self.board[738] = data & 0xFF
        data = self.int_data_covert(self.data.get('T16_B2', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T16_B2
        self.board[739] = data & 0xFF
        data = self.int_data_covert(self.data.get('T16_B3', '0')) + 50  # [-50, 200] 电池包电芯温度Cell_T16_B3
        self.board[740] = data & 0xFF

    def bms_274_data(self):
        """
        处理BMS_VCU_274 274数据
        742-749
        :return:
        """
        data = self.int_data_covert(self.data.get('byte0', '0'))  # byte0  [0, 3]
        self.board[742] = data & 0xFF
        data = self.int_data_covert(self.data.get('byte1', '0'))  # byte1  [0, 3]
        self.board[743] = data & 0xFF
        data = self.int_data_covert(self.data.get('byte2', '0'))  # byte2  [0, 3]
        self.board[744] = data & 0xFF
        data = self.int_data_covert(self.data.get('byte3', '0'))  # byte3  [0, 3]
        self.board[745] = data & 0xFF
        data = self.int_data_covert(self.data.get('byte4', '0'))  # byte4  [0, 3]
        self.board[746] = data & 0xFF
        data = self.int_data_covert(self.data.get('byte5', '0'))  # byte5  [0, 3]
        self.board[747] = data & 0xFF
        data = self.int_data_covert(self.data.get('byte6', '0'))  # byte6  [0, 3]
        self.board[748] = data & 0xFF
        data = self.int_data_covert(self.data.get('byte7', '0'))  # byte7  [0, 3]
        self.board[749] = data & 0xFF

    def bms_29a_data(self):
        """
        处理BMS_VCU_29A 29A数据  750-757
        :return:
        """
        self.board[997] = self.int_data_covert(self.data.get(f'bms_battery_pack_cap', 1))

        data = self.int_data_covert(
            self.data.get('bms_cell_voltg_min_validity_b', '0'))
        # BMSCellVoltgMinValidity_B [0, 1]
        self.board[751] = (self.board[751] | data & 0x01) & 0xFF

        data = self.int_data_covert(
            self.data.get('bms_cell_voltg_max_validity_b', '0'))  # BMSCellVoltgMaxValidity_B [0, 1]
        self.board[751] = (self.board[751] | ((data << 1) & 0x02))

        data = int(self.float_data_covert(self.data.get('bms_cell_voltg_max_b', '0')) * 1000)
        # bms_cell_voltage_max_b  [0, 5]
        self.board[752] = (data >> 8) & 0xFF
        self.board[753] = data & 0xFF

        data = int(self.float_data_covert(self.data.get('bms_cell_voltg_min_b', '0')) * 1000)
        # bms_cell_voltage_min_b  [0, 5]
        self.board[754] = (data >> 8) & 0xFF
        self.board[755] = data & 0xFF

        data = self.int_data_covert(self.data.get('bms_max_cell_voltg_num_b', '1')) - 1
        # bms_max_cell_voltage_num_b  [1, 256]
        self.board[756] = data & 0xFF

        data = self.int_data_covert(self.data.get('bms_min_cell_voltg_num_b', '1')) - 1
        # bms_min_cell_voltage_num_b  [1, 256]
        self.board[757] = data & 0xFF

    def bms_29b_data(self):
        """
        处理BMS_VCU_29B 29B数据  758-765
        :return:
        """
        self.board[997] = self.int_data_covert(self.data.get(f'bms_battery_pack_cap', 1))

        data = self.int_data_covert(self.data.get('bms_temp_min_validity_b', '0'))  # BMSTempMinValidity_B  [0, 1]
        self.board[759] = (self.board[759] | (data & 0x01)) & 0xff

        data = self.int_data_covert(self.data.get('bms_temp_max_validity_b', '0'))  # BMSTempMaxValidity_B  [0, 1]
        self.board[759] = (self.board[759] | ((data << 1) & 0x02)) & 0xff

        data = self.float_data_covert(self.data.get('bms_temp_max_b', '0'))  # bms_temp_max_b  [-40, 85]
        data = int((data + 40) * 2)
        self.board[760] = data & 0xFF

        data = self.float_data_covert(self.data.get('bms_temp_min_b', '0'))  # bms_temp_min_b  [-40, 85]
        data = int((data + 40) * 2)
        self.board[761] = data & 0xFF

        data = self.int_data_covert(self.data.get('bms_max_temp_num_b', '1')) - 1  # bms_max_temp_num_b  [1, 128]
        self.board[762] = data & 0xFF

        data = self.int_data_covert(self.data.get('bms_min_temp_num_b', '1')) - 1  # bms_min_temp_num_b  [1, 128]
        self.board[763] = data & 0xFF

    def bms_376_data(self):
        """
        处理BMS_CGW_376 376数据
        766-773
        :return:
        """
        data = self.int_data_covert(self.data.get('iso_ins_decrease_warning', '0'))
        self.board[768] = self.board[768] | (data & 0x07)

        data = self.int_data_covert(self.data.get('bms_full_chrg_flg', '0'))
        # Reserved18 [0, 1] bms_full_charge_state BMS满充状态
        self.board[772] = (data << 7) & 0x80

    def bms_379_data(self):
        """
        处理379数据
        774-781
        :return:
        """
        data = self.int_data_covert(self.data.get('slow_charging_lvl', '0'))
        # print("----->>>>>", data)
        self.board[774] = (data << 5) & 0xE0
        # print("----->>>>>", self.board[774])


if __name__ == '__main__':
    data = 'P0079340AF320180061300001A0test'.encode()
    list1 = [0 for _ in range(1000)]
    mem_cpy_replace(list1, data, 130)
    print(list1[130:150])
