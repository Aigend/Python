# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : account_token.py
# @Author : qiangwei.zhang.o
# @CreateTime : 2021/3/3 11:15 上午
# @Description :

import json
import random
import string
import time
from utils.httptool import request as rq
from utils.assertions import assert_equal
from utils.signature import encrypt, checkedPassword


def get_encryption_poseidon(host, app_id=10000, **kwargs):
    url = host + "/api/1/poseidon/account/get_encryption"
    querystring = {"app_id": app_id}
    response = rq("GET", url, params=querystring)
    return response.json()['data']['key_id'], response.json()['data']['key']


def get_encryption_acc(host, app_id=10000, **kwargs):
    url = host + "/acc/2/in/get_encryption"
    querystring = {"app_id": app_id, "nonce": str(int(time.time()))}
    response = rq("GET", url, params=querystring)
    return response.json()['data']['key_id'], response.json()['data']['key']


def send_email_verification_code(env, mysql, email=None, app_id=10001):
    # /acc/2/in/verification_code/send/email
    # http://showdoc.nevint.com/index.php?s=/123&page_id=14052
    # classifier: forgot_password忘记密码; register账户注册;change_email修改邮箱;deactivate_account注销账号;common_verification通用检查
    if not email:
        # ran_str = str(int(time.time()))[0:9]
        ran_str = ''.join(random.sample(string.hexdigits, 10))
        email = ran_str + "@163.com"
    host = env['host']['app_in']
    http = {
        "host": host,
        "method": 'POST',
        "uri": "/acc/2/in/verification_code/send/email",
        "headers": {'Content-Type': "application/x-www-form-urlencoded"},
        "params": {"region": 'cn',
                   "lang": "zh-cn",
                   "app_id": app_id,
                   'nonce': str(int(time.time() * 1000)),
                   },
        "data": {
            "email": email,
            "classifier": 'register',
        }
    }
    response = rq(http['method'], url=http['host'] + http['uri'], params=http['params'], data=http['data'], headers=http['headers'])
    response_dict = response.json()
    if response_dict['result_code'] == 'success':
        time.sleep(2)
        user_list = mysql['account_center'].fetch(table='ac_email_verification_code', where_model={'email': email}, fields=['verification_code'], order_by="create_time desc")
        verification_code = user_list[0]["verification_code"]
        return email, verification_code


def get_ticket(env, email, verification_code, app_id=10001):
    host = env['host']['app_in']
    http = {
        "host": host,
        "method": 'POST',
        "uri": "/acc/2/in/verification_code/email",
        "headers": {'Content-Type': "application/x-www-form-urlencoded"},
        "params": {"email": email,
                   "classifier": 'register',
                   "verification_code": verification_code,
                   "app_id": app_id,
                   'nonce': str(int(time.time() * 1000)),
                   }
    }
    response = rq(http['method'], url=http['host'] + http['uri'], params=http['params'], headers=http['headers'])
    response_dict = response.json()
    if response_dict['result_code'] == 'success':
        # 调用获取tick接口
        return response_dict['data']['ticket']


def app_email_register(env, email, ticket, app_id=10001):
    key_id, key = get_encryption_poseidon(env['host']['tsp'])
    password_e = encrypt(str("1q2w3e4r5t6y7u8i9o"), key).decode("utf-8")
    http = {
        "host": env['host']['app_in'],
        "uri": "/acc/3/in/app_email/register",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "params": {
            "region": "cn",
            "lang": "zh-cn",
            "app_id": app_id,
            "nonce": str(time.time())
        },
        "data": {
            "email": email,
            "password_e": password_e,
            "key_id": key_id,
            "ticket": ticket,
            "country": "cn",
            "city": "BEIJING",
            "language": "zh",
            "nick_name": 'Maple ' + ''.join(random.sample(string.ascii_letters, 6)),
            "first_name": ''.join(random.sample(string.ascii_letters, 6)),
            "last_name": ''.join(random.sample(string.ascii_letters, 8)),
            "device_id": ''.join(random.sample(string.ascii_letters, 13)),
            "ip": '127.0.0.1',
        }
    }
    response = rq(http['method'], url=http['host'] + http['uri'], params=http['params'], data=http['data'], headers=http['headers'])
    response_dict = response.json()
    assert response_dict["data"]["account_id"]
    return response_dict["data"]["account_id"]


# region=cn&lang=zh-cn&app_id=10000&nonce=1611914557.4189749&timestamp=1611914557&sign=18ad899271c8752f64217dad960988b9'
def email_login(env, email, app_id=10001):
    key_id, key = get_encryption_poseidon(env['host']['tsp_in'])
    password_e = checkedPassword(str("1q2w3e4r5t6y7u8i9o"), key).decode("utf-8")
    http = {
        "host": env['host']['app_in'],
        "uri": "/acc/2/in/login/email",
        # "uri": "/acc/3/in/app_email/login",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "params": {
            "region": "cn",
            "lang": "zh-cn",
            "app_id": app_id,
            'nonce': f"test{str(int(time.time() * 1000))}"
        },
        "data": {
            "email": email,
            "password_e": password_e,
            "key_id": key_id,
            "device_id": '10001',
            "terminal": json.dumps({"app_id": "10001", "desc": "测试专属id"}),
            "origin_app_id": app_id,
            "remote_ip": "127.0.0.1",
        }
    }
    response = rq(http['method'], url=http['host'] + http['uri'], params=http['params'], data=http['data'], headers=http['headers'], is_sign=True)
    response_dict = response.json()
    assert response_dict['result_code'] == 'success'
    assert response_dict['data']['access_token']
    assert response_dict['data']['account_id']
    return response_dict['data']['account_id'], response_dict['data']['access_token']


