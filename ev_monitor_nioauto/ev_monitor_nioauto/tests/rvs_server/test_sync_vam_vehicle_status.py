#!/usr/bin/env python
# coding=utf-8

"""
:file: test_sync_vam_vehicle_status
:author: yongiqng.wu
:contact: yongqing.wu@nio.com
:Date: Created on 2019/07/04
:Description:
"""

# !/usr/bin/env python
# coding=utf-8
import json
import time
import pytest

"""
:file:
:author: wu
:Description: vam同步车辆状态tag到tsp
:kafka文档: http://showdoc.nevint.com/index.php?s=/365&page_id=15591 (密码：vam123456)
"""

test_data = [
    ("推送内部车,期望保存成功",
     json.dumps({
         "vehicleIdentity": 0, "vehicleColor": "白色", "provinceCode": "420000", "cityCode": "420100", "isDelete": "0",
         "vehiclePurpose": "5", "vehicleStatusName": "可用", "vehiclePurposeName": "设备巡检车", "sendTime": 1562054402186,
         "vehicleNo": "沪WP1652", "cityName": "武汉市", "vehicleIdentityName": "内部", "provinceName": "湖北省",
         "vehicleVin": "SQETEST0999647340", "vehicleType": "2", "vehicleTypeName": "江铃", "vehicleStatus": 10
     }), {'vehicle_identity': 0, 'vehicle_condition': 10}),

    (
        "推送外部车,期望保存成功",
        json.dumps({
            "vehicleIdentity": 1, "vehicleColor": "白色", "provinceCode": "420000", "cityCode": "420100", "isDelete": "0",
            "vehiclePurpose": "5", "vehicleStatusName": "可用", "vehiclePurposeName": "设备巡检车", "sendTime": 1562054402186,
            "vehicleNo": "沪WP1652", "cityName": "武汉市", "vehicleIdentityName": "内部", "provinceName": "湖北省",
            "vehicleVin": "SQETEST0999647340", "vehicleType": "2", "vehicleTypeName": "江铃", "vehicleStatus": 3
        }), {'vehicle_identity': 1, 'vehicle_condition': 3}),

    (
        "推送内部车且已出售,期望保存成功并修改为外部车辆",
        json.dumps({
            "vehicleIdentity": 0, "vehicleColor": "白色", "provinceCode": "420000", "cityCode": "420100", "isDelete": "1",
            # "isDelete" 为 0, 则存入mysql中的'vehicle_identity'与推送Kafka的"vehicleIdentity"一致,
            # "isDelete" 为 1, 则存入mysql中的'vehicle_identity'为1, 为外部车
            "vehiclePurpose": "5", "vehicleStatusName": "可用", "vehiclePurposeName": "设备巡检车", "sendTime": 1562054402186,
            "vehicleNo": "沪WP1652", "cityName": "武汉市", "vehicleIdentityName": "内部", "provinceName": "湖北省",
            "vehicleVin": "SQETEST0999647340", "vehicleType": "2", "vehicleTypeName": "江铃", "vehicleStatus": 12
        }), {'vehicle_identity': 1, 'vehicle_condition': 12}),
    (
        "推送车辆已报废,期望保存成功并修改为报废状态",
        json.dumps({
            "vehicleIdentity": 0, "vehicleColor": "白色", "provinceCode": "420000", "cityCode": "420100", "isDelete": "1",
            # "isDelete" 为 0, 则存入mysql中的'vehicle_identity'与推送Kafka的"vehicleIdentity"一致,
            # "isDelete" 为 1, 则存入mysql中的'vehicle_identity'为1, 为外部车
            "vehiclePurpose": "5", "vehicleStatusName": "可用", "vehiclePurposeName": "设备巡检车", "sendTime": 1562054402186,
            "vehicleNo": "沪WP1652", "cityName": "武汉市", "vehicleIdentityName": "内部", "provinceName": "湖北省",
            "vehicleVin": "SQETEST0999647340", "vehicleType": "2", "vehicleTypeName": "江铃", "vehicleStatus": 12,
            "maintenanceStatus": 0, "suspensionStatus": 1, "allocationStatus": 0, "dispositionStatus": 3
        }), {'vehicle_identity': 1, 'vehicle_condition': 8})
]


def idfn():
    return [i[0] for i in test_data]

# TODO 马克波罗服务暂不支持，先跳过
@pytest.mark.marcopolo_skip
@pytest.mark.test
class TestSyncVamVehicleStatus(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, mysql):
        pass

    @pytest.mark.parametrize("case_id,request_data,expect", test_data, ids=idfn())
    def test_sync_vam_vehicle_status(self, vid, kafka, checker, request_data, expect, case_id, cmdopt):
        # 推送消息至kafka
        kafka['do'].produce(kafka['topics']['vam_vehicle_tag'], request_data)
        time.sleep(10)
        checker.check_mysql_tables(expect, ['vehicle_profile_info_extend'])
