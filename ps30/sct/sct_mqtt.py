# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/4/28 13:57
# @File: sct_mqtt.py
import time
import threading
from enum import Enum, unique

from paho.mqtt import client as mqtt_client

from PUS_ctrl_message_pb2 import *
from PCU_pb2 import *
from utils.log import log


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

    def __init__(self, queue, sct):
        """

        :param queue:
        :param sct:

        """
        self.queue = queue
        self.sct = sct + 1
        self.connect_status = 0
        self.client = mqtt_client.Client(f'LOCAL/SCT_{self.sct}', clean_session=False)
        self.client.username_pw_set('pp', 'N7102io')
        self.client.on_connect = self.on_connect
        self.client.connect('192.168.1.10', 8200, keepalive=5)

        self.topic_data_all_sct = f"data/all/sct/{self.sct}"  # // sct-mcs
        # self.topic_data_basic_sct = f"data/basic/sct/{self.sct}"
        # self.topic_data_rt_sct = f"data/rt/sct/{self.sct}"
        # self.topic_data_alarm_sct = f"data/alarm/sct/{self.sct}"
        # self.topic_data_event_sct = f"data/event/sct/{self.sct}"

        self.topic_ctrl_pcu = "ctrl/pcu/1"  # // sct-pcu
        # self.topic_send_topic = "sendTopic"
        # self.topic_rota_server_sct = "rota/server/sct/"  # // sct-mcs ver result
        # self.topic_debug_mcs = "debug/mcs/"  # // sct-mcs r
        # self.topic_ota_server_sct = "ota/server/sct/"  # // sct-mcs
        self.topic_data_status_sct = f"data/status/sct/{self.sct}"  # // sct-pcu
        # self.topic_data_set_sct = "data/set/sct/"
        self.topic_ctrl_mcs = "ctrl/mcs/"  # // sct-mcs ### SCT 发送给SCT的控制响应topic
        # self.topic_txt_mcs = "txt/mcs/"  # // sct-mcs

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connect_status = 1
            log.info(f"<SCT>:sct{self.sct} Connected to MQTT Broker!")
        else:
            log.error(f"<SCT>:sct{self.sct} Failed to connect mcs broker, return code {rc}")

    def on_subscribe(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        print(f"<SCT>:sct{self.sct} subscribe success")

    def subscribe(self):
        """

        :return:
        """

        # self.client.on_subscribe = on_subscribe
        self.client.on_message = self.on_message

        # self.client.subscribe(f"data/all/mcs/")  # // mcs-sct
        self.client.subscribe(f"ctrl/sct/{self.sct}")  # pcu-sct mcs-sct
        # self.client.subscribe(f"recvTopic")  #
        # self.client.subscribe(f"ota/sct/{self.sct}")  # mcs-sct result
        # self.client.subscribe(f"debug/sct/{self.sct}")  # mcs-sct r
        # self.client.subscribe(f"ota/client/sct/{self.sct}")  # mcs-sct
        self.client.subscribe(f"data/rt/pcu/1")  # pcu-sct
        # self.client.subscribe(f"data/set/mcs/{self.sct}")  # mcs-sct
        # self.client.subscribe(f"txt/mcs/{self.sct}")  # mcs-sct

    def on_message(self, client, userdata, msg):
        """
        解析响应的消息
        :param client:
        :param userdata:
        :param msg:
        :return:
        """
        if msg.topic == "data/rt/pcu/1":
            self.sct_unpack_pcu_rt_msg(msg)
        elif msg.topic == f"ctrl/sct/{self.sct}":
            self.sct_unpack_ctrl_msg(msg)
        else:
            log.warning(f"Received payload:`{len(msg.payload)}` from topic `{msg.topic}` Qos `{msg.qos}`")

    def sct_unpack_pcu_rt_msg(self, msg):
        """
        解析PCU发送给SCT的topic "data/rt/pcu/1" 消息
        :param payload:
        :return:
        """
        _func = sys._getframe().f_code.co_name
        pcu_sct_real = PCU_SCT_REAL()
        try:
            pcu_sct_real.ParseFromString(msg.payload)
        except Exception as e:
            log.error(f"<SCT>:func {_func} parse pcu topic `data/rt/pcu/1` happen error: {e}, payload:{msg.payload}")
        # else:
        #     for i in range(len(pcu_sct_real.pcu_channel_real)):
        #         obj = pcu_sct_real.pcu_channel_real[i]
        #         # self.dump_object(obj)
        #         msg = f"<SCT> sct{i + 1} channel info"
        #         for des, val in obj.ListFields():
        #             msg += f', {des.__dict__.get("name")}: {val}'
        #         print(msg)

    def sct_unpack_ctrl_msg(self, msg):
        """
        解析发送给SCT的控制消息，控制响应消息:f"ctrl/sct/{self.sct}"
        :param msg:
        :return:
        """
        _func = sys._getframe().f_code.co_name
        ctrl_msg = CTRL_MESSAGE()
        try:
            ctrl_msg.ParseFromString(msg.payload)
        except Exception as e:
            print(f"<SCT>:func {_func} parse ctrl message happen error: {e}, payload:{msg.payload}")
        else:
            print(
                f"<SCT>:{time.asctime()} func {_func},device>>{ctrl_msg.device}, id>>{ctrl_msg.id}, cmd_id>>{ctrl_msg.cmd_id},rep_args>>{ctrl_msg.req_args}")
            if msg.topic == f"ctrl/sct/{self.sct}":
                data = self.sct_pack_mcs_ctrl_reply_msg(ctrl_msg)
                result = self.client.publish(f"ctrl/mcs/", data)
                if result[0] != 0:  # result: [0, 1]
                    log.error(f"<SCT>:sct failed to send mcs ctrl reply msg")

    def sct_pack_pcu_ctrl_req_msg(self, cmd_id: SCT_CTRL_PCU_ENUM, data: list):
        """
        SCT 发送给PCU的控制消息
        :param cmd_id:
        :param data: list类型，元素为element.isnumeric()为True的字符串
            data 中各元素的含义代表如下：
            - voltage_req；
            - current_req;
            - bms_measure_voltage；  电池测量电压
            - cc1_sts;   1-断开，0-闭合（仅认证测试用）
            - region;   1-欧标，0-国标
            - emulate_charge： 1-不检测电池电压，0-检测电池电压
        :return:
        """
        ctrl_pcu_req = CTRL_MESSAGE()
        ctrl_pcu_req.device = 3
        ctrl_pcu_req.id = self.sct  # 1-4
        ctrl_pcu_req.timestamp = 0
        ctrl_pcu_req.ctrl_type = CTRL_TYPE.REQ  # req 0, rep 1
        ctrl_pcu_req.cmd_id = str(cmd_id.value).encode()
        ctrl_pcu_req.req_args.extend(data)
        # ctrl_pcu.req_args.append(str(data.get('charge_volt_req', '0')))
        # ctrl_pcu.req_args.append(str(data.get('charge_curr_req', '0')))
        # ctrl_pcu.req_args.append(str(data.get('battery_volt', '0')))
        # ctrl_pcu.req_args.append(str(data.get('cc1_state', '0')))
        # ctrl_pcu.req_args.append(str(data.get('region', '0'))) #  1-欧标，0-国标
        # ctrl_pcu.req_args.append(str(data.get('emulate_charge', '0')))
        return ctrl_pcu_req

    def sct_pack_mcs_ctrl_reply_msg(self, ctrl_msg):
        """
        SCT 发送给MCS的控制响应消息
        :return:
        """
        mcs_ctrl_rep = CTRL_MESSAGE()
        mcs_ctrl_rep.device = 3
        mcs_ctrl_rep.id = self.sct  # 1-4
        mcs_ctrl_rep.timestamp = 0
        mcs_ctrl_rep.ctrl_type = CTRL_TYPE.REP  # req 0, rep 1
        mcs_ctrl_rep.cmd_id = ctrl_msg.cmd_id
        for arg in ctrl_msg.req_args:
            mcs_ctrl_rep.rep_args.append(arg)
        data = mcs_ctrl_rep.SerializeToString()
        return data

    def sct_status_msg_threading(self, data):
        """
        SCT 发送给status信息, 周期500ms
        :return:
        """
        while True:
            if data.get("status"):
                result = self.client.publish(self.topic_data_status_sct, data.get("status"))
                if result[0] != 0:  # result: [0, 1]
                    log.error(f"<SCT>:sct failed to send topic `{self.topic_data_status_sct}` data")
            time.sleep(0.5)  # 500ms发送一次心跳

    def sct_all_msg_threading(self, data):
        """
        SCT 发送给全量信息, 周期1s
        :return:
        """
        while True:
            if data.get("all"):
                result = self.client.publish(self.topic_data_all_sct, data.get("all"))
                if result[0] != 0:  # result: [0, 1]
                    log.error(f"<SCT>:sct failed to send topic `{self.topic_data_all_sct}` data")
            time.sleep(1)  # 1s发送一次

    def publish(self):
        """

        :return:
        """
        data = {}
        sct_all_thread = threading.Thread(target=self.sct_all_msg_threading, args=(data,))
        sct_status_thread = threading.Thread(target=self.sct_status_msg_threading, args=(data,))
        sct_all_thread.daemon = True
        sct_status_thread.daemon = True
        sct_all_thread.start()
        sct_status_thread.start()
        while True:
            try:
                if not self.queue.empty():
                    data.update(self.queue.get())
                time.sleep(1)
            except Exception as e:
                _, exc_value, _ = sys.exc_info()
                log.error(f"<SCT>:sct back process update script data happen error:{exc_value}")
                time.sleep(1)


def start_sct_mqtt_process(queue, sct):
    """

    :param queue:
    :param sct:
    :return:
    """
    log.info(f"<SCT>:begin to create sct{sct} mqtt sub process")
    sct_mqtt = SctMqtt(queue, sct)
    time.sleep(5)
    log.info(f"<SCT>:connect_status:{str(sct_mqtt.connect_status)}")
    sct_mqtt.subscribe()
    sct_mqtt.client.loop_start()
    sct_mqtt.publish()


if __name__ == "__main__":
    pass
