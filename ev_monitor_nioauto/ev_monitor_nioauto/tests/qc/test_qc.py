#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/09/30 13:38
@contact: li.liu2@nio.com
@description:

    灾备环境联调测试
    在联调前，需要确认如下信息：
        1. 版本信息

        2. 域名与ip
            host-record=app.nio.com,129.211.153.187,60
            host-record=tsp.nio.com,118.89.97.228,60
            host-record=v.nioint.com,10.132.200.4,60
            host-record=tsp-nmp.nioint.com,10.132.140.17,60

        3. 正式灾备前的准备： https://confluence.nioint.com/pages/viewpage.action?pageId=312319971

"""


class TestQC(object):
    def test_qc(self, env, publish_msg, vid, vin):
        """
        校验qc 消息平台能收到数据


        LJ1EEAUU7J7700497
        ce86a87d33414d38b0820d4fe09358de
        ChDZ0IcO3ShwIz_Mi-3wcjUiEAEYdSCVTigC


        TODO
        0. 确认config/prod/prod_config.yaml配置正常
        1. 通知孙立雪mysql 断开同步
        2. 打开qc kafka 监控 swc-tsp-data_collection-prod-vehicle_data
            python utils/kafka_client.py
        3. 先取一下mysql里的值。保持上报的值和线上的一样
            select * from status_light where  id='ce86a87d33414d38b0820d4fe09358de';
        4.上报数据保持原值
            publish_msg('light_change_event', light_status={'hi_beam_on': 0, 'lo_beam_on':0, 'head_light_on':0})
        5. 校验kafka有数据
        6. 校验qc数据库的数据更新了（qc数据库 http://10.128.231.2/  DB:tsp_ro）

        """

        print(f'qc env: {env} vid:{vid} vin: {vin}')

        nextev_message, light_change_obj = publish_msg('light_change_event', light_status={'hi_beam_on': 0, 'lo_beam_on': 0, 'head_light_on': 0})

    def test_downstream_stoner_and_metis(self, publish_msg,vid,vin):
        """
        LJ1EEAUU7J7700497
        ce86a87d33414d38b0820d4fe09358de
        ChDZ0IcO3ShwIz_Mi-3wcjUiEAEYdSCVTigC

        TODO

        1. 通知孙立雪mysql 断开同步
        2. 通知下游做监控 Metis 是shanchuan Stoner是yan.xie
        3. 查询车的status_wti获得wti情况
        4. 打开监听 swc-cvs-tsp-prod-80001-wti_can_signal
        5. 上报数据
        6. 查看kafka有无数据推送
        7. 查看数据库里是否有新增的wti
        8. 手机DNS改为灾备DNS（外网10.128.224.32，52.80.245.88），查看车辆数据为刚上报的数据
        """

        data = {
            # "around_alarm": 1,
            "icc_id": "898602F9091830045817",
            "reissue": False,
            # "journey_id": "2019031100001",
            "sample_points": [
                {
                    # "sample_ts": 1596875977655,

                    "alarm_signal": {"signal_int": [
                        # {"name": "VCUImdStopDriving", "sn": "1552283654775", "value": 1}
                        {'name': 'TpmsFrntLeWhlPressSts', 'value': 2, 'alarm_level': 2, 'wti_code': 'WTI-TPMS-17', 'description': '左前轮胎压力低'},

                    ]},
                    "bms_status": {"avg_cell_volt": 1.88100004196167, "avg_temp": 36, "chrg_pwr_lmt": 155.5, "dischrg_pwr_lmt": 259.1000061035156, "health_status": 33.400001525878906,
                                   "in_coolant_temp": 3.375, "isolation_level": 1, "out_coolant_temp": 4.625}, "can_msg": {"can_data": [{"msg_id": 628, "value": "0000000000000000"}]},
                    "driving_data": {"aclrtn_pedal_posn": 51.74399948120117, "average_speed": 217.2375030517578, "brk_pedal_sts": {"state": 0, "valid": 1}, "max_speed": 229.0500030517578,
                                     "min_speed": 272.92498779296875, "steer_whl_rotn_ag": 501.5, "steer_whl_rotn_spd": 855, "vcu_drvg_mod": 2}, "driving_motor": {"pwr_sys_rdy": True, "motor_list": [
                    {"drvmotr_cntrl_temp": 46, "drvmotr_contl_dc_bus_curnt": 1460.300048828125, "drvmotr_contl_involt": 146.5, "drvmotr_rotn_spd": 11647, "drvmotr_rotn_torq": -209.75,
                     "drvmotr_sn": 1,
                     "drvmotr_sts": 3, "drvmotr_temp": 165, "max_neg_torq_st": 2011.0, "max_pos_torq_st": -1258.25, "torq_command": 1899.125},
                    {"drvmotr_cntrl_temp": -35, "drvmotr_contl_dc_bus_curnt": 1748.4000244140625, "drvmotr_contl_involt": 700.5, "drvmotr_rotn_spd": -23102, "drvmotr_rotn_torq": 288.5,
                     "drvmotr_sn": 2,
                     "drvmotr_sts": 4, "drvmotr_temp": 54, "max_neg_torq_st": 761.375, "max_pos_torq_st": 1334.375, "torq_command": 1705.75}]}, "evm_flag": True,
                    "extremum_data": {"highest_temp": 78, "hist_temp_btry_sbsys_sn": 243, "hist_temp_prb_sn": 52, "hist_volt_btry_sbsys_sn": 208, "hist_volt_singl_btry_sn": 146, "lowest_temp": -29,
                                      "lwst_temp_btry_sbsys_sn": 136, "lwst_temp_prb_sn": 48, "lwst_volt_btry_sbsys_sn": 52, "lwst_volt_singl_btry_sn": 181, "sin_btry_hist_volt": 2.6670000553131104,
                                      "sin_btry_lwst_volt": 0.26100000739097595},
                    "hvac_status": {"air_con_on": True, "amb_temp_c": -1.5, "cbn_pre_sts": 0, "ccu_cbn_pre_ac_ena_sts": 1, "ccu_cbn_pre_aqs_ena_sts": 0, "outside_temp_c": -33, "pm_2p5_cabin": 881,
                                    "pm_2p5_filter_active": False}, "occupant_status": {"fr_le_seat_occupant_status": 2, "fr_ri_seat_occupant_status": 0},
                    "position_status": {"altitude": -64.6, "altitude_uncertainty": 2197.4,
                                        "attitude": {"acc_len": 2836677.7, "acc_x": 2.033031726E7, "acc_x_calib_sts": 2, "acc_y": 3.196797993E7, "acc_y_calib_sts": 3, "acc_z": 2.847818824E7,
                                                     "acc_z_calib_sts": 3, "depth": -22.17, "dip": 60.41, "gyro_x": 2.561101066E7, "gyro_x_calib_sts": 1, "gyro_y": 4.16873312E7,
                                                     "gyro_y_calib_sts": 2,
                                                     "gyro_z": 4.442714075E7, "gyro_z_calib_sts": 1, "heading": 18.53, "imu_status": 4, "mag_len": 10629.11, "mag_x": 49310.44, "mag_y": 44430.97,
                                                     "mag_z": 42073.26, "pitch": 1.58, "roll": -2.04, "single_tick_calib_sts": 0, "temp": 221.28, "x_accel": 433, "x_accel_valid": False,
                                                     "x_ang_rate": 342,
                                                     "x_ang_rate_valid": False, "y_accel": 83, "y_accel_valid": False, "y_ang_rate": 387, "y_ang_rate_valid": True, "yaw": 193.19, "z_accel": 395,
                                                     "z_accel_valid": True, "z_ang_rate": 367, "z_ang_rate_valid": True, "sensors": [
                                                {"cal_status": 0, "fault_bad_meas": True, "fault_bad_ttag": True, "fault_missing_meas": False, "fault_noisy_meas": True, "is_ready": False,
                                                 "is_used": False,
                                                 "obs_freq": 18, "time_status": 1, "type": 5}]}, "climb": 435.959, "climb_uncertainty": -618.218, "fusion_mode": 4, "gps_speed": 113,
                                        "gps_speed_uncertainty": 303, "gps_ts": 1551774732868, "heading": 95, "latitude": 31.739919, "latitude_uncertainty": 149.193, "longitude": 105.328681,
                                        "longitude_uncertainty": -72.16, "mode": 5, "posng_valid_type": 1,
                                        "satellite": {"quantity": 1007, "skyview": [{"azimuth": 187, "elevation": 169, "prn_id": 176, "snr": 52.195154, "used": True}],
                                                      "snr": [64.716563, 20.642889]}},

                    "soc_status": {"btry_cap": 354.8999938964844, "btry_qual_actvtn": False, "chrg_final_soc": 28, "chrg_state": 1, "dump_enrgy": 49.79999923706055, "hivolt_btry_curnt": -325.5,
                                   "realtime_power_consumption": 117, "remaining_range": 346, "sin_btry_hist_temp": 76, "sin_btry_lwst_temp": 2, "soc": 23, "btry_paks": [
                            {"btry_pak_curnt": -1189.800048828125, "btry_pak_hist_temp": 21.5, "btry_pak_lwst_temp": -29.5, "btry_pak_sn": 1, "btry_pak_voltage": 277.1000061035156,
                             "frm_start_btry_sn": 1,
                             "sin_btry_qunty_of_frm": 3, "sin_btry_qunty_of_pak": 3, "temp_prb_qunty": 3, "prb_temp_lst": [10, 20, 30], "prb_temp_lst_inv": [], "sin_btry_voltage": [10, 20, 30],
                             "sin_btry_voltage_inv": []}]},
                    "tyre_status": {"frnt_le_whl_press": 317.1629943847656, "frnt_le_whl_temp": -44, "frnt_ri_whl_press": 83.75299835205078, "frnt_ri_whl_temp": 116,
                                    "re_le_whl_press": 328.1470031738281,
                                    "re_le_whl_temp": 186, "re_ri_whl_press": 155.1490020751953, "re_ri_whl_temp": -3},
                    "vehicle_status": {"chrg_state": 3, "comf_ena": 0, "dc_dc_sts": 2, "gear": 0, "insulatn_resis": 38604, "mileage": 11014458, "oprtn_mode": 3, "soc": 88, "speed": 182.6437530517578,
                                       "urgt_prw_shtdwn": True, "vehl_state": 3, "vehl_totl_curnt": 1991.5, "vehl_totl_volt": 469.1000061035156}}]}

        nextev_message, journey_update_obj = publish_msg('periodical_journey_update',
                                                         icc_id='898602F9091830045817',
                                                         reissue=False,
                                                         around_alarm=1,
                                                         sample_points=
                                                         [{
                                                             "alarm_signal": {"signal_int": [
                                                                 # {'name': 'BMSPackOverTemp', 'value': 1, 'alarm_level': 1, 'evm_alarm_level': 3, 'alarm_code': 1, 'wti_code': 'WTI-BMS-8'}
                                                                 {'name': 'BMSPackThermOutOfCtrlAlrm', 'value': 2, 'alarm_level': 1, 'wti_code': 'WTI-BMS-9'}
                                                             ]},
                                                             "vehicle_status":{
                                                                 "ntester":False
                                                             }
                                                         }]
                                                         )

    def test_ecall(self,publish_msg,vid,vin):
        """
        TODO

        1. 通知孙立雪mysql 断开同步
        2. 通知下游做监控 Metis 是shanchuan
        3. 查询车的ecall_event获得ecall情况
        4. 打开监听 swc-cvs-tsp-prod-80001-ecall
        5. 上报数据
        6. 查看kafka有无数据推送
        7. 查看数据库里是否有新增的ecall

        """

        nextev_message, obj = publish_msg('ecall_event', sleep_time=4)
