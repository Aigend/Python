# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/9/10 16:03
# @File:matrix_tools.py
import json
import logging
import os
import re
import socket
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from logging.handlers import RotatingFileHandler
from multiprocessing import Process
from multiprocessing import Queue
from urllib.parse import urlparse


class _Logger:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(_Logger, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, path=os.path.join(os.getcwd(), "matrix_log")):
        if not os.path.exists(path):
            os.makedirs(path)
        if os.path.exists(os.path.join(path, "all.log")):
            try:
                os.remove(os.path.join(path, "all.log"))
            except Exception:
                pass
        if not hasattr(self, "logger"):
            self.logger = logging.getLogger(path)
            self.logger.setLevel(logging.DEBUG)
            fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(filename)s] [line:%(lineno)d] %(message)s',
                                    '%Y-%m-%d %H:%M:%S')
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(fmt)
            console_handler.setLevel(logging.DEBUG)
            file_handler = RotatingFileHandler(filename=os.path.join(path, "all.log"), mode="a",
                                               maxBytes=1024 * 1024 * 1024, backupCount=1, encoding='utf-8')
            file_handler.setFormatter(fmt)
            file_handler.setLevel(logging.INFO)
            if not self.logger.handlers:
                self.logger.addHandler(console_handler)
                self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger


log = _Logger().get_logger()


class HTTPRequestHandler(BaseHTTPRequestHandler):
    response_init = {
        "dtc": {
            "request": {
                "operation": 1
            },
            "response": {
                "result_code": "0",
                "message": "test",
                "dtc": "p00120"
            }
        },
        "reflash": {
            "request": {
                "BMS version": "/home/zoo/Desktop/P0208587 CF.zip",
                "SPM version": 0,
                "operation": 2
            },
            "response": {
                "result_code": "0",
                "message": "test"
            }
        },
        "progress": {
            "response": {
                "result_code": "0",
                "progress": "0 %",  # 这里调试发现需要有空格，否则主控无法识别
                "status": "running"
            }
        },
        "bms_version": {
            "request": {
                "operation": 4
            },
            "response": {
                "result_code": "0",
                "message": "test",
                "version": "P0208587 CG"
            }
        },
        "matrix_version": {
            "request": {
                "operation": 5
            },
            "response": {
                "result_code": "0",
                "message": "test",
                "version": "MX.AA.20.02"
            }
        },
        "close_refresh": {
            "request": {
                "operation": 3
            },
            "response": {
                "result_code": "0",
                "message": "test"
            }
        },
        "ddl_command": {
            "request": {
                "operation": 6,
                "ddl": "doip_reset_gateway"
            },
            "response": {
                "result_code": "0",
                "message": "test",
                "ddl_output": "json_string"
            }
        },
        "ddl_self_define": {
            "request": {
                "operation": 7,
                "ddl": "path_on_ps.xml"
            },
            "response": {
                "result_code": "0",
                "message": "test",
                "ddl_output": "json_string"
            }
        }
    }
    queue = Queue()
    operator_map = {
        "1": "dtc",  # 获取DTC 数据
        "2": "reflash",  # 刷写
        "3": "close_refresh",  # 关闭
        "4": "bms_version",  # 获取BMS版本号
        "5": "matrix_version",  # 获取Matrix版本号
        "6": "ddl_command",  # 执行预置组合命令
        "7": "ddl_self_define",  # 执行自定义组合命令
    }

    def update_body_data(self):
        def deal_post_data(data, response_init):
            if isinstance(data, dict):
                for k, val in data.items():
                    if k in response_init and isinstance(val, dict):
                        deal_post_data(val, response_init[k])
                    elif k in response_init and response_init[k].__class__ == int:
                        if isinstance(val, int):
                            response_init[k] = val
                        elif isinstance(val, str) and val.isnumeric():
                            response_init[k] = int(val)
                    elif k in response_init and response_init[k].__class__ == str:
                        response_init[k] = str(val)
                    else:
                        log.warning(f"<Matrix> {k} not given value")

        data = {}
        while not HTTPRequestHandler.queue.empty():
            data = HTTPRequestHandler.queue.get()
        deal_post_data(data, HTTPRequestHandler.response_init)

    def do_GET(self):
        """
        处理 get 请求, 获取升级进度
        :return:
        """
        parsed_result = urlparse(self.path)
        path = parsed_result.path
        # query = parse_qs(parsed_result.query)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        status = {
            "result_code": 0,
        }
        log.info(f"<UM><GET>:UM Get income path:{path}")
        if path == '/bd2/bms_flash':  # 获取升级进度
            self.update_body_data()
            status = HTTPRequestHandler.response_init.get("progress").get("response")
            log.info(f"<UM><GET><{path}><Response>:{status}")
        elif path == "/update/matrix/data":
            pass
            # log.info(f"<UM><GET><{path}>:{HTTPRequestHandler.body_data}")
        elif re.match("/bd2/bms_flash/set/bus/can\d+", path):
            # log.info(f"<UM><GET><{path}>:{HTTPRequestHandler.body_data}")
            self.update_body_data()
        response.write(json.dumps(status).encode(encoding='utf-8'))
        self.wfile.write(response.getvalue())

    def do_POST(self):
        """
        处理post 请求
        :return:
        """
        log.info("<UM>UM post income...")
        parsed_result = urlparse(self.path)
        path = parsed_result.path
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = BytesIO()
        status = {
            "result_code": "0",
            "message": "",
        }
        if path == '/bd2/bms_flash':
            content_len = int(self.headers.get('Content-Length', 0))
            post_body = json.loads(self.rfile.read(content_len))
            log.info(f"<UM><POST><{path}>:UM Post:{post_body}")
            self.update_body_data()
            operator_key = post_body.get("operation")
            if operator_key in HTTPRequestHandler.operator_map:
                operator_val = HTTPRequestHandler.operator_map[operator_key]
                status = HTTPRequestHandler.response_init.get(operator_val).get("response")
            else:
                log.warning(f"<UM><POST><{path}><Response>:current program not deal operator key->{operator_key}")
        else:
            status['result_code'] = '2'
            status['message'] = ''
            log.warning(f"<UM><POST><{path}><Response>:current program not deal url")
        log.info(f"<UM><POST><{path}><Response>:{status}")
        response.write(json.dumps(status).encode(encoding='utf-8'))
        self.wfile.write(response.getvalue())


