# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/7/20 20:47
# @File:views.py
import json
import multiprocessing
import sys
import time
from multiprocessing import Queue

from django.http import JsonResponse
from django.views import View

from liquid.liquid_data import liquid_real_time_key, liquid_alarm_key
from liquid.liquid_mqtt import start_can_send_process
from utils.log import log

liquid_rep_json = {"real_msg": {}, "alarm_msg": {}}  # 保存发送的数据，每次请求
liquid_start_server_flag = False
liquid_p = ""
liquid_q = Queue()


class LiquidView(View):

    def post(self, request):
        data = {
            'result_code': '0',
            'message': "OK"
        }
        post_body = json.loads(request.body)
        try:
            liquid_covert_key_to_msg(post_body)
        except ValueError:
            _, exc_value, _ = sys.exc_info()
            log.error(f"<Liquid>:Post请求实时信息数据初始化异常:{str(exc_value)}")
            return JsonResponse({'result_code': "3", 'message': f'数据初始化异常，请排查报错的数据类型, {exc_value}', })
        global liquid_p, liquid_q, liquid_rep_json, liquid_start_server_flag
        if not liquid_start_server_flag or (isinstance(liquid_p, multiprocessing.Process) and not liquid_p.is_alive()):
            liquid_p = multiprocessing.Process(target=start_can_send_process, args=(liquid_q,))
            liquid_p.daemon = True
            liquid_p.start()
            log.info(f"<Liquid>:create liquid mqtt client back process success, pid:{liquid_p.pid}")
            liquid_start_server_flag = True
        log.info("<Liquid>:update liquid data success...")
        liquid_q.put(liquid_rep_json)
        return JsonResponse(data)

    def get(self, request, *args):
        data = {
            'result_code': '0',
            'message': 'OK',
        }
        global liquid_p, liquid_start_server_flag
        if isinstance(liquid_p, multiprocessing.Process) and not liquid_p.is_alive():
            log.info("<Liquid>:pid process close")
            liquid_start_server_flag = False
            liquid_p.terminate()
            liquid_p.join(timeout=10)
            time.sleep(1)
        else:
            log.error("<Liquid>:kill liquid process not exists")
            data["result_code"] = "2"
            data["message"] = "kill liquid process not exists "
        return JsonResponse(data)


