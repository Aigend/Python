#!/usr/bin/env python
# coding=utf-8
import random
import string
import time
from datetime import date
from nio_messages import wti, pb2
from nio_messages.can_data import CAN_DATA
from nio_messages.pb2.alarm_data_pb2 import AlarmData
from nio_messages.pb2.driving_behaviour_msg_pb2 import DrivingBehaviourEvent
from nio_messages.pb2.heating_status_pb2 import HeatingStatus
from nio_messages.pb2.light_status_pb2 import LightStatus
from nio_messages.pb2.nbs_status_pb2 import NBSStatus
from nio_messages.pb2.soc_status_pb2 import SOCStatus
from nio_messages.pb2.position_status_pb2 import PositionStatus
from nio_messages.pb2.vehicle_status_pb2 import VehicleStatus
from nio_messages.pb2.door_status_pb2 import DoorStatus
from nio_messages.pb2.hvac_status_pb2 import HVACStatus
from nio_messages.pb2.window_status_pb2 import WindowStatus
from nio_messages.pb2.driving_data_pb2 import DrivingData
from nio_messages.pb2.extremum_data_pb2 import ExtremumData
from nio_messages.pb2.bms_status_pb2 import BmsStatus
from nio_messages.pb2.tyre_status_pb2 import TyreStatus
from nio_messages.pb2.can_msg_pb2 import CanMsg
from nio_messages.pb2.occupant_status_pb2 import OccupantStatus
from nio_messages.pb2.driving_motor_pb2 import DrivingMotor
from nio_messages.pb2.alarm_signal_pb2 import AlarmSignal
from nio_messages.pb2.signal_status_pb2 import SignalStatus
from nio_messages.pb2.connection_status_message_pb2 import ConnectionStatusMsg
from nio_messages.pb2.adas_header_pb2 import AdasHeader
from nio_messages.pb2.feature_status_pb2 import FeatureStatus
from nio_messages.pb2.low_soc_range_pb2 import LowSocRange
from nio_messages.pb2.body_status_pb2 import BodyStatus
from nio_messages.pb2.trip_status_pb2 import TripStatus
from nio_messages.pb2.gd_system_information_msg_pb2 import GDSystemInformationEvent
from nio_messages.pb2.gd_event_report_msg_pb2 import GDEventReportEvent
from nio_messages.pb2.power_swap_pb2 import PowerSwapEvent, PowerSwapPeriodic
from nio_messages.pb2.cdm_app_upload_pb2 import UploadInfo
from nio_messages.pb2.dlb_flow_warn_pb2 import FlowInfo, EventFlowInfo
from nio_messages.pb2.sa_cellular_status_msg_pb2 import SACellularStatus
from nio_messages.pb2.can_signal_pb2 import CanSignal
from nio_messages.pb2.high_frequency_msg_pb2 import HighFreData


def gen_soc_status(data=None):
    if data is None:
        data = {}
    soc_status = SOCStatus()
    soc_status.soc = data.get('soc', random.randint(0, 200) * 0.5)
    soc_status.chrg_state = data.get('chrg_state', random.choice([0, 1, 2, 3]))
    soc_status.btry_cap = data.get('btry_cap', random.randint(0, 10000) * 0.1)
    soc_status.remaining_range = data.get('remaining_range', round(random.randint(0, 2000) * 0.5))  # 范围:[0:1000]
    soc_status.hivolt_btry_curnt = data.get('hivolt_btry_curnt', random.randint(-20000, 20000) * 0.1)
    soc_status.chrg_final_soc = data.get('chrg_final_soc', random.randint(0, 100))
    soc_status.max_soc = data.get('max_soc', random.randint(50, 100))
    soc_status.lock_soc = data.get('lock_soc', random.randint(0, 50))
    soc_status.soc_lock_status = data.get('soc_lock_status', random.choice([0, 1]))
    soc_status.soc_v2l_status = data.get('soc_v2l_status', random.randint(0, 7))

    if 'btry_paks' not in data:
        btry_paks = soc_status.btry_paks.add()
        btry_paks.btry_pak_sn = 1
        btry_paks.btry_pak_hist_temp = random.randint(-80, 170) * 0.5
        btry_paks.btry_pak_lwst_temp = random.randint(-80, 170) * 0.5
        btry_paks.btry_pak_voltage = random.randint(0, 6000) * 0.1
        btry_paks.btry_pak_curnt = random.randint(-20000, 20000) * 0.1
        btry_paks.sin_btry_qunty_of_pak = 3
        btry_paks.frm_start_btry_sn = 1
        btry_paks.sin_btry_qunty_of_frm = 3
        btry_paks.sin_btry_voltage.extend([10, 20, 30])
        btry_paks.temp_prb_qunty = btry_paks.sin_btry_qunty_of_pak
        btry_paks.prb_temp_lst.extend([10, 20, 30])
        btry_paks.sin_btry_voltage_inv.extend([1, 2])
        btry_paks.prb_temp_lst_inv.extend([1, 2])

    else:
        for i, item in enumerate(data['btry_paks']):
            btry_paks = soc_status.btry_paks.add()
            btry_paks.btry_pak_sn = item.get('btry_pak_sn', i + 1)  # 电池包序列号
            btry_paks.btry_pak_hist_temp = item.get('btry_pak_hist_temp', random.randint(-80, 170) * 0.5)  # 电池包最高温度值
            btry_paks.btry_pak_lwst_temp = item.get('btry_pak_lwst_temp', random.randint(-80, 170) * 0.5)  # 电池包最低温度值
            btry_paks.btry_pak_voltage = item.get('btry_pak_voltage', random.randint(0, 6000) * 0.1)  # 可充电储能装置电压
            btry_paks.btry_pak_curnt = item.get('btry_pak_curnt', random.randint(-20000, 20000) * 0.1)  # 可充电储能装置电流
            btry_paks.sin_btry_qunty_of_pak = item.get('sin_btry_qunty_of_pak', 3)  # 单体电池总数，实车应为192
            btry_paks.frm_start_btry_sn = item.get('frm_start_btry_sn', i + 1)  # 本帧起始电池序号
            btry_paks.sin_btry_qunty_of_frm = item.get('sin_btry_qunty_of_frm', 3)  # 本帧单体电池总数，实车应为192
            btry_paks.sin_btry_voltage.extend(item.get('sin_btry_voltage', [10, 20, 30]))  # 单体电池电压（0V～60V），实车应有192个
            btry_paks.temp_prb_qunty = item.get('temp_prb_qunty', btry_paks.sin_btry_qunty_of_pak)  # 温度探针个数，实车应为64
            btry_paks.prb_temp_lst.extend(item.get('prb_temp_lst', [10, 20, 30]))  # 探针温度列表（偏置40度，即温度为当前数字加40），实车应有64个
            btry_paks.sin_btry_voltage_inv.extend(item.get('sin_btry_voltage_inv', [1, 2]))  # 在一个BMS电压采样周期内没有检测到温度的探针序号
            btry_paks.prb_temp_lst_inv.extend(item.get('prb_temp_lst_inv', [1, 2]))  # 在一个BMS温度采样周期内没有检测到温度的探针序号

    soc_status.dump_enrgy = data.get('dump_enrgy', random.randint(0, 1000) * 0.1)
    soc_status.sin_btry_hist_temp = data.get('sin_btry_hist_temp', random.randint(-50, 200))
    soc_status.sin_btry_lwst_temp = data.get('sin_btry_lwst_temp', random.randint(-50, 200))
    soc_status.btry_qual_actvtn = data.get('btry_qual_actvtn', random.choice([True, False]))
    soc_status.realtime_power_consumption = data.get('realtime_power_consumption', random.randint(-300, 700))

    return soc_status


def gen_charging_info(data=None):
    if data is None:
        data = {}
    charging_info = SOCStatus.ChargingInfo()
    charging_info.charger_type = data.get('charger_type', random.choice([0, 1, 2, 3, 4, 5]))
    charging_info.estimate_chrg_time = data.get('estimate_chrg_time', random.randint(0, 1440))
    charging_info.in_volt_ac = data.get('in_volt_ac', round(random.uniform(0, 400), 1))  # 充电交流输入电压
    charging_info.in_volt_dc = data.get('in_volt_dc', round(random.uniform(0, 600), 2))  # 充电直流输入电压
    charging_info.in_curnt_ac = data.get('in_curnt_ac', round(random.uniform(0, 400), 1))

    return charging_info


