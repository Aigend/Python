#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/07 19:13
@contact: li.liu2@nio.com
@description:
    给手机推送消息，消息会在 朋友->消息 中显示。App端如要验证，需需要手机先登陆（bind）
    http://showdoc.nevint.com/index.php?s=/13&page_id=60

    * 支持按照Client ID／User ID 进行推送。
    * 支持透传（MiPush）
    * 支持消息分类
    * 支持只记录历史，不推送的功能。或者只推送，不记录历史的功能。
    手机的通知指的是通知栏弹出信息。通知栏弹出的条件如下：
    * 手机系统开启允许通知
    * 用户登陆了APP且没有退出登陆（即手机为绑定状态binding表visible=1。手机登陆后的黑屏，或者kill进程都不会使得手机unbind。只有点击logout退出APP时，才会调用unbind接口解绑）
    notify接口被谁调用：
        * 有的时候时直接被第三方服务调用，例如infotainment_fundamental的的nomi时刻通知，
        * 有时是通过别的接口封装一下用，例如hermes->APP Msg（APP中台）接口api/1/in/app_msg/common->notify接口。
    推送形式 channel字段：
        * 根据notify接口的channel值可选:"all", "mqtt", "mipush", "apns", "jpush", "hwpush", "email"。
        * "all"：默认值
            默认指的是找最合适的方法推，如手机在线并保持常亮的话，会优先选mqtt推送。
            不可mqtt推送时，按照苹果小米等不同手机类型推到不同平台再由平台push
        * "mqtt"：使用MQTT方式来推送；
        * "mipush"：使用Mipush方式来推送，要求设备是有Mipush的regid；
            用小米的时候，根据设备登陆NIOApp的活跃程度（即每天的连接数，连接数每天会变动）的一定倍数关系来确定当天能够接受多少条push信息。
            所以如果小米设备连接不活跃的话，可能给的push配额会比较少导致5001 exceed quota error
        * "apns"：使用APNS方式推送，要求设备是有APNS的device token；
        * "jpush"：按Jpush方式推送，要求设备有Jpush的regid。
        * "email"：推送到邮箱，要求账号为邮箱注册账户。
    推送类型category：'category', ['default', 'activity', 'red_packet', "logistics", "notification"]
        * "default" 默认（app中显示在通知里）
        * "activity" 活动
        * "red_packet" 积分红包
        * "logistics" 物流
        * "notification" 通知
    推送是否存储 store_history：
        * 'store_history': True 记录历史消息存到数据库。默认是True。
        * 如果store_history=True，则即使没有弹出通知，也会在消息中看到消息记录。

