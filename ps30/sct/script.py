#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/28 13:43
# @Author  : wenlong.jin@nio.com
# @File    : script.py
# @Software: ps20
"""
用于在实际开发板环境下查看主控和SCT之间的日志信息，观察topic信息
 只订阅topic数据，不进行发送
"""
import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))
import time

from enum import Enum, unique

from paho.mqtt import client as mqtt_client
from PUS_ctrl_message_pb2 import *
from PCU_pb2 import *
from SCT_pb2 import *


@unique
class SCT_CTRL_PCU_ENUM(Enum):
    SCT_CTRL_PCU_READY = 0x00,
    SCT_CTRL_PCU_START_ISD = 0x10,  # 启动绝缘检测
    SCT_CTRL_PCU_STOP_ISD = 0x11,  # 停止绝缘检测
    SCT_CTRL_PCU_START_CHARGE = 0x12,  # 启动充电
    SCT_CTRL_PCU_STOP_CHARGE = 0x13,  # 停止充电
    SCT_CTRL_PCU_ADJUST_POWER = 0x14,  # 功率调节
    SCT_HEARTBEAT = 0x20,


class SctMqtt:

    def __init__(self):
        """

        :param queue:
        :param sct:

        """
        self.connect_status = 0
        self.client = mqtt_client.Client(f'script', clean_session=False)
        self.client.username_pw_set('pp', 'N7102io')
        self.client.on_connect = self.on_connect
        self.client.connect('192.168.1.10', 8200, keepalive=5)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connect_status = 1
            print(f"<SCT>:script Connected to MQTT Broker!")
        else:
            print(f"<SCT>:script Failed to connect mcs broker, return code {rc}")

    def on_subscribe(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        print(f"<SCT>:script subscribe success")

    def subscribe(self):
        """

        :return:
        """

        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message

        # self.client.subscribe(f"data/all/mcs/")  # // mcs-sct
        self.client.subscribe(f"ctrl/sct/4")  # pcu-sct mcs-sct
        # self.client.subscribe(f"recvTopic")  #
        # self.client.subscribe(f"ota/sct/{self.sct}")  # mcs-sct result
        # self.client.subscribe(f"debug/sct/{self.sct}")  # mcs-sct r
        # self.client.subscribe(f"ota/client/sct/{self.sct}")  # mcs-sct
        self.client.subscribe(f"data/rt/pcu/1")  # pcu-sct
        # self.client.subscribe(f"data/set/mcs/{self.sct}")  # mcs-sct
        # self.client.subscribe(f"txt/mcs/{self.sct}")  # mcs-sct

        self.client.subscribe(f"data/all/sct/4")  # // sct-mcs
        self.client.subscribe(f"data/rt/sct/4")
        # self.client.subscribe(f"data/#")

        self.client.subscribe("ctrl/pcu/1")
        self.client.subscribe(f"data/status/sct/4")
        self.client.subscribe("ctrl/mcs/")

    def on_message(self, client, userdata, msg):
        """
        解析响应的消息
        :param client:
        :param userdata:
        :param msg:
        :return:
        """
        if msg.topic == "data/rt/pcu/1":
            self.pcu_sct_message_unpack(msg)
        elif msg.topic == f"ctrl/sct/4":
            self.ctrl_message_unpack(msg)
        elif msg.topic == "ctrl/mcs/":
            self.ctrl_message_unpack(msg)
        elif msg.topic == "data/all/sct/4":
            self.sct_all_message_unpack(msg)
        elif msg.topic == "data/status/sct/4":
            self.sct_status_message_unpack(msg)
        # else:
        #     print(f"<SCT>:{time.time()} Received payload:`{len(msg.payload)}` from topic `{msg.topic}` Qos {msg.qos}")

    def pcu_sct_message_unpack(self, msg):
        """
        解析PCU发送给SCT的topic "data/rt/pcu/1" 消息
        :param msg:
        :return:
        """
        _func = sys._getframe().f_code.co_name
        pcu_sct_real = PCU_SCT_REAL()
        try:
            pcu_sct_real.ParseFromString(msg.payload)
        except Exception as e:
            print(f"<SCT>:func {_func} parse pcu topic `data/rt/pcu/1` happen error: {e}, payload:{msg.payload}")
        else:
            pass
            # print(
            #     f"<SCT>:{time.asctime()},func {_func},topic>>{msg.topic},Qos>>{msg.qos}")

    def ctrl_message_unpack(self, msg):
        """
        解析发送给SCT的控制消息，控制响应消息:f"ctrl/sct/{self.sct}"
        :param msg:
        :return:
        """
        _func = sys._getframe().f_code.co_name
        ctrl_pcu_reply = CTRL_MESSAGE()
        try:
            ctrl_pcu_reply.ParseFromString(msg.payload)
        except Exception as e:
            print(f"<SCT>:func {_func} parse ctrl message happen error: {e}, payload:{msg.payload}")
        else:
            pass
            # args = ctrl_pcu_reply.req_args if ctrl_pcu_reply.ctrl_type == 0 else ctrl_pcu_reply.rep_args
            # print(
            #     f"<SCT>:{time.asctime()} topic>>{msg.topic}, device>>{ctrl_pcu_reply.device}, id>>{ctrl_pcu_reply.id}, timestamp>>{ctrl_pcu_reply.timestamp}, cmd_id>>{ctrl_pcu_reply.cmd_id}, args>>{args},Qos>>{msg.qos}")

    def sct_all_message_unpack(self, msg):
        _func = sys._getframe().f_code.co_name
        sct_msg = SCT_MESSAGE()
        try:
            sct_msg.ParseFromString(msg.payload)
        except Exception as e:
            print(f"<SCT>:func {_func} parse sct message happen error: {e}, payload:{msg.payload}")
        else:
            print(
                f"<SCT>:{time.time()} topic>>{msg.topic}, device>>{sct_msg.device}, id>>{sct_msg.id},timestamp>>{sct_msg.timestamp},Qos>>{msg.qos}")
            msg = ""
            for des, val in sct_msg.basic_info.ListFields():
                msg += f'{des.__dict__.get("name")}: {val}\n'
            for des, val in sct_msg.status_info.ListFields():
                msg += f'{des.__dict__.get("name")}: {val}\n'
            for des, val in sct_msg.alarm_info.ListFields():
                msg += f'{des.__dict__.get("name")}: {val}\n'
            for des, val in sct_msg.realtime_info.ListFields():
                msg += f'{des.__dict__.get("name")}: {val}\n'
            for des, val in sct_msg.event.ListFields():
                msg += f'{des.__dict__.get("name")}: {val}\n'
            for des, val in sct_msg.settings_info.ListFields():
                msg += f'{des.__dict__.get("name")}: {val}\n'
            for des, val in sct_msg.dtc_info.ListFields():
                msg += f'{des.__dict__.get("name")}: {val}\n'
            print(msg)

    def sct_status_message_unpack(self, msg):
        _func = sys._getframe().f_code.co_name
        sct_msg = SCT_STATUS_INFO_MESSAGE()
        try:
            sct_msg.ParseFromString(msg.payload)
        except Exception as e:
            print(f"<SCT>:func {_func} parse sct status message happen error: {e}, payload:{msg.payload}")
        else:
            pass
            # print(
            #     f"<SCT>:{time.asctime()} topic>>{msg.topic},Qos>>{msg.qos}")
            # self.dump_object(sct_msg)

    def publish(self):
        """

        :return:
        """
        while True:
            try:
                pass
                time.sleep(1)
            except Exception as e:
                _, exc_value, _ = sys.exc_info()
                time.sleep(1)

    def dump_object(self, obj):
        """
        遍历msg消息值,打印
        :param obj:
        :return:
        """

        for descriptor in obj.DESCRIPTOR.fields:
            value = getattr(obj, descriptor.name)
            if descriptor.type == descriptor.TYPE_MESSAGE:
                if descriptor.label == descriptor.LABEL_REPEATED:
                    map(self.dump_object, value)
                else:
                    self.dump_object(value)
            elif descriptor.type == descriptor.TYPE_ENUM:
                enum_name = descriptor.enum_type.values[value].name
                print("#### %s: %s" % (descriptor.full_name, enum_name))
            else:
                print("**** %s: %s" % (descriptor.full_name, value))


def start_sct_mqtt_process():
    """
    :return:
    """
    sct_mqtt = SctMqtt()
    time.sleep(5)
    print(f"connect_status:{str(sct_mqtt.connect_status)}")
    sct_mqtt.subscribe()
    sct_mqtt.client.loop_start()  # 是启用一个进程保持loop()的重复调用，就不需要定期心跳了，对应的有loop_stop()
    sct_mqtt.publish()


if __name__ == "__main__":
    start_sct_mqtt_process()
