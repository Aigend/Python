# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/10/8 16:50
# @File:bms_utils.py
import copy
import re
from utils.log import log

bms_map_key = {
    # BMS AF
    "bms_contactor_states": "1521",  # // bms_cntctr_sts
    "bms_sts": "1515",  # 电池状态
    "bms_abort_cls_reason": "1533",  # 5XX619 //bms_abort_cls_reason BMS退出预充原因
    "bms_inhibit_cls_reason": "1534",  # 5XX620 //bms_inhibit_cls_reason BMS禁止预充原因

    # BMS AC
    "bms_pack_crrnt": "1021",  # BMS电池包总电流
    "bms_pack_voltage": "1020",  # BMS电池包总电压
    "bms_fault_lvl": ("1501", "740014"),  # BMS故障等级
    "bms_soc": "1023",  # BMS 实际SOC
    "bms_customer_usage_soc": "1022",  # BMS 用户SOC
    "bms_charge_available": ("1503", "740017"),  # //电池可充电标志
    "bms_ac_test_status": "1509",  # //AC测试状态
    "hv_batt_soc_low_warn": "",
    "bms_check_sum_ac": "",

    # BMS AD
    "bms_dischg_crrnt_limit": "",
    "bms_voltage_limit_max": '1010',  # BMS电池包最高允许总电压
    "bms_balance_sts": "1510",  # //均衡状态
    "bms_inter_lock_sts": ("1511", "740031"),  # //高压互锁标志
    "bms_voltage_limit_min": '1011',  # BMS电池包最低允许总电压
    "bms_isolation_lvl": ("1502", "740015"),  # BMS绝缘等级
    "bms_alm_clk_sts": "",
    "bms_dc_chrg_derate_crrnt_sts": "1519",  # // BMS直流充电减额电流状态
    "bms_charge_state": "1508",  # //BMS充电状态
    "bms_fault_cat": "1530",  # 故障等级位掩码 [0,255], 1

    # BMS AE
    "bms_if_bms_soc_set": "1516",  # //SOC 达到目标值
    "bms_if_pack_voltage_set": "1517",  # //达到总电压目标值
    "bms_if_cell_voltage_set": "1518",  # //达到单体电压目标值
    "bms_hv_isolation": '740001',  # BMS绝缘故障
    "bms_connector_over_temp": '740002',  # BMS高压继电器过温故障
    "bms_chrg_conn_over_temp": '740003',  # BMS充电连接器过温故障
    "bms_chrg_conn_error": '740004',  # BMS充电连接器故障
    "bms_pack_over_temp": '740005',  # BMS电池包温度过高故障
    "bms_hv_conector_error": '740006',  # BMS高压继电器故障
    "bms_other_error": '740007',  # BMS其他故障
    "bms_over_current": '740008',  # BMS过流故障
    "bms_voltg_mismatch": '740009',  # BMS电压不匹配
    "maximum_permit_charge_cell_volt": '1017',  # BMS单体最高允许充电电压
    "bms_high_resl_soc": "1041",  # BMS 高实际SOC [0, 102.3] 0.1 //BMS高分辨率SOC
    "bms_cel_slf_dchrg_sts": "1526",  # BMS单体自放电状态 [0, 3] fact=1
    "bms_pack_iso_dec_sts": "1525",  # BMS电池包绝缘下降状态 [0, 3] fact =1
    "bms_inhibit_chrg_flt": '740027',  # BMS 禁止充电告警

    # BMS 267
    "bms_dc_chrg_current_req": "1026",  # BMSDCChrgCrntReq 电池充电请求电流 [-2000, 4553.5] factor=0.1
    "bms_dc_chrg_voltage_req": "1025",  # BMSDCChrgVoltgReq 电池充电请求电压 [0, 600] factor=0.1
    "bms_chrg_current_limit": "1027",  # BMSChgCrrntLimit 电池充电限流值 [-2000, 0] factot=0.1
    "bms_pack_energy_available": "1028",  # BMSPackEnergyAvailable 电池可用电量 [0, 100] factor=0.1
    "bms_dc_chrg_mode": "1512",  # 直流充电模式
    "bms_req_wakeup_obcm": "",
    "bms_pack_therm_out_of_ctrl_vld": "1524",  # BMS电池包热失控故障有效性 [0, 1] fact=1
    "bms_pack_therm_out_of_ctrl_alrm": '740028',  # BMS 热管理失控告警

    # BMS 268
    "bms_dischrg_power_limit_st": "1046",  # BMSDischrgPowerLimitST 电池短时放电功率限值 [0, 1000] 0.1
    "bms_dischrg_power_limit_lt": "1045",  # BMSDischrgPowerLimitLT 电池长时放电功率限值 [0, 1000] 0.1
    "bms_dischrg_power_limit_dynamic": "1044",  # BMSDischrgPowerLimitDynamic 电池动态放电功率限值 [0, 1000] 0.1
    "bms_insolation_resistance_value": "1029",  # BMSInsulationResistanceValue 电池绝缘电阻值 [0, 65535] factor=1

    # BMS 269
    "bms_cell_voltg_max": "1032",  # BMSCellVoltgMax 电池最高单体电压 [0, 5] factor=0.001
    "bms_cell_voltg_min": "1034",  # BMSCellVoltgMin 电池最低单体电压 [0, 5] 0.001
    "bms_estimate_chrg_time": "1030",  # BMSEstimateChrgTime 电池预估剩余充电时间 [0, 1440] factor=1
    "bms_cell_voltg_average": "1035",  # BMSCellVoltgAverage 电池平均单体电压 [0, 5] 0.001
    "bms_cell_voltg_average_validity": "",  # //平均单体电压有效标识:  0-valid; 1-invalid
    "bms_cell_voltg_max_validity": "",  # 最大单体电压有效标识
    "bms_cell_voltg_min_validity": "",  # 最小单体电压有效标识

    # BMS 26A
    "bms_chrg_power_limit_st": "1049",  # BMSChrgPowerLimitST 电池短时充电功率极值 [0, 1000] 0.1
    "bms_chrg_power_limit_lt": "1048",  # BMSChrgPowerLimitLT 电池长时充电功率极值 [0, 1000] 0.1
    "bms_chrg_power_limit_dynamic": "1047",  # BMSChrgPowerLimitDynamic 电池动态充电功率限值 [0， 1000] 0.1

    # BMS 26F
    "bms_protocal_version": '1002',  # 协议版本
    "bms_battery_type": "1008",  # //BMS电池类型 点表描述为电芯类型
    "bms_max_permit_dc_charge_voltage": '1015',  # BMS最大允许直流充电电压
    "bms_battery_rated_capacity": '1006',  # 电池额定容量
    "bms_battery_pack_cap": '1012',  # 电芯类型 //点表描述为电池类型

    # BMS 270
    "bms_battery_rated_voltage": '1009',  # 电池额定电压
    "bms_ready_dc_charging": "1506",  # //直流充电就绪状态
    "bms_dc_charging_volt_measure": "",  # //充电电压测量值: Resolution-0.1; 0~1000V; offset: 0;
    "bms_dc_charging_curr_measure": "",  # //充电电流测量值: Resolution-0.1; -400~0V; offset: -400;

    # BMS 271
    "bms_maximum_cell_voltage_number": "1031",  # BMSMaximumCellVoltageNumber 电池最高单体电压单体编号 [1, 256], factor=1
    "bms_maximum_cell_temp": "1036",  # BMSMaximumCellTemp 电池最高电芯温度 [-50, 200] 1
    "bms_maximum_temp_number": "1039",  # BMSMaximumTempNumber 电池最高电芯温度编号 [1, 128] 1
    "bms_minimum_cell_temp": "1037",  # BMSMinimumCellTemp 电池最低电芯温度 [-50, 200] 1
    "bms_minimum_temp_number": "1040",  # BMSMinimumTempNumber 电池最低电芯温度编号 [1, 128] 1
    "bms_dc_chrg_final_soc": '1016',  # BMS充电截止SOC

    # BMS 272
    "bms_cell_voltage_over_under": ('740010', '740011'),
    # 1XX046 BMS电池单体电压过高 '1XX047',  # BMS电池单体电压过低 # //单体电压过高过低: 0x00:正常  0x01:过高 0x10:过低
    "bms_soc_over_under": "1513",  # //SOC 当前可用状态//SOC过高过低
    "bms_dc_chrg_curr_over": '740016',  # BMS 电流过大//充电电流过流
    "battery_temp_over": '740012',  # 1XX048 BMS电池包温度过高  # //蓄电池温度过高状态
    "battery_output_connector_state": "1507",  # //输出电连接器状态
    "dc_charging_permit_status": ("1505", "740030"),  # //允许充电状态
    "battery_abnormal_alarm4": "740035",
    "battery_abnormal_alarm3": "740034",
    "battery_abnormal_alarm2": "740033",
    "battery_abnormal_alarm1": "740032",
    "egy_storg_err8": "",
    "egy_storg_err7": "",
    "egy_storg_err6": "",
    "egy_storg_err5": "",
    "egy_storg_err4": "",
    "egy_storg_err3": "",
    "egy_storg_err2": "",
    "egy_storg_err1": "",
    "soc_jump_alarm": "",
    "battery_type_dismatch_alarm": '740018',  # BMS 电池类型不匹配告警
    "battery_consistency_alarm": '740019',  # BMS 电池一致性告警
    "battery_temp_differ_alarm": '740020',  # BMS 电池温差过大告警
    "battery_pck_volt_over_alarm": '740021',  # BMS 电池包过压告警
    "battery_pck_volt_under_alarm": '740022',  # BMS 电池包限压告警
    "battery_cell_vol_high_alarm": '740023',  # BMS 电池单体电压过高告警
    "battery_cell_vol_low_alarm": '740024',  # BMS 电池单体电压过低告警
    "battery_cell_temp_high_alarm": '740025',  # BMS 电池单体温度过高告警
    "battery_cell_temp_low_alarm": '740026',  # BMS 电池单体温度过低告警
    "soc_jump_reason": "1514",  # SOC 跳跃原因
    "battery_soc_high_alarm": "",
    "battery_over_temp_alarm": "",
    "bms_hv_isolation_alarm": "",

    # BMS 273
    "bms_minimum_cell_voltage_number": "1033",  # BMSMinimumCellVoltageNumber 电池最低单体电压单体编号 [1, 256] 1
    "bms_max_voltage_subsys_number": "",
    "bms_min_voltage_subsys_number": "",
    "bms_max_temp_subsys_number": "",
    "bms_min_temp_subsys_number": "",

    # BMS 372
    "maximum_charging_current": '1014',  # C1# BMS最大充电电流
    "battery_normal_capacity": '1007',  # 电池标称总能量
    "maximum_charging_voltage": '1013',  # BMS最大充电电压
    "maximum_permit_temp": '1018',  # BMS最高允许温度

    # BMS 373
    "bms_temp_max": "1036",  # BMS最高电芯温度
    "bms_temp_min": "1037",  # BMS最低电芯温度
    "bms_temp_average": "1038",  # BMSTempAverage 电池平均电芯温度 [-40, 85] 0.5
    "bms_ess_inlet_temp": "1042",  # BMSESSInletTemp 电池包入水口温度 [-40, 85] 0.125
    "bms_temp_max_validity": "",
    "bms_temp_min_validity": "",
    "bms_hv_shutdown_req": ("1504", '740029'),  # //高压下电请求
    "bms_temp_average_validity": "",
    "bms_ess_inlet_temp_validity": "",
    "bms_ess_inlet_temp_mask": "",
    "bms_ess_outlet_temp": "1043",  # BMSESSOutletTemp 电池包出水口温度 [-40, 85] 0.125
    "bms_ess_outlet_temp_validity": "",
    "bms_ess_outlet_temp_mask": "",
    "bms_cell_tar_temp_mode_req_A": "1528",  # BMS单体目标温度请求方式 [0, 3] fact=1
    "reflash_req": "1520",  # //BMS重新刷新请求
    "bms_over_dc_chrg_protect": "1531",  # BMS直流过充保护告警
    "bms_cell_tar_temp": "1532",  # 5XX613 BMS单体目标温度 [-20, 43.5] fact=0.5
    "bms_cell_tar_temp_validity": "1527",  # 5XX612 BMS单体目标温度有效性 [0, 1] fact=1

    # BMS 29A
    "bms_cell_voltg_min_validity_b": "",
    "bms_cell_voltg_max_validity_b": "",
    "bms_cell_voltg_max_b": "1051",  # bms_cell_voltage_max_b  [0, 5] 0.001 BMS最高电池单体电压_B
    "bms_cell_voltg_min_b": "1053",  # bms_cell_voltage_min_b  [0, 5] 0.001 BMS最低电池单体电压_B
    "bms_max_cell_voltg_num_b": "1050",  # bms_max_cell_voltage_num_b  [1, 256] 1 BMS最高电池单体电压单体编号_B
    "bms_min_cell_voltg_num_b": "1052",  # bms_min_cell_voltage_num_b  [1, 256] 1 BMS最低电池单体电压单体编号_B

    # BMS 29B
    "bms_temp_min_validity_b": "",
    "bms_temp_max_validity_b": "",
    "bms_temp_max_b": "1054",  # bms_temp_max_b  [-40, 85] 0.5 BMS最高电芯温度_B
    "bms_temp_min_b": "1055",  # bms_temp_min_b  [-40, 85] 0.5 BMS最低电芯温度_B
    "bms_max_temp_num_b": "1056",  # bms_max_temp_num_b  [1, 128] 1 BMS最高电芯温度编号_B
    "bms_min_temp_num_b": "1057",  # bms_min_temp_num_b  [1, 128] 1 BMS最低电芯温度编号_B

    # BMS 274
    "byte0": "1346",  # BMS 电池包0X274帧第1字节
    "byte1": "1347",  # BMS 电池包0X274帧第1字节
    "byte2": "1348",  # BMS 电池包0X274帧第1字节
    "byte3": "1349",  # BMS 电池包0X274帧第1字节
    "byte4": "1350",  # BMS 电池包0X274帧第1字节
    "byte5": "1351",  # BMS 电池包0X274帧第1字节
    "byte6": "1352",  # BMS 电池包0X274帧第1字节
    "byte7": "1353",  # BMS 电池包0X274帧第1字节

    # "": "##",  # 电池预留
    # "#": "**",  # 电池黑名单

    # BMS 376
    "iso_ins_decrease_warning": "1529",  # C1# BMS绝缘下降告警来源
    "bms_full_chrg_flg": '1522',  # //BMS满充状态

    # BMS 379
    "slow_charging_lvl": "1535",  # BMS慢充保养状态 正确性

    # BMS 68C
    "battery_pack_id": '1001',  # 蔚来ID
    "gb_battery_pack_id": '1005',  # 国标ID
    "bms_software_ver": '1003',  # 软件版本
    "bms_hardware_ver": '1004',  # 硬件版本

    # 101
    "bms_lock_state": '1523',  # //BMS电池锁状态 待修改，前端包含，但目前进程中未配置

    # CDC 定义变量
    "bms_pack_under_temp": '740013',  # BMS电池包温度过低, 开发代码固定写死为0
    "bms_pack_power": "1019",
    "bms_soh": "1024",  # 代码固定为100

    # BMS 26C 电池单体电压数据
    "N1": "1058",
    "N2": "1059",
    "N3": "1060",
    "N4": "1061",
    "N5": "1062",
    "N6": "1063",
    "N7": "1064",
    "N8": "1065",
    "N9": "1066",
    "N10": "1067",
    "N11": "1068",
    "N12": "1069",
    "N13": "1070",
    "N14": "1071",
    "N15": "1072",
    "N16": "1073",
    "N17": "1074",
    "N18": "1075",
    "N19": "1076",
    "N20": "1077",
    "N21": "1078",
    "N22": "1079",
    "N23": "1080",
    "N24": "1081",
    "N25": "1082",
    "N26": "1083",
    "N27": "1084",
    "N28": "1085",
    "N29": "1086",
    "N30": "1087",
    "N31": "1088",
    "N32": "1089",
    "N33": "1090",
    "N34": "1091",
    "N35": "1092",
    "N36": "1093",
    "N37": "1094",
    "N38": "1095",
    "N39": "1096",
    "N40": "1097",
    "N41": "1098",
    "N42": "1099",
    "N43": "1100",
    "N44": "1101",
    "N45": "1102",
    "N46": "1103",
    "N47": "1104",
    "N48": "1105",
    "N49": "1106",
    "N50": "1107",
    "N51": "1108",
    "N52": "1109",
    "N53": "1110",
    "N54": "1111",
    "N55": "1112",
    "N56": "1113",
    "N57": "1114",
    "N58": "1115",
    "N59": "1116",
    "N60": "1117",
    "N61": "1118",
    "N62": "1119",
    "N63": "1120",
    "N64": "1121",
    "N65": "1122",
    "N66": "1123",
    "N67": "1124",
    "N68": "1125",
    "N69": "1126",
    "N70": "1127",
    "N71": "1128",
    "N72": "1129",
    "N73": "1130",
    "N74": "1131",
    "N75": "1132",
    "N76": "1133",
    "N77": "1134",
    "N78": "1135",
    "N79": "1136",
    "N80": "1137",
    "N81": "1138",
    "N82": "1139",
    "N83": "1140",
    "N84": "1141",
    "N85": "1142",
    "N86": "1143",
    "N87": "1144",
    "N88": "1145",
    "N89": "1146",
    "N90": "1147",
    "N91": "1148",
    "N92": "1149",
    "N93": "1150",
    "N94": "1151",
    "N95": "1152",
    "N96": "1153",
    "N97": "1154",
    "N98": "1155",
    "N99": "1156",
    "N100": "1157",
    "N101": "1158",
    "N102": "1159",
    "N103": "1160",
    "N104": "1161",
    "N105": "1162",
    "N106": "1163",
    "N107": "1164",
    "N108": "1165",
    "N109": "1166",
    "N110": "1167",
    "N111": "1168",
    "N112": "1169",
    "N113": "1170",
    "N114": "1171",
    "N115": "1172",
    "N116": "1173",
    "N117": "1174",
    "N118": "1175",
    "N119": "1176",
    "N120": "1177",
    "N121": "1178",
    "N122": "1179",
    "N123": "1180",
    "N124": "1181",
    "N125": "1182",
    "N126": "1183",
    "N127": "1184",
    "N128": "1185",
    "N129": "1186",
    "N130": "1187",
    "N131": "1188",
    "N132": "1189",
    "N133": "1190",
    "N134": "1191",
    "N135": "1192",
    "N136": "1193",
    "N137": "1194",
    "N138": "1195",
    "N139": "1196",
    "N140": "1197",
    "N141": "1198",
    "N142": "1199",
    "N143": "1200",
    "N144": "1201",
    "N145": "1202",
    "N146": "1203",
    "N147": "1204",
    "N148": "1205",
    "N149": "1206",
    "N150": "1207",
    "N151": "1208",
    "N152": "1209",
    "N153": "1210",
    "N154": "1211",
    "N155": "1212",
    "N156": "1213",
    "N157": "1214",
    "N158": "1215",
    "N159": "1216",
    "N160": "1217",
    "N161": "1218",
    "N162": "1219",
    "N163": "1220",
    "N164": "1221",
    "N165": "1222",
    "N166": "1223",
    "N167": "1224",
    "N168": "1225",
    "N169": "1226",
    "N170": "1227",
    "N171": "1228",
    "N172": "1229",
    "N173": "1230",
    "N174": "1231",
    "N175": "1232",
    "N176": "1233",
    "N177": "1234",
    "N178": "1235",
    "N179": "1236",
    "N180": "1237",
    "N181": "1238",
    "N182": "1239",
    "N183": "1240",
    "N184": "1241",
    "N185": "1242",
    "N186": "1243",
    "N187": "1244",
    "N188": "1245",
    "N189": "1246",
    "N190": "1247",
    "N191": "1248",
    "N192": "1249",
    # 电池单体温度数据
    "CAP_102AH": {
        "T1_A1": '1250',
        "T1_A2": '1251',
        "T1_B1": '1252',
        "T1_B2": '1253',
        "T2_A1": '1254',
        "T2_A2": '1255',
        "T2_B1": '1256',
        "T2_B2": '1257',
        "T3_A1": '1258',
        "T3_A2": '1259',
        "T3_B1": '1260',
        "T3_B2": '1261',
        "T4_A1": '1262',
        "T4_A2": '1263',
        "T4_B1": '1264',
        "T4_B2": '1265',
        "T5_A1": '1266',
        "T5_A2": '1267',
        "T5_B1": '1268',
        "T5_B2": '1269',
        "T6_A1": '1270',
        "T6_A2": '1271',
        "T6_B1": '1272',
        "T6_B2": '1273',
        "T7_A1": '1274',
        "T7_A2": '1275',
        "T7_B1": '1276',
        "T7_B2": '1277',
        "T8_A1": '1278',
        "T8_A2": '1279',
        "T8_B1": '1280',
        "T8_B2": '1281',
        "T9_A1": '1282',
        "T9_A2": '1283',
        "T9_B1": '1284',
        "T9_B2": '1285',
        "T10_A1": '1286',
        "T10_A2": '1287',
        "T10_B1": '1288',
        "T10_B2": '1289',
        "T11_A1": '1290',
        "T11_A2": '1291',
        "T11_B1": '1292',
        "T11_B2": '1293',
        "T12_A1": '1294',
        "T12_A2": '1295',
        "T12_B1": '1296',
        "T12_B2": '1297',
        "T13_A1": '1298',
        "T13_A2": '1299',
        "T13_B1": '1300',
        "T13_B2": '1301',
        "T14_A1": '1302',
        "T14_A2": '1303',
        "T14_B1": '1304',
        "T14_B2": '1305',
        "T15_A1": '1306',
        "T15_A2": '1307',
        "T15_B1": '1308',
        "T15_B2": '1309',
        "T16_A1": '1310',
        "T16_A2": '1311',
        "T16_B1": '1312',
        "T16_B2": '1313',
    },  # 16*4
    # "CAP_50AH": {},  # 暂时没有
    "CAP_120AH": {
        "T1_A1": '1250',
        "T1_A2": '1251',
        "T1_A3": '1252',
        "T1_B1": '1253',
        "T1_B2": '1254',
        "T1_B3": '1255',
        "T2_A1": '1256',
        "T2_A2": '1257',
        "T2_A3": '1258',
        "T2_B1": '1259',
        "T2_B2": '1260',
        "T2_B3": '1261',
        "T3_A1": '1262',
        "T3_A2": '1263',
        "T3_A3": '1264',
        "T3_B1": '1265',
        "T3_B2": '1266',
        "T3_B3": '1267',
        "T4_A1": '1268',
        "T4_A2": '1269',
        "T4_A3": '1270',
        "T4_B1": '1271',
        "T4_B2": '1272',
        "T4_B3": '1273',
        "T5_A1": '1274',
        "T5_A2": '1275',
        "T5_A3": '1276',
        "T5_B1": '1277',
        "T5_B2": '1278',
        "T5_B3": '1279',
        "T6_A1": '1280',
        "T6_A2": '1281',
        "T6_A3": '1282',
        "T6_B1": '1283',
        "T6_B2": '1284',
        "T6_B3": '1285',
        "T7_A1": '1286',
        "T7_A2": '1287',
        "T7_A3": '1288',
        "T7_B1": '1289',
        "T7_B2": '1290',
        "T7_B3": '1291',
        "T8_A1": '1292',
        "T8_A2": '1293',
        "T8_A3": '1294',
        "T8_B1": '1295',
        "T8_B2": '1296',
        "T8_B3": '1297',
        "T9_A1": '1298',
        "T9_A2": '1299',
        "T9_A3": '1300',
        "T9_B1": '1301',
        "T9_B2": '1302',
        "T9_B3": '1303',
        "T10_A1": '1304',
        "T10_A2": '1305',
        "T10_A3": '1306',
        "T10_B1": '1307',
        "T10_B2": '1308',
        "T10_B3": '1309',
        "T11_A1": '1310',
        "T11_A2": '1311',
        "T11_A3": '1312',
        "T11_B1": '1313',
        "T11_B2": '1314',
        "T11_B3": '1315',
        "T12_A1": '1316',
        "T12_A2": '1317',
        "T12_A3": '1318',
        "T12_B1": '1319',
        "T12_B2": '1320',
        "T12_B3": '1321',
        "T13_A1": '1322',
        "T13_A2": '1323',
        "T13_A3": '1324',
        "T13_B1": '1325',
        "T13_B2": '1326',
        "T13_B3": '1327',
        "T14_A1": '1328',
        "T14_A2": '1329',
        "T14_A3": '1330',
        "T14_B1": '1331',
        "T14_B2": '1332',
        "T14_B3": '1333',
        "T15_A1": '1334',
        "T15_A2": '1335',
        "T15_A3": '1336',
        "T15_B1": '1337',
        "T15_B2": '1338',
        "T15_B3": '1339',
        "T16_A1": '1340',
        "T16_A2": '1341',
        "T16_A3": '1342',
        "T16_B1": '1343',
        "T16_B2": '1344',
        "T16_B3": '1345',
    },  # 16*6
    "CAP_280AH": {
        "T1_A1": '1250',
        "T1_A2": '1251',
        "T1_B1": '1252',
        "T1_B2": '1253',
        "T2_A1": '1254',
        "T2_A2": '1255',
        "T2_B1": '1256',
        "T2_B2": '1257',
        "T3_A1": '1258',
        "T3_A2": '1259',
        "T3_B1": '1260',
        "T3_B2": '1261',
        "T4_A1": '1262',
        "T4_A2": '1263',
        "T4_B1": '1264',
        "T4_B2": '1265',
        "T5_A1": '1266',
        "T5_A2": '1267',
        "T5_B1": '1268',
        "T5_B2": '1269',
        "T6_A1": '1270',
        "T6_A2": '1271',
        "T6_B1": '1272',
        "T6_B2": '1273',
        "T7_A1": '1274',
        "T7_A2": '1275',
        "T7_B1": '1276',
        "T7_B2": '1277',
        "T8_A1": '1278',
        "T8_A2": '1279',
        "T8_B1": '1280',
        "T8_B2": '1281',
        "T9_A1": '1282',
        "T9_A2": '1283',
        "T9_B1": '1284',
        "T9_B2": '1285',
        "T10_A1": '1286',
        "T10_A2": '1287',
        "T10_B1": '1288',
        "T10_B2": '1289',
        "T11_A1": '1290',
        "T11_A2": '1291',
        "T11_B1": '1292',
        "T11_B2": '1293',
        "T12_A1": '1294',
        "T12_A2": '1295',
        "T12_B1": '1296',
        "T12_B2": '1297',
    },  # 12*4
    "CAP_75KWH": {
        "T1_A1": '1250',
        "T1_A2": '1251',
        "T1_A3": '1252',
        "T1_B1": '1253',
        "T1_B2": '1254',
        "T1_B3": '1255',
        "T2_A1": '1256',
        "T2_A2": '1257',
        "T2_A3": '1258',
        "T2_B1": '1259',
        "T2_B2": '1260',
        "T2_B3": '1261',
        "T3_A1": '1262',
        "T3_A2": '1263',
        "T3_A3": '1264',
        "T3_B1": '1265',
        "T3_B2": '1266',
        "T3_B3": '1267',
        "T4_A1": '1268',
        "T4_A2": '1269',
        "T4_A3": '1270',
        "T4_B1": '1271',
        "T4_B2": '1272',
        "T4_B3": '1273',
        "T5_A1": '1274',
        "T5_A2": '1275',
        "T5_A3": '1276',
        "T5_B1": '1277',
        "T5_B2": '1278',
        "T5_B3": '1279',
        "T6_A1": '1280',
        "T6_A2": '1281',
        "T6_A3": '1282',
        "T6_B1": '1283',
        "T6_B2": '1284',
        "T6_B3": '1285',
        "T7_A1": '1286',
        "T7_A2": '1287',
        "T7_A3": '1288',
        "T7_B1": '1289',
        "T7_B2": '1290',
        "T7_B3": '1291',
        "T8_A1": '1292',
        "T8_A2": '1293',
        "T8_A3": '1294',
        "T8_B1": '1295',
        "T8_B2": '1296',
        "T8_B3": '1297',
    },  # 8*6
}


