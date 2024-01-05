#!/usr/bin/env python
# coding=utf-8

"""
智慧提醒：
https://confluence.nioint.com/pages/viewpage.action?pageId=276278721
"""

import json
import time
from pprint import pprint

import allure
import pytest

from config.cert import web_cert
from utils.assertions import assert_equal
from utils.httptool import request


class TestIntelgent:


    def test_tyre(self, kafka):
        """
        智慧提醒 胎压

  do2:
    bootstrap.servers:
      - 10.125.234.185:9092
      - 10.125.233.31:9092
      - 10.125.232.186:9092
    group.id: ev_monitor_test
    auto.offset.reset: latest
    security.protocol: sasl_plaintext
    sasl.mechanisms: PLAIN
    sasl.password: PVvkrqfRUNj1v2FZ
    sasl.username: GCFzCNGS
    enable.partition.eof: False
    topics:
      artemis: do-artemis-activewarning-status-sit # 胎压告警



        vehicle_id: 4e18c0f0ab734805a802b845a02ad824
    client_id: "ChDaRLq8_tbIqc0iNNSEKddPEAEY9cUBIJVOKAI="
    vin: SQETEST0514819462
    account_id: 212409581
    phone: 98762667410
    pw: 112233

        liftestyle_test.intelligent_reminder
        """


        #li
        # vid='4e18c0f0ab734805a802b845a02ad824'
        # vin='SQETEST0514819462'
        # phone= 98762667410
        # phone_code = 112233


        vid='d0a29e2ab0a34f92a81e63353aee2999'
        vin='SQETEST0253795679'
        phone= 98762653318
        phone_code = 993147




        # # stat_1
        # vid='ed37c834509248b7914c9498c4d2129a'
        # vin='SQETEST0596093473'
        # phone= 98762667422
        # phone_code=112233



        # phone=98762751379
        # phone_code=729843
        # # vid='26c6c7242ad34bdb8d1c88b3c4a64a9b'
        # vid='7603c4d5dd4b46d59ba8c6e7ae0929c9'
        # # vid='5ddb3fe683674a5a8496f682a5787b87'
        # vin='SQETEST0072554874'

        # # 春丽
        # vid='d2d39828e2b1402fa32b01c9a3b84f30'
        # vin='SQETEST0360302093'
        # phone= 98762345112
        # phone_code=112233


        data = json.dumps(
            {"warningNo": "64101190220120200507", "vin": vin, "masterPhone": phone,
             "warningStatus": "10301001", "vid": vid,
             "signals": [
                 {
                     "type": "10311001",
                     "signal": "TpmsReLeWhlDeltaPressSts",
                     "descript": "左后轮胎正在快速漏气",
                     "wtiCode": "WTI-TPMS-13"
                 }
             ]})

        kafka['do_2'].produce(kafka['topics']['artemis'], data)



# icar redis
    def test_poster(self,redis):
        """海报删除redis记录"""

        print("\n=====all======")
        pprint(f"{redis['dawn'].keys('**dawn**')}")

        # 缓存user信息5分钟，拿不到去"/uds/in/user/v2/users取
        # pprint(c.get('dawn_user_account_965951979'))

        # # 缓存mobile信息分钟，拿不到去"/uds/in/user/v2/users取
        # pprint(redis['dawn'].get('dawn_user_mobile_98762667410'))
        #


        pprint(f"=====redis get and delete======")

        # #每天0点10分清楚前一天缓存

        # # 缓存mobile信息，拿不到去cms表里取，有效期为5分钟
        pprint(redis['dawn'].get('dawn_read_promotion_533758357_20200615'))
        pprint(redis['dawn'].delete('dawn_read_promotion_533758357_20200623'))

        pprint(redis['dawn'].get('dawn_read_promotion_212409581_20200615'))
        pprint(redis['dawn'].delete('dawn_read_promotion_212409581_20200623'))


    def test_insurance(self,kafka):
        mobile: 98762751379 / 729843
        accountId: 780072597

        vid='4e18c0f0ab734805a802b845a02ad824'
        vin='SQETEST0514819462'
        phone= 98762667410
        account_id= "212409581"
        # account_id= "780072597"
        # vid='5ddb3fe683674a5a8496f682a5787b87'
        # vid='7603c4d5dd4b46d59ba8c6e7ae0929c9'
        # vid='26c6c7242ad34bdb8d1c88b3c4a64a9b'

        data = json.dumps({"scene_id": "package", "target": {"type": "single", "account_ids": [account_id]},
                                          "msg_id": "432874cd-2825-452a-81e7-76d037140e006",
                                          "field_values": {"packageName": "服务续包",
                                                           "vehicleId": vid,
                                                           "time": int(time.time())}, "create_time": int(time.time())})


        print(data)
        kafka['do_2'].produce(kafka['topics']['msgalert'], data)
