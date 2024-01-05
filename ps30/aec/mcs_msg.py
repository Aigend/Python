# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/4/28 14:47
# @File: mcs_msg.py
"""模拟MCS和仿真AEC通信

本模块只用于调试和压测使用，对仿真工具框架无任何影响

在无真实站环境下调试
"""
import json
import threading
import time
from multiprocessing import Pipe, Process

import zmq
import sys
import os

if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(os.getcwd()), "utils"))

from utils.log import log

# aec_ip = "tcp://127.0.0.1:8801"
# mcs_ip = "tcp://127.0.0.1:8802"

aec_ip = "tcp://192.168.1.13:8800"
mcs_ip = "tcp://192.168.1.10:8800"

result = {
    "timestamp": "",
    "total": 0,
    "pass": 0,
    "fail": 0,
    "detail": []
}


def receive(out_pipe, in_pipe):
    """
    接收AEC的返回数据，并进行打印，暂不处理
    :param out_pipe:
    :param in_pipe:
    :return:
    """
    out_pipe.close()
    topic = b"AEC"
    context = zmq.Context()
    log.info(f"<MCS>:Connecting `{aec_ip}` server…")
    sub_socket = context.socket(zmq.SUB)
    sub_socket.connect(aec_ip)
    sub_socket.subscribe(topic)
    while True:
        rec = sub_socket.recv_multipart()
        msg_topic = rec[0].decode()  # MCS
        msg_timestamp = rec[1].decode()
        msg_type = rec[2].decode()  # b"HB"
        msg_command = rec[3].decode()  #
        msg_comment = rec[4].decode()  #
        log.info(
            f"<MCS>:recv msg_topic:{msg_topic}, msg_type:{msg_type}, msg_command:{msg_command}, msg_comment:{msg_comment}, msg_timestamp:{msg_timestamp}")
        # if count == 5:
        #     count += 1
        #     msg_topic = b"MCS"
        #     msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
        #     msg_type = b"INFO"
        #     msg_command = b"STEP"
        #     msg_comment = json.dumps({"step": "2201"}).encode()
        #     in_pipe.send([msg_topic, msg_timestamp, msg_type, msg_command, msg_comment])
        #     time.sleep(1)
        # elif count == 10:
        #     count = 0
        #     msg_topic = b"MCS"
        #     msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
        #     msg_type = b"INFO"
        #     msg_command = b"STEP"
        #     msg_comment = json.dumps({"step": "2202"}).encode()
        #     in_pipe.send([msg_topic, msg_timestamp, msg_type, msg_command, msg_comment])
        #     time.sleep(5)
        # elif msg_type == "HB":
        #     count += 1
        #     print(f"conut:{count}")


def send_HB(pub_socket):
    """
    MCS 发布心跳信号
    :param pub_socket:
    :return:
    """
    while True:
        msg_topic = b"MCS"
        msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
        msg_type = b"HB"
        msg_command = b""
        msg_comment = b""
        pub_socket.send_multipart([msg_topic, msg_timestamp, msg_type, msg_command, msg_comment])
        time.sleep(1)


def send_station_id(pub_socket):
    """
    MCS send 站ID
    :param pub_socket:
    :return:
    """
    while True:
        msg_topic = b"MCS"
        msg_timestamp = bytes(str(int(time.time() * 1000)), encoding='utf-8')
        msg_type = b"INFO"
        msg_command = b"SWAP-ID"
        msg_comment = b"PS-NIO-ad1100b5-98123ce6"
        pub_socket.send_multipart([msg_topic, msg_timestamp, msg_type, msg_command, msg_comment])
        time.sleep(0.5)


def send_reply_data(pub_socket, out_pipe):
    """
    接收到AEC发送的数据，控制返回的信息
    :param pub_socket:
    :param out_pipe:
    :return:
    """
    # data = {}
    while True:
        content = out_pipe.recv()
        # if isinstance(content, dict):
        #     data.update(content)
        #     log.info("<MCS>:update reply data")
        log.info(f"<MCS>:reply:{content}")
        pub_socket.send_multipart(content)
        # data.clear()


def send(queue, out_pipe, in_pipe):
    """
    MCS 发布 心跳
    :param queue:
    :param out_pipe:
    :param in_pipe:
    :return:
    """
    context = zmq.Context()
    pub_socket = context.socket(zmq.PUB)
    pub_socket.bind(mcs_ip)
    log.info(f"<MCS>:MCS bind `{mcs_ip}`, rec script data and send to `{aec_ip}` ...")
    in_pipe.close()
    data = {}  # 这里存储MCS发送的心跳信息数据
    threads = [threading.Thread(target=send_HB, args=(pub_socket,)),
               threading.Thread(target=send_station_id, args=(pub_socket,)),
               threading.Thread(target=send_reply_data, args=(pub_socket, out_pipe))]
    for th in threads:
        th.daemon = True
        th.start()
    while True:
        # 脚本发送需要发送给AEC的数据，这里发送给AEC
        if not queue.empty():
            data = queue.get()
        if isinstance(data, list) and not data:
            pub_socket.send_multipart(data)
        time.sleep(1)  # 避免长时间占用CPU


def mcs_init_process(procs, queue):
    """

    :param procs:
    :param queue:
    :return:
    """
    rcv = procs.get("receive")
    snd = procs.get("send")
    if not (isinstance(snd, Process) and snd.is_alive() and isinstance(rcv, Process) and rcv.is_alive()):
        out_pipe, in_pipe = Pipe()  # 用于脚本和数据更新监听使用
        procs["receive"] = Process(target=receive, args=(out_pipe, in_pipe))
        procs["send"] = Process(target=send, args=(queue, out_pipe, in_pipe))
        procs["receive"].daemon = True
        procs["receive"].start()
        procs["send"].daemon = True
        procs["send"].start()
        log.info(f"<MCS>:MCS sub process receive {procs['receive'].pid}, send {procs['send'].pid}")


if __name__ == "__main__":
    from multiprocessing import Queue

    q = Queue()
    procs = {}
    mcs_init_process(procs, q)
    while True:
        time.sleep(100)