def gen_position_status(data=None):
    '''
    车机端采样上来的GPS数据，经常发现漂移现象，经常到太平洋上，故在当前把在销售范围以外的Position给过滤掉了。
    为性能考虑，采取了一种快速判定办法。基本思路是：把整个行政区域划分为几个小的矩形，然后再排除掉一些矩形区域。
    只要一个点在限定的区域内，并且不在排除的区域内，则判定成功，否则失败
    '''
    if data is None:
        data = {}
    position_status = PositionStatus()
    position_status.posng_valid_type = data.get('posng_valid_type', random.choice([0, 1, 2]))
    position_status.longitude = data.get('longitude', round(random.uniform(88, 117), 6))
    position_status.latitude = data.get('latitude', round(random.uniform(32, 39), 6))
    position_status.heading = data.get('heading', random.randint(0, 359))
    position_status.altitude = data.get('altitude', round(random.randint(-10000, 50000) * 0.1, 1))
    position_status.gps_speed = data.get('gps_speed', random.randint(0, 360))

    position_status.climb = data.get('climb', round(random.randint(-1000000, 1000000) * 0.001, 3))
    position_status.gps_ts = data.get('gps_ts', int(round(time.time() * 1000)))
    position_status.longitude_uncertainty = data.get('longitude_uncertainty', round(random.uniform(-180, 180), 3))
    position_status.latitude_uncertainty = data.get('latitude_uncertainty', round(random.uniform(-180, 180), 3))
    position_status.altitude_uncertainty = data.get('altitude_uncertainty',
                                                    round(random.randint(-10000, 50000) * 0.1, 1))
    position_status.gps_speed_uncertainty = data.get('gps_speed_uncertainty', random.randint(0, 360))
    position_status.climb_uncertainty = data.get('climb_uncertainty',
                                                 round(random.randint(-1000000, 1000000) * 0.001, 3))
    position_status.mode = data.get('mode', random.randint(0, 5))
    position_status.fusion_mode = data.get('fusion_mode', random.randint(0, 4))

    position_status.satellite.quantity = data.get('satellite', {}).get('quantity', random.randint(0, 10000))
    position_status.satellite.snr.extend(
        data.get('satellite', {}).get('snr', [round(random.uniform(0, 100), 6), round(random.uniform(0, 100), 6)]))

    try:
        for i in range(len(data['satellite']['skyview'])):
            skyview = position_status.satellite.skyview.add()
            PRN_ID_LIST = list(range(1, 97)) + list(range(120, 164)) + list(range(173, 183)) + list(
                range(193, 198)) + list(range(211, 247))
            skyview.prn_id = data['satellite']['skyview'][i].get('prn_id', random.choice(PRN_ID_LIST))
            skyview.azimuth = data['satellite']['skyview'][i].get('azimuth', random.randint(0, 360))
            skyview.elevation = data['satellite']['skyview'][i].get('elevation', random.randint(0, 360))
            skyview.snr = data['satellite']['skyview'][i].get('snr', round(random.uniform(0, 100), 6))
            skyview.used = data['satellite']['skyview'][i].get('used', random.choice([True, False]))
    except KeyError:
        skyview = position_status.satellite.skyview.add()
        PRN_ID_LIST = list(range(1, 97)) + list(range(120, 164)) + list(range(173, 183)) + list(range(193, 198)) + list(
            range(211, 247))
        skyview.prn_id = random.choice(PRN_ID_LIST)
        skyview.azimuth = random.randint(0, 360)
        skyview.elevation = random.randint(0, 360)
        skyview.snr = round(random.uniform(0, 100), 6)
        skyview.used = random.choice([True, False])

    position_status.attitude.heading = data.get('attitude', {}).get('heading', round(random.uniform(0, 360), 2))
    position_status.attitude.pitch = data.get('attitude', {}).get('pitch', round(random.uniform(-90, 90), 2))
    position_status.attitude.yaw = data.get('attitude', {}).get('yaw', round(random.uniform(0, 360), 2))
    position_status.attitude.roll = data.get('attitude', {}).get('roll', round(random.uniform(-180, 180), 2))
    position_status.attitude.dip = data.get('attitude', {}).get('dip', round(random.uniform(-180, 180), 2))
    position_status.attitude.mag_len = data.get('attitude', {}).get('mag_len', round(random.uniform(0, 50000), 2))
    position_status.attitude.mag_x = data.get('attitude', {}).get('mag_x', round(random.uniform(0, 50000), 2))
    position_status.attitude.mag_y = data.get('attitude', {}).get('mag_y', round(random.uniform(0, 50000), 2))
    position_status.attitude.mag_z = data.get('attitude', {}).get('mag_z', round(random.uniform(0, 50000), 2))
    position_status.attitude.acc_len = data.get('attitude', {}).get('acc_len', round(random.uniform(0, 5000000), 2))
    position_status.attitude.acc_x = data.get('attitude', {}).get('acc_x', round(random.uniform(0, 50000000), 2))
    position_status.attitude.acc_y = data.get('attitude', {}).get('acc_y', round(random.uniform(0, 50000000), 2))
    position_status.attitude.acc_z = data.get('attitude', {}).get('acc_z', round(random.uniform(0, 50000000), 2))
    position_status.attitude.gyro_x = data.get('attitude', {}).get('gyro_x', round(random.uniform(0, 50000000), 2))
    position_status.attitude.gyro_y = data.get('attitude', {}).get('gyro_y', round(random.uniform(0, 50000000), 2))
    position_status.attitude.gyro_z = data.get('attitude', {}).get('gyro_z', round(random.uniform(0, 50000000), 2))
    position_status.attitude.temp = data.get('attitude', {}).get('temp', round(random.uniform(-50, 300), 2))
    position_status.attitude.depth = data.get('attitude', {}).get('depth', round(random.uniform(-100, 900), 2))
    position_status.attitude.x_accel = data.get('attitude', {}).get('x_accel', random.randint(0, 500))
    position_status.attitude.y_accel = data.get('attitude', {}).get('y_accel', random.randint(0, 500))
    position_status.attitude.z_accel = data.get('attitude', {}).get('z_accel', random.randint(0, 500))
    position_status.attitude.x_ang_rate = data.get('attitude', {}).get('x_ang_rate', random.randint(0, 500))
    position_status.attitude.y_ang_rate = data.get('attitude', {}).get('y_ang_rate', random.randint(0, 500))
    position_status.attitude.z_ang_rate = data.get('attitude', {}).get('z_ang_rate', random.randint(0, 500))
    position_status.attitude.imu_status = data.get('attitude', {}).get('imu_status', random.choice([0, 1, 2, 3, 4]))
    position_status.attitude.single_tick_calib_sts = data.get('attitude', {}).get('single_tick_calib_sts',
                                                                                  random.choice([0, 1, 2, 3]))
    position_status.attitude.acc_x_calib_sts = data.get('attitude', {}).get('acc_x_calib_sts',
                                                                            random.choice([0, 1, 2, 3]))
    position_status.attitude.acc_y_calib_sts = data.get('attitude', {}).get('acc_y_calib_sts',
                                                                            random.choice([0, 1, 2, 3]))
    position_status.attitude.acc_z_calib_sts = data.get('attitude', {}).get('acc_z_calib_sts',
                                                                            random.choice([0, 1, 2, 3]))
    position_status.attitude.gyro_x_calib_sts = data.get('attitude', {}).get('gyro_x_calib_sts',
                                                                             random.choice([0, 1, 2, 3]))
    position_status.attitude.gyro_y_calib_sts = data.get('attitude', {}).get('gyro_y_calib_sts',
                                                                             random.choice([0, 1, 2, 3]))
    position_status.attitude.gyro_z_calib_sts = data.get('attitude', {}).get('gyro_z_calib_sts',
                                                                             random.choice([0, 1, 2, 3]))
    position_status.attitude.x_accel_valid = data.get('attitude', {}).get('x_accel_valid', random.choice([True, False]))
    position_status.attitude.y_accel_valid = data.get('attitude', {}).get('y_accel_valid', random.choice([True, False]))
    position_status.attitude.z_accel_valid = data.get('attitude', {}).get('z_accel_valid', random.choice([True, False]))
    position_status.attitude.x_ang_rate_valid = data.get('attitude', {}).get('x_ang_rate_valid',
                                                                             random.choice([True, False]))
    position_status.attitude.y_ang_rate_valid = data.get('attitude', {}).get('y_ang_rate_valid',
                                                                             random.choice([True, False]))
    position_status.attitude.z_ang_rate_valid = data.get('attitude', {}).get('z_ang_rate_valid',
                                                                             random.choice([True, False]))

    try:
        for i in range(len(data['attitude']['sensors'])):
            sensors = position_status.attitude.sensors.add()
            sensors.type = data['attitude']['sensors'][i].get('type',
                                                              random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 255]))
            sensors.is_used = data['attitude']['sensors'][i].get('is_used', random.choice([True, False]))
            sensors.is_ready = data['attitude']['sensors'][i].get('is_ready', random.choice([True, False]))
            sensors.cal_status = data['attitude']['sensors'][i].get('cal_status', random.choice([0, 1, 2, 3]))
            sensors.time_status = data['attitude']['sensors'][i].get('time_status', random.choice([0, 1, 2, 3]))
            sensors.obs_freq = data['attitude']['sensors'][i].get('obs_freq', random.randint(0, 100))
            sensors.fault_bad_meas = data['attitude']['sensors'][i].get('fault_bad_meas', random.choice([True, False]))
            sensors.fault_bad_ttag = data['attitude']['sensors'][i].get('fault_bad_ttag', random.choice([True, False]))
            sensors.fault_missing_meas = data['attitude']['sensors'][i].get('fault_missing_meas',
                                                                            random.choice([True, False]))
            sensors.fault_noisy_meas = data['attitude']['sensors'][i].get('fault_noisy_meas',
                                                                          random.choice([True, False]))

    except KeyError:
        sensors = position_status.attitude.sensors.add()
        sensors.type = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 255])
        sensors.is_used = random.choice([True, False])
        sensors.is_ready = random.choice([True, False])
        sensors.cal_status = random.choice([0, 1, 2, 3])
        sensors.time_status = random.choice([0, 1, 2, 3])
        sensors.obs_freq = random.randint(0, 100)
        sensors.fault_bad_meas = random.choice([True, False])
        sensors.fault_bad_ttag = random.choice([True, False])
        sensors.fault_missing_meas = random.choice([True, False])
        sensors.fault_noisy_meas = random.choice([True, False])

    return position_status


