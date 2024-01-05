# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_message_push.py
# @Author : qiangwei.zhang.o
# @CreateTime : 2021/2/26 10:52 上午
# @Description :

import json
import pytest
import random
import string
from utils.logger import logger
from data.email_content import long_text, html5, markdown_file_title, markdown_file_font, markdown_file_url, markdown_file_img, markdown_file_form, markdown_file_emoji
import time

"""
    push_email: swc-cvs-nmp-eu-test-push-email # app_message邮件推送
      push_mi: swc-cvs-nmp-eu-test-push-mi # app_message小米推送
      push_apns: swc-cvs-nmp-eu-test-push-apns # app_message苹果推送
      push_hw: swc-cvs-nmp-eu-test-push-hw # app_message华为推送
      push_fcm: swc-cvs-nmp-eu-test-push-fcm # app_message谷歌推送
      push_feishu: swc-cvs-nmp-eu-test-push-feishu # app_message谷歌推送  
"""

cn_push_email = "swc-cvs-nmp-cn-test-push-email"  # app_message邮件推送
cn_push_mi = "swc-cvs-nmp-cn-test-push-mi"  # app_message小米推送
cn_push_apns = "swc-cvs-nmp-cn-test-push-apns"  # app_message苹果推送
cn_push_hw = "swc-cvs-nmp-cn-test-push-hw"  # app_message华为推送
cn_push_fcm = "swc-cvs-nmp-cn-test-push-fcm"  # app_message谷歌推送
cn_push_sms = "swc-cvs-nmp-cn-test-push-sms"  # 短信推送
cn_push_fei_shu = "swc-cvs-nmp-cn-test-push-feishu"  # 短信推送

eu_push_email = "swc-cvs-nmp-eu-test-push-email"  # app_message邮件推送
eu_push_mi = "swc-cvs-nmp-eu-test-push-mi"  # app_message小米推送
eu_push_apns = "swc-cvs-nmp-eu-test-push-apns"  # app_message苹果推送
eu_push_hw = "swc-cvs-nmp-eu-test-push-hw"  # app_message华为推送
eu_push_fcm = "swc-cvs-nmp-eu-test-push-fcm"  # app_message谷歌推送
eu_push_sms = "swc-cvs-nmp-eu-test-push-sms"  # 短信推送
eu_push_fei_shu = "swc-cvs-nmp-eu-test-push-feishu"  # 短信推送


