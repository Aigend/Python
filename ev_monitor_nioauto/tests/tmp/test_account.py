#!/usr/bin/env python
# coding=utf-8
import copy
import csv
import json
import time

from tests.tmp.lat_long import LAT_LONG
from utils.assertions import assert_equal
from utils.coordTransform import wgs84_to_gcj02
from utils.time_parse import utc_strtime_to_timestamp
from utils.httptool import request


# from config.cert import web_cert

class TestAccount(object):

    def test_apply_fake_mobile_prod(self):
        """
        prod假手机号申请注册相关
        https://confluence.nioint.com/pages/viewpage.action?pageId=250158120
        :return:
        """
        host_in='https://app-int.nio.com'
        # host_in='https://app-stg-int.nio.com'

        host='https://app.nio.com'

        # [BETA]接口访问权限管理2.1 http://showdoc.nevint.com/index.php?s=/123&page_id=18228
        # 操作人只需要调用一次该接口
        # http = {
        #     "host": host_in,
        #     "uri": "/acc/3/in/add_kv_access",
        #     "method": "POST",
        #     "headers": {
        #         "Content-Type": "application/x-www-form-urlencoded"
        #     },
        #     "params": {
        #         "app_id": "10007",
        #         "region":"cn",
        #         "lang":"zh-cn",
        #         "nonce":"Stringtest"
        #     },
        #     "data":{
        #         "access_app_id":"100164",
        #         "fake_mobile":True,
        #         "operator":"li.liu2@nio.com"
        #     }
        #
        # }
        # response = request(http['method'], url=http['host'] + http['uri'], params=http['params'], headers=http['headers'], data=http['data']).json()
        # assert response['result_code']=='success'

        # 申请/刷新员工身份票据 http://showdoc.nevint.com/index.php?s=/123&page_id=5041
        # http = {
        #     "host": host_in,
        #     "uri": "/acc/3/in/email_ticket/refresh",
        #     "method": "POST",
        #     "headers": {
        #         "Content-Type": "application/x-www-form-urlencoded"
        #     },
        #     "params": {
        #         "app_id": "10007",
        #         "region":"cn",
        #         "lang":"zh-cn",
        #         "nonce":"Stringtest"
        #     },
        #     "data":{
        #         "effect_minutes":60*24*89, # 89天，最长不超过90天
        #         "email":"li.liu2@nio.com"
        #     }
        #
        # }
        # response = request(http['method'], url=http['host'] + http['uri'], params=http['params'], headers=http['headers'], data=http['data']).json()
        #
        # assert response['result_code']=='success'

        # # 申请假手机号
        # # 假手机号：http://showdoc.nevint.com/index.php?s=/123&page_id=5045
        # # ticket = input("输入ticket（来自邮件）:")
        # ticket = '9b5a01e9-dd61-42bc-b2b6-7f46e9d598d4-75ca5974-d3d8-43cb-9f6a-766663742ed3-49e9c9a6-d0bc-4438-b8bc-42bb0b35c174'
        # http = {
        #     "host": host_in,
        #     "uri": "/acc/3/in/fake_mobile/claim_as_fake",
        #     "method": "POST",
        #     "headers": {
        #         "Content-Type": "application/x-www-form-urlencoded"
        #     },
        #     "params": {
        #         "app_id": "10014",
        #         "region":"cn",
        #         "lang":"zh-cn",
        #         "nonce":"Stringtest"
        #     },
        #     "data":{
        #         "claimer":"li.liu2@nio.com",
        #         "ticket": ticket,
        #         "effect_minutes": 60*24*8, # 8 day
        #         "allowed_count":12,
        #         "reminder":"none",
        #         "country_code": "86"
        #
        #     }
        #
        # }
        # response = request(http['method'], url=http['host'] + http['uri'], params=http['params'], headers=http['headers'], data=http['data']).json()
        #
        # assert response['result_code']=='success'
        # print(f'=====\n {response["data"]}')
        #
        # # 手机号注册 http://showdoc.nevint.com/index.php?s=/123&page_id=3165
        # http = {
        #     "host": host,
        #     "uri": "/acc/2/register",
        #     "method": "POST",
        #     "headers": {
        #         "Content-Type": "application/x-www-form-urlencoded",
        #         'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BLN-AL20 Build/HONORBLN-AL20)/2.9.5-Lifestyle-Android'
        #     },
        #     "params": {
        #         "app_id": "10001",
        #         "region": "cn",
        #         "lang": "zh-cn",
        #         "nonce": "Stringtest"
        #     },
        #     "data": {
        #         # "country_code": response["data"]['country_code'],
        #         # "mobile": response["data"]['mobile'],
        #         # "verification_code": response["data"]['verification_code'],
        #         "country_code": '86',
        #         "mobile": '98762346092',
        #         "verification_code": '566550',
        #
        #         "device_id": "123123123",
        #     }
        #
        # }
        # response = request(http['method'], url=http['host'] + http['uri'], params=http['params'], headers=http['headers'], data=http['data']).json()
        #
        # assert response['result_code'] == 'success'
        # print(f'=====\n {response["data"]}')

        # 刷新手机号时间
        # ticket = '9b5a01e9-dd61-42bc-b2b6-7f46e9d598d4-75ca5974-d3d8-43cb-9f6a-766663742ed3-49e9c9a6-d0bc-4438-b8bc-42bb0b35c174'
        # ticket = '2c201d3f-0e96-453f-a085-501bce3bce19-edd5fbfa-4753-40a6-94dc-f1127df91115-1839f295-5d42-49ec-9e01-6c83da66aaa0'
        # http = {
        #     "host": host_in,
        #     "uri": "/acc/3/in/fake_mobile/refresh",
        #     "method": "POST",
        #     "headers": {
        #         "Content-Type": "application/x-www-form-urlencoded"
        #     },
        #     "params": {
        #         "app_id": "10014",
        #         "region":"cn",
        #         "lang":"zh-cn",
        #         "nonce":"Stringtest"
        #     },
        #     "data":{
        #         "claimer":"li.liu2@nio.com",
        #         "ticket": ticket,
        #         "effect_minutes": 60*24*8, # prod
        #         "allowed_count":12, # prod
        #         # "effect_minutes": 525600,
        #         # "allowed_count":100000,
        #         "country_code": "86",
        #         "mobile":"98762346109",
        #
        #     }
        #
        # }
        # response = request(http['method'], url=http['host'] + http['uri'], params=http['params'], headers=http['headers'], data=http['data']).json()

        ## 查询fake mobile信息 http://showdoc.nevint.com/index.php?s=/123&page_id=5047
        ticket = '9b5a01e9-dd61-42bc-b2b6-7f46e9d598d4-75ca5974-d3d8-43cb-9f6a-766663742ed3-49e9c9a6-d0bc-4438-b8bc-42bb0b35c174'
        http = {
            "host": host_in,
            "uri": "/acc/3/in/fake_mobile/detail",
            "method": "GET",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "params": {
                "app_id": "10007",
                "nonce": "Stringtest",
                "claimer": "li.liu2@nio.com",
                "ticket": ticket,
                "country_code": "86",
                "mobile": "98762346092",
            },

        }
        response = request(http['method'], url=http['host'] + http['uri'], params=http['params'], headers=http['headers']).json()
