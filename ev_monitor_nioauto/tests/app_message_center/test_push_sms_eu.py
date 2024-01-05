# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_push_sms.py
# @Author : qiangwei.zhang.o
# @CreateTime : 2021/3/23 11:02 上午
# @Description :
"""
E.164是国际电信联盟定义的在PSTN和一些数据网使用的国际公共电话码号方案，同时定义了具体的码号的格式。E.164定义了最大15数字，完整号码有国际呼叫前缀。
E.164号码是MSISDN号码，它是主叫用户为呼叫移动通信网中用户所需拨号的号码。
其格式为：CC+NDC+SN，也可以表示为：国家代码+N1N2N3+H0H1H2H3＋ABCD
（CC=国家码，中国为86；NDC=国内目的码；SN=用户号码）

{"verify_notification@nio.io":{"host":"smtp.office365.com","port":"587","user_name":"notification@nio.io","password":"NCpwr281fiR7","properties":{"mail.smtp.starttls.required":"ture","mail.smtp.auth":"true","mail.smtp.starttls.enable":"true"}},"notification@nio.io":{"host":"email-smtp.eu-central-1.amazonaws.com","port":"587","user_name":"AKIAUZKWFNV4XNSMRVP2","password":"BJucOLEcDQ1f5fyDM6mmfXlo3TVPtjIPcN1VHp05jFTV","properties":{"mail.smtp.starttls.required":"ture","mail.smtp.auth":"true","mail.smtp.starttls.enable":"true"}},"notification@nio.com":{"host":"smtp.partner.outlook.cn","port":"587","user_name":"notification@nio.com","password":"L28EL7#0vlp3vDuK","properties":{"mail.smtp.starttls.required":"ture","mail.smtp.auth":"true","mail.smtp.starttls.enable":"true"}},"tsp@nioint.com":{"host":"smtpint.nioint.com","port":"465","user_name":"tsp@nioint.com","password":"2ghlmcl1hblsqt_TSP","properties":{"mail.smtp.ssl.enable":"true","mail.smtp.auth":"true"}}}


"""
# +47 468 21 625
from tests.app_message_center.clear_rate_limit import clear_rate_limit

norway_phone_number = [
    ("+4795861510", "Vijay Sharma", "vijay.sharma@nio.com"),
    ("+4746821625", "Espen Byrjall", "espen.byrjall@nio.com"),
    ("+4790416210", "Jangir", "jangir.taher@nio.com"),
    ("+4792256265", "Stine Skyseth", "stine.skyseth@nio.com"),
    ("+4748361533", "Ola Smines", "ola.smines@nio.com"),
    ("+4745243903", "Jon Christian Aardal", "jonchristian.aardal@nio.com"),
    ("+4791305149", "Marianne Moelmen", "marianne.moelmen@nio.com"),
    ("+4790551411", "Marius Hayler", "marius.hayler@nio.com"),
    ("+4746895930", "Renate Eliesen", "renate.eliesen1@nio.com"),
]

email_config = {"verify_notification@nio.io": {"host": "smtp.office365.com", "port": "587", "user_name": "notification@nio.io", "password": "NCpwr281fiR7",
                                               "properties": {"mail.smtp.starttls.required": "ture", "mail.smtp.auth": "true", "mail.smtp.starttls.enable": "true"}}}

import time
import pytest
from utils.http_client import TSPRequest as hreq
from utils.collection_message_states import collection_message_states
from utils.logger import logger

skip_env_list = ["test", "stg"]
eu_sms_push_path = "/api/2/in/message/eu/sms_push"
eu_sms_direct_sms_push = "/api/2/in/message/eu/sms_direct_push"
eu_sms_voice_message_push = "/api/2/in/message/eu/voice_message"
server_app_id = 10000
# recipients_one = "+4746821625"  # Espen Byrjall
# recipients_one = "+4746821625"  # Espen Byrjall
# recipients_one = "+4790416210"  # Jangir
# recipients_one = "+4795861510"  # Vijay Sharma
recipients_one = "+8617610551933"  #
recipients_batch = ",".join(list([user[0] for user in norway_phone_number]))


