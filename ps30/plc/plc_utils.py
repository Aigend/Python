# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/10/31 10:48
# @File:plc_utils.py
import sys
import threading
import time
from socket import *

from plc.plc_rep_msg import PLC_STATUS_REP_STRUCT
from plc.plc_req_msg import generate_PLC_REQUSET_STRUCT
from utils.log import log

threading_flag = False


def run(client, q):
    try:
        global threading_flag
        while True:
            if threading_flag:
                break
            recv_msg = client.recv(284)
            # log.info(f"<PLC>:正常打印主控下发给PLC的数据{len(recv_msg)}")
            req = generate_PLC_REQUSET_STRUCT(recv_msg)
    except Exception as e:
        _, exc_value, _ = sys.exc_info()
        log.error(f"<PLC>:PLC 此时接收主控数据也异常:{str(exc_value)}")
        time.sleep(1)


def start_plc_server_receive(q):
    """
        检查plc是否与主控成功建立了连接
    :param q:
    :return:
    """
    data = ""
    while not isinstance(data, PLC_STATUS_REP_STRUCT):
        if not q.empty():
            data = q.get()
        time.sleep(1)
    log.info("<PLC>:init struct data first")
    tcp_server = socket(AF_INET, SOCK_STREAM)
    tcp_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    address = ('0.0.0.0', 8000)
    log.info("<PLC>:bind 192.168.1.15 8000 port")
    tcp_server.bind(address)
    tcp_server.listen(128)
    while True:
        log.info('<PLC>:waiting for connection...')
        client_socket, client_addr = tcp_server.accept()
        log.info(f"<PLC>:client_socket:{client_socket}")
        log.info(f"<PLC>:client_addr:{client_addr}")
        # global threading_flag
        # th = threading.Thread(target=run, args=(client_socket, q))
        # th.daemon = True
        # th.start()
        while True:
            if not q.empty():
                data = q.get()
                log.info("<PLC>:update plc socket req")
            try:
                if isinstance(data, PLC_STATUS_REP_STRUCT):
                    client_socket.send(data)
                time.sleep(0.1)
            except Exception as e:
                _, exc_value, _ = sys.exc_info()
                log.error(f"<PLC>:PLC 发送PLC数据异常:{exc_value}")
                # threading_flag = True
                time.sleep(1)
                client_socket.close()
                break
        log.info("<PLC>:服务端状态如下：")
        if not getattr(tcp_server, '_closed'):
            log.warning("<PLC>:当前socket服务端正在运行中")
        elif getattr(tcp_server, '_closed'):
            log.warning("<PLC>:当前socket服务端已经关闭了")
