# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_mipush_callback.py
# @Author : qiangwei.zhang
# @time: 2021/09/10
# @api: GET_/api/XXX 【必填】
# @showdoc:http://showdoc.nevint.com/index.php?s=/13&page_id=1273
# @Description :脚本描述

import allure
import pytest
import time
import json
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from utils.time_parse import now_shanghai_strtime, now_utc_strtime

aws_sns_callback_path = "/api/2/message_tracker/sns"

aws_sns_callback_keys = "case_name,result,sender_name,recipients,message_id"
aws_sns_callback_cases = (
    ["正案例_送达邮件", "delivery", "notification@nio.io", "550736273@qq.com", f"aws-sns-callback-delivery-{int(time.time() * 10000)}"],
    ["正案例_跳信邮件", "bounce", "notification@nio.io", "550736273@qq.com", f"aws-sns-callback-bounce-{int(time.time() * 10000)}"],
)
aws_sns_callback_ids = [f"{case[0]}" for case in aws_sns_callback_cases]


@pytest.mark.parametrize(aws_sns_callback_keys, aws_sns_callback_cases, ids=aws_sns_callback_ids)
def test_aws_sns_callback_delivery(env, mysql, case_name, result, sender_name, recipients, message_id):
    now_time = now_shanghai_strtime("%Y-%m-%dT%H:%M:%S.%f")
    bounce = {
        'notificationType': 'Bounce',
        'bounce': {
            'feedbackId': '0107017de01ca7a1-d637c72f-2157-480d-82d9-81d32955aa69-000000',
            'bounceType': 'Transient',
            'bounceSubType': 'General',
            'bouncedRecipients': [
                {
                    'emailAddress': recipients,
                    'action': 'failed',
                    'status': '4.4.7',
                    'diagnosticCode': 'smtp; 554 4.4.7 Message expired: unable to deliver in 840 minutes.<421 4.4.0 Unable to lookup DNS for ni.dt.ac.fe.ss>'
                }
            ],
            'timestamp': now_time,
            'reportingMTA': 'dns; b228-21.smtp-out.eu-central-1.amazonses.com'
        },
        'mail': {
            'timestamp': now_time,
            'source': sender_name,
            'sourceArn': 'arn:aws:ses:eu-central-1:329282579833:identity/notification@nio.io',
            'sourceIp': '3.127.44.197',
            'sendingAccountId': '329282579833',
            'messageId': '0107017ddd06be3a-5375b71a-b2b0-4f21-927c-4d3f7571ded5-000000',
            'destination': [recipients],
            'headersTruncated': False,
            'headers': [
                {'name': 'Received',
                 'value': 'from app-message-center-65d45f988-hblgb (ec2-3-127-44-197.eu-central-1.compute.amazonaws.com [3.127.44.197]) by email-smtp.amazonaws.com with SMTP (SimpleEmailService-d-FEESSNZSE) id mXB8fHIYMIbwydw1PFSv for EU.fe.268@ni.dt.ac.fe.ss; Tue, 21 Dec 2021 12:45:46 +0000 (UTC)'},
                {'name': 'Date', 'value': 'Tue, 21 Dec 2021 20:45:46 +0800 (CST)'},
                {'name': 'From', 'value': sender_name},
                {'name': 'To', 'value': recipients},
                {'name': 'Message-ID', 'value': '<1585355804.467.1640090746404@app-message-center-65d45f988-hblgb>'},
                {'name': 'Subject', 'value': 'NIO Security Alert'},
                {'name': 'MIME-Version', 'value': '1.0'},
                {'name': 'Content-Type', 'value': 'multipart/mixed;  boundary="----=_Part_465_280984537.1640090746230"'},
                {'name': 'X-SES-CONFIGURATION-SET', 'value': 'cvs_marketinfo'},
                {'name': 'X-NMP-MESSAGE-ID', 'value': message_id}
            ],
            'commonHeaders': {
                'from': [sender_name],
                'date': 'Tue, 21 Dec 2021 20:45:46 +0800 (CST)',
                'to': [recipients],
                'messageId': '<1585355804.467.1640090746404@app-message-center-65d45f988-hblgb>',
                'subject': 'NIO Security Alert'
            }
        }
    }
    delivery = {
        'notificationType': 'Delivery',
        'mail': {
            'timestamp': now_time,
            'source': sender_name,
            'sourceArn': 'arn:aws:ses:eu-central-1:329282579833:identity/notification@nio.io',
            'sourceIp': '18.159.13.28',
            'sendingAccountId': '329282579833',
            'messageId': '0107017ddd00a403-c093fc6b-aa0c-4f61-be62-fb0d1b28361b-000000',
            'destination': [recipients],
            'headersTruncated': False,
            'headers': [
                {'name': 'Received',
                 'value': 'from app-message-center-78b9b5dfff-sfg75 (ec2-18-159-13-28.eu-central-1.compute.amazonaws.com [18.159.13.28]) by email-smtp.amazonaws.com with SMTP (SimpleEmailService-d-4WREKH0TE) id W93fUK4gZqSDttRUepOv for jc.aardal@gmail.com; Tue, 21 Dec 2021 12:39:06 +0000 (UTC)'},
                {'name': 'Date', 'value': 'Tue, 21 Dec 2021 20:39:06 +0800 (CST)'},
                {'name': 'From', 'value': sender_name},
                {'name': 'To', 'value': recipients},
                {'name': 'Message-ID', 'value': '<1285070962.527.1640090346479@app-message-center-78b9b5dfff-sfg75>'},
                {'name': 'Subject', 'value': 'NIO'},
                {'name': 'MIME-Version', 'value': '1.0'},
                {'name': 'Content-Type', 'value': 'multipart/mixed;  boundary="----=_Part_525_686146723.1640090346320"'},
                {'name': 'X-SES-CONFIGURATION-SET', 'value': 'cvs_marketinfo'},
                {'name': 'X-NMP-MESSAGE-ID', 'value': message_id}
            ],
            'commonHeaders': {
                'from': [sender_name],
                'date': 'Tue, 21 Dec 2021 20:39:06 +0800 (CST)',
                'to': [recipients],
                'messageId': '<1285070962.527.1640090346479@app-message-center-78b9b5dfff-sfg75>',
                'subject': 'NIO'
            }
        },
        'delivery':
            {
                'timestamp': now_time,
                'processingTimeMillis': 610,
                'recipients': [recipients],
                'smtpResponse': '250 2.0.0 OK  1640090347 e20si2186665wmq.170 - gsmtp',
                'remoteMtaIp': '66.102.1.26',
                'reportingMTA': 'b228-21.smtp-out.eu-central-1.amazonses.com'
            }
    }
    result_dict = {
        "delivery": delivery,
        "bounce": bounce,
    }

    inputs = {
        "host": env['host']['app_ex'],
        "path": aws_sns_callback_path,
        "method": "POST",
        "headers": {
            "Content-Type": "text/plain",
            "x-amz-sns-message-type": "Notification",
            "x-amz-sns-topic-arn": "arn:aws:sns:eu-central-1:329282579833:DS_CVS_SES"
        },
        "data": json.dumps({
            "Type": "Notification",
            "MessageId": "daf13e9c-90ac-5224-bd06-64a75d87644e",
            "TopicArn": "arn:aws:sns:eu-central-1:329282579833:DS_CVS_SES",
            "Message": json.dumps(result_dict.get(result)),
            "Timestamp": now_time,
            "SignatureVersion": "1",
            "Signature": "o8S03bLdtVa7YOA/ydxfXCRCE5jJe4h5j8J3EIxp4+YGG1r5NamQ42vwXjWvUTvXBUIGxhEv22oXD/8DAJUaqo0Tau4eqIrBXvGUGakmnrq+401khGdqxptopj6d8JJ7Xph8C0tiAPrbnw0YAg27U2flkMcuMLXRAnFqrc5EGsCJb0umSBHgOZHuu+GrUjMvydRLmsSbFNy0LHHVqw1hN8K/b9Z9qHN6MuUmUoacpcX3L7xMW/565pQAC6P5G5dnkQ7Ri13iTo0G+WA2gYEOhaH68k+lDKUWkSAqC1eEG1UBBW7ORTnZWu6qzlCLWQKKOU0cm0RfTrort6mUKygPyg==",
            "SigningCertURL": "https://sns.eu-central-1.amazonaws.com/SimpleNotificationService-7ff5318490ec183fbaddaa2a969abfda.pem",
            "UnsubscribeURL": "https://sns.eu-central-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-central-1:329282579833:DS_CVS_SES:b5d1fed9-0a15-49e9-96dd-ca291a033def"
        })
    }
    with allure.step(f"asw_sns{case_name}"):
        response = hreq.request(env, inputs)
    with allure.step("校验数据库"):
        assert response.get("result_code") == "success"
        res = mysql['nmp_app'].fetch("message_state", {"message_id": message_id}, retry_num=70)
        utc_time = now_utc_strtime()[:13]
        create_time = res[0].get("create_time")[:13]
        assert create_time == utc_time, f"create_time is not utc time, Expect {utc_time} Actual {create_time}"
        update_time = res[0].get("update_time")[:13]
        assert update_time == utc_time, f"update_time is not utc time, Expect {utc_time} Actual {update_time}"
        logger.debug(res)
        assert res