def liquid_covert_key_to_msg(post_body):
    """

    :param post_body:
    :return:
    """
    global liquid_rep_json
    liquid_data = post_body.get("liquid", {})
    data = liquid_data.get("inside_loop", {})
    data.update(liquid_data.get("lc_params", {}))
    data.update(liquid_data.get("set_data", {}))
    data.update(liquid_data.get("outside1_loop", {}))
    data.update(liquid_data.get("outside2_loop", {}))
    data.update(liquid_data.get("station_rt_status", {}))
    data.update(liquid_data.get("alarm_info", {}))

    # print(data)

    def update(key, val):
        if key in data:
            return data[key]
        elif liquid_real_time_key.get(key) in liquid_rep_json['real_msg']:
            return liquid_rep_json["real_msg"][liquid_real_time_key.get(key)]
        elif liquid_alarm_key.get(key) in liquid_rep_json['alarm_msg']:
            return liquid_rep_json["alarm_msg"][liquid_alarm_key.get(key)]
        else:
            return val

    liquid_rep_json["real_msg"]["power_protection_switch"] = int(update("300001", 0))
    liquid_rep_json["real_msg"]["big_tank_low_level_switch"] = int(update("300002", 0))
    liquid_rep_json["real_msg"]["big_tank_high_level_switch"] = int(update("300003", 0))
    liquid_rep_json["real_msg"]["drain_valve_switch"] = int(update("300004", 0))
    liquid_rep_json["real_msg"]["inner_loop_flow_switch"] = int(update("300005", 0))
    liquid_rep_json["real_msg"]["heating_stage_started"] = int(update("300006", 0))
    liquid_rep_json["real_msg"]["heating_stage_fault"] = int(update("300007", 0))
    liquid_rep_json["real_msg"]["compressor_1_started"] = int(update("300008", 0))
    liquid_rep_json["real_msg"]["compressor_2_started"] = int(update("300009", 0))
    liquid_rep_json["real_msg"]["compressor_1_power_protection"] = int(update("300010", 0))
    liquid_rep_json["real_msg"]["compressor_2_power_protection"] = int(update("300011", 0))
    liquid_rep_json["real_msg"]["pump_1_frequency_fault"] = int(update("300012", 0))
    liquid_rep_json["real_msg"]["pump_1_frequency_feedback"] = float(update("300013", 0))
    liquid_rep_json["real_msg"]["pump_1_started"] = int(update("300014", 0))
    liquid_rep_json["real_msg"]["pump_2_frequency_feedback"] = float(update("300015", 0))
    liquid_rep_json["real_msg"]["pump_2_frequency_fault"] = int(update("300016", 0))
    liquid_rep_json["real_msg"]["pump_2_started"] = int(update("300017", 0))
    liquid_rep_json["real_msg"]["pump_3_frequency_fault"] = int(update("300018", 0))
    liquid_rep_json["real_msg"]["pump_3_frequency_feedback"] = int(update("300019", 0))
    liquid_rep_json["real_msg"]["pump_3_started"] = int(update("300020", 0))
    liquid_rep_json["real_msg"]["fan_1_frequency_fault"] = int(update("300021", 0))
    liquid_rep_json["real_msg"]["fan_1_frequency_feedback"] = int(update("300022", 0))
    liquid_rep_json["real_msg"]["fan_1_started"] = int(update("300023", 0))
    liquid_rep_json["real_msg"]["fan_2_frequency_fault"] = int(update("300024", 0))
    liquid_rep_json["real_msg"]["fan_2_frequency_feedback"] = int(update("300025", 0))
    liquid_rep_json["real_msg"]["fan_2_started"] = int(update("300026", 0))
    liquid_rep_json["real_msg"]["press_meter_1"] = float(update("300500", 0))
    liquid_rep_json["real_msg"]["press_meter_2"] = float(update("300501", 0))
    liquid_rep_json["real_msg"]["tank_temp"] = float(update("300502", 0))
    liquid_rep_json["real_msg"]["tank_level"] = float(update("300503", 0))
    liquid_rep_json["real_msg"]["front_backwater_temp"] = float(update("300504", 0))
    liquid_rep_json["real_msg"]["back_backwater_temp"] = float(update("300505", 0))
    liquid_rep_json["real_msg"]["flow_meter_1"] = float(update("300506", 0))
    liquid_rep_json["real_msg"]["flow_meter_2"] = float(update("300507", 0))
    liquid_rep_json["real_msg"]["electric_cabinet_temp"] = float(update("300508", 0))
    liquid_rep_json["real_msg"]["exhaust_1_temp"] = float(update("300509", 0))
    liquid_rep_json["real_msg"]["exhaust_2_temp"] = float(update("300510", 0))
    liquid_rep_json["real_msg"]["compressor_1_pressure_low"] = float(update("300511", 0))
    liquid_rep_json["real_msg"]["compressor_2_pressure_low"] = float(update("300512", 0))
    liquid_rep_json["real_msg"]["compressor_1_pressure_high"] = float(update("300513", 0))
    liquid_rep_json["real_msg"]["compressor_2_pressure_high"] = float(update("300514", 0))
    liquid_rep_json["real_msg"]["exchanger_temp"] = float(update("300515", 0))
    liquid_rep_json["real_msg"]["software_version"] = str(update("30", "4.0.8"))
    liquid_rep_json["real_msg"]["manufacturer"] = int(update("31", 4))
    liquid_rep_json["real_msg"]["hardware_version"] = str(update("hardware_version", "A0.0"))

    liquid_rep_json["real_msg"]["frequency_of_1_fan"] = int(update("frequency_of_1_fan", 0))
    liquid_rep_json["real_msg"]["frequency_of_1_pump"] = float(update("frequency_of_1_pump", 0.0))
    liquid_rep_json["real_msg"]["frequency_of_2_fan"] = int(update("frequency_of_2_fan", 0))
    liquid_rep_json["real_msg"]["frequency_of_2_pump"] = float(update("frequency_of_2_pump", 0.0))
    liquid_rep_json["real_msg"]["frequency_of_3_pump"] = int(update("frequency_of_3_pump", 0))
    liquid_rep_json["real_msg"]["higher_limit_setting_temp_of_tank"] = int(
        update("higher_limit_setting_temp_of_tank", 26))
    liquid_rep_json["real_msg"]["lower_limit_setting_temp_of_tank"] = int(
        update("lower_limit_setting_temp_of_tank", 18))
    liquid_rep_json["real_msg"]["middle_limit_setting_temp_of_tank"] = int(
        update("middle_limit_setting_temp_of_tank", 22))
    liquid_rep_json["real_msg"]["remote_reset"] = int(update("remote_reset", 0))
    liquid_rep_json["real_msg"]["remote_start_cooling_system"] = int(update("remote_start_cooling_system", 0))
    liquid_rep_json["real_msg"]["set_cooling_system_in_manual_mode"] = int(
        update("set_cooling_system_in_manual_mode", 0))
    liquid_rep_json["real_msg"]["set_cooling_system_in_remote_mode"] = int(
        update("set_cooling_system_in_remote_mode", 1))
    liquid_rep_json["real_msg"]["start_1_fan"] = int(update("start_1_fan", 0))
    liquid_rep_json["real_msg"]["start_1_pump"] = int(update("start_1_pump", 0))
    liquid_rep_json["real_msg"]["start_2_fan"] = int(update("start_2_fan", 0))
    liquid_rep_json["real_msg"]["start_2_pump"] = int(update("start_2_pump", 0))
    liquid_rep_json["real_msg"]["start_3_pump"] = int(update("start_3_pump", 0))

    liquid_rep_json["alarm_msg"]["low_level_protection_of_tank_trigger"] = int(update("700400", 0))
    liquid_rep_json["alarm_msg"]["high_level_protection_of_tank_trigger"] = int(update("700401", 0))
    liquid_rep_json["alarm_msg"]["tank_level_is_low"] = int(update("700402", 0))
    liquid_rep_json["alarm_msg"]["tank_level_is_high"] = int(update("700403", 0))
    liquid_rep_json["alarm_msg"]["temp_of_tank_is_too_high_to_stop_pump"] = int(update("700404", 0))
    liquid_rep_json["alarm_msg"]["temp_sensor_of_tank_fault"] = int(update("700405", 0))
    liquid_rep_json["alarm_msg"]["level_sensor_of_tank_fault"] = int(update("700406", 0))
    liquid_rep_json["alarm_msg"]["low_level_swtich_mismatching_level_meter"] = int(update("700407", 0))
    liquid_rep_json["alarm_msg"]["high_level_swtich_mismatching_level_meter"] = int(update("700408", 0))
    liquid_rep_json["alarm_msg"]["flow_meter_1_fault"] = int(update("700409", 0))
    liquid_rep_json["alarm_msg"]["flow_meter_2_fault"] = int(update("700410", 0))
    liquid_rep_json["alarm_msg"]["press_meter_1_fault"] = int(update("700411", 0))
    liquid_rep_json["alarm_msg"]["press_meter_2_fault"] = int(update("700412", 0))
    liquid_rep_json["alarm_msg"]["backwater_temp_sensor_1_fault"] = int(update("700413", 0))
    liquid_rep_json["alarm_msg"]["backwater_temp_sensor_2_fault"] = int(update("700414", 0))
    liquid_rep_json["alarm_msg"]["solenoid_valve_1_open_failed"] = int(update("700415", 0))
    liquid_rep_json["alarm_msg"]["solenoid_valve_1_close_failed"] = int(update("700416", 0))
    liquid_rep_json["alarm_msg"]["solenoid_valve_2_open_failed"] = int(update("700417", 0))
    liquid_rep_json["alarm_msg"]["solenoid_valve_2_close_failed"] = int(update("700418", 0))
    liquid_rep_json["alarm_msg"]["drain_valve_switch_is_opened"] = int(update("700419", 0))
    liquid_rep_json["alarm_msg"]["heating_stage_is_abnormal"] = int(update("700420", 0))
    liquid_rep_json["alarm_msg"]["heating_stage_contactor_is_abnormal"] = int(update("700421", 0))
    liquid_rep_json["alarm_msg"]["flow_protection_of_inner_loop_trigger"] = int(update("700422", 0))
    liquid_rep_json["alarm_msg"]["high_press_of_1_compressor_trigger"] = int(update("700423", 0))
    liquid_rep_json["alarm_msg"]["low_press_of_1_compressor_trigger"] = int(update("700424", 0))
    liquid_rep_json["alarm_msg"]["high_press_of_2_compressor_trigger"] = int(update("700425", 0))
    liquid_rep_json["alarm_msg"]["low_press_of_2_compressor_trigger"] = int(update("700426", 0))
    liquid_rep_json["alarm_msg"]["compressor_1_cocontactor_trigger"] = int(update("700427", 0))
    liquid_rep_json["alarm_msg"]["compressor_2_cocontactor_trigger"] = int(update("700428", 0))
    liquid_rep_json["alarm_msg"]["temp_of_water_outlet_is_low"] = int(update("700429", 0))
    liquid_rep_json["alarm_msg"]["exhaust_1_temp_high"] = int(update("700430", 0))
    liquid_rep_json["alarm_msg"]["exhaust_2_temp_high"] = int(update("700431", 0))
    liquid_rep_json["alarm_msg"]["high_press_senor_of_1compressor_fault"] = int(update("700432", 0))
    liquid_rep_json["alarm_msg"]["high_press_senor_of_2compressor_fault"] = int(update("700433", 0))
    liquid_rep_json["alarm_msg"]["low_press_senor_of_1compressor_fault"] = int(update("700434", 0))
    liquid_rep_json["alarm_msg"]["low_press_senor_of_2compressor_fault"] = int(update("700435", 0))
    liquid_rep_json["alarm_msg"]["temp_of_water_outlet_fault"] = int(update("700436", 0))
    liquid_rep_json["alarm_msg"]["temp_of_1_compressor_fault"] = int(update("700437", 0))
    liquid_rep_json["alarm_msg"]["temp_of_2_compressor_fault"] = int(update("700438", 0))
    liquid_rep_json["alarm_msg"]["maintenance_cycle_of_3_pump_reach"] = int(update("700439", 0))
    liquid_rep_json["alarm_msg"]["maintenance_cycle_of_1_pump_reach"] = int(update("700440", 0))
    liquid_rep_json["alarm_msg"]["maintenance_cycle_of_2_pump_reach"] = int(update("700441", 0))
    liquid_rep_json["alarm_msg"]["maintenance_cycle_of_1_compressor_reach"] = int(update("700442", 0))
    liquid_rep_json["alarm_msg"]["maintenance_cycle_of_1_fan_reach"] = int(update("700443", 0))
    liquid_rep_json["alarm_msg"]["maintenance_cycle_of_2_compressor_reach"] = int(update("700444", 0))
    liquid_rep_json["alarm_msg"]["maintenance_cycle_of_2_fan_reach"] = int(update("700445", 0))
    liquid_rep_json["alarm_msg"]["maintenance_cycle_of_heating_reach"] = int(update("700446", 0))
    liquid_rep_json["alarm_msg"]["frozen_start_3_pump"] = int(update("700447", 0))
    liquid_rep_json["alarm_msg"]["frozen_start_heating"] = int(update("700448", 0))
    liquid_rep_json["alarm_msg"]["temp_of_electric_cabinet_is_high"] = int(update("700449", 0))
    liquid_rep_json["alarm_msg"]["temp_of_electric_cabinet_fault"] = int(update("700450", 0))
    liquid_rep_json["alarm_msg"]["power_protection_trigger"] = int(update("700451", 0))
    liquid_rep_json["alarm_msg"]["compressor_1_overload"] = int(update("700452", 0))
    liquid_rep_json["alarm_msg"]["compressor_2_overload"] = int(update("700453", 0))
    liquid_rep_json["alarm_msg"]["converter_fault_of_1_pump"] = int(update("700454", 0))
    liquid_rep_json["alarm_msg"]["converter_fault_of_2_pump"] = int(update("700455", 0))
    liquid_rep_json["alarm_msg"]["converter_fault_of_3_pump"] = int(update("700456", 0))
    liquid_rep_json["alarm_msg"]["converter_fault_of_1_fan"] = int(update("700457", 0))
    liquid_rep_json["alarm_msg"]["converter_fault_of_2_fan"] = int(update("700458", 0))
    # liquid_rep_json["alarm_msg"]["Compressor_1_pk_protection"] = int(update("Compressor_1_pk_protection", 0))
    # 代码上没有这个，3.5号的接口文档未更新
    liquid_rep_json["alarm_msg"]["communication_lost"] = int(update("communication_lost", 0))
    # liquid_rep_json["alarm_msg"]["Compressor_2_pk_protection"] = int(update("Compressor_2_pk_protection", 0))
    # 代码上没有这个，3.5号的接口文档未更新
    # log.info(liquid_rep_json['alarm_msg'])
