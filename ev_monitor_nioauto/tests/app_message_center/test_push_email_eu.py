# -*- coding: utf-8 -*-
# @Project : cvs_basic_autotest
# @File : test_push_email.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/3/16 6:04 下午
# @Description :

"""
1.银龙存在为True，消息平台不存在
2.银龙存在为False，消息平台不存在
3.银龙存在为True,消息平台存在为True
4.消息平台存在为True,银龙不存在
5.消息平台存在为False,银龙不存在
6.消息平台不存在,银龙不存在
"""

import time
import os
import pytest
import allure
import string
import random

from tests.app_message_center.clear_rate_limit import clear_rate_limit
from utils.assertions import assert_equal
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from data.email_content import long_text, html5
from utils.random_tool import random_string, random_int
from config.settings import BASE_DIR
from utils.collection_message_states import collection_message_states

allow_environment = ["test_marcopolo", "stg_marcopolo"]


def get_user_retry(func):
    def inner(*args, **kwargs):
        ret = func(*args, **kwargs)
        max_retry = 20
        number = 0
        if not ret:
            while number < max_retry:
                number += 1
                time.sleep(5)
                logger.debug(f"尝试第:{number}次")
                result = func(*args, **kwargs)
                if result:
                    return result
        else:
            return ret

    return inner


