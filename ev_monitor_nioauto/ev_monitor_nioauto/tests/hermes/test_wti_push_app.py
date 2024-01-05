#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2021/05/26 20:04
@contact: hongzhen.bi@nio.com
@description: 车辆故障app提醒
"""
import copy
import random
import time
from datetime import datetime

import pytest

from nio_messages import wti


class TestWtiPushApp(object):
    """
    相关开关：
        推送功能配置开关，在configmap 中的 app.alarm.push.switch
        个人推送开关，存在vehicle_push_switch表中

    前置条件：车机版本大于BL230、不在维修中、不在升级中

    逻辑：如果const_wti表 app_push_enabled=1-->slytherin推送kafka(swc-cvs-tsp-{env}-80001-wti_alarm)--->hermes---调用接口---->APP Msg（api/1/in/app_msg/common）--->APP Message api(nofify)--->APP
        车辆故障上报后，tsp消费故障信息存入redis（hermes_test:app_wti_push:402355066:SQETEST0999647340-1622198547999-TPMS-10-WTI）
        后推送给app，其中该key对应的value会记录推送状态以及故障信息，key的ttl为72小时

    redis存储内容：
        {
            "vehicle_id":"9347f56bb63e4af190c1cfe744f8c45e",
            "request":{
                "wti_code":"WTI-TPMS-22",
                "description":"检测到爱车右前轮胎温度过高",
                "alarm_level":"2",
                "app_display":"右前轮胎温度过高",
                "alarm_id":"SQETEST0999647340-1622201483358-TPMS-22-WTI",
                "title":"车辆故障",
                "vehicle_id":"9347f56bb63e4af190c1cfe744f8c45e",
                "link_value":"nio://so/WTIMessage?clickType\u003dwti\u0026vinCode\u003dSQETEST0999647340\u0026vehicleId\u003d9347f56bb63e4af190c1cfe744f8c45e"
            },
            "response":{
                "request_id":"7zcqjXEcvB2aFeFSurG9eB",
                "result_code":"success",
                "message":"success",
                "server_time":1622201489
            }
        }
    """
    @pytest.fixture(autouse=False)
    def prepare(self, env, vin, cmdopt, vid, redis, publish_msg_by_kafka):
        # slytherin有缓存车机版本，先删掉
        redis['cluster'].delete(f"remote_vehicle_{cmdopt}:vehicle_status:{vid}:VersionModel")
        # 上报did使车机版本大于BL230
        did_data_list = [{"ecu": "CGW",
                          "dids": [{"id": "F140", "value": "V0001541 ZX", "sample_ts": int(time.time() * 1000)}]
                          }]
        publish_msg_by_kafka('did_update_event', vid=vid, vin=vin, did_data_list=did_data_list, sleep_time=2)

        # 上报一个能触发hermes更新vehicle_profile缓存的事件
        publish_msg_by_kafka('alarm_signal_update_event')

        account = env['vehicles']['normal']['account_id']
        pattern = f"hermes_{cmdopt}:app_wti_push:{account}:{vin}*"
        keys = redis['cluster'].keys(pattern)
        for key in keys:
            redis['cluster'].delete(key)

    def test_wti_push_app(self, prepare, env, cmdopt, vin, mysql, publish_msg_by_kafka, redis):

        sample_ts = round(time.time() * 1000)
        wti_temp = copy.deepcopy(wti.SIGNAL)

        # here we want to choose alarm which is wti_enabled
        for s in wti.SIGNAL:
            # 带note标记的都是比较特殊的wti，不选它
            if 'note' in s:
                wti_temp.remove(s)
                continue
            wti_const = mysql['rvs'].fetch('const_wti',
                                           where_model={"wti_code": s['wti_code']},
                                           fields=['wti_enabled', 'app_push_enabled'])[0]
            if wti_const['wti_enabled'] == 0 or wti_const['app_push_enabled'] == 0:
                wti_temp.remove(s)

        s = random.choice(wti_temp)
        s['sn'] = str(sample_ts)
        # 构造并上报消息
        nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                   alarm_signal={'signal_int': [s]},
                                                   sample_ts=sample_ts)
        time.sleep(30)
        sn = obj['alarm_signal']['signal_int'][0]['sn']
        alarm_id = '{}-{}-{}-WTI'.format(vin, sn, s['wti_code'][4:])
        account = env['vehicles']['normal']['account_id']
        key = f"hermes_{cmdopt}:app_wti_push:{account}:{alarm_id}"
        assert redis['cluster'].get(key) is not None

        # kibana log关键字：start push wti alarm, vehicleId:{vid}

    def test_3level_evm_wti_push_stuff(self, env, cmdopt, vin, vid, mysql, publish_msg_by_kafka, redis):
        """
        三级EVM WTI短信和飞书推送员工
        配置项:
            要通知的人员在VMS中事件预警->报警通知配置页面进行配置，
            Hermes在部署时或每小时调用VMS接口同步人员配置到redis中（redis key: hermes_test:evm_notify）

        推送后redis key:
            hermes_test:wti_sms:vid:wti_code:date
            ttl为3天
        """
        # 关掉所有WTI
        publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': []})

        sample_ts = round(time.time() * 1000)
        wti_temp = copy.deepcopy(wti.EVM_WTI_SIGNAL)

        # here we want to choose alarm which is wti_enabled
        for s in wti.EVM_WTI_SIGNAL:
            # 剔除级别不为3的WTI
            if s['evm_alarm_level'] != 3:
                wti_temp.remove(s)
                continue

        s = random.choice(wti_temp)
        s['sn'] = str(sample_ts)
        # 先删除redis
        date = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
        key = f"hermes_{cmdopt}:wti_sms:{vid}:{s['wti_code']}:{date}"
        redis['cluster'].delete(key)
        # 构造并上报消息
        publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': [s]}, sample_ts=sample_ts)
        time.sleep(3)

        assert redis['cluster'].get(key) is not None
        # 验证飞书和短信。kibana log关键字：push wti notify, wti:
