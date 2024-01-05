# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/8/1 17:40
# @File:tools.py
import errno
import os
import platform
import socket
import subprocess
import time

import psutil
import serial.tools.list_ports
import yaml

from utils.constant import SERIAL_NODE
from utils.log import log
from aec.aec_msg import aec_ip

"""
    具体操作：
        1、 netstat -tln 查看本机的网络连接列表,找到你所开启服务占用的端口,例如8080
        2、找到端口对应的进程，就是PID: lsof -i:8080 PID为9808
        3、使用kill -9 9808即可释放改端口
        4、netstat -tln 查看是否释放即可
"""


def deal_recv_data(data, rec):
    if isinstance(data, dict):
        for name, val in data.items():
            if isinstance(val, dict):
                deal_recv_data(val, rec)
            else:
                rec[name] = val
    return rec


def net_is_used(port, ip=aec_ip):
    """
    创建一个socket服务并连接到对应的ip:port。如果能连接，则端口被占用；如果端口可用，则无法连接
    :param port:
    :param ip:
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        s.shutdown(2)
        return True
    except:
        return False


def reset_liquid_ip_config(ip, port="", module=""):
    can_enter_path = f"lsof -i:{port}"


def check_can_init_setting(can_name, bitrate):
    """

    :param can_name:
    :param bitrate:
    :return:
    """
    try:
        os.system(f"echo 4096 > /sys/class/net/{can_name}/tx_queue_len")
        time.sleep(1)
        os.system(f"ifconfig {can_name} down")
        time.sleep(1)
        os.system(f"ip link set {can_name} up type can bitrate {bitrate}")
        time.sleep(1)
        os.system(f"ifconfig {can_name} up")
        time.sleep(1)
        return True
    except Exception as e:
        return False


def check_redis_pid_exists():
    """
        Check whether pid exists in the current process table. UNIX only.
    :return:
    """
    pids = psutil.pids()
    for pi in pids:
        if "redis-server" in psutil.Process(pi).name():
            print(f"<AI>:redis-server has already started:{psutil.Process(pi).name()}, pid:{pi}")
            pid = pi
            break
    else:
        p = subprocess.Popen("redis-server", shell=True, stdout=subprocess.PIPE)
        print(f"<AI>:start redis-server, pid:{p.pid}")
        pid = p.pid
    if "Linux" in platform.system():
        if pid < 0:
            return False
        if pid == 0:
            # According to "man 2 kill" PID 0 refers to every process
            # in the process group of the calling process.
            # On certain systems 0 is a valid PID but we have no way
            # to know that in a portable fashion.
            raise ValueError('invalid PID 0')
        try:
            os.kill(pid, 0)
        except OSError as err:
            if err.errno == errno.ESRCH:
                # ESRCH == No such process
                return False
            elif err.errno == errno.EPERM:
                # EPERM clearly means there's a process to deny access to
                return True
            else:
                # According to "man 2 kill" possible error values are
                # (EINVAL, EPERM, ESRCH)
                raise
        else:
            return True


def check_ip_address_available(ip, port="", module=""):
    """

    :param ip:
    :param port:
    :param module:
    :return:
    """
    ip_address = psutil.net_if_addrs()
    try:
        for eth_name, eth_info in ip_address.items():
            if "eth" in eth_name:
                for address in eth_info:
                    if address.family.name == 'AF_INET' and address.address == ip:
                        return True
    except Exception as e:
        log.error(f"<{module}>:when check {ip} happen error ,please check hard env...")
    return False


def check_serial_port_available(port, module=""):
    """
        通过串口数据判断meter和sensor 所使用的串口

        pcu 串口0：
                [19:13:12.643] 01 03 00 00 00 72 C5 EF
                [19:13:13.266] 02 03 00 00 00 72 C5 DC
                [19:13:13.793] 03 03 00 00 00 72 C4 0D
                [19:13:14.418] 04 03 00 00 00 72 C5 BA
        PCU 串口1：01 03 00 01 00 04 15 C9

    :param module:
    :return:
    """
    port_list = list(serial.tools.list_ports.comports())
    for port in port_list:
        if "ttyUSB" in port.name and f"/dev/{port.name}" == SERIAL_NODE.get(module.lower()):
            return True
    # if not SERIAL_NODE.get(module.lower()):
    #     port_list = list(serial.tools.list_ports.comports())
    #     for port in port_list:
    #         if "ttyUSB" in port.name and f"/dev/{port.name}" not in SERIAL_NODE.values():
    #             ser = None
    #             try:
    #                 ser = serial.Serial(f"/dev/{port.name}", 9600, timeout=0.5)
    #                 ser.flushInput()  # 清空缓冲区
    #                 while True:
    #                     count = ser.inWaiting()
    #                     if count != 0:
    #                         recv = ser.read(8)
    #                         log.info(f"<tools>:{port.name}, recv data:{[hex(d) for d in recv]}")
    #                         if len(recv) > 4 and recv[1] == 3 and recv[5] == 0x04:
    #                             # 温湿度 01 03 00 01 00 04 15 C9
    #                             SERIAL_NODE["sensor"] = f"/dev/{port.name}"
    #                         elif len(recv) > 1 and recv[1] == 17:
    #                             # 电表 01 11 FE DC BA 98 76 54 32 10 06 E5 未连接时查询的数据
    #                             # 连接上时，查询的数据，用于连接后立刻重新连接的场景
    #                             SERIAL_NODE["meter"] = f"/dev/{port.name}"
    #                         elif len(recv) > 4 and recv[1] == 3 and recv[5] == 0x04:  # PCU 温湿度
    #                             SERIAL_NODE["pcu_sensor"] = f"/dev/{port.name}"  # 连接pcu的串口1 tx接A rx接B
    #                             # 温湿度 01 03 00 01 00 04 15 C9
    #                         elif len(recv) > 4 and recv[1] == 3 and recv[5] == 0x72:
    #                             # b'\x04\x03\x00\x00\x00r\xc5\xba'
    #                             # b'\x01\x03\x00\x00\x00r\xc5\xef'
    #                             # b'\x02\x03\x00\x00\x00r\xc5\xdc'
    #                             # b'\x03\x03\x00\x00\x00r\xc4\r'
    #                             # b'\x04\x03\x00\x00\x00r\xc5\xba'
    #                             # b'\x01\x03\x00\x00\x00r\xc5\xef'
    #                             # b'\x02\x03\x00\x00\x00r\xc5\xdc'
    #                             # b'\x03\x03\x00\x00\x00r\xc4\r'
    #                             # b'\x04\x03\x00\x00\x00r\xc5\xba'
    #                             SERIAL_NODE["pcu_meter"] = f"/dev/{port.name}"  # PCU 电表
    #                         break
    #                 ser.close()  # 关闭串口
    #             except Exception as e:
    #                 _, exc_value, _ = sys.exc_info()
    #                 if ser and ser.is_open:
    #                     ser.close()
    #     log.info(f"<tools>:tools 在{module}模块函数中获取的串口为:{SERIAL_NODE}")


def save_dict_to_yaml(dict_value: dict, save_path: str):
    """
    dict保存为yaml
    :param dict_value:
    :param save_path:
    :return:
    """
    if not os.path.exists(os.path.dirname(save_path)):
        os.makedirs(os.path.dirname(save_path))
    with open(save_path, 'w') as file:
        file.write(yaml.dump(dict_value, allow_unicode=True))


def read_yaml_to_dict(yaml_path: str, ):
    """

    :param yaml_path:
    :return:
    """
    with open(yaml_path, encoding='utf-8') as file:
        dict_value = yaml.load(file.read(), Loader=yaml.FullLoader)
        return dict_value


if __name__ == '__main__':
    ip_address = psutil.net_if_addrs()
    for eth_name, eth_info in ip_address.items():
        print(eth_name)
        for i in eth_info:
            print(type(i))
            print(i.address)