@pytest.mark.run(order=1)
class TestPushEmailEU(object):
    """
    1）推送邮件接口
        接口文档 http://showdoc.nevint.com/index.php?s=/13&page_id=29731
        推送成功的条件：
            1.留资注册邮箱账户（目前在account马克波罗环境注册邮箱账户，会通过Kafka推送到留资）
            2.开启对应渠道订阅开关 set_switch
        redis校验:
            * key的规则：及缓存内容
            nmp:notification_switch:{user_id}:{channel}:{category} 缓存开关状态
            nmp:EuUserService:map:user:{user_id} 缓存account_id
            nmp:EuUserService:map:acc:{account_id} 缓存user_id
        mysql校验：
            email_history
            email_history_meta_info
            notification_switch
        字段说明：
            user_ids: 官网留资用户id（user_ids，account_ids，recipients三选一）
            account_ids:account用户ID（user_ids，account_ids，recipients三选一）
            recipients: 收件人邮箱（user_ids，account_ids，recipients三选一）（verify渠道不需要在留资存在，端口号可配置目前test环境是100423）
            subject: 主题{不支持变量名称，接口不限制长度}
            content: 内容{不支持变量名称，接口不限制长度}
            category: 渠道 email{marketing_email,fellow_contact},push{likes,reply}
        测试数据：
            "user_id": 115745824, "email": "550736273@qq.com", "account_id": 1007994704
            nmp:notification_switch:115745824:email:marketing_email
            nmp:notification_switch:115745824:email:fellow_contact
            nmp:EuUserService:map:user:115745824
            nmp:EuUserService:map:acc:1007994704
        测试场景：
            1.正案例
                账户在account存在（account_id）
                账户在留资存在（user_id）
                账户已订阅
                推送消息成功
            user_ids: 官网留资用户id,  account_ids:account用户ID, recipients 收件人
                1.单个正常用户推送
                2.多个正常用户推送
                3.多个正常用户推送，存在重复用户id
                4.单个异常用户
                5.多个异常用户
                6.一部分正常用户，一部分异常用户
                7.重复用户
                8.异常数据，分隔符前后有空格，中间包含异常数据（非整数类型）
                （user_ids，account_ids，recipients三选一）
            recipients: 在官网留资存在的邮箱（user_ids，account_ids，recipients三选一）
            subject: 主题
            content: 内容
            category: 渠道
            字段：
                user_ids: 官网留资用户id,  account_ids:account用户ID, recipients
                    1.只传一个  测试通过
                    2.三个都传  测试通过（有校验）
                    3.三个都不传 测试通过（有校验）
                    4.传2个 测试通过（有校验）
                category：
                    1.传正常值 测试通过
                    2.异常值
                    3.不传 测试通过（有校验）
                subject：
                    1.长度限制 （否，app网关有整体playload校验，默认1M）
                    2.必传校验 测试通过（有校验）
                    3.支持格式 字符串
                    4.支持变量（不支持）
                content：
                    1.长度限制 （否，app网关有整体playload校验，默认1M）
                    2.必传校验 测试通过（有校验）
                    3.支持格式 html5,图片链接 测试通过
                    4.支持变量如用户昵称（不支持）

    2）订阅开关设置接口
        http://showdoc.nevint.com/index.php?s=/13&page_id=29818
        channel:
            * email
                category
                    * marketing_email
                    * fellow_contact
            * push(like,reply)
                    * likes
                    * reply
        switch（switch_status）: True or False
        user_id:用户在留资用户user_id
        account_id:用户在account的account_id
        redis_key: nmp:notification_switch:{user_id}:{channel}:{category}
        业务逻辑：
            设置订阅与取消订阅
            可以订阅或取消订阅对应channel的category；
                email对应marketing_email,fellow_contact;
                push对应likes,reply(后续扩展本次不做测试内容)
            设置订阅与取消订阅，会在mysql数据库存入，同时存入redis
            同时传user_id和account_id会以user_id为准
            只传account_id以account_id为准
        特殊情况：
            同时传user_id和account_id会以user_id为准，如果user_id无法解析，报错-- Internal Server Error；
            同时传user_id和account_id会以user_id为准，account_id无法解析，不会报错，不取account_id；
            只传account_id，account_id无法解析，会报错-- Internal Server Error
    3）查询订阅状态接口
        http://showdoc.nevint.com/index.php?s=/13&page_id=29846
        会将该账户下对应channel下的渠道订阅状态返回，可以同时传多个渠道
        同时传user_id和account_id会以user_id为准，忽略account_id，如果user_id无法解析，报错-- Internal Server Error；
        只传account_id，会根据account_id获取
        user_id和account_id 必须为正整数的数值类型，或正整数的字符串类型
    疑问问题和答案：Q&A
        Q1:  result_code 一部分成功，一部分失败状态码success, 全部失败状态码为success
            A— 无需更改
        Q2: 是否需要去重复逻辑，账户重复会发送两封一样的邮件，
           A 暂时不加去重复逻辑；
        Q3: redis key名称是否需要区分环境
            nmp:notification_switch:{user_id}:{channel}:{category}缓存开关状态
            nmp:EuUserService:map:user:{user_id}缓存account_id
            nmp:EuUserService:map:acc:{account_id}缓存user_id
            A 不需要，不存在不同环境共用一个redis的情况
        Q4: subject，content 是否有长度限制,支持变量如用户昵称
            A 暂时无长度限制，不支持变量，app的网关有限制默认1M可调整
        Q5:push  likes渠道的作用
            A —后续扩展
        Q6: 一次发送邮件条数目前有加限制么
            A 限制最多100条
        Q7:有无遗漏内容
            未公开用法：渠道：Verify 100423 直接发送到邮箱账户，无需注册,用在发送验证码场景
            fellow_contact 业务上的区分，系统内无区分，相当于透传
        Q8:通过user_id调用set_switch未判断用户是否在留资存在，不存在的user_id也能设置成功,是否加判断在留资是否存在
            不加该判断也无影响，后续发邮件会去查邮箱，但是会造成一部分垃圾数据，也有可能会导致，ID未未注册用户ID，后续注册后直接有状态数据的情况
            A 后续修改
        Q9:字符串有空格，后面数据无法处理，前面账户会报不存在,其中任何一个账户有问题（包含空格，非整数数字）会导致其他账户也无法正常发送邮件
            A 后续再修改
    问题记录：
            问题1：批量发送时，一部分成功一部分失败了，正常应该都成功，调单个可以成功--已解决，已验证
            问题2：设置订阅状态，先使用user_id订阅，再使用account_id取消订阅，数据库里状态为取消订阅，redis里未修改 --已解决，已验证

    测试数据eu_stg:
    {
        "user_id": "181914013",
        "email": "1619409286UtJTLw@walla.com",
        "account_id": "1015335784"
      }
            """

    @pytest.fixture(scope="class")
    def prepare_eu_email_account(self, env, cmdopt):
        cmdopt = "test_marcopolo" if cmdopt == 'test' else cmdopt
        # 消息平台test环境和test_marcopolo环境对应留资test_marcopolo环境
        file_path = f'{BASE_DIR}/config/{cmdopt}/email_account_info_{cmdopt}.txt'
        account_list = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    account_msg = {}
                    account_msg_list = line.split(',')
                    account_msg['account_id'] = account_msg_list[0]
                    account_msg['user_id'] = account_msg_list[1]
                    account_msg['recipient'] = account_msg_list[2]
                    account_msg['password'] = account_msg_list[3]
                    account_list.append(account_msg)
            return account_list
        else:
            logger.error(f"请先配置数据文件{file_path}\n数据格式：account_id,user_id,email,password,pseudo_email,create_time")

    def set_switch(self, env, channel, category, user_id=None, status=True):
        inputs = {
            "host": env['host']['app_in'],
            "path": "/api/2/in/message/set_switch",
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "params": {
                "region": "eu",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": "10007",
                "sign": ""
            },
            "data": {
                "user_id": user_id,
                "channel": channel,
                "category": category,
                "switch": status,
            }
        }
        response = hreq.request(env, inputs)
        assert response["result_code"] == "success"

    eu_email_not_subscribe_keys = 'case_name,category,white_app_id,recipients'
    eu_email_not_subscribe_cases = [
        ('正案例_无需订阅_验证码渠道_白名单app_id_10007', 'verify', '10007', "550736273@qq.com"),
        ('正案例_无需订阅_验证码渠道_白名单app_id_1000006', 'verify', '1000006', "550736273@qq.com"),
        ('正案例_无需订阅_验证码渠道__留资不存在', 'verify', '1000006', "maplepurple1123@163.com"),
        # ('反案例_无需订阅_验证码渠道_非白名单app_id_1000003', 'verify', '1000003', "550736273@qq.com"),
        ('正案例_无需订阅_试驾渠道_白名单app_id_1000075', 'test_drive', '1000075', "550736273@qq.com"),
        ('正案例_无需订阅_试驾渠道_留资不存在', 'test_drive', '1000075', "maplepurple1123@163.com"),
        ('正案例_无需订阅_mp_order', 'mp_order', '1000075', "maplepurple1123@163.com"),
        # ('反案例_无需订阅_试驾渠道_非白名单app_id_1000003', 'test_drive', '1000003', "550736273@qq.com"),
    ]
    eu_email_not_subscribe_ids = [f"{case[0]}" for case in eu_email_not_subscribe_cases]

    @pytest.mark.parametrize(eu_email_not_subscribe_keys, eu_email_not_subscribe_cases, ids=eu_email_not_subscribe_ids)
    def test_eu_email_not_subscribe(self, env, cmdopt, mysql, redis, case_name, category, white_app_id, recipients):
        clear_rate_limit(redis, cmdopt, 10000)
        if cmdopt not in allow_environment:
            logger.debug(f"该案例允许执行的环境为{allow_environment};不在【{cmdopt}】环境执行")
            return 0
        with allure.step(f"【{cmdopt}】环境,无需订阅{category}频道发送邮件:{case_name}"):
            http = {
                "host": env['host']['app_in'],
                "path": "/api/2/in/message/email_push",
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {
                    "region": "eu",
                    "lang": "zh-cn",
                    "hash_type": "sha256",
                    "app_id": white_app_id,
                    "sign": ""
                },
                "json": {
                    "recipients": recipients,
                    "subject": f"【{cmdopt}】环境eu_verify接口邮件:time:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}category:{category}",
                    "content": f"【{cmdopt}】环境，eu_email_push\n{case_name}",
                    "category": category,
                }
            }
            response = hreq.request(env, http)
            if case_name.startswith("反案例"):
                assert response == "Not found\n"
            else:
                assert response['result_code'] == 'success'
                assert response['data']["details"][0]["result"] == 'success', f"{response['data']['details'][0]['recipient']}邮件发送失败request_id:{response['request_id']}"
                message_id = response['data']['message_id']
                with allure.step("校验mysql"):
                    email_history = mysql['nmp_app'].fetch('email_history', {'message_id': message_id}, ['recipient'])
                    recipient_list = recipients.split(',')
                    for email_history_info in email_history:
                        assert (email_history_info['recipient'] in recipient_list) == True
                    email_content = mysql['nmp_app'].fetch('email_history_meta_info', {'message_id': message_id})
                    assert len(email_content) == 1
        with allure.step(f"【{cmdopt}】环境,清理频率限制"):
            if "test" in cmdopt:
                redis["app_message"].delete(f"rate.limiting:email_push_{white_app_id}")
                # redis["app_message"].delete(f"rate.limiting:eu/email_direct_push_{white_app_id}")

    get_switch_keys = 'case_name,channels,user_data_type'
    get_switch_cases = [
        ('正案例_', 'email', 'user_id'),
        ('正案例_', 'email', 'account_id'),
        ('正案例_', 'push', 'user_id'),
        ('正案例_', 'push', 'account_id'),
        ('正案例_', 'email,push', 'user_id'),
        ('正案例_', 'email,push', 'account_id'),
        ('正案例_', 'email,push', 'user_id,not_exist'),
        ('正案例_', 'email,push', 'account_id,not_exist'),
        ('反案例_', 'email,push', 'error_key,not_exist'),
    ]
    get_switch_ids = [f"{case[0]}{case[1]}_{case[2]}" for case in get_switch_cases]

    @pytest.mark.parametrize(get_switch_keys, get_switch_cases, ids=get_switch_ids)
    def test_get_switch(self, env, cmdopt, mysql, prepare_eu_email_account, case_name, channels, user_data_type):

        if cmdopt not in allow_environment:
            logger.debug(f"该案例允许执行的环境为{allow_environment};不在【{cmdopt}】环境执行")
            return 0
        account_msg_list = prepare_eu_email_account
        account_msg = account_msg_list[0]
        user_data = account_msg.get(user_data_type)
        if not user_data:
            user_data = '99999999'
        with allure.step(f"【{cmdopt}】环境,获取订阅开关接口{user_data_type}:{user_data}订阅{channels}渠道{case_name}"):
            inputs = {
                "host": env['host']['app_in'],
                "path": "/api/2/in/message/get_switch",
                "method": "GET",
                "headers": {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                "params": {
                    "hash_type": "sha256",
                    "channels": channels,
                    "app_id": "10007",
                    user_data_type.split(',')[0]: user_data,
                    "sign": ""
                }
            }
            response = hreq.request(env, inputs)
            if case_name.startswith("反案例"):
                assert response['result_code'] == 'invalid_param'
                assert response['debug_msg'] == 'require user_id or account_id'
            else:
                assert response['result_code'] == 'success'
                res_len = len(response['data'])
                params_keys = inputs['params'].keys()
                where_model = {"channel in": channels.split(',')}
                for key in ['user_id', 'account_id']:
                    if key in params_keys and str(inputs['params'][key]).isdigit():
                        where_model[key] = inputs['params'][key]
                with allure.step("校验mysql"):
                    switch_status = mysql['nmp_app'].fetch('notification_switch', where_model, ["count(1) as switch_status_count"])
                    mysql_len = switch_status[0]["switch_status_count"]
                    assert int(mysql_len) == res_len
                    logger.debug(switch_status)

    get_switch_list_keys = 'case_name,channels,user_id_num,except_result_code'
    get_switch_list_cases = [
        ('正案例_channels只查email', 'email', 1, "success"),
        ('正案例_channels只查push', 'push', '1', "success"),
        ('正案例_channels查email+push', 'email,push', 1, "success"),
        ('反案例_channels随便填写类型', 'not_exist', 1, "success"),
        ('正案例_100个用户', 'email,push', 100, "success"),
        ('正案例_50个用户', 'email,push', 50, "success"),
        ('反案例_101个用户', 'email,push', 101, "invalid_param"),
        ('反案例_用户不是数值类型', 'email,push', 'not_num_str', "invalid_param"),
        ('反案例_用户不存在', 'email,push', 'not_exist', "success"),
        ('正案例_部分用户不存在', 'email,push', 'part_exist', "success"),
    ]
    get_switch_list_ids = [f"{case[0]}" for case in get_switch_list_cases]

    @pytest.mark.parametrize(get_switch_list_keys, get_switch_list_cases, ids=get_switch_list_ids)
    def test_get_switch_list(self, env, cmdopt, mysql, case_name, channels, user_id_num, except_result_code):
        """
         http://showdoc.nevint.com/index.php?s=/647&page_id=30551
         channels
            * 必填
            * email
            * push
            * 数量无限制
            * channels类型无限制，随便填写无校验
         user_ids
            * 必填
            * 最多100条
            * 整型数据
            * 字符串类型异常数据会报错
        """
        """
        测试场景
            1.channels只查email
            2.channels只查push
            3.channels查email+push
            4.channels随便填写类型，可以请求成功
            5.channels填写100个以上，可以请求成功
            6.channels必填
            7.user_ids只查1个
            8.user_ids查100个
            9.user_ids查超过100个，有限制
            10.user_ids不存在，可以请求成功
            11.user_ids部分不存在，可以请求成功
            12.user_ids字符串类型异常数据会报错         
        """

        if cmdopt not in allow_environment:
            logger.debug(f"该案例允许执行的环境为{allow_environment};不在【{cmdopt}】环境执行")
            return 0
        with allure.step(f"【{cmdopt}】环境,批量获取订阅开关接口{channels}渠道{case_name}"):
            if str(user_id_num).isdigit():
                ns_in_mysql = mysql['nmp_app'].fetch('notification_switch', where_model={'user_id>': 1}, fields=['distinct user_id'], suffix=f"limit {int(user_id_num)}")
                user_ids = ','.join([str(ns.get('user_id')) for ns in ns_in_mysql])
            else:
                ns_in_mysql = mysql['nmp_app'].fetch('notification_switch', where_model={'user_id>': 1}, fields=['distinct user_id'], suffix=f"limit 10")
                user_ids = ','.join([str(ns.get('user_id')) for ns in ns_in_mysql])
                part_exist_user_ids = user_ids + ',1,2'
                user_data_map = {
                    "not_num_str": 'error_data_type',
                    "not_exist": '1,2',
                    "part_exist": part_exist_user_ids,
                    "None": None,
                }
                user_ids = user_data_map.get(user_id_num, None)
            http = {
                "host": env['host']['app_in'],
                "path": "/api/2/in/message/get_switch_list",
                "method": "GET",
                "headers": {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                "params": {
                    "channels": channels,
                    "app_id": "10007",
                    "user_ids": user_ids,
                    "sign": ""
                }
            }
            response = hreq.request(env, http)
            assert response['result_code'] == except_result_code
            if case_name.startswith("正案例"):
                with allure.step("校验mysql"):
                    assert response['result_code'] == 'success'
                    res_len = len(response['data'])
                    channel_list = channels.split(',')
                    switch_status = mysql['nmp_app'].fetch('notification_switch', {'user_id in': user_ids.split(','), "channel in": channel_list},
                                                           ["count(1) as switch_status_count"])
                    mysql_len = switch_status[0]["switch_status_count"]
                    assert int(mysql_len) == res_len
                    logger.debug(switch_status)

    push_eu_email_keys = 'case_name,category,status,user_data_type'
    push_eu_email_cases = [
        ('正案例_根据user_id订阅fellow_contact后发送邮件', 'fellow_contact', True, 'user_id'),
        ('正案例_根据user_id订阅marketing_email后发送邮件', 'marketing_email', True, 'user_id'),
        ('正案例_根据account_id订阅fellow_contact后发送邮件', 'fellow_contact', True, 'account_id'),
        ('正案例_根据account_id订阅marketing_email后发送邮件', 'marketing_email', True, 'account_id'),
        ('正案例_根据recipients订阅fellow_contact后发送邮件', 'fellow_contact', True, 'recipient'),
        ('正案例_根据recipients订阅marketing_email后发送邮件', 'marketing_email', True, 'recipient'),
        ('正案例_根据user_id取消fellow_contact订阅后发送邮件', 'fellow_contact', True, 'user_id'),
        ('正案例_根据account_id取消fellow_contact订阅后发送邮件', 'fellow_contact', False, 'account_id'),
        ('正案例_根据recipient取消fellow_contact订阅后发送邮件', 'fellow_contact', False, 'recipient'),
        ('正案例_根据user_id取消marketing_email订阅后发送邮件', 'marketing_email', False, 'user_id'),
        ('正案例_根据account_id取消marketing_email订阅后发送邮件', 'marketing_email', False, 'account_id'),
        ('正案例_根据recipient取消marketing_email订阅后发送邮件', 'marketing_email', False, 'recipient'),
        ('正案例_根据account_id订阅service_email后发送邮件', 'service_email', True, 'account_id'),
        ('正案例_根据recipient订阅order_email后发送邮件', 'order_email', True, 'recipient'),
        ('正案例_根据user_id订阅order_email后发送邮件', 'order_email', True, 'user_id'),
        ('正案例_根据account_id订阅order_email后发送邮件', 'order_email', True, 'account_id'),
    ]
    push_eu_email_ids = [f"{case[0]}" for case in push_eu_email_cases]

    @pytest.mark.parametrize(push_eu_email_keys, push_eu_email_cases, ids=push_eu_email_ids)
    def test_push_eu_email(self, env, cmdopt, mysql, redis, prepare_eu_email_account, case_name, category, status, user_data_type):
        """
        1.银龙存在为True，消息平台存在为True
        2.银龙存在为True，消息平台不存在
        3.银龙不存在，消息平台存在为True
        4.银龙不存在，消息平台不存在
        5.银龙存在为False，消息平台存在为True
        6.银龙存在为False，消息平台存在为False
        7.银龙存在为True，消息平台存在为False
        """
        #
        app_id = 10007
        if cmdopt not in allow_environment:
            logger.debug(f"该案例允许执行的环境为{allow_environment};不在【{cmdopt}】环境执行")
            return 0
        with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
            if "test" in cmdopt:
                redis["app_message"].delete(f"rate.limiting:email_push_{app_id}")
        account_msg_list = prepare_eu_email_account
        account_msg = account_msg_list[2] if category == 'order_email' or category == 'service_email' else account_msg_list[0]
        user_data = account_msg.get(user_data_type)
        user_id = account_msg.get("user_id")
        recipient = account_msg.get("recipient")
        if category not in ('service_email', 'order_email'):
            self.set_switch(env, 'email', category, user_id, status)
        path = "/api/2/in/message/email_push"
        inputs = {
            "host": env['host']['app_in'],
            "path": path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "region": "eu",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": app_id,
                "sign": ""
            },
            "json": {
                f"{user_data_type}s": user_data,
                "subject": f"{cmdopt}time:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}category:{category}",
                "content": f"{case_name}, {category}, {status}",
                "category": category,
            }
        }
        response = hreq.request(env, inputs)

        assert response['result_code'] == 'success'
        if status:
            assert response['data']["details"][0]["result"] == 'success'
        else:
            assert response['data']["details"][0]["result"] == 'not_subscribe'
        response.pop("request_id")
        response.pop("server_time")
        message_id = response["data"].pop("message_id")
        if status:
            # 订阅返回结果
            expected_response = {
                "data": {
                    "details": [{f"{user_data_type}": user_data, "result": "success"}],
                    "success": 1,
                    "failure": 0,
                },
                "result_code": "success",
            }
            assert_equal(response, expected_response)
            expected_states = [21, 22, 23, 24, 26]
            ms_st = f"{message_id}|{expected_states}|{path}"
            collection_message_states(cmdopt, ms_st)
            with allure.step("校验mysql"):
                email_history = mysql['nmp_app'].fetch('email_history', {'message_id': message_id}, ['recipient'])
                recipient_list = recipient.split(',')
                for email_history_info in email_history:
                    assert (email_history_info['recipient'] in recipient_list) == True
                email_content = mysql['nmp_app'].fetch('email_history_meta_info', {'message_id': message_id})
                assert len(email_content) == 1
        else:
            # 未订阅返回结果
            expected_response = {
                "data": {
                    "details": [{f"{user_data_type}": user_data, "result": "not_subscribe", "reason": f"user do not subscribe the category:{category}"}],
                    "success": 0,
                    "failure": 1,
                },
                "result_code": "success",
            }
            assert_equal(response, expected_response)

    push_eu_email_batch_keys = 'case_name,category,status_list,user_data_type,user_number'
    push_eu_email_batch_cases = [
        # ('正案例_根据user_id同时推送2个订阅', 'fellow_contact', [True, True], 'user_id', 2),
        ('正案例_根据user_id同时推送2个订阅', 'marketing_email', [True, True], 'user_id', 2),
        # ('正案例_根据account_id同时推送2个订阅', 'fellow_contact', [True, True], 'account_id', 2),
        # ('正案例_根据account_id同时推送2个订阅', 'marketing_email', [True, True], 'account_id', 2),
        # ('正案例_根据recipients同时推送2个订阅', 'fellow_contact', [True, True], 'recipient', 2),
        # ('正案例_根据recipients同时推送2个订阅', 'marketing_email', [True, True], 'recipient', 2),
        # ('反案例_根据user_id同时推送2个未订阅', 'fellow_contact', [False, False], 'user_id', 2),
        # ('反案例_根据user_id同时推送3个1个订阅1个未订阅,1个非邮箱格式', 'fellow_contact', [True, False, "error_format"], 'account_id', 3),
        # ('反案例_根据user_id同时推送3个1个订阅1个未订阅,1个非邮箱格式', 'fellow_contact', [True, False, "error_format"], 'user_id', 3),
        # ('反案例_根据user_id同时推送3个1个订阅1个未订阅,1个非邮箱格式', 'fellow_contact', [True, False, "error_format"], 'recipient', 3),
        # ('反案例_根据user_id同时推送3个非邮箱格式', 'fellow_contact', ["error_format", "error_format", "error_format"], 'recipient', 3),
        # ('反案例_根据user_id推送1个非邮箱格式', 'fellow_contact', ["error_format"], 'recipient', 1),
    ]
    push_eu_email_batch_ids = [f"{case[0]}" for case in push_eu_email_batch_cases]

    @pytest.mark.parametrize(push_eu_email_batch_keys, push_eu_email_batch_cases, ids=push_eu_email_batch_ids)
    def test_push_eu_email_batch(self, env, cmdopt, mysql, redis, prepare_eu_email_account, case_name, category, status_list, user_data_type, user_number):

        send_failure_reason_map = {"user_id": "user id or email not exist", "account_id": "account id or email not exist", "recipient": "the recipient does not match rgex"}
        if cmdopt not in allow_environment:
            logger.debug(f"该案例允许执行的环境为{allow_environment};不在【{cmdopt}】环境执行")
            return 0
        account_msg_list = prepare_eu_email_account
        user_data, recipients, expected_details, expected_success, expected_failure, recipients_status = '', '', [], 0, 0, {}
        for i in range(user_number):
            account_msg = account_msg_list[i]
            status = status_list[i]
            recipients_status[account_msg.get('recipient')] = status
            random_int_str = random_int(8)
            if status == "error_format":
                if user_data:
                    user_data = user_data + ',' + random_int_str
                else:
                    user_data = str(random_int_str)
            else:
                if user_data:
                    user_data = user_data + ',' + account_msg.get(user_data_type)
                else:
                    user_data = account_msg.get(user_data_type)
            recipients = recipients + account_msg.get('recipient') + ','
            user_id = account_msg.get('user_id')
            self.set_switch(env, 'email', category, user_id, status)
            if status:
                if status == "error_format":
                    expected_details.append({f"{user_data_type}": random_int_str, "result": f"invalid_{user_data_type}",
                                             "reason": send_failure_reason_map.get(user_data_type)})
                    expected_failure = expected_failure + 1
                else:
                    expected_details.append({f"{user_data_type}": account_msg.get(user_data_type), "result": "success"})
                    expected_success = expected_success + 1
            else:
                expected_details.append(
                    {f"{user_data_type}": account_msg.get(user_data_type), "result": "not_subscribe", "reason": f"user do not subscribe the category:{category}"})
                expected_failure = expected_failure + 1
        expected_response = {
            "data": {
                # 多个值根据用户值进行排序
                "details": sorted(expected_details, key=lambda x: x[user_data_type], reverse=True),
                "success": expected_success,
                "failure": expected_failure,
            },
            "result_code": "success",
        }
        app_id = 10007
        path = "/api/2/in/message/email_push"
        inputs = {
            "host": env['host']['app_in'],
            "path": path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "region": "eu",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": app_id,
                "sign": ""
            },
            "json": {
                f"{user_data_type}s": user_data,
                "subject": f"{cmdopt}time:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}category:{category}",
                "content": f"{html5}",
                "category": category,
            }
        }
        with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
            if "test" in cmdopt:
                redis["app_message"].delete(f"rate.limiting:eu/email_push_{app_id}")
        response = hreq.request(env, inputs)
        assert response['result_code'] == 'success'
        assert response['data']["details"][0]["result"] == 'success', f"{response['data']['details'][0]['recipient']}邮件发送失败request_id:{response['request_id']}"
        response.pop("request_id")
        response.pop("server_time")
        message_id = response["data"].pop("message_id")
        details = response["data"]['details']
        response["data"]['details'] = sorted(details, key=lambda x: x[user_data_type], reverse=True)
        assert_equal(response, expected_response)
        recipient_list = recipients.split(',')
        for recipient in recipient_list:
            recipient_status = recipients_status.get(recipient)
            if recipient_status and recipient_status != "error_format":
                # 订阅返回结果
                expected_states = [21, 22, 23, 24, 26]
                ms_st = f"{message_id}|{expected_states}|{path}"
                collection_message_states(cmdopt, ms_st)
                with allure.step("校验mysql"):
                    email_history = mysql['nmp_app'].fetch('email_history', {'message_id': message_id, 'recipient': recipient})
                    assert len(email_history) == 1
                    email_content = mysql['nmp_app'].fetch('email_history_meta_info', {'message_id': message_id})
                    assert len(email_content) == 1


