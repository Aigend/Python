# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/2/3 17:21
# @File: sct_data.py
SCT = {
    # 基本信息 16个
    "basic": {
        "software_version": "210",  # 1-1 SCT软件版本号
        "bootloader_version": "211",  # 1-1 SCT Bootloader版本号
        "hardware_version": "212",  # 1-1 SCT硬件版本号
        "qr_code": "213",  # 1-1 SCT终端二维码
        "rated_power": "214",  # 1-1 SCT额定功率
        "output_power_min": "215",  # 1-1 SCT最小输出功率
        "output_current_max": "216",  # 1-1 SCT最大可输出电流
        "output_voltage_max": "217",  # 1-1 SCT最高输出电压
        "output_voltage_min": "218",  # 1-1 SCT最低输出电压
        "cooling_type": "219",  # 1-1 SCT冷却方式 0:风冷 1:液冷（水冷、油冷）
        "charge_protocol_type": "220",  # 1-1 SCT充电标准 0:国标 1:欧标
        "parking_lock": "221",  # 1-1 SCT地锁联控 0:无地锁 1:有地锁
        "ip": "222",  # 1-1 SCT本地ip
        "bluetooth_name": "223",  # 1-1 SCT地锁蓝牙名称
        "bluetooth_psword": "224",  # 1-1 SCT地锁蓝牙匹配码
        "secc_version": ("288", 1)  # SECC版本号|充电终端|SCT||| # 这里的288代表第一个SCT的该变量的key值，1代表不同SCT该变量的key的间隔
    },

    # 实时信息 70个
    "real": {
        "ambient_temperature": "200000",  # SCT 终端环境温度
        "control_panel_temperature": "200001",  # SCT 终端控制板温度
        "inlet_temperature": "200002",  # SCT 进液口温度
        "outlet_temperature": "200003",  # SCT 出液口温度
        "coolant_pressure": "200004",  # SCT 冷却液压力
        "coolant_flow_rate": "200005",  # SCT 冷却液流速
        "fan_speed": "200006",  # SCT 散热风扇转速
        "output_relay_front_voltage": "200007",  # SCT 输出继电器前端电压
        "output_relay_behind_voltage": "200008",  # SCT 输出继电器后端电压
        "output_current": "200009",  # SCT 输出电流
        "positive_ground_resistence": "200010",  # SCT 正极对地电阻
        "negative_ground_resistence": "200011",  # SCT 负极对地电阻
        "add_up_energy": "200012",  # SCT 积分电量
        "output_voltage": "200013",  # SCT 输出电压
        "dcem_output_current": "200014",  # SCT 电表输出电流
        "output_energy": "200015",  # SCT 输出电量
        "charge_beginning_em_reading": "200016",  # SCT 开始充电时电表读数
        "charge_ending_em_reading": "200017",  # SCT 结束充电时电表读数
        "current_em_reading": "200018",  # SCT 电表当前读数
        "current_charge_energy": "200019",  # SCT 当前充电电量
        "pile_highest_output_voltage": "200020",  # SCT 充电机最高输出电压
        "pile_lowest_output_voltage": "200021",  # SCT 充电机最低输出电压
        "pile_highest_output_current": "200022",  # SCT 充电机最高输出电流
        "pile_output_voltage": "200023",  # SCT 充电机输出电压
        "pile_output_current": "200024",  # SCT 充电机输出电流
        "total_charge_time": "200025",  # SCT 累计充电时间
        "pile_output_energy": "200026",  # SCT 充电桩输出功率
        "bms_request_voltage": "200027",  # SCT-bms请求电压
        "bms_request_current": "200028",  # SCT-bms请求电流
        "bms_current_soc": "200029",  # SCT-bms当前SOC
        "bms_last_charge_time": "200030",  # SCT-bms剩余充电时间
        "bms_allow_highest_voltage": "200031",  # SCT-bms最高允许充电总电压
        "bms_protocol_version": "200032",  # SCT-bms协议版本号
        "battery_type": "200033",  # SCT-bms电池类型
        "battery_rated_capacity": "200034",  # SCT-bms电池额定容量
        "battery_rated_voltage": "200035",  # SCT-bms电池额定总电压
        "battery_factory_name": "200036",  # SCT-bms电池厂商名称
        "battery_produce_date": "200037",  # SCT-bms电池生产日期
        "battery_charge_number": "200038",  # SCT-bms电池已充电次数
        "battery_property_identification": "200039",  # SCT-bms电池组产权标识
        "car_identification_code": "200040",  # SCT 车辆识别码
        "bms_software_version": "200041",  # SCT-bms软件版本号
        "cell_allow_highest_voltage": "200042",  # SCT 单体最高允许电压
        "allow_highest_current": "200043",  # SCT 最高允许充电电流
        "battery_rated_energy": "200044",  # SCT 动力电池额定总能量
        "highest_allow_charge_voltage": "200045",  # SCT 最高允许充电总电压
        "highest_allow_charge_temperature": "200046",  # SCT 最高允许充电温度
        "bms_detection_voltage": "200047",  # SCT-bms检测电压
        "bms_detection_current": "200048",  # SCT-bms检测电流
        "highest_voltage_cell_number": "200049",  # SCT-bms最高单体电压编号
        "cell_highest_temperature": "200050",  # SCT-bms单体电池最高温度
        "cell_lowest_temperature": "200051",  # SCT-bms单体电池最低温度
        "lowest_temperature_cell_number": "200052",  # SCT-bms最低单体温度所在编号
        "end_soc": "200053",  # SCT 终止SOC
        "cell_lowest_voltage": "200054",  # SCT-bms最低单体电压
        "cell_highest_voltage": "200055",  # SCT-bms最高单体电压
        "battery_lowest_temperature": "200056",  # SCT-bms动力电池最低温度
        "battery_highest_temperature": "200057",  # SCT-bms动力电池最高温度
        "battery_number": "200058",  # SCT-bms电池组序号
        "car_battery_current_voltage": "200059",  # SCT-bms整车动力蓄电池当前电压
        "terminal_two_dimen_code": "200060",  # SCT 终端二维码
        "gun_head_pos_temp": "200061",  # SCT 充电枪头正极温度
        "gun_head_neg_temp": "200062",  # SCT 充电枪头负极温度
        "gun_tail_pos_temp": "200063",  # SCT 充电枪尾正极温度
        "gun_tail_neg_temp": "200064",  # SCT 充电枪尾负极温度
        "in_copper_bar_pos_temp": "200065",  # SCT 输入铜排正极温度
        "in_copper_bar_neg_temp": "200066",  # SCT 输入铜排负极温度
        "start_request_id": "200067",  # SCT start_request_id
        "stop_request_id": "200068",  # SCT stop_request_id
        "order_id": "200069",  # SCT order_id
    },

    # 状态信息 43个
    "status": {
        "auxi_power_output_status": "200640",  # /* 辅助电源输出状态|充电终端|SCT|0|0|1 */
        "DC_relay_positive_state": "200641",  # /* 直流继电器正极状态|充电终端|SCT|0|0|1 */
        "DC_relay_negative_state": "200642",  # /* 直流继电器负极状态|充电终端|SCT|0|0|1 */
        "electromagnetic_lock_state": "200643",  # /* 电磁锁状态|充电终端|SCT|0|0|1 */
        "reset_button_status": "200644",  # /* 复位按钮状态|充电终端|SCT|0|0|1 */
        "cc1_state": "200645",  # /* cc1状态|充电终端|SCT|0|0|4 */
        "cc2_state": "200646",  # /* cc2状态|充电终端|SCT|0|0|1 */
        "work_state": "200647",  # /* 终端工作状态|充电终端|SCT|0|0|3 */
        "output_relay_pstv_fb_state": "200648",  # /* 输出继电器正极反馈状态|充电终端|SCT|0|0|1 */
        "output_relay_ngtv_fb_state": "200649",  # /* 输出继电器负极反馈状态|充电终端|SCT|0|0|1 */
        "electronic_lock_fb_state": "200650",  # /* 电子锁反馈|充电终端|SCT|0|0|1 */
        "bluetooth_communication_state": "200651",  # /* 蓝牙模块通信状态|充电终端|SCT|0|0|1 */
        "pump_work_state": "200652",  # /* 泵工作状态|充电终端|SCT|0|0|2 */
        "liquid_level_state": "200653",  # /* 液位状态|充电终端|SCT|0|0|2 */
        "charge_mode": "200654",  # /* 充电模式|充电终端|SCT|0|0|2 */
        "bms_identify_result": "200655",  # /* BMS辨识结果|充电终端|SCT|0|0|0xFF */
        "charge_pile_prepare_state": "200656",  # /* 充电机充电准备状态|充电终端|SCT|0|0|0xFF */
        "charge_allow_state": "200657",  # /* 充电允许状态|充电终端|SCT|0|0|1 */
        "pile_stop_charge_reason": "200658",  # /* 充电机终止原因|充电终端|SCT|0|0|0xFF */
        "pile_fault_stop_charge_reason": "200659",  # /* 充电机终止充电故障原因|充电终端|SCT|0|0|0xFF */
        "pile_error_stop_charge_reason": "200660",  # /* 充电机终止充电错误原因|充电终端|SCT|0|0|0xFF */
        "server_stop_reason": "200661",  # /* 服务结束原因|充电终端|SCT|0|0|5 */
        "bms_charge_mode": "200662",  # /* BMS充电模式|充电终端|SCT|0|0|2 */
        "bms_stop_charge_reason": "200663",  # /* BMS终止充电原因|充电终端|SCT|0|0|0xFF */
        "bms_fault_stop_charge_reason": "200664",  # /* BMS终止充电故障原因|充电终端|SCT|0|0|0xFF */
        "bms_error_stop_charge_reason": "200665",  # /* BMS终止充电错误原因|充电终端|SCT|0|0|0xFF */
        "battery_cell_over_voltage_state": "200666",  # /* 单体过压状态|充电终端|SCT|0|0|2 */
        "soc_state": "200667",  # /* SOC状态|充电终端|SCT|0|0|2 */
        "battery_over_current_state": "200668",  # /* 电池充电过流状态|充电终端|SCT|0|0|2 */
        "battery_over_temperature_state": "200669",  # /* 电池过温状态|充电终端|SCT|0|0|2 */
        "battery_insulation_state": "200670",  # /* 电池绝缘状态|充电终端|SCT|0|0|2 */
        "output_connector_state": "200671",  # /* 输出连接器状态|充电终端|SCT|0|0|2 */
        "battery_allow_charge_state": "200672",  # /* 电池允许充电|充电终端|SCT|0|0|1 */
        "battery_ready_state": "200673",  # /* 电池充电准备就绪状态|充电终端|SCT|0|0x00|1 */
        "pos_communication_state": "200674",  # /* pos机通讯状态|充电终端|SCT|0|0x00|1 */
        "meter_communication_state": "200675",  # /* 电表通讯状态|充电终端|SCT|0|0x00|1 */
        "charging_state": "200676",  # /* 充电状态|充电终端|SCT|0|0x00|1 */
        "fault_state": "200677",  # /* 故障状态|充电终端|SCT|0|0|4 */
        "charging_icc_dis_state": "200678",  # /* icc显示充电状态|充电终端|SCT|0|0x00|1 */
        "key1_state": "",  # /* 按键1状态|充电终端|SCT|0|0|4 */
        "key2_state": "",  # /* 按键2状态|充电终端|SCT|0|0|4 */
        "key3_state": "",  # /* 按键3状态|充电终端|SCT|0|0|4 */
        "gunHolder_state": ""  # 还枪座状态|充电终端|SCT|0|0|4
    },

    # 报警信息
    "alarm": {
        "positive_pole_output_relay_adhered": "760001",  # 输出继电器正极粘连
        "positive_pole_output_relay_moved_misses": "760002",  # 输出继电器正极拒动
        "negative_pole_output_relay_adhered": "760003",  # 输出继电器负极粘连
        "negative_pole_output_relay_moved_misses": "760004",  # 输出继电器负极拒动
        "cc1_voltage_fault": "760005",  # CC1电压故障
        "auxiliary_power_voltage_fault": "760006",  # 辅助电源电压故障
        "elec_locked_fault": "760007",  # 电子锁上锁失败
        "elec_unlocked_fault": "760008",  # 电子锁解锁失败
        "charging_gun_over_temp_fault": "760009",  # 枪温过温故障
        "charging_gun_over_temp_alarm": "760010",  # 枪温过温告警
        "charging_gun_temp_collected_fault": "760011",  # 枪温采集异常
        "liquid_inlet_over_temp_fault": "760012",  # 进液口过温故障
        "liquid_inlet_over_temp_alarm": "760013",  # 进液口过温告警
        "liquid_inlet_coll_temp_alarm": "760014",  # 进液口温度采集异常
        "liquid_outlet_over_temp_fault": "760015",  # 出液口过温故障
        "liquid_outlet_over_temp_alarm": "760016",  # 出液口过温告警
        "liquid_outlet_coll_temp_alarm": "760017",  # 出液口温度采集异常
        "pump_idle_fault": "760018",  # 油泵转速故障
        "fan1_speed_fault": "760019",  # 1#风机转速故障
        "fan2_speed_fault": "760020",  # 2#风机转速故障
        "pump_over_pressure_fault": "760021",  # 泵出口压力高故障
        "pressure_sensor_fault": "760022",  # 压力传感器故障
        "flow_switch_fault": "760023",  # 流量开关故障
        "liquid_level_low_alarm": "760024",  # 液位低告警
        "insulation_module_commu_fault": "760025",  # 绝缘检测通信故障
        "positive_ground_insulation_alarm": "760026",  # 正极对地绝缘告警
        "positive_ground_insulation_fault": "760027",  # 正极对地绝缘故障
        "negative_ground_insulation_alarm": "760028",  # 负极对地绝缘告警
        "negative_ground_insulation_fault": "760029",  # 负极对地绝缘故障
        "output_voltage_collected_alarm": "760030",  # 输出电压采集告警
        "output_current_collected_alarm": "760031",  # 输出电流采集告警
        "insulation_check_timeout": "760032",  # 绝缘检测超时故障
        "insulation_voltage_over_set": "760033",  # 绝缘检测电压高于设定故障
        "insulation_voltage_under_set": "760034",  # 绝缘检测电压低于设定故障
        "dcem_communication_fault": "760035",  # 直流电表通信告警
        "dcem_voltage_collected_alarm": "760036",  # 直流电表电压采集告警
        "dcem_current_collected_alarm": "760037",  # 直流电表电流采集告警
        "dcem_engey_error": "760038",  # 直流电表电量异常
        "bluetooth_communication_alarm": "760039",  # 蓝牙模块通信告警
        "bluetooth_parking_lock_commu_fault": "760040",  # 蓝牙地锁通信故障
        "bluetooth_parking_locked_fail": "760041",  # 蓝牙地锁上锁失败
        "bluetooth_parking_unlocked_fail": "760042",  # 蓝牙地锁解锁失败
        "card_commu_alarm": "760043",  # 读卡器通信告警
        "card_read_alarm": "760044",  # 读卡器读卡失败告警
        "dc_over_voltage_alarm": "760045",  # 直流输出过压告警
        "dc_over_voltage_fault": "760046",  # 直流输出过压故障
        "dc_under_voltage_fault": "760047",  # 直流输出欠压故障
        "dc_over_current_alarm": "760048",  # 直流输出过流告警
        "dc_over_current_fault": "760049",  # 直流输出过流故障
        "outside_contactor_voltage_over_threshold": "760050",  # 输出继电器外侧电压大于阈值故障
        "bms_voltage_over_output_range": "760051",  # 电池电压超过输出范围故障
        "bms_req_voltage_over_output_range": "760052",  # 电池需求电压超出充电机输出范围故障
        "bms_req_voltage_under_output_range": "760053",  # 电池需求电压低于充电机输出范围故障
        "bms_voltage_not_match_bcp": "760054",  # 电池电压与通信报文不匹配告警
        "prepare_voltage_not_match": "760055",  # 预充电压不匹配故障
        "bms_req_current_over_output_current": "760056",  # 需求电流高于最高允许充电电流告警
        "battery_soc_abnormal": "760057",  # BMS车辆电池soc异常告警
        "battery_over_current": "760058",  # 车辆电池充电过流告警
        "battery_temp_high": "760059",  # 车辆电池温度过高告警
        "battery_insulation_fault": "760060",  # 车辆电池绝缘异常告警
        "battery_cell_voltage_alarm": "760061",  # 车辆单体电池电压告警
        "battery_connector_alarm": "760062",  # 车辆蓄电池连接器告警
        "bms_high_voltage_relay_alarm": "760063",  # BMS检测高压继电器故障
        "bms_cc2_alarm": "760064",  # BMS检测CC2故障
        "bms_other_alarm": "760065",  # BMS其他故障
        "bms_over_current": "760066",  # BMS检测电流过流
        "bms_voltage_fault": "760067",  # BMS检测电压异常
        "none_bhm_brm_overtime": "760068",  # 未收到BHM，BRM超时
        "with_bhm_brm_overtime": "760069",  # 收到BHM，BRM超时
        "sct_get_bcp_overtime": "760070",  # 接收BCP超时
        "sct_get_bro_overtime": "760071",  # 接收BRO超时
        "sct_get_bcl_overtime": "760072",  # 接收BCL超时
        "sct_get_bcs_overtime": "760073",  # 接收BCS超时
        "bms_get_crm_overtime": "760074",  # BMS接收CRM超时
        "bms_get_cro_overtime": "760075",  # BMS接收CRO超时
        "bms_get_cml_overtime": "760076",  # BMS接收CML超时
        "bms_get_ccs_overtime": "760077",  # BMS接收CCS超时
        "bms_get_cst_overtime": "760078",  # BMS接收CST超时
        "bms_get_csd_overtime": "760079",  # BMS接收CSD超时
        "bms_communication_fault": "760080",  # BMS通信故障
        "pcu_output_over_voltage": "760081",  # SCT PCU输出电压过压
        "pcu_output_under_voltage": "760082",  # SCT PCU输出电压欠压
        "pcu_output_current_fault": "760083",  # SCT PCU输出电流异常
        "sct_get_bst_stop_cmd": "",  # SCT BST中止充电
        "sct_get_bsm_stop_cmd": "",  # SCT BSM中止充电
        "pcu_state_fault_stop": "760084",  # SCT PCU状态故障
        "pcu_ctrl_fault_stop": "760085",  # SCT PCU控制故障
        "pcu_commu_fault_stop": "760086",  # SCT PCU通讯故障
        "mqtt_commu_fault": "760087",  # SCT mqtt通讯故障
        "none_current_output_current": "760088",  # SCT 无电流3分钟停机
        "cd_over_bcp_fault": "760089",  # SCT 输出电压大于等于BCP最高电压
        "in_copper_pos_alarm": "760090",  # SCT 输入铜排正极温度告警
        "in_copper_pos_fault": "760091",  # SCT 输入铜排正极温度故障
        "in_copper_pos_erro": "760092",  # SCT 输入铜排正极温度采集错误
        "in_copper_neg_alarm": "760093",  # SCT 输入铜排负极温度告警
        "in_copper_neg_fault": "760094",  # SCT 输入铜排负极温度故障
        "in_copper_neg_erro": "760095",  # SCT 输入铜排负极温度采集错误
        "in_air_temp_alarm": "760096",  # SCT 进风口环温告警
        "in_air_temp_fault": "760097",  # SCT 进风口环温故障
        "in_air_temp_erro": "760098",  # SCT 进风口环温错误
        "charg_tail_gun_over_temp_fault": "760099",  # SCT 枪尾温度告警
        "charg_tail_gun_over_temp_alarm": "760100",  # SCT 枪尾温度故障
        "charg_tail_gun_temp_collected_fault": "760101",  # SCT 枪尾温度采集错误
        "coolant_pressure_fault": "760102",  # SCT 液压故障
        "coolant_pressure_alarm": "760103",  # SCT 液压告警
        "coolant_pressure_erro": "760104",  # SCT 液压采集异常
        "dc_outside_volt_over_10v": "760105",  # SCT DC外侧高于10V故障
        "light_commun_fault": "760106",  # SCT 灯板通讯故障
        "bms_soc_over_range": "",  # SCT soc大于100故障
    },

    # 事件信息
    "event": {
        "command_id": "",  # char command_id[51]; /* 命令id||||| */
        "gun_id": "",  # char gun_id[257]; /* 枪id||||| */
        "gun_session": "",  # char gun_session[51]; /* 插枪session||||| */
        "service_status": "",  # int32_t service_status; /* 服务状态||||| */
        "start_power_meter": "",  # int32_t start_power_meter; /* 电表起始电量||||| */
        "charg_capacity": "",  # int32_t charg_capacity; /* 当前充电电量||||| */
        "charg_integral_quantity": "",  # int32_t charg_integral_quantity; /* 当前充电积分电量||||| */
        "quantity_electricity_meter": "",  # int32_t quantity_electricity_meter; /* 电表当前电量||||| */
        "initial_soc": "",  # int32_t initial_soc; /* 起始SOC||||| */
        "current_soc": "",  # int32_t current_soc; /* 当前SOC||||| */
        "vin_code": "",  # char vin_code[18]; /* 车辆VIN码||||| */
        "service_end_reason": "",  # char service_end_reason[51]; /* 服务结束原因||||| */
        "encrypt_meter_data": "",  # char encrypt_meter_data[51]; /* 加密电表数据||||| */
        "get_vin_state": "",  # int32_t get_vin_state; /* vin码获取状态||||| */
        "random": "",  # char random[17]; /* random||||| */
        "brand_id": "",  # char brand_id[9]; /* brand_id||||| */
        "hmac": "",  # char hmac[33]; /* hmac||||| */
        "sub_id": "",  # char sub_id[17]; /* sub_id||||| */
        "get_secret_state": "",  # int32_t get_secret_state; /* 加密获取状态||||| */
        "card_uid": "",  # char card_uid[64]; /* sub_id||||| */
        "stop_err_code": "",  # 停机故障码|||||
    },

    # 配置信息
    "setting": {
        "region": "902500",  # /* 使用地区|充电终端|SCT|0|0|1 */
        "cool_type": "902501",  # /* 冷却类型|充电终端|SCT|0|0|1 */
        "resource_work_mode": "902502",  # /* 设备鉴权模式|充电终端|SCT|0|0|1 */
        "charge_stop_soc": "902503",  # /* 充电截至SOC|充电终端|SCT|0|0|1 */
        "stop_charging_disconnect": "902504",  # /* 断网后是否结束充电|充电终端|SCT|0|0|1 */
        "stop_charg_time_disconnect": "902505",  # /* 断网后停止充电的间隔时间 |充电终端|SCT|0|0|4 */
        "gun_over_temp_alarm_val": "902506",  # /* 枪温过温告警阈值 |充电终端|SCT|0|0|3 */
        "gun_over_temp_fault_val": "902507",  # /* 枪温过温故障阈值 |充电终端|SCT|0|0|1 */
        "gun_low_temp_alarm_val": "902508",  # /* 枪温低温告警阈值 |充电终端|SCT|0|0|1 */
        "gun_low_temp_fault_val": "902509",  # /* 枪温低温故障阈值 |充电终端|SCT|0|0|1 */
        "liquid_inlet_over_temp_alarm_val": "902510",  # /* 进液口过温告警阈值 |充电终端|SCT|0|0|1 */
        "liquid_inlet_over_temp_fault_val": "902511",  # /* 进液口过温故障阈值|充电终端|SCT|0|0|2 */
        "liquid_inlet_low_temp_alarm_val": "902512",  # /* 进液口低温告警阈值|充电终端|SCT|0|0|2 */
        "liquid_inlet_low_temp_fault_val": "902513",  # /* 进液口低温故障阈值|充电终端|SCT|0|0|2 */
        "liquid_outlet_over_temp_alarm_val": "902514",  # /* 出液口过温告警阈值|充电终端|SCT|0|0|0xFF */
        "liquid_outlet_over_temp_fault_val": "902515",  # /* 出液口过温故障阈值 |充电终端|SCT|0|0|0xFF */
        "liquid_outlet_low_temp_alarm_val": "902516",  # /* 出液口低温告警阈值|充电终端|SCT|0|0|1 */
        "liquid_outlet_low_temp_fault_val": "902517",  # /* 出液口低温故障阈值 |充电终端|SCT|0|0|0xFF */
        "positive_ground_insulation_alarm_val": "902518",  # /* 正极对地绝缘告警阈值 |充电终端|SCT|0|0|0xFF */
        "positive_ground_insulation_fault_val": "902519",  # /* 正极对地绝缘故障阈值 |充电终端|SCT|0|0|0xFF */
        "negative_ground_insulation_alarm_val": "902520",  # /* 负极对地绝缘告警阈值 |充电终端|SCT|0|0|5 */
        "negative_ground_insulation_fault_val": "902521",  # /* 负极对地绝缘故障阈值|充电终端|SCT|0|0|2 */
        "dc_over_current_alarm_val": "902522",  # /* 直流输出过流告警阈值 |充电终端|SCT|0|0|0xFF */
        "dc_over_current_fault_val": "902523",  # /* 直流输出过流故障阈值 |充电终端|SCT|0|0|2 */
        "dc_over_voltage_alarm_val": "902524",  # /* 直流输出过压告警阈值 |充电终端|SCT|0|0|2 */
        "dc_over_voltage_fault_val": "902525",  # /* 直流输出过压故障阈值 |充电终端|SCT|0|0|2 */
        "dc_under_voltage_alarm_val": "902526",  # /* 直流输出欠压告警阈值|充电终端|SCT|0|0|2 */
        "dc_under_voltage_fault_val": "902527",  # /* 直流输出欠压故障阈值|充电终端|SCT|0|0|2 */
        "max_out_volt_val": "902528",  # /* 最高输出电压 |充电终端|SCT|0|0|2 */
        "min_out_volt_val": "902529",  # /* 最低输出电压 |充电终端|SCT|0|0|1 */
        "max_out_current_val": "902530",  # /* 最大输出电流 |充电终端|SCT|0|0|0xFF */
        "energy_check_val": "902531",  # /* 电量有效值校验阈值 |充电终端|SCT|0|0|0xFF */
        "dcem_voltage_collect_fault_val": "902532",  # /* 直流电表电压采集故障阈值|充电终端|SCT|0|0|0xFF */
        "dcem_current_collect_fault_val": "902533",  # /* 直流电表电流采集故障阈值|充电终端|SCT|0|0|0xFF */
        "outer_volt_insolate_val": "902534",  # /* 绝缘阶段外测电压保护阈值 |充电终端|SCT|0|0|0xFF */
        "bhm_overtimer": "902535",  # /* BHM超时时间|充电终端|SCT|0|0|0xFF */
        "brm_overtimer": "902536",  # /* BRM超时时间|充电终端|SCT|0|0|0xFF */
        "bcp_overtimer": "902537",  # /* BCP超时时间 |充电终端|SCT|0|0|0xFF */
        "bro_overtimer": "902538",  # /* BRO超时时间 |充电终端|SCT|0|0|0xFF */
        "bcl_overtimer": "902539",  # /* BCL超时时间 |充电终端|SCT|0|0|0xFF */
        "bcs_overtimer": "902540",  # /* BCS超时时间|充电终端|SCT|0|0|0xFF */
        "bat_cell_volt_abnormal_protect": "902541",  # /* 单体电压异常保护使能|充电终端|SCT|0|0|0xFF */
        "bat_cell_soc_abnormal_protect": "902542",  # /* SOC异常保护使能|充电终端|SCT|0|0|0xFF */
        "bat_over_current_protect": "902543",  # /* BMS电池过流保护使能|充电终端|SCT|0|0|0xFF */
        "bat_high_temp_protect": "902544",  # /* 电池高温保护使能|充电终端|SCT|0|0|0xFF */
        "bat_insul_abnormal_protect": "902545",  # /* 电池绝缘异常保护使能|充电终端|SCT|0|0|0xFF */
        "bat_connect_abnormal_protect": "902546",  # /* 电池连接器异常保护使能|充电终端|SCT|0|0|0xFF */
        "in_pos_copper_bar_temp_alarm_val": "902549",  # /* 输入铜排正极温度告警|充电终端|SCT|0|0|0xFF */
        "in_pos_copper_bar_temp_fault_val": "902550",  # /* 输入铜排正极温度故障|充电终端|SCT|0|0|0xFF */
        "in_neg_copper_bar_temp_alarm_val": "902551",  # /* 输入铜排负极温度告警|充电终端|SCT|0|0|0xFF */
        "in_neg_copper_bar_temp_fault_val": "902552",  # /* 输入铜排负极温度故障|充电终端|SCT|0|0|0xFF */
        "in_air_temp_alarm_val": "902553",  # /* 进风口环温告警阈值|充电终端|SCT|0|0|0xFF */
        "in_air_temp_fault_val": "902554",  # /* 进风口环温故障阈值|充电终端|SCT|0|0|0xFF */
        "gun_tail_temp_alarm_val": "902555",  # /* 枪尾温度告警阈值|充电终端|SCT|0|0|0xFF */
        "gun_tail_temp_fault_val": "902556",  # /* 枪尾温度故障阈值|充电终端|SCT|0|0|0xFF */
        "hydraulic_fault_val": "902557",  # /* 液压故障阈值|充电终端|SCT|0|0|0xFF */
        "hydraulic_alarm_val": "902558",  # /* 液压告警阈值|充电终端|SCT|0|0|0xFF */
        "ground_lock_bluetooth_ssid": "902547",  # /* 地锁蓝牙ssid|充电终端|SCT|0|0|0xFF */
        "ground_lock_bluetooth_match_code": "902548",  # /* 地锁蓝牙匹配码|充电终端|SCT|0|0|0xFF */
    },

    # 诊断信息
    "dtc": {
        "type": "",  # int32_t type; /* 诊断信息类型 */
        "message": "",  # char message[21]; /* 诊断 */
    }
}


