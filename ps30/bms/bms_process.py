# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/7/21 14:07
# @File:bms_process.py
import sys
import threading
import psutil
import time
from multiprocessing import Queue

import can

from bms.bms_can import send_data, can_recv
from utils.log import log


class MyThread(threading.Thread):
    lock = threading.Lock()
    boardx = [0 for _ in range(0, 1000)]
    q = Queue()

    def __init__(self, thread_id, name, bus, branch):
        """
        :param thread_id:
        :param name:
        :param branch:"board_d"
        :param bus:
        """
        super(MyThread, self).__init__()
        self.thread_id = thread_id
        self.name = name
        self.bus = bus
        self.branch = branch
        self.time_count_10ms = 1
        self.time_count_100ms = 1
        self.time_count_250ms = 1
        self.time_count_500ms = 1
        self.time_count_1000ms = 1
        self.can_send_data = [0 for _ in range(0, 8)]

    def update_bms_data(self):
        """
            不同进程获取数据使用同一个消息队列
        :return:
        """
        try:
            if not MyThread.q.empty():
                MyThread.boardx = MyThread.q.get()
                log.info(f"<BMS>:{self.branch},{self.bus.channel} bms data update")
        except Exception as e:
            _, exc_value, _ = sys.exc_info()
            log.error(f"<BMS>: update send data happen error:{exc_value}")

    def run(self):
        """

        :return:
        """
        log.info(f"enter {self.branch},{self.bus.channel} {self.name} can_send_bms_data function")
        if self.name == "Thread-1":
            log.info(f"{self.branch},{self.bus.channel}, Thread-1 is ready")
            while True:
                self.update_bms_data()
                if self.time_count_10ms % 10 == 2:
                    send_data(self.bus, 0xAF, MyThread.boardx[0:8], False, branch=self.branch, lock=MyThread.lock)  # AF
                elif self.time_count_10ms % 10 == 5:
                    # print('thread 1 --> AC')
                    send_data(self.bus, 0xAC, MyThread.boardx[8:16], False, branch=self.branch,
                              lock=MyThread.lock)  # AC
                elif self.time_count_10ms % 10 == 8:
                    # print('thread 1 --> AD')
                    send_data(self.bus, 0xAD, MyThread.boardx[16:24], False, branch=self.branch,
                              lock=MyThread.lock)  # AD
                elif self.time_count_10ms % 10 == 0:
                    # print('thread 1 --> AE')
                    send_data(self.bus, 0xAE, MyThread.boardx[24:32], False, branch=self.branch,
                              lock=MyThread.lock)  # AE
                    self.time_count_10ms = 0
                self.time_count_10ms = self.time_count_10ms + 1
                time.sleep(0.001)
        elif self.name == "Thread-2":
            log.info(f"{self.branch},{self.bus.channel}, Thread-2 is ready")
            while True:
                volt_frame_num = MyThread.boardx[998]
                if 15 <= self.time_count_1000ms % 100 < volt_frame_num + 15:
                    start = 230 + ((self.time_count_1000ms % 100) - 15) * 8
                    end = start + 8
                    send_data(self.bus, 0x26C, MyThread.boardx[start:end], False, branch=self.branch,
                              lock=MyThread.lock)  # 374
                elif self.time_count_1000ms % 100 == 66:
                    send_data(self.bus, 0x267, MyThread.boardx[32:40], False, branch=self.branch,
                              lock=MyThread.lock)  # 267
                elif self.time_count_1000ms % 100 == 67:
                    send_data(self.bus, 0x268, MyThread.boardx[40:48], False, branch=self.branch,
                              lock=MyThread.lock)  # 268
                elif self.time_count_1000ms % 100 == 68:
                    send_data(self.bus, 0x269, MyThread.boardx[48:56], False, branch=self.branch,
                              lock=MyThread.lock)  # 269
                elif self.time_count_1000ms % 100 == 69:
                    send_data(self.bus, 0x26A, MyThread.boardx[56:64], False, branch=self.branch,
                              lock=MyThread.lock)  # 26A
                elif self.boardx[997] == 8 and self.time_count_1000ms % 100 == 70:
                    send_data(self.bus, 0x29A, MyThread.boardx[750:758], False, branch=self.branch,
                              lock=MyThread.lock)  # 26A
                elif self.boardx[997] == 8 and self.time_count_1000ms % 100 == 71:
                    send_data(self.bus, 0x29B, MyThread.boardx[758:766], False, branch=self.branch,
                              lock=MyThread.lock)  # 29B
                elif self.time_count_1000ms % 100 == 72:
                    send_data(self.bus, 0x274, MyThread.boardx[742:750], False, branch=self.branch,
                              lock=MyThread.lock)  # 274

                elif self.time_count_1000ms % 500 == 98:
                    # print('thread 4 --> 372')
                    send_data(self.bus, 0x372, MyThread.boardx[112:120], False, branch=self.branch,
                              lock=MyThread.lock)  # 372
                elif self.time_count_1000ms % 500 == 99:
                    # print('thread 4 --> 373')
                    send_data(self.bus, 0x373, MyThread.boardx[120:128], False, branch=self.branch,
                              lock=MyThread.lock)  # 373

                elif self.time_count_1000ms % 1000 == 0:
                    send_data(self.bus, 0x376, MyThread.boardx[766:774], False, branch=self.branch,
                              lock=MyThread.lock)  # 376
                    self.time_count_1000ms = 1
                elif self.time_count_1000ms % 1000 == 73:
                    send_data(self.bus, 0x379, MyThread.boardx[774:782], False, branch=self.branch,
                              lock=MyThread.lock)  # 379
                self.time_count_1000ms = self.time_count_1000ms + 1
                time.sleep(0.001)
        elif self.name == "Thread-3":
            log.info(f"{self.branch},{self.bus.channel}, Thread-3 is ready")
            while True:
                temp_frame_num = MyThread.boardx[999]
                if 75 <= self.time_count_250ms % 250 < temp_frame_num + 75:
                    start = 614 + ((self.time_count_250ms % 250) - 75) * 8
                    end = start + 8
                    send_data(self.bus, 0x374, MyThread.boardx[start:end], False, branch=self.branch,
                              lock=MyThread.lock)  # 374
                elif self.time_count_250ms % 250 == 93:
                    send_data(self.bus, 0x26f, MyThread.boardx[72:80], False, branch=self.branch,
                              lock=MyThread.lock)  # 26F
                elif self.time_count_250ms % 250 == 94:
                    send_data(self.bus, 0x270, MyThread.boardx[80:88], False, branch=self.branch,
                              lock=MyThread.lock)  # 270
                elif self.time_count_250ms % 250 == 95:
                    send_data(self.bus, 0x271, MyThread.boardx[88:96], False, branch=self.branch,
                              lock=MyThread.lock)  # 271
                elif self.time_count_250ms % 250 == 96:
                    send_data(self.bus, 0x272, MyThread.boardx[96:104], False, branch=self.branch,
                              lock=MyThread.lock)  # 272
                elif self.time_count_250ms % 250 == 97:
                    send_data(self.bus, 0x273, MyThread.boardx[104:112], False, branch=self.branch,
                              lock=MyThread.lock)  # 273
                self.time_count_250ms = self.time_count_250ms + 1
                time.sleep(0.001)
        elif self.name == "Thread-4":
            log.info(f"{self.branch},{self.bus.channel}, Thread-4 is ready")
            while True:
                can_recv(self.bus, MyThread.boardx, branch=self.branch, lock=MyThread.lock)
                time.sleep(0.001)


def start_can_send_process(branch, bus, boardx, q):
    """

    :param branch:
    :param bus:
    :param boardx:
    :param q:
    :return:
    """
    log.info(f"<BMS>:enter {bus} {branch} start can send process func")
    MyThread.boardx = boardx
    MyThread.q = q
    bus = can.interface.Bus(bustype="socketcan", channel=bus, bitrate=500000)
    thread1 = MyThread(1, "Thread-1", bus, branch, )
    thread2 = MyThread(2, "Thread-2", bus, branch, )
    thread3 = MyThread(3, "Thread-3", bus, branch, )
    thread4 = MyThread(4, "Thread-4", bus, branch, )
    thread_pool = [thread1, thread2, thread3, thread4]
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    for th in thread_pool:
        th.join()


def front_start_can_send_process(brn_node, can_node, boardx, bms_process_pool, q, typ, alive):
    """

    :param brn_node:
    :param can_node:
    :param boardx:
    :param bms_process_pool
    :param q:
    :param typ:
    :param alive:
    :return:
    """
    if typ in ["all", "basic"] and alive:
        log.info(f"<BMS>:BMS子进程{bms_process_pool[can_node].pid}存在，进行kill重启操作")
        proc = psutil.Process(bms_process_pool[can_node].pid)
        proc.kill()
        time.sleep(10)
    log.info(f"<BMS>:enter {can_node} {brn_node} start can send process func")
    MyThread.boardx = boardx
    MyThread.q = q
    bus = can.interface.Bus(bustype="socketcan", channel=can_node, bitrate=500000)
    thread1 = MyThread(1, "Thread-1", bus, brn_node, )
    thread2 = MyThread(2, "Thread-2", bus, brn_node, )
    thread3 = MyThread(3, "Thread-3", bus, brn_node, )
    thread4 = MyThread(4, "Thread-4", bus, brn_node, )
    thread_pool = [thread1, thread2, thread3, thread4]
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    for th in thread_pool:
        th.join()
