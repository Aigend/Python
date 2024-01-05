# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/7/21 14:06
# @File:bms_can.py
import sys
import time
import traceback

import can

from utils.log import log

ccs_query_type = 0
response_frameNO = 0
send_mul_frame_flag = 0
send_all_frame_flag = 0
flag = False


def send_data(bus, id, data, extended_id, **kwargs):
    """

    :param bus:
    :param id:
    :param data:
    :param extended_id:
    :return:
    """
    try:
        msg = can.Message(arbitration_id=id, data=data, is_extended_id=extended_id)
        bus.send(msg)
        time.sleep(0.05)  # 调试发现这里不加时间间隔会导致 CanError:Transmit buffer full报错
    except can.CanError as e:
        _, exc_value, _ = sys.exc_info()
        log.error(f"<BMS>:{bus.channel},{kwargs.get('branch')} : BMS Message NOT sent, happen error: {str(exc_value)}")
        log.error(f"<BMS>:{bus.channel},{kwargs.get('branch')} id:{str(hex(id))}, data:{str([hex(d) for d in data])}")
        traceback.print_exc()
        time.sleep(1)


def can_recv(bus, boardx, **kwargs):
    """

    :param bus:
    :param boardx:
    :return:
    """
    global ccs_query_type, response_frameNO, send_mul_frame_flag, send_all_frame_flag, flag
    try:
        msg = bus.recv(100)
        if msg and msg.arbitration_id == 0x60C:
            # log.info(f"<BMS>:recive CDC {[hex(i) for i in msg.data]}")
            if (msg.data[2] == 0x01) & (msg.data[3] == 0x67):
                # and ccs_query_type != 1
                # log.debug(f"{hex(msg.arbitration_id), hex(msg.data[2]), hex(msg.data[3])}")
                # 查询电池id，130-132
                data = [0x10, 0x23, 0x62, 0x01, 0x67, boardx[130], boardx[131], boardx[132]]
                send_data(bus, 0x68C, data, False, lock=kwargs.get("lock"))
                log.info(f"{bus.channel},{kwargs.get('branch')}=====电池ID data frame1=====:{[hex(i) for i in data]}")
                msg.arbitration_id = 0
                msg.data = [0, 0, 0, 0, 0, 0, 0, 0]
                response_frameNO = 2
                ccs_query_type = 1

            elif (msg.data[2] == 0x01) & (msg.data[3] == 0x65):
                # and ccs_query_type != 2
                # log.debug(f"{hex(msg.arbitration_id), hex(msg.data[2]), hex(msg.data[3])}")
                # 查询国标id，163-165
                data = [0x10, 0x1B, 0x62, 0x01, 0x65, boardx[163], boardx[164], boardx[165]]
                send_data(bus, 0x68C, data, False, lock=kwargs.get("lock"))
                log.info(
                    f"{bus.channel},{kwargs.get('branch')}=====电池国标ID data frame1=====:{[hex(i) for i in data]}")
                msg.arbitration_id = 0
                msg.data = [0, 0, 0, 0, 0, 0, 0, 0]
                response_frameNO = 2
                ccs_query_type = 2

            elif (msg.data[2] == 0xf1) & (msg.data[3] == 0x18):
                # and ccs_query_type != 3
                # log.debug(f"{hex(msg.arbitration_id), hex(msg.data[2]), hex(msg.data[3])}")
                # 发送软件版本，196-198
                data = [0x10, 0x0E, 0x62, 0xf1, 0x18, boardx[196], boardx[197], boardx[198]]
                send_data(bus, 0x68C, data, False, lock=kwargs.get("lock"))
                log.info(f"{bus.channel},{kwargs.get('branch')}=====软件版本 data frame1=====:{[hex(i) for i in data]}")
                msg.arbitration_id = 0
                msg.data = [0, 0, 0, 0, 0, 0, 0, 0]
                response_frameNO = 2
                ccs_query_type = 3

            elif (msg.data[2] == 0xf1) & (msg.data[3] == 0x10):
                # and ccs_query_type != 4
                # log.debug(f"{hex(msg.arbitration_id), hex(msg.data[2]), hex(msg.data[3])}")
                # 查询硬件版本
                data = [0x10, 0x0E, 0x62, 0xf1, 0x10, boardx[213], boardx[214], boardx[215]]
                send_data(bus, 0x68C, data, False, lock=kwargs.get("lock"))
                log.info(f"{bus.channel},{kwargs.get('branch')}=====硬件版本 data frame1=====:{[hex(i) for i in data]}")
                msg.arbitration_id = 0
                msg.data = [0, 0, 0, 0, 0, 0, 0, 0]
                response_frameNO = 2
                ccs_query_type = 4

            # elif (msg.data[2] == 0xf1) & (msg.data[3] == 0x01):
            #     data = [0x10, 0x0E, 0x62, 0xf1, 0x01, boardx[213], boardx[214], boardx[215]]
            #     send_data(bus, 0x68C, data, False, lock=kwargs.get("lock"))
            #     log.info(f"{bus.channel},{kwargs.get('branch')}=====硬件版本 data frame1=====:{[hex(i) for i in data]}")
            #     msg.arbitration_id = 0
            #     msg.data = [0, 0, 0, 0, 0, 0, 0, 0]
            #     response_frameNO = 2
            #     ccs_query_type = 4

            elif (msg.data[0] == 0x30) & (msg.data[1] == 0x00):
                # 发送多帧信息
                send_mul_frame_flag = 1
                msg.arbitration_id = 0
                msg.data = [0, 0, 0, 0, 0, 0, 0, 0]
                can_send_data = [0 for _ in range(0, 8)]
                if (ccs_query_type == 1) & (send_mul_frame_flag == 1):
                    while ccs_query_type == 1:  # 电池ID
                        if response_frameNO == 2:
                            can_send_data[0] = 0x21
                        elif response_frameNO == 3:
                            can_send_data[0] = 0x22
                        elif response_frameNO == 4:
                            can_send_data[0] = 0x23
                        elif response_frameNO == 5:
                            can_send_data[0] = 0x24
                        elif response_frameNO == 6:
                            can_send_data[0] = 0x25
                            can_send_data[1] = 0x00
                            for i_num in range(2, 8):
                                can_send_data[i_num] = 0xAA
                            send_data(bus, 0x68C, can_send_data, False, lock=kwargs.get("lock"))
                            log.info(
                                f"{bus.channel},{kwargs.get('branch')}=====电池ID data frame{response_frameNO}=====:{[hex(i) for i in can_send_data]}")
                            ccs_query_type = 0
                            response_frameNO = 0
                            send_mul_frame_flag = 0
                            send_all_frame_flag += 1
                            break
                        if response_frameNO != 0:
                            dataNO = 133 + (response_frameNO - 2) * 7
                            for i_num in range(1, 8):
                                can_send_data[i_num] = boardx[dataNO]
                                dataNO = dataNO + 1
                            send_data(bus, 0x68C, can_send_data, False, lock=kwargs.get("lock"))
                            log.info(
                                f"{bus.channel},{kwargs.get('branch')}=====电池ID data frame{response_frameNO}=====:{[hex(i) for i in can_send_data]}")
                            response_frameNO = response_frameNO + 1
                elif (ccs_query_type == 2) & (send_mul_frame_flag == 1):
                    while (ccs_query_type == 2) & (send_mul_frame_flag == 1):  # 电池国标ID
                        if response_frameNO == 2:
                            can_send_data[0] = 0x21
                        elif response_frameNO == 3:
                            can_send_data[0] = 0x22
                        elif response_frameNO == 4:
                            can_send_data[0] = 0x23
                            dataNO = 180
                            for i_num in range(1, 8):
                                can_send_data[i_num] = boardx[dataNO]
                                dataNO = dataNO + 1
                            send_data(bus, 0x68C, can_send_data, False, lock=kwargs.get("lock"))
                            log.info(
                                f"{bus.channel},{kwargs.get('branch')}=====电池国标ID data frame{response_frameNO}=====:{[hex(i) for i in can_send_data]}")
                            ccs_query_type = 0
                            response_frameNO = 0
                            send_mul_frame_flag = 0
                            send_all_frame_flag += 1
                            break
                        if response_frameNO != 0:
                            dataNO = 166 + (response_frameNO - 2) * 7
                            for i_num in range(1, 8):
                                can_send_data[i_num] = boardx[dataNO]
                                dataNO = dataNO + 1
                            send_data(bus, 0x68C, can_send_data, False, lock=kwargs.get("lock"))
                            log.info(
                                f"{bus.channel},{kwargs.get('branch')}=====电池国标ID data frame{response_frameNO}=====:{[hex(i) for i in can_send_data]}")
                            response_frameNO = response_frameNO + 1
                elif (ccs_query_type == 3) & (send_mul_frame_flag == 1):
                    while (ccs_query_type == 3) & (send_mul_frame_flag == 1):  # 软件版本
                        if response_frameNO == 2:
                            can_send_data[0] = 0x21
                        elif response_frameNO == 3:
                            can_send_data[0] = 0x22
                            can_send_data[1] = boardx[206]
                            for i_num in range(2, 8):
                                can_send_data[i_num] = 0xAA
                            send_data(bus, 0x68C, can_send_data, False, lock=kwargs.get("lock"))
                            log.info(
                                f"{bus.channel},{kwargs.get('branch')}=====软件版本 data frame3=====:{[hex(i) for i in can_send_data]}")
                            ccs_query_type = 0
                            response_frameNO = 0
                            send_mul_frame_flag = 0
                            send_all_frame_flag += 1
                            break
                        if response_frameNO != 0:
                            dataNO = 199 + (response_frameNO - 2) * 7
                            for i_num in range(1, 8):
                                can_send_data[i_num] = boardx[dataNO]
                                dataNO = dataNO + 1
                            send_data(bus, 0x68C, can_send_data, False, lock=kwargs.get("lock"))
                            log.info(
                                f"{bus.channel},{kwargs.get('branch')}=====软件版本 data frame2=====:{[hex(i) for i in can_send_data]}")
                            response_frameNO = response_frameNO + 1
                elif (ccs_query_type == 4) & (send_mul_frame_flag == 1):
                    while (ccs_query_type == 4) & (send_mul_frame_flag == 1):  # 硬件版本
                        if response_frameNO == 2:
                            can_send_data[0] = 0x21
                        elif response_frameNO == 3:
                            can_send_data[0] = 0x22
                            can_send_data[1] = boardx[223]
                            for i_num in range(2, 8):
                                can_send_data[i_num] = 0xAA
                            send_data(bus, 0x68C, can_send_data, False, lock=kwargs.get("lock"))
                            log.info(
                                f"{bus.channel},{kwargs.get('branch')}=====硬件版本 data frame3=====:{[hex(i) for i in can_send_data]}")
                            ccs_query_type = 0
                            response_frameNO = 0
                            send_mul_frame_flag = 0
                            send_all_frame_flag += 1
                            break
                        if response_frameNO != 0:
                            dataNO = 216 + (response_frameNO - 2) * 7
                            for i_num in range(1, 8):
                                can_send_data[i_num] = boardx[dataNO]
                                dataNO = dataNO + 1
                            send_data(bus, 0x68C, can_send_data, False, lock=kwargs.get("lock"))
                            log.info(
                                f"{bus.channel},{kwargs.get('branch')}=====硬件版本 data frame2=====:{[hex(i) for i in can_send_data]}")
                            response_frameNO = response_frameNO + 1
        if msg and msg.arbitration_id == 0x50:
            vcu_hv_contactor_request = (msg.data[0] >> 3) & 0x3
            bms_contactor_states = boardx[0] & 0x3
            if vcu_hv_contactor_request == 2:
                if bms_contactor_states != 1:
                    boardx[0] = (boardx[0] & 0xF8) | 0x1
                    log.warning(f"<BMS>: update {kwargs.get('branch')} bms_contactor_states: 1")
            elif vcu_hv_contactor_request == 1:
                if bms_contactor_states != 3:
                    boardx[0] = (boardx[0] & 0xF8) | 0x3
                    log.warning(f"<BMS>: update {kwargs.get('branch')} bms_contactor_states: 3")

    except can.CanError:
        _, exc_value, _ = sys.exc_info()
        log.error(f"<BMS>:{bus.channel},{kwargs.get('branch')} : BMS Recv Message happen error: {str(exc_value)}")
        time.sleep(1)
