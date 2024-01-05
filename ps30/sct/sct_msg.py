#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/9 14:31
# @Author  : wenlong.jin@nio.com
# @File    : sct_msg.py
# @Software: ps20

import SCT_pb2

from utils.log import log


class SctMsg:

    def __init__(self, data, sct):
        self.data = data
        self.sct_msg = SCT_pb2.SCT_MESSAGE()

        self.sct_msg.proto_version = 1
        self.sct_msg.device = 3
        self.sct_msg.id = sct + 1
        self.sct_msg.timestamp = 0

        self.init()

        self.sct_all_serialize = self.sct_msg.SerializeToString()
        self.sct_status_serialize = self.sct_msg.status_info.SerializeToString()

    def init(self):
        self.init_basic_info()
        self.init_status_info()
        self.init_alarm_info()
        self.init_real_info()
        self.init_event_info()
        self.init_setting_info()
        self.init_dtc_info()

    def convert(self, data, var_name, default_val):
        if var_name not in data:
            return default_val
        val = data.get(var_name)
        if default_val.__class__ == val.__class__:
            return val
        elif default_val.__class__ == float:
            try:
                return float(val)
            except ValueError:
                log.error(f"<SCT> data float convert happen error, variable name:{var_name}, val:{val}, return default")
                return default_val
        elif default_val.__class__ == str:
            return str(val)
        elif default_val.__class__ == bool:
            return False if val == "0" else True
        elif default_val.__class__ == int:
            try:
                return int(val)
            except ValueError:
                log.error(f"<SCT> data int convert happen error, variable name:{var_name}, val:{val}, return default")
                return default_val

    def init_basic_info(self):
        basic = self.data.get("basic", {})
        basic_info = SCT_pb2.SCT_BASIC_INFO_MESSAGE()
        basic_info.software_version = self.convert(basic, "software_version", "023023.1.2.3")  # //软件版本号|充电终端|SCT|||
        basic_info.bootloader_version = self.convert(basic, "bootloader_version",
                                                     "BOOT-V1.3-20220422")  # //Bootloader版本号|充电终端|SCT|||
        basic_info.hardware_version = self.convert(basic, "hardware_version",
                                                   "0.0.1b-PCB-220923")  # //硬件版本号|充电终端|SCT|||
        basic_info.qr_code = self.convert(basic, "qr_code",
                                          "68747470733a2f2f6170702e6e696f2e636f6d2f646f776e6c6f61643f71725f747970653d70652e706326736e3d503032333834343041413232393930303034584a")  # //终端二维码|充电终端|SCT|||
        basic_info.rated_power = self.convert(basic, "rated_power", 200.0)  # //额定功率|充电终端|SCT|||
        basic_info.output_power_min = self.convert(basic, "output_power_min", 0.0)  # //最小输出功率|充电终端|SCT|||
        basic_info.output_current_max = self.convert(basic, "output_current_max", 250.0)  # //最大可输出电流|充电终端|SCT|||
        basic_info.output_voltage_max = self.convert(basic, "output_voltage_max", 1000.0)  # //最高输出电压|充电终端|SCT|||
        basic_info.output_voltage_min = self.convert(basic, "output_voltage_min", 200.0)  # //最低输出电压|充电终端|SCT|||
        basic_info.cooling_type = self.convert(basic, "cooling_type", 0)  # //冷却方式 0:风冷 1:液冷（水冷、油冷）|充电终端|SCT|||
        basic_info.charge_protocol_type = self.convert(basic, "charge_protocol_type", 0)  # //充电标准 0:国标 1:欧标|充电终端|SCT|||
        basic_info.parking_lock = self.convert(basic, "parking_lock", False)  # //地锁联控 0:无地锁 1:有地锁|充电终端|SCT|||
        basic_info.ip = self.convert(basic, "ip", "192.168.8.3")  # //本地ip|充电终端|SCT|||
        basic_info.bluetooth_name = self.convert(basic, "bluetooth_name", "bt123456")  # //地锁蓝牙名称|充电终端|SCT|||
        basic_info.bluetooth_psword = self.convert(basic, "bluetooth_psword", "mm123456")  # //地锁蓝牙匹配码|充电终端|SCT|||
        basic_info.secc_version = self.convert(basic, "secc_version", "1.2.3")  # SECC版本号|充电终端|SCT|||
        self.sct_msg.basic_info.MergeFrom(basic_info)

    def init_status_info(self):
        """
        根据sct_data生成
        :return:
        """
        status = self.data.get("status", {})
        status_info = SCT_pb2.SCT_STATUS_INFO_MESSAGE()
        status_info.auxi_power_output_status = self.convert(status, "auxi_power_output_status",
                                                            0)  # //辅助电源输出状态|充电终端|SCT|0|0|1
        status_info.DC_relay_positive_state = self.convert(status, "DC_relay_positive_state",
                                                           0)  # //直流继电器正极状态|充电终端|SCT|0|0|1
        status_info.DC_relay_negative_state = self.convert(status, "DC_relay_negative_state",
                                                           0)  # //直流继电器负极状态|充电终端|SCT|0|0|1
        status_info.electromagnetic_lock_state = self.convert(status, "electromagnetic_lock_state",
                                                              0)  # //电磁锁状态|充电终端|SCT|0|0|1
        status_info.reset_button_status = self.convert(status, "reset_button_status", 0)  # //复位按钮状态|充电终端|SCT|0|0|1
        status_info.cc1_state = self.convert(status, "cc1_state", 3)  # //cc1状态|充电终端|SCT|0|0|4
        status_info.cc2_state = self.convert(status, "cc2_state", 0)  # //cc2状态|充电终端|SCT|0|0|1
        status_info.work_state = self.convert(status, "work_state", 3)  # //终端工作状态|充电终端|SCT|0|0|3
        status_info.output_relay_pstv_fb_state = self.convert(status, "output_relay_pstv_fb_state",
                                                              1)  # //输出继电器正极反馈状态|充电终端|SCT|0|0|1
        status_info.output_relay_ngtv_fb_state = self.convert(status, "output_relay_ngtv_fb_state",
                                                              1)  # //输出继电器负极反馈状态|充电终端|SCT|0|0|1
        status_info.electronic_lock_fb_state = self.convert(status, "electronic_lock_fb_state",
                                                            0)  # //电子锁反馈|充电终端|SCT|0|0|1
        status_info.bluetooth_communication_state = self.convert(status, "bluetooth_communication_state",
                                                                 0)  # //蓝牙模块通信状态|充电终端|SCT|0|0|1
        status_info.pump_work_state = self.convert(status, "pump_work_state", 0)  # //泵工作状态|充电终端|SCT|0|0|2
        status_info.liquid_level_state = self.convert(status, "liquid_level_state", 0)  # //液位状态|充电终端|SCT|0|0|2
        status_info.charge_mode = self.convert(status, "charge_mode", 0)  # //充电模式|充电终端|SCT|0|0|2
        status_info.bms_identify_result = self.convert(status, "bms_identify_result",
                                                       0)  # //BMS辨识结果|充电终端|SCT|0|0|0xFF
        status_info.charge_pile_prepare_state = self.convert(status, "charge_pile_prepare_state",
                                                             0)  # //充电机充电准备状态|充电终端|SCT|0|0|0xFF
        status_info.charge_allow_state = self.convert(status, "charge_allow_state", 0)  # //充电允许状态|充电终端|SCT|0|0|1
        status_info.pile_stop_charge_reason = self.convert(status, "pile_stop_charge_reason",
                                                           0)  # //充电机终止原因|充电终端|SCT|0|0|0xFF
        status_info.pile_fault_stop_charge_reason = self.convert(status, "pile_fault_stop_charge_reason",
                                                                 0)  # //充电机终止充电故障原因|充电终端|SCT|0|0|0xFF
        status_info.pile_error_stop_charge_reason = self.convert(status, "pile_error_stop_charge_reason",
                                                                 0)  # //充电机终止充电错误原因|充电终端|SCT|0|0|0xFF
        status_info.server_stop_reason = self.convert(status, "server_stop_reason", 0)  # //服务结束原因|充电终端|SCT|0|0|5
        status_info.bms_charge_mode = self.convert(status, "bms_charge_mode", 0)  # //BMS充电模式|充电终端|SCT|0|0|2
        status_info.bms_stop_charge_reason = self.convert(status, "bms_stop_charge_reason",
                                                          0)  # //BMS终止充电原因|充电终端|SCT|0|0|0xFF
        status_info.bms_fault_stop_charge_reason = self.convert(status, "bms_fault_stop_charge_reason",
                                                                0)  # //BMS终止充电故障原因|充电终端|SCT|0|0|0xFF
        status_info.bms_error_stop_charge_reason = self.convert(status, "bms_error_stop_charge_reason",
                                                                0)  # //BMS终止充电错误原因|充电终端|SCT|0|0|0xFF
        status_info.battery_cell_over_voltage_state = self.convert(status, "battery_cell_over_voltage_state",
                                                                   0)  # //单体过压状态|充电终端|SCT|0|0|2
        status_info.soc_state = self.convert(status, "soc_state", 0)  # //SOC状态|充电终端|SCT|0|0|2
        status_info.battery_over_current_state = self.convert(status, "battery_over_current_state",
                                                              0)  # //电池充电过流状态|充电终端|SCT|0|0|2
        status_info.battery_over_temperature_state = self.convert(status, "battery_over_temperature_state",
                                                                  0)  # //电池过温状态|充电终端|SCT|0|0|2
        status_info.battery_insulation_state = self.convert(status, "battery_insulation_state",
                                                            0)  # //电池绝缘状态|充电终端|SCT|0|0|2
        status_info.output_connector_state = self.convert(status, "output_connector_state",
                                                          0)  # //输出连接器状态|充电终端|SCT|0|0|2
        status_info.battery_allow_charge_state = self.convert(status, "battery_allow_charge_state",
                                                              0)  # //电池允许充电|充电终端|SCT|0|0|1
        status_info.battery_ready_state = self.convert(status, "battery_ready_state",
                                                       0)  # //电池充电准备就绪状态|充电终端|SCT|0x00|0x00|0xFF
        status_info.pos_communication_state = self.convert(status, "pos_communication_state",
                                                           1)  # /* pos机通讯状态|充电终端|SCT|0|0x00|1 */
        status_info.meter_communication_state = self.convert(status, "meter_communication_state",
                                                             1)  # /* 电表通讯状态|充电终端|SCT|0|0x00|1 */
        status_info.charging_state = self.convert(status, "charging_state",
                                                  5)  # /* 充电状态|充电终端|SCT|0|0x00|1 */
        status_info.fault_state = self.convert(status, "fault_state",
                                               1)  # /* 故障状态|充电终端|SCT|0|0|4 */
        status_info.charging_icc_dis_state = self.convert(status, "charging_icc_dis_state",
                                                          6)  # /* icc显示充电状态|充电终端|SCT|0|0x00|1 */
        status_info.key1_state = self.convert(status, "key1_state", 1)  # //按键1状态|充电终端|SCT|0|0|4
        status_info.key2_state = self.convert(status, "key2_state", 1)  # //按键2状态|充电终端|SCT|0|0|4
        status_info.key3_state = self.convert(status, "key3_state", 1)  # //按键3状态|充电终端|SCT|0|0|4
        status_info.gunHolder_state = self.convert(status, "gunHolder_state", 0)  # //还枪座状态|充电终端|SCT|0|0|4
        self.sct_msg.status_info.MergeFrom(status_info)

    def init_alarm_info(self):
        alarm = self.data.get("alarm", {})

    def init_real_info(self):
        """
        根据sct_data生成
        :return:
        """
        real = self.data.get("real", {})
        real_info = SCT_pb2.SCT_REALTIME_INFO_MESSAGE()
        real_info.ambient_temperature = self.convert(real, "ambient_temperature", 25)  # //终端环境温度|充电终端|SCT|-50|0|200
        real_info.control_panel_temperature = self.convert(real, "control_panel_temperature",
                                                           33)  # //终端控制板温度|充电终端|SCT|-50|0|200
        real_info.inlet_temperature = self.convert(real, "inlet_temperature", 30)  # //进液口温度|充电终端|SCT|-50|0|200
        real_info.outlet_temperature = self.convert(real, "outlet_temperature", 30)  # //出液口温度|充电终端|SCT|-50|0|200
        real_info.coolant_pressure = self.convert(real, "coolant_pressure", 3000)  # //冷却液压力|充电终端|SCT|||
        real_info.coolant_flow_rate = self.convert(real, "coolant_flow_rate", 0)  # //冷却液流速|充电终端|SCT|||
        real_info.fan_speed = self.convert(real, "fan_speed", 0)  # //散热风扇转速|充电终端|SCT|||
        real_info.output_relay_front_voltage = self.convert(real, "output_relay_front_voltage",
                                                            0.0)  # //输出继电器前端电压|充电终端|SCT|0|0|1000
        real_info.output_relay_behind_voltage = self.convert(real, "output_relay_behind_voltage",
                                                             0.0)  # //输出继电器后端电压|充电终端|SCT|0|0|1000
        real_info.output_current = self.convert(real, "output_current", 0.0)  # //输出电流|充电终端|SCT|0|0|1000
        real_info.positive_ground_resistence = self.convert(real, "positive_ground_resistence",
                                                            0)  # //正极对地电阻|充电终端|SCT|0|0|
        real_info.negative_ground_resistence = self.convert(real, "negative_ground_resistence",
                                                            0)  # //负极对地电阻|充电终端|SCT|0|0|
        real_info.add_up_energy = self.convert(real, "add_up_energy", 0.0)  # //积分电量|充电终端|SCT|0|0|1000
        real_info.output_voltage = self.convert(real, "output_voltage", 0.0)  # //输出电压|充电终端|SCT|0|0|1000
        real_info.dcem_output_current = self.convert(real, "dcem_output_current",
                                                     0.0)  # //电表输出电流|充电终端|SCT|0|0|1000
        real_info.output_energy = self.convert(real, "output_energy", 0.0)  # //输出电量|充电终端|SCT|0|0|1000
        real_info.charge_beginning_em_reading = self.convert(real, "charge_beginning_em_reading",
                                                             0.0)  # //开始充电时电表读数|充电终端|SCT|0|0|1000
        real_info.charge_ending_em_reading = self.convert(real, "charge_ending_em_reading",
                                                          0.0)  # //结束充电时电表读数|充电终端|SCT|0|0|1000
        real_info.current_em_reading = self.convert(real, "current_em_reading",
                                                    0.0)  # //电表当前读数|充电终端|SCT|0|0|1000
        real_info.current_charge_energy = self.convert(real, "current_charge_energy",
                                                       0.0)  # //当前充电电量|充电终端|SCT|0|0|1000
        real_info.pile_highest_output_voltage = self.convert(real, "pile_highest_output_voltage",
                                                             1000.0)  # //充电机最高输出电压|充电终端|SCT|0|0|1000
        real_info.pile_lowest_output_voltage = self.convert(real, "pile_lowest_output_voltage",
                                                            200.0)  # //充电机最低输出电压|充电终端|SCT|0|0|1000
        real_info.pile_highest_output_current = self.convert(real, "pile_highest_output_current",
                                                             250.0)  # //充电机最高输出电流|充电终端|SCT|0|0|1000
        real_info.pile_output_voltage = self.convert(real, "pile_output_voltage",
                                                     0.1)  # //充电机输出电压|充电终端|SCT|0|0|1000
        real_info.pile_output_current = self.convert(real, "pile_output_current",
                                                     0.1)  # //充电机输出电流|充电终端|SCT|0|0|1000
        real_info.total_charge_time = self.convert(real, "total_charge_time", 0)  # //累计充电时间|充电终端|SCT|0|0|
        real_info.pile_output_energy = self.convert(real, "pile_output_energy",
                                                    0.00001)  # //充电桩输出能量|充电终端|SCT|0|0|1000
        real_info.bms_request_voltage = self.convert(real, "bms_request_voltage",
                                                     0.0)  # //BMS请求电压|充电终端|SCT|0|0|1000
        real_info.bms_request_current = self.convert(real, "bms_request_current",
                                                     0.0)  # //BMS请求电流|充电终端|SCT|0|0|1000
        real_info.bms_current_soc = self.convert(real, "bms_current_soc", 0)  # //BMS当前SOC|充电终端|SCT|0|0|100
        real_info.bms_last_charge_time = self.convert(real, "bms_last_charge_time",
                                                      0)  # //BMS剩余充电时间|充电终端|SCT|||
        real_info.bms_allow_highest_voltage = self.convert(real, "bms_allow_highest_voltage",
                                                           0.0)  # //BMS最高允许充电总电压|充电终端|SCT|0|0|1000
        real_info.bms_protocol_version = self.convert(real, "bms_protocol_version", 0)  # //BMS协议版本号|充电终端|SCT|||
        real_info.battery_type = self.convert(real, "battery_type", 0)  # //电池类型|充电终端|SCT|0|0|255
        real_info.battery_rated_capacity = self.convert(real, "battery_rated_capacity",
                                                        0.0)  # //电池额定容量|充电终端|SCT|0|0|1000
        real_info.battery_rated_voltage = self.convert(real, "battery_rated_voltage",
                                                       0.0)  # //电池额定总电压|充电终端|SCT|0|0|1000
        real_info.battery_factory_name = self.convert(real, "battery_factory_name", "")  # //电池厂商名称|充电终端|SCT|||
        real_info.battery_produce_date = self.convert(real, "battery_produce_date",
                                                      "1985-00-00")  # //电池生产日期|充电终端|SCT|||
        real_info.battery_charge_number = self.convert(real, "battery_charge_number",
                                                       0)  # //电池已充电次数|充电终端|SCT|||
        real_info.battery_property_identification = self.convert(real, "battery_property_identification",
                                                                 0)  # //电池组产权标识|充电终端|SCT|0|0|1
        real_info.car_identification_code = self.convert(real, "car_identification_code",
                                                         "")  # //车辆识别码|充电终端|SCT|||
        real_info.bms_software_version = self.convert(real, "bms_software_version",
                                                      "")  # //bms软件版本号|充电终端|SCT|||
        real_info.cell_allow_highest_voltage = self.convert(real, "cell_allow_highest_voltage",
                                                            0.0)  # //单体最高允许电压|充电终端|SCT|0|0|1000
        real_info.allow_highest_current = self.convert(real, "allow_highest_current",
                                                       0.0)  # //最高允许充电电流|充电终端|SCT|0|0|1000
        real_info.battery_rated_energy = self.convert(real, "battery_rated_energy",
                                                      0.0)  # //动力电池额定总能量|充电终端|SCT|0|0|1000
        real_info.highest_allow_charge_voltage = self.convert(real, "highest_allow_charge_voltage",
                                                              0.0)  # //最高允许充电总电压|充电终端|SCT|0|0|1000
        real_info.highest_allow_charge_temperature = self.convert(real, "highest_allow_charge_temperature",
                                                                  0)  # //最高允许充电温度|充电终端|SCT|-50|0|200
        real_info.bms_detection_voltage = self.convert(real, "bms_detection_voltage",
                                                       0.0)  # //bms检测电压|充电终端|SCT|0|0|1000
        real_info.bms_detection_current = self.convert(real, "bms_detection_current",
                                                       0.0)  # //bms检测电流|充电终端|SCT|0|0|1000
        real_info.highest_voltage_cell_number = self.convert(real, "highest_voltage_cell_number",
                                                             0)  # //最高单体电压编号|充电终端|SCT|||
        real_info.cell_highest_temperature = self.convert(real, "cell_highest_temperature",
                                                          0)  # //单体电池最高温度|充电终端|SCT|-50|0|200
        real_info.cell_lowest_temperature = self.convert(real, "cell_lowest_temperature",
                                                         0)  # //单体电池最低温度|充电终端|SCT|-50|0|200
        real_info.lowest_temperature_cell_number = self.convert(real, "lowest_temperature_cell_number",
                                                                0)  # //最低单体温度所在编号|充电终端|SCT|||
        real_info.end_soc = self.convert(real, "end_soc", 0)  # //终止SOC|充电终端|SCT|0|0|100
        real_info.cell_lowest_voltage = self.convert(real, "cell_lowest_voltage",
                                                     0.0)  # //最低单体电压|充电终端|SCT|0|0|100
        real_info.cell_highest_voltage = self.convert(real, "cell_highest_voltage",
                                                      0.0)  # //最高单体电压|充电终端|SCT|0|0|100
        real_info.battery_lowest_temperature = self.convert(real, "battery_lowest_temperature",
                                                            0)  # //动力电池最低温度|充电终端|SCT|-50|0|200
        real_info.battery_highest_temperature = self.convert(real, "battery_highest_temperature",
                                                             0)  # //动力电池最高温度|充电终端|SCT|-50|0|200
        real_info.battery_number = self.convert(real, "battery_number", 0)  # //电池组序号|充电终端|SCT|||
        real_info.car_battery_current_voltage = self.convert(real, "car_battery_current_voltage",
                                                             0.0)  # //整车动力蓄电池当前电压|充电终端|SCT|0|0|1000
        real_info.terminal_two_dimen_code = self.convert(real, "terminal_two_dimen_code",
                                                         "68747470733a2f2f6170702e6e696f2e636f6d2f646f776e6c6f61643f71725f747970653d70652e706326736e3d503032333834343041413232393930303034584a")  # SCT 终端二维码
        real_info.gun_head_pos_temp = self.convert(real, "gun_head_pos_temp", 255)  # SCT 充电枪头正极温度
        real_info.gun_head_neg_temp = self.convert(real, "gun_head_neg_temp", 255)  # SCT 充电枪头负极温度
        real_info.gun_tail_pos_temp = self.convert(real, "gun_tail_pos_temp", 255)  # SCT 充电枪尾正极温度
        real_info.gun_tail_neg_temp = self.convert(real, "gun_tail_neg_temp", 255)  # SCT 充电枪尾负极温度
        real_info.in_copper_bar_pos_temp = self.convert(real, "in_copper_bar_pos_temp", 255)  # SCT 输入铜排正极温度

        real_info.in_copper_bar_neg_temp = self.convert(real, "in_copper_bar_neg_temp", 255)  # SCT 输入铜排负极温度
        real_info.start_request_id = self.convert(real, "start_request_id", "")  # SCT start_request_id
        real_info.stop_request_id = self.convert(real, "stop_request_id", "")  # SCT stop_request_id
        real_info.order_id = self.convert(real, "order_id", "")  # SCT order_id
        self.sct_msg.realtime_info.MergeFrom(real_info)

    def init_event_info(self):
        event = self.data.get("event", {})

    def init_setting_info(self):
        setting = self.data.get("setting", {})
        set_info = SCT_pb2.SCT_SETTINGS_INFO_MESSAGE()
        set_info.region = self.convert(setting, "region", 0)  # //使用地区|充电终端|SCT|0|0|1
        set_info.cool_type = self.convert(setting, "cool_type", 0)  # //冷却类型|充电终端|SCT|0|0|1
        set_info.resource_work_mode = self.convert(setting, "resource_work_mode", 2)  # //设备鉴权模式|充电终端|SCT|0|0|1
        set_info.charge_stop_soc = self.convert(setting, "charge_stop_soc", 100)  # //充电截至SOC|充电终端|SCT|0|0|1
        set_info.stop_charging_disconnect = self.convert(setting, "stop_charging_disconnect",
                                                         0)  # //断网后是否结束充电|充电终端|SCT|0|0|1
        set_info.stop_charg_time_disconnect = self.convert(setting, "stop_charg_time_disconnect",
                                                           600)  # //断网后停止充电的间隔时间 |充电终端|SCT|0|0|4
        set_info.gun_over_temp_alarm_val = self.convert(setting, "gun_over_temp_alarm_val",
                                                        90)  # //枪温过温告警阈值 |充电终端|SCT|0|0|3
        set_info.gun_over_temp_fault_val = self.convert(setting, "gun_over_temp_fault_val",
                                                        100)  # //枪温过温故障阈值 |充电终端|SCT|0|0|1
        set_info.gun_low_temp_alarm_val = self.convert(setting, "gun_low_temp_alarm_val",
                                                       -25)  # //枪温低温告警阈值 |充电终端|SCT|0|0|1
        set_info.gun_low_temp_fault_val = self.convert(setting, "gun_low_temp_fault_val",
                                                       -45)  # //枪温低温故障阈值 |充电终端|SCT|0|0|1
        set_info.liquid_inlet_over_temp_alarm_val = self.convert(setting, "liquid_inlet_over_temp_alarm_val",
                                                                 70)  # //进液口过温告警阈值 |充电终端|SCT|0|0|1
        set_info.liquid_inlet_over_temp_fault_val = self.convert(setting, "liquid_inlet_over_temp_fault_val",
                                                                 80)  # //进液口过温故障阈值|充电终端|SCT|0|0|2
        set_info.liquid_inlet_low_temp_alarm_val = self.convert(setting, "liquid_inlet_low_temp_alarm_val",
                                                                -25)  # //进液口低温告警阈值|充电终端|SCT|0|0|2
        set_info.liquid_inlet_low_temp_fault_val = self.convert(setting, "liquid_inlet_low_temp_fault_val",
                                                                -40)  # //进液口低温故障阈值|充电终端|SCT|0|0|2
        set_info.liquid_outlet_over_temp_alarm_val = self.convert(setting, "liquid_outlet_over_temp_alarm_val",
                                                                  50)  # //出液口过温告警阈值|充电终端|SCT|0|0|0xFF
        set_info.liquid_outlet_over_temp_fault_val = self.convert(setting, "liquid_outlet_over_temp_fault_val",
                                                                  60)  # //出液口过温故障阈值 |充电终端|SCT|0|0|0xFF
        set_info.liquid_outlet_low_temp_alarm_val = self.convert(setting, "liquid_outlet_low_temp_alarm_val",
                                                                 -25)  # //出液口低温告警阈值|充电终端|SCT|0|0|1
        set_info.liquid_outlet_low_temp_fault_val = self.convert(setting, "liquid_outlet_low_temp_fault_val",
                                                                 -40)  # //出液口低温故障阈值 |充电终端|SCT|0|0|0xFF
        set_info.positive_ground_insulation_alarm_val = self.convert(setting,
                                                                     "positive_ground_insulation_alarm_val",
                                                                     500)  # //正极对地绝缘告警阈值 |充电终端|SCT|0|0|0xFF
        set_info.positive_ground_insulation_fault_val = self.convert(setting,
                                                                     "positive_ground_insulation_fault_val",
                                                                     100)  # //正极对地绝缘故障阈值 |充电终端|SCT|0|0|0xFF
        set_info.negative_ground_insulation_alarm_val = self.convert(setting,
                                                                     "negative_ground_insulation_alarm_val",
                                                                     500)  # //负极对地绝缘告警阈值 |充电终端|SCT|0|0|5
        set_info.negative_ground_insulation_fault_val = self.convert(setting,
                                                                     "negative_ground_insulation_fault_val",
                                                                     100)  # //负极对地绝缘故障阈值|充电终端|SCT|0|0|2
        # set_info.positive_negative_insulation_alarm_val = self.convert(setting,
        #     "positive_negative_insulation_alarm_val", 0)  # //正极对负极绝缘告警阈值 |充电终端|SCT|0|0|0xFF
        # set_info.positive_negative_insulation_fault_val = self.convert(setting,
        #     "positive_negative_insulation_fault_val", 0)  # //正极对负极绝缘故障阈值|充电终端|SCT|0|0|0xFF
        set_info.dc_over_current_alarm_val = self.convert(setting, "dc_over_current_alarm_val",
                                                          5)  # //直流输出过流告警阈值 |充电终端|SCT|0|0|0xFF
        set_info.dc_over_current_fault_val = self.convert(setting, "dc_over_current_fault_val",
                                                          10)  # //直流输出过流故障阈值 |充电终端|SCT|0|0|2
        set_info.dc_over_voltage_alarm_val = self.convert(setting, "dc_over_voltage_alarm_val",
                                                          2)  # //直流输出过压告警阈值 |充电终端|SCT|0|0|2
        set_info.dc_over_voltage_fault_val = self.convert(setting, "dc_over_voltage_fault_val",
                                                          5)  # //直流输出过压故障阈值 |充电终端|SCT|0|0|2
        set_info.dc_under_voltage_alarm_val = self.convert(setting, "dc_under_voltage_alarm_val",
                                                           3)  # //直流输出欠压告警阈值|充电终端|SCT|0|0|2
        set_info.dc_under_voltage_fault_val = self.convert(setting, "dc_under_voltage_fault_val",
                                                           5)  # //直流输出欠压故障阈值|充电终端|SCT|0|0|2
        set_info.max_out_volt_val = self.convert(setting, "max_out_volt_val", 1000)  # //最高输出电压 |充电终端|SCT|0|0|2
        set_info.min_out_volt_val = self.convert(setting, "min_out_volt_val", 200)  # //最低输出电压 |充电终端|SCT|0|0|1
        set_info.max_out_current_val = self.convert(setting, "max_out_current_val",
                                                    250)  # //最大输出电流 |充电终端|SCT|0|0|0xFF
        set_info.energy_check_val = self.convert(setting, "energy_check_val",
                                                 1)  # //电量有效值校验阈值 |充电终端|SCT|0|0|0xFF
        set_info.dcem_voltage_collect_fault_val = self.convert(setting, "dcem_voltage_collect_fault_val",
                                                               5)  # //直流电表电压采集故障阈值|充电终端|SCT|0|0|0xFF
        set_info.dcem_current_collect_fault_val = self.convert(setting, "dcem_current_collect_fault_val",
                                                               10)  # //直流电表电流采集故障阈值|充电终端|SCT|0|0|0xFF
        set_info.outer_volt_insolate_val = self.convert(setting, "outer_volt_insolate_val",
                                                        100)  # //绝缘阶段外测电压保护阈值 |充电终端|SCT|0|0|0xFF
        set_info.bhm_overtimer = self.convert(setting, "bhm_overtimer", 15)  # //BHM超时时间|充电终端|SCT|0|0|0xFF
        set_info.brm_overtimer = self.convert(setting, "brm_overtimer", 5)  # //BRM超时时间|充电终端|SCT|0|0|0xFF
        set_info.bcp_overtimer = self.convert(setting, "bcp_overtimer", 5)  # //BCP超时时间 |充电终端|SCT|0|0|0xFF
        set_info.bro_overtimer = self.convert(setting, "bro_overtimer", 60)  # //BRO超时时间 |充电终端|SCT|0|0|0xFF
        set_info.bcl_overtimer = self.convert(setting, "bcl_overtimer", 1)  # //BCL超时时间 |充电终端|SCT|0|0|0xFF
        set_info.bcs_overtimer = self.convert(setting, "bcs_overtimer", 5)  # //BCS超时时间|充电终端|SCT|0|0|0xFF
        set_info.bat_cell_volt_abnormal_protect = self.convert(setting, "bat_cell_volt_abnormal_protect",
                                                               1)  # //单体电压异常保护使能|充电终端|SCT|0|0|0xFF
        set_info.bat_cell_soc_abnormal_protect = self.convert(setting, "bat_cell_soc_abnormal_protect",
                                                              1)  # //SOC异常保护使能|充电终端|SCT|0|0|0xFF
        set_info.bat_over_current_protect = self.convert(setting, "bat_over_current_protect",
                                                         1)  # //BMS电池过流保护使能|充电终端|SCT|0|0|0xFF
        set_info.bat_high_temp_protect = self.convert(setting, "bat_high_temp_protect",
                                                      1)  # //电池高温保护使能|充电终端|SCT|0|0|0xFF
        set_info.bat_insul_abnormal_protect = self.convert(setting, "bat_insul_abnormal_protect",
                                                           1)  # //电池绝缘异常保护使能|充电终端|SCT|0|0|0xFF
        set_info.bat_connect_abnormal_protect = self.convert(setting, "bat_connect_abnormal_protect",
                                                             1)  # //电池连接器异常保护使能|充电终端|SCT|0|0|0xFF
        set_info.in_pos_copper_bar_temp_alarm_val = self.convert(setting, "in_pos_copper_bar_temp_alarm_val",
                                                                 70)  # /* 输入铜排正极温度告警|充电终端|SCT|0|0|0xFF */
        set_info.in_pos_copper_bar_temp_fault_val = self.convert(setting, "in_pos_copper_bar_temp_fault_val",
                                                                 70)  # /* 输入铜排正极温度故障|充电终端|SCT|0|0|0xFF */
        set_info.in_neg_copper_bar_temp_alarm_val = self.convert(setting, "in_neg_copper_bar_temp_alarm_val",
                                                                 70)  # /* 输入铜排负极温度告警|充电终端|SCT|0|0|0xFF */
        set_info.in_neg_copper_bar_temp_fault_val = self.convert(setting, "in_neg_copper_bar_temp_fault_val",
                                                                 70)  # /* 输入铜排负极温度故障|充电终端|SCT|0|0|0xFF */
        set_info.in_air_temp_alarm_val = self.convert(setting, "in_air_temp_alarm_val",
                                                      60)  # /* 进风口环温告警阈值|充电终端|SCT|0|0|0xFF */
        set_info.in_air_temp_fault_val = self.convert(setting, "in_air_temp_fault_val",
                                                      70)  # /* 进风口环温故障阈值|充电终端|SCT|0|0|0xFF */
        set_info.gun_tail_temp_alarm_val = self.convert(setting, "gun_tail_temp_alarm_val",
                                                        70)  # /* 枪尾温度告警阈值|充电终端|SCT|0|0|0xFF */
        set_info.gun_tail_temp_fault_val = self.convert(setting, "gun_tail_temp_fault_val",
                                                        70)  # /* 枪尾温度故障阈值|充电终端|SCT|0|0|0xFF */
        set_info.hydraulic_fault_val = self.convert(setting, "hydraulic_fault_val",
                                                    8000)  # /* 液压故障阈值|充电终端|SCT|0|0|0xFF */
        set_info.hydraulic_alarm_val = self.convert(setting, "hydraulic_alarm_val",
                                                    7000)  # /* 液压告警阈值|充电终端|SCT|0|0|0xFF */
        set_info.ground_lock_bluetooth_ssid = self.convert(setting, "ground_lock_bluetooth_ssid",
                                                           "0")  # /* 地锁蓝牙ssid|充电终端|SCT|0|0|0xFF */
        set_info.ground_lock_bluetooth_match_code = self.convert(setting, "ground_lock_bluetooth_match_code",
                                                                 "0")  # /* 地锁蓝牙匹配码|充电终端|SCT|0|0|0xFF */

        self.sct_msg.settings_info.MergeFrom(set_info)

    def init_dtc_info(self):
        dtc = self.data.get("dtc", {})
