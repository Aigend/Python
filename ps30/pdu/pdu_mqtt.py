# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/2/1 9:24
# @File: pdu_mqtt.py
import time

from paho.mqtt import client as mqtt_client
from PUS_ctrl_message_pb2 import CTRL_MESSAGE
from pdu.pdu_msg import PduReplyMsg

from utils.log import log


class PduMqtt:

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
                log.info("<PDU>:Connected to MQTT Broker!")
            else:
                log.error(f"<PDU>: Failed to connect, return code {rc}")

        self.queue = queue
        self.pdu_rep_json = {}
        self.obj = ""
        self.client = mqtt_client.Client('python3-pdu-mqtt', clean_session=False)
        self.client.username_pw_set('pp', 'N7102io')
        self.client.on_connect = on_connect
        self.client.connect('192.168.1.10', 8200, keepalive=5)

    def subscribe(self):
        """

        :return:
        """
        self.client.on_message = self.on_message
        self.client.subscribe("ctrl/pdu/1")

    def on_message(self, client, userdata, msg):
        """
        接收到控制pdu的命令，进行返回消息设置并返回
        :param client:
        :param userdata:
        :param msg:
        :return:
        """
        ctrl_msg = CTRL_MESSAGE()
        ctrl_msg.ParseFromString(msg.payload)
        cmd_id = hex(ord(ctrl_msg.cmd_id))
        self.reply_pcu_ctrl_msg(ctrl_msg.cmd_id)
        if cmd_id == "0x10":
            self.print_cmd_info(msg, cmd_id, ctrl_msg)
            self.set_relay_state(ctrl_msg)
        elif cmd_id == "0x20":
            log.info(f"<PDU>:Received from `{msg.topic}` topic, cmd_id:`{cmd_id}`, payload: {msg.payload}")
        elif cmd_id == "0x21":
            log.info(f"<PDU>:Received from `{msg.topic}` topic, cmd_id:`{cmd_id}`, payload: {msg.payload}")
        elif cmd_id == "0x40":  #
            log.info(f"<PDU>:Received from `{msg.topic}` topic, cmd_id:`{cmd_id}`, payload: {msg.payload}")
        elif cmd_id == "0x41":  # 19-35批量控制诊断
            log.info(f"<PDU>:Received from `{msg.topic}` topic, cmd_id:`{cmd_id}`, payload: {msg.payload}")
        elif cmd_id == "0x42":  # 继电器单个操作
            log.info(f"<PDU>:Received from `{msg.topic}` topic, cmd_id:`{cmd_id}`, payload: {msg.payload}")
        elif cmd_id == "0x45":  # 复位命令
            log.info(f"<PDU>:Received from `{msg.topic}` topic, cmd_id:`{cmd_id}`, payload: {msg.payload}")
            self.pdu_reset()
        elif cmd_id == "0x46":
            pass
            # log.info(f"<PDU>:Received from `{msg.topic}` topic, cmd_id:`{cmd_id}`, payload: {msg.payload}")
        elif cmd_id == "0x50":
            pass

    def print_cmd_info(self, msg, cmd_id, ctrl_msg):
        log.info(f"<PDU>:Received from `{msg.topic}` topic, cmd_id:`{cmd_id}`, payload: {msg.payload}")
        if cmd_id == "0x10":
            cmd = hex(ord(ctrl_msg.req_args[0]))
            module = hex(ord(ctrl_msg.req_args[1]))
            branch = hex(ord(ctrl_msg.req_args[2]))
            log.info(f"<PDU>:cmd `{cmd}`, module:`{module}`, branch: {branch}")

    def pdu_reset(self):
        tmp = {
            "104001": 28,
            "104002": 28,
            "104003": 28,
            "104004": 28,
            "104101": 63,
            "104102": 60,
            "104103": 52,
            "104104": 71,
            "104105": 55,
            "104106": 47,
            "104107": 47,
            "104108": 71,

            "104011": 28,
            "104012": 28,
            "104013": 28,
            "104014": 28,
            "104121": 52,
            "104122": 52,
            "104123": 60,
            "104124": 60,
            "104125": 58,
            "104126": 37,
            "104127": 55,
            "104128": 55,

            "104021": 27,
            "104022": 27,
            "104023": 27,
            "104024": 27,
            "104141": 71,
            "104142": 63,
            "104143": 58,
            "104144": 24,
            "104145": 44,
            "104146": 44,
            "104147": 42,
            "104148": 47,

            "104031": 27,
            "104032": 27,
            "104033": 26,
            "104034": 26,
            "104161": 56,
            "104162": 57,
            "104163": 47,
            "104164": 58,
            "104165": 60,
            "104166": 50,
            "104167": 68,
            "104168": 39,

            "104041": 25,
            "104042": 25,
            "104043": 25,
            "104044": 25,
            "104181": 79,
            "104182": 26,
            "104183": 68,
            "104184": 48,
            "104185": 51,
            "104186": 51,
            "104187": 50,
            "104188": 55,

            "104300": 0,
            "104301": 0,
            "104306": 0,
            "104307": 0,
            "104308": 0,
            "104309": 0,

            "104314": 0,
            "104315": 0,
            "104320": 0,
            "104321": 0,
            "104322": 0,
            "104323": 0,

            "104328": 0,
            "104329": 0,
            "104334": 0,
            "104335": 0,
            "104336": 0,
            "104337": 0,

            "104342": 0,
            "104343": 0,
            "104348": 0,
            "104349": 0,
            "104350": 0,
            "104351": 0,

            "104356": 0,
            "104357": 0,
            "104362": 0,
            "104363": 0,
            "104364": 0,
            "104365": 0
        }
        self.queue.put(tmp)

    def set_relay_state(self, ctrl_msg):
        cmd = ord(ctrl_msg.req_args[0])
        module = ord(ctrl_msg.req_args[1])
        branch = ord(ctrl_msg.req_args[2])
        state = 0 if cmd == 0x0C else 1
        mod = (module - 1) // 2  # 0-4
        tmp = (module - 1) % 2  # 0, 1
        key_pos_start = 104300 if tmp == 0 else 104308
        key_neg_start = 104301 if tmp == 0 else 104309
        key_mid_pos_start = 104306  # 柔性充电时关闭KM4
        key_mid_neg_start = 104307  # 柔性充电时关闭KM4
        if module == branch:
            pos = str(key_pos_start + 14 * mod)
            neg = str(key_neg_start + 14 * mod)
        else:
            pos = str(key_mid_pos_start + 14 * mod)
            neg = str(key_mid_neg_start + 14 * mod)
        log.warning(f"<PDU>:update {pos}, {neg} cmd {cmd}, state {state}")
        tmp = {pos: state, neg: state}
        self.queue.put(tmp)

    def reply_pcu_ctrl_msg(self, cmd_id):
        """

        :return:
        """
        ctrl_msg = CTRL_MESSAGE()
        ctrl_msg.device = 1
        ctrl_msg.id = 1
        ctrl_msg.ctrl_type = 1
        ctrl_msg.cmd_id = cmd_id
        send_msg = ctrl_msg.SerializeToString()
        self.client.publish("ctrl/pcu/1", send_msg)

    def publish(self):
        """

        :return:
        """
        send_msg = ""
        pdu_data_topic = "data/all/pdu/1"  # PDU发送给PCU的实时数据
        while True:
            if not self.queue.empty():
                update = self.queue.get()
                self.pdu_rep_json.update(update)
                obj = PduReplyMsg(self.pdu_rep_json)
                send_msg = obj.pdu_msg.SerializeToString()
            time.sleep(0.1)  # 100ms的周期发送
            if send_msg:
                result = self.client.publish(pdu_data_topic, send_msg)
                if result[0] != 0:  # result: [0, 1]
                    log.warning(f"<PDU>:Failed to send real time data message to topic")


def start_mqtt_send_process(queue):
    """

    :param queue:
    :return:
    """
    pdu_mqtt = PduMqtt(queue)
    pdu_mqtt.subscribe()
    # loop_forever()用来保持无穷阻塞调用loop()
    pdu_mqtt.client.loop_start()  # 是启用一个进程保持loop()的重复调用，就不需要定期心跳了，对应的有loop_stop()
    pdu_mqtt.publish()
