"""
@Project: ps30
@File: utils.py
@Author: wenlong.jin
@Time: 2023/11/14 10:52
@version: 1.0.0
@Description:
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from paho.mqtt import client as mqtt_client

from mpc.MCS_CONTROL_pb2 import BatteryCompartment
from utils.log import log


def demo():
    """
    本地测试demo
    :return:
    """
    ctrl_msg = BatteryCompartment()
    ctrl_msg.ParseFromString(b'\x08\x04\x10\x10')  # 调试关闭A7 手动停止充电
    print(ctrl_msg.device)
    print(ctrl_msg.index)
    print(ctrl_msg.action)


class MpcMqtt:

    def __init__(self, queue):
        def on_connect(client, userdata, flags, rc):
            """
                0	连接成功
                1	协议版本错误
                2	无效的客户端标识
                3	服务器无法使用
                4	错误的用户名或密码
                5	未经授权
            :param client:
            :param userdata:
            :param flags:
            :param rc:
            :return:
            """
            if rc == 0:
                log.info("<MPC>:Connected to MQTT Broker!")
            else:
                log.error(f"<MPC>: Failed to connect, return code {rc}")

        self.queue = queue
        self.pdu_rep_json = {}
        self.obj = ""
        self.client = mqtt_client.Client('python3-mpc-mqtt', clean_session=False)
        self.client.username_pw_set('pp', 'N7102io')
        self.client.on_connect = on_connect
        self.client.connect('192.168.1.10', 8200, keepalive=10)

    def publish(self):
        """

        :return:
        """
        branch = ""
        ctrl_mcs_battery_topic = "ctrl/mcs/compartment"
        ctrl_msg = BatteryCompartment()
        ctrl_msg.ParseFromString(b'\x08\x04\x10\x10')  # 调试关闭A7 手动停止充电
        while True:
            if self.queue.empty():
                time.sleep(1)
                continue
            _info = self.queue.get()
            if not isinstance(_info, (str, int)):
                break
            branch = _info
            ctrl_msg.index = int(branch)  # 修改关闭的支路
            obj = ctrl_msg.SerializeToString()
            res = self.client.publish(ctrl_mcs_battery_topic, payload=obj)
            if res[0] != 0:
                log.error(f"<MPC>:mpc send topic `ctrl/mcs/compartment` fail, res {res[0]}")


def start_mpc_process(queue):
    """

    :param queue:
    :return:
    """
    mpc_mqtt = MpcMqtt(queue)
    # loop_forever()用来保持无穷阻塞调用loop()
    mpc_mqtt.client.loop_start()  # 是启用一个进程保持loop()的重复调用，就不需要定期心跳了，对应的有loop_stop()
    mpc_mqtt.publish()


# def set_mpc_status(branch):
#     """
#     模拟MPC，发出停止充电的动作
#     :param branch:
#     :return:
#     """
#     client = mqtt_client.Client('python3-mpc-mqtt', clean_session=False)
#     client.username_pw_set('pp', 'N7102io')
#     client.connect('192.168.1.10', 8200, keepalive=10)
#     client.loop_start()
#     ctrl_msg = BatteryCompartment()
#     ctrl_msg.ParseFromString(b'\x08\x04\x10\x10')  # 调试关闭A7 手动停止充电
#     ctrl_msg.index = int(branch)
#     obj = ctrl_msg.SerializeToString()
#     res = client.publish("ctrl/mcs/compartment", payload=obj)
#     if res[0] != 0:
#         log.error(f"<MPC>:mpc send topic `ctrl/mcs/compartment` fail, res {res[0]}")
#     client.disconnect()
#     client.loop_stop()


if __name__ == '__main__':
    demo()
