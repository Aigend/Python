#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:chunming.liu
@time: 2020/06/16 16:38
@contact: chunming.liu@nio.com
@description: 发起http请求的客户端，封装了requests，根据tsp的业务场景增加了变量替换、自动签名、证书查找、自动代理等功能
"""
import json
from utils.logger import logger as logging
from json import JSONDecodeError
import allure
import curlify
import requests
from utils.signature import moatkeeper_signature


class TSPRequest(object):
    @staticmethod
    def request(env, inputs):
        # 1. 用配置文件中的数据替换测试数据中{{}}中间的内容
        # inputs = render(env, inputs) # 放到pytest_generate_tests中了
        cmdopt = env['cmdopt']
        # 2.app_id转换
        if 'marcopolo' in cmdopt and 'params' in inputs and 'sign' in inputs['params']:
            inputs['params']['hash_type'] = 'sha256'
            app_id_map = {'10001': 1000004, '10002': 1000003, '10003': 1000014, '10006': 1000027, '10014': 1000012, '10018': 1000014, '10016': 10000}
            if "data" in inputs and "origin_app_id" in inputs["data"]:
                inputs['data']['origin_app_id'] = app_id_map.get(str(inputs['data']['origin_app_id']), inputs['data']['origin_app_id'])
            inputs['params']['app_id'] = app_id_map.get(str(inputs['params']['app_id']), inputs['params']['app_id'])
        # 3. 计算签名，并添加到params
        if 'params' in inputs and 'sign' in inputs['params']:
            # 将headers中的key统一转化为全小写
            inputs["headers"] = {str(k).lower(): v for k, v in inputs.get('headers', {}).items()}
            sign = moatkeeper_signature(inputs, env['secret'][int(inputs["params"]["app_id"])], inputs["headers"].get('authorization'))
            inputs['params']["sign"] = sign

        # 安全网关已对staging外网域名(app-stg.nio.com)配置防BOT规则,非原生APP请求会被拦截,需要加一个自定义请求头才能放行
        if 'stg' in cmdopt:
            if 'headers' not in inputs:
                inputs['headers'] = {}
            inputs['headers']['Rastoken'] = '8cdy4mDeE8ySwzRwzRF8dN8zMaYK2H9n'

        # 4. 设置代理，命令行如何设置代理的话，就走代理
        if env.get('proxy'):
            inputs['proxies'] = env.get('proxies')

        # 5. 发送请求
        # logging.info("请求对象\n" + json.dumps(inputs, indent=2, ensure_ascii=False))
        logging.info(f"请求对象\n{inputs}")  # inputs 中包含有字节流使用dump会报错暂时去掉
        with allure.step("发起请求{}{}".format(inputs.get("method"), inputs.get("host") + inputs.get("path"))):
            if "files" not in inputs.keys():
                allure.attach(json.dumps(inputs, indent=2, ensure_ascii=False), '请求对象')
            r = requests.request(inputs.pop("method"),
                                 url=inputs.pop("host") + inputs.pop("path"),
                                 **inputs)
            if not inputs.get("files"):  # 如果是上传文件类请求不打印curl语句
                curl_print(r.request, inputs)
            r.encoding = 'utf-8'
            logging.info(f'Response status code: {r.status_code}')
            try:
                response = r.json()
                response_txt = json.dumps(response, indent=2, ensure_ascii=False)
            except JSONDecodeError:
                response = response_txt = r.text
            allure.attach(response_txt, '响应结果')
            logging.info("响应结果\n" + response_txt)
            return response


def curl_print(req: requests.request, inputs):
    curl_str = curlify.to_curl(req)
    if 'cert' in inputs and inputs['cert'] is not None:
        curl_str += f" --tlsv1.2 --cert {inputs['cert'][0]} --key {inputs['cert'][1]}"
        curl_str += f" --cacert {inputs['verify']}" if 'verify' in inputs else " -k"
    logging.info(curl_str)
