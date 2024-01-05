# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/1/31 9:25
# @File: self.pdu_msg.py
import time

import PDU_pb2

r"""
D:\nio\mcu-app\LIB\Nanopb\user\PDU.pb.h
"""


class PduReplyMsg:
    fault_1 = {
        1: [0, 1, 2],
        2: [0, 1, 3],
        3: [0, 2, 3],
        4: [1, 5, 6],
        5: [1, 5, 7],
        6: [1, 6, 7],
    }

    fault_2 = {
        1: [1, 2],
        2: [1, 3],
        3: [1, 5],
        4: [1, 6],
        5: [1, 7],
        6: [2, 3],
        7: [2, 5],
        8: [2, 6],
        9: [2, 7],
        10: [3, 5],
        11: [3, 6],
        12: [3, 7],
        13: [5, 6],
        14: [5, 7],
        15: [6, 7],
    }

    def __init__(self, data):
        self.data = data
        self.pdu_msg = PDU_pb2.PDU_MESSAGE()

        self.pdu_msg.proto_version = 1
        self.pdu_msg.device = 1
        self.pdu_msg.id = 0
        self.pdu_msg.timestamp = int(round(time.time() * 1000))

        self.init_basic_info()
        self.init_realtime_info()

    def init_realtime_info(self):
        self.init_spdu_real_info()
        self.init_fpga_relay_state_info()
        self.init_fpga_pdu_fault_info()
        self.init_fpga_version_info()
        self.init_fpga_fault_code()

    def init_basic_info(self):
        """
            BASIC INFO 目前版本信息固定写死，调通后根据key值传入
        :return:
        """
        self.pdu_msg.basic_info.mcu_software_version = "023022.1.1.20"  # mcu软件版本号|PDU|||PDU|
        self.pdu_msg.basic_info.fpga_software_version = "023026.2.2.8"  # fpga软件版本号|PDU|||PDU|
        self.pdu_msg.basic_info.spdu1_software_version = "1.0.0.4"  # 子pdu1软件版本号|PDU|||PDU|
        self.pdu_msg.basic_info.spdu2_software_version = "1.0.0.4"  # 子pdu2软件版本号|PDU|||PDU|
        self.pdu_msg.basic_info.spdu3_software_version = "1.0.0.4"  # 子pdu3软件版本号|PDU|||PDU|
        self.pdu_msg.basic_info.spdu4_software_version = "1.0.0.4"  # 子pdu4软件版本号|PDU|||PDU|
        self.pdu_msg.basic_info.spdu5_software_version = "1.0.0.4"  # 子pdu5软件版本号|PDU|||PDU|

    def init_spdu_real_info(self, ):
        # 子PDU实时数据|PDU|PDU|||
        spdu_1 = self.pdu_msg.realtime_info.spdu_real.add()
        spdu_1.temperature_1 = int(self.data.get('104001', 0))
        spdu_1.temperature_2 = int(self.data.get('104002', 0))
        spdu_1.temperature_3 = int(self.data.get('104003', 0))
        spdu_1.temperature_4 = int(self.data.get('104004', 0))
        spdu_1.voltage_1 = float(self.data.get('104101', 0.0))
        spdu_1.voltage_2 = float(self.data.get('104102', 0.0))
        spdu_1.voltage_3 = float(self.data.get('104103', 0.0))
        spdu_1.voltage_4 = float(self.data.get('104104', 0.0))
        spdu_1.voltage_5 = float(self.data.get('104105', 0.0))
        spdu_1.voltage_6 = float(self.data.get('104106', 0.0))
        spdu_1.voltage_7 = float(self.data.get('104107', 0.0))
        spdu_1.voltage_8 = float(self.data.get('104108', 0.0))

        spdu_2 = self.pdu_msg.realtime_info.spdu_real.add()
        spdu_2.temperature_1 = int(self.data.get('104011', 0))
        spdu_2.temperature_2 = int(self.data.get('104012', 0))
        spdu_2.temperature_3 = int(self.data.get('104013', 0))
        spdu_2.temperature_4 = int(self.data.get('104014', 0))
        spdu_2.voltage_1 = float(self.data.get('104121', 0.0))
        spdu_2.voltage_2 = float(self.data.get('104122', 0.0))
        spdu_2.voltage_3 = float(self.data.get('104123', 0.0))
        spdu_2.voltage_4 = float(self.data.get('104124', 0.0))
        spdu_2.voltage_5 = float(self.data.get('104125', 0.0))
        spdu_2.voltage_6 = float(self.data.get('104126', 0.0))
        spdu_2.voltage_7 = float(self.data.get('104127', 0.0))
        spdu_2.voltage_8 = float(self.data.get('104128', 0.0))

        spdu_3 = self.pdu_msg.realtime_info.spdu_real.add()
        spdu_3.temperature_1 = int(self.data.get('104021', 0))
        spdu_3.temperature_2 = int(self.data.get('104022', 0))
        spdu_3.temperature_3 = int(self.data.get('104023', 0))
        spdu_3.temperature_4 = int(self.data.get('104024', 0))
        spdu_3.voltage_1 = float(self.data.get('104141', 0.0))
        spdu_3.voltage_2 = float(self.data.get('104142', 0.0))
        spdu_3.voltage_3 = float(self.data.get('104143', 0.0))
        spdu_3.voltage_4 = float(self.data.get('104144', 0.0))
        spdu_3.voltage_5 = float(self.data.get('104145', 0.0))
        spdu_3.voltage_6 = float(self.data.get('104146', 0.0))
        spdu_3.voltage_7 = float(self.data.get('104147', 0.0))
        spdu_3.voltage_8 = float(self.data.get('104148', 0.0))

        spdu_4 = self.pdu_msg.realtime_info.spdu_real.add()
        spdu_4.temperature_1 = int(self.data.get('104031', 0))
        spdu_4.temperature_2 = int(self.data.get('104032', 0))
        spdu_4.temperature_3 = int(self.data.get('104033', 0))
        spdu_4.temperature_4 = int(self.data.get('104034', 0))
        spdu_4.voltage_1 = float(self.data.get('104161', 0.0))
        spdu_4.voltage_2 = float(self.data.get('104162', 0.0))
        spdu_4.voltage_3 = float(self.data.get('104163', 0.0))
        spdu_4.voltage_4 = float(self.data.get('104164', 0.0))
        spdu_4.voltage_5 = float(self.data.get('104165', 0.0))
        spdu_4.voltage_6 = float(self.data.get('104166', 0.0))
        spdu_4.voltage_7 = float(self.data.get('104167', 0.0))
        spdu_4.voltage_8 = float(self.data.get('104168', 0.0))

        spdu_5 = self.pdu_msg.realtime_info.spdu_real.add()
        spdu_5.temperature_1 = int(self.data.get('104041', 0))
        spdu_5.temperature_2 = int(self.data.get('104042', 0))
        spdu_5.temperature_3 = int(self.data.get('104043', 0))
        spdu_5.temperature_4 = int(self.data.get('104044', 0))
        spdu_5.voltage_1 = float(self.data.get('104181', 0.0))
        spdu_5.voltage_2 = float(self.data.get('104182', 0.0))
        spdu_5.voltage_3 = float(self.data.get('104183', 0.0))
        spdu_5.voltage_4 = float(self.data.get('104184', 0.0))
        spdu_5.voltage_5 = float(self.data.get('104185', 0.0))
        spdu_5.voltage_6 = float(self.data.get('104186', 0.0))
        spdu_5.voltage_7 = float(self.data.get('104187', 0.0))
        spdu_5.voltage_8 = float(self.data.get('104188', 0.0))

    def init_fpga_relay_state_info(self):
        spdu_1_state = int(self.data.get("104300", 0)) & 0x01  # KM1
        spdu_1_state = spdu_1_state | ((int(self.data.get('104301', 0)) & 0x01) << 1)  # KM1
        spdu_1_state = spdu_1_state | ((int(self.data.get('104302', 0)) & 0x01) << 2)  # KM2
        spdu_1_state = spdu_1_state | ((int(self.data.get('104303', 0)) & 0x01) << 3)  # KM2
        spdu_1_state = spdu_1_state | ((int(self.data.get('104304', 0)) & 0x01) << 4)  # KM3
        spdu_1_state = spdu_1_state | ((int(self.data.get('104305', 0)) & 0x01) << 5)  # KM3
        spdu_1_state = spdu_1_state | ((int(self.data.get('104306', 0)) & 0x01) << 6)  # KM4
        spdu_1_state = spdu_1_state | ((int(self.data.get('104307', 0)) & 0x01) << 7)  # KM4
        spdu_1_state = spdu_1_state | ((int(self.data.get('104308', 0)) & 0x01) << 8)  # KM5
        spdu_1_state = spdu_1_state | ((int(self.data.get('104309', 0)) & 0x01) << 9)  # KM5
        spdu_1_state = spdu_1_state | ((int(self.data.get('104310', 0)) & 0x01) << 10)  # KM6
        spdu_1_state = spdu_1_state | ((int(self.data.get('104311', 0)) & 0x01) << 11)  # KM6
        spdu_1_state = spdu_1_state | ((int(self.data.get('104312', 0)) & 0x01) << 12)  # KM7
        spdu_1_state = spdu_1_state | ((int(self.data.get('104313', 0)) & 0x01) << 13)  # KM7
        self.pdu_msg.realtime_info.fpga_real.relay_state.append(spdu_1_state)  # 继电器1状态|||||

        spdu_2_state = int(self.data.get("104314", 0)) & 0x01
        spdu_2_state = spdu_2_state | ((int(self.data.get('104315', 0)) & 0x01) << 1)
        spdu_2_state = spdu_2_state | ((int(self.data.get('104316', 0)) & 0x01) << 2)
        spdu_2_state = spdu_2_state | ((int(self.data.get('104317', 0)) & 0x01) << 3)
        spdu_2_state = spdu_2_state | ((int(self.data.get('104318', 0)) & 0x01) << 4)
        spdu_2_state = spdu_2_state | ((int(self.data.get('104319', 0)) & 0x01) << 5)
        spdu_2_state = spdu_2_state | ((int(self.data.get('104320', 0)) & 0x01) << 6)
        spdu_2_state = spdu_2_state | ((int(self.data.get('104321', 0)) & 0x01) << 7)
        spdu_2_state = spdu_2_state | ((int(self.data.get('104322', 0)) & 0x01) << 8)
        spdu_2_state = spdu_2_state | ((int(self.data.get('104323', 0)) & 0x01) << 9)
        spdu_2_state = spdu_2_state | ((int(self.data.get('104324', 0)) & 0x01) << 10)
        spdu_2_state = spdu_2_state | ((int(self.data.get('104325', 0)) & 0x01) << 11)
        spdu_2_state = spdu_2_state | ((int(self.data.get('104326', 0)) & 0x01) << 12)
        spdu_2_state = spdu_2_state | ((int(self.data.get('104327', 0)) & 0x01) << 13)
        self.pdu_msg.realtime_info.fpga_real.relay_state.append(spdu_2_state)  # 继电器2状态|||||

        spdu_3_state = int(self.data.get("104328", 0)) & 0x01
        spdu_3_state = spdu_3_state | ((int(self.data.get('104329', 0)) & 0x01) << 1)
        spdu_3_state = spdu_3_state | ((int(self.data.get('104330', 0)) & 0x01) << 2)
        spdu_3_state = spdu_3_state | ((int(self.data.get('104331', 0)) & 0x01) << 3)
        spdu_3_state = spdu_3_state | ((int(self.data.get('104332', 0)) & 0x01) << 4)
        spdu_3_state = spdu_3_state | ((int(self.data.get('104333', 0)) & 0x01) << 5)
        spdu_3_state = spdu_3_state | ((int(self.data.get('104334', 0)) & 0x01) << 6)
        spdu_3_state = spdu_3_state | ((int(self.data.get('104335', 0)) & 0x01) << 7)
        spdu_3_state = spdu_3_state | ((int(self.data.get('104336', 0)) & 0x01) << 8)
        spdu_3_state = spdu_3_state | ((int(self.data.get('104337', 0)) & 0x01) << 9)
        spdu_3_state = spdu_3_state | ((int(self.data.get('104338', 0)) & 0x01) << 10)
        spdu_3_state = spdu_3_state | ((int(self.data.get('104339', 0)) & 0x01) << 11)
        spdu_3_state = spdu_3_state | ((int(self.data.get('104340', 0)) & 0x01) << 12)
        spdu_3_state = spdu_3_state | ((int(self.data.get('104341', 0)) & 0x01) << 13)
        self.pdu_msg.realtime_info.fpga_real.relay_state.append(spdu_3_state)  # 继电器3状态|||||

        spdu_4_state = int(self.data.get("104342", 0)) & 0x01
        spdu_4_state = spdu_4_state | ((int(self.data.get('104343', 0)) & 0x01) << 1)
        spdu_4_state = spdu_4_state | ((int(self.data.get('104344', 0)) & 0x01) << 2)
        spdu_4_state = spdu_4_state | ((int(self.data.get('104345', 0)) & 0x01) << 3)
        spdu_4_state = spdu_4_state | ((int(self.data.get('104346', 0)) & 0x01) << 4)
        spdu_4_state = spdu_4_state | ((int(self.data.get('104347', 0)) & 0x01) << 5)
        spdu_4_state = spdu_4_state | ((int(self.data.get('104348', 0)) & 0x01) << 6)
        spdu_4_state = spdu_4_state | ((int(self.data.get('104349', 0)) & 0x01) << 7)
        spdu_4_state = spdu_4_state | ((int(self.data.get('104350', 0)) & 0x01) << 8)
        spdu_4_state = spdu_4_state | ((int(self.data.get('104351', 0)) & 0x01) << 9)
        spdu_4_state = spdu_4_state | ((int(self.data.get('104352', 0)) & 0x01) << 10)
        spdu_4_state = spdu_4_state | ((int(self.data.get('104353', 0)) & 0x01) << 11)
        spdu_4_state = spdu_4_state | ((int(self.data.get('104354', 0)) & 0x01) << 12)
        spdu_4_state = spdu_4_state | ((int(self.data.get('104355', 0)) & 0x01) << 13)
        self.pdu_msg.realtime_info.fpga_real.relay_state.append(spdu_4_state)  # 继电器4状态|||||

        spdu_5_state = int(self.data.get("104356", 0)) & 0x01
        spdu_5_state = spdu_5_state | ((int(self.data.get('104357', 0)) & 0x01) << 1)
        spdu_5_state = spdu_5_state | ((int(self.data.get('104358', 0)) & 0x01) << 2)
        spdu_5_state = spdu_5_state | ((int(self.data.get('104359', 0)) & 0x01) << 3)
        spdu_5_state = spdu_5_state | ((int(self.data.get('104360', 0)) & 0x01) << 4)
        spdu_5_state = spdu_5_state | ((int(self.data.get('104361', 0)) & 0x01) << 5)
        spdu_5_state = spdu_5_state | ((int(self.data.get('104362', 0)) & 0x01) << 6)
        spdu_5_state = spdu_5_state | ((int(self.data.get('104363', 0)) & 0x01) << 7)
        spdu_5_state = spdu_5_state | ((int(self.data.get('104364', 0)) & 0x01) << 8)
        spdu_5_state = spdu_5_state | ((int(self.data.get('104365', 0)) & 0x01) << 9)
        spdu_5_state = spdu_5_state | ((int(self.data.get('104366', 0)) & 0x01) << 10)
        spdu_5_state = spdu_5_state | ((int(self.data.get('104367', 0)) & 0x01) << 11)
        spdu_5_state = spdu_5_state | ((int(self.data.get('104368', 0)) & 0x01) << 12)
        spdu_5_state = spdu_5_state | ((int(self.data.get('104369', 0)) & 0x01) << 13)
        self.pdu_msg.realtime_info.fpga_real.relay_state.append(spdu_5_state)  # 继电器5状态|||||

    def init_fpga_fault_code(self):
        self.init_fpga_fault_description1()
        self.init_fpga_fault_description2()
        self.init_fpga_fault_description3()
        self.init_fpga_fault_description4()
        self.init_fpga_fault_description5()
        self.init_fpga_fault_description6()
        self.init_fpga_fault_description7()
        self.init_fpga_fault_description8()
        fault_1 = 1 if self.pdu_msg.realtime_info.fpga_real.fault_description1 else 0
        fault_2 = 1 if self.pdu_msg.realtime_info.fpga_real.fault_description2 else 0
        fault_3 = 1 if self.pdu_msg.realtime_info.fpga_real.fault_description3[0] else 0
        fault_4 = 1 if self.pdu_msg.realtime_info.fpga_real.fault_description4[0] else 0
        fault_5 = 1 if self.pdu_msg.realtime_info.fpga_real.fault_description5[0] else 0
        fault_6 = 1 if self.pdu_msg.realtime_info.fpga_real.fault_description6[0] else 0
        fault_7 = 1 if self.pdu_msg.realtime_info.fpga_real.fault_description7 else 0
        fault_code = fault_1 | fault_2 << 1 | fault_3 << 2 | fault_4 << 3 | fault_5 << 4 | fault_6 << 5 | fault_7 << 6
        self.pdu_msg.realtime_info.fpga_real.fault_code = fault_code  # 故障码|||||

    def init_fpga_fault_description1(self):
        flag = False
        board_num = 0
        relay_1_num = 0
        relay_2_num = 0
        for i in range(1, 6):
            start = 718000 + 8 * (i - 1)
            for j in range(1, 7):
                oss_key = str(start + j - 1)
                if self.data.get(oss_key) == "1":
                    board_num = i * 2 if PduReplyMsg.fault_1[j][0] else i * 2 - 1
                    relay_1_num = PduReplyMsg.fault_1[j][1]
                    relay_2_num = PduReplyMsg.fault_1[j][2]
                    flag = True
                    break
            if flag:
                break
        fault = board_num << 16 | relay_1_num << 8 | relay_2_num
        self.pdu_msg.realtime_info.fpga_real.fault_description1 = fault  # 故障描述1|||||

    def init_fpga_fault_description2(self):
        flag = False
        board_num = 0
        relay_1_num = 0
        relay_2_num = 0
        for i in range(5):
            start = 718040 + 16 * i
            for j in range(15):
                oss_key = str(start + j)
                if self.data.get(oss_key) == "1":
                    board_num = j + 1
                    relay_1_num = PduReplyMsg.fault_2[j + 1][0]
                    relay_2_num = PduReplyMsg.fault_2[j + 1][1]
                    flag = True
                    break
            if flag:
                break
        fault = board_num << 16 | relay_1_num << 8 | relay_2_num
        self.pdu_msg.realtime_info.fpga_real.fault_description2 = fault  # 故障描述2|||||

    def init_fpga_fault_description3(self):
        # PDU-FPGA正极接触器粘连
        fault_byte1 = int(self.data.get('718120', 0)) & 0x01
        fault_byte1 = fault_byte1 | (int(self.data.get('718121', 0)) & 0x01) << 1
        fault_byte1 = fault_byte1 | (int(self.data.get('718122', 0)) & 0x01) << 2
        fault_byte1 = fault_byte1 | (int(self.data.get('718123', 0)) & 0x01) << 3
        fault_byte1 = fault_byte1 | (int(self.data.get('718124', 0)) & 0x01) << 4
        fault_byte1 = fault_byte1 | (int(self.data.get('718125', 0)) & 0x01) << 5
        fault_byte1 = fault_byte1 | (int(self.data.get('718126', 0)) & 0x01) << 6

        fault_byte1 = fault_byte1 | (int(self.data.get('718128', 0)) & 0x01) << 7
        fault_byte1 = fault_byte1 | (int(self.data.get('718129', 0)) & 0x01) << 8
        fault_byte1 = fault_byte1 | (int(self.data.get('718130', 0)) & 0x01) << 9
        fault_byte1 = fault_byte1 | (int(self.data.get('718131', 0)) & 0x01) << 10
        fault_byte1 = fault_byte1 | (int(self.data.get('718132', 0)) & 0x01) << 11
        fault_byte1 = fault_byte1 | (int(self.data.get('718133', 0)) & 0x01) << 12
        fault_byte1 = fault_byte1 | (int(self.data.get('718134', 0)) & 0x01) << 13

        fault_byte1 = fault_byte1 | (int(self.data.get('718136', 0)) & 0x01) << 14
        fault_byte1 = fault_byte1 | (int(self.data.get('718137', 0)) & 0x01) << 15
        fault_byte1 = fault_byte1 | (int(self.data.get('718138', 0)) & 0x01) << 16
        fault_byte1 = fault_byte1 | (int(self.data.get('718139', 0)) & 0x01) << 17
        fault_byte1 = fault_byte1 | (int(self.data.get('718140', 0)) & 0x01) << 18
        fault_byte1 = fault_byte1 | (int(self.data.get('718141', 0)) & 0x01) << 19
        fault_byte1 = fault_byte1 | (int(self.data.get('718142', 0)) & 0x01) << 20

        fault_byte1 = fault_byte1 | (int(self.data.get('718244', 0)) & 0x01) << 21
        fault_byte1 = fault_byte1 | (int(self.data.get('718245', 0)) & 0x01) << 22
        fault_byte1 = fault_byte1 | (int(self.data.get('718246', 0)) & 0x01) << 23

        fault_byte0 = int(self.data.get('718247', 0)) & 0x01
        fault_byte0 = fault_byte0 | (int(self.data.get('718248', 0)) & 0x01) << 1
        fault_byte0 = fault_byte0 | (int(self.data.get('718249', 0)) & 0x01) << 2
        fault_byte0 = fault_byte0 | (int(self.data.get('718250', 0)) & 0x01) << 3

        fault_byte0 = fault_byte0 | (int(self.data.get('718252', 0)) & 0x01) << 4
        fault_byte0 = fault_byte0 | (int(self.data.get('718253', 0)) & 0x01) << 5
        fault_byte0 = fault_byte0 | (int(self.data.get('718254', 0)) & 0x01) << 6
        fault_byte0 = fault_byte0 | (int(self.data.get('718255', 0)) & 0x01) << 7
        fault_byte0 = fault_byte0 | (int(self.data.get('718256', 0)) & 0x01) << 8
        fault_byte0 = fault_byte0 | (int(self.data.get('718257', 0)) & 0x01) << 9
        fault_byte0 = fault_byte0 | (int(self.data.get('718258', 0)) & 0x01) << 10

        count = 0
        for i in str(bin(fault_byte1))[2:]:
            if i == '1':
                count += 1
        for i in str(bin(fault_byte0))[2:]:
            if i == '1':
                count += 1
        fault_byte0 = fault_byte0 | ((count & 0xFF) << 16)

        self.pdu_msg.realtime_info.fpga_real.fault_description3.append(fault_byte0)  # 故障描述3|||||
        self.pdu_msg.realtime_info.fpga_real.fault_description3.append(fault_byte1)  # 故障描述3|||||

    def init_fpga_fault_description4(self):
        # PDU-FPGA负极接触器粘连
        fault_byte1 = int(self.data.get('718160', 0)) & 0x01
        fault_byte1 = fault_byte1 | (int(self.data.get('718161', 0)) & 0x01) << 1
        fault_byte1 = fault_byte1 | (int(self.data.get('718162', 0)) & 0x01) << 2
        fault_byte1 = fault_byte1 | (int(self.data.get('718163', 0)) & 0x01) << 3
        fault_byte1 = fault_byte1 | (int(self.data.get('718164', 0)) & 0x01) << 4
        fault_byte1 = fault_byte1 | (int(self.data.get('718165', 0)) & 0x01) << 5
        fault_byte1 = fault_byte1 | (int(self.data.get('718166', 0)) & 0x01) << 6

        fault_byte1 = fault_byte1 | (int(self.data.get('718168', 0)) & 0x01) << 7
        fault_byte1 = fault_byte1 | (int(self.data.get('718169', 0)) & 0x01) << 8
        fault_byte1 = fault_byte1 | (int(self.data.get('718170', 0)) & 0x01) << 9
        fault_byte1 = fault_byte1 | (int(self.data.get('718171', 0)) & 0x01) << 10
        fault_byte1 = fault_byte1 | (int(self.data.get('718172', 0)) & 0x01) << 11
        fault_byte1 = fault_byte1 | (int(self.data.get('718173', 0)) & 0x01) << 12
        fault_byte1 = fault_byte1 | (int(self.data.get('718174', 0)) & 0x01) << 13

        fault_byte1 = fault_byte1 | (int(self.data.get('718176', 0)) & 0x01) << 14
        fault_byte1 = fault_byte1 | (int(self.data.get('718177', 0)) & 0x01) << 15
        fault_byte1 = fault_byte1 | (int(self.data.get('718178', 0)) & 0x01) << 16
        fault_byte1 = fault_byte1 | (int(self.data.get('718179', 0)) & 0x01) << 17
        fault_byte1 = fault_byte1 | (int(self.data.get('718180', 0)) & 0x01) << 18
        fault_byte1 = fault_byte1 | (int(self.data.get('718181', 0)) & 0x01) << 19
        fault_byte1 = fault_byte1 | (int(self.data.get('718182', 0)) & 0x01) << 20

        fault_byte1 = fault_byte1 | (int(self.data.get('718284', 0)) & 0x01) << 21
        fault_byte1 = fault_byte1 | (int(self.data.get('718285', 0)) & 0x01) << 22
        fault_byte1 = fault_byte1 | (int(self.data.get('718286', 0)) & 0x01) << 23

        fault_byte0 = int(self.data.get('718287', 0)) & 0x01
        fault_byte0 = fault_byte0 | (int(self.data.get('718288', 0)) & 0x01) << 1
        fault_byte0 = fault_byte0 | (int(self.data.get('718289', 0)) & 0x01) << 2
        fault_byte0 = fault_byte0 | (int(self.data.get('718290', 0)) & 0x01) << 3

        fault_byte0 = fault_byte0 | (int(self.data.get('718292', 0)) & 0x01) << 4
        fault_byte0 = fault_byte0 | (int(self.data.get('718293', 0)) & 0x01) << 5
        fault_byte0 = fault_byte0 | (int(self.data.get('718294', 0)) & 0x01) << 6
        fault_byte0 = fault_byte0 | (int(self.data.get('718295', 0)) & 0x01) << 7
        fault_byte0 = fault_byte0 | (int(self.data.get('718296', 0)) & 0x01) << 8
        fault_byte0 = fault_byte0 | (int(self.data.get('718297', 0)) & 0x01) << 9
        fault_byte0 = fault_byte0 | (int(self.data.get('718298', 0)) & 0x01) << 10

        count = 0
        for i in str(bin(fault_byte1))[2:]:
            if i == '1':
                count += 1
        for i in str(bin(fault_byte0))[2:]:
            if i == '1':
                count += 1
        fault_byte0 = fault_byte0 | ((count & 0xFF) << 16)

        self.pdu_msg.realtime_info.fpga_real.fault_description4.append(fault_byte0)  # 故障描述4|||||
        self.pdu_msg.realtime_info.fpga_real.fault_description4.append(fault_byte1)  # 故障描述4|||||

    def init_fpga_fault_description5(self):
        # PDU-FPGA正极接触器拒动
        fault_byte1 = int(self.data.get('718200', 0)) & 0x01
        fault_byte1 = fault_byte1 | (int(self.data.get('718201', 0)) & 0x01) << 1
        fault_byte1 = fault_byte1 | (int(self.data.get('718202', 0)) & 0x01) << 2
        fault_byte1 = fault_byte1 | (int(self.data.get('718203', 0)) & 0x01) << 3
        fault_byte1 = fault_byte1 | (int(self.data.get('718204', 0)) & 0x01) << 4
        fault_byte1 = fault_byte1 | (int(self.data.get('718205', 0)) & 0x01) << 5
        fault_byte1 = fault_byte1 | (int(self.data.get('718206', 0)) & 0x01) << 6

        fault_byte1 = fault_byte1 | (int(self.data.get('718208', 0)) & 0x01) << 7
        fault_byte1 = fault_byte1 | (int(self.data.get('718209', 0)) & 0x01) << 8
        fault_byte1 = fault_byte1 | (int(self.data.get('718210', 0)) & 0x01) << 9
        fault_byte1 = fault_byte1 | (int(self.data.get('718211', 0)) & 0x01) << 10
        fault_byte1 = fault_byte1 | (int(self.data.get('718212', 0)) & 0x01) << 11
        fault_byte1 = fault_byte1 | (int(self.data.get('718213', 0)) & 0x01) << 12
        fault_byte1 = fault_byte1 | (int(self.data.get('718214', 0)) & 0x01) << 13

        fault_byte1 = fault_byte1 | (int(self.data.get('718216', 0)) & 0x01) << 14
        fault_byte1 = fault_byte1 | (int(self.data.get('718217', 0)) & 0x01) << 15
        fault_byte1 = fault_byte1 | (int(self.data.get('718218', 0)) & 0x01) << 16
        fault_byte1 = fault_byte1 | (int(self.data.get('718219', 0)) & 0x01) << 17
        fault_byte1 = fault_byte1 | (int(self.data.get('718220', 0)) & 0x01) << 18
        fault_byte1 = fault_byte1 | (int(self.data.get('718221', 0)) & 0x01) << 19
        fault_byte1 = fault_byte1 | (int(self.data.get('718222', 0)) & 0x01) << 20

        fault_byte1 = fault_byte1 | (int(self.data.get('718224', 0)) & 0x01) << 21
        fault_byte1 = fault_byte1 | (int(self.data.get('718225', 0)) & 0x01) << 22
        fault_byte1 = fault_byte1 | (int(self.data.get('718226', 0)) & 0x01) << 23

        fault_byte0 = int(self.data.get('718227', 0)) & 0x01
        fault_byte0 = fault_byte0 | (int(self.data.get('718228', 0)) & 0x01) << 1
        fault_byte0 = fault_byte0 | (int(self.data.get('718229', 0)) & 0x01) << 2
        fault_byte0 = fault_byte0 | (int(self.data.get('718230', 0)) & 0x01) << 3

        fault_byte0 = fault_byte0 | (int(self.data.get('718232', 0)) & 0x01) << 4
        fault_byte0 = fault_byte0 | (int(self.data.get('718233', 0)) & 0x01) << 5
        fault_byte0 = fault_byte0 | (int(self.data.get('718234', 0)) & 0x01) << 6
        fault_byte0 = fault_byte0 | (int(self.data.get('718235', 0)) & 0x01) << 7
        fault_byte0 = fault_byte0 | (int(self.data.get('718236', 0)) & 0x01) << 8
        fault_byte0 = fault_byte0 | (int(self.data.get('718237', 0)) & 0x01) << 9
        fault_byte0 = fault_byte0 | (int(self.data.get('718238', 0)) & 0x01) << 10

        count = 0
        for i in str(bin(fault_byte1))[2:]:
            if i == '1':
                count += 1
        for i in str(bin(fault_byte0))[2:]:
            if i == '1':
                count += 1
        fault_byte0 = fault_byte0 | ((count & 0xFF) << 16)

        self.pdu_msg.realtime_info.fpga_real.fault_description5.append(fault_byte0)  # 故障描述5|||||
        self.pdu_msg.realtime_info.fpga_real.fault_description5.append(fault_byte1)  # 故障描述5|||||

    def init_fpga_fault_description6(self):
        # PDU-FPGA负极接触器拒动
        fault_byte1 = int(self.data.get('718240', 0)) & 0x01
        fault_byte1 = fault_byte1 | (int(self.data.get('718241', 0)) & 0x01) << 1
        fault_byte1 = fault_byte1 | (int(self.data.get('718242', 0)) & 0x01) << 2
        fault_byte1 = fault_byte1 | (int(self.data.get('718243', 0)) & 0x01) << 3
        fault_byte1 = fault_byte1 | (int(self.data.get('718244', 0)) & 0x01) << 4
        fault_byte1 = fault_byte1 | (int(self.data.get('718245', 0)) & 0x01) << 5
        fault_byte1 = fault_byte1 | (int(self.data.get('718246', 0)) & 0x01) << 6

        fault_byte1 = fault_byte1 | (int(self.data.get('718248', 0)) & 0x01) << 7
        fault_byte1 = fault_byte1 | (int(self.data.get('718249', 0)) & 0x01) << 8
        fault_byte1 = fault_byte1 | (int(self.data.get('718250', 0)) & 0x01) << 9
        fault_byte1 = fault_byte1 | (int(self.data.get('718251', 0)) & 0x01) << 10
        fault_byte1 = fault_byte1 | (int(self.data.get('718252', 0)) & 0x01) << 11
        fault_byte1 = fault_byte1 | (int(self.data.get('718253', 0)) & 0x01) << 12
        fault_byte1 = fault_byte1 | (int(self.data.get('718254', 0)) & 0x01) << 13

        fault_byte1 = fault_byte1 | (int(self.data.get('718256', 0)) & 0x01) << 14
        fault_byte1 = fault_byte1 | (int(self.data.get('718257', 0)) & 0x01) << 15
        fault_byte1 = fault_byte1 | (int(self.data.get('718258', 0)) & 0x01) << 16
        fault_byte1 = fault_byte1 | (int(self.data.get('718259', 0)) & 0x01) << 17
        fault_byte1 = fault_byte1 | (int(self.data.get('718260', 0)) & 0x01) << 18
        fault_byte1 = fault_byte1 | (int(self.data.get('718261', 0)) & 0x01) << 19
        fault_byte1 = fault_byte1 | (int(self.data.get('718262', 0)) & 0x01) << 20

        fault_byte1 = fault_byte1 | (int(self.data.get('718264', 0)) & 0x01) << 21
        fault_byte1 = fault_byte1 | (int(self.data.get('718265', 0)) & 0x01) << 22
        fault_byte1 = fault_byte1 | (int(self.data.get('718266', 0)) & 0x01) << 23

        fault_byte0 = int(self.data.get('718267', 0)) & 0x01
        fault_byte0 = fault_byte0 | (int(self.data.get('718268', 0)) & 0x01) << 1
        fault_byte0 = fault_byte0 | (int(self.data.get('718269', 0)) & 0x01) << 2
        fault_byte0 = fault_byte0 | (int(self.data.get('718270', 0)) & 0x01) << 3

        fault_byte0 = fault_byte0 | (int(self.data.get('718272', 0)) & 0x01) << 4
        fault_byte0 = fault_byte0 | (int(self.data.get('718273', 0)) & 0x01) << 5
        fault_byte0 = fault_byte0 | (int(self.data.get('718274', 0)) & 0x01) << 6
        fault_byte0 = fault_byte0 | (int(self.data.get('718275', 0)) & 0x01) << 7
        fault_byte0 = fault_byte0 | (int(self.data.get('718276', 0)) & 0x01) << 8
        fault_byte0 = fault_byte0 | (int(self.data.get('718277', 0)) & 0x01) << 9
        fault_byte0 = fault_byte0 | (int(self.data.get('718278', 0)) & 0x01) << 10

        count = 0
        for i in str(bin(fault_byte1))[2:]:
            if i == '1':
                count += 1
        for i in str(bin(fault_byte0))[2:]:
            if i == '1':
                count += 1
        fault_byte0 = fault_byte0 | ((count & 0xFF) << 16)

        self.pdu_msg.realtime_info.fpga_real.fault_description6.append(fault_byte0)  # 故障描述6|||||
        self.pdu_msg.realtime_info.fpga_real.fault_description6.append(fault_byte1)  # 故障描述6|||||

    def init_fpga_fault_description7(self):
        # 各bit0~bit4依次表示PDU子板1~子板5的接线情况，如为0表示子板连接正常，如为1表示子板连接故障（可能没有插好）
        fault = int(self.data.get('718280', 0)) & 0x01
        fault = fault | (int(self.data.get('718281', 0)) & 0x01) << 1
        fault = fault | (int(self.data.get('718282', 0)) & 0x01) << 2
        fault = fault | (int(self.data.get('718283', 0)) & 0x01) << 3
        fault = fault | (int(self.data.get('718284', 0)) & 0x01) << 4
        self.pdu_msg.realtime_info.fpga_real.fault_description7 = fault  # 故障描述7|||||

    def init_fpga_fault_description8(self):
        self.pdu_msg.realtime_info.fpga_real.fault_description8 = 0  # 故障描述8|||||

    def init_fpga_version_info(self):
        self.pdu_msg.realtime_info.fpga_real.fpga_version.append(0)  # FPGA版本|||||

    def init_fpga_pdu_fault_info(self):
        self.pdu_msg.realtime_info.fpga_real.pdu_fault = 0  # PDU故障|||||
