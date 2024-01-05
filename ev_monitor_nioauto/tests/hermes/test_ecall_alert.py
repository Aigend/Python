#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2021/05/31 16:33
@contact: hongzhen.bi@nio.com
@description: 推送<邮件>和<短信>ecall告警
"""

import time


class TestEcallAlert(object):
    """
    配置项:
        1、存在hermes数据库的over_see_config表，rule_name='ECallActor'，内容如下
            {
                "param_map":{
                    "mail_enable":"false",
                    "mail_detail":"车辆E-Call事件发生",
                    "sms_enable":"false",
                    "sms_detail":"车辆E-Call事件发生"
                }
            }
        2、要通知的人员在VMS中事件预警->报警通知配置页面进行配置，
        Hermes在部署时或每小时调用VMS接口同步人员配置到redis中（redis key: hermes_test:ecall_notify）

    推送邮件或短信告警后存在1小时的冷却时间，ttl hermes_{env}:ECallActor_cooling_key::{vid}:{reason} 为1小时

    记录e_call的相关log到remote_vehicle_test.over_see_event_ecall

    注意：
        1、hard_trigger的ecall不会触发本告警推送
        2、若 vehicle_profile_info_extend.vehicle_identity = 0 (内部车)，
          推送信息中增加一行 "车辆用途：{车辆用途}"，车辆用途来自于 数据统计的数据库中 vehicle_tag.vam_vehicle_purpose
    """

    def test_ecall_alert(self, cmdopt, vid, mysql, publish_msg_by_kafka, redis):
        # 避免1分钟内重复报ecall事件，否则服务端不处理
        time.sleep(62)
        # 上报
        ts = int(time.time() * 1000)
        nextev_message, obj = publish_msg_by_kafka('ecall_event', sample_ts=ts, sleep_time=4)
        log_mysql = mysql['rvs'].fetch('over_see_event_ecall', {"vehicle_id": vid, "sample_time": ts // 1000})
        assert len(log_mysql)
        cooling_key = redis['datacollection'].get(f"hermes_{cmdopt}:ECallActor_cooling_key::{vid}:{obj['reason_code']}")
        assert cooling_key