def bms_convert_key_to_var(bms_node, data):
    """
        0，P50 50Ah；#50度电池，已经去掉了
        1，P70 102Ah；#70度电池
        2，P84；#84度电池，已淘汰
        3，P70 102Ah X；#70度电池，材料差异
        4，P84锁电；84度锁成70度，换电调度
        5，P70 LFP； 70度，材料不同，现在未使用
        6，P100 NCM； 100度电池，NCM材料
        7，P100 锁电70；100度锁70
        8，P75；75度
        9，P100 锁电84；已淘汰
        10，P150；现在没有
        11，P100 锁电75；当75度使用
        12～16，预留
    :param bms_node:
    :param data:
    :return:
    """
    result = {}
    brn = re.search("bms(\d+)", bms_node).group(1)
    info = str(int(brn) + 1)  # 1-21
    # print("info", info)
    temp = int(brn) * 4  # 00-80, 每隔4个
    alarm = f"74{temp}" if temp > 9 else f"740{temp}"
    # print("alarm", alarm)
    battery_type = int(data.get(f"{info}012", 6))  # 1012
    # print("battery_type", str(battery_type))
    bms_key = copy.deepcopy(bms_map_key)
    if battery_type in [6, 7, 9, 11, 13, 14]:
        temp = bms_key.get("CAP_280AH", {})   # 前端 100度电池
        bms_key.update(temp)
    elif battery_type in [1, 3]:
        temp = bms_key.get("CAP_102AH", {})  # 前端 70度电池
        bms_key.update(temp)
    elif battery_type in [2, 4]:
        temp = bms_key.get("CAP_120AH", {})
        bms_key.update(temp)
    elif battery_type in [0, ]:
        temp = bms_key.get("CAP_50AH", {})
        bms_key.update(temp)
    elif battery_type in [8, ]:
        temp = bms_key.get("CAP_75KWH", {})  # 前端 75度电池
        bms_key.update(temp)
    for var_name, k_value in bms_key.items():
        if isinstance(k_value, str) and 3 < len(k_value) < 6:
            k = info + k_value[-3:]
            if k in data:
                result[var_name] = data.get(k, '0')
        elif isinstance(k_value, str) and len(k_value) == 6:
            k = alarm + k_value[-2:]
            if k in data:
                result[var_name] = data.get(k, '0')
        elif isinstance(k_value, str) and len(k_value) == 0:
            if var_name in data:
                result[var_name] = data.get(var_name, '0')
        elif isinstance(k_value, tuple):  # 多个key会给同一个变量赋值的情况
            for k_val in k_value:
                if isinstance(k_val, str) and 3 < len(k_val) < 6:
                    if info + k_val[-3:] in data:
                        result[var_name] = data.get(info + k_val[-3:])
                elif isinstance(k_val, str) and len(k_val) == 6:
                    if alarm + k_val[-2:] in data:
                        result[var_name] = data.get(alarm + k_val[-2:])
    return result


if __name__ == '__main__':
    a = {3: '1'}
    if int(float(a.get(3))):
        print("##")