def gen_vehicle_status(data=None):
    if data is None:
        data = {}
    vehicle_status = VehicleStatus()
    vehicle_status.vehl_state = data.get('vehl_state', random.choice(
        [1, 2, 3, 4, 254, 255]))  # vehicle_status_pb2.VehicleStatus.DRIVING
    vehicle_status.chrg_state = data.get('chrg_state', random.choice(
        [1, 2, 3, 4, 254, 255]))  # vehicle_status_pb2.VehicleStatus.NOT_CHARGING
    vehicle_status.oprtn_mode = data.get('oprtn_mode', random.choice(
        [1, 2, 3, 254, 255]))  # vehicle_status_pb2.VehicleStatus.PURE_ELECTRIC
    vehicle_status.speed = data.get('speed', round(random.randint(0,
                                                            6400) * 0.05625, 1))  # 0~2200表示0km/h~220km/h,0xFFFE异常(-2),0xFFFF无效(-1)
    # mileage 最大值为2000000
    '''
    为了防止被恶意篡改里程，及误操作里程数据，并且保证EVM上报数据中的里程的质量，里程上报数据只允许比数据库中存的数据增大，不允许减少，并且符合里程大小小于2000000才会予以更新。
    具体里程更新逻辑如下：
        1.当里程较上次更新减少时，不进行更新。
        2.当里程较上次更新增加小于500km时，不做任何操作，允许更新。
        3.当里程较上次更新增加大于500km且小于50000km时，将检查其平均每天里程是否超过2000km，即平均每秒的里程增加不超过0.02314815km，才允许更新。
        4.当里程较上次更新增加大于50000km时，将检查其平均每天里程是否超过1200km，即平均每秒的里程增加不超过0.01388889km，才允许更新
    '''
    vehicle_status.mileage = data.get('mileage', random.randint(0,
                                                                2000))  # 0~9999999表示0km~999999.9km,0xFFFFFFFE异常(-2),0xFFFFFFFF无效(-1)
    vehicle_status.vehl_totl_volt = data.get('vehl_totl_volt', random.randint(0,
                                                                              6000) * 0.1)  # SH，总电压,GB0~10000表示0~1000V,SH0~60000表示0~6000V,0xFFFE异常(-2),0xFFFF无效(-1)
    vehicle_status.vehl_totl_curnt = data.get('vehl_totl_curnt', round(random.uniform(-3000, 3000),
                                                                       1))  # 0~20000表示-1000A~+10000A,0xFFFE异常(-2),0xFFFF无效(-1)
    vehicle_status.soc = data.get('soc', random.randint(0, 200) * 0.5)  # 0~100表示0%~100%,0xFE异常(-2),0xFF无效(-1)
    vehicle_status.dc_dc_sts = data.get('dc_dc_sts',
                                        random.choice([1, 2, 254, 255]))  # vehicle_status_pb2.VehicleStatus.WORKING
    vehicle_status.gear = data.get('gear', random.randint(0, 7))  # 0表示空挡,1~12表示1~12档,13表示倒挡,14表示自动D挡,15表示停车P挡
    vehicle_status.insulatn_resis = data.get('insulatn_resis', random.randint(0, 65535))  # 0~60000表示0~60000千欧
    vehicle_status.urgt_prw_shtdwn = data.get('urgt_prw_shtdwn', random.choice([True, False]))
    vehicle_status.comf_ena = data.get('comf_ena', random.choice([0, 1]))
    vehicle_status.thermal_keeping = data.get('thermal_keeping', random.choice([True, False]))
    vehicle_status.vehl_type_dbc = data.get('vehl_type_dbc', random.choice(["ES8_7.5.11", "ES6_3.0.11"]))
    vehicle_status.ntester = data.get('ntester', False)

    return vehicle_status


def gen_battery_package_info(data=None, vin=None):
    if data is None:
        data = {}
    battery_package_info = SOCStatus.BatteryPackageInfo()
    if 'btry_pak_encoding' in data:
        for i, item in enumerate(data['btry_pak_encoding']):
            btry_pak_encoding = battery_package_info.btry_pak_encoding.add()
            btry_pak_encoding.btry_pak_sn = item.get('btry_pak_sn', i + 1)
            # 车机电池编码规范（ 70KWH70KWH 50ah P0000084开头 70KWH 102ah P00793开头  84KWH 120ah P0085553和P0073713开头）
            # btry_pak_encoding.nio_encoding = item.get('nio_encoding', random.choice(['P0085553', 'P0073713', 'P0000084']) + ''.join(random.sample(string.ascii_uppercase + string.digits, 24)))
            # 虚拟电池编码规范 vin+'0000000000DDtest'
            gbt = generate_random_gbt_code('001', 'P')
            _, nio_encoding = generate_random_nio_code()
            btry_pak_encoding.nio_encoding = item.get('nio_encoding', nio_encoding)
            btry_pak_encoding.re_encoding = item.get('re_encoding', gbt)
    else:
        btry_pak_encoding1 = battery_package_info.btry_pak_encoding.add()
        btry_pak_encoding1.btry_pak_sn = 1
        gbt = generate_random_gbt_code('001', 'P')
        _, nio_encoding = generate_random_nio_code()
        # 车机电池编码规范（ 70KWH70KWH 50ah P0000084开头 70KWH 102ah P00793开头  84KWH 120ah P0085553和P0073713开头）
        # btry_pak_encoding1.nio_encoding = random.choice(['P0085553', 'P0073713', 'P0000084']) + ''.join(random.sample(string.ascii_uppercase + string.digits, 24))
        btry_pak_encoding1.nio_encoding = nio_encoding
        # 虚拟电池编码规范 vin+'0000000000DDtest'
        # btry_pak_encoding1.nio_encoding = vin + '000000000DDtest'
        # btry_pak_encoding1.re_encoding = 'TSPP' + ''.join(random.sample(string.ascii_uppercase + string.digits, 20))
        btry_pak_encoding1.re_encoding = gbt

    if 'btry_pak_health_status' in data:
        for i, item in enumerate(data['btry_pak_health_status']):
            btry_pak_health_status = battery_package_info.btry_pak_health_status.add()
            btry_pak_health_status.btry_pak_sn = item.get('btry_pak_sn', i + 1)
            btry_pak_health_status.battery_health_status = item.get('battery_health_status',
                                                                    round(random.uniform(0, 1), 1))
    else:
        btry_pak_health_status1 = battery_package_info.btry_pak_health_status.add()
        btry_pak_health_status1.btry_pak_sn = 1
        btry_pak_health_status1.battery_health_status = round(random.uniform(0, 1), 1)

    return battery_package_info


def gen_door_status(data=None):
    if data is None:
        data = {}
    door_status = DoorStatus()
    # DoorLocks
    door_status.door_locks.door_lock_frnt_le_sts = data.get('door_locks', {}).get('door_lock_frnt_le_sts',
                                                                                  random.choice([0, 1, 2]))  # 0 = unlocked, 1 = locked, 2 = reserved, 7 = invalid
    door_status.door_locks.door_lock_frnt_ri_sts = data.get('door_locks', {}).get('door_lock_frnt_ri_sts',
                                                                                  random.choice([0, 1, 2]))  # door_status_pb2.DoorStatus.LOCK_LOCKED
    door_status.door_locks.entry_meth = data.get('door_locks', {}).get('entry_meth',
                                                                       random.choice([0, 1, 2, 3, 4, 7]))  # entry method, 0:remote app, 1:key_fob_1, 2:key_fob_2, 3:nfc, 4:reserved, 7:invalid
    door_status.door_locks.user_id = data.get('door_locks', {}).get('user_id', random.randint(0, 9999))  # 账号id，int32
    door_status.door_locks.access_mode = data.get('door_locks', {}).get('access_mode',
                                                                        random.randint(0, 31))  # 访问模式，31为invalid
    door_status.door_locks.account_id = data.get('door_locks', {}).get('account_id', random.randint(0, 4294967295))  # 账号id，int32

    # DoorAjars
    door_status.door_ajars.door_ajar_frnt_le_sts = data.get('door_ajars', {}).get('door_ajar_frnt_le_sts',
                                                                                  random.choice([0, 1, 2]))  # 车门状态 0 = open, 1 = closed, 2 = reserved, 3 = invalid
    door_status.door_ajars.door_ajar_frnt_ri_sts = data.get('door_ajars', {}).get('door_ajar_frnt_ri_sts',
                                                                                  random.choice([0, 1, 2]))
    door_status.door_ajars.door_ajar_re_le_sts = data.get('door_ajars', {}).get('door_ajar_re_le_sts',
                                                                                random.choice([0, 1, 2]))
    door_status.door_ajars.door_ajar_re_ri_sts = data.get('door_ajars', {}).get('door_ajar_re_ri_sts',
                                                                                random.choice([0, 1, 2]))

    # ChargePort
    if not data or 'charge_port_status' not in data:
        charge_port1 = door_status.charge_port_status.add()
        charge_port1.charge_port_sn = 0  # first
        charge_port1.ajar_status = random.choice([0, 1, 2, 3])
        charge_port2 = door_status.charge_port_status.add()
        charge_port2.charge_port_sn = 1  # second
        charge_port2.ajar_status = random.choice([0, 1, 2, 3])
    else:
        for i in range(len(data['charge_port_status'])):
            charge_port = door_status.charge_port_status.add()
            charge_port.charge_port_sn = data['charge_port_status'][i].get('charge_port_sn', i + 1)
            charge_port.ajar_status = data['charge_port_status'][i].get('ajar_status', random.choice([0, 1, 2, 3]))

    # Tailgate
    door_status.tailgate_status.ajar_status = data.get('tailgate_status', {}).get('ajar_status', random.choice(
        [0, 1, 2, 3]))  # door_status_pb2.DoorStatus.AJAR_CLOSED

    # EngineHood
    door_status.engine_hood_status.ajar_status = data.get('engine_hood_status', {}).get('ajar_status', random.choice(
        [0, 1, 2, 3]))  # door_status_pb2.DoorStatus.AJAR_OPENED

    # All locked
    door_status.vehicle_lock_status = data.get('vehicle_lock_status', random.choice(
        [0, 1, 2, 3]))  # vehicle fully locked status, 0 = not fully locked, 1 = fully locked, 2 = reserved, 3 = invalid

    return door_status


def gen_hvac_status(data=None):
    if data is None:
        data = {}
    hvac_status = HVACStatus()
    hvac_status.amb_temp_c = data.get('amb_temp_c', random.randint(-80, 172) * 0.5)
    hvac_status.outside_temp_c = data.get('outside_temp_c', random.randint(-80, 120) * 0.5)
    hvac_status.air_con_on = data.get("air_con_on", random.choice([True, False]))
    hvac_status.pm_2p5_cabin = data.get('pm_2p5_cabin', random.randint(0, 1023))
    hvac_status.pm_2p5_filter_active = data.get('pm_2p5_filter_active', random.choice([True, False]))
    hvac_status.cbn_pre_sts = data.get('cbn_pre_sts', random.choice([0, 1, 2, 3]))
    hvac_status.ccu_cbn_pre_ac_ena_sts = data.get("ccu_cbn_pre_ac_ena_sts", random.choice([0, 1]))
    hvac_status.ccu_cbn_pre_aqs_ena_sts = data.get('ccu_cbn_pre_aqs_ena_sts', random.choice([0, 1]))
    hvac_status.cbn_hi_t_dry_sts = data.get('cbn_hi_t_dry_sts', random.choice([0, 1, 2]))   # 超强干燥功能状态
    hvac_status.ccu_max_defrst_sts = data.get('ccu_max_defrst_sts', random.choice([0, 1]))  # 空调除霜
    return hvac_status


def gen_window_status(data=None):
    if data is None:
        data = {}
    window_status = WindowStatus()
    window_status.window_positions.win_frnt_le_posn = data.get('window_positions', {}).get('win_frnt_le_posn',
                                                                                           random.randint(0,
                                                                                                          100))  # 范围:[0:100] or =127
    window_status.window_positions.win_frnt_ri_posn = data.get('window_positions', {}).get('win_frnt_ri_posn',
                                                                                           random.randint(0,
                                                                                                          100))  # 范围:[0:100] or =127
    window_status.window_positions.win_re_le_posn = data.get('window_positions', {}).get('win_re_le_posn',
                                                                                         random.randint(0,
                                                                                                        100))  # 范围:[0:100] or =127
    window_status.window_positions.win_re_ri_posn = data.get('window_positions', {}).get('win_re_ri_posn',
                                                                                         random.randint(0,
                                                                                                        100))  # 范围:[0:100] or =127
    window_status.sun_roof_positions.sun_roof_posn = data.get('sun_roof_positions', {}).get('sun_roof_posn',
                                                                                            random.randint(0,
                                                                                                           100))  # 范围:[0:100] or =101 or =102 or =127
    window_status.sun_roof_positions.sun_roof_shade_posn = data.get('sun_roof_positions', {}).get('sun_roof_shade_posn',
                                                                                                  random.randint(0,
                                                                                                                 100))  # 范围:[0:100]
    window_status.sun_roof_positions.sun_roof_posn_sts = data.get('sun_roof_positions', {}).get('sun_roof_posn_sts',
                                                                                                random.randint(0, 7))

    if data.get('window_positions'):
        window_status.window_positions.win_frnt_le_failure.MergeFrom(gen_window_failure(data.get('window_positions', {}).get('win_frnt_le_failure', None)))
        window_status.window_positions.win_frnt_ri_failure.MergeFrom(gen_window_failure(
            data.get('window_positions', {}).get('win_frnt_ri_failure', None)))
        window_status.window_positions.win_re_le_failure.MergeFrom(gen_window_failure(
            data.get('window_positions', {}).get('win_re_le_failure', None)))
        window_status.window_positions.win_re_ri_failure.MergeFrom(gen_window_failure(
            data.get('window_positions', {}).get('win_re_ri_failure', None)))
        window_status.sun_roof_positions.sun_roof_failure.MergeFrom(gen_sunroof_failure(data.get('sun_roof_positions', {}).get('sun_roof_failure',
                                                                                                      None)))
        window_status.sun_roof_positions.sun_roof_shade_failure.MergeFrom(gen_sunroof_failure(data.get('sun_roof_positions', {}).get('sun_roof_shade_failure',
                                                                                                    None)))

    return window_status


def gen_window_failure(data=None):
    if data is None:
        data = {}
    window_failure = WindowStatus.WindowFailure()
    window_failure.hal_error = data.get('hal_error', random.choice([True, False]))
    window_failure.motor_relay_error = data.get('motor_relay_error', random.choice([True, False]))
    window_failure.over_heat_protect = data.get('over_heat_protect', random.choice([True, False]))
    window_failure.lin_response_error = data.get('lin_response_error', random.choice([True, False]))
    window_failure.fl_under_voltage = data.get('fl_under_voltage', random.choice([True, False]))
    window_failure.fl_over_voltage = data.get('fl_over_voltage', random.choice([True, False]))
    window_failure.fl_switch_stick_error = data.get('fl_switch_stick_error', random.choice([True, False]))
    return window_failure


def gen_sunroof_failure(data=None):
    if data is None:
        data = {}
    sunroof_failure = WindowStatus.SunRoofFailure()
    sunroof_failure.ecu_status = data.get('ecu_status', random.choice([True, False]))
    sunroof_failure.hall_sensor_status = data.get('hall_sensor_status', random.choice([True, False]))
    sunroof_failure.relay_status = data.get('relay_status', random.choice([True, False]))
    sunroof_failure.lin_response_error = data.get('lin_response_error', random.choice([True, False]))
    sunroof_failure.over_voltage = data.get('over_voltage', random.choice([True, False]))
    sunroof_failure.under_voltage = data.get('under_voltage', random.choice([True, False]))
    return sunroof_failure


def gen_connection_status(data=None):
    if data is None:
        data = {}
    connectionStatus = ConnectionStatusMsg.connectionStatus()
    connectionStatus.ecu_type = data.get('ecu_type', random.randint(0, 2))
    connectionStatus.status = data.get('status', random.randint(0, 2))
    return connectionStatus


def gen_light_status(data=None):
    if data is None:
        data = {}
    light_status = LightStatus()
    light_status.hi_beam_on = data.get('hi_beam_on', random.choice([0, 1, 2, 3]))
    light_status.lo_beam_on = data.get('lo_beam_on', random.choice([0, 1, 2, 3]))
    light_status.head_light_on = data.get('head_light_on', random.choice([0, 1, 2, 3]))
    return light_status


def gen_driving_data(data=None):
    if data is None:
        data = {}
    driving_data = DrivingData()
    driving_data.vcu_drvg_mod = data.get('vcu_drvg_mod',
                                         random.choice([0, 1, 2, 3, 7]))  # driving_data_pb2.DrivingData.ECONOMY_MODE
    driving_data.steer_whl_rotn_ag = data.get('steer_whl_rotn_ag',
                                              round(random.randint(0, 8000) * 0.1, 1))  # 方向盘转角，0-800度
    driving_data.steer_whl_rotn_spd = data.get('steer_whl_rotn_spd', random.randint(0, 510) * 5)  # 方向盘转速，0-2550度/秒
    driving_data.aclrtn_pedal_posn = data.get('aclrtn_pedal_posn',
                                              round(random.randint(0, 255) * 0.392, 3))  # 加速器踏板位置，0%~99.96%
    driving_data.brk_pedal_sts.state = data.get('brk_pedal_sts', {}).get('state', random.choice([0, 1, 2, 3]))  # 制动踏板状态
    driving_data.brk_pedal_sts.valid = data.get('brk_pedal_sts', {}).get('valid', random.choice([0, 1]))  # 制动踏板是否有效
    driving_data.average_speed = data.get('average_speed', round(random.randint(0, 6400) * 0.05625, 1))  # 上一个上传区间内的平均车速
    driving_data.max_speed = data.get('max_speed', round(random.randint(0, 6400) * 0.05625, 1))
    driving_data.min_speed = data.get('min_speed', round(random.randint(0, 6400) * 0.05625, 1))
    driving_data.veh_dispd_spd = data.get('veh_dispd_spd', round(random.randint(0, 360)))
    driving_data.veh_outd_hum = data.get('veh_outd_hum', round(random.randint(0, 100)))
    driving_data.veh_dispd_spd_sts = data.get('veh_dispd_spd_sts', random.choice([0, 1]))
    return driving_data


def gen_extremum_data(data=None):
    if data is None:
        data = {}
    extremum_data = ExtremumData()
    extremum_data.hist_volt_btry_sbsys_sn = data.get('hist_volt_btry_sbsys_sn', random.randint(1,
                                                                                               250))  # 最高电压电池子系统代号，1~250，0xFE表示异常(254),0xFF表示无效(255)
    extremum_data.hist_volt_singl_btry_sn = data.get('hist_volt_singl_btry_sn', random.randint(1,
                                                                                               255))  # 最高电压电池单体代号，1~250，0xFE表示异常(254),0xFF表示无效(255)
    extremum_data.sin_btry_hist_volt = data.get('sin_btry_hist_volt', random.randint(0,
                                                                                     5000) * 0.001)  # 单体电池最高电压，0~15000表示0~15V，0xFFFE表示异常，0xFFFF表示无效  校验范围:[0:100)
    extremum_data.lwst_volt_btry_sbsys_sn = data.get('lwst_volt_btry_sbsys_sn',
                                                     random.randint(1, 250))  # 最低电压电池子系统号，1~250，0xFE表示异常(254),0xFF表示无效
    extremum_data.lwst_volt_singl_btry_sn = data.get('lwst_volt_singl_btry_sn',
                                                     random.randint(1, 256))  # 最低电压电池单体代号，1~250，0xFE表示异常(254),0xFF表示无效
    extremum_data.sin_btry_lwst_volt = data.get('sin_btry_lwst_volt', random.randint(0,
                                                                                     5000) * 0.001)  # 单体电池最低电压，0~15000表示0~15V，0xFFFE表示异常，0xFFFF表示无效  校验范围:[0:100)
    extremum_data.hist_temp_btry_sbsys_sn = data.get('hist_temp_btry_sbsys_sn',
                                                     random.randint(1, 250))  # 最高温度探针单体序号，1~250，0xFE表示异常(254),0xFF表示无效
    extremum_data.hist_temp_prb_sn = data.get('hist_temp_prb_sn', random.randint(1, 128))  # 最低温度探针单体代号
    extremum_data.highest_temp = data.get('highest_temp',
                                          random.randint(-80, 170) * 0.5)  # 最低温度子系统号，1~250，0xFE表示异常(254),0xFF表示无效
    extremum_data.lwst_temp_btry_sbsys_sn = data.get('lwst_temp_btry_sbsys_sn',
                                                     random.randint(1, 250))  # 最高温度子系统号 对应MSG_LIST里的hist_temp_btry_sn
    extremum_data.lwst_temp_prb_sn = data.get('lwst_temp_prb_sn', random.randint(1, 128))
    extremum_data.lowest_temp = data.get('lowest_temp', random.randint(-80, 170) * 0.5)  # 1~250，代表-40~+，offset是40

    return extremum_data


