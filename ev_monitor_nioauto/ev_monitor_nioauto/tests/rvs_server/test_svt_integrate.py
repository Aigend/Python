#!/usr/bin/env python
# coding=utf-8

"""
Description: ecall事件和车机端联调
前置条件：车辆处于正常车辆状态，即同时满足{VehState}== Parked vehicle ，并且{ComfEna} == Comfort not enabled，并且Repair Modeis off，并且No tester is connected
Case:
        验证通过API配置ecall setting能正常下发到车机端
        验证hard_trigger事件能触发，上报及呼叫所配置的手机
        验证soft_trigger事件能触发，上报及呼叫所配置的手机
        验证airbag_pump_tigger事件能触发，上报及呼叫所配置的手机
        验证nio_call_trigger事件能触发，上报及呼叫所配置的手机
        验证通过API关闭ecall后，ecall事件可以被触发落库，但是不呼叫手机

"""
import pytest


@pytest.mark.skip
class TestEcallCrossDebug(object):
    """
    前置条件：车辆处于正常车辆状态，即同时满足{VehState}== Parked vehicle ，并且{ComfEna} == Comfort not enabled，并且Repair Modeis off，并且No tester is connected

    """

    def test_ecall_default_setting(self):
        """
        验证初始默认配置， SVT 的触发都为disable，此时不能触发svt事件

        1.	断开天线，校验SVT不被触发

        2.	断开LV电源，校验SVT不被触发

        3.	触发车辆报警，校验SVT不被触发

        4.	车辆非法移动超过100m，校验SVT不被触发

        """

    def test_lv_bat_remove_and_svt_off(self):
        """
        验证通过API配置了lv_bat_remove=enable时，LV电源的断开与恢复会触发svt事件

        1.	通过API 配置lv_bat_remove 为enable，并且超过5秒触发
            API:http://showdoc.nevint.com/index.php?s=/11&page_id=901
            Type='svt_setting', Values示例如下：
            {
            "trigger": {
                "lv_bat_remove":{"timeout": 5,"enable": true},
                "gnss_ant_fault": {"enable": false},
                "unauth_mv_alarm": {"dist": 100,"enable": false},
                "anti_theft_alarm": {"enable": false}
            },
            "svt_mode":"off",
            "debug": false,
            "ver": 1,
            "ts": 1490166348
            }

        2.	断开LV电源，验证svt触发并落库，reason_code=lv_bat_removal_on

        3.	恢复LV电源连接，验证svt触发并落库，其中reason_code=lv_bat_removal_off


        """

    def test_lv_bat_remove_and_svt_on(self):
        """
        验证通过API配置了lv_bat_remove=enable时，LV电源的断开与恢复会触发svt事件，当配置svt_mode = on后，每隔30秒亦会有svt事件上报

        1.	通过API 配置lv_bat_remove 为enable，并且超过5秒触发
            API:http://showdoc.nevint.com/index.php?s=/11&page_id=901
            Type='svt_setting', Values示例如下：
            {
            "trigger": {
                "lv_bat_remove":{"timeout": 5,"enable": true},
                "gnss_ant_fault": {"enable": false},
                "unauth_mv_alarm": {"dist": 100,"enable": false},
                "anti_theft_alarm": {"enable": false}
            },
            "svt_mode":"off",
            "debug": false,
            "ver": 1,
            "ts": 1490166348
            }

        2.	断开LV电源，验证svt触发并落库，reason_code=lv_bat_removal_on

        3.  通过API配置svt_mode = on, 验证每隔30秒，会有reason_code=data_report的svt事件上报，该svt事件会存储到mysql数据库中

        4.  通过API配置svt_mode = off, 验证不再有上一步reason_code=data_report的svt事件上报

        5.	恢复LV电源连接，验证svt触发并落库，其中reason_code=lv_bat_removal_off

        """

    def test_anti_theft_alarm_and_svt_on(self):
        """
        验证通过API配置了anti_theft_alarm=enable时，alarm信号的开关会触发svt事件，当配置svt_mode = on后，每隔30秒亦会有svt事件上报

        1.	通过API 配置lv_bat_remove 为enable，并且超过5秒触发
            API:http://showdoc.nevint.com/index.php?s=/11&page_id=901
            Type='svt_setting', Values示例如下：
            {
            "trigger": {
                "lv_bat_remove":{"timeout": 5,"enable": false},
                "gnss_ant_fault": {"enable": false},
                "unauth_mv_alarm": {"dist": 100,"enable": false},
                "anti_theft_alarm": {"enable": true}
            },
            "svt_mode":"off",
            "debug": false,
            "ver": 1,
            "ts": 1490166348
            }

        2.	触发theft alarm信号，验证svt触发并落库，reason_code=anti_theft_alarm_on

        3.  通过API配置svt_mode = on, 验证每隔30秒，会有reason_code=data_report的svt事件上报，该svt事件会存储到mysql数据库中

        4.  通过API配置svt_mode = off, 验证不再有上一步reason_code=data_report的svt事件上报

        5.	取消触发theft alarm，验证svt触发并落库，reason_code=anti_theft_alarm_off

        """

    def test_unauth_mv_alarm_and_svt_on(self):
        """
        验证通过API配置了unauth_mv_alarm=enable时，非法移动会触发svt事件，当配置svt_mode =on后，每隔30秒亦会有svt事件上报

        1.	通过API 配置lv_bat_remove 为enable，并且超过5秒触发
            API:http://showdoc.nevint.com/index.php?s=/11&page_id=901
            Type='svt_setting', Values示例如下：
            {
            "trigger": {
                "lv_bat_remove":{"timeout": 5,"enable": false},
                "gnss_ant_fault": {"enable": false},
                "unauth_mv_alarm": {"dist": 100,"enable": true},
                "anti_theft_alarm": {"enable": false}
            },
            "svt_mode":"off",
            "debug": false,
            "ver": 1,
            "ts": 1490166348
            }

        2.	非法移动车辆超过100米，验证svt触发并落库，reason_code=unauth_movement_on

        3.  通过API配置svt_mode = on, 验证每隔30秒，会有reason_code=data_report的svt事件上报，该svt事件会存储到mysql数据库中

        4.  通过API配置svt_mode = off, 验证不再有上一步reason_code=data_report的svt事件上报

        """

    def test_gnss_ant_fault_and_svt_on(self):
        """
        验证通过API配置了gnss_ant_fault=enable时，天线的断开与恢复会触发svt事件，当配置svt_mode =on后，每隔30秒亦会有svt事件上报

        1.	通过API 配置lv_bat_remove 为enable，并且超过5秒触发
            API:http://showdoc.nevint.com/index.php?s=/11&page_id=901
            Type='svt_setting', Values示例如下：
            {
            "trigger": {
                "lv_bat_remove":{"timeout": 5,"enable": false},
                "gnss_ant_fault": {"enable": true},
                "unauth_mv_alarm": {"dist": 100,"enable": false},
                "anti_theft_alarm": {"enable": false}
            },
            "svt_mode":"off",
            "debug": false,
            "ver": 1,
            "ts": 1490166348
            }

        2.	断开天线，验证svt触发并落库，reason_code=gnss_ant_fault_on

        3.  通过API配置svt_mode = on, 验证每隔30秒，会有reason_code=data_report的svt事件上报，该svt事件会存储到mysql数据库中

        4.  通过API配置svt_mode = off, 验证不再有上一步reason_code=data_report的svt事件上报

        5.	重现连接天线,，验证svt触发并落库，reason_code=gnss_ant_fault_off

        """

    def test_no_svt_on_repair_mode(self):
        """
        验证通过API配置车辆为Repair mode下，不能触发svt事件

        1.	通过API 配置车辆处于Repair mode
            http://showdoc.nevint.com/index.php?s=/11&page_id=901
            type=repair_mode, values={ "repair_mode": "ON", "publish_ts":1523522508 }

        2.	断开天线，校验SVT不被触发

        3.	断开LV电源，校验SVT不被触发

        4.	触发车辆报警，校验SVT不被触发

        5.	车辆非法移动超过100m，校验SVT不被触发

        6. 调用API恢复车辆使之处于正常状态
            type=repair_mode, values={ "repair_mode": "OFF", "publish_ts":1523522508 }

        """