"""
import json
import random
import time
import allure
import pytest

from tests.app_message_center.test_push_notify import init_notify_account
from utils.logger import logger
from utils.assertions import assert_equal
from utils.http_client import TSPRequest as hreq

# app_id = 10001
register_path = '/api/1/message/register_client'
bind_path = '/api/1/message/bind_client'
unbind_path = '/api/1/message/unbind_client'
update_path = '/api/1/message/update_client'

userinfo_test = [{'user_id': '397571871', 'phone': '98762754786', 'phone_code': '437364', 'app_id': '10001', 'channel': 'hwpush', 'description': '华为手机真机登录'},
                 {'user_id': '14967171', 'phone': '98762754808', 'phone_code': '136277', 'app_id': '10001', 'channel': 'mipush', 'description': '小米手机真机登录'},
                 {'user_id': '67669783', 'phone': '98762754809', 'phone_code': '640440', 'app_id': '10002', 'channel': 'apns', 'description': '苹果手机真机登录'},
                 {'user_id': '239367547', 'phone': '98762754810', 'phone_code': '933026', 'app_id': '10001', 'channel': 'jpush', 'description': '华为手机真机登录'},
                 {'user_id': '212409581', 'phone': '98762667410', 'phone_code': '112233', 'app_id': '10002', 'channel': 'apns', 'description': 'li苹果手机真机登录'},
                 ]

userinfo_stg = [{'user_id': '50223594', 'phone': '98762487791', 'phone_code': '568730', 'app_id': '10001', 'channel': 'hwpush', 'description': '华为手机真机登录'},
                {'user_id': '482613576', 'phone': '98762487792', 'phone_code': '567406', 'app_id': '10001', 'channel': 'mipush', 'description': '小米手机真机登录'},
                {'user_id': '475159811', 'phone': '98762487793', 'phone_code': '331995', 'app_id': '10002', 'channel': 'apns', 'description': '苹果手机真机登录'},
                ]


class TestNotify(object):
    push_notify_one_config_cn_keys = "case_name,category,target_app_id,channel,host_key,data_key"
    push_notify_one_config_cn_cases = [
        # TOC服务 10001 允许的category测试案例
        ("正案例_TOC_category=default,target_app_id=10001", 'activity', "10001", 'all', "app_in", "nmp_app"),
        ("正案例_TOC_category=notification,target_app_id=10001", 'notification', "10001", 'all', "app_in", "nmp_app"),
        ("正案例_TOC_category=activity,target_app_id=10001", 'activity', "10001", 'all', "app_in", "nmp_app"),
        ("正案例_TOC_category=logistics,target_app_id=10001", 'logistics', "10001", 'all', "app_in", "nmp_app"),
        ("正案例_TOC_category=red_packet,target_app_id=10001", 'red_packet', "10001", 'all', "app_in", "nmp_app"),
        # TOC服务 10002 允许的category测试案例
        ("正案例_TOC_category=default,target_app_id=10002", 'activity', "10002", 'all', "app_in", "nmp_app"),
        ("正案例_TOC_category=notification,target_app_id=10002", 'notification', "10002", 'all', "app_in", "nmp_app"),
        ("正案例_TOC_category=activity,target_app_id=10002", 'activity', "10002", 'all', "app_in", "nmp_app"),
        ("正案例_TOC_category=logistics,target_app_id=10002", 'logistics', "10002", 'all', "app_in", "nmp_app"),
        ("正案例_TOC_category=red_packet,target_app_id=10002", 'red_packet', "10002", 'all', "app_in", "nmp_app"),
    ]

    @pytest.mark.parametrize(push_notify_one_config_cn_keys, push_notify_one_config_cn_cases)
    def test_notify_by_app_id(self, env, cmdopt, case_name, category, target_app_id, channel, host_key, data_key, mysql):
        """
            给手机推送消息，消息会在 朋友->消息 中显示。App端如要验证，需需要手机先登陆（bind）
            http://showdoc.nevint.com/index.php?s=/13&page_id=60
            推送成功的条件：
                1.account注册（手机号，验证码注册，或者邮箱注册（邮箱注册账户将会推送消息到邮箱渠道为email））
                2.在消息平台注册client_id（新设备首次登录注册）
                3.绑定客户端（app登录时调用）（理论上一个账户同时存在一个绑定，退出时会进行解绑）
                4.
            redis校验:会造成大量缓存占用redis内存去掉了缓存机制（2021.5.7）
                * key的规则：keyPattern = "msg_cache:{app_id}:{user_id}:{category}:"
                * app_id：实际为group_id(10001和10002会在redis中存为10001)
        """
        target_app_ids = "10001,10002"
        user_id = env["app_message_keeper"][data_key][int(target_app_id)]["user1"]["account_id"]
        init_notify_account(env, mysql, data_key, host_key, user_id, target_app_id)
        group_id = ['10001', '10002']
        inputs = {
            "host": env['host']['app_in'],
            "path": "/api/1/in/message/notify",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": 'Dalvik/2.1.0 (Linux; U; Android 7.0; BLN-AL20 Build/HONORBLN-AL20)/2.9.5-Lifestyle-Android',
            },
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "sign": "",
                "app_id": "10000"
            },
            "data": {
                'nonce': 'MrVIRwkCLBKySgCA',
                'async': False,
                'user_ids': user_id,
                'ttl': 100000,
                'target_app_ids': target_app_ids,
                'do_push': True,
                'scenario': 'fs_system',
                'channel': channel,
                "category": category,
                'payload': json.dumps(
                    {
                        "target_link": "http://www.niohome.com",
                        "description": f"description时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} category:{category}user_id:{user_id}app_id:{target_app_id}",
                        "title": f"【{cmdopt}】环境{channel}渠道推送测试"})
            },
        }

        response = hreq.request(env, inputs)
        assert response['result_code'] == 'success'
        message_id = response['data'].pop('message_id', '')
        time.sleep(5)
        with allure.step("校验mysql"):
            message_in_mysql = mysql['nmp_app'].fetch(f'history_{str(user_id)[-3:]}', {'user_id': user_id, 'message_id': message_id})
            assert_equal(len(message_in_mysql), 1)

    @pytest.mark.skip('manual')
    @pytest.mark.parametrize('category, channel, user_id, app_id, description',
                             [
                                 # ('default', 'mqtt', '397571871', '10001', '华为手机真机登录'),
                                 # ('red_packet', 'all', '320597641,14967171', '10001', '华为手机真机登录'),
                                 # ('in_box', 'all', '1014839931', '1000004', '马克波罗test环境'),
                                 # ('logistics', 'mqtt', '397571871', '10001', '华为手机真机登录'),
                                 # ('logistics', 'mqtt', '1482247961', '10001', '华为手机真机登录'),
                                 # ("activity", 'all', '239367547', '10001', '华为手机真机登录'),
                                 # ("activity", 'all', '14967171', '10001', '华为手机真机登录'),
                                 # ("activity", 'all', '180205016', '10001', 'prod苹果推送'),
                                 # ("activity", 'all', '180205016', '10001', 'prod苹果推送'),
                                 # ("activity", 'all', '100722', '10002', 'test苹果推送'),
                                 # ("activity", 'all', '35899062', '10002', 'test苹果推送'),
                                 # ("activity", 'all', '301124399', '10001', 'vivo test安卓推送'),
                                 # ("activity", 'vivo', '301124399', '10001', 'vivo test安卓推送'),
                                 # ("activity", 'all', '151103551', '10001', 'oppo test安卓推送'),
                                 # ("activity", 'oppo', '151103551', '10001', 'oppo test安卓推送'),
                                 ("notification", 'all', '245460322', '10001', 'oppo test安卓推送'),
                                 # ("notification", 'mipush', '791993250', '10001', '小米手机真机登录'),
                                 # ("activity", 'all', '14967171', '10001', '小米手机真机登录'),
                                 # ("activity", 'hwpush', '170511972', '10001', '小米手机真机登录'),
                                 # ("activity", 'all', '854720060', '10002', '苹果手机真机登录'),
                                 # ("activity", 'apns', '66650651', '10002', '苹果手机真机登录'),
                                 # ("activity", 'apns', '67669783', '10002', '苹果手机真机登录'),
                                 # ("activity", 'apns', '475159811', '10002', '苹果手机真机登录'),
                                 # ("activity", 'all', '212409581', '10002', '苹果手机真机登录'),
                                 # ("activity", 'all', '212409581', '10002', '苹果手机真机登录'),
                             ])
    def test_notify(self, env, cmdopt, category, channel, user_id, description, app_id, mysql, redis):
        """
            给手机推送消息，消息会在 朋友->消息 中显示。App端如要验证，需需要手机先登陆（bind）
            http://showdoc.nevint.com/index.php?s=/13&page_id=60
            推送成功的条件：
                1.account注册（手机号，验证码注册，或者邮箱注册（邮箱注册账户将会推送消息到邮箱渠道为email））
                2.在消息平台注册client_id（新设备首次登录注册）
                3.绑定客户端（app登录时调用）（理论上一个账户同时存在一个绑定，退出时会进行解绑）
                4.
            redis校验:会造成大量缓存占用redis内存去掉了缓存机制（2021.5.7）
                * key的规则：keyPattern = "msg_cache:{app_id}:{user_id}:{category}:"
                * app_id：实际为group_id(10001和10002会在redis中存为10001)
        """

        # user_id = "301124399"  # vivo
        # user_id = "151103551"  # oppo
        # user_id = "820876676"  # oppo
        # user_id = "100398"  # oppo vivo 线上机器


        target_app_ids = "10001,10002"
        target_app_ids = "10001"
        if 'marcopolo' in cmdopt:
            target_app_ids = '1000003,1000004'
        inputs = {
            "host": env['host']['app_in'],
            "path": "/api/1/in/message/notify",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": 'Dalvik/2.1.0 (Linux; U; Android 7.0; BLN-AL20 Build/HONORBLN-AL20)/2.9.5-Lifestyle-Android'
            },
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "sign": "",
                "app_id": "10000"
            },
            "data": {
                'nonce': 'MrVIRwkCLBKySgCA',
                'async': False,
                'user_ids': user_id,
                'ttl': 100000,
                'target_app_ids': target_app_ids,
                'do_push': True,
                'scenario': "ls_link",
                'channel': channel,
                "category": category,
                'payload': json.dumps(
                    {
                        "target_link": "http://www.niohome.com",
                        "description": f"description时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} category:{category}user_id:{user_id}app_id:{app_id}",
                        "title": f"【{cmdopt}】环境message_api {channel}渠道推送测试"})
            },
        }

        response = hreq.request(env, inputs)
        assert response['result_code'] == 'success'
        message_id = response['data'].pop('message_id', '')
        time.sleep(5)
        with allure.step("校验mysql"):
            message_in_mysql = mysql['nmp_app'].fetch(f'history_{str(user_id)[-3:]}', {'user_id': user_id, 'message_id': message_id})
            assert_equal(len(message_in_mysql), 1)


    def test_notify_batch(self, env, cmdopt, mysql, redis):
        """
            给手机推送消息，消息会在 朋友->消息 中显示。App端如要验证，需需要手机先登陆（bind）
            http://showdoc.nevint.com/index.php?s=/13&page_id=60
            推送成功的条件：
                1.account注册（手机号，验证码注册，或者邮箱注册（邮箱注册账户将会推送消息到邮箱渠道为email））
                2.在消息平台注册client_id（新设备首次登录注册）
                3.绑定客户端（app登录时调用）（理论上一个账户同时存在一个绑定，退出时会进行解绑）
                4.
            redis校验:
                * key的规则：keyPattern = "msg_cache:{app_id}:{user_id}:{category}:"
                * app_id：实际为group_id(10001和10002会在redis中存为10001)
        """
        category = random.choice(['default', 'activity', 'red_packet', "logistics", "notification"])
        user_id_ls = mysql["nmp_app"].fetch("bindings", where_model={'visible': 1, 'user_id>': 1000, 'app_id in': ['10001', '10002']}, fields=["account_id", "user_id"],
                                            suffix=f"limit 10")
        user_ids = [str(u.get("user_id")) for u in user_id_ls]
        user_ids.append("-1")  # 添加假数据，所以会存在部分推送不成功
        app_id = "10001,10002"
        inputs = {
            "host": env['host']['app_in'],
            "path": "/api/1/in/message/notify",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": 'Dalvik/2.1.0 (Linux; U; Android 7.0; BLN-AL20 Build/HONORBLN-AL20)/2.9.5-Lifestyle-Android'
            },
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "sign": "",
                "app_id": "10013"
            },
            "data": {
                'nonce': 'MrVIRwkCLBKySgCA',
                'async': False,
                'user_ids': ','.join(user_ids),
                'ttl': 100000,
                'target_app_ids': app_id,
                'do_push': True,
                'scenario': 'fs_system',
                "category": category,
                'payload': json.dumps(
                    {"target_link": "http://www.niohome.com",
                     "description": f"description时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} category:{category}user_id:{','.join(user_ids)}app_id:{app_id}",
                     "title": f"【{cmdopt}】环境batch推送测试"})
            },
        }

        response = hreq.request(env, inputs)
        message_id = response.get("data").get('message_id', '')
        details = response.get("data").get("details")
        user_id_success = set([detail.get("user_id") for detail in details if detail.get("result") == "success"])
        time.sleep(5)
        with allure.step("校验mysql"):
            for user_id in user_id_success:
                message_in_mysql = mysql['nmp_app'].fetch(f'history_{str(user_id)[-3:]}', {'user_id': user_id, 'message_id': message_id})
                assert_equal(len(message_in_mysql), 1)
            assert response['result_code'] == 'partial_success'