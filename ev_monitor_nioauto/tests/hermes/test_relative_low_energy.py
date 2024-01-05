#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2021/06/24 18:00
@contact: hongzhen.bi@nio.com
@description: 相对低电量告警推送
@需求汇总: https://confluence.nioint.com/pages/viewpage.action?pageId=215813610
@showdoc: http://showdoc.nevint.com/index.php?s=/150&page_id=21529
"""
import json

import allure
import pytest


class TestRelativeLowEnergyPush:

    @pytest.fixture(autouse=True)
    def prepare(self, cmdopt, vid, redis):
        redis['cluster'].delete(f"hermes_{cmdopt}:relative_tri_count:{vid}")
        redis['cluster'].delete(f"hermes_{cmdopt}:relative_alarm_status:{vid}")

    def test_relative_low_energy_push(self, cmdopt, vid, publish_msg_by_kafka, redis, kafka):
        """
        告警标志key: hermes_test:relative_alarm_status:{vid}
        触发告警次数count: hermes_test:relative_tri_count:{vid}

        """
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_notification'])

        with allure.step("本地需要先缓存1次，本地缓存1分钟过期"):
            for i in range(5):
                # 修改车辆状态满足前提条件
                publish_msg_by_kafka('periodical_journey_update', sample_points=[
                    {
                        "soc_status": {"remaining_range": 10},
                        "position_status": {"posng_valid_type": 0,
                                            "longitude": 109.924199,
                                            "latitude": 36.661108},
                        "vehicle_status": {"vehl_state": 3}
                    }
                ], sleep_time=2)
                count = redis['cluster'].get(f"hermes_{cmdopt}:relative_tri_count:{vid}")
                if count and int(count) == 1:
                    break
            for i in range(8):
                # 修改车辆状态满足前提条件
                publish_msg_by_kafka('periodical_journey_update', sample_points=[
                    {
                        "soc_status": {"remaining_range": 10},
                        "position_status": {"posng_valid_type": 0,
                                            "longitude": 109.924199,
                                            "latitude": 36.661108},
                        "vehicle_status": {"vehl_state": 3}
                    }
                ], sleep_time=2)
                count = redis['cluster'].get(f"hermes_{cmdopt}:relative_tri_count:{vid}")
                assert int(count) == i + 2

        with allure.step("count=10触发推送，redis归0"):
            publish_msg_by_kafka('periodical_journey_update', sample_points=[
                {
                    "soc_status": {"remaining_range": 10},
                    "position_status": {"posng_valid_type": 0,
                                        "longitude": 109.924199,
                                        "latitude": 36.661108}
                }
            ], sleep_time=2)
            count = redis['cluster'].get(f"hermes_{cmdopt}:relative_tri_count:{vid}")
            assert int(count) == 0
            count = redis['cluster'].get(f"hermes_{cmdopt}:relative_alarm_status:{vid}")
            assert int(count) == 1
            # push成功查询kibana log关键字："relative_low_energy notification, vehicle_id: {vid}, content: {msg}"

        with allure.step("push成功后会推送kafka"):
            kafka_msg = None
            is_found = False
            for data in kafka['comn'].consume(kafka['topics']['vehicle_notification'], timeout=10):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                if vid == kafka_msg['data']['vehicle_id']:
                    is_found = True
                    break
            assert is_found is True
            print(kafka_msg)

        with allure.step("在距离充电资源60km范围内，若剩余里程大于25km，则清除告警"):
            publish_msg_by_kafka('periodical_journey_update', sample_points=[
                {
                    "soc_status": {"remaining_range": 30},
                    "position_status": {"posng_valid_type": 0,
                                        "longitude": 116.4594552536267,
                                        "latitude": 40.0202844228925}
                }
            ], sleep_time=2)
            count = redis['cluster'].get(f"hermes_{cmdopt}:relative_alarm_status:{vid}")
            assert int(count) == 0
