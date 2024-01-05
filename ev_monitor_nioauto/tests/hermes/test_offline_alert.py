#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2021/05/31 14:40
@contact: hongzhen.bi@nio.com
@description: 车辆离线预警
"""
import time

import allure

from nio_messages.nextev_msg import gen_nextev_message


class TestOfflineAlert(object):
    """
    接受到车辆离线消息,redis缓存最近次离线时间
    ZRANGE hermes_test:oversee_monitor 0 10 withscores
    GET hermes_test:oversee_monitor_item_VehicleOnlineStateActor_{vid}
    告警记录相关log到over_see_event_cgw_offline

    配置项：存在hermes数据库的over_see_config表，rule_name='VehicleOnlineStateActor'，内容如下
        {
            "param_map":{
                "mail_enable":"false",      # 设置是否开启邮件告警
                "mail_to":"hongzhen.bi@nio.com,li.liu2@nio.com",
                "mail_detail":"[test]车辆10日未上线",     # 邮件告警内容
                "vehl_offline_warning_min":"1",     # 当车辆离线时间,超过该值后,发出车辆预警
                "vehl_offline_recheck_min":"1",     # 对应oversee的score每次命中检查后添加该时间（每隔该时间检查一次是否达到发车辆预警的时间）
                "sms_enable":"false",       # 设置是否开启短信告警
                "sms_to":"15011051120,13952120960",
                "sms_detail":"车辆10日未上线"
            }
        }
    """
    def test_offline_alert(self, cmdopt, vid, kafka, redis):
        ts = int(time.time() * 1000)
        msg = gen_nextev_message("", {"status": "OFFLINE"}, publish_ts=ts, msg_type=4, account_id=vid)
        kafka['cvs'].produce(kafka['topics']['cgw'], msg)
        time.sleep(10)
        assert len(redis['datacollection'].zset_zrange(f"hermes_{cmdopt}:oversee_monitor", start=0, end=10)) == 1
        assert redis['datacollection'].get(f"hermes_{cmdopt}:oversee_monitor_item_VehicleOnlineStateActor_{vid}") is not None

        with allure.step("发出离线报警后,删除最近次上报的离线的记录时间"):
            # 等待 vehl_offline_warning_min 时间
            time.sleep(60)
            assert redis['datacollection'].get(f"hermes_{cmdopt}:oversee_monitor_item_VehicleOnlineStateActor_{vid}") is None