def phone_login(env, mobile, vc_code, app_id=10001):
    """
    /acc/2/login
    接口文档：http://showdoc.nevint.com/index.php?s=/123&page_id=3160
    """
    # mobile = env['vehicles']['normal']['mobile']
    # vc_code = env['vehicles']['normal']['vc_code']
    mobile = mobile
    vc_code = vc_code
    # account_id = 1003669139
    country_code = '86'
    app_id = app_id
    host = env['host']['app_in']
    http = {
        "host": host,
        "method": "POST",
        "uri": "/acc/2/login",
        "headers": {'content-type': 'application/x-www-form-urlencoded',
                    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BLN-AL20 Build/HONORBLN-AL20)/2.9.5-Lifestyle-Android'
                    },
        "params": {
            'region': 'cn',
            'lang': 'zh-cn',
            'app_id': app_id,
            'nonce': int(time.time()),
        },
        "data": {
            'mobile': mobile,
            'verification_code': vc_code,
            'country_code': country_code,
            'authentication_type': 'mobile_verification_code',
            'device_id': app_id,
            "terminal": '{"name":"我的华为手机","model":"HUAWEI P10"}',
        },
    }
    response = rq(http['method'], url=http['host'] + http['uri'], params=http['params'], data=http['data'], headers=http['headers'], is_sign=True)
    response_dict = response.json()
    assert response_dict['result_code'] == 'success'
    assert response_dict['data']['access_token']
    assert response_dict['data']['account_id']
    return response_dict['data']['account_id'], response_dict['data']['access_token']


def register_client(env, app_id=10001):
    # http://showdoc.nevint.com/index.php?s=/13&page_id=1070
    if str(app_id) == '10001':
        device_type = 'android'
        brand = 'Huawei'
        os = 'android'
    elif str(app_id) == '10002':
        device_type = 'ios'
        brand = 'IPhone'
        os = 'ios'
    else:
        device_type = 'android'
        brand = 'Huawei'
        os = 'android'
    http = {
        "host": env['host']['app_in'],
        "uri": "/api/1/message/register_client",
        "method": "POST",
        "headers": {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        'params': {
            'app_id': app_id,
            'region': 'cn',
            'lang': 'zh_cn'
        },
        'data': {
            'app_version': '9.1.0',
            'brand': brand,
            'device_type': device_type,
            'device_id': ''.join(random.sample(string.ascii_letters, 13)),
            'device_token': ''.join(random.sample(string.ascii_letters, 13)),
            'os': os,
            'os_version': '6.0',
            'nonce': f"test{str(int(time.time() * 1000))}"
        },
    }
    response = rq(http['method'], url=http['host'] + http['uri'],
                  params=http['params'], data=http['data'], headers=http['headers'])
    if response.status_code == 200:
        response_dict = response.json()
        assert response_dict['result_code'] == 'success'
        return app_id, response_dict['data']['client_id']


def prepare_bind(env, access_token, client_id_app, app_id=10001):
    '''
    用户登陆|退出APP时，调用binding|unbinding 接口
    http://showdoc.nevint.com/index.php?s=/13&page_id=1071
    绑定和解绑客户端是针对用户而言的，每个用户可以绑定多个客户端，通过这样的机制能保证，推送给这个用户的时候，各个设备都可以收到相应的推送。同理，设备解绑之后将不再收到发送给此用户的信息。
    '''
    http = {
        "host": env['host']['app'],
        "uri": "/api/1/message/bind_client",
        "method": "POST",
        "headers": {
            "authorization": f'Bearer {access_token}',
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": 'Dalvik/2.1.0 (Linux; U; Android 7.0; BLN-AL20 Build/HONORBLN-AL20)/2.9.5-Lifestyle-Android'
        },
        "params": {
            "region": "cn",
            "lang": "zh-cn",
            "app_id": app_id,
        },
        "data": {
            'client_id': client_id_app,
            'nonce': f"test{str(int(time.time() * 1000))}"
        }
    }

    response = rq(http['method'], url=http['host'] + http['uri'],
                  params=http['params'], data=http['data'], headers=http['headers']).json()
    assert_equal(response['result_code'], 'success')


def prepare_unbind(env, access_token, client_id_app, app_id=10001):
    '''
    用户登陆|退出APP时，调用binding|unbinding 接口
    http://showdoc.nevint.com/index.php?s=/13&page_id=1071
    绑定和解绑客户端是针对用户而言的，每个用户可以绑定多个客户端，通过这样的机制能保证，推送给这个用户的时候，各个设备都可以收到相应的推送。同理，设备解绑之后将不再收到发送给此用户的信息。
    '''
    http = {
        "host": env['host']['app'],
        "uri": "/api/1/message/unbind_client",
        "method": "POST",
        "headers": {
            "authorization": f'Bearer {access_token}',
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": 'Dalvik/2.1.0 (Linux; U; Android 7.0; BLN-AL20 Build/HONORBLN-AL20)/2.9.5-Lifestyle-Android'
        },
        "params": {
            "region": "cn",
            "lang": "zh-cn",
            "app_id": app_id,
        },
        "data": {
            'client_id': client_id_app,
            'nonce': f"test{str(int(time.time() * 1000))}"
        }
    }

    response = rq(http['method'], url=http['host'] + http['uri'],
                  params=http['params'], data=http['data'], headers=http['headers']).json()
    assert_equal(response['result_code'], 'success')
