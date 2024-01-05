""" 
@author:dun.yuan
@time: 2022/5/6 3:47 PM
@contact: dun.yuan@nio.com
@description: 试驾车数据报告生成，试驾单target_status=DROVE的时候，从data_report取begin_time和end_time之前的数据点
第一个和最后一个点vehicle_state=2或者3选取作为试驾行程的起始和结束点，试驾数据从这两个点中间取
@showdoc：消费https://apidoc.nioint.com/project/1084/interface/api/148290
生产http://showdoc.nevint.com/index.php?s=/11&page_id=33742
"""
import json
import random
import time
import allure
import gzip
import pytest

from utils.assertions import assert_equal
from utils.httptool import request


@pytest.mark.test
class TestTrialDriveReport(object):
    def test_trial_drive_report(self, env, kafka, mysql, publish_msg_by_kafka):
        begin_time = round(time.time())
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['trial_drive'])
        time.sleep(1)
        with allure.step("模拟一段试驾行程"):
            vid = 'ce0a53e2090b49dc91c49ee054e35f4d'
            vin = 'SQETEST0495164801'
            trip_id = str(round(time.time()))
            mileage = mysql['rvs'].fetch_one('status_vehicle', {"id": vid})['mileage']

            # 构造并上报消息
            _, obj = publish_msg_by_kafka('trip_start_event', protobuf_v=18, vid=vid, vin=vin,
                                          vehicle_status={'mileage': mileage, 'vehl_state': 3},
                                          trip_status={'trip_id': trip_id, 'trip_state': 2, 'trip_odometer': 0})
            trip = {'max_speed': round(obj['vehicle_status']['speed'], 1)}

            # 上报周期行程事件和驾驶行为事件
            rapid_swerve, rapid_deceleration, rapid_acceleration = 0, 0, 0
            for i in range(3):
                _, obj = publish_msg_by_kafka('periodical_journey_update', protobuf_v=18, vid=vid, vin=vin,
                                              sample_points=[
                                                  {'vehicle_status': {"mileage": mileage + i, 'vehl_state': 1},
                                                   'trip_status': {'trip_id': trip_id, 'trip_state': 2,
                                                                   'trip_odometer': i}}])
                if obj['sample_points'][0]['vehicle_status']['speed'] > trip['max_speed']:
                    trip['max_speed'] = round(obj['sample_points'][0]['vehicle_status']['speed'], 1)

                nextev_message, driving_behaviour_obj = publish_msg_by_kafka('driving_behaviour_event', protobuf_v=18,
                                                                             vid=vid, vin=vin)

                if driving_behaviour_obj['behaviour'][0] == 0:
                    rapid_swerve += 1
                elif driving_behaviour_obj['behaviour'][0] == 1:
                    rapid_deceleration += 1
                elif driving_behaviour_obj['behaviour'][0] == 2:
                    rapid_acceleration += 1

            # 上报trip_end消息
            _, obj = publish_msg_by_kafka('trip_end_event', protobuf_v=18, vid=vid, vin=vin,
                                          vehicle_status={'mileage': mileage + random.randint(3, 10), 'vehl_state': 3},
                                          position_status={'longitude': 121.2653, 'latitude': 31.3756},
                                          # 用最后一包数据的经纬度去infotainment查询试驾历史天气, 必须保证经纬度对应的地区在天气历史表存在
                                          trip_status={'trip_id': trip_id, 'trip_state': 2, 'trip_odometer': 5})

            if rapid_acceleration:
                trip['rapid_acceleration'] = rapid_acceleration

            if obj['vehicle_status']['speed'] > trip['max_speed']:
                trip['max_speed'] = round(obj['vehicle_status']['speed'], 1)
            trip['trip_mileage'] = obj['vehicle_status']['mileage'] - mileage

        with allure.step("推送试驾结束消息"):
            end_time = round(time.time())
            data = {
                'order_no': f'test{begin_time}',
                'target_order': {
                    'begin_time': begin_time,
                    'end_time': end_time,
                    'vins': vin,
                    'status': 4
                }
            }
        with allure.step("调用data report接口查询数据"):
            kafka['comn'].produce(kafka['topics']['drive_test'], json.dumps(data))
            res = request('GET', url=f"{env['host']['tsp_in']}/api/1/in/data/vehicle/{vid}/history/simplification",
                          params={'start_time': begin_time*1000, 'end_time': end_time*1000,
                                  'detail_field': 'position_status.longitude_gcj02,position_status.latitude_gcj02',
                                  'sampling_rate': 1, 'order': 'asc'}).json()
            track = list(filter(lambda x: x.pop('msg_type') != 'driving_behaviour_event', res['data']))
            for it in track:
                it['longitude'] = it.pop('position_status.longitude_gcj02')
                it['latitude'] = it.pop('position_status.latitude_gcj02')
                it['timestamp'] = it.pop('sample_ts')
            trip['track'] = track

        with allure.step("验证试驾行程推送"):
            expect_msg = {'trip': trip, 'trial_order_no': data['order_no'], 'model_type': 'ET7', 'vin': vin}
            with allure.step('校验 {}'.format(kafka['topics']['trial_drive'])):
                kafka_msg = None
                is_found = False
                for data in kafka['comn'].consume(kafka['topics']['trial_drive'], timeout=30):
                    kafka_msg = json.loads(gzip.decompress(data).decode())
                    print(kafka_msg)
                    if kafka_msg['trial_order_no'] == expect_msg['trial_order_no']:
                        is_found = True
                        break
                assert_equal(True, is_found)
                kafka_msg.pop('weather')
                kafka_msg['trip'].pop('trip_duration')
                assert_equal(kafka_msg, expect_msg)
