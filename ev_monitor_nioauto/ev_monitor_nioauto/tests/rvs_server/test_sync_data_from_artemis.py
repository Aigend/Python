""" 
@author:dun.yuan
@time: 2022/5/23 6:09 PM
@contact: dun.yuan@nio.com
@description: 从artemis同步标定数据, 记录在vehicle_soft_config表
@showdoc：https://apidoc.nioint.com/project/2662/interface/api/331506
"""
import random
import time

import allure
import json
from utils.time_parse import timestamp_to_utc_strtime


class TestSyncDataFromArtemus(object):
    def test_sync_data_from_artemis(self, vid, vin, kafka, checker):
        with allure.step('模拟artemis推送标定数据'):
            sample_ts = round(time.time()*1000)
            time.sleep(1)
            data = {"message_id": "dolore et",
                    "vin": vin,
                    "activity_code": "FPE2020043001ES8G1F",
                    "activity_status": random.choice([2001, 2005, 2010, 2015, 2100]),
                    "activity_type": random.choice([1001, 1005]),
                    "finish_status": 12781001, #random.choice([12781001, 12781002]),
                    "dealer_code": "laborum ad nulla minim dolor",
                    "ro_no": "sunt occaecat consectetur Excepteur cillum",
                    "car_model": "model", "activity_name": "aute",
                    "activity_sub_type": random.choice(['RJSJ', 'ZYGZ', '70411002', '70411002'])}
            kafka['comn'].produce(kafka['topics']['activity-changed'], json.dumps(data))

        with allure.step('验证存储标定记录'):
            res = checker.mysql.fetch_one('vehicle_soft_config', {'vehicle_id': vid, 'sample_time>': timestamp_to_utc_strtime(sample_ts)})
            assert res['type'] == 'calibrate'
            assert res['value'] == '1'
