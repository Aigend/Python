#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2021/05/31 18:42
@contact: hongzhen.bi@nio.com
@description: 车辆维修订单提醒
"""
import json
import time

import allure


class TestRepairOrder(object):
    """
    配置项: 存在hermes数据库的over_see_config表，rule_name='RepairModeActor'，内容如下
        {
            "param_map":{
                "repair_mode_recheck_min":"1",
                "repair_mode_warning_min":"1",
                "mail_enable":"false",
                "mail_to":"hongzhen.bi@nio.com,li.liu2@nio.com",
                "mail_detail":"[test]维修模式%s 订单号:%s",
                "sms_enable":"false",
                "sms_to":"15011051120,13952120960",
                "sms_detail":"维修模式%s 订单号：%s",
                "repair_mode_delay_mail_enable":"false",
                "repair_mode_delay_mail_to":"hongzhen.bi@nio.com,li.liu2@nio.com",
                "repair_mode_delay_mail_detail":"[test]repair mode delay mail booking order number:%s",
                "repair_mode_delay_sms_enable":"false",
                "repair_mode_delay_sms_to":"15011051120,13952120960",
                "repair_mode_delay_sms_detail":"[test]repair mode delay sms booking order number:%s"
            }
        }

    """

    def test_repair_order(self, env, cmdopt, vid, kafka, redis):
        ts = int(time.time())
        vid = env['vehicles']['vehicle_for_repair']['vehicle_id']
        with allure.step("验证车辆产生维修开始订单,hermes可以根据配置给相关人员发送邮件或短信告警"):
            vehicle_repair_order = json.dumps({
                "owner_phone": "13761473462", "order_status_name": "维修开始", "som_order_no": "BSHHB00020180720001113",
                "account_id": "1112538414", "receipt_type": "", "booking_order_no": "BSHHB00020180720001113",
                "order_status_code": '5', "update_at": ts, "ro_no": "BSHHB00020180720001113", "update_by": "用户代表",
                "vehicle_id": vid,
                "order_type": "101210034", "timestamp": ts, "status": 5,
                "repair_order_no": "BSHHB00020180720001113"
            })

            kafka['do'].produce(kafka['topics']['repair'], vehicle_repair_order)

        with allure.step("验证车辆的维修单超过repair_mode_warning_min配置的时间后仍然没有结束,期望hemres可以根据配置给相关人员发送短信或者邮件告警"):
            time.sleep(70)
            # pass

        with allure.step("验证车辆产生维结束修订单,hermes可以根据配置给相关人员发送邮件或短信告警"):
            vehicle_repair_order = json.dumps({
                "owner_phone": "13761473462", "order_status_name": "维修结束", "som_order_no": "BSHHB00020180720001113",
                "account_id": "1112538414", "receipt_type": "", "booking_order_no": "BSHHB00020180720001113",
                "order_status_code": '10', "update_at": ts, "ro_no": "BSHHB00020180720001113", "update_by": "用户代表",
                "vehicle_id": vid,
                "order_type": "101210034", "timestamp": ts, "status": 10,
                "repair_order_no": "BSHHB00020180720001113"
            })

            kafka['do'].produce(kafka['topics']['repair'], vehicle_repair_order)