# @pytest.mark.skip("manual")
class TestMessagePushByKafka(object):
    push_email_kafka_eu_keys = "case_name,sender_name,recipient,push_time,ttl"
    push_email_kafka_eu_cases = [
        ("正案例_能收到_当前时间_超时时间1000", "notification@nio.com", "qiangwei.zhang@nio.com", int(time.time()), 1000),
        ("反案例_无法收到_当前时间减1000_超时时间100", "notification@nio.com", "qiangwei.zhang@nio.com", int(time.time()) - 1000, 100),
    ]
    push_email_kafka_eu_ids = [f"{case[0]}" for case in push_email_kafka_eu_cases]

    @pytest.mark.parametrize(push_email_kafka_eu_keys, push_email_kafka_eu_cases, ids=push_email_kafka_eu_ids)
    def test_push_email_kafka_eu(self, cmdopt, vid, kafka, case_name, sender_name, recipient, push_time, ttl):
        '''
        通过kafka渠道发送邮件
        工单详情：http://venus.nioint.com/#/detailWorkflow/wf-20210226104943-0Hmessage
            push 测试邮件推送，发送kafka topic swc-cvs-nmp-cn-test-push-email即可（cvs集群）
                内容为json格式:json.dumps({"recipient":"qiangwei.zhang@nio.com","subject":"Nio Test Subject","content":"","priority":1,"batch":false})
                    recipient:邮箱（必填）
                    subject:邮件主题（必填）
                    content:内容（支持文本以及html）（必填）
                    priority:优先级（1，2）1最高（非必填）
                    batch:批量发送开关（非必填）
        手动检查邮箱是否收到邮件
        测试场景：
            1.单个收件人
            2.多个收件人
            3.多个收件人中有重复数据（同一个邮箱去重逻辑，会加到message_center）
            4.邮箱通过","分割
            5.邮件内容为text
            6.邮件内容为html
            7.邮件内容为html+text
            8.格式错误的数据
        疑问点确认：
            1.批量发送邮箱是否有数量限制 (未加限制)
            2.邮件内容的长度（无限制）
            3.是否支持传附件（不支持）
            4.上游的调用方（message_center我们自己么，后续会提供api供其他系统调用）
            5.发送和接收邮件有持久化的数据么（该版本无记录）
            6.priority:优先级（1，2）1最高 batch:批量发送开关，该版本是否有业务逻辑上的判断分支（保留字段后续会使用，该版本未使用）
            7.支持的邮箱类型（无限制）
        '''
        nio_email = "qiangwei.zhang@nio.com"
        category = "marketing_email"  # marketing_email, verify, fellow_contact
        sender_name = "notification@nio.io"  # tsp@nioint.com和notification@nio.com
        message_id = f"9ccc22d4-792e-4a2d-9070-dbca7{random.randint(0, 1000000)}"
        value = json.dumps(
            {
                "recipient": nio_email,
                "sender_name": sender_name,
                "message_id": message_id,
                "subject": f"【{cmdopt}】环境kafka推送邮件push_email_kafka_eu。时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "content": "kafka push email test",
                "category": category,
                "priority": 1,
                "push_time": push_time,
                "ttl": ttl,
                "batch": True
            }
        )
        kafka['cvs'].produce(kafka['topics']['push_email'], value)

        # for data in kafka['cvs'].consume(kafka['topics']['push_email'], timeout=10):
        #     logger.debug(f"consume_content:{data}")

    def test_fcm_push_kafka_eu(self, cmdopt, vid, kafka):
        title = f"蔚来【{cmdopt}】 fcm push test"
        description = f"蔚来【{cmdopt}】环境kafka推送fcm_push{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
        message_id = f"9ccc22d4-792e-4a2d-9070-dbca7{random.randint(0, 1000000)}"
        """
        "account_id": "1006908429",
        "email": "EU.fe.512@ni.dt.ac.fe.ss",
        "password": "pan_gu@123456",
        "verification_code": "456792"
        ""
        """
        client_id = "ChBSR9vFo3XBOwmTru8cBCnxEAEYkJZ8IMSEPSgB"
        token_stg = "cm9LK_DrRDaATtt96i5H37:APA91bFa0I0ZUtarSIySVfwoRpcc-vms71jQvfXRAohASEC1JNEBaysJcH7RLklW3RTdFQTQ8hfEEn0pqqOSJF8KaqIuHZephcwykSOxNUxSFTSs3mIWJ_UY-vjYd3f8-eDpSmiGdl3T"
        value = json.dumps(
            {
                "client_list": [
                    # {"client_id": "ChAHSmqGrajjG7UlkGW5p0lMEAEY8M0IIJFOKAE\u003d",
                    #  "device_token": "cWSMI4rgTZicIau6nyGyT0:APA91bFLqgBnTXgC292R5LuLBmepmjNWMnoSLxyp11g9dsyNb1Pct_OaWTY9fRKBpNp8sI2E1j1cpGf_-3rvkDojIoPd_WbJz_TTyGuMIeXa71TRbvSsU1fMjEgMmfkht3meOIPByEhp",
                    #  "app_id": "1000003"
                    #  },
                    {"client_id": client_id,
                     "device_token": token_stg,
                     "app_id": "1000003"
                     }
                ],
                "scenario": "ls_system",  # 消息通知的场景
                "title": title,  # 消息通知的标题
                "description": description,  # 消息通知的内容
                "retry": 3,  # 重发次数。如果apns接口没有返回，则重新入队进行重发，如果apns返回类似bad device token，则不会重发。
                "push_time": int(time.time()),  # 苹果apns接口定义的一个字段。设定消息的过期时间
                "ttl": 10000,  # 苹果apns接口定义的一个字段。设定消息的过期时间
                "passThrough": 0,  # 值为1即透传。是苹果apns接口定义的一个字段。消息内容能照常发给手机应用，只是手机端不做显示。这个控制都是由苹果完成。
                "payload_map": {
                    "scenario": "ls_system",
                    "description": description,
                    "message_id": message_id,
                    "title": title
                },
                "message_id": message_id,  # 服务内存里会记录消息数据以给多个client发送时的减少计算量，根据message_id进行索引，如果发送的消息mesage_id不变，则一直是原来的老消息。
                # "priority": 2,  # 优先级（1，2）1最高，优先级高的会放在优先队列里发送
                # "batch": False  # 保留字段，批量发送的开关。目前(2021/5/17)没逻辑
            })
        kafka['cvs'].produce(kafka['topics']['push_fcm'], value)

    push_fei_shu_kafka_eu_keys = "case_name,sender_name,recipient,push_time,ttl"
    push_fei_shu_kafka_eu_cases = [
        ("正案例_能收到_当前时间_超时时间1000", "cn", 'qiangwei.zhang@nio.com', int(time.time()), 1000),
        ("反案例_无法收到_当前时间减1000_超时时间100", "cn", 'qiangwei.zhang@nio.com', int(time.time()) - 1000, 100),
    ]
    push_fei_shu_kafka_eu_ids = [f"{case[0]}" for case in push_fei_shu_kafka_eu_cases]

    @pytest.mark.parametrize(push_fei_shu_kafka_eu_keys, push_fei_shu_kafka_eu_cases, ids=push_fei_shu_kafka_eu_ids)
    def test_fei_shu_push_kafka_eu(self, cmdopt, kafka, case_name, sender_name, recipient, push_time, ttl):
        # sender_name 马克波罗环境和，国内推送使用同一个topic，根据sender_name区分走不同的配置
        title = f"{cmdopt}飞书kafka推送{sender_name}时间:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
        url = "https://nio.feishu.cn/docs/doccntRo2MGjg51qDbQ0xgFEh0g"
        image_key = "img_v2_d4b2d692-8066-4202-b1b4-7b6418d6d0fg"
        content = f"*{case_name}*\n**蔚来ET7荣获2021年红点奖**\n[nio](https://www.nio.cn/)\n![picture]({image_key})\n"
        # content = markdown_file_title + markdown_file_font + markdown_file_url + markdown_file_img + markdown_file_form + markdown_file_emoji
        # content = "普通文本\n标准emoji 😁😢🌞💼🏆❌✅\n*斜体*\n**粗体**\n~~删除线~~\n[文字链接](https://www.feishu.cn)\n<at id=all></at>\n ---\n上面是一行分割线\n![光标hover图片上的tips文案可不填](img_v2_d4b2d692-8066-4202-b1b4-7b6418d6d0fg)\n上面是一个图片标签"
        message_id = f"9ccc22d4-792e-4a2d-9070-dbca7{random.randint(0, 1000000)}"
        value = json.dumps(
            {
                "recipient": recipient,
                "title": title,
                "content": content,
                "url": url,
                "sender_name": sender_name,
                "message_id": message_id,
                "push_time": push_time,
                "ttl": ttl,
                "priority": 2,
                "batch": False
            }
        )
        kafka['cvs'].produce(kafka['topics']['push_feishu'], value)

    def test_apns_push_kafka_eu(self, cmdopt, kafka):
        """
        测试case
        1.校验给单个用户发送消息，iphone 手机能收到消息。
        2.校验给多个个用户发送消息，多台iphone 手机能收到消息
        3.校验message_id不变时，发送的消息还是原来的消息，message_id变更时，发送的消息是最新的消息
        4.校验passThrough=1（透传）时，手机不显示消息。
        5.校验优先级高的消息会优先发送。（kafka消费后会将消息放到优先队列中）

        注意：
        1.每次发消息时，须修改meesage_id
        2. passThrough须为0，否则手机端不显示通知

        """
        title = f"蔚来【{cmdopt}】 apns push test"
        description = f"蔚来【{cmdopt}】环境kafka推送apns_push{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
        message_id = f"9ccc22d4-792e-4a2d-9070-dbca7{random.randint(0, 1000000)}"
        token = "98a100822fd37b9241f0f789f57bc40aacd798b0f226755ceb174aff86448971"
        value = json.dumps(
            {
                "client_list": [
                    {"client_id": "ChAu9tpoFfXwdURtgj91p9p6EAEY2eAHIJJOKAA=",
                     # "device_token": "b598e6d3d3a28e601223d062830fac18d440ae00e0f232b37ea0aa35e987801f",  # 手机是否能收到消息，关键在于device_token需要写对
                     "device_token": token,  # 手机是否能收到消息，关键在于device_token需要写对
                     "app_id": "1000003"
                     }
                ],
                "scenario": "ls_system",  # 消息通知的场景
                "title": title,  # 消息通知的标题
                "description": description,  # 消息通知的内容
                "retry": 0,  # 重发次数。如果apns接口没有返回，则重新入队进行重发，如果apns返回类似bad device token，则不会重发。
                "ttl": 10000,  # 苹果apns接口定义的一个字段。设定消息的过期时间
                "push_time": int(time.time()),  # 苹果apns接口定义的一个字段。设定消息的过期时间
                "passThrough": 0,  # 值为1即透传。是苹果apns接口定义的一个字段。消息内容能照常发给手机应用，只是手机端不做显示。这个控制都是由苹果完成。
                "payload_map": {
                    "scenario": "ls_system",
                    "description": description,
                    "message_id": message_id,
                    "title": title
                },
                "message_id": message_id,  # 服务内存里会记录消息数据以给多个client发送时的减少计算量，根据message_id进行索引，如果发送的消息mesage_id不变，则一直是原来的老消息。
                "priority": 2,  # 优先级（1，2）1最高，优先级高的会放在优先队列里发送
                "batch": False  # 保留字段，批量发送的开关。目前(2021/5/17)没逻辑
            })
        kafka['cvs'].produce(kafka['topics']['push_apns'], value)

    def test_mi_push_kafak_batch_eu(self, cmdopt, kafka):
        """
        测试case
        1.校验给单个用户发送消息，小米 手机能收到消息。
        2.校验给多个用户发送消息，多台小米 手机能收到消息
        3.校验passThrough=1（透传）时，手机不显示消息

        注意：
        1.每次发消息时，须修改meesage_id
        2. passThrough须为0，否则手机端不显示通知

        """
        title = f"蔚来【{cmdopt}】环境kafka推送mi_push{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
        description = f"蔚来【{cmdopt}】环境kafka推送mi_push测试"
        message_id = f"9ccc22d4-792e-4a2d-9070-dbca7{random.randint(0, 1000000)}"

        value = json.dumps(
            {
                "client_list": [
                    # 98762751645手机号  581210316用户ID TEST环境 依依
                    {"client_id": "ChCebvA33QG-N39lgEPiS0EEEAEY8dQIIJFOKAE=",
                     "device_token": "6iX7x1pAKrMmxY2vBa9qytMMkCYiYEW02W8bPCoMOWgg8nUs8nIndGAegVAU5Efu",  # 手机是否能收到消息，关键在于device_token需要写对
                     "app_id": "10001"
                     },
                    # 98762754808手机号  14967171用户ID TEST环境 自己
                    {
                        "client_id": "ChBAnWVNUYcCm5_AjcWgls4lEAEY78EIIJFOKAE=",
                        "device_token": "EJhhxUbCxgQ2Z0SVa78SztRFvTQ0vZyvD7gA/qTFi8LdlOBjPaGWrBcwZovOy4wm",
                        "app_id": "10001",
                        "user_id": 14967171
                    },
                ],
                "scenario": "ls_system",  # 消息通知的场景
                "title": title,  # 消息通知的标题
                "description": description,  # 消息通知的内容
                "retry": 0,  # 重发次数。如果apns接口没有返回，则重新入队进行重发，如果apns返回类似bad device token，则不会重发。
                "ttl": 10000,  # 苹果apns接口定义的一个字段。设定消息的过期时间
                "passThrough": 1,  # 值为1即透传。是苹果apns接口定义的一个字段。消息内容能照常发给手机应用，只是手机端不做显示。这个控制都是由苹果完成。
                "payload_map": {
                    "scenario": "ls_system",
                    "description": description,
                    "message_id": message_id,
                    "title": title
                },
                "message_id": message_id,  # 服务内存里会记录消息数据以给多个client发送时的减少计算量，根据message_id进行索引，如果发送的消息mesage_id不变，则一直是原来的老消息。
                "priority": 2,  # 优先级（1，2）1最高，优先级高的会放在优先队列里发送
                "batch": False  # 保留字段，批量发送的开关。目前(2021/5/17)没逻辑
            })
        kafka['cvs'].produce(kafka['topics']['push_mi'], value)

    def test_mi_push_kafak_eu(self, cmdopt, kafka):
        """
        测试case
        1.校验给单个用户发送消息，小米 手机能收到消息。
        2.校验给多个个用户发送消息，多台小米 手机能收到消息
        3.校验passThrough=1（透传）时，手机不显示消息

        注意：
        1.每次发消息时，须修改meesage_id
        2. passThrough须为0，否则手机端不显示通知

        """
        title = f"蔚来【{cmdopt}】环境kafka推送mi_push{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
        description = f"蔚来【{cmdopt}】环境kafka推送mi_push测试"
        message_id = f"9ccc22d4-792e-4a2d-9070-dbca7{random.randint(0, 1000000)}"

        value = json.dumps(
            {
                "client_list": [
                    # 98762754808手机号  14967171用户ID TEST环境 自己
                    {"client_id": "ChBAnWVNUYcCm5_AjcWgls4lEAEY78EIIJFOKAE=",
                     "device_token": "EJhhxUbCxgQ2Z0SVa78SztRFvTQ0vZyvD7gA/qTFi8LdlOBjPaGWrBcwZovOy4wm",
                     "app_id": "10001"
                     },
                ],
                "scenario": "ls_system",  # 消息通知的场景
                "title": title,  # 消息通知的标题
                "description": description,  # 消息通知的内容
                "retry": 0,  # 重发次数。如果apns接口没有返回，则重新入队进行重发，如果apns返回类似bad device token，则不会重发。
                "ttl": 10000,  # 苹果apns接口定义的一个字段。设定消息的过期时间
                "passThrough": 0,  # 值为1即透传。是苹果apns接口定义的一个字段。消息内容能照常发给手机应用，只是手机端不做显示。这个控制都是由苹果完成。
                "payload_map": {
                    "scenario": "ls_system",
                    "description": description,
                    "message_id": message_id,
                    "title": title},
                "message_id": message_id,  # 服务内存里会记录消息数据以给多个client发送时的减少计算量，根据message_id进行索引，如果发送的消息mesage_id不变，则一直是原来的老消息。
                "priority": 2,  # 优先级（1，2）1最高，优先级高的会放在优先队列里发送
                "batch": False  # 保留字段，批量发送的开关。目前(2021/5/17)没逻辑
            })
        kafka['cvs'].produce(kafka['topics']['push_mi'], value)

    def test_hw_push_kafak_eu(self, cmdopt, kafka):
        """
        注意：
        1.每次发消息时，须修改 message_id
        2. passThrough须为0，否则手机端不显示通知

        """
        title = f"蔚来【{cmdopt}】kafka hw push test"
        account_id = 449726622
        description = f"蔚来【{cmdopt}】环境kafka推送hw_push,account_id:{account_id};time{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
        message_id = f"9ccc22d4-792e-4a2d-9070-dbca7{random.randint(0, 1000000)}"
        value = json.dumps(
            {
                "client_list": [
                    {"client_id": "ChDuMX705TTGNBUlwEQvJ-nJEAEY4OIIIJFOKAE=",
                     "device_token": "IQAAAACy0Pr_AAAXCZYbbhs1bsWSfxGg8IBFnxHAwriLwd-LSZ5Ns2_2rx1wVfu28NXQ3KdxIgHfqqJApTlrfn-_ZDqC7S1WHE5BFxuKFraCu9bf7w",
                     # 手机是否能收到消息，关键在于device_token需要写对
                     "app_id": "10001"
                     }
                ],
                "scenario": "ls_system",  # 消息通知的场景
                "title": title,  # 消息通知的标题
                "description": description,  # 消息通知的内容
                "retry": 3,  # 重发次数。如果apns接口没有返回，则重新入队进行重发，如果apns返回类似bad device token，则不会重发。
                "ttl": 10000,  # 设定消息的过期时间
                "push_time": int(time.time()),
                "passThrough": 0,  # 值为1即透传。是苹果apns接口定义的一个字段。消息内容能照常发给手机应用，只是手机端不做显示。这个控制都是由苹果完成。
                "payload_map": {
                    "scenario": "ls_system",
                    "description": description,
                    "message_id": message_id,
                    "title": title
                },
                "message_id": message_id,  # 服务内存里会记录消息数据以给多个client发送时的减少计算量，根据message_id进行索引，如果发送的消息mesage_id不变，则一直是原来的老消息。
                "priority": 2,  # 优先级（1，2）1最高，优先级高的会放在优先队列里发送
                "batch": False  # 保留字段，批量发送的开关。目前(2021/5/17)没逻辑
            })
        kafka['cvs'].produce(kafka['topics']['push_hw'], value)

    def test_hw_push_kafak_eu_stg(self, cmdopt, kafka):
        """
        注意：
        1.每次发消息时，须修改 message_id
        2. passThrough须为0，否则手机端不显示通知

        """
        title = f"蔚来【{cmdopt}】kafka hw push test"
        account_id = 131586927  # 手机号:98762489569验证码:120670
        description = f"蔚来【{cmdopt}】环境kafka推送hw_push,account_id:{account_id};time{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
        message_id = f"9ccc22d4-792e-4a2d-9070-dbca7{random.randint(0, 1000000)}"
        value = json.dumps(
            {
                "client_list": [
                    {"client_id": "ChC4_IBCMzDs__PcGWrC2ATaEAEYvc57IJFOKAE=",
                     "device_token": "IQAAAACy0Pr_AAAXCZYbbhs1bsWSfxGg8IBFnxHAwriLwd-LSZ5Ns2_2rx1wVfu28NXQ3KdxIgHfqqJApTlrfn-_ZDqC7S1WHE5BFxuKFraCu9bf7w",
                     # 手机是否能收到消息，关键在于device_token需要写对
                     "app_id": "10001"
                     }
                ],
                "scenario": "ls_system",  # 消息通知的场景
                "title": title,  # 消息通知的标题
                "description": description,  # 消息通知的内容
                "retry": 3,  # 重发次数。如果apns接口没有返回，则重新入队进行重发，如果apns返回类似bad device token，则不会重发。
                "ttl": 10000,  # 设定消息的过期时间
                "push_time": int(time.time()),
                "passThrough": 0,  # 值为1即透传。是苹果apns接口定义的一个字段。消息内容能照常发给手机应用，只是手机端不做显示。这个控制都是由苹果完成。
                "payload_map": {
                    "scenario": "ls_system",
                    "description": description,
                    "message_id": message_id,
                    "title": title
                },
                "message_id": message_id,  # 服务内存里会记录消息数据以给多个client发送时的减少计算量，根据message_id进行索引，如果发送的消息mesage_id不变，则一直是原来的老消息。
                "priority": 2,  # 优先级（1，2）1最高，优先级高的会放在优先队列里发送
                "batch": False  # 保留字段，批量发送的开关。目前(2021/5/17)没逻辑
            })
        kafka['cvs'].produce(kafka['topics']['push_hw'], value)
