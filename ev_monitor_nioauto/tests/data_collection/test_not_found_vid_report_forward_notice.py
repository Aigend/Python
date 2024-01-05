""" 
@author:dun.yuan
@time: 2021/11/19 11:37 上午
@contact: dun.yuan@nio.com
@description: 实际情况中，对于有车辆vehicle_id不存在于vehicle_profile表中，但有数据上报的情况，
              如果发送的是充电/行程开始事件或充电/行程周期性事件时，转发notice消息到kafka特定的topic。
@showdoc：http://showdoc.nevint.com/index.php?s=/datacollection&page_id=6840
"""
import time

import allure
import pytest
import random
import json
from utils.assertions import assert_equal


class TestWrongVidForwardNotice(object):
    @pytest.mark.test
    def test_wrong_vid_report_forward_notice(self, kafka, publish_msg_by_kafka, checker):
        # 重置offset
        kafka['cvs'].set_offset_to_end(kafka['topics']['notice'])
        has_platform = random.choice([0, 1, 2])

        with allure.step("随机选择会转发vid不存在notice的事件"):
            event_name = random.choice(['charge_start_event', 'journey_start_event', 'trip_start_event',
                                        'periodical_charge_update', 'periodical_journey_update'])

        with allure.step("构造并上报消息"):
            checker.mysql.delete('vehicle_profile', {'id': '00c42efa8e364173b44129e6e4b358fe'})
            notice = {
                "noticeType": "NonExistVehicle",
                "staticInfo": {
                    "vehicleId": "00c42efa8e364173b44129e6e4b358fe",
                    "vin": "SQETEST0024324412",
                    "iccId": "SQETEST0024324412abc"
                }
            }
            time.sleep(5)
            if has_platform == 1:
                _, obj = publish_msg_by_kafka(event_name, platform_type=1, vid=notice['staticInfo']['vehicleId'],
                                              vin=notice['staticInfo']['vin'], icc_id=notice['staticInfo']['iccId'])
                notice['staticInfo']['platformType'] = "NT2"
            elif has_platform == 2:
                _, obj = publish_msg_by_kafka(event_name, platform_type=2, vid=notice['staticInfo']['vehicleId'],
                                              vin=notice['staticInfo']['vin'], icc_id=notice['staticInfo']['iccId'])
                notice['staticInfo']['platformType'] = "NT1_2"
            else:
                _, obj = publish_msg_by_kafka(event_name, platform_type=0, vid=notice['staticInfo']['vehicleId'],
                                              vin=notice['staticInfo']['vin'], icc_id=notice['staticInfo']['iccId'])
                notice['staticInfo']['platformType'] = "NT1"

        with allure.step('校验 {}'.format(kafka['topics']['notice'])):
            msg = None
            for data in kafka['cvs'].consume(kafka['topics']['notice'], timeout=30):
                msg = json.loads(data)
                if msg['staticInfo']['vehicleId'] == notice['staticInfo']['vehicleId']:
                    msg.pop('timestamp')
                    assert_equal(msg, notice)
                    break
            assert msg

        with allure.step("验证不存在的vid插入vehicle_profile，存储平台信息，eccmode正确。这属于rvs的功能"):
            res = checker.mysql.fetch_one('vehicle_profile', {'id': '00c42efa8e364173b44129e6e4b358fe'})
            if has_platform == 2:
                assert res['platform'] == 'NT1.2'
                assert res['dk_cert_mode'] == 'rsa'
            elif has_platform == 1:
                assert res['platform'] == 'NT2.0'
                assert res['dk_cert_mode'] == 'ecc'
            else:
                assert res['platform'] == 'NT1.0'
                assert res['dk_cert_mode'] == 'rsa'
