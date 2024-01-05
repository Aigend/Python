#!/usr/bin/env python
# coding=utf-8
import time

import pytest


class TestDelayAlerm(object):
    @pytest.mark.skip('manual')
    def test_delay_alert(self, env, mysql, publish_msg, publish_msg_by_kafka):
        """
        消息延迟告警，一辆车30分钟内出现300条以上的延迟500s的消息，会发送邮件报警。

        publish_ts是车机端监测到网络在线时，往待发送队列push数据时打的timestamp。如果publish_ts和云端当前时间差距很大，说明网络延时。

        Redis：
            alias conn_redis='redis-cli -h swc-cache-master-evmonitor-test.nioint.com -p 6380'

            zrange hermes_test:oversee_temp_monitor_item_MessageDelayMonitor_{vid} {start_time_unit_s} {end_time_unit_s}
                1）example: zrange hermes_test:oversee_temp_monitor_item_MessageDelayMonitor_4e18c0f0ab734805a802b845a02ad824 0 10000000000000
                    里面的value是云端接收到延迟500秒数据的当前时间。每一个value表示一条延迟消息
                2）往redis里插入前服务会把30分钟以前的数据清空


        step:
            1. 运行如下脚本构造300条延迟数据
            2. 检查邮件有无收到（在hermes_test.over_see_config配置邮件通知人 rule_name=MessageDelayActor）
            3. 校验redis满了300条不再记录
            4. 校验一小时内不会报两次

        """



        # 构造并上报消息

        # 延迟500s
        publish_ts = int(round(time.time() * 1000)) - 1000 * 600

        sample_ts = publish_ts
        print(f'publish_ts {publish_ts}')

        for i in range(300):
            # 注意时间要每隔1秒报一个，服务器处理没那么精确。
            nextev_message, light_change_obj = publish_msg_by_kafka('light_change_event',  publish_ts=publish_ts, sample_ts=sample_ts, sleep_time=1)