def gen_bms_status(data=None):
    if data is None:
        data = {}
    bms_status = BmsStatus()
    bms_status.isolation_level = data.get('isolation_level', random.choice([0, 1, 2, 3]))
    bms_status.health_status = data.get('health_status', round(random.randint(0, 1000) * 0.1, 1))
    bms_status.chrg_pwr_lmt = data.get('chrg_pwr_lmt', round(random.randint(0, 10000) * 0.1, 1))
    bms_status.dischrg_pwr_lmt = data.get('dischrg_pwr_lmt', round(random.randint(0, 10000) * 0.1, 1))
    bms_status.avg_cell_volt = data.get('avg_cell_volt', round(random.randint(0, 5000) * 0.001, 3))
    bms_status.avg_temp = data.get('avg_temp', round(random.randint(-40, 85) * 0.5, 1))
    bms_status.in_coolant_temp = data.get('in_coolant_temp', round(random.randint(-40, 85) * 0.125, 3))
    bms_status.out_coolant_temp = data.get('out_coolant_temp', round(random.randint(-40, 85) * 0.125, 3))

    return bms_status


def gen_can_msg(data=None):
    if data is None:
        can_msg = CanMsg()
        for i in range(2):
            can_data1 = can_msg.can_data.add()
            random_key = random.choice(list(CAN_DATA))
            can_data1.msg_id = CAN_DATA[random_key]['msg_id']
            can_data1.value = CAN_DATA[random_key]['value']
    else:
        can_msg = CanMsg()
        if 'can_data' in data:
            for i in range(len(data['can_data'])):
                can_data = can_msg.can_data.add()
                can_data.msg_id = data['can_data'][i]['msg_id']
                value = data['can_data'][i]['value']
                if isinstance(value, bytes):
                    can_data.value = data['can_data'][i]['value']
                elif isinstance(value, str):
                    can_data.value = bytes.fromhex(value)
        if 'can_news' in data:
            for item in data['can_news']:
                can_news = can_msg.can_news.add()
                can_news.msg_id = item['msg_id']
                for it in item['value']:
                    if isinstance(it, bytes):
                        can_news.value.append(it)
                    elif isinstance(it, str):
                        can_news.value.append(bytes.fromhex(it))

    return can_msg


def gen_can_signal(data=None):
    can_signal = CanSignal()
    if not data:
        can_signal.sample_ts = round(time.time() * 1000)
        for i in range(2):
            signal_info1 = can_signal.signal_info.add()
            random_key = random.choice(list(CAN_DATA))
            signal_info1.id = CAN_DATA[random_key]['msg_id']
            for j in range(2):
                data_info1 = signal_info1.data_info.add()
                data_info1.ts_offset = j
                data_info1.data = CAN_DATA[random_key]['value']
    else:
        can_signal.sample_ts = data.get('sample_ts', round(time.time() * 1000))
        for item in data.get('signal_info'):
            signal_info1 = can_signal.signal_info.add()
            signal_info1.id = item.get('id')
            for it in item.get('data_info'):
                data_info1 = signal_info1.data_info.add()
                data_info1.ts_offset = it.get('ts_offset', random.randint(0, 5))
                if isinstance(it['data'], bytes):
                    data_info1.data = it['data']
                elif isinstance(it['data'], str):
                    data_info1.data = bytes.fromhex(it['data'])
    return can_signal


def gen_tyre_status(data=None):
    if data is None:
        data = {}
    tyre_status = TyreStatus()
    tyre_status.frnt_le_whl_press = data.get('frnt_le_whl_press', random.randint(0, 255) * 1.373)
    tyre_status.frnt_le_whl_temp = data.get('frnt_le_whl_temp', random.randint(-50, 205))
    tyre_status.frnt_ri_whl_press = data.get('frnt_ri_whl_press', random.randint(0, 255) * 1.373)
    tyre_status.frnt_ri_whl_temp = data.get('frnt_ri_whl_temp', random.randint(-50, 205))
    tyre_status.re_le_whl_press = data.get('re_le_whl_press', random.randint(0, 255) * 1.373)
    tyre_status.re_le_whl_temp = data.get('re_le_whl_temp', random.randint(-50, 205))
    tyre_status.re_ri_whl_press = data.get('re_ri_whl_press', random.randint(0, 255) * 1.373)
    tyre_status.re_ri_whl_temp = data.get('re_ri_whl_temp', random.randint(-50, 205))

    return tyre_status


def gen_occupant_status(data=None):
    if data is None:
        data = {}

    occupant_status = OccupantStatus()
    occupant_status.fr_le_seat_occupant_status = data.get('fr_le_seat_occupant_status', random.choice(
        [0, 1, 2, 3]))  # occupant_status_pb2.OccupantStatus.OCCUPANT
    occupant_status.fr_ri_seat_occupant_status = data.get('fr_ri_seat_occupant_status', random.choice(
        [0, 1, 2, 3]))  # occupant_status_pb2.OccupantStatus.NO_OCCUPANT

    return occupant_status


def gen_driving_motor(data=None):
    if data is None:
        data = {}

    driving_motor = DrivingMotor()
    driving_motor.pwr_sys_rdy = data.get('pwr_sys_rdy',
                                         random.choice([True, False]))  # True  # power system ready / not ready state

    if data and 'motor_list' in data:
        for i in range(len(data['motor_list'])):
            motor = driving_motor.motor_list.add()
            motor.drvmotr_sn = data['motor_list'][i].get('drvmotr_sn', i + 1)  # 驱动电机序号，1~253
            motor.drvmotr_sts = data['motor_list'][i].get('drvmotr_sts', random.choice(
                [1, 2, 3, 4, 254, 255]))  # driving_motor_pb2.DrivingMotor.MotorDataUnit.ENERGY_CONSUMPTION  # 驱动电机状态
            motor.drvmotr_cntrl_temp = data['motor_list'][i].get('drvmotr_cntrl_temp', random.randint(-40,
                                                                                                      215))  # 驱动电机控制器温度，0~250表示-40~210度，0xFE表示异常(254),0xFF表示无效(255)
            motor.drvmotr_rotn_spd = data['motor_list'][i].get('drvmotr_rotn_spd', random.randint(-32768,
                                                                                                  32767))  # 驱动电机转速，0~65531表示-20000r/min~45531r/min，0xFFFE表示异常，0xFFFF表示无效
            motor.drvmotr_rotn_torq = data['motor_list'][i].get('drvmotr_rotn_torq', random.randint(-16384,
                                                                                                    16376) * 0.125)  # 驱动电机转矩，0~65531表示-2000Nm~4553.1Nm，0xFFFE表示异常，0xFFFF表示无效
            motor.drvmotr_temp = data['motor_list'][i].get('drvmotr_temp', random.randint(-40,
                                                                                          215))  # 驱动电机温度，0~250表示-40~210度，0xFE表示异常(254),0xFF表示无效(255)
            motor.drvmotr_contl_involt = data['motor_list'][i].get('drvmotr_contl_involt', random.randint(0,
                                                                                                          4095) * 0.25)  # 电机控制器输入电压，0~60000表示0~6000V，0xFFFE表示异常，0xFFFF表示无效
            motor.drvmotr_contl_dc_bus_curnt = data['motor_list'][i].get('drvmotr_contl_dc_bus_curnt',
                                                                         random.randint(-20480,
                                                                                        20470) * 0.1)  # 电机控制器直流母线电流，0~20000表示-1000A~+1000A，0xFFFE表示异常，0xFFFF表示无效
            motor.torq_command = data['motor_list'][i].get('torq_command', random.randint(-16384, 16376) * 0.125)
            motor.max_pos_torq_st = data['motor_list'][i].get('max_pos_torq_st', random.randint(-16384, 16376) * 0.125)
            motor.max_neg_torq_st = data['motor_list'][i].get('max_neg_torq_st', random.randint(-16384, 16376) * 0.125)

    else:
        for i in range(2):
            motor = driving_motor.motor_list.add()
            motor.drvmotr_sn = i + 1  # 驱动电机序号，1~253
            motor.drvmotr_sts = random.choice([1, 2, 3, 4, 254, 255])
            motor.drvmotr_cntrl_temp = random.randint(-40, 215)
            motor.drvmotr_rotn_spd = random.randint(-32768, 32767)
            motor.drvmotr_rotn_torq = random.randint(-16384, 16376) * 0.125
            motor.drvmotr_temp = random.randint(-40, 215)
            motor.drvmotr_contl_involt = random.randint(0, 4095) * 0.25
            motor.drvmotr_contl_dc_bus_curnt = random.randint(-20480, 20470) * 0.1
            motor.torq_command = random.randint(-16384, 16376) * 0.125
            motor.max_pos_torq_st = random.randint(-16384, 16376) * 0.125
            motor.max_neg_torq_st = random.randint(-16384, 16376) * 0.125

    return driving_motor


def gen_alarm_signal(data=None, sample_ts=None):
    if data is None:
        data = {}

    alarm_signal = AlarmSignal()

    signals = []

    # default
    if not data or 'signal_int' not in data:
        while True:
            s = random.choice(wti.SIGNAL)
            # 带note标记的都是比较特殊的wti，此处随机选一个的时候不选它
            if 'note' in s:
                continue
            signals.append(s)
            break

        for i in range(len(signals)):
            signal_int = alarm_signal.signal_int.add()
            signal_int.sn = signals[i].get('sn', str(sample_ts))
            signal_int.name = signals[i]['name']
            if isinstance(signals[i]['value'], list):
                signal_int.value = random.choice(signals[i]['value'])
            elif isinstance(signals[i]['value'], int):
                signal_int.value = signals[i]['value']
    # customer passed the signal data
    else:
        signals.extend(data['signal_int'])
        # 可以传空的signal int list
        if len(signals) and signals != [{}]:
            for i in range(len(signals)):
                signal_int = alarm_signal.signal_int.add()
                signal_int.sn = signals[i].get('sn', str(sample_ts))
                signal_int.name = signals[i]['name']
                if isinstance(signals[i]['value'], list):
                    signal_int.value = random.choice(signals[i]['value'])
                elif isinstance(signals[i]['value'], int):
                    signal_int.value = signals[i]['value']

    return alarm_signal


def gen_signal_status(data=None):
    if data is None:
        data = {}

    signal_status = SignalStatus()
    signal_status.signal_type = data.get('signal_type', random.choice([0, 1, 2, 3]))
    signal_status.gps_status = data.get('gps_status', random.choice([0, 1, 2, 3]))

    return signal_status


def gen_alarm_data(data=None):
    if data is None:
        data = {}
    alarm_data = AlarmData()

    if 'common_failure' in data:
        for i in range(len(data['common_failure'])):
            common_failure_unit = alarm_data.common_failure.add()
            common_failure_unit.alarm_tag = data['common_failure'][i].get('alarm_tag', random.choice(list(range(19))))
            common_failure_unit.alarm_level = data['common_failure'][i].get('alarm_level',
                                                                            random.choice([0, 1, 2, 3, 254, 255]))
    else:
        data['common_failure'] = []
        for i in range(1):
            common_failure_unit = alarm_data.common_failure.add()
            data['common_failure'].append({})
            common_failure_unit.alarm_tag = data['common_failure'][i].get('alarm_tag', random.choice(list(range(19))))
            common_failure_unit.alarm_level = data['common_failure'][i].get('alarm_level',
                                                                            random.choice([0, 1, 2, 3, 254, 255]))

    if 'bj_extension' in data:
        for i in range(len(data['bj_extension'])):
            bj_extension_unit = alarm_data.bj_extension.add()
            bj_extension_unit.alarm_tag = data['bj_extension'][i].get('alarm_tag', random.choice(list(range(11))))
            bj_extension_unit.alarm_level = data['bj_extension'][i].get('alarm_level',
                                                                        random.choice([0, 1, 2, 3, 254, 255]))
    else:
        data['bj_extension'] = []
        for i in range(1):
            bj_extension_unit = alarm_data.bj_extension.add()
            data['bj_extension'].append({})
            bj_extension_unit.alarm_tag = data['bj_extension'][i].get('alarm_tag', random.choice(list(range(11))))
            bj_extension_unit.alarm_level = data['bj_extension'][i].get('alarm_level',
                                                                        random.choice([0, 1, 2, 3, 254, 255]))

    if 'sh_extension' in data:
        for i in range(len(data['sh_extension'])):
            sh_extension_unit = alarm_data.sh_extension.add()
            sh_extension_unit.alarm_tag = data['sh_extension'][i].get('alarm_tag', random.choice(
                list(range(6))))  # driving_motor_pb2.DrivingMotor.MotorDataUnit.ENERGY_CONSUMPTION  # 驱动电机状态
            sh_extension_unit.alarm_level = data['sh_extension'][i].get('alarm_level',
                                                                        random.choice([0, 1, 2, 3, 254,
                                                                                       255]))  # driving_motor_pb2.DrivingMotor.MotorDataUnit.ENERGY_CONSUMPTION  # 驱动电机状态
    else:
        data['sh_extension'] = []
        for i in range(1):
            sh_extension_unit = alarm_data.sh_extension.add()
            data['sh_extension'].append({})
            sh_extension_unit.alarm_tag = data['sh_extension'][i].get('alarm_tag', random.choice(
                list(range(6))))  # driving_motor_pb2.DrivingMotor.MotorDataUnit.ENERGY_CONSUMPTION  # 驱动电机状态
            sh_extension_unit.alarm_level = data['sh_extension'][i].get('alarm_level',
                                                                        random.choice([0, 1, 2, 3, 254, 255]))

    return alarm_data


def gen_driving_behaviour_event(vin, data=None):
    if data is None:
        data = {}

    driving_behaviour_event = DrivingBehaviourEvent()
    driving_behaviour_event.id = data.get('id', vin)
    driving_behaviour_event.version = data.get('version', pb2.VERSION)
    '''
    1.采样时间毫秒与秒兼容处理。
    2.新的sample_ts 需要大于数据库中的 sample_ts。
    3.publish_ts 与 sample_ts，取较小的作为 sample_ts。
    4.对于采样时间超前的情况进行过滤，大于当前时间+1小时则不进行更新
    '''
    driving_behaviour_event.sample_ts = data.get('sample_ts', round(time.time() * 1000))
    driving_behaviour_event.behaviour.extend(data.get('behaviour', random.sample([0, 1, 2], 1)))

    return driving_behaviour_event


def gen_heating_status(data=None):
    if data is None:
        data = {}

    heating_status = HeatingStatus()
    heating_status.steer_wheel_heat_sts = data.get('steer_wheel_heat_sts', random.choice(
        [0, 1, 2, 3]))  # 方向盘加热状态， 0-off, 1-on, 2-reserved, 3-invalid
    heating_status.seat_heat_frnt_le_sts = data.get('seat_heat_frnt_le_sts', random.choice(
        [0, 1, 2, 3, 7]))  # 主驾座椅加热状态， 0-off, 1-low, 2-middle, 3-high, 7-invalid
    heating_status.seat_heat_frnt_ri_sts = data.get('seat_heat_frnt_ri_sts', random.choice(
        [0, 1, 2, 3, 7]))  # 副驾座椅热状态， 0-off, 1-low, 2-middle, 3-high, 7-invalid
    heating_status.seat_heat_re_le_sts = data.get('seat_heat_re_le_sts', random.choice(
        [0, 1, 2, 3, 7]))  # 左后座椅加热状态， 0-off, 1-low, 2-middle, 3-high, 7-invalid
    heating_status.seat_heat_re_ri_sts = data.get('seat_heat_re_ri_sts', random.choice(
        [0, 1, 2, 3, 7]))  # 右后座椅加热状态， 0-off, 1-low, 2-middle, 3-high, 7-invalid
    heating_status.hv_batt_pre_sts = data.get('hv_batt_pre_sts', random.choice(
        [0, 1, 2, 3]))  # 高压电池预加热状态， 0-off, 1-preheating, 2-calculating, 3-invalid
    heating_status.seat_vent_frnt_le_sts = data.get('seat_vent_frnt_le_sts', random.choice(
        [0, 1, 2, 3, 7]))  # 主驾座椅通风状态， 0-off, 1-low, 2-middle, 3-high, 7-invalid
    heating_status.seat_vent_frnt_ri_sts = data.get('seat_vent_frnt_ri_sts', random.choice(
        [0, 1, 2, 3, 7]))  # 副驾座椅通风状态， 0-off, 1-low, 2-middle, 3-high, 7-invalid
    heating_status.btry_warm_up_sts = data.get('btry_warm_up_sts', random.choice([0, 1, 2]))
    heating_status.seat_vent_re_le_sts = data.get('seat_vent_re_le_sts', random.choice(
        [0, 1, 2, 3, 7]))  # 主驾座椅通风状态， 0-off, 1-low, 2-middle, 3-high, 7-invalid
    heating_status.seat_vent_re_ri_sts = data.get('seat_vent_re_ri_sts', random.choice(
        [0, 1, 2, 3, 7]))  # 副驾座椅通风状态， 0-off, 1-low, 2-middle, 3-high, 7-invalid
    return heating_status


def gen_nbs_status(data=None):
    if data is None:
        data = {}

    nbs_status = NBSStatus()
    nbs_status.nbs_sts = data.get('nbs_sts', random.choice(
        [0, 1, 2, 3, 4, 5, 6]))  # NBS功能状态，0-off, 1-invalid, 2-standby, 3-moving, 4-abort, 5-fail, 6-reserved
    nbs_status.nbs_blkage = data.get('nbs_blkage', random.randint(0, 3))  # 车辆是否被障碍物阻挡：0-无阻挡，1-前方阻挡，2-后方阻挡，3-前后方都有阻挡
    nbs_status.nbs_instruction = data.get('nbs_instruction', random.randint(0, 15))  # NearbySummoning Instruction
    nbs_status.nbs_abort_reason = data.get('nbs_abort_reason', random.randint(0, 35))  # NearbySummoning Abort Reason
    nbs_status.nbs_blkage_frnt_le = data.get('nbs_blkage_frnt_le', random.choice([0, 1]))
    nbs_status.nbs_blkage_frnt_ri = data.get('nbs_blkage_frnt_ri', random.choice([0, 1]))
    nbs_status.nbs_blkage_re_le = data.get('nbs_blkage_re_le', random.choice([0, 1]))
    nbs_status.nbs_blkage_re_ri = data.get('nbs_blkage_re_ri', random.choice([0, 1]))
    return nbs_status


