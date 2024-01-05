#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: wenlong.jin
@File: script.py
@Project: ps30
@Time: 2023/7/3 10:50
"""

import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))

import time
from paho.mqtt import client as mqtt_client
from PUS_ctrl_message_pb2 import *
from SCT_pb2 import *


class IccMqtt:

    def __init__(self, queue, icc):
        """

        :param queue:
        :param icc:

        """
        self.queue = queue
        self.icc = icc + 1
        self.connect_status = 0
        self.client = mqtt_client.Client(f'ICC_{self.icc}', clean_session=False)
        self.client.username_pw_set('pp', 'N7102io')
        self.client.on_connect = self.on_connect
        self.client.connect('192.168.1.10', 8200, keepalive=5)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connect_status = 1
            print(f"<ICC>:icc{self.icc} Connected to MQTT Broker!")
        else:
            print(f"<ICC>:icc{self.icc} Failed to connect mcs broker, return code {rc}")

    def on_subscribe(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        print(f"<ICC>:icc{self.icc} subscribe success")

    def subscribe(self):
        """

        :return:
        """
        self.client.on_message = self.on_message
        self.client.subscribe(f"ctrl/icc/{self.icc}")
        self.client.subscribe(f"ctrl/icc/{self.icc}")

    def on_message(self, client, userdata, msg):
        """
        解析响应的消息
        :param client:
        :param userdata:
        :param msg:
        :return:
        """
        if msg.topic == f"ctrl/icc/{self.icc}":
            self.icc_unpack_ctrl_msg(msg)

    def icc_unpack_ctrl_msg(self, msg):
        """
        解析发送给ICC的控制消息，控制响应消息:f"ctrl/icc/{self.icc}"
        :param msg:
        :return:
        """
        _func = sys._getframe().f_code.co_name
        ctrl_msg = CTRL_MESSAGE()
        try:
            ctrl_msg.ParseFromString(msg.payload)
        except Exception as e:
            print(f"<ICC>:func {_func} parse ctrl message happen error: {e}, payload:{msg.payload}")
        else:
            print(
                f"<ICC>:{time.asctime()} func {_func},device>>{ctrl_msg.device}, id>>{ctrl_msg.id}, cmd_id>>{ctrl_msg.cmd_id},rep_args>>{ctrl_msg.req_args}")
            # if msg.topic == f"ctrl/icc/{self.icc}":
            #     data = self.icc_pack_mcs_ctrl_reply_msg(ctrl_msg)
            #     result = self.client.publish(f"ctrl/mcs/", data)
            #     if result[0] != 0:  # result: [0, 1]
            #         print(f"<ICC>:icc failed to send mcs ctrl reply msg")

    def icc_pack_mcs_ctrl_reply_msg(self, ctrl_msg):
        """
        ICC 发送给MCS的控制响应消息
        :return:
        """
        mcs_ctrl_rep = CTRL_MESSAGE()
        mcs_ctrl_rep.device = 7
        mcs_ctrl_rep.id = self.icc  # 1-4
        mcs_ctrl_rep.timestamp = 0
        mcs_ctrl_rep.ctrl_type = CTRL_TYPE.REP  # req 0, rep 1
        mcs_ctrl_rep.cmd_id = ctrl_msg.cmd_id
        for arg in ctrl_msg.req_args:
            mcs_ctrl_rep.rep_args.append(arg)
        data = mcs_ctrl_rep.SerializeToString()
        return data

    def publish(self):
        """

        :return:
        """
        data = {}
        while True:
            try:
                if not self.queue.empty():
                    data.update(self.queue.get())
                time.sleep(1)
            except Exception as e:
                _, exc_value, _ = sys.exc_info()
                print(f"<ICC>:icc back process update script data happen error:{exc_value}")
                time.sleep(1)


def start_icc_mqtt_process(queue, icc):
    """

    :param queue:
    :param icc:
    :return:
    """
    print(f"<ICC>:begin to create icc{icc} mqtt sub process")
    icc_mqtt = IccMqtt(queue, icc)
    time.sleep(5)
    print(f"connect_status:{str(icc_mqtt.connect_status)}")
    icc_mqtt.subscribe()
    icc_mqtt.client.loop_start()
    icc_mqtt.publish()