def change_sct_key_to_var(sct_node, data):
    """
    :param sct_node:0-3
    :param data:
    :return:
    """
    result = {'basic': {},
              'real': {},
              'alarm': {},
              'status': {},
              'setting': {}}
    _add = {
        'basic': sct_node * 15,  # 基本数据通信点表key值每支路sct间隔15:210, 225, ......
        'real': sct_node * 80,  # 实时数据通信点表key值每支路sct间隔80:200000, 200080, ......
        'alarm': sct_node * 500,  # 报警数据通信点表key值每支路sct间隔500:760001, 760501, ......
        'status': sct_node * 40,  # 状态数据通信点表key值每支路sct间隔40:200640, 200680, ......
        'setting': sct_node * 100,  # 配置数据通信点表key值每支路sct间隔100:902500, 902600, ......
        # 'event': sct_node * 5,  # 事件数据通信点表key值每支路sct间隔10:102000, 102010, ......
        # 'dtc': sct_node * 5,  # dtc数据通信点表key值每支路sct间隔10:102000, 102010, ......
    }
    for info, res in result.items():
        add = _add[info]
        if info not in SCT:
            continue
        for var_name, k_value in SCT[info].items():
            if isinstance(k_value, str) and k_value.isnumeric() and str(int(k_value) + add) in data:
                result[info][var_name] = data.get(str(int(k_value) + add))
            elif isinstance(k_value, tuple):  # 部分数据点在点表中排序不规则，做了特殊处理
                tmp = int(k_value[1]) * sct_node
                k = str(int(k_value[0]) + tmp)
                if k in data:
                    result[info][var_name] = data.get(k)
    # log.debug(f"<SCT>:发送的数据转换后的结果:{result}")
    return result