def gen_adas_header(data=None, ts=None):
    if data is None:
        data = {}

    adas_header = AdasHeader()
    adas_header.timestamp = data.get('timestamp', ts if ts else round(time.time() * 1000))
    adas_header.vehicle_type = data.get('vehicle_type', random.choice([0, 1, 2, 3]))
    adas_header.adc_git_branch = data.get('adc_git_branch', 'Kaku')
    adas_header.adc_git_commit = data.get('adc_git_commit', '876bfd5af')
    adas_header.proto_git_commit = data.get('proto_git_commit', '0a82e066c')
    adas_header.vehicle_state = data.get('vehicle_state', random.choice([0, 1, 2, 3, 15]))
    adas_header.mileage = data.get('mileage', random.randint(0, 2000))
    adas_header.vehicle_speed = data.get('vehicle_speed', round(random.uniform(1, 10), 1))
    adas_header.yaw_rate = data.get('yaw_rate', round(random.uniform(1, 10), 1))
    adas_header.steering_angle = data.get('steering_angle', round(random.uniform(1, 10), 1))
    adas_header.steering_angle_speed = data.get('steering_angle_speed', round(random.uniform(1, 10), 1))
    adas_header.acc_pedal_position = data.get('acc_pedal_position', round(random.uniform(1, 10), 1))
    adas_header.brake_pedal_status = data.get('brake_pedal_status', random.choice([0, 1, 2, 3]))
    adas_header.brake_pressure = data.get('brake_pressure', round(random.uniform(1, 10), 1))
    adas_header.turn_indicator = data.get('turn_indicator', random.choice([0, 1, 2, 3]))
    adas_header.gps_longitude = data.get('gps_longitude', round(random.uniform(1, 10), 1))
    adas_header.gps_latitude = data.get('gps_latitude', round(random.uniform(1, 10), 1))
    adas_header.gps_heading = data.get('gps_heading', round(random.uniform(1, 10), 1))
    adas_header.gps_status = data.get('gps_status', random.choice([0, 1, 2, 3]))
    adas_header.gps_hdop = data.get('gps_hdop', round(random.uniform(1, 10), 1))

    return adas_header


def gen_feature_status(data=None, ts=None):
    if data is None:
        data = {}

    feature_status = FeatureStatus()
    feature_status.lks_tq_req_valid = data.get('lks_tq_req_valid', random.choice([True, False]))
    feature_status.das_drowsiness_sts = data.get('das_drowsiness_sts', random.randint(0, 7))
    feature_status.hma_sts = data.get('hma_sts', random.randint(0, 7))
    feature_status.lane_assist_sts = data.get('lane_assist_sts', random.randint(0, 7))
    feature_status.tja_sts = data.get('tja_sts', random.randint(0, 7))
    feature_status.tsr_operating_sts = data.get('tsr_operating_sts', random.randint(0, 7))
    feature_status.acc_mod = data.get('acc_mod', random.randint(0, 7))
    feature_status.lks_le_tracking_sts = data.get('lks_le_tracking_sts', random.randint(0, 3))
    feature_status.lks_ri_tracking_sts = data.get('lks_ri_tracking_sts', random.randint(0, 3))
    feature_status.lks_sts = data.get('lks_sts', random.randint(0, 7))
    feature_status.aeb_sts = data.get('aeb_sts', random.randint(0, 3))
    feature_status.fcw_set_sts = data.get('fcw_set_sts', random.randint(0, 3))
    feature_status.go_notifier_on_off_sts = data.get('go_notifier_on_off_sts', random.choice([True, False]))
    feature_status.obj_valid = data.get('obj_valid', random.choice([True, False]))
    feature_status.pcw_latent_warn_on_off_sts = data.get('pcw_latent_warn_on_off_sts', random.choice([True, False]))
    feature_status.pcw_pre_warn_on_off_sts = data.get('pcw_pre_warn_on_off_sts', random.choice([True, False]))
    feature_status.text_info = data.get('text_info', random.randint(0, 19))
    feature_status.tsr_spd_lim_data_on_off_sts = data.get('tsr_spd_lim_data_on_off_sts', random.choice([True, False]))
    feature_status.frnt_le_rsds_disp = data.get('frnt_le_rsds_disp', random.randint(0, 8))
    feature_status.frnt_ri_rsds_disp = data.get('frnt_ri_rsds_disp', random.randint(0, 8))
    feature_status.acc_np_sts = data.get('acc_np_sts', random.randint(0, 7))
    feature_status.timestamp = data.get('timestamp', ts // 1000 if ts else round(time.time()))
    feature_status.sapa_status = data.get('sapa_status', random.randint(0, 7))
    feature_status.nop_sts = data.get('nop_sts', random.randint(0, 7))
    feature_status.nop_msg = data.get('nop_msg', random.randint(0, 31))
    feature_status.nop_enable = data.get('nop_enable', random.choice([True, False]))
    feature_status.nop_lane_chng_confirm_method = data.get('nop_lane_chng_confirm_method', random.randint(0, 3))

    return feature_status


def gen_low_soc_range(data=None):
    if data is None:
        data = {}
    low_soc_range = LowSocRange()
    low_soc_range.low_soc_status = data.get('low_soc_status', random.choice([0, 1, 2]))
    return low_soc_range


def gen_body_status(data=None):
    if data is None:
        data = {}
    '''
    optional int32 wiper_req = 1; //RLS wiper request to CGW 0 Wiper off;1 Wiper action once;2 Speed1(Lo);3 Speed2(Hi);4 Reserved;5 Reserved;6 Reserved;7 SNA
    optional int32 rain_sensor_fail_sts = 2; //Rain sensor failure status 0 No Error 1 Error
    optional int32 frnt_wipr_inter_spd = 3; //Front wiper intermittent speed 0 Reserved;1 intermittent speed 1;2 intermittent speed 2;3 intermittent speed 3;4 intermittent speed 4;5 Reserved;6 Reserved;7 Invalid
    optional int32 frnt_wiper_park_sts = 4; //Front wiper park position status 0 Park;1 No park;2 Reserved;3 Invalid
    optional int32 frnt_wipr_swt_sts = 5; //Front wiper switch status 0 Front wiper off;1 Front wiper low speed;2 Front wiper high speed;3 Front wiper intermediate speed;4 Front wiper wipe one time;5 Reserved;6 Reserved;7 Invalid
    optional int32 wiper_swith_position = 6; //Wiper switch position 0 Wiper off;1 Wiper in Auto mode;2 Wiper in manual mode;3 Wash mode;4 Reserved;5 Reserved;6 Reserved;7 Reserved;
    optional int32 drv_cushion_length_pos = 7; //Driver Cushion Length position 0-65534
    optional int32 drv_cushion_hight_pos = 8; //Driver Cushion Height position 0-16382
    optional int32 drv_backrest_pos =9; //Driver Cushion Backrest position 0-65534
    optional int32 drv_cushion_tilt_pos =10;  //Driver Cushion Tilt position 0-65534
    optional int32 pass_cushion_length_pos = 11; //Passenger Cushion Length position 0-65534
    optional int32 pass_leg_support_pos = 12; //Passenger Leg Support position 0-65534
    optional int32 pass_backrest_pos = 13; //Passenger Backrest position 0-65534
    optional int32 seat_adjmt_frnt_ri_cush_lift_mot_posn = 14;  //Passenger Cushion Height position 0-16383
    optional int32 seat_adjmt_foot_rest_mot_posn = 15; //Passenger FootRest position 0-16383
    '''
    body_status = BodyStatus()
    body_status.wiper_req = data.get('wiper_req', random.randint(0, 7))
    body_status.rain_sensor_fail_sts = data.get('rain_sensor_fail_sts', random.randint(0, 1))
    body_status.frnt_wipr_inter_spd = data.get('frnt_wipr_inter_spd', random.randint(0, 7))
    body_status.frnt_wiper_park_sts = data.get('frnt_wiper_park_sts', random.randint(0, 3))
    body_status.frnt_wipr_swt_sts = data.get('frnt_wipr_swt_sts', random.randint(0, 7))
    body_status.wiper_swith_position = data.get('wiper_swith_position', random.randint(0, 7))
    body_status.drv_cushion_length_pos = data.get('drv_cushion_length_pos', random.randint(0, 65534))
    body_status.drv_cushion_hight_pos = data.get('drv_cushion_hight_pos', random.randint(0, 16382))
    body_status.drv_backrest_pos = data.get('drv_backrest_pos', random.randint(0, 65534))
    body_status.drv_cushion_tilt_pos = data.get('drv_cushion_tilt_pos', random.randint(0, 65534))
    body_status.pass_cushion_length_pos = data.get('pass_cushion_length_pos', random.randint(0, 65534))
    body_status.pass_leg_support_pos = data.get('pass_leg_support_pos', random.randint(0, 65534))
    body_status.pass_backrest_pos = data.get('pass_backrest_pos', random.randint(0, 65534))
    body_status.seat_adjmt_frnt_ri_cush_lift_mot_posn = data.get('seat_adjmt_frnt_ri_cush_lift_mot_posn',
                                                                 random.randint(0, 16383))
    body_status.seat_adjmt_foot_rest_mot_posn = data.get('seat_adjmt_foot_rest_mot_posn', random.randint(0, 16383))
    return body_status


def gen_trip_status(data=None):
    if data is None:
        data = {}
    '''
    optional int32 trip_state = 1; //trip state 1 trip off;2 trip on ;3 invalil;
    optional float trip_odometer = 2; //trip odometer in CDC, 0-9999.9
    optional float trip_eng =3;   // the battery consumes power during the trip
    optional float hv_ass_eng_pct = 4; // High voltage accessory power consumption ratio 0-100
    optional float lv_ass_eng_pct = 5; // Low voltage accessory power consumption ratio 0-100
    optional float dri_eng_pct = 6;  // Ratio of drving energy consumption to total power consumption 0-100
    optional float reg_eng_pct = 7; // Ratio of energy recovery to total power consumption 0-100
    '''
    trip_status = TripStatus()
    trip_status.trip_state = data.get('trip_state', random.randint(1, 3))
    trip_status.trip_odometer = data.get('trip_odometer', random.randint(0, 100))
    trip_status.trip_eng = data.get('trip_eng', random.randint(0, 100))
    trip_status.hv_ass_eng_pct = data.get('hv_ass_eng_pct', random.randint(0, 100))
    trip_status.lv_ass_eng_pct = data.get('lv_ass_eng_pct', random.randint(0, 100))
    trip_status.dri_eng_pct = data.get('dri_eng_pct', random.randint(0, 100))
    trip_status.reg_eng_pct = data.get('reg_eng_pct', random.randint(0, 100))
    trip_status.hvh_eng_pct = data.get('hvh_eng_pct', random.randint(0, 100))
    trip_status.trip_id = data.get('trip_id', str(round(time.time())))
    trip_status.user_id = data.get('user_id', round(time.time()))
    return trip_status


def gen_sys_info_item(data=None):
    sys_info_item = GDSystemInformationEvent.SysInfoItem()
    sys_info_item.key = data.get('key')
    sys_info_item.value = data.get('value', str(random.randint(0, 100)))
    return sys_info_item


def gen_event_item(data=None):
    event_item = GDEventReportEvent.GDEventItem()
    event_item.event_type = data.get('event_type', random.choice([0, 1, 2, 3]))
    event_item.can_id = data.get('can_id', random.randint(0, 2147483647))
    event_item.can_bus_id = data.get('can_bus_id', random.randint(0, 2147483647))
    event_item.counter = data.get('counter', random.randint(0, 255))
    return event_item


def generate_random_nio_code():
    # 电池nio_code生成格式
    # [8位零件号(数字字母)]V[两位版本号(字母)]D[5位制造日期(数字，儒略日期格式)][6位供应商代码(数字字母)]S[6位供应商信息(数字字母)]N[5位序列号(数字)]
    # 8位零件号一般使用P开头, 按照虚拟电池包创建要求，在'P0085553', 'P0073713', 'P0000084'三个值中选择
    # nio_code为36位字符串，nio_encoding为去掉nio_code的4个标识码(V D S N)后的32位字符串
    # 按照虚拟电池包创建要求，后五位改为Dtest方便过滤
    component_no = random.choice(['P0085553', 'P0073713', 'P0000084'])
    version = ''.join(random.choices(string.ascii_uppercase, k=2))
    product_date = ''.join(random.choices(string.digits, k=5))
    supplier = ''.join(random.choices(string.digits + string.ascii_uppercase, k=6))
    supplier_info = ''.join(random.choices(string.digits + string.ascii_uppercase, k=6))
    # sn = ''.join(random.choices(string.digits, k=5))
    sn = 'Dtest'
    nio_code = f'{component_no}V{version}D{product_date}{supplier}S{supplier_info}N{sn}'
    nio_encoding = f'{component_no}{version}{product_date}{supplier}{supplier_info}{sn}'
    return nio_code, nio_encoding


def generate_random_gbt_code(supplier, product_type, count=1):
    # 电池国标码生成格式
    # https://git.nevint.com/greatwall/battery-trace/blob/master/docs/GBT%E5%9B%BD%E6%A0%87%E8%A7%A3%E6%9E%90.png
    # [3位供应商代码][1位产品类型代码][1位电池类型代码][2位规格代码][7位追溯信息代码][3位生产日期代码][7位序列号]
    # 共24位字符串
    # 供应商代码:
    # 03U - 正力蔚来
    # 001 - CATL
    # 071 - XPT
    # 产品类型代码:
    # P: 电池
    # M: 模组
    # C: 单体
    # 电池类型A-G，Z为其他，具体指代参考上述文档
    # 规格代码： 01, 03
    battery_type_option = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'Z']
    year_option = ['7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    month_option = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C']
    day_option = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L',
                  'M', 'N', 'P', 'R', 'S', 'T', 'V', 'W', 'X', 'Y']
    battery_type = random.choice(battery_type_option)
    spec = random.choice(["01", "03"])
    trace = ''.join(random.choices(string.digits, k=7))
    today = date.today()
    year = today.year
    month = today.month
    day = today.day
    if year < 2017:
        year = 2017
    produce_date = f'{year_option[year - 2017]}{month_option[month - 1]}{day_option[day % 31]}'
    if count < 2:
        result = f'{supplier}{product_type}{battery_type}{spec}{trace}{produce_date}' \
                 f'{"".join(random.choices(string.digits + string.ascii_uppercase, k=7))}'
    else:
        result = []
        for _ in range(count):
            result.append(f'{supplier}{product_type}{battery_type}{spec}{trace}{produce_date}'
                          f'{"".join(random.choices(string.digits + string.ascii_uppercase, k=7))}')
    return result