@pytest.mark.skip("manual")
@pytest.mark.run(order=1)
class TestPushSMS(object):
    """
    接口文档 http://showdoc.nevint.com/index.php?s=/13&page_id=30142
    """

    @pytest.mark.parametrize("case_name,recipients,host_key,data_key", [
        # ("正案例_单个人发送_TOC", recipients_one, "app_in", "nmp_app"),
        ("正案例_单个人发送_TOB", recipients_one, "app_tob_in", "nmp_app_tob"),
        # ("正案例_多个人发送_TOC", recipients_batch, "app_in", "nmp_app",
    ])
    def test_push_sms_eu(self, env, redis, cmdopt, mysql, case_name, recipients, host_key, data_key):
        clear_rate_limit(redis, cmdopt, 10000)
        if cmdopt in skip_env_list:
            logger.debug(f"该测试案例不适用【{cmdopt}】环境")
            return 0
        category = 'ads'
        http = {
            "host": env['host'][host_key],
            "path": eu_sms_push_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "region": "eu",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": server_app_id,
                "sign": ""
            },
            "json": {
                "recipients": recipients,
                "content": f"【{cmdopt}】environment. Push SMS test. eu_sms_push_path",
                "category": category,
            }
        }
        response = hreq.request(env, http)
        assert response['result_code'] == 'success'
        message_id = response['data']['message_id']
        sms_history_list = mysql[data_key].fetch("sms_history", {"message_id": message_id}, ["recipient"])
        for sms_history in sms_history_list:
            assert str(sms_history['recipient']) in recipients.split(",")
        sms_history_info = mysql[data_key].fetch("sms_history_meta_info", {"message_id": message_id}, )
        assert len(sms_history_info) == 1

    @pytest.mark.parametrize("case_name,recipients,host_key,data_key", [
        ("正案例_单个人发送_TOC", recipients_one, "app_in", "nmp_app"),
        # ("正案例_单个人发送_TOB", recipients_one, "app_tob_in", "nmp_app_tob"),
        # ("正案例_多个人发送_TOC", recipients_batch,"app_in", "nmp_tob"),
    ])
    def test_push_sms_direct_eu(self, env, cmdopt, mysql, case_name, recipients, host_key, data_key):
        if cmdopt in skip_env_list:
            logger.debug(f"该测试案例不适用【{cmdopt}】环境")
            return 0
        category = 'ads'
        http = {
            "host": env['host'][host_key],
            "path": eu_sms_direct_sms_push,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "region": "eu",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": server_app_id,
                "sign": ""
            },
            "json": {
                "recipients": recipients,
                "content": f"【{cmdopt}】environment. NIO Push SMS test. eu_sms_direct_sms_push",
                "category": category,
            }
        }
        response = hreq.request(env, http)
        assert response['result_code'] == 'success'
        message_id = response['data']['message_id']
        sms_history_list = mysql[data_key].fetch("sms_history", {"message_id": message_id}, ["recipient"])
        for sms_history in sms_history_list:
            assert str(sms_history['recipient']) in recipients.split(",")
        sms_history_info = mysql[data_key].fetch("sms_history_meta_info", {"message_id": message_id}, )
        assert len(sms_history_info) == 1

    @pytest.mark.skip("manual")
    @pytest.mark.parametrize("case_name,recipients,host_key,data_key", [
        ("正案例_单个人发送_TOC", recipients_one, "app_in", "nmp_app"),
        # ("正案例_单个人发送_TOB", recipients_one, "app_tob_in", "nmp_app_tob"),
    ])
    def test_push_sms_voce_message_eu(self, env, cmdopt, mysql, case_name, recipients, host_key, data_key):
        if cmdopt in skip_env_list:
            logger.debug(f"该测试案例不适用【{cmdopt}】环境")
            return 0
        category = 'ads'
        http = {
            "host": env['host'][host_key],
            "path": eu_sms_voice_message_push,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "region": "eu",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": server_app_id,
                "sign": ""
            },
            "json": {
                "recipients": recipients,
                # "content": "God morgen,Ha en fin dag,95861510,Takk,NIO voice messages to test if any bother please forgive me",
                "content": "NIO voice messages to test if any bother please forgive me, Best wishes for you",
                "category": category,
            }
        }
        response = hreq.request(env, http)
        assert response['result_code'] == 'success'
        message_id = response['data']['message_id']
        sms_history_list = mysql[data_key].fetch("sms_history", {"message_id": message_id}, ["recipient"])
        for sms_history in sms_history_list:
            assert str(sms_history['recipient']) in recipients.split(",")
        sms_history_info = mysql[data_key].fetch("sms_history_meta_info", {"message_id": message_id}, )
        assert len(sms_history_info) == 1
