# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2022/11/8 18:29
# @File: liquid_mqtt.py
import json
import sys
import time

from paho.mqtt import client as mqtt_client

from utils.log import log


class LiquidMqtt:
    
    def __init__(self, queue):
        """

        :param queue:
        """
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self.connect_status = 1
                log.info("<Liquid>:Connected to MQTT Broker!")
            else:
                log.error(f"<Liquid>: Failed to connect, return code {rc}")
        self.queue = queue
        self.connect_status = 0
        self.client = mqtt_client.Client('python-mqtt-liquid', clean_session=False)
        self.client.username_pw_set('pp', 'N7102io')
        self.client.on_connect = on_connect
        self.client.connect('192.168.1.10', 8200, keepalive=5)

    def subscribe(self):
        """

        :return:
        """
        # def on_subscribe(self.client, userdata, mid, granted_qos):
        #     log.info(mid)
        #     log.info(granted_qos)
        def on_message(client, userdata, msg):
            log.info(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        # self.client.on_subscribe = on_subscribe
        self.client.on_message = on_message
        self.client.subscribe("ctrl/raw/lc/1")

    def publish(self):
        """

        :return:
        """
        real_msg = ""
        alarm_msg = ""
        while True:
            if not self.connect_status:
                continue
            try:
                if not self.queue.empty():
                    data = self.queue.get()
                    if data.get("real_msg"):
                        real_msg = data.get("real_msg")
                    if data.get("alarm_msg"):
                        alarm_msg = data.get("alarm_msg")
                        # log.info(alarm_msg)
                    # log.info("<Liquid>:data update success"),

                time.sleep(0.1)
                if real_msg:
                    result = self.client.publish("data/raw/lc/1", json.dumps(real_msg))
                    if result[0] != 0:  # result: [0, 1]
                        log.error(f"<Liquid>:Failed to send real time data message to topic")
                    # else:
                    #     print("<Liquid> real time data ")
                time.sleep(0.9)
                if alarm_msg:
                    result = self.client.publish("alarm/raw/lc/1", json.dumps(alarm_msg))
                    if result[0] != 0:  # result: [0, 1]
                        log.error(f"<Liquid>:Failed to send alarm data message to topic")
                    # else:
                    #     print("<Liquid>: alarm data")
            except Exception as e:
                _, exc_value, _ = sys.exc_info()
                log.error(f"<Liquid>:liquid back mqtt process happen error:{exc_value}")
                time.sleep(1)


def start_can_send_process(queue):
    """

    :param queue:
    :return:
    """
    liquid_mqtt = LiquidMqtt(queue)
    liquid_mqtt.subscribe()
    liquid_mqtt.client.loop_start()  # 是启用一个进程保持loop()的重复调用，就不需要定期心跳了，对应的有loop_stop()
    liquid_mqtt.publish()


if __name__ == '__main__':
    import multiprocessing
    from multiprocessing import Queue
    q = Queue()
    proc = multiprocessing.Process(target=start_can_send_process, args=(q, ))
    proc.daemon = True
    proc.start()
    while True:
        time.sleep(5)