def gen_power_swap_event(data=None):
    if data is None:
        data = {}
    power_swap = PowerSwapEvent()
    power_swap.veh_pwr_swap_mod_req = data.get('veh_pwr_swap_mod_req', random.randint(0, 3))
    power_swap.pwr_swap_mod_sts = data.get('pwr_swap_mod_sts', random.randint(0, 3))
    power_swap.pwr_swap_res = data.get('pwr_swap_res', random.randint(0, 3))
    power_swap.veh_posn_confirm = data.get('veh_posn_confirm', random.randint(0, 3))
    power_swap.veh_prep_req = data.get('veh_prep_req', random.randint(0, 2))
    power_swap.pwr_swap_cdn_prep = data.get('pwr_swap_cdn_prep', random.randint(0, 3))
    power_swap.epb_sts = data.get('epb_sts', random.randint(0, 4))
    power_swap.vcu_act_gear = data.get('vcu_act_gear', random.randint(0, 4))
    power_swap.lc_deactivation_request_sts = data.get('lc_deactivation_request_sts', random.randint(0, 1))
    power_swap.chd_secu_door_lock_sts = data.get('chd_secu_door_lock_sts', random.randint(0, 3))
    power_swap.pwr_swap_mod_failr_warn = data.get('pwr_swap_mod_failr_warn', random.randint(0, 7))
    power_swap.pwr_swap_warn_text = data.get('pwr_swap_warn_text', random.randint(0, 26))
    power_swap.pwr_swap_steer_whl_rotn_ag = data.get('pwr_swap_steer_whl_rotn_ag', random.randint(0, 900))
    return power_swap


def gen_power_swap_periodic(data=None):
    if data is None:
        data = {}
    power_swap = PowerSwapPeriodic()
    power_swap.pwr_swap_process = data.get('pwr_swap_process', random.randint(0, 11))
    power_swap.station_pwr_swap_step = data.get('station_pwr_swap_step', random.randint(0, 9))
    power_swap.cdc_chd_secu_door_lock_req = data.get('cdc_chd_secu_door_lock_req', random.randint(0, 3))
    power_swap.cgw_chd_secu_door_lock_unlock = data.get('cgw_chd_secu_door_lock_unlock', random.randint(0, 3))
    power_swap.bcm_chd_secu_door_lock_sts = data.get('bcm_chd_secu_door_lock_sts', random.randint(0, 3))
    return power_swap


def gen_upload_info(data=None):
    if data is None:
        data = {}
    upload_info = UploadInfo()
    upload_info.event_name = data.get('event_name', "event_1")
    upload_info.rules_trig = data.get('rules_trig', "rule_2")
    upload_info.latitude = data.get('latitude', round(random.uniform(32, 39), 6))
    upload_info.longitude = data.get('longitude', round(random.uniform(88, 117), 6))
    upload_info.priority = data.get('priority', random.randint(0, 3))
    return upload_info


def gen_flow_info(data=None):
    if data is None:
        data = {}
    flow_info = FlowInfo()
    flow_info.stat_starttime = data.get('stat_starttime', round(time.time()))
    flow_info.stat_endtime = data.get('stat_endtime', round(time.time()))
    flow_info.stat_endtime = data.get('stat_endtime', random.randint(0, 1000000000))
    if 'event_info' in data:
        for item in data['event_info']:
            event_info = flow_info.event_info.add()
            event_info.app_name = item['app_name']
            event_info.event_name = item['event_name']
            event_info.event_flow = item['event_flow']

    else:
        event_info = flow_info.event_info.add()
        event_info.app_name = 'cdm_app'
        event_info.event_name = 'report_cdm_version'
        event_info.event_flow = random.randint(0, 10000)
    return flow_info


def gen_sa_cellular_status(data=None):
    if data is None:
        data = {}
    sa_cellular_status = SACellularStatus()
    sa_cellular_status.prefmode_number = data.get('prefmode_number', random.randint(1, 100))
    sa_cellular_status.cfun_number = data.get('cfun_number', random.randint(1, 100))
    sa_cellular_status.disconnection_type = data.get('disconnection_type', random.choice([1, 2, 3, 4, 5]))
    sa_cellular_status.disconnection_duration = data.get('disconnection_duration', random.randint(1, 2000))
    sa_cellular_status.flight_mode_number = data.get('flight_mode_number', random.randint(1, 100))
    sa_cellular_status.restart_or_not = data.get('restart_or_not', random.choice([0, 1]))
    return sa_cellular_status


def gen_high_fre_data(data=None):
    if data is None:
        data = {}
    high_fre_data = HighFreData()
    high_fre_data.sample_time = data.get('sample_time', round(time.time()*1000))
    high_fre_data.can_msg.MergeFrom(data.get('can_msg', gen_can_msg(None)))
    high_fre_data.attitude.MergeFrom(data.get('attitude', gen_position_status(None).attitude))
    high_fre_data.steerWhlag.MergeFrom(data.get('steerWhlag', gen_driving_data(None)))
    return high_fre_data