class UpdateMatrixData(BaseHTTPRequestHandler):
    queue = Queue()

    def do_POST(self):
        """
        处理post 请求
        :return:
        """
        log.info("<Matrix> <Script> post income...")
        parsed_result = urlparse(self.path)
        path = parsed_result.path
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = BytesIO()
        status = {
            "result_code": "0",
            "message": "",
        }
        if path == "/update/matrix/data":
            content_len = int(self.headers.get('Content-Length', 0))
            post_body = json.loads(self.rfile.read(content_len))
            log.info(f"<Matrix> <Script> Post请求的数据:{post_body}")
            UpdateMatrixData.queue.put(post_body)
        else:
            status['result_code'] = '2'
            status['message'] = 'post url not illegal'
            log.warning("<Matrix> <Script> post url not illegal")
        response.write(json.dumps(status).encode(encoding='utf-8'))
        self.wfile.write(response.getvalue())


def net_is_used(port, ip='0.0.0.0'):
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
        # log.warning('%s:%d is used' % (ip, port))
        return True
    except:
        # log.warning('%s:%d is unused' % (ip, port))
        return False


def matrix_init_back_process(ip, port, msg, queue):
    """

    :param ip:
    :param port:
    :param msg:
    :param queue:
    :return:
    """
    log.info(f'<Matrix> start {msg} back process http app...')
    if msg == "matrix":
        HTTPRequestHandler.queue = queue
        matrix = HTTPServer((ip, port), HTTPRequestHandler)
        log.info(f"<Matrix> matrix has started, {ip}, {port}")
        matrix.serve_forever()
    elif msg == "test":
        UpdateMatrixData.queue = queue
        test = HTTPServer((ip, port), UpdateMatrixData)
        log.info(f"<Matrix> test has started, {ip}, {port}")
        test.serve_forever()


if __name__ == '__main__':
    for port in [5003, 8091]:
        if net_is_used(port):
            if port == 8091:
                log.error(f"<Matrix> environment port {port} is used, please check environment port")
            elif port == 5003:
                log.error(f"<Matrix> environment port {port} is used, please check whether matrix program is running")
            sys.exit(1)
    matrix_q = Queue()
    matrix_process = Process(target=matrix_init_back_process, args=('0.0.0.0', 5003, "matrix", matrix_q))
    receive_process = Process(target=matrix_init_back_process, args=("0.0.0.0", 8091, "test", matrix_q))
    matrix_process.daemon = True
    receive_process.daemon = True
    matrix_process.start()
    receive_process.start()
    matrix_process.join()
    receive_process.join()
