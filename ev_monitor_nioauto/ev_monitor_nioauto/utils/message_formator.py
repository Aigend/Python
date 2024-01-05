import codecs
import copy
import json
import time
from datetime import datetime
from nio_messages.can_data import CAN_DATA
from nio_messages.wti import TYRE_WIT_SIGNAL
from utils.coordTransform import wgs84_to_gcj02
from utils.time_parse import timestamp_to_utc_strtime
from utils.http_client import TSPRequest as hreq
from utils.random_tool import format_time_to_int_10


class MessageFormator(object):
    def __init__(self, vehicle_id, sample_ts=None, env=None, cmdopt='test'):
        self.vehicle_id = vehicle_id
        self.env = env
        self.cmdopt = cmdopt
        if sample_ts:
            self.sample_ts = sample_ts
            str_time = timestamp_to_utc_strtime(sample_ts)
            self.sample_time = str_time if str_time[-7:] != '.000000' else str_time[:-7]
        else:
            self.sample_ts = None
            self.sample_time = None

    def to_mysql_status_position(self, position_status):
        data = copy.deepcopy(position_status)

        data['id'] = self.vehicle_id
        data['sample_time'] = self.sample_time
        data['satellite_snr'] = ','.join(['%.6f' % item for item in position_status['satellite']['snr']])
        data['satellite_quantity'] = position_status['satellite']['quantity']

        if 'marcopolo' in self.cmdopt:
            data['longitude_gcj02'] = position_status['longitude']
            data['latitude_gcj02'] = position_status['latitude']
        else:
            gcj02_coord = wgs84_to_gcj02(position_status['longitude'], position_status['latitude'])
            data['longitude_gcj02'] = round(gcj02_coord[0], 6)
            data['latitude_gcj02'] = round(gcj02_coord[1], 6)
        data['longitude_wgs84'] = position_status['longitude']
        data['latitude_wgs84'] = position_status['latitude']
        data['gps_time'] = str(datetime.utcfromtimestamp(int(position_status['gps_ts']) / 1000.0))
        data['altitude'] = 9999.999 if position_status['altitude'] > 9999.999 else position_status['altitude']
        data['climb'] = 9999.999999 if position_status['climb'] > 9999.999999 else position_status['climb']

        data.pop('longitude')
        data.pop('latitude')
        data.pop('satellite')
        data.pop('attitude')
        data.pop('gps_ts')

        return data

    def to_mysql_status_vehicle(self, vehicle_status):
        data = copy.deepcopy(vehicle_status)

        data['id'] = self.vehicle_id
        data['sample_time'] = self.sample_time
        data['vehl_totl_volt'] = round(vehicle_status['vehl_totl_volt'], 1)
        data['speed'] = round(vehicle_status['speed'], 1)
        data['vehl_totl_curnt'] = round(vehicle_status['vehl_totl_curnt'], 1)
        data['chrg_sts'] = vehicle_status['chrg_state']
        data['vehl_sts'] = vehicle_status['vehl_state']
        data['thermal_keeping'] = 1 if (data['thermal_keeping'] == True) else 0
        data['urgt_prw_shtdwn'] = 1 if (data['urgt_prw_shtdwn'] == True) else 0

        data.pop('chrg_state')
        data.pop('vehl_state')

        return data

    def to_mysql_status_soc(self, soc_status, charging_info=None):
        data = copy.deepcopy(soc_status)

        if charging_info:
            data.update(charging_info)
            if 'in_curnt_ac' in data:
                data['in_curnt_ac'] = round(data['in_curnt_ac'], 1)
        data['id'] = self.vehicle_id
        data['sample_time'] = self.sample_time
        data['btry_cap'] = round(soc_status['btry_cap'], 1)
        data['hivolt_btry_curnt'] = round(soc_status['hivolt_btry_curnt'], 1)
        data['dump_enrgy'] = round(soc_status['dump_enrgy'], 1)
        data['btry_pak_sum'] = len(soc_status['btry_paks'])
        data['power_consumption'] = soc_status['realtime_power_consumption']
        data['btry_qual_actvtn'] = 1 if soc_status['btry_qual_actvtn'] == True else 0
        # 这个值是由rvs server添加的值，用户可自己设定。不是来源于上报的值
        # 可以通过上报special event事件type为max_charging_soc_event来设置
        # data['max_soc'] = 100.0
        data['v2l_status'] = data.pop('soc_v2l_status')
        data.pop('btry_paks')
        data.pop('realtime_power_consumption')

        return data

    def to_mysql_status_btry_packs(self, btry_paks=None, btry_pak_encoding=None, btry_pak_health_status=None):
        data = {}

        data['id'] = self.vehicle_id
        data['sample_time'] = self.sample_time

        if btry_paks:
            data.update(btry_paks)
            data['serial_num'] = btry_paks['btry_pak_sn']
            data['voltage'] = round(btry_paks['btry_pak_voltage'], 1)
            data['current'] = round(btry_paks['btry_pak_curnt'], 1)
            data['sin_btry_voltage'] = ','.join([str(item) for item in btry_paks['sin_btry_voltage']])
            data['prb_temp_lst'] = ','.join([str(item) for item in btry_paks['prb_temp_lst']])
            data['sin_btry_voltage_inv'] = ','.join([str(item) for item in btry_paks['sin_btry_voltage_inv']])
            data['prb_temp_lst_inv'] = ','.join([str(item) for item in btry_paks['prb_temp_lst_inv']])
            data.pop('btry_pak_sn')
            data.pop('btry_pak_voltage')
            data.pop('btry_pak_curnt')

        if btry_pak_encoding:
            data['nio_encoding'] = btry_pak_encoding['nio_encoding']
            data['re_encoding'] = btry_pak_encoding['re_encoding']

        if btry_pak_health_status:
            data['battery_health_status'] = round(btry_pak_health_status['battery_health_status'], 1)

        return data

    def to_mysql_status_skyview(self, skyview):
        data = copy.deepcopy(skyview)
        data['id'] = self.vehicle_id
        data['sample_time'] = self.sample_time

        return data

    def to_mysql_status_attitude(self, attitude):
        data = copy.deepcopy(attitude)
        data['id'] = self.vehicle_id
        data['sample_time'] = self.sample_time

        data.pop('sensors')

        return data

    def to_mysql_status_sensors(self, sensors):
        data = copy.deepcopy(sensors)
        data['id'] = self.vehicle_id
        data['sample_time'] = self.sample_time

        return data

    def to_mysql_status_door(self, door_status):
        data = {}

        data['id'] = self.vehicle_id
        data['sample_time'] = self.sample_time
        data.update(door_status['door_locks'])
        data['door_ajar_frnt_ri_sts'] = door_status['door_ajars']['door_ajar_frnt_ri_sts']
        data['door_ajar_frnt_le_sts'] = door_status['door_ajars']['door_ajar_frnt_le_sts']
        data['door_ajar_re_ri_sts'] = door_status['door_ajars']['door_ajar_re_ri_sts']
        data['door_ajar_re_le_sts'] = door_status['door_ajars']['door_ajar_re_le_sts']
        data['fst_chrg_port_ajar_sts'] = door_status['charge_port_status'][0]['ajar_status']
        data['sec_chrg_port_ajar_sts'] = door_status['charge_port_status'][1]['ajar_status']
        data['tailgate_ajar_sts'] = door_status['tailgate_status']['ajar_status']
        data['engine_hood_ajar_sts'] = door_status['engine_hood_status']['ajar_status']
        data['vehicle_lock_status'] = door_status['vehicle_lock_status']

        return data

    def to_mysql_status_driving_behv(self, behaviour):
        data = {}

        data['id'] = self.vehicle_id
        data['sample_time'] = self.sample_time
        data['behv_type'] = behaviour

        return data

    def to_mysql_status_window(self, window_status):
        data = {}

        data['id'] = self.vehicle_id
        data['sample_time'] = self.sample_time

        # mysql不落库下面这些failure
        for f in ['win_frnt_ri_failure', 'win_frnt_ri_failure', 'win_re_le_failure', 'win_re_ri_failure']:
            window_status['window_positions'].pop(f, '')
        for f in ['sun_roof_failure', 'sun_roof_shade_failure']:
            window_status['sun_roof_positions'].pop(f, '')

        data.update(window_status['window_positions'])
        data.update(window_status['sun_roof_positions'])

        return data

    def to_mysql_status_light(self, light_status):
        data = {}

        data['id'] = self.vehicle_id
        data['sample_time'] = self.sample_time
        data['high_beam_on'] = light_status['hi_beam_on']
        data['low_beam_on'] = light_status['lo_beam_on']
        data['head_light_on'] = light_status['head_light_on']

        return data

    def to_mysql_status_heating(self, heating_status):
        data = copy.deepcopy(heating_status)
        data['id'] = self.vehicle_id
        data['sample_time'] = self.sample_time
        return data

    def to_mysql_status_nbs(self, nbs_status):
        data = copy.deepcopy(nbs_status)
        data['id'] = self.vehicle_id
        data['sample_time'] = self.sample_time
        return data

    def to_mysql_status_occupant(self, occupant_status):
        data = {}

        data['id'] = self.vehicle_id
        data['sample_time'] = self.sample_time

        data['fr_le_seat'] = occupant_status['fr_le_seat_occupant_status']
        data['fr_ri_seat'] = occupant_status['fr_ri_seat_occupant_status']

        return data

    # TODO update all func param with _item if it is list
    def to_mysql_status_driving_motor_data(self, driving_motor_data_item):
        data = copy.deepcopy(driving_motor_data_item)

        data['id'] = self.vehicle_id
        data['sample_time'] = self.sample_time
        data['drvmotr_contl_dc_bus_curnt'] = round(driving_motor_data_item['drvmotr_contl_dc_bus_curnt'], 1)

        return data

    def to_mysql_status_driving_motor(self, driving_motor):
        # data = copy.deepcopy(driving_motor)
        data = {}

        data['id'] = self.vehicle_id
        data['sample_time'] = self.sample_time
        data['drvmotr_qunty'] = len(driving_motor['motor_list'])
        data['pwr_sys_rdy'] = int(driving_motor['pwr_sys_rdy'])

        return data

    def to_mysql_status_extremum_data(self, extremum_data):
        data = copy.deepcopy(extremum_data)

        data['id'] = self.vehicle_id
        data['sample_time'] = self.sample_time
        data['sin_btry_lwst_volt'] = round(extremum_data['sin_btry_lwst_volt'], 3)
        data['sin_btry_hist_volt'] = round(extremum_data['sin_btry_hist_volt'], 3)

        return data

    def to_mysql_status_driving_data(self, driving_data):
        data = {}

        data['id'] = self.vehicle_id
        data['sample_time'] = self.sample_time
        data['aclrtn_pedal_posn'] = round(driving_data['aclrtn_pedal_posn'], 3)
        data['max_speed'] = round(driving_data['max_speed'], 1)
        data['min_speed'] = round(driving_data['min_speed'], 1)
        data['average_speed'] = round(driving_data['average_speed'], 1)
        data['steer_whl_rotn_ag'] = round(driving_data['steer_whl_rotn_ag'], 1)
        data['steer_whl_rotn_spd'] = driving_data['steer_whl_rotn_spd']
        data['veh_drvg_mod'] = driving_data['vcu_drvg_mod']
        data['brk_pedal_valid'] = driving_data['brk_pedal_sts']['valid']
        data['brk_pedal_state'] = driving_data['brk_pedal_sts']['state']
        data['dispd_spd'] = driving_data['veh_dispd_spd']
        data['outd_hum'] = driving_data['veh_outd_hum']
        data['dispd_spd_sts'] = driving_data['veh_dispd_spd_sts']

        return data

    def to_mysql_status_bms(self, bms_status):
        data = copy.deepcopy(bms_status)

        data['id'] = self.vehicle_id
        data['sample_time'] = self.sample_time
        data['avg_cell_volt'] = round(bms_status['avg_cell_volt'], 3)
        data['dischrg_pwr_lmt'] = round(bms_status['dischrg_pwr_lmt'], 1)
        data['chrg_pwr_lmt'] = round(bms_status['chrg_pwr_lmt'], 1)
        data['health_status'] = round(bms_status['health_status'], 1)

        return data

    def to_mysql_status_hvac(self, hvac_status):
        data = copy.deepcopy(hvac_status)

        data['id'] = self.vehicle_id
        data['sample_time'] = self.sample_time

        if hvac_status['air_con_on'] == 1 or hvac_status['ccu_cbn_pre_ac_ena_sts'] == 1:
            data['air_con_on'] = 1

        return data

    def to_mysql_status_can_msg(self, can_msg):
        data = copy.deepcopy(can_msg)

        data['id'] = self.vehicle_id
        data['sample_time'] = self.sample_time
        data['can_data'][0]['value'] = codecs.encode(can_msg['can_data'][0]['value'], 'hex').decode('ascii').upper()
        data['can_data'] = json.dumps(data['can_data']).replace(' ', '')

        return data

    def to_mysql_status_tyre(self, tyre_status):
        data = copy.deepcopy(tyre_status)

        data['id'] = self.vehicle_id
        data['sample_time'] = self.sample_time
        data['re_ri_whl_press'] = round(tyre_status['re_ri_whl_press'], 3)
        data['frnt_le_whl_press'] = round(tyre_status['frnt_le_whl_press'], 3)
        data['frnt_ri_whl_press'] = round(tyre_status['frnt_ri_whl_press'], 3)
        data['re_le_whl_press'] = round(tyre_status['re_le_whl_press'], 3)

        return data

    def to_mysql_status_did(self, did_data: list):
        data = []

        for i in range(len(did_data)):
            for j in range(len(did_data[i]['dids'])):
                d = {}
                d['ecu'] = did_data[i]['ecu']
                d['didid'] = did_data[i]['dids'][j]['id']
                d['value'] = did_data[i]['dids'][j]['value']
                ts = did_data[i]['dids'][j]['sample_ts']
                d['sample_time'] = str(datetime.utcfromtimestamp(int(ts) / 1000.0))
                data.append(d)

        return data

    def to_fota_mysql_vehicle_dids(self, did_data: list):
        # Fota Mysql的 vehicle_dids 表
        data = copy.deepcopy(did_data)
        for i in range(len(data)):
            for j in range(len(data[i]['dids'])):
                data[i]['dids'][j].pop('sample_ts')

        return data

    def to_mysql_status_wti_alarm(self, vin, alarm_signal_int: list = None, wti_accompany: list = None):
        data = []

        for i, item in enumerate(alarm_signal_int):
            wti_one = {}
            wti_one['id'] = self.vehicle_id
            wti_one['sample_time'] = self.sample_time
            wti_one['can_sn'] = int(item['sn'])
            wti_one['wti_code'] = wti_accompany[i]['wti_code']
            wti_one['alarm_level'] = wti_accompany[i]['alarm_level']
            wti_one['alarm_id'] = vin + '-' + item['sn'] + '-' + wti_accompany[i]['wti_code'][4:] + '-WTI'
            data.append(wti_one)
        return data

    def to_mysql_vehicle_alarm_process(self, vin, alarm_signal_int: list = None, wti_accompany=None):
        data = []
        for i, item in enumerate(alarm_signal_int):
            wti_one = {}
            wti_one['vehicle_id'] = self.vehicle_id
            wti_one['wti_code'] = wti_accompany[i]['wti_code']
            wti_one['alarm_id'] = vin + '-' + item['sn'] + '-' + wti_accompany[i]['wti_code'][4:] + '-WTI'
            wti_one['status'] = 1
            data.append(wti_one)
        return data

    def to_mysql_history_wti_alarm(self, vin, alarm_signal_int: dict = None, wti_accompany: list = None):
        data = []

        for i, item in enumerate(alarm_signal_int):
            wti_one = {}
            wti_one['vehicle_id'] = self.vehicle_id
            wti_one['start_time'] = timestamp_to_utc_strtime(item['sn'], adjust=True)
            wti_one['wti_code'] = wti_accompany[i]['wti_code']
            wti_one['wti_code'] = wti_accompany[i]['wti_code']
            wti_one['alarm_id'] = '{}-{}-{}-WTI'.format(vin, item['sn'], wti_accompany[i]['wti_code'][4:])
            wti_one['end_time'] = None
            data.append(wti_one)
        return data

    def to_mysql_svt_event(self, svt_obj):
        data = {}
        data['vehicle_id'] = self.vehicle_id
        data['sample_time'] = self.sample_time
        data['event_id'] = svt_obj['event_id'] // 1000
        data['reason_code'] = svt_obj['reason_code']

        data['svt_data'] = {}
        data['svt_data']['vehicle_status'] = {
            'vehicle_state': svt_obj['status']['vehicle_status']['vehl_state'],
            'charge_state': svt_obj['status']['vehicle_status']['chrg_state'],
            'operation_mode': svt_obj['status']['vehicle_status']['oprtn_mode'],
            'speed': round(svt_obj['status']['vehicle_status']['speed'], 1),
            'mileage': svt_obj['status']['vehicle_status']['mileage'],
            'total_voltage': round(svt_obj['status']['vehicle_status']['vehl_totl_volt'], 1),
            'total_current': round(svt_obj['status']['vehicle_status']['vehl_totl_curnt'], 1),
            'soc': svt_obj['status']['vehicle_status']['soc'],
            'dc_dc_status': svt_obj['status']['vehicle_status']['dc_dc_sts'],
            'gear': svt_obj['status']['vehicle_status']['gear'],
            'insulation_resistance': svt_obj['status']['vehicle_status']['insulatn_resis'],
            'urgent_power_shutdown': svt_obj['status']['vehicle_status']['urgt_prw_shtdwn'],
            'sample_time': svt_obj['sample_ts'] // 1000,
            'comf_ena': svt_obj['status']['vehicle_status']['comf_ena'],
            "ntester": svt_obj['status']['vehicle_status']['ntester'],
            "vehl_type_dbc": svt_obj['status']['vehicle_status']['vehl_type_dbc']
        }
        data['svt_data']['position_status'] = {
            "posng_valid_type": svt_obj['status']['position_status']['posng_valid_type'],
            "heading": svt_obj['status']['position_status']['heading'],
            "altitude": svt_obj['status']['position_status']['altitude'],
            "gps_speed": svt_obj['status']['position_status']['gps_speed'],
            "climb": svt_obj['status']['position_status']['climb'],
            "satellite_quantity": svt_obj['status']['position_status']['satellite']['quantity'],
            "gps_time": svt_obj['status']['position_status']['gps_ts'] // 1000,
            "longitude_uncertainty": svt_obj['status']['position_status']['longitude_uncertainty'],
            "latitude_uncertainty": svt_obj['status']['position_status']['latitude_uncertainty'],
            "altitude_uncertainty": svt_obj['status']['position_status']['altitude_uncertainty'],
            "sample_time": svt_obj['sample_ts'] // 1000,
            "mode": svt_obj['status']['position_status']['mode'],
            "fusion_mode": svt_obj['status']['position_status']['fusion_mode'],
        }
        gcj02_coord = wgs84_to_gcj02(svt_obj['status']['position_status']['longitude'],
                                     svt_obj['status']['position_status']['latitude'])

        data['svt_data']['position_status']['longitude'] = gcj02_coord[0]
        data['svt_data']['position_status']['latitude'] = gcj02_coord[1]

        data['svt_data']['pow_supply_source'] = svt_obj['status']['pow_supply_source']
        data['svt_data']['backup_battery_level'] = round(svt_obj['status']['backup_battery_level'], 3)
        data['svt_data']['gnss_ant_stats'] = svt_obj['status']['gnss_ant_stats']
        data['svt_data']['anti_theft_alarm'] = svt_obj['status']['anti_theft_alarm']

        return data

    def to_mysql_ecall_event(self, ecall_status, event_id, reason_code, alarm_signal, window_mysql, door_mysql, model_type=None, model_type_year=None):
        data = {}
        data['vehicle_id'] = self.vehicle_id
        data['sample_time'] = self.sample_time
        data['event_id'] = event_id
        data['reason_code'] = reason_code
        # 长期规划中除了MQTT，还有SMS 短信通知
        data['channel'] = 'MQTT'
        # https://jira.nioint.com/browse/CVS-17896
        # ecall推送增加字段判断内部车 rvs库vehicle_profile_info_extend.vehicle_identity
        data['vehicle_identity'] = 1

        data['ecall_data'] = {
            "mileage": ecall_status['vehicle_status']['mileage'],
            "heading": ecall_status['position_status']['heading'],
            "location_type": "gps",
            "gps_speed": ecall_status['position_status']['gps_speed'],
            "speed": round(ecall_status['vehicle_status']['speed'], 1),
            "remaining_mileage": ecall_status['soc_status']['remaining_range'],
            "airbag_pop_out": reason_code == 'airbag_pump_trigger',

        }

        if 'window_status' in ecall_status:
            win_posn = ecall_status['window_status']['window_positions']
            # 车窗数据报0的时候存0， 报1的时候也存0
            data['ecall_data']["win_frnt_le_posn"] = win_posn['win_frnt_le_posn'] if win_posn['win_frnt_le_posn'] != 1 else 0
            data['ecall_data']["win_re_ri_posn"] = win_posn['win_re_ri_posn'] if win_posn['win_re_ri_posn'] != 1 else 0
            data['ecall_data']["win_re_le_posn"] = win_posn['win_re_le_posn'] if win_posn['win_re_le_posn'] != 1 else 0
            data['ecall_data']["win_frnt_ri_posn"] = win_posn['win_frnt_ri_posn'] if win_posn['win_frnt_ri_posn'] != 1 else 0
            data['ecall_data']["sun_roof_shade_posn"] = ecall_status['window_status']['sun_roof_positions']['sun_roof_shade_posn']
            data['ecall_data']["sun_roof_posn"] = ecall_status['window_status']['sun_roof_positions']['sun_roof_posn']

        elif window_mysql:
            data['ecall_data']["win_frnt_le_posn"] = window_mysql['win_frnt_le_posn'] if window_mysql['win_frnt_le_posn'] != 1 else 0
            data['ecall_data']["win_re_ri_posn"] = window_mysql['win_re_ri_posn'] if window_mysql['win_re_ri_posn'] != 1 else 0
            data['ecall_data']["win_re_le_posn"] = window_mysql['win_re_le_posn'] if window_mysql['win_re_le_posn'] != 1 else 0
            data['ecall_data']["win_frnt_ri_posn"] = window_mysql['win_frnt_ri_posn'] if window_mysql['win_frnt_ri_posn'] != 1 else 0
            data['ecall_data']["sun_roof_shade_posn"] = window_mysql['sun_roof_shade_posn']
            data['ecall_data']["sun_roof_posn"] = window_mysql['sun_roof_posn']

        if model_type == 'EC6':
            data['ecall_data']["sun_roof_posn"] = 0
        elif (model_type_year == 'G1.F' and model_type == 'ES8') or model_type == 'ES6':
            posn = data['ecall_data']["sun_roof_posn"]
            map_new = {0: 126, 101: 0, 102: 126}
            if posn in map_new.keys():
                data['ecall_data']["sun_roof_posn"] = map_new[posn]
        else:
            sts = ecall_status['window_status']['sun_roof_positions']['sun_roof_posn_sts']
            m = {0: 126, 1: 126, 2: 126, 3: 0, 4: 'keep', 5: 'keep', 6: 100, 7: 127}
            if m[sts] != 'keep':
                data['ecall_data']["sun_roof_posn"] = m[sts]

        if 'door_status' in ecall_status:
            data['ecall_data']["tailgate_closed"] = ecall_status['door_status']['tailgate_status']['ajar_status'] == 0
            data['ecall_data']["door_re_le_sts"] = ecall_status['door_status']['door_ajars']['door_ajar_re_le_sts'] == 0
            data['ecall_data']["door_re_ri_sts"] = ecall_status['door_status']['door_ajars']['door_ajar_re_ri_sts'] == 0
            data['ecall_data']["door_frnt_ri_sts"] = ecall_status['door_status']['door_ajars']['door_ajar_frnt_ri_sts'] == 0
            data['ecall_data']["door_frnt_le_sts"] = ecall_status['door_status']['door_ajars']['door_ajar_frnt_le_sts'] == 0
        elif door_mysql:
            data['ecall_data']["tailgate_closed"] = door_mysql['tailgate_ajar_sts'] == 0
            data['ecall_data']["door_re_le_sts"] = door_mysql['door_ajar_re_le_sts'] == 0
            data['ecall_data']["door_re_ri_sts"] = door_mysql['door_ajar_re_ri_sts'] == 0
            data['ecall_data']["door_frnt_ri_sts"] = door_mysql['door_ajar_frnt_ri_sts'] == 0
            data['ecall_data']["door_frnt_le_sts"] = door_mysql['door_ajar_frnt_le_sts'] == 0

        gcj02_coord = wgs84_to_gcj02(ecall_status['position_status']['longitude'],
                                     ecall_status['position_status']['latitude'])

        data['ecall_data']['longitude'] = gcj02_coord[0]
        data['ecall_data']['latitude'] = gcj02_coord[1]

        # brake_fluid_min
        data['ecall_data']['brake_fluid_min'] = False
        for item in alarm_signal['signal_int']:
            if item['name'] == 'BrkFldWarnReq':
                data['ecall_data']['brake_fluid_min'] = True

        # tyre_alarm
        data['ecall_data']['tyre_alarm'] = []
        for item in alarm_signal['signal_int']:
            for x in TYRE_WIT_SIGNAL:
                if item['name'] == x['name']:
                    tmp = {
                        'description': x['description'],
                        'wti_code': x['wti_code'],
                        'start_time': int(item['sn'])
                    }
                    data['ecall_data']['tyre_alarm'].append(tmp)
                    break

        return data

    def to_mysql_status_lv_battery(self, lv_battery):
        data = {
            'vehicle_id': self.vehicle_id,
            'sample_time': self.sample_time,
            'lv_batt_soh_sul': lv_battery['lv_batt_soh_sul'],
            'lv_batt_soh_lam': lv_battery['lv_batt_soh_lam'],
            'lv_batt_soh_cor': lv_battery['lv_batt_soh_cor'],
            'lv_batt_soh_sul_sts': lv_battery['lv_batt_soh_sul_sts'],
            'lv_batt_soh_lam_sts': lv_battery['lv_batt_soh_lam_sts'],
            'lv_batt_soh_cor_sts': lv_battery['lv_batt_soh_cor_sts'],
            'lv_batt_soc': lv_battery['lv_batt_soc'],
            'lv_batt_soc_sts': lv_battery['lv_batt_soc_sts'],
            'lv_batt_customer_id': lv_battery['lv_batt_customer_id'],
        }
        return data

    def to_mysql_history_lv_battery(self, lv_battery):
        # sample_month、sample_week字段按照北京时间记录
        d = datetime.utcfromtimestamp(self.sample_ts / 1000 + 8 * 3600)
        data = {
            'vehicle_id': self.vehicle_id,
            'sample_time': self.sample_time,
            'lv_batt_soh_sul': lv_battery['lv_batt_soh_sul'],
            'lv_batt_soh_lam': lv_battery['lv_batt_soh_lam'],
            'lv_batt_soh_cor': lv_battery['lv_batt_soh_cor'],
            'lv_batt_soh_sul_sts': lv_battery['lv_batt_soh_sul_sts'],
            'lv_batt_soh_lam_sts': lv_battery['lv_batt_soh_lam_sts'],
            'lv_batt_soh_cor_sts': lv_battery['lv_batt_soh_cor_sts'],
            'lv_batt_soc': lv_battery['lv_batt_soc'],
            'lv_batt_soc_sts': lv_battery['lv_batt_soc_sts'],
            'lv_batt_customer_id': lv_battery['lv_batt_customer_id'],
            'sample_month': int(d.strftime('%Y%m')),
            'sample_week': d.isocalendar()[0] * 100 + d.isocalendar()[1]
        }
        return data

    def to_mysql_history_modem_event(self, modem_event):
        # sample_month、sample_week字段按照北京时间记录
        module_type = 1 if modem_event['module_type'] == 'toby' else 2
        data = {
            'vehicle_id': self.vehicle_id,
            'module_type': module_type,
            'event_type': modem_event['event_type'],
            'start_time': timestamp_to_utc_strtime(modem_event['event_detail']['start']['sample_ts']),
            'end_time': timestamp_to_utc_strtime(modem_event['event_detail']['end']['sample_ts']),
            'vehicle_state_s': modem_event['event_detail']['start']['vehicle_state'],
            'vehicle_state_e': modem_event['event_detail']['end']['vehicle_state'],
            'process_id_s': modem_event['event_detail']['start']['process_id'],
            'process_id_e': modem_event['event_detail']['end']['process_id'],
            'reason': modem_event['event_detail']['reason'],
            'soft_reset_times': modem_event['event_detail']['restore_reason']['soft_reset'],
            'graceful_reset_times': modem_event['event_detail']['restore_reason']['graceful_reset'],
            'hard_reset_times': modem_event['event_detail']['restore_reason']['hard_reset'],
            'emergency_switch_off_times': modem_event['event_detail']['restore_reason']['emergency_switch_off'],
            'sample_time': self.sample_time,
        }
        return data

    def to_mysql_vehicle_soc_history(self, power_data, event_name):
        data = dict()
        if event_name == 'power_swap_start':
            data = {
                'event_id': power_data['power_swap_id'],
                'start_battery_id': power_data['chg_subsys_encoding'],
                'start_time': self.sample_time,
                'start_energy': power_data['dump_enrgy'],
                'start_soc': power_data['soc'],
            }
        elif event_name == 'power_swap_end':
            data = {
                'event_id': power_data['power_swap_id'],
                'end_battery_id': power_data['chg_subsys_encoding'],
                'end_time': self.sample_time,
                'end_energy': power_data['dump_enrgy'],
                'end_soc': power_data['soc'],
                'status': int(power_data['is_success'])
            }
        elif event_name == 'power_swap_failure':
            data = {
                'event_id': power_data['power_swap_id'],
                'status': 1,
                'failure_info': {
                    'failure_count': str(power_data['failure_count']),
                    'fail_reason': power_data['fail_reason'],
                    'extend_info': power_data['extend_info'],
                }

            }
        elif event_name == 'charge_start_event':
            data = {
                'event_id': power_data['charge_id'],
                'start_battery_id': power_data['battery_package_info']['btry_pak_encoding'][0]['nio_encoding'],
                'end_battery_id': power_data['battery_package_info']['btry_pak_encoding'][0]['nio_encoding'],
                'start_time': self.sample_time,
                'start_energy': round(power_data['soc_status']['dump_enrgy'], 1),
                'start_soc': round(power_data['soc_status']['soc'], 1),
                'status': 1,
                'charger_type': power_data['charging_info']['charger_type'],
            }
        elif event_name == 'charge_end_event':
            data = {
                'event_id': power_data['charge_id'],
                'end_time': self.sample_time,
                'end_energy': round(power_data['soc_status']['dump_enrgy'], 1),
                'end_soc': round(power_data['soc_status']['soc'], 1),
                # 同一个charge_id的充电结束事件，如果上报多次，经纬度为第一次上报的，保持不变
                # 'longitude': longitude,
                # 'latitude': latitude,
                'is_end': 1,
            }
        return data

    def to_mysql_history_nfc_op(self, nfc_op):
        # d = datetime.fromtimestamp(self.sample_ts / 1000)
        data = {
            'vehicle_id': self.vehicle_id,
            'account_id': nfc_op['user_id'],
            'status': nfc_op['status'],
            'action': nfc_op['action'],
            'aid': nfc_op['aid'],
            'fail_reason': nfc_op['fail_reason'],
            'read_key_time': datetime.utcfromtimestamp(nfc_op['ts_read_key']).strftime('%Y-%m-%d %H:%M:%S'),
            'veri_key_time': datetime.utcfromtimestamp(nfc_op['ts_veri_key']).strftime('%Y-%m-%d %H:%M:%S'),
            'key_id': nfc_op['key_id'],
            'device_id': nfc_op['device_id'],
            'serial_number': nfc_op['cert_serial_number'],
            'extend_info': nfc_op['extend_info'],
        }
        return data

    def to_mysql_history_nkc_nfc_op(self, nfc_nfc_op):
        data = {
            'vehicle_id': self.vehicle_id,
            'account_id': nfc_nfc_op['user_id'],
            'status': nfc_nfc_op['status'],
            'action': nfc_nfc_op['action'],
            'aid': nfc_nfc_op['aid'],
            'fail_reason': nfc_nfc_op['fail_reason'],
            'read_key_time': datetime.utcfromtimestamp(nfc_nfc_op['ts_read_key']).strftime('%Y-%m-%d %H:%M:%S'),
            'key_id': nfc_nfc_op['key_id'],
            'device_id': nfc_nfc_op['device_id'],
            'cert_serial_number': nfc_nfc_op['cert_serial_number'],
            'extend_info': nfc_nfc_op['extend_info'],
            'time_consuming': nfc_nfc_op['time_consuming']
        }
        return data

    def to_mysql_history_ble_op(self, ble_op):
        data = {
            'status': ble_op['status'],
            'aid': ble_op['aid'],
            'action': str(ble_op['action']),
            'action_mode': ble_op['action_mode'],
            'conn_start_time': timestamp_to_utc_strtime(ble_op['conn_start_ts']),
            'conn_end_time': timestamp_to_utc_strtime(ble_op['conn_end_ts']),
            'read_key_time': timestamp_to_utc_strtime(ble_op['read_ts']),
            'veri_key_time': timestamp_to_utc_strtime(ble_op['verify_ts']),
            's_random': ble_op['s_random'],
            'device_id': ble_op['device_id'],
            'vehicle_id': self.vehicle_id,
            'device_rssi': ble_op['device_rssi'],
            'vehicle_rssi': ble_op['vehicle_rssi'],
            'action_latency': ble_op['action_latency'],
            'account_id': ble_op['user_id'] if ble_op['user_id'] else 0,
            'fail_reason': ble_op['fail_reason'],
            'key_id': ble_op['key_id'],
        }
        return data

    def to_mysql_status_car_key(self, car_key):
        data = {
            'vehicle_id': self.vehicle_id,
            'media_type': car_key['media_type'],
            'pas_switch_sts': car_key['current_pas_key_switch_sts'],
            'sample_time': timestamp_to_utc_strtime(car_key['sample_ts']),
        }
        return data

    def to_mysql_vehicle_data_mock(self, mock_data, platform, event_name, reissue=False):
        if 'start' in event_name:
            command = 1
        elif 'update' in event_name:
            if reissue == False:
                command = 2
            elif reissue == True:
                command = 3
        elif 'end' in event_name:
            command = 4
        data = {
            'vin': mock_data['id'],
            'command': command,
            'attribution': platform
        }
        return data

    def to_mysql_reportInfoList_in_message(self, mock_data):
        list = []
        data = {}
        vehl_state = mock_data['sample_points'][0]['vehicle_status']['vehl_state']
        data['vehicleState'] = vehl_state if vehl_state is not 4 else 3
        data['ChargeState'] = mock_data['sample_points'][0]['vehicle_status']['chrg_state']
        data['operationMode'] = mock_data['sample_points'][0]['vehicle_status']['oprtn_mode']
        data['speed'] = int(round(mock_data['sample_points'][0]['vehicle_status']['speed'], 1) * 10)
        data['mileage'] = mock_data['sample_points'][0]['vehicle_status']['mileage'] * 10
        data['vehicleTotalVoltage'] = round(mock_data['sample_points'][0]['vehicle_status']['vehl_totl_volt'] * 10)
        data['vehicleTotalCurrent'] = round((mock_data['sample_points'][0]['vehicle_status']['vehl_totl_curnt'] + 1000) * 10)
        data['soc'] = int(mock_data['sample_points'][0]['vehicle_status']['soc'])
        data['dcDcStatus'] = mock_data['sample_points'][0]['vehicle_status']['dc_dc_sts']
        drive_force = 1 if mock_data['sample_points'][0]['driving_data']['aclrtn_pedal_posn'] else 0
        brake_force = 1 if mock_data['sample_points'][0]['driving_data']['brk_pedal_sts']['state'] == 1 and \
                           mock_data['sample_points'][0]['driving_data']['brk_pedal_sts']['valid'] == 0 else 0
        value = (drive_force << 5) + (brake_force << 4)
        gear = mock_data['sample_points'][0]['vehicle_status']['gear']
        if gear == 0:
            value |= 0
        elif gear == 1:
            value |= 0xE
        elif gear == 2:
            value |= 0xD
        elif gear == 3:
            value |= 0xF
        else:
            value |= 0x07
        data['gear'] = value
        data['insulationResistance'] = mock_data['sample_points'][0]['vehicle_status']['insulatn_resis']
        list.append(data)
        return list

    def to_mysql_vehicle_journey_history(self, journey_start_message, journey_end_message, account_id):
        start_longitude, start_latitude = wgs84_to_gcj02(journey_start_message['position_status']['longitude'],
                                                         journey_start_message['position_status']['latitude'])
        end_longitude, end_latitude = wgs84_to_gcj02(journey_end_message['position_status']['longitude'],
                                                     journey_end_message['position_status']['latitude'])
        # 需要修改
        inputs = {
            "host": self.env['host']['tsp_in'],
            "method": "GET",
            "path": f'/api/1/in/data/vehicle/{self.vehicle_id}/journey/summary',
            "params": {
                "app_id": 10005,
                "lang": "zh-cn",
                "hash_type": "md5",
                "start_time": int(time.time()) - 10 * 60,
                "end_time": int(time.time()),
                "process_id": journey_start_message['journey_id'],
                "sign": ''
            }
        }
        result = hreq.request(self.env, inputs)
        end_mileage = journey_end_message['vehicle_status']['mileage'] if 'mileage' in journey_end_message['vehicle_status'] else result['data'][0]['end_mileage']
        end_soc = journey_end_message['soc_status'].get('soc') if 'soc' in journey_end_message['soc_status'] else result['data'][0]['end_soc']
        end_dump_energy = round(journey_end_message['soc_status']['dump_enrgy'], 1) if 'dump_enrgy' in journey_end_message['soc_status'] else result['data'][0]['end_dump_energy']
        data = {
            'vehicle_id': self.vehicle_id,
            'account_id': account_id,
            'journey_id': journey_start_message['journey_id'],
            'process_id': journey_start_message['journey_id'],
            'start_time': datetime.utcfromtimestamp(journey_start_message['sample_ts'] // 1000).strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': datetime.utcfromtimestamp(journey_end_message['sample_ts'] // 1000).strftime('%Y-%m-%d %H:%M:%S'),
            'start_soc': journey_start_message['soc_status']['soc'],
            'end_soc': end_soc,
            'start_dump_energy': round(journey_start_message['soc_status']['dump_enrgy'], 1),
            'end_dump_energy': end_dump_energy,
            'start_mileage': journey_start_message['vehicle_status']['mileage'],
            'end_mileage': end_mileage,
            'start_remaining_range': journey_start_message['soc_status']['remaining_range'],
            'end_remaining_range': journey_end_message['soc_status']['remaining_range'],
            'user_deleted': 0,
            # 'user_switch': 0,
            # 'rapid_swerve': 0,
            # 'rapid_deceleration': 0,
            # 'rapid_acceleration': 0,
            'is_end': 1,
            'start_longitude': round(start_longitude, 6),
            'start_latitude': round(start_latitude, 6),
            'end_longitude': round(end_longitude, 6),
            'end_latitude': round(end_latitude, 6),
        }
        return data

    def to_mysql_status_adas(self, feature_status_update):
        data = {}
        data['id'] = self.vehicle_id
        str_time = timestamp_to_utc_strtime(int(feature_status_update['FeatureStatusUpdate']['feature_status']['timestamp']) * 1000)
        data['feature_time'] = str_time if str_time[-7:] != '.000000' else str_time[:-7]
        data['sample_time'] = self.sample_time
        acc_np_sts = feature_status_update['FeatureStatusUpdate']['feature_status']['acc_np_sts']
        acc_np_map = {0: 0, 1: 0, 2: 0, 3: 1, 4: 0, 5: 2, 6: 2, 7: 0}
        data['np_status'] = acc_np_map[acc_np_sts]

        np_sts = feature_status_update['FeatureStatusUpdate']['feature_status']['nop_sts']
        nop_map = {0: 0, 1: 0, 2: 0, 3: 1, 4: 0, 5: 0, 6: 0, 7: 0}
        data['nop_status'] = nop_map[np_sts]

        return data

    def to_mysql_status_body(self, obj):
        data = obj['body_status']
        data['id'] = self.vehicle_id
        data['sample_time'] = self.sample_time
        return data

    def to_mysql_status_trip(self, obj):
        data = obj['trip_status']
        data['id'] = self.vehicle_id
        data['sample_time'] = self.sample_time
        return data


class MsgToCassandraFormator(object):
    def __init__(self, vehicle_id, sample_ts=None, cmdopt='test'):
        self.vehicle_id = vehicle_id
        self.sample_ts = datetime.utcfromtimestamp(sample_ts / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + 'Z' if sample_ts else None
        self.cmdopt = cmdopt

    def to_cassandra_history_did(self, did_update):
        data = []

        for i in range(len(did_update['did_data'])):
            for j in range(len(did_update['did_data'][i]['dids'])):
                d = {}
                d['ecu'] = did_update['did_data'][i]['ecu']
                d['did_id'] = did_update['did_data'][i]['dids'][j]['id']
                d['value'] = did_update['did_data'][i]['dids'][j]['value']
                ts = did_update['did_data'][i]['dids'][j]['sample_ts']
                d['sample_ts'] = datetime.utcfromtimestamp(ts / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + 'Z'
                data.append(d)

        return data

    def to_vehicle_data(self, obj, event_name, *args, **kwargs):
        if event_name == 'ecu_connection_status' and 'redis' in kwargs \
                and 'vid' in kwargs and 'cmdopt' in kwargs and 'latest_msg_type' in kwargs \
                and 'ecu_type' in kwargs and 'status' in kwargs and 'process_id' in kwargs:
            redis = kwargs['redis']
            data = {
                'vehicle_id': kwargs['vid'],
                'connection_status': {
                    'ecu_type': kwargs['ecu_type'],
                    'status': kwargs['status'],
                    'latest_msg_type': kwargs['latest_msg_type']
                },
                'msg_type': 'ecu_connection_status',
                'process_id': kwargs['process_id'],
                'sample_ts': timestamp_to_utc_strtime(kwargs['sample_ts'])[:-3] + 'Z'
            }
            if 'stg' in kwargs['cmdopt']:
                en = kwargs['cmdopt'].replace('stg', 'staging')
            else:
                en = kwargs['cmdopt']
            key_front = 'mp_remote_vehicle_' + en.split('_')[0] + ':vehicle_status:' + kwargs['vid'] \
                if 'marcopolo' in en else 'remote_vehicle_' + en + ':vehicle_status:' + kwargs['vid']

            position_key = key_front + ':PositionStatus'
            pos = json.loads(redis.get(position_key))

            data['position_status'] = {
                'altitude': pos['altitude'],
                'altitude_uncertainty': pos['altitude_uncertainty'],
                'attitude': None,
                'climb': pos['climb'],
                'climb_uncertainty': None,
                'fusion_mode': pos['fusion_mode'],
                'gps_speed': pos['gps_speed'],
                'gps_speed_uncertainty': None,
                'gps_ts': pos['gps_time'],
                'heading': pos['heading'],
                'latitude': None,
                'latitude_gcj02': round(pos['latitude'], 6),
                'latitude_uncertainty': pos['latitude_uncertainty'],
                'longitude': None,
                'longitude_gcj02': round(pos['longitude'], 6),
                'longitude_uncertainty': pos['longitude_uncertainty'],
                'mode': pos['mode'],
                'posng_valid_type': pos['posng_valid_type'],
                'satellite': None}
            soc_key = key_front + ':SocStatus'

            soc = json.loads(redis.get(soc_key))

            data['soc_status'] = {'btry_cap': soc['battery_cap'],
                                  'btry_pak_encoding': None,
                                  'btry_pak_lst': None,
                                  'btry_pak_sum': soc['battery_pack_sum'],
                                  'btry_qual_actvtn': soc['battery_qual_actvtn'],
                                  'chrg_final_soc': soc['charge_final_soc'],
                                  'chrg_state': soc['charge_state'],
                                  'dump_enrgy': soc['dump_energy'],
                                  'hivolt_btry_curnt': soc['hivolt_battery_current'],
                                  'realtime_power_consumption': soc['power_consumption'],
                                  'remaining_range': soc['remaining_range'],
                                  'sin_btry_hist_temp': soc.get('sin_battery_hist_temp', None),
                                  'sin_btry_lwst_temp': soc.get('sin_battery_lwst_temp', None),
                                  'soc': soc['soc'],
                                  'max_soc': soc['max_soc'],
                                  'lock_soc': soc['lock_soc'],
                                  'soc_lock_status': soc['soc_lock_status'],
                                  'v2l_status': soc.get('v2l_status', None)
                                  }

            ext_key = key_front + ':ExteriorStatus'
            ext = json.loads(redis.get(ext_key))

            data['vehicle_status'] = {'aclrtn_pedal_posn': None,
                                      'brk_pedal_state': None,
                                      'brk_pedal_valid': None,
                                      'chrg_state': ext['charge_state'],
                                      'comf_ena': ext['comf_ena'],
                                      'dc_dc_sts': ext['dc_dc_status'],
                                      'gear': ext['gear'],
                                      'insulatn_resis': ext['insulation_resistance'],
                                      'mileage': ext['mileage'],
                                      'ntester': ext['ntester'],
                                      'oprtn_mode': ext['operation_mode'],
                                      'soc': ext['soc'],
                                      'speed': ext['speed'],
                                      'thermal_keeping': None,
                                      'urgt_prw_shtdwn': ext['urgent_power_shutdown'],
                                      'vehl_state': ext['vehicle_state'],
                                      'vehl_totl_curnt': ext['total_current'],
                                      'vehl_totl_volt': ext['total_voltage'],
                                      'vehl_type_dbc': ext['vehl_type_dbc']}

            return data

        data = copy.deepcopy(obj)
        if 'version' in data:
            data.pop('version')
        if 'id' in data:
            data.pop('id')
        data['sample_ts'] = self.sample_ts
        data['vehicle_id'] = self.vehicle_id

        if 'vehicle_status' in data:
            data['vehicle_status']['vehl_totl_volt'] = round(data['vehicle_status']['vehl_totl_volt'], 1)
            data['vehicle_status']['vehl_totl_curnt'] = round(data['vehicle_status']['vehl_totl_curnt'], 1)
            data['vehicle_status']['speed'] = round(data['vehicle_status']['speed'], 1)
            data['vehicle_status']['aclrtn_pedal_posn'] = None
            data['vehicle_status']['brk_pedal_state'] = None
            data['vehicle_status']['brk_pedal_valid'] = None

        if 'soc_status' in data:
            data['soc_status']['btry_cap'] = round(data['soc_status']['btry_cap'], 1)
            data['soc_status']['hivolt_btry_curnt'] = round(data['soc_status']['hivolt_btry_curnt'], 1)
            data['soc_status']['dump_enrgy'] = round(data['soc_status']['dump_enrgy'], 1)

            data['soc_status']['btry_pak_lst'] = []
            for i, item in enumerate(data['soc_status'].get('btry_paks', [])):
                item['btry_pak_curnt'] = round(item['btry_pak_curnt'], 1)
                item['btry_pak_voltage'] = round(item['btry_pak_voltage'], 1)
                if 'sin_btry_voltage' in item:
                    item['sin_btry_volt_lst'] = item['sin_btry_voltage']
                    item.pop('sin_btry_voltage')
                data['soc_status']['btry_pak_lst'].append(item)
            data['soc_status'].pop('btry_paks')
            data['soc_status']['v2l_status'] = data['soc_status'].pop('soc_v2l_status')
            data['soc_status']['btry_pak_sum'] = len(data['soc_status']['btry_pak_lst'])
            data['soc_status']['btry_pak_encoding'] = None

        if 'battery_package_info' in data:
            for i, item in enumerate(data['battery_package_info'].get('btry_pak_health_status', [])):
                item['btry_pak_health_status'] = round(item['battery_health_status'], 1)
                item.pop('battery_health_status')
            data['btry_pak_info'] = data.pop('battery_package_info')
            if 'marcopolo' in self.cmdopt:
                data['btry_pak_info']['btry_pak_encoding'][0]['re_encoding'] = None
                data['btry_pak_info']['btry_pak_encoding'][0]['nio_encoding'] = data['btry_pak_info']['btry_pak_encoding'][0]['nio_encoding'][:27]

        if 'position_status' in data:
            if 'marcopolo' in self.cmdopt:
                data['position_status'] = None
            else:
                data['position_status']['satellite']['snr'] = [
                    round(data['position_status']['satellite']['snr'][0], 6),
                    round(data['position_status']['satellite']['snr'][1], 6)]
                gcj02_coord = wgs84_to_gcj02(data['position_status']['longitude'],
                                             data['position_status']['latitude'])
                data['position_status']['longitude_gcj02'] = round(gcj02_coord[0], 6)
                data['position_status']['latitude_gcj02'] = round(gcj02_coord[1], 6)

        if 'door_status' in data:
            data['door_status']['door_locks']['door_lock_fr_le_sts'] = data['door_status']['door_locks'].pop(
                'door_lock_frnt_le_sts')
            data['door_status']['door_locks']['door_lock_fr_ri_sts'] = data['door_status']['door_locks'].pop(
                'door_lock_frnt_ri_sts')
            data['door_status']['door_locks']['vehicle_lock_status'] = data['door_status'].pop('vehicle_lock_status')
            data['door_status']['door_ajars']['door_ajar_fr_le_sts'] = data['door_status']['door_ajars'].pop(
                'door_ajar_frnt_le_sts')
            data['door_status']['door_ajars']['door_ajar_fr_ri_sts'] = data['door_status']['door_ajars'].pop(
                'door_ajar_frnt_ri_sts')
            data['door_status']['charge_ports'] = data['door_status'].pop('charge_port_status')
            data['door_status']['tailgate_ajar_sts'] = data['door_status']['tailgate_status']['ajar_status']
            data['door_status'].pop('tailgate_status')
            data['door_status']['engine_hood_ajar_sts'] = data['door_status']['engine_hood_status']['ajar_status']
            data['door_status'].pop('engine_hood_status')

        if 'window_status' in data:
            data['window_status']['win_frnt_le_posn'] = data['window_status']['window_positions']['win_frnt_le_posn']
            data['window_status']['win_frnt_ri_posn'] = data['window_status']['window_positions']['win_frnt_ri_posn']
            data['window_status']['win_re_le_posn'] = data['window_status']['window_positions']['win_re_le_posn']
            data['window_status']['win_re_ri_posn'] = data['window_status']['window_positions']['win_re_ri_posn']
            data['window_status'].pop('window_positions')

            data['window_status']['sun_roof_posn'] = data['window_status']['sun_roof_positions']['sun_roof_posn']
            data['window_status']['sun_roof_shade_posn'] = data['window_status']['sun_roof_positions'][
                'sun_roof_shade_posn']
            data['window_status']['sun_roof_posn_sts'] = data['window_status']['sun_roof_positions'][
                'sun_roof_posn_sts']
            data['window_status'].pop('sun_roof_positions')

        if 'light_status' in data:
            pass

        if 'behaviour' in data:
            data['driving_behaviour'] = {}
            data['driving_behaviour']['behavior'] = data.pop('behaviour')

        if 'tyre_status' in data:
            data['tyre_status']['fr_le_whl_press'] = round(data['tyre_status']['frnt_le_whl_press'], 3)
            data['tyre_status']['fr_ri_whl_press'] = round(data['tyre_status']['frnt_ri_whl_press'], 3)
            data['tyre_status']['re_le_whl_press'] = round(data['tyre_status']['re_le_whl_press'], 3)
            data['tyre_status']['re_ri_whl_press'] = round(data['tyre_status']['re_ri_whl_press'], 3)
            data['tyre_status']['fr_le_whl_temp'] = data['tyre_status'].pop('frnt_le_whl_temp')
            data['tyre_status']['fr_ri_whl_temp'] = data['tyre_status'].pop('frnt_ri_whl_temp')
            data['tyre_status'].pop('frnt_le_whl_press')
            data['tyre_status'].pop('frnt_ri_whl_press')

        if 'extremum_data' in data:
            data['extremum_data']['sin_btry_hist_volt'] = round(data['extremum_data']['sin_btry_hist_volt'], 3)
            data['extremum_data']['sin_btry_lwst_volt'] = round(data['extremum_data']['sin_btry_lwst_volt'], 3)

        if 'driving_data' in data:
            data['driving_data']['veh_drvg_mod'] = data['driving_data'].pop('vcu_drvg_mod')
            data['driving_data']['max_speed'] = round(data['driving_data']['max_speed'], 1)
            data['driving_data']['min_speed'] = round(data['driving_data']['min_speed'], 1)
            data['driving_data']['average_speed'] = round(data['driving_data']['average_speed'], 1)
            data['driving_data']['steer_whl_rotn_ag'] = round(data['driving_data']['steer_whl_rotn_ag'], 1)
            data['driving_data']['aclrtn_pedal_posn'] = round(data['driving_data']['aclrtn_pedal_posn'], 3)
            data['driving_data']['brk_pedal_state'] = data['driving_data']['brk_pedal_sts']['state']
            data['driving_data']['brk_pedal_valid'] = data['driving_data']['brk_pedal_sts']['valid']
            data['driving_data'].pop('brk_pedal_sts')
            data['driving_data']['dispd_spd'] = data['driving_data'].pop('veh_dispd_spd')
            data['driving_data']['outd_hum'] = data['driving_data'].pop('veh_outd_hum')
            data['driving_data']['dispd_spd_sts'] = data['driving_data'].pop('veh_dispd_spd_sts')

        if 'driving_motor' in data:
            data['driving_motor_status'] = data.pop('driving_motor')
            data['driving_motor_status']['driving_motors'] = data['driving_motor_status'].pop('motor_list')
            data['driving_motor_status']['drvmotr_qunty'] = len(data['driving_motor_status']['driving_motors'])

            for item in data['driving_motor_status']['driving_motors']:
                item['drvmotr_contl_dc_bus_curnt'] = round(item['drvmotr_contl_dc_bus_curnt'], 1)

        if 'can_msg' in data:
            if 'can_data' in data['can_msg']:
                for item in data['can_msg']['can_data']:
                    if isinstance(item['value'], bytes):
                        value = item['value']
                    elif isinstance(item['value'], str):
                        value = bytes.fromhex(item['value'])
                    assert item['value'] == value
                    item['value'] = codecs.encode(item['value'], 'hex').decode('ascii').upper()
            else:
                data['can_msg']['can_data'] = []
            if 'can_news' in data['can_msg']:
                for item in data['can_msg']['can_news']:
                    can_data = {'msg_id': item['msg_id'], 'value': ''}
                    for it in item['value']:
                        if isinstance(it, bytes):
                            value = it
                        elif isinstance(it, str):
                            value = bytes.fromhex(it)
                        assert it == value
                        can_data['value'] += codecs.encode(it, 'hex').decode('ascii').upper()
                    data['can_msg']['can_data'].append(can_data)
                data['can_msg'].pop('can_news')

        if 'can_signal' in data:
            for item in data['can_signal']['signal_info']:
                for it in item['data_info']:
                    it['value'] = '0x' + codecs.encode(it.pop('data'), 'hex').decode('ascii')
                item['can_data'] = item.pop('data_info')
            data['can_signal']['can_signal_info'] = data['can_signal'].pop('signal_info')
            data['can_signal']['can_sample_ts'] = timestamp_to_utc_strtime(data['can_signal'].pop('sample_ts'))[:-3] + 'Z'

        if 'can_msg_list' in data:
            for can_msg in data['can_msg_list']:
                for item in can_msg['can_data']:
                    can_data = CAN_DATA[str(item['msg_id'])]
                    if isinstance(can_data['value'], bytes):
                        value = can_data['value']
                    elif isinstance(can_data['value'], str):
                        value = bytes.fromhex(can_data['value'])
                    assert item['value'] == value
                    item['value'] = codecs.encode(item['value'], 'hex').decode('ascii').upper()

        if 'hvac_status' in data:
            if data['hvac_status']['air_con_on'] == 1 or data['hvac_status']['ccu_cbn_pre_ac_ena_sts'] == 1:
                data['hvac_status']['air_con_on'] = True
            else:
                data['hvac_status']['air_con_on'] = False

        if 'alarm_data' in data:
            # alarm_data存到cassandra里的re_alarm_data里，
            data['re_alarm_data'] = {}
            data['re_alarm_data']['common_alarm'] = {}
            for item in obj['alarm_data'].get('common_failure', []):
                if item['alarm_level'] == 255:
                    data['re_alarm_data']['common_alarm'][str(item['alarm_tag'])] = -1
                elif item['alarm_level'] == 254:
                    data['re_alarm_data']['common_alarm'][str(item['alarm_tag'])] = -2
                else:
                    data['re_alarm_data']['common_alarm'][str(item['alarm_tag'])] = item['alarm_level']

            data['re_alarm_data']['alarm_extension_bj'] = {}
            for item in obj['alarm_data'].get('bj_extension', []):
                if item['alarm_level'] == 255:
                    data['re_alarm_data']['alarm_extension_bj'][str(item['alarm_tag'])] = -1
                elif item['alarm_level'] == 254:
                    data['re_alarm_data']['alarm_extension_bj'][str(item['alarm_tag'])] = -2
                else:
                    data['re_alarm_data']['alarm_extension_bj'][str(item['alarm_tag'])] = item['alarm_level']

            data['re_alarm_data']['alarm_extension_sh'] = {}
            for item in obj['alarm_data'].get('sh_extension', []):
                if item['alarm_level'] == 255:
                    data['re_alarm_data']['alarm_extension_sh'][str(item['alarm_tag'])] = -1
                elif item['alarm_level'] == 254:
                    data['re_alarm_data']['alarm_extension_sh'][str(item['alarm_tag'])] = -2
                else:
                    data['re_alarm_data']['alarm_extension_sh'][str(item['alarm_tag'])] = item['alarm_level']

            data.pop('alarm_data')

        if 'alarm_signal' in data:
            data['alarm_data'] = {}
            data['alarm_data']['signal_info'] = []

            if 'signal_int' in data['alarm_signal']:
                for item in data['alarm_signal']['signal_int']:
                    tmp = {'alarm_sn': item['sn'], 'name': item['name'], 'value': item['value']}
                    data['alarm_data']['signal_info'].append(tmp)

            if 'signal_float' in data['alarm_signal']:
                for item in data['alarm_signal']['signal_float']:
                    tmp = {'alarm_sn': item['sn'], 'name': item['name'], 'value': item['value']}
                    data['alarm_data']['signal_info'].append(tmp)

            data.pop('alarm_signal')

        if 'signal_status' in data:
            data.pop('signal_status')

        if 'charging_info' in data:
            if 'in_curnt_ac' in data['charging_info']:
                data['charging_info']['in_curnt_ac'] = round(data['charging_info']['in_curnt_ac'], 1)

        if 'pre_cgw_log_info' in data:
            for item in data['pre_cgw_log_info']:
                item['sample_ts'] = datetime.utcfromtimestamp(item['sample_ts'] / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + 'Z'
                item['cgw_log_voltage'] = item.pop('cgw_log_volatage')
            data['lv_batt_charging_status'] = dict()
            data['lv_batt_charging_status']['pre_cgw_log_info'] = data.pop('pre_cgw_log_info')
            data['lv_batt_charging_status']['cgw_log_soc'] = data.pop('cgw_log_soc')
            data['lv_batt_charging_status']['cgw_log_voltage'] = data.pop('cgw_log_voltage')
            data['lv_batt_charging_status']['event_id'] = data.pop('event_id')
            data['lv_batt_charging_status']['event_num'] = data.pop('event_num')

        if 'veh_elec_cns' in data and 'veh_elecc_cns_resd' in data:
            for item in data['veh_elec_cns']:
                item['bms_customer_usage'] = round(item.pop('BMSCustomerUsage'), 1)
                item['veh_elec_cns'] = round(item.pop('VehElecCns'), 1)
                item['veh_remaining_eyg'] = round(item.pop('VehRemainingEyg'), 1)
                item['sample_ts'] = datetime.utcfromtimestamp(item['sample_ts'] / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + 'Z'
            for item in data['veh_elecc_cns_resd']:
                item['bms_customer_usage'] = round(item.pop('BMSCustomerUsage'), 1)
                item['veh_elec_cns'] = round(item.pop('VehElecCns'), 1)
                item['veh_remaining_eyg'] = round(item.pop('VehRemainingEyg'), 1)
                item['sample_ts'] = datetime.utcfromtimestamp(item['sample_ts'] / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + 'Z'
            data['vehicle_energy_status'] = dict()
            data['vehicle_energy_status']['veh_elec_cns'] = data.pop('veh_elec_cns')
            data['vehicle_energy_status']['veh_elec_cns_resd'] = data.pop('veh_elecc_cns_resd')

        if 'did_info' in data:
            data['bms_did_info'] = data.pop('did_info')

        if 'bms_status' in data:
            data['bms_status']['health_status'] = round(data['bms_status']['health_status'], 1)
            data['bms_status']['chrg_pwr_lmt'] = round(data['bms_status']['chrg_pwr_lmt'], 1)
            data['bms_status']['dischrg_pwr_lmt'] = round(data['bms_status']['dischrg_pwr_lmt'], 1)
            data['bms_status']['avg_cell_volt'] = round(data['bms_status']['avg_cell_volt'], 3)

        if 'power_swap_periodic' in data:
            data['power_swap_status'] = data.pop('power_swap_periodic')

        if 'power_swap_event' in data:
            data['power_swap_status'] = data.pop('power_swap_event')

        if 'power_swap_service_window_position' in data:
            data['window_status'] = data.pop('power_swap_service_window_position')
            del data['window_status']['win_frnt_le_failure']
            del data['window_status']['win_frnt_ri_failure']
            del data['window_status']['win_re_le_failure']
            del data['window_status']['win_re_ri_failure']

        if 'trip_status' in data:
            data['trip_status']['account_id'] = data['trip_status'].pop('user_id')

        return data

    def to_vehicle_history(self, obj, event_name):
        return self.to_vehicle_data(obj, event_name)

    def to_driving_data(self, obj):
        data = {}
        data['sample_ts'] = self.sample_ts
        data['dump_enrgy'] = round(obj['soc_status']['dump_enrgy'], 1)
        data['mileage'] = obj['vehicle_status']['mileage']

        if 'marcopolo' in self.cmdopt:
            data['position'] = None
            data['posng_valid_type'] = None
        else:
            data['position'] = {}
            gcj02_coord = wgs84_to_gcj02(obj['position_status']['longitude'],
                                         obj['position_status']['latitude'])
            data['position']['latitude'] = round(gcj02_coord[1], 6)
            data['position']['longitude'] = round(gcj02_coord[0], 6)
            data['position']['altitude'] = obj['position_status']['altitude']
            data['posng_valid_type'] = obj['position_status']['posng_valid_type']
        data['soc'] = obj['soc_status']['soc']
        data['realtime_power_consumption'] = obj['soc_status']['realtime_power_consumption']
        data['speed'] = round(obj['vehicle_status']['speed'], 1)
        if 'nio_pilot_sts' in obj:
            data['nio_pilot_sts'] = obj['nio_pilot_sts']
        if 'version' in obj and obj['version'] > 17:
            if 'trip_status' in obj:
                data['process_id'] = obj['trip_status']['trip_id']
                data['trip_odometer'] = obj['trip_status']['trip_odometer']
            elif 'process_id' in obj:
                data['process_id'] = obj['process_id']
            elif 'charge_id' in obj:
                data['process_id'] = obj['charge_id']
        return data

    def to_evm_message(self, obj, event_name, domain, platform, reissue=False):
        data = {}
        data['vin'] = obj['id']
        data['attribution'] = int(platform)
        data['domain'] = domain
        data['ack'] = 1
        if 'start' in event_name:
            data['type'] = 1
        elif 'update' in event_name:
            if reissue == False:
                data['type'] = 2
            elif reissue == True:
                data['type'] = 3
        elif 'end' in event_name:
            data['type'] = 4
        return data

    def to_reportInfoList_in_message(self, obj):
        list = []
        data = {}
        vehl_state = obj['sample_points'][0]['vehicle_status']['vehl_state']
        data['vehicleState'] = vehl_state if vehl_state is not 4 else 3
        data['ChargeState'] = obj['sample_points'][0]['vehicle_status']['chrg_state']
        data['operationMode'] = obj['sample_points'][0]['vehicle_status']['oprtn_mode']
        data['speed'] = int(round(obj['sample_points'][0]['vehicle_status']['speed'], 1) * 10)
        data['mileage'] = obj['sample_points'][0]['vehicle_status']['mileage'] * 10
        data['vehicleTotalVoltage'] = round(obj['sample_points'][0]['vehicle_status']['vehl_totl_volt'] * 10)
        data['vehicleTotalCurrent'] = round((obj['sample_points'][0]['vehicle_status']['vehl_totl_curnt'] + 1000) * 10)
        data['soc'] = int(obj['sample_points'][0]['vehicle_status']['soc'])
        data['dcDcStatus'] = obj['sample_points'][0]['vehicle_status']['dc_dc_sts']
        drive_force = 1 if obj['sample_points'][0]['driving_data']['aclrtn_pedal_posn'] else 0
        brake_force = 1 if obj['sample_points'][0]['driving_data']['brk_pedal_sts']['state'] == 1 and \
                           obj['sample_points'][0]['driving_data']['brk_pedal_sts']['valid'] == 0 else 0
        value = (drive_force << 5) + (brake_force << 4)
        gear = obj['sample_points'][0]['vehicle_status']['gear']
        if gear == 0:
            value |= 0
        elif gear == 1:
            value |= 0xE
        elif gear == 2:
            value |= 0xD
        elif gear == 3:
            value |= 0xF
        else:
            value |= 0x07
        data['gear'] = value
        data['insulationResistance'] = obj['sample_points'][0]['vehicle_status']['insulatn_resis']
        data['info_body'] = "com.nextev.ev_monitoring.evm_server.bean.realtime_info.info_body.VehicleStatusInfo"
        list.append(data)
        return list


class MsgToMongodbFormator(object):
    def __init__(self, vehicle_id, sample_ts=None):
        self.vehicle_id = vehicle_id
        self.sample_ts = sample_ts if sample_ts else None

    def to_vehicle_position(self, position_status):
        data = {'_id': self.vehicle_id,
                'timestamp': self.sample_ts,
                'location': []}
        gcj02_coord = wgs84_to_gcj02(position_status['longitude'],
                                     position_status['latitude'])
        data['location'].extend([round(gcj02_coord[0], 6), round(gcj02_coord[1], 6)])

        return data

    def to_can_msg(self, can_msg_item):
        can_msg_item_in_obj = {
            '_id': self.vehicle_id + '_' + str(can_msg_item['msg_id']),
            'vehicle_id': self.vehicle_id,
            'timestamp': self.sample_ts,
            'msg_id': can_msg_item['msg_id'],
        }

        can_data = CAN_DATA[str(can_msg_item['msg_id'])]
        assert can_msg_item['value'] == can_data['value']
        can_msg_item_in_obj['value'] = json.loads(can_data['pasted_value'])

        return can_msg_item_in_obj


class MsgToRedisFormator(object):
    def __init__(self, vehicle_id, sample_ts=None):
        self.vehicle_id = vehicle_id
        self.sample_ts = sample_ts if sample_ts else None

    def to_position_status(self, position_status, env='test'):
        if 'marcopolo' in env:
            gcj02_longitude, gcj02_latitude = position_status['longitude'], position_status['latitude']
        else:
            gcj02_longitude, gcj02_latitude = wgs84_to_gcj02(position_status['longitude'], position_status['latitude'])
        data = {
            'posng_valid_type': position_status.get('posng_valid_type'),
            'longitude': gcj02_longitude if position_status.get('longitude') else None,
            'latitude': gcj02_latitude if position_status.get('latitude') else None,
            'heading': position_status.get('heading'),
            'altitude': position_status.get('altitude'),
            'gps_speed': position_status.get('gps_speed'),
            'climb': position_status.get('climb'),
            'satellite_quantity': position_status.get('satellite', {}).get('quantity'),
            'gps_time': position_status['gps_ts'] // 1000 if position_status.get('gps_ts') else None,
            'longitude_uncertainty': position_status.get('longitude_uncertainty'),
            'latitude_uncertainty': position_status.get('latitude_uncertainty'),
            'altitude_uncertainty': position_status.get('altitude_uncertainty'),
            'sample_time': self.sample_ts // 1000,
            'mode': position_status.get('mode'),
            'fusion_mode': position_status.get('fusion_mode')
        }

        return data

    def to_door_status(self, door_status):
        data = {"door_lock_front_left_status": door_status.get('door_locks', {}).get('door_lock_frnt_le_sts'),
                "door_lock_front_right_status": door_status.get('door_locks', {}).get('door_lock_frnt_ri_sts'),
                "door_ajar_front_left_status": door_status.get('door_ajars', {}).get('door_ajar_frnt_le_sts'),
                "door_ajar_front_right_status": door_status.get('door_ajars', {}).get('door_ajar_frnt_ri_sts'),
                "door_ajar_rear_left_status": door_status.get('door_ajars', {}).get('door_ajar_re_le_sts'),
                "door_ajar_rear_right_status": door_status.get('door_ajars', {}).get('door_ajar_re_ri_sts'),
                "first_charge_port_ajar_status": door_status.get('charge_port_status', [{}, {}])[0].get('ajar_status'),
                "second_charge_port_ajar_status": door_status.get('charge_port_status', [{}, {}])[1].get('ajar_status'),
                "tailgate_ajar_status": door_status.get('tailgate_status', {}).get('ajar_status'),
                "engine_hood_ajar_status": door_status.get('engine_hood_status', {}).get('ajar_status'),
                "vehicle_lock_status": door_status.get('vehicle_lock_status'),
                "sample_time": self.sample_ts // 1000}

        return data

    def to_driving_data(self, driving_data):
        data = {"veh_drvg_mod": driving_data.get('vcu_drvg_mod'),
                "steer_whl_rotn_ag": round(driving_data.get('steer_whl_rotn_ag', None), 1),
                "steer_whl_rotn_spd": driving_data.get('steer_whl_rotn_spd'),
                "aclrtn_pedal_posn": round(driving_data.get('aclrtn_pedal_posn', None), 3),
                "brk_pedal_state": driving_data.get('brk_pedal_sts', {}).get('state'),
                "brk_pedal_valid": driving_data.get('brk_pedal_sts', {}).get('valid'),
                "average_speed": str(int(driving_data['average_speed'])) if 'average_speed' in driving_data else None,
                "max_speed": str(int(driving_data['max_speed'])) if 'max_speed' in driving_data else None,
                "min_speed": str(int(driving_data['min_speed'])) if 'min_speed' in driving_data else None,
                "dispd_speed": driving_data.get('veh_dispd_spd', None),
                "outd_hum": driving_data.get('veh_outd_hum', None),
                "dispd_spd_sts": driving_data.get('veh_dispd_spd_sts', None),
                "sample_time": self.sample_ts // 1000}

        return data

    def to_tyre_status(self, tyre_status):
        data = {"front_left_wheel_press": round(tyre_status.get('frnt_le_whl_press', None), 3),
                "front_right_wheel_press": round(tyre_status.get('frnt_ri_whl_press', None), 3),
                "rear_left_wheel_press": round(tyre_status.get('re_le_whl_press', None), 3),
                "rear_right_wheel_press": round(tyre_status.get('re_ri_whl_press', None), 3),
                "rear_right_wheel_temp": tyre_status.get('re_ri_whl_temp'),
                "rear_left_wheel_temp": tyre_status.get('re_le_whl_temp'),
                "front_left_wheel_temp": tyre_status.get('frnt_le_whl_temp'),
                "front_right_wheel_temp": tyre_status.get('frnt_ri_whl_temp'),
                "sample_time": self.sample_ts // 1000}

        return data

    def to_occupant_status(self, occupant_status):
        data = {"fr_le_seat_occupant_status": occupant_status.get('fr_le_seat_occupant_status'),
                "fr_ri_seat_occupant_status": occupant_status.get('fr_ri_seat_occupant_status'),
                "sample_time": self.sample_ts // 1000}

        return data

    def to_bms_status(self, bms_status):
        data = {"id": self.vehicle_id,
                "isolation_level": bms_status.get('isolation_level'),
                "health_status": str(int(bms_status['health_status'])) if 'health_status' in bms_status else None,
                "chrg_pwr_lmt": str(int(bms_status['chrg_pwr_lmt'])) if 'chrg_pwr_lmt' in bms_status else None,
                "dischrg_pwr_lmt": str(int(bms_status['dischrg_pwr_lmt'])) if 'dischrg_pwr_lmt' in bms_status else None,
                "avg_cell_volt": str(int(bms_status['avg_cell_volt'])) if 'avg_cell_volt' in bms_status else None,
                "avg_temp": str(int(bms_status['avg_temp'])) if 'avg_temp' in bms_status else None,
                "in_coolant_temp": str(int(bms_status['in_coolant_temp'])) if 'in_coolant_temp' in bms_status else None,
                "out_coolant_temp": str(int(bms_status['out_coolant_temp'])) if 'out_coolant_temp' in bms_status else None,
                "sample_time": self.sample_ts // 1000
                }

        return data

    def to_soc_status(self, soc_battery_charge_dict):
        data = {"vehicle_id": self.vehicle_id,
                "battery_id": soc_battery_charge_dict.get('battery_package_info', {}).get('btry_pak_encoding', [{}])[0].get('nio_encoding', None),
                "soc": soc_battery_charge_dict.get('soc_status', {}).get('soc', None),
                "charge_state": soc_battery_charge_dict.get('soc_status', {}).get('chrg_state', None),
                "battery_cap": str(int(soc_battery_charge_dict['soc_status']['btry_cap'])) if 'btry_cap' in soc_battery_charge_dict.get('soc_status', {}) else None,
                "estimate_charge_time": soc_battery_charge_dict.get('charging_info', {}).get('estimate_chrg_time', None),
                "hivolt_battery_current": str(int(soc_battery_charge_dict['soc_status']['hivolt_btry_curnt'])) if 'hivolt_btry_curnt' in soc_battery_charge_dict.get('soc_status',
                                                                                                                                                                     {}) else None,
                "battery_pack_sum": len(soc_battery_charge_dict['soc_status']['btry_paks']) if type(
                    soc_battery_charge_dict.get('soc_status', {}).get('btry_paks')) is list else None,
                "dump_energy": str(int(soc_battery_charge_dict['soc_status']['dump_enrgy'])) if 'dump_enrgy' in soc_battery_charge_dict.get('soc_status', {}) else None,
                # 一下两个字段暂时不校验，等开发修复，app没有用到
                "sin_battery_hist_temp": None,
                # soc_battery_charge_dict.get('soc_status',{}).get('sin_btry_hist_temp') if soc_battery_charge_dict.get('soc_status',{}).get('sin_btry_hist_temp') else None,
                "sin_battery_lwst_temp": None,
                # soc_battery_charge_dict.get('soc_status',{}).get('sin_btry_lwst_temp') if soc_battery_charge_dict.get('soc_status',{}).get('sin_btry_lwst_temp') else None,
                "battery_qual_actvtn": soc_battery_charge_dict.get('soc_status', {}).get('btry_qual_actvtn', None),
                "power_consumption": soc_battery_charge_dict.get('soc_status', {}).get('realtime_power_consumption', None),
                "charger_type": soc_battery_charge_dict.get('charging_info', {}).get('charger_type', None),
                "remaining_range": soc_battery_charge_dict.get('soc_status', {}).get('remaining_range', 0.0),
                "charge_final_soc": soc_battery_charge_dict.get('soc_status', {}).get('chrg_final_soc', None),
                "in_volt_ac": handle_zero(soc_battery_charge_dict.get('charging_info', {}).get('in_volt_ac', None)),
                "in_volt_dc": handle_zero(soc_battery_charge_dict.get('charging_info', {}).get('in_volt_dc', None)),
                "in_curnt_ac": handle_zero(soc_battery_charge_dict.get('charging_info', {}).get('in_curnt_ac', None)),
                "max_soc": soc_battery_charge_dict.get('soc_status', {}).get('max_soc', 0.0),
                "lock_soc": soc_battery_charge_dict.get('soc_status', {}).get('lock_soc', 0.0),
                "soc_lock_status": soc_battery_charge_dict.get('soc_status', {}).get('soc_lock_status', 0),
                "v2l_status": soc_battery_charge_dict.get('soc_status', {}).get('soc_v2l_status', None),
                "sample_time": self.sample_ts // 1000,
                "btry_pak_lst": [
                    {"btry_pak_sn": soc_battery_charge_dict.get('soc_status', {}).get('btry_paks', [{}])[0].get('btry_pak_sn', None),
                     "chgSubsysEncoding": soc_battery_charge_dict.get('battery_package_info', {}).get('btry_pak_encoding', [{}])[0].get('nio_encoding', None),
                     "gb_encoding": soc_battery_charge_dict.get('battery_package_info', {}).get('btry_pak_encoding', [{}])[0].get('re_encoding', None),
                     "btry_pak_voltage": str(int(soc_battery_charge_dict['soc_status']['btry_paks'][0]['btry_pak_voltage'])) if 'btry_pak_voltage' in
                                                                                                                                soc_battery_charge_dict.get('soc_status', {}).get(
                                                                                                                                    'btry_paks', [{}])[
                                                                                                                                    0] else None,
                     "btry_pak_curnt": str(int(soc_battery_charge_dict['soc_status']['btry_paks'][0]['btry_pak_curnt'])) if 'btry_pak_curnt' in
                                                                                                                            soc_battery_charge_dict.get('soc_status', {}).get(
                                                                                                                                'btry_paks', [{}])[
                                                                                                                                0] else None,
                     "sin_btry_qunty_of_pak": soc_battery_charge_dict.get('soc_status', {}).get('btry_paks', [{}])[0].get('sin_btry_qunty_of_pak', None),
                     "frm_start_btry_sn": soc_battery_charge_dict.get('soc_status', {}).get('btry_paks', [{}])[0].get('frm_start_btry_sn', None),
                     "sin_btry_qunty_of_frm": soc_battery_charge_dict.get('soc_status', {}).get('btry_paks', [{}])[0].get('sin_btry_qunty_of_frm', None),
                     "sin_btry_volt_lst": soc_battery_charge_dict.get('soc_status', {}).get('btry_paks', [{}])[0].get('sin_btry_voltage', None),
                     "temp_prb_qunty": soc_battery_charge_dict.get('soc_status', {}).get('btry_paks', [{}])[0].get('temp_prb_qunty', None),
                     "prb_temp_lst": soc_battery_charge_dict.get('soc_status', {}).get('btry_paks', [{}])[0].get('prb_temp_lst', None),
                     "btry_pak_hist_temp": soc_battery_charge_dict.get('soc_status', {}).get('btry_paks', [{}])[0].get('btry_pak_hist_temp', None),
                     "btry_pak_lwst_temp": soc_battery_charge_dict.get('soc_status', {}).get('btry_paks', [{}])[0].get('btry_pak_lwst_temp', None)
                     }
                ]
                }
        if 'battery_pack_cap' in soc_battery_charge_dict['soc_status']:
            data["battery_pack_cap"] = soc_battery_charge_dict['soc_status']['battery_pack_cap']
        if 'chrg_req' in soc_battery_charge_dict['soc_status']:
            data["chrg_req"] = soc_battery_charge_dict['soc_status']['chrg_req']
        if 'charging_current' in soc_battery_charge_dict['soc_status']:
            data["charging_current"] = soc_battery_charge_dict['soc_status']['charging_current']
        if 'charging_voltage' in soc_battery_charge_dict['soc_status']:
            data["charging_voltage"] = soc_battery_charge_dict['soc_status']['charging_voltage']
        if 'charging_power' in soc_battery_charge_dict['soc_status']:
            data["charging_power"] = soc_battery_charge_dict['soc_status']['charging_power']
        return data

    def to_hvac_status(self, hvac_status):
        data = {"temperature": hvac_status.get('amb_temp_c', None),
                "outside_temperature": hvac_status.get('outside_temp_c', None),
                "air_conditioner_on": hvac_status.get('air_con_on', None),
                "pm_2p5_cabin": hvac_status.get('pm_2p5_cabin', None),
                "pm_2p5_filter_active": hvac_status.get('pm_2p5_filter_active', None),
                "cbn_pre_sts": hvac_status.get('cbn_pre_sts', None),
                "ccu_cbn_pre_ac_ena_sts": hvac_status.get('ccu_cbn_pre_ac_ena_sts', None),
                "ccu_cbn_pre_aqs_ena_sts": hvac_status.get('ccu_cbn_pre_aqs_ena_sts', None),
                "cbn_hi_t_dry_sts": hvac_status.get('cbn_hi_t_dry_sts', None),
                "ccu_max_defrst_sts": hvac_status.get('ccu_max_defrst_sts', None),
                "sample_time": self.sample_ts // 1000
                }
        if data.get('air_conditioner_on') is not None:
            if data['ccu_cbn_pre_ac_ena_sts']:
                data['air_conditioner_on'] = True
        return data

    def to_vehicle_status(self, vehicle_status):
        data = {"vehicle_state": vehicle_status.get('vehl_state', None),
                "charge_state": vehicle_status.get('chrg_state', None),
                "operation_mode": vehicle_status.get('oprtn_mode', None),
                "speed": str(int(vehicle_status['speed'])) if 'speed' in vehicle_status else None,
                "mileage": vehicle_status.get('mileage', None),
                "total_voltage": str(int(vehicle_status['vehl_totl_volt'])) if 'vehl_totl_volt' in vehicle_status else None,
                "total_current": str(int(vehicle_status['vehl_totl_curnt'])) if 'vehl_totl_curnt' in vehicle_status else None,
                "soc": vehicle_status.get('soc', None),
                "dc_dc_status": vehicle_status.get('dc_dc_sts', None),
                "gear": vehicle_status.get('gear', None),
                "insulation_resistance": vehicle_status.get('insulatn_resis', None),
                "urgent_power_shutdown": vehicle_status.get('urgt_prw_shtdwn', None),
                "sample_time": self.sample_ts // 1000,
                "comf_ena": vehicle_status.get('comf_ena', None),
                "ntester": vehicle_status.get('ntester', None),
                "vehl_type_dbc": vehicle_status.get('vehl_type_dbc', None),
                }

        return data

    def to_light_status(self, light_status):
        data = {
            "high_beam_on": light_status.get('hi_beam_on', None),
            "low_beam_on": light_status.get('lo_beam_on', None),
            "head_light_on": light_status.get('head_light_on', None),
            "sample_time": self.sample_ts // 1000}

        return data

    def to_extremum_data(self, extremum_data):
        data = {
            "hist_volt_btry_sbsys_sn": extremum_data.get('hist_volt_btry_sbsys_sn', None),
            "hist_volt_singl_btry_sn": extremum_data.get('hist_volt_singl_btry_sn', None),
            "sin_btry_hist_volt": str(int(extremum_data['sin_btry_hist_volt'])) if 'sin_btry_hist_volt' in extremum_data else None,
            "sin_btry_lwst_volt": str(int(extremum_data['sin_btry_lwst_volt'])) if 'sin_btry_lwst_volt' in extremum_data else None,
            "lwst_volt_btry_sbsys_sn": extremum_data.get('lwst_volt_btry_sbsys_sn', None),
            "lwst_volt_singl_btry_sn": extremum_data.get('lwst_volt_singl_btry_sn', None),
            "hist_temp_prb_sn": extremum_data.get('hist_temp_prb_sn', None),
            "lwst_temp_prb_sn": extremum_data.get('lwst_temp_prb_sn', None),
            "highest_temp": str(extremum_data['highest_temp']).split('.')[0] if 'highest_temp' in extremum_data else None,
            "lowest_temp": str(extremum_data['lowest_temp']).split('.')[0] if 'lowest_temp' in extremum_data else None,
            "lwst_temp_btry_sbsys_sn": extremum_data.get('lwst_temp_btry_sbsys_sn', None),
            "hist_temp_btry_sbsys_sn": extremum_data.get('hist_temp_btry_sbsys_sn', None),
            "sample_time": self.sample_ts // 1000
        }

        return data

    def to_window_status(self, window_status):
        data = {
            "win_front_left_posn": window_status.get('window_positions', {}).get('win_frnt_le_posn'),
            "win_front_right_posn": window_status.get('window_positions', {}).get('win_frnt_ri_posn'),
            "win_rear_left_posn": window_status.get('window_positions', {}).get('win_re_le_posn'),
            "win_rear_right_posn": window_status.get('window_positions', {}).get('win_re_ri_posn'),
            "sun_roof_posn": window_status.get('sun_roof_positions', {}).get('sun_roof_posn'),
            "sun_roof_shade_posn": window_status.get('sun_roof_positions', {}).get('sun_roof_shade_posn'),
            "sun_roof_posn_sts": window_status.get('sun_roof_positions', {}).get('sun_roof_posn_sts'),
            "sample_time": self.sample_ts // 1000
        }

        return data

    def to_heating_status(self, heating_status):
        data = {
            "steer_wheel_heat_sts": heating_status.get('steer_wheel_heat_sts'),
            "seat_heat_frnt_le_sts": heating_status.get('seat_heat_frnt_le_sts'),
            "seat_heat_frnt_ri_sts": heating_status.get('seat_heat_frnt_ri_sts'),
            "seat_heat_re_le_sts": heating_status.get('seat_heat_re_le_sts'),
            "seat_heat_re_ri_sts": heating_status.get('seat_heat_re_ri_sts'),
            "hv_batt_pre_sts": heating_status.get('hv_batt_pre_sts'),
            "seat_vent_frnt_le_sts": heating_status.get('seat_vent_frnt_le_sts'),
            "seat_vent_frnt_ri_sts": heating_status.get('seat_vent_frnt_ri_sts'),
            "btry_warm_up_sts": heating_status.get('btry_warm_up_sts'),
            "seat_vent_re_le_sts": heating_status.get('seat_vent_re_le_sts'),
            "seat_vent_re_ri_sts": heating_status.get('seat_vent_re_ri_sts'),
            "sample_time": self.sample_ts // 1000
        }

        return data

    def to_driving_motor(self, driving_motor):
        data = {"pwr_sys_rdy": driving_motor.get('pwr_sys_rdy', None),
                "drvmotr_qunty": len(driving_motor.get('motor_list', None)),
                "sample_time": self.sample_ts // 1000,
                }
        if driving_motor.get('motor_list') is not None:
            data_extend = {}
            data_extend['driving_motors'] = []
            for i in range(len(driving_motor.get('motor_list'))):
                data_extend['driving_motors'].append(
                    {
                        "drvmotr_sn": driving_motor.get('motor_list')[i].get('drvmotr_sn', None),
                        "drvmotr_sts": driving_motor.get('motor_list')[i].get('drvmotr_sts', None),
                        "drvmotr_cntrl_temp": driving_motor.get('motor_list')[i].get('drvmotr_cntrl_temp', None),
                        "drvmotr_rotn_spd": driving_motor.get('motor_list')[i].get('drvmotr_rotn_spd', None),
                        "drvmotr_rotn_torq": driving_motor.get('motor_list')[i].get('drvmotr_rotn_torq', None),
                        "drvmotr_temp": driving_motor.get('motor_list')[i].get('drvmotr_temp', None),
                        "drvmotr_contl_involt": driving_motor.get('motor_list')[i].get('drvmotr_contl_involt', None),
                        "drvmotr_contl_dc_bus_curnt": str(int(driving_motor['motor_list'][i]['drvmotr_contl_dc_bus_curnt'])) if 'drvmotr_contl_dc_bus_curnt' in
                                                                                                                                driving_motor.get('motor_list')[i] else None,
                        "torq_command": driving_motor.get('motor_list')[i].get('torq_command', None),
                        "max_pos_torq_st": driving_motor.get('motor_list')[i].get('max_pos_torq_st', None),
                        "max_neg_torq_st": driving_motor.get('motor_list')[i].get('max_neg_torq_st', None)
                    }
                )
            data.update(data_extend)

        return data


offset_sec = 28800
# offset_sec = 0


def format_to_template_detail(template, cmdopt="test"):
    data = {
        'app_id': template.get("app_id"),
        'channel': template.get("channel"),
        # 'id': str(template.get("id")),
        'id': str(template.get("template_id")),
        'name': template.get("name"),
        'status': template.get("status"),
        'template_str': bytes.decode(template.get("template")),
        'type': template.get("type"),
        'create_time': format_time_to_int_10(template.get("create_time"), offset_sec=offset_sec),
        'update_time': format_time_to_int_10(template.get("update_time"), offset_sec=offset_sec)
    }
    return data


def format_to_template_list(template_list, cmdopt="test"):
    tp_ls = []
    for template in template_list:
        data = {
            'id': int(template.get("id")),
            'template_id': str(template.get("template_id")),
            # 'online_only': int(template.get("online_only")),
            'channel': template.get("channel"),
            'status': int(template.get("status")),
            'name': template.get("name"),
            'type': template.get("type"),
            'app_id': template.get("app_id"),
            'create_time': format_time_to_int_10(template.get("create_time"), offset_sec=offset_sec),
            'update_time': format_time_to_int_10(template.get("update_time"), offset_sec=offset_sec)
        }
        tp_ls.append(data)
    return tp_ls


def format_to_variable_detail(variable, cmdopt="test"):
    data = {
        'app_id': variable.get("app_id"),
        'create_time': format_time_to_int_10(variable.get("create_time"), offset_sec=offset_sec),
        'id': variable.get("id"),
        'name': variable.get("name"),
        'url': variable.get("url"),
        'status': variable.get("status"),
        'update_time': format_time_to_int_10(variable.get("update_time"), offset_sec=offset_sec),
    }
    return data


def format_to_variable_list(variable_list, cmdopt="test"):
    vb_ls = []
    for variable in variable_list:
        data = {
            'id': int(variable.get("id")),
            'status': int(variable.get("status")),
            'name': variable.get("name"),
            'url': variable.get("url"),
            'app_id': variable.get("app_id"),
            'create_time': format_time_to_int_10(variable.get("create_time"), offset_sec=offset_sec),
            'update_time': format_time_to_int_10(variable.get("update_time"), offset_sec=offset_sec),
        }
        vb_ls.append(data)
    return vb_ls


def format_to_tag_detail(tag, cmdopt="test"):
    data = {
        'app_id': tag.get("app_id"),
        'create_time': format_time_to_int_10(tag.get("create_time"), offset_sec=offset_sec),
        'id': tag.get("id"),
        'type': int(tag.get("type")),
        'name': tag.get("name"),
        'url': tag.get("url"),
        'status': tag.get("status"),
        'update_time': format_time_to_int_10(tag.get("update_time"), offset_sec=offset_sec),
    }
    return data


def format_to_tag_list(tag_list, cmdopt="test"):
    vb_ls = []
    for tag in tag_list:
        data = {
            'id': int(tag.get("id")),
            'type': int(tag.get("type")),
            'status': int(tag.get("status")),
            'name': tag.get("name"),
            'url': tag.get("url"),
            'app_id': tag.get("app_id"),
            'create_time': format_time_to_int_10(tag.get("create_time"), offset_sec=offset_sec),
            'update_time': format_time_to_int_10(tag.get("update_time"), offset_sec=offset_sec),
        }
        data = {k: v for k, v in data.items() if v}
        vb_ls.append(data)
    return vb_ls


def format_to_task_list(task_list, cmdopt="test"):
    ts_ls = []
    for task in task_list:
        data = {
            'id': int(task.get("id")),
            'execution_data': task.get("execution_data"),
            'execution_result': task.get("execution_result"),
            'app_id': task.get("app_id"),
            'status': task.get("status"),
            'create_time': format_time_to_int_10(task.get("create_time"), offset_sec=offset_sec),
            'update_time': format_time_to_int_10(task.get("update_time"), offset_sec=offset_sec),
            'execution_time': task.get("execution_time"),
            'appointment_time': task.get("appointment_time")
        }
        data = {k: v for k, v in data.items() if v is not None}
        ts_ls.append(data)
    return ts_ls


def format_to_task_detail(task_list, cmdopt="test"):
    ts_ls = []
    for task in task_list:
        data = {
            'id': int(task.get("id")),
            'execution_data': task.get("execution_data"),
            'execution_result': task.get("execution_result"),
            'name': task.get("name"),
            'type': task.get("type"),
            'app_id': task.get("app_id"),
            'create_time': format_time_to_int_10(task.get("create_time"), offset_sec=offset_sec),
            'update_time': format_time_to_int_10(task.get("update_time"), offset_sec=offset_sec),
            'appointment_time': format_time_to_int_10(task.get("appointment_time"), offset_sec=offset_sec),
        }
        ts_ls.append(data)
    return ts_ls


def format_to_message_state(states, cmdopt="test"):
    ts_ls = []
    for state in states:
        data = {
            'id': int(state.get("id")),
            'message_id': state.get("message_id"),
            'client_id': state.get("client_id"),
            'state': state.get("state"),
            'reason': state.get("reason"),
            'create_time': format_time_to_int_10(state.get("create_time"), format="%Y-%m-%d %H:%M:%S.%f", offset_sec=offset_sec),
            'update_time': format_time_to_int_10(state.get("update_time"), format="%Y-%m-%d %H:%M:%S.%f", offset_sec=offset_sec)
        }

        # [data.pop(k) for k, v in data.items()]
        ts_ls.append(data)
    return ts_ls


class MsgToKafkaFormator(object):
    def __init__(self, vehicle_id, sample_ts=None):
        self.vehicle_id = vehicle_id
        self.sample_ts = sample_ts if sample_ts else None

    def to_connection_status_event(self, connection_status_obj, cassandra_obj):
        data = copy.deepcopy(connection_status_obj)
        data['params']['account_id'] = self.vehicle_id

        cassandra_obj.update({'vid': cassandra_obj.pop('vehicle_id')})
        cassandra_obj['position_status'].update({'latitude': round(cassandra_obj['position_status'].pop('latitude_gcj02'), 1)})
        cassandra_obj['position_status'].update({'longitude': round(cassandra_obj['position_status'].pop('longitude_gcj02'), 1)})
        cassandra_obj['position_status'].pop('altitude_uncertainty')
        cassandra_obj['position_status'].pop('fusion_mode')
        cassandra_obj['position_status'].pop('mode')
        cassandra_obj['position_status'].pop('latitude_uncertainty')
        cassandra_obj['position_status'].pop('longitude_uncertainty')
        cassandra_obj['soc_status'].pop('btry_pak_sum')
        cassandra_obj['soc_status'].pop('soc')
        cassandra_obj['soc_status'].pop('max_soc')
        cassandra_obj['soc_status'].pop('lock_soc')
        cassandra_obj['soc_status'].pop('soc_lock_status')
        cassandra_obj['soc_status'].pop('v2l_status')
        # cassandra_obj['vehicle_status'].pop('comf_ena')
        cassandra_obj['vehicle_status'].pop('ntester')
        cassandra_obj['vehicle_status'].pop('vehl_type_dbc')
        cassandra_obj['vehicle_status']['speed'] = round(cassandra_obj['vehicle_status']['speed'])

        data['params']['vehicle_status'] = cassandra_obj
        data['params']['vehicle_status']['sample_ts'] = self.sample_ts
        data['params'].pop('status')
        return data


def handle_zero(data):
    if data is None:
        return None
    elif data == 0:
        return 0.0
    else:
        return str(int(data))
