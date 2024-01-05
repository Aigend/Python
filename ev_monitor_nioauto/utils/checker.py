#!/usr/bin/env python
# coding=utf-8

"""
:author: li.liu
:Date: Created on 2019/1/8 下午5:04
"""
import copy
import datetime
import json
import time

import allure

from nio_messages.can_data import CAN_DATA
from utils import message_formator, time_parse
from utils.assertions import assert_equal
from utils.city_code import city_code
from utils.coordTransform import wgs84_to_gcj02
from utils.db import DB
from utils.http_client import TSPRequest
from utils.time_parse import timestamp_to_utc_strtime


class LazyProperty(object):
    # 使得属性只初始化一次，而@perperty装饰符每次都初始化属性
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value


class Checker(object):
    def __init__(self, vid, vin=None, cmdopt=None, env=None, api=None, redis_key_front=None):
        self.vid = vid
        self.vin = vin
        self.cmdopt = cmdopt
        self.redis_key_front = redis_key_front
        self.env = env
        self.api = api
        self.db = DB(cmdopt)

    @LazyProperty
    def mysql(self):
        return self.db.mysql['rvs']

    @LazyProperty
    def cassandra(self):
        return self.db.cassandra['datacollection']

    @LazyProperty
    def cassandra_driving(self):
        if self.cmdopt == 'test':
            return self.db.cassandra['datacollection_driving']

    @LazyProperty
    def mongodb(self):
        return self.db.mongodb['rvs']

    @LazyProperty
    def redis(self):
        return self.db.redis['cluster']

    @LazyProperty
    def kafka(self):
        return self.db.kafka

    @LazyProperty
    def mysql_fota(self):
        return self.db.mysql['fota']

    @LazyProperty
    def mysql_rvs_data(self):
        return self.db.mysql['rvs_data']

    def _clear_none(self, data):
        if isinstance(data, dict):
            return {k: self._clear_none(v) for k, v in data.items() if v is not None}
        elif isinstance(data, list):
            return [self._clear_none(item) for item in data if item is not None]
        elif isinstance(data, tuple):
            return tuple(self._clear_none(item) for item in data if item is not None)
        elif isinstance(data, set):
            return {self._clear_none(item) for item in data if item is not None}
        else:
            return data

    def check_mysql_tables(self, obj, tables, event_name=None, sample_ts=None, extra=None, platform=None, reissue=False):
        where_model, sample_time = {}, ''
        if sample_ts is not None:
            sample_time = timestamp_to_utc_strtime(sample_ts)
        elif 'sample_ts' in obj:
            sample_ts = obj['sample_ts']
            sample_time = timestamp_to_utc_strtime(sample_ts)

        where_model = {"id": self.vid}
        if event_name != 'alarm_signal_update_event' and sample_time != '':
            where_model['sample_time'] = sample_time

        formator = message_formator.MessageFormator(self.vid, sample_ts, cmdopt=self.cmdopt)

        # 如果是stg环境，需要等待30秒后在做校验
        # if self.cmdopt == 'stg':
        #     time.sleep(30)
        # else:
        #     time.sleep(3)

        for table in tables:
            if table == 'vehicle_profile_info_extend':
                with allure.step("校验 vam_vehicle_status 信息存入Mysql的 vehicle_profile_info_extend 表"):
                    vam_vehilce_status = self.mysql.fetch_one('vehicle_profile_info_extend', {"vin": self.vin}, fields=['vehicle_identity', 'vehicle_condition'],)
                    assert_equal(obj, vam_vehilce_status)
            elif table == 'status_position':
                # 校验status_position表
                with allure.step("校验 position_status 信息存入Mysql的 status_position 表"):
                    status_position_in_mysql = self.mysql.fetch_one('status_position', where_model, exclude_fields=['update_time', 'area_code'])
                    position_status_in_message = formator.to_mysql_status_position(obj['position_status'])
                    assert_equal(status_position_in_mysql, position_status_in_message)

            elif table == 'status_vehicle':
                # 校验status_vehicle表
                with allure.step("校验 status_vehicle 信息存入Mysql的 status_vehicle 表"):
                    status_vehicle_in_mysql = self.mysql.fetch_one('status_vehicle', where_model, exclude_fields=['update_time', 'vehl_mode'])
                    vehicle_status_in_message = formator.to_mysql_status_vehicle(obj['vehicle_status'])
                    assert_equal(status_vehicle_in_mysql, vehicle_status_in_message)

            elif table == 'status_soc':
                # 校验status_soc表
                if 'charging_info' in obj:
                    with allure.step("校验 status_soc 信息存入Mysql的 status_soc 表"):
                        # chg_subsys_encoding 字段的值来自battery_package_info.btry_pak_encoding的nio_encoding字段
                        status_soc_in_mysql = self.mysql.fetch_one('status_soc', where_model,
                                                                   exclude_fields=['update_time', 'chg_subsys_len',
                                                                                   'chg_subsys_encoding', 'chrg_pwr',
                                                                                   'battery_pack_cap', 'chrg_disp_volt',
                                                                                   'chrg_disp_lamp_req',
                                                                                   'chrg_disp_crrt'])
                        soc_status_in_message = formator.to_mysql_status_soc(obj['soc_status'], obj['charging_info'])
                        assert_equal(status_soc_in_mysql, soc_status_in_message)
                else:

                    with allure.step("校验 status_soc 信息存入Mysql的 status_soc 表"):
                        status_soc_in_mysql = self.mysql.fetch_one('status_soc', where_model,
                                                                   exclude_fields=['update_time', 'chg_subsys_len',
                                                                                   'chg_subsys_encoding',
                                                                                   'charger_type', 'in_volt_ac',
                                                                                   'in_volt_dc', 'in_curnt_ac',
                                                                                   'estimate_chrg_time',
                                                                                   'battery_pack_cap', 'chrg_disp_crrt',
                                                                                   'chrg_disp_lamp_req', 'chrg_pwr',
                                                                                   'chrg_disp_volt' ])
                        soc_status_in_message = formator.to_mysql_status_soc(obj['soc_status'])
                        assert_equal(status_soc_in_mysql, soc_status_in_message)

            elif table == 'status_btry_packs':
                # 校验status_btry_paks表
                with allure.step("校验 btry_paks 信息存入Mysql的 status_btry_packs 表"):

                    for i in range(len(obj['soc_status']['btry_paks'])):
                        if event_name == 'charge_start_event':
                            if ('battery_package_info' in obj
                                    and 'btry_pak_encoding' in obj['battery_package_info']
                                    and 'btry_pak_health_status' in obj['battery_package_info']):
                                where_models = {"serial_num": obj['soc_status']['btry_paks'][i]['btry_pak_sn']}
                                where_models.update(where_model)
                                btry_paks_status_in_mysql = self.mysql.fetch_one('status_btry_packs', where_models,
                                                                             exclude_fields=['update_time', 'chg_subsys_encoding', 'bid'])
                                btry_paks_status_in_message = formator.to_mysql_status_btry_packs(
                                    obj['soc_status']['btry_paks'][i],
                                    obj['battery_package_info']['btry_pak_encoding'][i],
                                    obj['battery_package_info']['btry_pak_health_status'][i])
                                if 'marcopolo' in self.cmdopt:
                                    btry_paks_status_in_mysql.pop("re_encoding")
                                    btry_paks_status_in_message.pop("re_encoding")
                                    btry_paks_status_in_message["nio_encoding"] = btry_paks_status_in_message["nio_encoding"][:-5]
                                assert_equal(btry_paks_status_in_mysql, btry_paks_status_in_message)
                        elif event_name == 'journey_start_event':
                            if ('btry_pak_encoding' in obj['battery_package_info'] and 'btry_pak_health_status' in obj[
                                'battery_package_info']):
                                where_models = {"serial_num": obj['soc_status']['btry_paks'][i]['btry_pak_sn']}
                                where_models.update(where_model)
                                btry_paks_status_in_mysql = self.mysql.fetch_one('status_btry_packs',
                                                                             where_models,
                                                                             exclude_fields=['update_time',
                                                                                             'chg_subsys_encoding',
                                                                                             'serial_num', 'voltage',
                                                                                             'current',
                                                                                             'bid',
                                                                                             'sin_btry_qunty_of_pak',
                                                                                             'frm_start_btry_sn',
                                                                                             'sin_btry_qunty_of_frm',
                                                                                             'sin_btry_voltage',
                                                                                             'temp_prb_qunty',
                                                                                             'prb_temp_lst',
                                                                                             'btry_pak_hist_temp',
                                                                                             'btry_pak_lwst_temp',
                                                                                             'sin_btry_voltage_inv',
                                                                                             'prb_temp_lst_inv'])
                                btry_paks_status_in_message = formator.to_mysql_status_btry_packs(
                                    btry_pak_encoding=obj['battery_package_info']['btry_pak_encoding'][i],
                                    btry_pak_health_status=obj['battery_package_info']['btry_pak_health_status'][i])
                                assert_equal(btry_paks_status_in_mysql, btry_paks_status_in_message)


                        else:
                            where_models = {"serial_num": obj['soc_status']['btry_paks'][i]['btry_pak_sn']}
                            where_models.update(where_model)
                            btry_paks_status_in_mysql = self.mysql.fetch_one('status_btry_packs',
                                                                         where_models,
                                                                         exclude_fields=['update_time', 'nio_encoding', 're_encoding', 'battery_health_status', 'chg_subsys_encoding','bid'])
                            btry_paks_status_in_message = formator.to_mysql_status_btry_packs(obj['soc_status']['btry_paks'][i])
                            assert_equal(btry_paks_status_in_mysql, btry_paks_status_in_message)

            elif table == 'status_skyview':
                time.sleep(2)
                # 校验status_skyview表
                with allure.step("校验 skyview_status 信息存入Mysql的 status_skyview 表"):
                    for item in obj['position_status']['satellite']['skyview']:
                        where_models = {"prn_id": item['prn_id']}
                        where_models.update(where_model)
                        skyview_in_mysql = self.mysql.fetch_one('status_skyview', where_models, exclude_fields=['update_time'])
                        skyview_in_message = formator.to_mysql_status_skyview(item)
                        assert_equal(skyview_in_mysql, skyview_in_message)

            elif table == 'status_attitude':
                # 校验status_attitude表
                with allure.step("校验 attitude 信息存入Mysql的 status_attitude 表"):
                    attitude_in_mysql = self.mysql.fetch_one('status_attitude', where_model, exclude_fields=['update_time'])
                    attitude_in_message = formator.to_mysql_status_attitude(obj['position_status']['attitude'])
                    assert_equal(attitude_in_mysql, attitude_in_message)

            elif table == 'status_sensors':
                # 校验status_sensors表
                with allure.step("校验 sensors 信息存入Mysql的 status_sensors 表"):
                    sensors = obj['position_status']['attitude']['sensors']
                    for item in sensors:
                        where_models = {"type": item['type']}
                        where_models.update(where_model)
                        sensors_in_mysql = self.mysql.fetch_one('status_sensors', where_models,
                                                            exclude_fields=['update_time'])
                        sensors_in_message = formator.to_mysql_status_sensors(item)
                        assert_equal(sensors_in_mysql, sensors_in_message)

            elif table == 'status_door':
                # 校验status_door表
                with allure.step("校验 door_status 信息存入Mysql的 status_door 表"):
                    status_door_in_mysql = self.mysql.fetch_one('status_door', where_model, exclude_fields=['update_time'])
                    # 如果上报account_id, mysql user_id字段存储account_id
                    if 'account_id' in obj['door_status']['door_locks']:
                        obj['door_status']['door_locks']['user_id'] = obj['door_status']['door_locks'].pop('account_id')
                    door_status_in_message = formator.to_mysql_status_door(obj['door_status'])
                    assert_equal(status_door_in_mysql, door_status_in_message)

            elif table == 'status_driving_behv':
                # 校验status_driving_behv表
                with allure.step("校验 driving_behaviour 信息存入Mysql的 status_driving_behv 表"):
                    for item in obj['behaviour']:
                        where_models = {"behv_type": item}
                        where_models.update(where_model)
                        driving_behaviour_in_mysql = self.mysql.fetch_one('status_driving_behv', where_models,
                                                                      exclude_fields=['update_time'])
                        driving_behaviour_in_message = formator.to_mysql_status_driving_behv(item)
                        assert_equal(driving_behaviour_in_mysql, driving_behaviour_in_message)

            elif table == 'status_hvac':
                # 校验status_driving_behv表
                with allure.step("校验 hvac_status 信息存入Mysql的 status_hvac 表"):
                    if event_name == 'journey_start_event':
                        pm25_fil_in_mysql = self.mysql.fetch_one('status_hvac', where_model,
                                                             exclude_fields=['update_time', 'ac_target_temp_c',
                                                                             'cabin_preconditioning'])['pm25_fil']
                        pm25_fil_in_message = obj['pm25_fil']
                        assert_equal(pm25_fil_in_mysql, pm25_fil_in_message)
                    else:
                        status_hvac_in_mysql = self.mysql.fetch_one('status_hvac', where_model,
                                                                exclude_fields=['update_time', 'ac_target_temp_c',
                                                                                'cabin_preconditioning', 'pm25_fil'])
                        status_hvac_in_message = formator.to_mysql_status_hvac(obj['hvac_status'])
                        assert_equal(status_hvac_in_mysql, status_hvac_in_message)

            elif table == 'status_window':
                # 校验status_window表
                with allure.step("校验 window_status 信息存入Mysql的 status_window 表"):
                    window_status_in_mysql = \
                        self.mysql.fetch_one('status_window', where_model, exclude_fields=['update_time'])
                    window_status_in_message = formator.to_mysql_status_window(obj['window_status'])
                    assert_equal(window_status_in_mysql, window_status_in_message)

            elif table == 'status_light':
                # 校验status_light表
                with allure.step("校验 light_status 信息存入Mysql的 status_light 表"):
                    light_status_in_mysql = \
                        self.mysql.fetch_one('status_light', where_model, exclude_fields=['update_time'])
                    light_status_in_message = formator.to_mysql_status_light(obj['light_status'])
                    assert_equal(light_status_in_mysql, light_status_in_message)

            elif table == 'status_heating':
                # 校验status_heating表
                with allure.step("校验 heating_status 信息存入Mysql的 status_heating 表"):
                    heating_status_in_mysql = self.mysql.fetch_one('status_heating', where_model, exclude_fields=['update_time'])
                    heating_status_in_message = formator.to_mysql_status_heating(obj['heating_status'])
                    assert_equal(heating_status_in_mysql, heating_status_in_message)

            elif table == 'status_nbs':
                # 校验status_heating表
                with allure.step("校验 heating_status 信息存入Mysql的 status_nbs 表"):
                    nbs_status_in_mysql = self.mysql.fetch_one('status_nbs', where_model, exclude_fields=['update_time'])
                    nbs_status_in_message = formator.to_mysql_status_nbs(obj['nbs_status'])
                    assert_equal(nbs_status_in_mysql, nbs_status_in_message)

            elif table == 'status_occupant':
                # 校验status_occupant表
                with allure.step("校验 occupant 信息存入Mysql的 status_occupant 表"):
                    occupant_status_in_mysql = \
                        self.mysql.fetch_one('status_occupant', where_model, exclude_fields=['update_time'])
                    occupant_status_in_message = formator.to_mysql_status_occupant(obj['occupant_status'])
                    assert_equal(occupant_status_in_mysql, occupant_status_in_message)

            elif table == 'status_driving_motor_data':
                # 校验status_driving_motor_data表
                with allure.step("校验 driving_motor_data 信息存入Mysql的 status_driving_motor_data 表"):
                    for item in obj['driving_motor']['motor_list']:
                        driving_motor_data_in_message = formator.to_mysql_status_driving_motor_data(item)
                        where_models = {'drvmotr_sn': item['drvmotr_sn'], 'sample_time': driving_motor_data_in_message['sample_time']}
                        where_models.update(where_model)
                        driving_motor_data_in_mysql = self.mysql.fetch_one('status_driving_motor_data', where_models,
                                                                       exclude_fields=['update_time'])
                        assert_equal(driving_motor_data_in_mysql, driving_motor_data_in_message)

            elif table == 'status_driving_motor':
                # 校验status_driving_motor表
                with allure.step("校验 driving_motor 信息存入Mysql的 status_driving_motor 表"):
                    driving_motor_in_mysql = self.mysql.fetch_one('status_driving_motor', where_model, exclude_fields=['update_time'])
                    driving_motor_in_message = formator.to_mysql_status_driving_motor(obj['driving_motor'])
                    assert_equal(driving_motor_in_mysql, driving_motor_in_message)

            elif table == 'status_extremum_data':
                # 校验status_extremum_data表
                with allure.step("校验 extremum_data 信息存入Mysql的 status_extremum_data 表"):
                    extremum_data_in_mysql = self.mysql.fetch_one('status_extremum_data', where_model, exclude_fields=['update_time'])
                    extremum_data_in_message = formator.to_mysql_status_extremum_data(obj['extremum_data'])
                    assert_equal(extremum_data_in_mysql, extremum_data_in_message)

            elif table == 'status_driving_data':
                # 校验status_driving_data表
                with allure.step("校验 driving_data 信息存入Mysql的 status_driving_data 表"):
                    driving_data_in_mysql = self.mysql.fetch_one('status_driving_data', where_model, exclude_fields=['update_time'])
                    driving_data_in_message = formator.to_mysql_status_driving_data(obj['driving_data'])
                    assert_equal(driving_data_in_mysql, driving_data_in_message)

            elif table == 'status_bms':
                # 校验status_bms表
                with allure.step("校验 bms_status 信息存入Mysql的 status_bms 表"):
                    bms_in_mysql = self.mysql.fetch_one('status_bms', where_model, exclude_fields=['update_time'])
                    bms_in_message = formator.to_mysql_status_bms(obj['bms_status'])
                    assert_equal(bms_in_mysql, bms_in_message)

            elif table == 'status_can_msg':
                # 校验status_bms表
                with allure.step("校验 can_msg 信息存入Mysql的 status_can_msg 表"):
                    can_msg_in_mysql = self.mysql.fetch_one('status_can_msg', where_model, exclude_fields=['update_time'])
                    can_msg_in_message = formator.to_mysql_status_can_msg(obj['can_msg'])
                    assert_equal(can_msg_in_mysql, can_msg_in_message)

            elif table == 'status_tyre':
                # 校验status_tyre表
                with allure.step("校验 tyre_status 信息存入Mysql的 status_tyre 表"):
                    status_tyre_in_mysql = self.mysql.fetch_one('status_tyre', where_model, exclude_fields=['update_time'])
                    status_tyre_in_message = formator.to_mysql_status_tyre(obj['tyre_status'])
                    assert_equal(status_tyre_in_mysql, status_tyre_in_message)

            elif table == 'status_did':
                # 校验 status_did表
                with allure.step("校验 did 信息存入Mysql的 status_did 表"):
                    where_models = {"tag": obj['did_tag']}
                    where_models.update(where_model)
                    where_models['vid'] =where_models.pop('id')
                    status_did_in_mysql = self.mysql.fetch('status_did', where_models,
                                                           exclude_fields=['update_time', 'tag', 'id', 'vid'])
                    status_did_in_message = formator.to_mysql_status_did(obj['did_data'])

                    mysql_sorted = sorted(status_did_in_mysql, key=lambda x: x['ecu'] + x['didid'])
                    msg_sorted = sorted(status_did_in_message, key=lambda x: x['ecu'] + x['didid'])

                    assert_equal(mysql_sorted, msg_sorted)

            elif table == 'vehicle_dids':
                # 校验 vehicle_dids
                with allure.step("校验 did 信息存入Fota Mysql的 vehicle_dids 表"):
                    dids_in_mysql = self.mysql_fota.fetch_one('vehicle_dids', {"vid": self.vid, "dids_tag": obj['did_tag']},
                                                          fields=['dids_json'])['dids_json']
                    dids_in_msg = formator.to_fota_mysql_vehicle_dids(obj['did_data'])
                    dids_in_mysql = json.loads(dids_in_mysql)

                    dids_in_mysql_chg = {}
                    for item in dids_in_mysql:
                        dids_in_mysql_chg[item['ecu']] = sorted(item['dids'], key=lambda x: x['id'])

                    dids_in_msg_chg = {}
                    for item in dids_in_msg:
                        dids_in_msg_chg[item['ecu']] = sorted(item['dids'], key=lambda x: x['id'])

                    assert_equal(dids_in_mysql_chg, dids_in_msg_chg)

            elif table == 'status_wti_alarm':
                with allure.step("校验 alarm_singal 信息存入Mysql的 status_wti_alarm 表"):
                    if event_name == 'alarm_signal_update_event':
                        alarm_signal = obj['alarm_signal']
                    elif event_name == 'periodical_charge_update' or 'periodical_journey_update':
                        alarm_signal = obj['sample_points'][0]['alarm_signal']
                    else:
                        raise Exception('event_name {} is wrong'.format(event_name))

                    if 'signal_int' in alarm_signal:
                        # extra like list [{'name': 'DCDCHotSpotTemp', 'value': [121, 125, 135], 'alarm_level': 1, 'wti_code': 'WTI-EVM-12'}]
                        tmp_msg = formator.to_mysql_status_wti_alarm(vin=self.vid if 'marcopolo' in self.cmdopt else self.vin,
                                                                     alarm_signal_int=alarm_signal['signal_int'],
                                                                     wti_accompany=extra)
                        status_wti_alarm_in_message = {item['wti_code']: item for item in tmp_msg}

                        wti_code_list = [item['wti_code'] for item in extra]
                        status_wti_alarm_in_mysql = {}
                        for item in wti_code_list:
                            where_models = {'wti_code': item}
                            where_models.update(where_model)
                            where_models['sample_time'] = status_wti_alarm_in_message[wti_code_list[0]]['sample_time']
                            tmp_mysql = self.mysql.fetch_one('status_wti_alarm', where_models,
                                                         exclude_fields=['update_time'])
                            status_wti_alarm_in_mysql[item] = tmp_mysql

                        assert_equal(status_wti_alarm_in_mysql, status_wti_alarm_in_message)

            elif table == 'history_wti_alarm':
                with allure.step("校验 alarm_singal 信息存入Mysql的 history_wti_alarm 表"):
                    if event_name == 'alarm_signal_update_event':
                        alarm_signal = obj['alarm_signal']
                        sp = obj['sample_points']
                    elif event_name in ['periodical_charge_update', 'periodical_journey_update']:
                        alarm_signal = obj['sample_points'][0]['alarm_signal']
                        sp = obj['sample_points'][0]
                    else:
                        raise Exception('event_name {} is wrong'.format(event_name))

                    if 'signal_int' in alarm_signal:
                        alarm_id_list = ['{}-{}-{}-WTI'.format(self.vid if 'marcopolo' in self.cmdopt else self.vin,
                                                               alarm_signal['signal_int'][i]['sn'],
                                                               item['wti_code'][4:]) for i, item in enumerate(extra)]
                        tmp_mysql = self.mysql.fetch('history_wti_alarm',
                                                     {"vehicle_id": self.vid,
                                                      'alarm_id in': alarm_id_list},
                                                     suffix=' and `mileage` is not NULL',
                                                     fields=['vehicle_id', 'alarm_id', 'wti_code',
                                                             'start_time', 'end_time', 'chrg_sts', 'vehl_sts',
                                                             'soc', 'mileage', 'alarm_tag', 'latitude', 'longitude',
                                                             'charger_type', 'model', 'city_code',
                                                             # alarm_signal_update_event 事件不把EVM alarm数据上报国家平台,即reported_national_tag=0
                                                             # update事件会如果上报在evm范围内的alarm，并且vehicle_platform_activated表中alarm_enable=1时，会把数据上报国家平台，即reported_national_tag=1
                                                             # 'reported_local_tag', 'reported_national_tag'
                                                             ])
                        history_wti_alarm_in_mysql = {}
                        for item in tmp_mysql:
                            if event_name not in ['periodical_charge_update', 'periodical_journey_update']:
                                item.pop('latitude')
                                item.pop('longitude')
                            history_wti_alarm_in_mysql[item['alarm_id']] = item

                        # extra like list [{'name': 'DCDCHotSpotTemp', 'value': [121, 125, 135], 'alarm_level': 1, 'wti_code': 'WTI-EVM-12'}]
                        tmp_msg = formator.to_mysql_history_wti_alarm(vin=self.vid if 'marcopolo' in self.cmdopt else self.vin,
                                                                      alarm_signal_int=alarm_signal['signal_int'],
                                                                      wti_accompany=extra)
                        charger_type_in_mysql = self.mysql.fetch_one('status_soc', where_model, fields=['charger_type'])['charger_type']
                        vehicle_profile = self.mysql.fetch_one('vehicle_profile', {"id": self.vid})
                        vehicle_extend = self.mysql.fetch_one('vehicle_profile_info_extend', {"vehicle_id": self.vid})
                        vehicle_type = self.mysql.fetch('vehicle_profile_info_extend', {"vehicle_id": self.vid})[0].get('vehicle_type', None)

                        position_in_mysql = self.mysql.fetch('status_position', where_model)[0]
                        if self.cmdopt == "stg_marcopolo":
                            city_code_in_mysql = None
                        else:
                            city_code_in_mysql = city_code(self.mysql.fetch('vehicle_navigation', {"id": self.vid})[0]['area_code'])

                        history_wti_alarm_in_message = {}
                        for item in tmp_msg:
                            item['charger_type'] = charger_type_in_mysql
                            item['vehl_sts'] = sp['vehicle_status']['vehl_state']
                            item['chrg_sts'] = sp['soc_status']['chrg_state']
                            item['soc'] = sp['soc_status']['soc']
                            item['mileage'] = sp['vehicle_status']['mileage']
                            item['city_code'] = city_code_in_mysql
                            if event_name in ['periodical_charge_update', 'periodical_journey_update']:
                                item['latitude'] = None if 'marcopolo' in self.cmdopt else position_in_mysql['latitude_gcj02']
                                item['longitude'] = None if 'marcopolo' in self.cmdopt else position_in_mysql['longitude_gcj02']
                            # 当前alarm_tag判断逻辑以字段first_activation_time为准
                            if 'test' in vehicle_extend['vehicle_type']:
                                item['alarm_tag'] = 2
                            else:
                                if vehicle_profile is not None and vehicle_profile['first_activation_time'] is not None:
                                    if vehicle_type and 'test' in vehicle_type:
                                        item['alarm_tag'] = 2
                                    else:
                                        item['alarm_tag'] = 1
                                else:
                                    item['alarm_tag'] = 0

                            item['model'] = vehicle_profile['model']
                            history_wti_alarm_in_message[item['alarm_id']] = item

                        assert_equal(history_wti_alarm_in_mysql, history_wti_alarm_in_message)

            # elif table == 'vehicle_alarm_process':
            #     with allure.step("校验 alarm_singal 信息存入Mysql的 vehicle_alarm_process 表"):
            #         if event_name == 'alarm_signal_update_event':
            #             alarm_signal = obj['alarm_signal']
            #         elif event_name == 'periodical_charge_update' or 'periodical_journey_update':
            #             alarm_signal = obj['sample_points'][0]['alarm_signal']
            #         else:
            #             raise Exception('event_name {} is wrong'.format(event_name))
            #
            #         if 'signal_int' in alarm_signal:
            #             alarm_id_list = ['{}-{}-{}-WTI'.format(self.vin, alarm_signal['signal_int'][i]['sn'], item['wti_code'][4:]) for i, item in enumerate(extra)]
            #             tmp_mysql = self.mysql.fetch('vehicle_alarm_process',
            #                                          where_model={'vehicle_id': self.vid, 'alarm_id in': alarm_id_list},
            #                                          fields=['vehicle_id', 'alarm_id', 'wti_code', 'status'])
            #             vehicle_alarm_process_in_mysql = {item['alarm_id']: item for item in tmp_mysql}
            #
            #             # extra like list [{'name': 'DCDCHotSpotTemp', 'value': [121, 125, 135], 'alarm_level': 1, 'wti_code': 'WTI-EVM-12'}]
            #             tmp_message = formator.to_mysql_vehicle_alarm_process(vin=self.vin,
            #                                                                   alarm_signal_int=alarm_signal[
            #                                                                       'signal_int'], wti_accompany=extra)
            #
            #             vehicle_alarm_process_in_message = {item['alarm_id']: item for item in tmp_message}
            #
            #             assert_equal(vehicle_alarm_process_in_mysql, vehicle_alarm_process_in_message)

            elif table == 'svt_event':
                with allure.step("校验 svt_event 信息存入Mysql的 svt_event 表"):
                    svt_event_in_mysql = self.mysql.fetch_one('svt_event', {"vehicle_id": self.vid, "event_id": obj['event_id'] // 1000},
                                                          exclude_fields=['id', 'create_time'])
                    svt_event_in_message = formator.to_mysql_svt_event(obj)
                    svt_event_in_mysql['svt_data'] = json.loads(svt_event_in_mysql['svt_data'])
                    svt_event_in_mysql['svt_data']['vehicle_status']['speed'] = round(svt_event_in_mysql['svt_data']['vehicle_status']['speed'], 1)
                    assert_equal(svt_event_in_mysql, svt_event_in_message)

            elif table == 'ecall_event':
                with allure.step("校验 ecall_event 信息存入Mysql的 ecall_event 表"):
                    if event_name == 'ecall_event':
                        ecall_status = obj['status']
                        event_id = obj['event_id'] // 1000
                        reason_code = obj['reason_code']
                        alarm_signal = obj['status']['alarm_signal']
                        window_in_mysql = None
                        door_in_mysql = None

                    elif event_name in ('periodical_charge_update', 'periodical_journey_update'):
                        ecall_status = obj['sample_points'][0]
                        event_id = sample_ts // 1000
                        reason_code = 'urgt_prw_shtdwn'
                        alarm_signal = obj['sample_points'][0]['alarm_signal']
                        window_in_mysql = self.mysql.fetch_one('status_window', {'id': self.vid}, exclude_fields=['update_time'])
                        door_in_mysql = self.mysql.fetch_one('status_door', {'id': self.vid}, exclude_fields=['update_time'])

                    elif event_name == 'alarm_signal_update_event':
                        ecall_status = obj['sample_points']
                        event_id = sample_ts // 1000
                        reason_code = 'urgt_prw_shtdwn'
                        alarm_signal = obj['alarm_signal']
                        window_in_mysql = self.mysql.fetch_one('status_window', where_model, exclude_fields=['update_time'])
                        door_in_mysql = self.mysql.fetch_one('status_door', where_model, exclude_fields=['update_time'])
                    elif event_name == 'instant_status_resp':
                        ecall_status = obj['sample_point']
                        event_id = sample_ts // 1000
                        reason_code = 'urgt_prw_shtdwn'
                        alarm_signal = obj['sample_point']['alarm_signal']
                        window_in_mysql = self.mysql.fetch_one('status_window', where_model, exclude_fields=['update_time'])
                        door_in_mysql = self.mysql.fetch_one('status_door', where_model, exclude_fields=['update_time'])
                    else:
                        raise Exception('event_name error')
                    vehicle_model = self.mysql.fetch_one('vehicle_profile', {"id": self.vid}, fields=['model_type', 'model_type_year'])
                    model_type = vehicle_model['model_type']
                    model_type_year = vehicle_model['model_type_year']
                    ecall_event_in_mysql = self.mysql.fetch_one('ecall_event', {"vehicle_id": self.vid, "event_id": event_id},
                                                            exclude_fields=['id', 'create_time'])
                    ecall_event_in_message = formator.to_mysql_ecall_event(ecall_status=ecall_status,
                                                                           event_id=event_id,
                                                                           reason_code=reason_code,
                                                                           alarm_signal=alarm_signal,
                                                                           window_mysql=window_in_mysql,
                                                                           door_mysql=door_in_mysql,
                                                                           model_type=model_type,
                                                                           model_type_year=model_type_year
                                                                           )
                    ecall_event_in_message.pop('vehicle_identity')
                    ecall_event_in_mysql['ecall_data'] = json.loads(ecall_event_in_mysql['ecall_data'])

                    # sorted the tyre_alarm list
                    ecall_event_in_mysql['ecall_data']['tyre_alarm'] = sorted(
                        ecall_event_in_mysql['ecall_data']['tyre_alarm'], key=lambda k: k['wti_code'])
                    ecall_event_in_message['ecall_data']['tyre_alarm'] = sorted(
                        ecall_event_in_message['ecall_data']['tyre_alarm'], key=lambda k: k['wti_code'])

                    # round the speed value
                    # ecall_event_in_mysql['ecall_data']['speed'] = round(ecall_event_in_mysql['ecall_data']['speed'])

                    assert_equal(ecall_event_in_mysql, ecall_event_in_message)

            elif table == 'status_lv_battery':
                with allure.step("校验 lv_battery 信息存入Mysql的 status_lv_battery 表"):
                    if sample_time:
                        where_model = {"vehicle_id": self.vid, 'sample_time': sample_time}
                    else:
                        where_model = {"vehicle_id": self.vid, }

                    status_lv_battery_in_mysql = self.mysql.fetch_one('status_lv_battery', where_model,
                                                                  exclude_fields=['id', 'update_time'])
                    if 'can_msg' in obj:  # 通过lv_batt_charging_event事件上报
                        lv_batt_charging_msg = {}
                        for item in obj['can_msg']['can_data']:
                            can_data = CAN_DATA[str(item['msg_id'])]
                            pasted_value = json.loads(can_data['pasted_value'])
                            if 'LVBattSOHSUL' in pasted_value: lv_batt_charging_msg['lv_batt_soh_sul'] = pasted_value.get('LVBattSOHSUL')
                            if 'LVBattSOHLAM' in pasted_value: lv_batt_charging_msg['lv_batt_soh_lam'] = pasted_value.get('LVBattSOHLAM')
                            if 'LVBattSOHCOR' in pasted_value: lv_batt_charging_msg['lv_batt_soh_cor'] = pasted_value.get('LVBattSOHCOR')
                            if 'LVBattSOHSULSts' in pasted_value: lv_batt_charging_msg['lv_batt_soh_sul_sts'] = pasted_value.get('LVBattSOHSULSts')
                            if 'LVBattSOHLAMSts' in pasted_value: lv_batt_charging_msg['lv_batt_soh_lam_sts'] = pasted_value.get('LVBattSOHLAMSts')
                            if 'LVBattSOHCORSts' in pasted_value: lv_batt_charging_msg['lv_batt_soh_cor_sts'] = pasted_value.get('LVBattSOHCORSts')
                            if 'LVBattSOC' in pasted_value: lv_batt_charging_msg['lv_batt_soc'] = pasted_value.get('LVBattSOC')
                            if 'LVBattSOCSts' in pasted_value: lv_batt_charging_msg['lv_batt_soc_sts'] = pasted_value.get('LVBattSOCSts')
                            if 'LVBattSOHSUL' in pasted_value: lv_batt_charging_msg['lv_batt_customer_id'] = pasted_value.get('LVBattCustomerID')
                    else:  # 通过特殊事件上报
                        lv_batt_charging_msg = obj
                    status_lv_battery_in_message = formator.to_mysql_status_lv_battery(lv_batt_charging_msg)
                    assert_equal(status_lv_battery_in_mysql, status_lv_battery_in_message)

            elif table == 'history_lv_battery':
                with allure.step("校验 lv_battery 信息存入Mysql的 history_lv_battery 表"):
                    history_lv_battery_in_mysql = self.mysql.fetch_one('history_lv_battery',
                                                                   {"vehicle_id": self.vid,
                                                                    "sample_time": timestamp_to_utc_strtime(sample_ts)},
                                                                   exclude_fields=['id', 'update_time'])
                    if 'can_msg' in obj:  # 通过lv_batt_charging_event事件上报
                        lv_batt_charging_msg = {}
                        for item in obj['can_msg']['can_data']:
                            can_data = CAN_DATA[str(item['msg_id'])]
                            pasted_value = json.loads(can_data['pasted_value'])
                            if 'LVBattSOHSUL' in pasted_value: lv_batt_charging_msg['lv_batt_soh_sul'] = pasted_value.get('LVBattSOHSUL')
                            if 'LVBattSOHLAM' in pasted_value: lv_batt_charging_msg['lv_batt_soh_lam'] = pasted_value.get('LVBattSOHLAM')
                            if 'LVBattSOHCOR' in pasted_value: lv_batt_charging_msg['lv_batt_soh_cor'] = pasted_value.get('LVBattSOHCOR')
                            if 'LVBattSOHSULSts' in pasted_value: lv_batt_charging_msg['lv_batt_soh_sul_sts'] = pasted_value.get('LVBattSOHSULSts')
                            if 'LVBattSOHLAMSts' in pasted_value: lv_batt_charging_msg['lv_batt_soh_lam_sts'] = pasted_value.get('LVBattSOHLAMSts')
                            if 'LVBattSOHCORSts' in pasted_value: lv_batt_charging_msg['lv_batt_soh_cor_sts'] = pasted_value.get('LVBattSOHCORSts')
                            if 'LVBattSOC' in pasted_value: lv_batt_charging_msg['lv_batt_soc'] = pasted_value.get('LVBattSOC')
                            if 'LVBattSOCSts' in pasted_value: lv_batt_charging_msg['lv_batt_soc_sts'] = pasted_value.get('LVBattSOCSts')
                            if 'LVBattSOHSUL' in pasted_value: lv_batt_charging_msg['lv_batt_customer_id'] = pasted_value.get('LVBattCustomerID')
                        history_lv_battery_in_message = formator.to_mysql_history_lv_battery(lv_batt_charging_msg)
                    else:  # 通过特殊事件上报
                        history_lv_battery_in_message = formator.to_mysql_history_lv_battery(obj)
                    assert_equal(history_lv_battery_in_mysql, history_lv_battery_in_message)

            elif table == 'history_modem_event':
                with allure.step("校验 modem_event 信息存入Mysql的 history_modem_event 表"):
                    history_modem_event_in_mysql = self.mysql.fetch_one('history_modem_event',
                                                                   {"vehicle_id": self.vid,
                                                                    "sample_time": timestamp_to_utc_strtime(sample_ts)},
                                                                   exclude_fields=['id', 'update_time'])
                    history_modem_event_in_message = formator.to_mysql_history_modem_event(obj)
                    cgw_did = self.mysql.fetch_one('status_package_version', {'id': self.vid})['package_part_number']
                    history_modem_event_in_message['package_part_num'] = cgw_did
                    assert_equal(history_modem_event_in_mysql, history_modem_event_in_message)

            elif table == 'vehicle_soc_history':
                with allure.step(
                        "校验 power swap的{event_name} 信息存入Mysql的 vehicle_soc_history 表".format(event_name=event_name)):
                    if event_name == 'power_swap_start':
                        # 注意只取了表里的部分字段
                        vehicle_soc_history_in_mysql = self.mysql.fetch_one('vehicle_soc_history',
                                                                        where_model={
                                                                            "vehicle_id": self.vid,
                                                                            "event_type": 2,
                                                                            "event_id": obj['power_swap_id']},
                                                                        fields=['event_id', 'start_battery_id',
                                                                                'start_time', 'start_energy',
                                                                                'start_soc', 'latitude',
                                                                                'longitude']
                                                                        )
                        vehicle_soc_history_in_message = formator.to_mysql_vehicle_soc_history(obj, event_name)
                        if self.cmdopt != "stg_marcopolo":
                            inputs = {
                                "host": self.env['host']['tsp_in'],
                                "path": self.api['data_query']['data_track_newest'].format(vehicle_id=self.vid),
                                "method": "GET",
                                "params": {
                                    #"hash_type": "sha256",
                                    'inquire_time': int(sample_ts / 1000),
                                    'app_id': 10001,
                                    "sign": ""
                                }
                            }
                            response = TSPRequest.request(self.env, inputs)
                            vehicle_soc_history_in_message.update({'latitude': response['data']['track'][0]['latitude'],
                                                                   'longitude': response['data']['track'][0][
                                                                       'longitude']})
                        else:
                            vehicle_soc_history_in_message.update({'latitude': None, 'longitude': None})

                        assert_equal(vehicle_soc_history_in_mysql, vehicle_soc_history_in_message)

                    elif event_name == 'power_swap_end':
                        # 注意只取了表里的部分字段
                        vehicle_soc_history_in_mysql = self.mysql.fetch_one('vehicle_soc_history',
                                                                        where_model={
                                                                            "vehicle_id": self.vid,
                                                                            "event_type": 2,
                                                                            "event_id": obj['power_swap_id']},
                                                                        fields=['event_id', 'end_battery_id',
                                                                                'end_time', 'end_energy', 'end_soc',
                                                                                'status']
                                                                        )
                        vehicle_soc_history_in_message = formator.to_mysql_vehicle_soc_history(obj, event_name)

                        assert_equal(vehicle_soc_history_in_mysql, vehicle_soc_history_in_message)

                    elif event_name == 'power_swap_failure':
                        # 注意只取了表里的部分字段
                        # 目前的逻辑确是多次上报同一个event_id只存第一次的fail reason
                        vehicle_soc_history_in_mysql = self.mysql.fetch_one('vehicle_soc_history',
                                                                        where_model={
                                                                            "vehicle_id": self.vid,
                                                                            "event_type": 2,
                                                                            "event_id": obj['power_swap_id']},
                                                                        fields=['event_id', 'status', 'failure_info']
                                                                        )
                        vehicle_soc_history_in_mysql['failure_info'] = json.loads(
                            vehicle_soc_history_in_mysql['failure_info'])

                        vehicle_soc_history_in_message = formator.to_mysql_vehicle_soc_history(obj, event_name)

                        assert_equal(vehicle_soc_history_in_mysql, vehicle_soc_history_in_message)

                    elif event_name == 'charge_start_event':
                        # 注意只取了表里的部分字段
                        vehicle_soc_history_in_mysql = self.mysql.fetch_one('vehicle_soc_history',
                                                                        where_model={
                                                                            "vehicle_id": self.vid,
                                                                            "event_type": 1,
                                                                            "event_id": obj['charge_id'],
                                                                            "start_time": sample_time},
                                                                        fields=['event_id', 'start_time', 'start_battery_id',
                                                                                'end_battery_id', 'start_energy', 'start_soc',
                                                                                'status', 'charger_type']
                                                                        )
                        vehicle_soc_history_in_message = formator.to_mysql_vehicle_soc_history(obj, event_name)

                        assert_equal(vehicle_soc_history_in_mysql, vehicle_soc_history_in_message)

                    elif event_name == 'charge_end_event':
                        # 注意只取了表里的部分字段
                        vehicle_soc_history_in_mysql = self.mysql.fetch_one('vehicle_soc_history',
                                                                        where_model={
                                                                            "vehicle_id": self.vid,
                                                                            "event_type": 1,
                                                                            "event_id": obj['charge_id'],
                                                                            "end_time": sample_time},
                                                                        fields=['event_id', 'end_time',
                                                                                'end_energy', 'end_soc',
                                                                                # 同一个charge_id的充电结束事件，如果上报多次，经纬度为第一次上报的，保持不变
                                                                                # 'longitude', 'latitude',
                                                                                'is_end']
                                                                        )
                        vehicle_soc_history_in_message = formator.to_mysql_vehicle_soc_history(obj, event_name)

                        assert_equal(vehicle_soc_history_in_mysql, vehicle_soc_history_in_message)

            elif table == 'vehicle_journey_history':
                with allure.step("校验 {event_name} 信息存入Mysql的 vehicle_journey_history 表".format(event_name=event_name)):
                    if event_name == 'journey_start_event':
                        # 注意只取了表里的部分字段
                        vehicle_soc_history_in_mysql = self.mysql.fetch_one('vehicle_journey_history',
                                                                        where_model={
                                                                            "vehicle_id": self.vid,
                                                                            "start_time": timestamp_to_utc_strtime(obj['sample_ts']),
                                                                            "process_id": obj['journey_id']},
                                                                        fields=['journey_id', 'start_soc', 'start_dump_energy',
                                                                                'start_mileage', 'start_remaining_range', 'user_deleted',
                                                                                'user_switch', 'start_longitude', 'start_latitude']
                                                                        )
                        vehicle_soc_history_in_message = formator.to_mysql_vehicle_soc_history(obj, event_name)

                        assert_equal(vehicle_soc_history_in_mysql, vehicle_soc_history_in_message)

                    elif event_name == 'journey_end_event':
                        # 注意只取了表里的部分字段
                        vehicle_soc_history_in_mysql = self.mysql.fetch_one('vehicle_journey_history',
                                                                        where_model={
                                                                            "vehicle_id": self.vid,
                                                                            "end_time": timestamp_to_utc_strtime(obj['sample_ts']),
                                                                            "process_id": obj['journey_id']},
                                                                        fields=['journey_id', 'end_soc', 'end_dump_energy',
                                                                                'end_mileage', 'end_remaining_range', 'user_deleted',
                                                                                'user_switch', 'end_longitude', 'end_latitude'
                                                                                                                'is_end']
                                                                        )
                        vehicle_soc_history_in_message = formator.to_mysql_vehicle_soc_history(obj, event_name)

                        assert_equal(vehicle_soc_history_in_mysql, vehicle_soc_history_in_message)

            elif table == 'history_nfc_op':
                with allure.step("校验 nfc_op 信息存入Mysql的 history_nfc_op 表"):
                    history_nfc_op_in_mysql = self.mysql.fetch_one('history_nfc_op',
                                                               {"vehicle_id": self.vid,
                                                                "key_id": obj['key_id']},
                                                               exclude_fields=['id', 'update_time'])
                    history_nfc_op_in_message = formator.to_mysql_history_nfc_op(obj)
                    assert_equal(history_nfc_op_in_mysql, history_nfc_op_in_message)

            elif table == 'history_ble_op':
                with allure.step("校验 ble_op 信息存入Mysql的 history_ble_op 表"):
                    history_ble_op_in_mysql = self.mysql.fetch_one('history_ble_op',
                                                               {"vehicle_id": self.vid,
                                                                "s_random": obj['s_random']},
                                                               exclude_fields=['id', 'update_time', 'ctrl_cmd_ts'])
                    history_ble_op_in_message = formator.to_mysql_history_ble_op(obj)
                    assert_equal(history_ble_op_in_mysql, history_ble_op_in_message)

            elif table == 'history_nkc_op':
                with allure.step("校验 nkc_nfc_op 信息存入Mysql的 history_nkc_op 表"):
                    history_nkc_nfc_op_in_mysql = self.mysql_rvs_data.fetch_one('history_nkc_op',
                                                                        {"vehicle_id": self.vid,
                                                                         "key_id": obj['key_id']},
                                                                        exclude_fields=['id', 'create_time'])
                    history_nkc_nfc_op_in_message = formator.to_mysql_history_nkc_nfc_op(obj)
                    assert_equal(history_nkc_nfc_op_in_mysql, history_nkc_nfc_op_in_message)

            elif table == 'status_car_key':
                with allure.step("校验 car_key_settings 信息存入Mysql的 status_car_key 表"):
                    car_key_in_mysql = self.mysql.fetch_one('status_car_key',
                                                        {"vehicle_id": self.vid,
                                                         "media_type": obj['media_type']},
                                                        exclude_fields=['id', 'update_time'])
                    car_key_in_message = formator.to_mysql_status_car_key(obj)
                    assert_equal(car_key_in_mysql, car_key_in_message)

            elif table == 'vehicle_data_mock':
                sample_time = time_parse.time_sec_to_strtime(sample_ts)
                vehicle_data_mock_in_mysql = self.mysql.fetch('vehicle_data_mock',
                                                              {"vin": obj['id'],
                                                               "sample_time": sample_time},
                                                              exclude_fields=['id', 'sample_time', 'update_time'])[-1]
                with allure.step("校验 evm_message 信息存入Mysql的 vehicle_data_mock 表"):
                    evm_vehicle_data_mock_in_mysql = {
                        "vin": vehicle_data_mock_in_mysql['vin'],
                        "command": vehicle_data_mock_in_mysql['command'],
                        "attribution": vehicle_data_mock_in_mysql['attribution'],
                    }
                    mock_in_message = formator.to_mysql_vehicle_data_mock(obj, platform, event_name, reissue)
                    assert_equal(evm_vehicle_data_mock_in_mysql, mock_in_message)

                    if 'update' in event_name:
                        with allure.step("校验 evm_message 信息存入Mysql的 vehicle_data_mock 表"):
                            message_in_mysql = json.loads(vehicle_data_mock_in_mysql['message'])
                            dataUnit_in_mysql = message_in_mysql['dataUnit']['reportInfoList']
                            dataUnit_in_message = formator.to_mysql_reportInfoList_in_message(obj)
                            assert_equal(dataUnit_in_mysql[0]['infoBody'], dataUnit_in_message[0])

            elif table == 'status_adas':
                with allure.step("校验 adas np 信息存入Mysql的 status_adas 表"):
                    adas_np_in_message = formator.to_mysql_status_adas(obj)
                    where_model['sample_time'] = adas_np_in_message['sample_time']
                    adas_in_mysql = self.mysql.fetch_one('status_adas', where_model,
                                                     exclude_fields=['update_time'])
                    assert_equal(adas_in_mysql, adas_np_in_message)
            elif table == 'status_body':
                with allure.step("校验 adas np 信息存入Mysql的 status_body 表"):
                    status_body_in_mysql = self.mysql.fetch_one('status_body', where_model,
                                                            exclude_fields=['update_time'])
                    status_body_in_message = formator.to_mysql_status_body(obj)
                    assert_equal(status_body_in_mysql, status_body_in_message)
            elif table == 'status_trip':
                with allure.step("校验 trip 信息存入Mysql的 status_trip表"):
                    status_trip_in_mysql = self.mysql.fetch_one('status_trip', where_model,
                                                            exclude_fields=['update_time'])
                    status_trip_in_message = formator.to_mysql_status_trip(obj)
                    assert_equal(status_trip_in_mysql, status_trip_in_message)
            else:
                raise Exception('table {0} is invalid'.format(table))

    def get_mysql_status_tables(self, tables) -> dict:
        status_data_in_mysql = dict()
        for table in tables:
            status_data_in_mysql[table] = self.mysql.fetch(table, {"id": self.vid})[0]

        return status_data_in_mysql

    def check_cassandra_tables(self, obj, tables, event_name=None, sample_ts=None, domain=None, platform=None, reissue=False, *args, **kwargs):
        if not sample_ts and 'sample_ts' in obj:
            sample_ts = obj['sample_ts']

        cassandra_formator = message_formator.MsgToCassandraFormator(self.vid, sample_ts, self.cmdopt)
        sample_date = datetime.datetime.fromtimestamp(sample_ts / 1000.0).strftime('%Y-%m')

        for table in tables:
            if table == 'vehicle_data':
                with allure.step("校验{0}存入Cassandra的{1}".format(event_name, table)):
                    if event_name == 'ecu_connection_status':
                        # ecu_connection_status
                        event_in_cassandra = self.cassandra.fetch('vehicle_data',
                                                                  {'vehicle_id': self.vid,
                                                                   'sample_date': sample_date,
                                                                   'sample_ts': sample_ts,
                                                                   'msg_type': event_name},
                                                                  fields=tables[table])
                        assert len(event_in_cassandra) == 1
                        event_in_cassandra = event_in_cassandra[0]

                        obj_to_vehicle_data = cassandra_formator.to_vehicle_data(obj, event_name=event_name, redis=self.redis, vid=self.vid, cmdopt=self.cmdopt,
                                                                                 latest_msg_type=kwargs['latest_msg_type'], ecu_type=kwargs['ecu_type'], status=kwargs['status'],
                                                                                 sample_ts=sample_ts, process_id=kwargs['process_id'])
                        assert_equal(event_in_cassandra, obj_to_vehicle_data)
                    elif event_name == 'journey_start_event':
                        event_in_cassandra = self.cassandra.fetch(table,
                                                                  where_model={'vehicle_id': self.vid,
                                                                               'sample_date': sample_date,
                                                                               'sample_ts': sample_ts,
                                                                               'msg_type': event_name
                                                                               },
                                                                  fields=tables[table]
                                                                  )

                        assert len(event_in_cassandra) == 1
                        event_in_cassandra = event_in_cassandra[0]
                        event_in_cassandra['pm25_fil'] = event_in_cassandra.pop('hvac_status')['pm25_fil']
                        if 'btry_pak_info' in event_in_cassandra:
                            assert event_in_cassandra['btry_pak_info']['btry_pak_encoding'][0]['bid'] is not None
                            event_in_cassandra['btry_pak_info']['btry_pak_encoding'][0].pop('bid')
                        obj_to_vehicle_data = cassandra_formator.to_vehicle_data(obj, event_name=event_name)
                        assert_equal(event_in_cassandra, obj_to_vehicle_data)
                    elif event_name == 'nbs_status_change_event':
                        event_in_cassandra = self.cassandra.fetch(table,
                                                                  where_model={'vehicle_id': self.vid,
                                                                               'sample_date': sample_date,
                                                                               'sample_ts': sample_ts,
                                                                               'msg_type': event_name
                                                                               },
                                                                  fields=tables[table]
                                                                  )

                        assert len(event_in_cassandra) == 1
                        event_in_cassandra = event_in_cassandra[0]
                        if 'nbs_status' in event_in_cassandra.keys():
                            if 'discard_nbs_blkage_frnt_le' in event_in_cassandra['nbs_status'].keys():
                                event_in_cassandra['nbs_status'].pop('discard_nbs_blkage_frnt_le')
                            if 'discard_nbs_blkage_frnt_ri' in event_in_cassandra['nbs_status'].keys():
                                event_in_cassandra['nbs_status'].pop('discard_nbs_blkage_frnt_ri')
                            if 'discard_nbs_blkage_re_le' in event_in_cassandra['nbs_status'].keys():
                                event_in_cassandra['nbs_status'].pop('discard_nbs_blkage_re_le')
                            if 'discard_nbs_blkage_re_ri' in event_in_cassandra['nbs_status'].keys():
                                event_in_cassandra['nbs_status'].pop('discard_nbs_blkage_re_ri')
                        obj_to_vehicle_data = cassandra_formator.to_vehicle_data(obj, event_name=event_name)
                        assert_equal(event_in_cassandra, obj_to_vehicle_data)
                    elif event_name == 'bms_power_swap_event':
                        event_in_cassandra = self.cassandra.fetch(table,
                                                                  where_model={'vehicle_id': self.vid,
                                                                               'sample_date': sample_date,
                                                                               'sample_ts': sample_ts,
                                                                               'msg_type': event_name
                                                                               },
                                                                  fields=tables[table]
                                                                  )

                        assert len(event_in_cassandra) == 1
                        dids = []
                        for item in obj['did_data_before']:
                            item['bms_type'] = 0
                            dids.append(item)
                        for item in obj['did_data_after']:
                            item['bms_type'] = 1
                            dids.append(item)
                        obj_to_vehicle_data ={'bms_did_info': dids}
                        assert_equal(event_in_cassandra[0], obj_to_vehicle_data)
                    elif event_name == 'bms_did_event':
                        event_in_cassandra = self.cassandra.fetch(table,
                                                                  where_model={'vehicle_id': self.vid,
                                                                               'sample_date': sample_date,
                                                                               'sample_ts': sample_ts,
                                                                               'msg_type': event_name
                                                                               },
                                                                  fields=tables[table]
                                                                  )

                        assert len(event_in_cassandra) == 1
                        for item in event_in_cassandra[0]['bms_did_info']:
                            del item['bms_type']
                        obj_to_vehicle_data = cassandra_formator.to_vehicle_data(obj, event_name=event_name)
                        assert_equal(event_in_cassandra[0], obj_to_vehicle_data)
                    elif event_name == 'nbs_abort_event':
                        event_in_cassandra = self.cassandra.fetch(table,
                                                                  where_model={'vehicle_id': self.vid,
                                                                               'sample_date': sample_date,
                                                                               'sample_ts': sample_ts,
                                                                               'msg_type': event_name
                                                                               },
                                                                  fields=tables[table]
                                                                  )

                        assert len(event_in_cassandra) == 1
                        obj['can_msg_list'] = obj.pop('can_msg')
                        obj['vehicle_status.vehl_type_dbc'] = obj.pop('dbc_type')
                        obj_to_vehicle_data = cassandra_formator.to_vehicle_data(obj, event_name=event_name)
                        assert_equal(event_in_cassandra[0], obj_to_vehicle_data)
                    elif event_name == 'power_swap_service_periodic':
                        event_in_cassandra = self.cassandra.fetch(table,
                                                                  where_model={'vehicle_id': self.vid,
                                                                               'sample_date': sample_date,
                                                                               'sample_ts': sample_ts,
                                                                               'msg_type': event_name
                                                                               },
                                                                  fields=tables[table]
                                                                  )

                        assert len(event_in_cassandra) == 1
                        obj_to_vehicle_data = cassandra_formator.to_vehicle_data(obj, event_name=event_name)
                        for k in list(event_in_cassandra[0]['power_swap_status'].keys()):
                            if event_in_cassandra[0]['power_swap_status'][k] is None:
                                del event_in_cassandra[0]['power_swap_status'][k]
                        assert_equal(event_in_cassandra[0], obj_to_vehicle_data)
                    elif event_name == 'power_swap_service_event':
                        event_in_cassandra = self.cassandra.fetch(table,
                                                                  where_model={'vehicle_id': self.vid,
                                                                               'sample_date': sample_date,
                                                                               'sample_ts': sample_ts,
                                                                               'msg_type': event_name
                                                                               },
                                                                  fields=tables[table]
                                                                  )

                        assert len(event_in_cassandra) == 1
                        obj_to_vehicle_data = cassandra_formator.to_vehicle_data(obj, event_name=event_name)
                        obj_to_vehicle_data['power_swap_status']['event_type'] = obj_to_vehicle_data.pop('event_type')
                        for k in list(event_in_cassandra[0]['power_swap_status'].keys()):
                            if event_in_cassandra[0]['power_swap_status'][k] is None:
                                del event_in_cassandra[0]['power_swap_status'][k]
                        for k in list(event_in_cassandra[0]['window_status'].keys()):
                            if event_in_cassandra[0]['window_status'][k] is None:
                                del event_in_cassandra[0]['window_status'][k]
                        assert_equal(event_in_cassandra[0], obj_to_vehicle_data)
                    elif event_name == 'sa_batt_status_event':
                        event_in_cassandra = self.cassandra.fetch(table,
                                                                  where_model={'vehicle_id': self.vid,
                                                                               'sample_date': sample_date,
                                                                               'sample_ts': sample_ts,
                                                                               'msg_type': event_name
                                                                               },
                                                                  fields=tables[table]
                                                                  )

                        assert len(event_in_cassandra) == 1
                        event_in_cassandra[0]['sa_batt_health'] = event_in_cassandra[0].pop('sa_batt_health_status')
                        obj_to_vehicle_data = cassandra_formator.to_vehicle_data(obj, event_name=event_name)
                        assert_equal(event_in_cassandra[0], obj_to_vehicle_data)
                    elif event_name == 'wifi_connect_event':
                        event_in_cassandra = self.cassandra.fetch(table,
                                                                  where_model={'vehicle_id': self.vid,
                                                                               'sample_date': sample_date,
                                                                               'sample_ts': sample_ts,
                                                                               'msg_type': event_name
                                                                               },
                                                                  fields=tables[table]
                                                                  )

                        assert len(event_in_cassandra) == 1
                        data = copy.deepcopy(obj)
                        del(data['id'])
                        del(data['version'])
                        del(data['sample_ts'])
                        assert_equal(event_in_cassandra[0]['wifi_connect_status'], data)
                    else:
                        event_in_cassandra = self.cassandra.fetch(table,
                                                                  where_model={'vehicle_id': self.vid,
                                                                               'sample_date': sample_date,
                                                                               'sample_ts': sample_ts,
                                                                               'msg_type': event_name
                                                                               },
                                                                  fields=tables[table]
                                                                  )

                        assert len(event_in_cassandra) == 1
                        event_in_cassandra = event_in_cassandra[0]
                        if 'hvac_status' in event_in_cassandra:
                            event_in_cassandra['hvac_status'].pop('pm25_fil')
                        # if 'trip_status' in event_in_cassandra:
                        #     # (instant_status_resp, periodical_journey_update)当前车机版本不支持字段，验证前临时移除
                        #     event_in_cassandra['trip_status'].pop('hvh_eng_pct')
                        #     event_in_cassandra['trip_status'].pop('trip_id')
                        if 'btry_pak_info' in event_in_cassandra:
                            assert event_in_cassandra['btry_pak_info']['btry_pak_encoding'][0]['bid'] is not None
                            event_in_cassandra['btry_pak_info']['btry_pak_encoding'][0].pop('bid')
                        obj_to_vehicle_data = cassandra_formator.to_vehicle_data(obj, event_name=event_name)
                        if 'can_signal' in event_in_cassandra:
                            if event_in_cassandra['can_signal']:
                                if self.cmdopt == 'test':
                                    for item in event_in_cassandra['can_signal']['can_signal_info']:
                                        item.pop('discard_id')
                            else:
                                event_in_cassandra.pop('can_signal')

                        # if 'can_msg' in event_in_cassandra:
                        #     for item in event_in_cassandra['can_msg']['can_data']:
                        #         item['value'] = json.loads(item['value'])
                        assert_equal(event_in_cassandra, obj_to_vehicle_data)




            elif table == 'vehicle_history':
                with allure.step("校验{0}存入Cassandra的{1}".format(event_name, table)):
                    event_in_cassandra = self.cassandra.fetch(table,
                                                              where_model={'vehicle_id': self.vid,
                                                                           'sample_date': sample_date,
                                                                           'sample_ts': sample_ts,
                                                                           'msg_type': event_name
                                                                           },
                                                              fields=tables[table]
                                                              )
                    assert len(event_in_cassandra) == 1
                    event_in_cassandra = event_in_cassandra[0]
                    obj_to_vehicle_history = cassandra_formator.to_vehicle_history(obj, event_name=event_name)
                    if 'can_msg' in event_in_cassandra:
                        for item in event_in_cassandra['can_msg']['can_data']:
                            item['value'] = json.loads(item['value'])
                    assert_equal(event_in_cassandra, obj_to_vehicle_history)


            elif table == 'driving_data':
                with allure.step("校验{0}存入Cassandra的{1}".format(event_name, table)):
                    if self.cmdopt == 'test':
                        event_in_cassandra = self.cassandra_driving.fetch(table,
                                                                          where_model={'vehicle_id': self.vid,
                                                                                       'sample_date': sample_date,
                                                                                       'sample_ts': sample_ts,
                                                                                       },
                                                                          fields=tables[table]
                                                                          )
                    else:
                        event_in_cassandra = self.cassandra.fetch(table,
                                                                  where_model={'vehicle_id': self.vid,
                                                                               'sample_date': sample_date,
                                                                               'sample_ts': sample_ts,
                                                                               },
                                                                  fields=tables[table]
                                                                  )
                    assert len(event_in_cassandra) == 1
                    event_in_cassandra = event_in_cassandra[0]
                    obj_to_driving_data = cassandra_formator.to_driving_data(obj)
                    assert_equal(event_in_cassandra, obj_to_driving_data)

            elif table == 'evm_message':
                # jenkins时区为utc，而本地为北京时区
                # sample_date = datetime.datetime.fromtimestamp(sample_ts / 1000.0).strftime('%Y-%m-%d-%H')
                sample_date = time_parse.utc_to_local(timestamp=sample_ts / 1000.0, offset_hour=8)
                event_in_cassandra = self.cassandra.fetch(table, where_model={'vin': obj['id'],
                                                                              'attribution': platform,
                                                                              'insert_date': sample_date},
                                                          fields=['vin', 'attribution', 'ack',
                                                                  'domain', 'type', 'message'])[-1]
                with allure.step("校验{0}存入Cassandra的{1}".format(event_name, table)):
                    evm_event_in_cassandra = {
                        "vin": event_in_cassandra['vin'],
                        "attribution": event_in_cassandra['attribution'],
                        "ack": event_in_cassandra['ack'],
                        "domain": event_in_cassandra['domain'],
                        "type": event_in_cassandra['type']
                    }
                    cassandra_formator = message_formator.MsgToCassandraFormator(obj['id'], sample_ts)
                    obj_to_evm_message = cassandra_formator.to_evm_message(obj, event_name, domain, platform, reissue)
                    assert_equal(evm_event_in_cassandra, obj_to_evm_message)

                    if 'update' in event_name:
                        with allure.step("校验{0}存入Cassandra的{1}".format(event_name, table)):
                            cassandra_formator = message_formator.MsgToCassandraFormator(obj['id'], sample_ts)
                            message_in_cassandra = json.loads(event_in_cassandra['message'])
                            dataUnit_in_cassandra = message_in_cassandra['dataUnit']['reportInfoList']
                            obj_to_evm_dataUnit = cassandra_formator.to_reportInfoList_in_message(obj)
                            assert_equal(dataUnit_in_cassandra[0]['infoBody'], obj_to_evm_dataUnit[0])

    def check_mongodb_collections(self, obj, collections: list, event_name=None, sample_ts=None):
        if not sample_ts and 'sample_ts' in obj:
            sample_ts = obj['sample_ts']
        mongodb_formator = message_formator.MsgToMongodbFormator(self.vid, sample_ts)

        for collection in collections:
            if collection == 'vehicle_position':
                with allure.step("校验 position信息存入mongodb.vehicle_position"):
                    vehicle_position_in_mongodb = self.mongodb.find('vehicle_position', {"_id": self.vid})[0]
                    vehicle_position_in_msg = mongodb_formator.to_vehicle_position(obj['position_status'])
                    assert_equal(vehicle_position_in_mongodb, vehicle_position_in_msg)


            elif collection == 'can_msg':
                with allure.step("校验 can msg信息存入mongodb.can_msg"):
                    for item in obj['can_msg']['can_data']:
                        can_msg_in_mongodb = \
                            self.mongodb.find('can_msg', {"_id": self.vid + '_' + str(item['msg_id'])})[0]
                        can_msg_in_msg = mongodb_formator.to_can_msg(item)
                        assert_equal(can_msg_in_mongodb, can_msg_in_msg)

    def check_redis(self, obj, keys, event_name=None, clear_none=False, sample_ts=None):
        if not sample_ts and 'sample_ts' in obj:
            sample_ts = obj['sample_ts']
        redis_formator = message_formator.MsgToRedisFormator(self.vid, sample_ts)
        remote_vehicle_redis_key_front = self.redis_key_front['remote_vehicle']
        key_front = remote_vehicle_redis_key_front + ':vehicle_status:' + self.vid
        for key in keys:
            if key == 'PositionStatus':
                with allure.step("校验 position_status 信息存入Redis的 PositionStatus"):
                    key = key_front + ':PositionStatus'
                    status_position_in_redis = self.redis.get(key)
                    status_position_in_redis = json.loads(status_position_in_redis)
                    status_position_in_message = redis_formator.to_position_status(obj.get('position_status'),
                                                                                   env=self.cmdopt)
                    if clear_none:
                        status_position_in_message = self._clear_none(status_position_in_message)
                    assert_equal(status_position_in_redis, status_position_in_message)

            elif key == 'DoorStatus':
                with allure.step("校验 door_status 信息存入Redis的 DoorStatus"):
                    key = key_front + ':DoorStatus'
                    status_door_in_redis = self.redis.get(key)
                    status_door_in_redis = json.loads(status_door_in_redis)
                    status_door_in_message = redis_formator.to_door_status(obj.get('door_status'))
                    if clear_none:
                        status_door_in_message = self._clear_none(status_door_in_message)
                    assert_equal(status_door_in_redis, status_door_in_message)

            elif key == 'DrivingData':
                with allure.step("校验 driving_status 信息存入Redis的 DrivingData"):
                    key = key_front + ':DrivingData'
                    status_driving_in_redis = self.redis.get(key)
                    status_driving_in_redis = json.loads(status_driving_in_redis)
                    if status_driving_in_redis.get('max_speed') != None:
                        status_driving_in_redis['max_speed'] = str(status_driving_in_redis.get('max_speed')).split('.')[
                            0]
                    if status_driving_in_redis.get('average_speed') != None:
                        status_driving_in_redis['average_speed'] = \
                            str(status_driving_in_redis['average_speed']).split('.')[0]
                    if status_driving_in_redis.get('min_speed') != None:
                        status_driving_in_redis['min_speed'] = str(status_driving_in_redis['min_speed']).split('.')[0]
                    status_driving_in_message = redis_formator.to_driving_data(obj.get('driving_data'))
                    if clear_none:
                        status_driving_in_message = self._clear_none(status_driving_in_message)
                    assert_equal(status_driving_in_redis, status_driving_in_message)

            elif key == 'TyreStatus':
                with allure.step("校验 tyre_status 信息存入Redis的 TyreStatus"):
                    key = key_front + ':TyreStatus'
                    status_tyre_in_redis = self.redis.get(key)
                    status_tyre_in_redis = json.loads(status_tyre_in_redis)
                    status_tyre_in_message = redis_formator.to_tyre_status(obj.get('tyre_status'))
                    if clear_none:
                        status_tyre_in_message = self._clear_none(status_tyre_in_message)
                    assert_equal(status_tyre_in_redis, status_tyre_in_message)

            elif key == 'OccupantStatus':
                with allure.step("校验 occupant_status 信息存入Redis的 OccupantStatus"):
                    key = key_front + ':OccupantStatus'
                    status_occupant_in_redis = self.redis.get(key)
                    status_occupant_in_redis = json.loads(status_occupant_in_redis)
                    status_occupant_in_message = redis_formator.to_occupant_status(obj.get('occupant_status'))
                    if clear_none:
                        status_occupant_in_message = self._clear_none(status_occupant_in_message)
                    assert_equal(status_occupant_in_redis, status_occupant_in_message)

            elif key == 'BmsStatus':
                with allure.step("校验 bms_status 信息存入Redis的 BmsStatus"):
                    key = key_front + ':BmsStatus'
                    status_bms_in_redis = self.redis.get(key)
                    status_bms_in_redis = json.loads(status_bms_in_redis)
                    if status_bms_in_redis.get('update_time'):
                        del status_bms_in_redis['update_time']
                    status_bms_in_redis['health_status'] = str(status_bms_in_redis['health_status']).split('.')[0]
                    status_bms_in_redis['chrg_pwr_lmt'] = str(status_bms_in_redis['chrg_pwr_lmt']).split('.')[0]
                    status_bms_in_redis['dischrg_pwr_lmt'] = str(status_bms_in_redis['dischrg_pwr_lmt']).split('.')[0]
                    status_bms_in_redis['avg_temp'] = str(status_bms_in_redis['avg_temp']).split('.')[0]
                    status_bms_in_redis['avg_cell_volt'] = str(status_bms_in_redis['avg_cell_volt']).split('.')[0]
                    status_bms_in_redis['in_coolant_temp'] = str(status_bms_in_redis['in_coolant_temp']).split('.')[0]
                    status_bms_in_redis['out_coolant_temp'] = str(status_bms_in_redis['out_coolant_temp']).split('.')[0]
                    status_bms_in_message = redis_formator.to_bms_status(obj.get('bms_status'))
                    if clear_none:
                        status_bms_in_message = self._clear_none(status_bms_in_message)
                    assert_equal(status_bms_in_redis, status_bms_in_message)

            elif key == 'SocStatus':
                with allure.step("校验 soc_status 信息存入Redis的  BmsStatus"):
                    key = key_front + ':SocStatus'
                    status_soc_in_redis = self.redis.get(key)
                    status_soc_in_redis = json.loads(status_soc_in_redis)
                    status_soc_in_redis['sin_battery_hist_temp'] = None
                    status_soc_in_redis['sin_battery_lwst_temp'] = None
                    # status_soc_in_redis['chg_subsys_len'] = None
                    # status_soc_in_redis['battery_id'] = None
                    status_soc_in_redis['battery_cap'] = str(status_soc_in_redis['battery_cap']).split('.')[0]
                    status_soc_in_redis['hivolt_battery_current'] = \
                        str(status_soc_in_redis['hivolt_battery_current']).split('.')[0]
                    status_soc_in_redis['dump_energy'] = str(status_soc_in_redis['dump_energy']).split('.')[0]
                    if status_soc_in_redis.get('in_volt_ac'):
                        status_soc_in_redis['in_volt_ac'] = str(status_soc_in_redis['in_volt_ac']).split('.')[0]
                    if status_soc_in_redis.get('in_volt_dc'):
                        status_soc_in_redis['in_volt_dc'] = str(status_soc_in_redis['in_volt_dc']).split('.')[0]
                    if status_soc_in_redis.get('in_curnt_ac'):
                        status_soc_in_redis['in_curnt_ac'] = str(status_soc_in_redis['in_curnt_ac']).split('.')[0]
                    status_soc_in_redis['btry_pak_lst'][0]['btry_pak_voltage'] = \
                        str(status_soc_in_redis['btry_pak_lst'][0]['btry_pak_voltage']).split('.')[0]
                    status_soc_in_redis['btry_pak_lst'][0]['btry_pak_curnt'] = \
                        str(status_soc_in_redis['btry_pak_lst'][0]['btry_pak_curnt']).split('.')[0]
                    soc_battery_charge_dict = {}
                    soc_status = obj.get('soc_status')
                    battert_status = obj.get('battery_package_info')
                    charging_info = obj.get('charging_info')
                    if soc_status != None:
                        soc_battery_charge_dict['soc_status'] = soc_status
                    if battert_status != None:
                        soc_battery_charge_dict['battery_package_info'] = battert_status
                    if charging_info != None:
                        soc_battery_charge_dict['charging_info'] = charging_info
                    status_soc_in_message = redis_formator.to_soc_status(soc_battery_charge_dict)
                    # journey_update_event
                    # if event_name in ['journey_end_event', 'journey_start_event', 'charge_end_event',
                    #                   'journey_update_event', 'charge_update_event']:
                    #     status_soc_in_redis['max_soc'] = 100.0
                    #     status_soc_in_message['btry_pak_lst'][0]['chgSubsysEncoding'] = None
                    # if event_name == 'charge_start_event':
                    #     status_soc_in_redis['max_soc'] = 100.0
                    # if event_name == 'journey_update_event':
                    #     status_soc_in_redis['charger_type'] = None
                    #     status_soc_in_redis['in_volt_ac'] = None
                    #     status_soc_in_redis['in_volt_dc'] = None
                    #     status_soc_in_redis['in_curnt_ac'] = None
                    #     status_soc_in_redis['estimate_charge_time'] = None
                    if clear_none:
                        status_soc_in_message = self._clear_none(status_soc_in_message)
                        status_soc_in_redis = self._clear_none(status_soc_in_redis)
                    # if event_name == 'journey_start_event':
                    #     if 'chgSubsysEncoding' in status_soc_in_redis['btry_pak_lst'][0].keys():
                    #         status_soc_in_redis['btry_pak_lst'][0].pop('chgSubsysEncoding')
                    # if event_name in ['journey_start_event', 'journey_end_event', 'charge_start_event', 'journey_update_event', 'charge_update_event', 'charge_end_event']:
                    #     status_soc_in_redis['max_soc'] = 100.0
                    redis_keys = status_soc_in_redis.keys()
                    msg_keys = status_soc_in_message.keys()
                    for key in ['btry_pak_lst', 'battery_id', 'chg_subsys_len', 'charger_type', 'estimate_charge_time', 'in_curnt_ac', 'in_volt_ac', 'in_volt_dc', 'max_soc']:
                        if key == 'btry_pak_lst':
                            btry_pak_lst_redis_keys = status_soc_in_redis['btry_pak_lst'][0].keys()
                            btry_pak_lst_msg_keys = status_soc_in_message['btry_pak_lst'][0].keys()
                            if 'chgSubsysEncoding' in btry_pak_lst_msg_keys and 'chgSubsysEncoding' not in btry_pak_lst_redis_keys:
                                status_soc_in_message['btry_pak_lst'][0].pop('chgSubsysEncoding')
                            if 'nio_encoding' in btry_pak_lst_redis_keys:
                                status_soc_in_redis['btry_pak_lst'][0].pop('nio_encoding')
                        if key in redis_keys and key not in msg_keys:
                            status_soc_in_redis.pop(key)
                    assert_equal(status_soc_in_redis, status_soc_in_message)

            elif key == 'HvacStatus':
                with allure.step("校验 hvac_status 信息存入Redis的 HvacStatus"):
                    key = key_front + ':HvacStatus'
                    status_havc_in_redis = self.redis.get(key)
                    status_hvac_in_redis = json.loads(status_havc_in_redis)
                    status_hvac_in_message = redis_formator.to_hvac_status(obj.get('hvac_status'))
                    if clear_none:
                        status_hvac_in_message = self._clear_none(status_hvac_in_message)
                    status_hvac_in_message['ccu_cbn_pre_ac_ena_sts'] = True if status_hvac_in_message.pop('ccu_cbn_pre_ac_ena_sts') else False
                    status_hvac_in_message['ccu_cbn_pre_aqs_ena_sts'] = True if status_hvac_in_message.pop('ccu_cbn_pre_aqs_ena_sts') else False
                    if 'pm25_fil' in status_hvac_in_redis:
                        status_hvac_in_redis.pop('pm25_fil')
                    assert_equal(status_hvac_in_redis, status_hvac_in_message)

            elif key == 'ExteriorStatus':
                with allure.step("校验 vehicle_status 信息存入Redis的 ExteriorStatus"):
                    key = key_front + ':ExteriorStatus'
                    status_vehicle_in_redis = self.redis.get(key)
                    status_vehicle_in_redis = json.loads(status_vehicle_in_redis)
                    if status_vehicle_in_redis.get('speed') != None:
                        status_vehicle_in_redis['speed'] = str(status_vehicle_in_redis['speed']).split('.')[0]
                    if status_vehicle_in_redis.get('total_voltage') != None:
                        status_vehicle_in_redis['total_voltage'] = \
                            str(status_vehicle_in_redis['total_voltage']).split('.')[0]
                    if status_vehicle_in_redis.get('total_current') != None:
                        status_vehicle_in_redis['total_current'] = \
                            str(status_vehicle_in_redis['total_current']).split('.')[0]
                        if status_vehicle_in_redis['total_current'] == '-0':
                            status_vehicle_in_redis['total_current'] = '0'
                    status_vehicle_in_message = redis_formator.to_vehicle_status(obj.get('vehicle_status'))
                    if clear_none:
                        status_vehicle_in_message = self._clear_none(status_vehicle_in_message)
                    assert_equal(status_vehicle_in_redis, status_vehicle_in_message)

            elif key == 'LightStatus':
                with allure.step("校验 light_status 信息存入Redis的 LightStatus"):
                    key = key_front + ':LightStatus'
                    status_light_in_redis = self.redis.get(key)
                    status_light_in_redis = json.loads(status_light_in_redis)
                    status_light_in_message = redis_formator.to_light_status(obj.get('light_status'))
                    if clear_none:
                        status_light_in_message = self._clear_none(status_light_in_message)
                    assert_equal(status_light_in_redis, status_light_in_message)

            elif key == 'ExtremumData':
                with allure.step("校验 extremum_data 信息存入Redis的 ExtremumData"):
                    key = key_front + ':ExtremumData'
                    status_extremum_in_redis = self.redis.get(key)
                    status_extremum_in_redis = json.loads(status_extremum_in_redis)
                    status_extremum_in_redis['sin_btry_hist_volt'] = \
                        str(status_extremum_in_redis['sin_btry_hist_volt']).split('.')[0]
                    status_extremum_in_redis['sin_btry_lwst_volt'] = \
                        str(status_extremum_in_redis['sin_btry_lwst_volt']).split('.')[0]
                    status_extremum_in_redis['highest_temp'] = str(status_extremum_in_redis['highest_temp']).split('.')[
                        0]
                    status_extremum_in_redis['lowest_temp'] = str(status_extremum_in_redis['lowest_temp']).split('.')[0]
                    status_extremum_in_message = redis_formator.to_extremum_data(obj.get('extremum_data'))
                    if clear_none:
                        status_extremum_in_message = self._clear_none(status_extremum_in_message)
                    assert_equal(status_extremum_in_redis, status_extremum_in_message)

            elif key == 'WindowStatus':
                with allure.step("校验 window_status 信息存入Redis的 WindowStatus"):
                    key = key_front + ':WindowStatus'
                    status_window_in_redis = self.redis.get(key)
                    status_window_in_redis = json.loads(status_window_in_redis)
                    status_window_in_message = redis_formator.to_window_status(obj.get('window_status'))
                    if clear_none:
                        status_window_in_message = self._clear_none(status_window_in_message)
                    assert_equal(status_window_in_redis, status_window_in_message)
            elif key == 'HeatingStatus':
                with allure.step("校验 heating_status 信息存入Redis的 HeatingStatus"):
                    key = key_front + ':HeatingStatus'
                    status_heating_in_redis = self.redis.get(key)
                    status_heating_in_redis = json.loads(status_heating_in_redis)
                    status_heating_in_message = redis_formator.to_heating_status(obj.get('heating_status'))
                    if clear_none:
                        status_heating_in_message = self._clear_none(status_heating_in_message)
                    assert_equal(status_heating_in_redis, status_heating_in_message)
            elif key == 'DrivingMotor':
                with allure.step("校验 driving_motor 信息存入Redis的 DrivingMotor"):
                    key = key_front + ':DrivingMotor'
                    status_driving_motor_in_redis = self.redis.get(key)
                    status_driving_motor_in_redis = json.loads(status_driving_motor_in_redis)
                    if status_driving_motor_in_redis.get('driving_motors') != None:
                        for i in range(len(status_driving_motor_in_redis.get('driving_motors'))):
                            status_driving_motor_in_redis.get('driving_motors')[i]['drvmotr_contl_dc_bus_curnt'] = \
                                str(status_driving_motor_in_redis.get('driving_motors')[i].get(
                                    'drvmotr_contl_dc_bus_curnt')).split('.')[0]
                    status_driving_motor_in_message = redis_formator.to_driving_motor(obj.get('driving_motor'))
                    if clear_none:
                        status_driving_motor_in_message = self._clear_none(status_driving_motor_in_message)
                    assert_equal(status_driving_motor_in_redis, status_driving_motor_in_message)
            elif key.startswith('charge_push_start'):
                key = f'{remote_vehicle_redis_key_front}:charge_push:{self.vid}:{key.split(".")[1]}:start'
                assert self.redis.get(key)
            elif key.startswith('charge_push_end'):
                key = f'{remote_vehicle_redis_key_front}:charge_push:{self.vid}:{key.split(".")[1]}:end'
                assert self.redis.get(key)
            else:
                raise Exception('ERROR')

    def check_alarm_signal_kafka(self, obj, kafka_msg):
        if 'repair' in kafka_msg['vehicle_status'].keys():
            kafka_msg['vehicle_status'].pop('repair')
        alarm_data_in_msg = {}
        alarm_data_in_msg['vehicle_status'] = {}

        if 'marcopolo' not in self.cmdopt:
            # 校验Kafka内有位置信息
            result = wgs84_to_gcj02(obj['sample_points']['position_status']['longitude'], obj['sample_points']['position_status']['latitude'])
            alarm_data_in_msg['vehicle_status']['longitude'] = result[0]
            alarm_data_in_msg['vehicle_status']['latitude'] = result[1]
        if 'marcopolo' not in self.cmdopt:
            # 校验Kafka内有电池包信息
            key = self.redis_key_front['remote_vehicle'] + ':vehicle_status:' + self.vid + ':SocStatus'
            status_soc_in_redis = json.loads(self.redis.get(key))
            alarm_data_in_msg['vehicle_status']['nio_battery_id'] = status_soc_in_redis['battery_id']
        # 校验Kafka内有维修状态信息
        alarm_data_in_msg['vehicle_status']['ntester'] = obj['sample_points']['vehicle_status']['ntester']

        # 校验Kafka存原始的can信息，而不是WTI code
        alarm_data_in_msg['signals'] = obj['alarm_signal']['signal_int']

        alarm_data_in_msg['sample_time'] = obj['sample_ts']
        alarm_data_in_msg['vehicle_id'] = self.vid
        if 'marcopolo' not in self.cmdopt:
            alarm_data_in_msg['vin'] = self.vin

        # 不再校验是否含有bid
        if 'bid' in alarm_data_in_msg['vehicle_status']:
            alarm_data_in_msg['vehicle_status'].pop('bid')
        if 'bid' in kafka_msg['vehicle_status']:
            kafka_msg['vehicle_status'].pop('bid')

        assert_equal(alarm_data_in_msg, kafka_msg)
        pass