def test_get_user_is(env):
    """
        接口文档：http://showdoc.nevint.com/index.php?s=/636&page_id=29860
        留资user那边可以根据app_id来配置返回字段，
        message_center的app_id=10022
        可以根据account_ids,user_ids,emails来查询用户列表
        123449046,169261665
    """
    # user_ids = "110342461,140079227"
    account_ids = "1018777684,1012879849"
    host = env['host']['zeus_in']
    inputs = {
        "host": host,
        "path": "/zeus/in/user/v1/users",
        "method": "GET",
        "params": {
            "hash_type": "sha256",
            "account_ids": account_ids,
            # "user_ids": user_ids,
            # "emails": "550736273@qq.com,842244250@qq.com,",
            "app_id": "10022",
            "offset": 0,
            "count": 50,
            "sign": ""
        }
    }
    response = hreq.request(env, inputs)
    logger.debug(response)
    assert response['result_code'] == 'success'
    user_data_list = response['data']['list']
    if user_data_list:
        return user_data_list[0]['user_id']
    else:
        return False


def register_email_zeus(env, cmdopt):
    """
    该方法用于创建留资账号，账号数据写入文件并返回list
    """
    file_path = f'{BASE_DIR}/config/{cmdopt}/email_account_info_{cmdopt}.txt'
    if os.path.exists(file_path):
        os.remove(file_path)
    list_account = []
    for email in ["550736273@qq.com", "842244250@qq.com", "maplepurple1123@163.com"]:
        host = 'http://10.110.3.103:5000'
        api = '/pangu/email_register_zeus'
        inputs = {
            "host": host,
            "method": 'POST',
            "path": api,
            "headers": {'Content-Type': 'application/json'},
            "json": {
                "nick_name": f"evm_{cmdopt}_{random_string(6)}",
                "email": email,
                "env": cmdopt
            }
        }
        res_dict = hreq.request(env, inputs)
        if res_dict.get('result_code') == "success":
            logger.debug(res_dict)
            data = res_dict.get('data')
            res_account_msg = data.get("account_register_info")
            account_id = res_account_msg.get('account_id')
            user_id = data.get("user").get("user_id")
            email = data.get("email")
            password = data.get("password")
            pseudo_email = data.get("pseudo_email")
            email_account_info = f"{account_id},{user_id},{email},{password},{pseudo_email},{res_account_msg.get('create_time')}"
            res_msg = {"account_id": account_id, "user_id": user_id, "recipient": email, "password": password, "pseudo_email": pseudo_email}
            list_account.append(res_msg)
            with open(file_path, 'a+')as f:
                logger.debug(email_account_info)
                f.write(f'{email_account_info}\n')
    return list_account
