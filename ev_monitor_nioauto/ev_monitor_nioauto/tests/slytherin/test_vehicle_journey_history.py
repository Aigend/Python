#!/usr/bin/env python
# coding=utf-8

"""
:file: test_vehicle_journey_history.py
:author: muhan.chen
:Date: Created on 2018/9/21 下午3:10
:Description: 处理行程开始、行程中、行程结束事件，将数据存入vehicle_journey_history
"""
import json
import time
import allure
import pytest

from utils import message_formator
from utils.assertions import assert_equal
from utils.coordTransform import wgs84_to_gcj02
from utils.logger import logger
from utils.time_parse import timestamp_to_utc_strtime
from utils.http_client import TSPRequest as hreq


@pytest.mark.test
class TestVehiJourHis(object):
    @pytest.fixture(scope='function', autouse=False)
    def tag(self):
        return 'vehicle_history_2'

    def test_vehicle_journey_history(self, env, vid, redis_key_front, checker, publish_msg_by_kafka, mysql):
        """
        运行本case需保证与上一次运行相隔至少5分钟，或将数据库中记录的5分钟内的相同journey_id的数据条目删除
        """
        vid = env['vehicles']['vehicle_history_1']['vehicle_id']
        vin = env['vehicles']['vehicle_history_1']['vin']
        journey_id = int(time.time())
        remote_vehicle_redis_key_front = redis_key_front['remote_vehicle']
        # 清除redis 缓存
        checker.redis.delete(f'{remote_vehicle_redis_key_front}:journey_last:{vid}:{journey_id}')

        # 构造并上报消息
        nextev_message, journey_start_message = publish_msg_by_kafka('journey_start_event',
                                                                     vid=vid, vin=vin,
                                                                     journey_id=str(journey_id))

        max_speed, min_speed, avg_speed, rapid_swerve, rapid_deceleration, rapid_acceleration = 0, 400, 0, 0, 0, 0
        for i in range(3):
            nextev_message, journey_update_message = publish_msg_by_kafka('periodical_journey_update',
                                                                          journey_id=str(journey_id),
                                                                          vid=vid, vin=vin)
            nextev_message, driving_behaviour_obj = publish_msg_by_kafka('driving_behaviour_event', vid=vid, vin=vin)

            max_speed = max(max_speed, journey_update_message['sample_points'][0]['driving_data']['max_speed'])
            min_speed = min(min_speed, journey_update_message['sample_points'][0]['driving_data']['min_speed'])
            if i == 2:
                avg_speed = journey_update_message['sample_points'][0]['driving_data']['average_speed']

            if driving_behaviour_obj['behaviour'][0] == 0:
                rapid_swerve += 1
            elif driving_behaviour_obj['behaviour'][0] == 1:
                rapid_deceleration += 1
            elif driving_behaviour_obj['behaviour'][0] == 2:
                rapid_acceleration += 1

        with allure.step("journey_end事件不上报soc/dump_energy/mileage时,等待5秒左右服务调用journey/summary来获取补齐相应数据"):
            nextev_message, journey_end_message = publish_msg_by_kafka('journey_end_event',
                                                                       vid=vid, vin=vin,
                                                                       journey_id=str(journey_id),
                                                                       clear_fields=['vehicle_status.mileage',
                                                                                     'soc_status.soc',
                                                                                     'soc_status.dump_enrgy'])

        vehicle_journey_in_mysql = mysql['sharding'].fetch(f'vehicle_journey_history_{vid[:2]}',
                                                           {"vehicle_id": vid,
                                                            "process_id": str(journey_id)},
                                                           suffix=' and `max_speed` is not NULL',
                                                           exclude_fields=['create_time', 'update_time',
                                                                           'id', 'user_switch',
                                                                           'start_area_code', 'journey_id',
                                                                           'end_area_code', 'total_fall',
                                                                           'total_rise'])[0]

        with allure.step("校验vehicle_journey_history会记录行程中急加速等的次数"):
            assert_equal(rapid_swerve, vehicle_journey_in_mysql.pop('rapid_swerve'))
            assert_equal(rapid_deceleration, vehicle_journey_in_mysql.pop('rapid_deceleration'))
            assert_equal(rapid_acceleration, vehicle_journey_in_mysql.pop('rapid_acceleration'))

        with allure.step("校验vehicle_journey_history中的最大最小平均速度来源于journey_update事件"):
            assert vehicle_journey_in_mysql.pop('max_speed') == round(max_speed, 1)
            assert vehicle_journey_in_mysql.pop('min_speed') == round(min_speed, 1)
            assert vehicle_journey_in_mysql.pop('avg_speed') == round(avg_speed, 1)

        with allure.step("校验 journey_start和end 存入 vehicle_journey_history"):
            formator = message_formator.MessageFormator(vid, env=env)
            account_id = env['vehicles']['vehicle_history_1']['account_id']
            # 马可波罗服务需要修改路径
            journey_message = formator.to_mysql_vehicle_journey_history(journey_start_message, journey_end_message,
                                                                        account_id)
            # 5分钟内再次上报journey事件，journey_id是并不等于process_id，为了不影响重复测试，我们把journey_id pop掉
            journey_message.pop('journey_id')
            assert_equal(vehicle_journey_in_mysql, journey_message)

        with allure.step("校验redis中会维护一个process内的最大和最小速度，vehicle_journey_history中的最大最小平均速度来源于此"):

            re_data = checker.redis.get(f'{remote_vehicle_redis_key_front}:journey_last:{vid}:{journey_id}')
            data = json.loads(re_data)
            assert_equal(int(data['driving_data']['max_speed']), int(max_speed))
            assert_equal(int(data['driving_data']['min_speed']), int(min_speed))
            assert_equal(int(data['driving_data']['average_speed']), int(avg_speed))

    def test_invalid_position(self, env, vid, checker, publish_msg_by_kafka):
        vid = env['vehicles']['vehicle_history_1']['vehicle_id']
        vin = env['vehicles']['vehicle_history_1']['vin']
        journey_id = int(time.time())

        with allure.step("行程开始上报无效的经纬度数据：小于等于0"):
            nextev_message, journey_start_message = publish_msg_by_kafka('journey_start_event',
                                                                         vid=vid, vin=vin,
                                                                         journey_id=str(journey_id),
                                                                         position_status={'longitude': 0,
                                                                                          'latitude': -1})

        nextev_message, update_start = publish_msg_by_kafka('periodical_journey_update', journey_id=str(journey_id),
                                                            vid=vid, vin=vin)

        nextev_message, update_end = publish_msg_by_kafka('periodical_journey_update', journey_id=str(journey_id),
                                                          vid=vid, vin=vin)

        with allure.step("行程结束上报无效的经纬度数据：字段为空"):
            nextev_message, journey_end_message = publish_msg_by_kafka('journey_end_event',
                                                                       vid=vid, vin=vin,
                                                                       journey_id=str(journey_id),
                                                                       clear_fields=['position_status.longitude',
                                                                                     'position_status.latitude'])

        vehicle_journey_in_mysql = checker.mysql.fetch('vehicle_journey_history',
                                                       {"vehicle_id": vid,
                                                        "process_id": str(journey_id)},
                                                       suffix=' and `start_latitude` is not NULL')[0]

        with allure.step("行程开始，行程结束时若位置信息无效，则行程结束后取上报updte过程中最开始有效位置及最后有效位置存入vehicle_journey_history经纬度字段"):
            start_longitude, start_latitude = wgs84_to_gcj02(
                update_start['sample_points'][0]['position_status']['longitude'],
                update_start['sample_points'][0]['position_status']['latitude'])
            end_longitude, end_latitude = wgs84_to_gcj02(update_end['sample_points'][0]['position_status']['longitude'],
                                                         update_end['sample_points'][0]['position_status']['latitude'])
            assert vehicle_journey_in_mysql['start_longitude'] == round(start_longitude, 6)
            assert vehicle_journey_in_mysql['start_latitude'] == round(start_latitude, 6)
            assert vehicle_journey_in_mysql['end_longitude'] == round(end_longitude, 6)
            assert vehicle_journey_in_mysql['end_latitude'] == round(end_latitude, 6)

    def test_0_position(self, env, vid, checker, publish_msg_by_kafka):
        # 须中国境内的经纬度才转84坐标，否则直接存原始经纬度
        vid = env['vehicles']['vehicle_history_1']['vehicle_id']
        vin = env['vehicles']['vehicle_history_1']['vin']
        journey_id = int(time.time())

        with allure.step("行程开始上报无效的经纬度数据：小于等于0"):
            nextev_message, journey_start_message = publish_msg_by_kafka('journey_start_event',
                                                                         vid=vid, vin=vin,
                                                                         journey_id=str(journey_id),
                                                                         position_status={'longitude': 0,
                                                                                          'latitude': 0})
        with allure.step("上报第一个journey_update经纬度数据非零"):
            nextev_message, update_start = publish_msg_by_kafka('periodical_journey_update', journey_id=str(journey_id),
                                                                vid=vid, vin=vin,
                                                                sample_points=[{'position_status': {'longitude': 121,
                                                                                                    'latitude': 31}}]
                                                                )

        with allure.step("上报最后一个journey_update经纬度数据非零"):
            nextev_message, update_end = publish_msg_by_kafka('periodical_journey_update', journey_id=str(journey_id),
                                                              vid=vid, vin=vin,
                                                              sample_points=[{'position_status': {'longitude': 116,
                                                                                                  'latitude': 40}}]
                                                              )

        with allure.step("行程结束上报无效的经纬度数据：小于等于0"):
            nextev_message, journey_end_message = publish_msg_by_kafka('journey_end_event',
                                                                       vid=vid, vin=vin,
                                                                       journey_id=str(journey_id),
                                                                       position_status={'longitude': 0,
                                                                                        'latitude': 0})

        vehicle_journey_in_mysql = checker.mysql.fetch('vehicle_journey_history',
                                                       {"vehicle_id": vid,
                                                        "process_id": str(journey_id)},
                                                       suffix=' and `start_latitude` is not NULL')[0]

        with allure.step("行程开始/行程结束时若位置信息无效，使用update中的第一个/最后一个 非零位置（无论是否有效）进行补充"):
            start_longitude, start_latitude = wgs84_to_gcj02(
                update_start['sample_points'][0]['position_status']['longitude'],
                update_start['sample_points'][0]['position_status']['latitude'])
            end_longitude, end_latitude = wgs84_to_gcj02(update_end['sample_points'][0]['position_status']['longitude'],
                                                         update_end['sample_points'][0]['position_status']['latitude'])
            assert vehicle_journey_in_mysql['start_longitude'] == round(start_longitude, 6)
            assert vehicle_journey_in_mysql['start_latitude'] == round(start_latitude, 6)
            assert vehicle_journey_in_mysql['end_longitude'] == round(end_longitude, 6)
            assert vehicle_journey_in_mysql['end_latitude'] == round(end_latitude, 6)

    def test_update_journey_invalid_position(self, env, vid, checker, publish_msg_by_kafka):
        """
        位置信息有效过滤（84坐标为零的判断）
        """
        vid = env['vehicles']['vehicle_history_1']['vehicle_id']
        vin = env['vehicles']['vehicle_history_1']['vin']
        journey_id = int(time.time())

        with allure.step("行程开始上报无效的经纬度数据：等于0"):
            sample_ts_start = int(time.time() * 1000)
            nextev_message, journey_start_message = publish_msg_by_kafka('journey_start_event',
                                                                         vid=vid, vin=vin,
                                                                         journey_id=str(journey_id),
                                                                         sample_ts=sample_ts_start,
                                                                         clear_fields=['position_status.longitude', 'position_status.latitude'])

        with allure.step("上报最后一个journey_update经纬度数据为0"):
            nextev_message, update = publish_msg_by_kafka('periodical_journey_update', journey_id=str(journey_id),
                                                          vid=vid, vin=vin,
                                                          clear_fields=['sample_points[0].position_status.longitude', 'sample_points[0].position_status.latitude'])

        with allure.step("行程结束上报无效的经纬度数据：等于0"):
            sample_ts_end = int(time.time() * 1000)
            nextev_message, journey_end_message = publish_msg_by_kafka('journey_end_event', sleep_time=4,
                                                                       vid=vid, vin=vin,
                                                                       journey_id=str(journey_id),
                                                                       sample_ts=sample_ts_end,
                                                                       clear_fields=['position_status.latitude', 'position_status.longitude'])

        vehicle_journey_in_mysql = checker.mysql.fetch('vehicle_journey_history',
                                                       {"vehicle_id": vid,
                                                        "process_id": str(journey_id)},
                                                       suffix=' and `start_latitude` is not NULL')[0]

        with allure.step("update数据也无效则调用data_report接口journey/track/newest接口查询最新经纬度补充开始结束位置数据"):
            # 校验调用接口补充开始位置数据
            inputs = {
                "host": env['host']['tsp_in'],
                "method": "GET",
                "path": f"/api/1/in/data/vehicle/{vid}/journey/track/newest",
                "params": {
                    'app_id': 10001,
                    'inquire_time': sample_ts_start // 1000,
                    "hash_type": "md5",
                    "sign": ''
                },
                "timeout": 5.0
            }
            start_data = hreq.request(env, inputs)
            logger.info("request status is {}".format(start_data["result_code"]))
            assert vehicle_journey_in_mysql['start_longitude'] == start_data['data']['track'][0]['longitude']
            assert vehicle_journey_in_mysql['start_latitude'] == start_data['data']['track'][0]['latitude']
            # 校验调用接口补充结束位置数据
            inputs = {
                "host": env['host']['tsp_in'],
                "method": "GET",
                "path": f"/api/1/in/data/vehicle/{vid}/journey/track/newest",
                "params": {
                    'app_id': 10001,
                    'inquire_time': sample_ts_end // 1000,
                    "hash_type": "md5",
                    "sign": ''
                },
                "timeout": 5.0
            }
            end_data = hreq.request(env, inputs)
            logger.info("request status is {}".format(start_data["result_code"]))
            assert vehicle_journey_in_mysql['end_longitude'] == end_data['data']['track'][0]['longitude']
            assert vehicle_journey_in_mysql['end_latitude'] == end_data['data']['track'][0]['latitude']

    def test_journey_id_is_same_in_5min(self, env, checker, publish_msg_by_kafka):
        """
        运行本case需保证与上一次运行相隔至少5分钟，或将数据库中记录的5分钟内的相同journey_id的数据条目删除
        """
        vid = env['vehicles']['vehicle_history_2']['vehicle_id']
        vin = env['vehicles']['vehicle_history_2']['vin']
        # 第一次上报消息
        checker.mysql.fetch('const_wti', where_model={"wti_enabled": 0}, fields=['wti_code'])
        journey_id_1st = int(time.time())
        nextev_message_start_1st, journey_start_message_1st = publish_msg_by_kafka('journey_start_event',
                                                                                   vid=vid, vin=vin,
                                                                                   journey_id=str(journey_id_1st),
                                                                                   sleep_time=3)
        nextev_message_end_1st, journey_end_message_end_1st = publish_msg_by_kafka('journey_end_event',
                                                                                   vid=vid, vin=vin,
                                                                                   journey_id=str(journey_id_1st),
                                                                                   sleep_time=60)

        # 5分钟之内第二次上报消息
        journey_id_2nd = int(time.time())
        nextev_message_start_2nd, journey_start_message_2nd = publish_msg_by_kafka('journey_start_event',
                                                                                   vid=vid, vin=vin,
                                                                                   journey_id=str(journey_id_2nd),
                                                                                   sleep_time=3)
        nextev_message_end_2nd, journey_end_message_2nd = publish_msg_by_kafka('journey_end_event',
                                                                               vid=vid, vin=vin,
                                                                               journey_id=str(journey_id_2nd),
                                                                               sleep_time=3)
        # 校验第二次上报消息后Mysql中存储的journey_id为journey_id_1st
        with allure.step("校验 journey_start和end 存入 vehicle_journey_history"):
            journey_id_in_mysql = checker.mysql.fetch('vehicle_journey_history',
                                                      {"vehicle_id": vid,
                                                       "process_id": str(journey_id_2nd)},
                                                      fields=['journey_id'])[0]
            assert_equal(journey_id_in_mysql['journey_id'], str(journey_id_1st))

    def test_area_code(self, env, vid, checker, publish_msg_by_kafka):
        """
        完整行程周期事件上报成功，会存储area_code开始/结束字段
        """
        vid = env['vehicles']['vehicle_history_1']['vehicle_id']
        vin = env['vehicles']['vehicle_history_1']['vin']
        journey_id = str(int(time.time()))

        # 上报完整行程
        start_time = int(time.time() * 1000)
        nextev_message, journey_start_message = publish_msg_by_kafka('journey_start_event',
                                                                     vid=vid, vin=vin,
                                                                     sample_ts=start_time,
                                                                     journey_id=journey_id)

        nextev_message, update = publish_msg_by_kafka('periodical_journey_update', journey_id=journey_id,
                                                      vid=vid, vin=vin)

        end_time = int(time.time() * 1000)
        nextev_message, journey_end_message = publish_msg_by_kafka('journey_end_event',
                                                                   vid=vid, vin=vin,
                                                                   sample_ts=end_time,
                                                                   journey_id=journey_id,
                                                                   sleep_time=10)

        vehicle_journey_history = checker.mysql.fetch('vehicle_journey_history',
                                                      {"vehicle_id": vid,
                                                       "process_id": journey_id})[0]

        # vehicle_journey_history记录补全area_code有大约4秒的延迟
        with allure.step("vehicle_navigation_district表中拿取开始时间之前相近的时间对应的area_code"):
            start_area_code_navigation = checker.mysql.fetch('vehicle_navigation_district',
                                                             {"vehicle_id": vid,
                                                              "update_time<": timestamp_to_utc_strtime(start_time)},
                                                             order_by='update_time desc')[0]
            assert_equal(vehicle_journey_history['start_area_code'], start_area_code_navigation['area_code'])
        with allure.step("vehicle_navigation_district表中拿取结束时间之前相近的时间对应的area_code"):
            end_area_code_navigation = checker.mysql.fetch('vehicle_navigation_district',
                                                           {"vehicle_id": vid,
                                                            "update_time<": timestamp_to_utc_strtime(end_time)},
                                                           order_by='update_time desc')[0]
            assert_equal(vehicle_journey_history['end_area_code'], end_area_code_navigation['area_code'])

    def test_driving_behaviour_event(self, env, vid, checker, publish_msg_by_kafka):
        """
        driving_bahaviour_event事件的sample_ts减相关行程的start_time >= 72小时,不会更新mysql
        """
        vid = env['vehicles']['vehicle_history_1']['vehicle_id']
        vin = env['vehicles']['vehicle_history_1']['vin']
        journey_id = int(time.time())

        # 构造并上报消息
        start_time = int(time.time() * 1000)
        nextev_message, journey_start_message = publish_msg_by_kafka('journey_start_event',
                                                                     vid=vid, vin=vin,
                                                                     journey_id=str(journey_id),
                                                                     sample_ts=start_time)

        nextev_message, driving_behaviour_obj = publish_msg_by_kafka('driving_behaviour_event', vid=vid, vin=vin,
                                                                     sample_ts=start_time + 72 * 60 * 60 * 1000)

        nextev_message, journey_end_message = publish_msg_by_kafka('journey_end_event',
                                                                   vid=vid, vin=vin,
                                                                   journey_id=str(journey_id))

        vehicle_journey_in_mysql = checker.mysql.fetch('vehicle_journey_history',
                                                       {"vehicle_id": vid,
                                                        "process_id": str(journey_id)},
                                                       fields=['rapid_swerve', 'rapid_deceleration',
                                                               'rapid_acceleration'])[0]

        with allure.step("校验vehicle_journey_history会记录行程中急加速等的次数"):
            assert_equal(vehicle_journey_in_mysql['rapid_swerve'], 0)
            assert_equal(vehicle_journey_in_mysql['rapid_deceleration'], 0)
            assert_equal(vehicle_journey_in_mysql['rapid_acceleration'], 0)

    def test_journey_update_position_0_redis_0(self, checker, env, publish_msg_by_kafka, redis_key_front, vid, redis):
        remote_vehicle_key_front = redis_key_front['remote_vehicle']
        vid = env['vehicles']['vehicle_history_1']['vehicle_id']
        vin = env['vehicles']['vehicle_history_1']['vin']
        journey_id = int(time.time())
        # 清除redis 缓存
        redis_key_journey_first = f'{remote_vehicle_key_front}:journey_first:{vid}:{journey_id}'
        redis_key_journey_last = f'{remote_vehicle_key_front}:journey_last:{vid}:{journey_id}'

        # 验证proto小于18的版本，不会生成trip
        redis_key_trip_first = f'{remote_vehicle_key_front}:trip_first:{vid}:{journey_id}'
        redis_key_trip_last = f'{remote_vehicle_key_front}:trip_last:{vid}:{journey_id}'

        # 构造并上报消息
        publish_msg_by_kafka('journey_start_event', vid=vid, vin=vin, journey_id=str(journey_id))

        publish_msg_by_kafka('periodical_journey_update', vid=vid, vin=vin, journey_id=str(journey_id),
                             sample_points=[{'position_status': {'longitude': 0, 'latitude': 0},
                                             'trip_status': {'trip_id': str(journey_id)}}])

        publish_msg_by_kafka('journey_end_event', vid=vid, vin=vin, journey_id=str(journey_id))

        with allure.step("校验redis存储逻辑，journey update数据存入redis时，不进行经纬度的判断，直接存入，当需要补偿数据时才进行经纬度有效判断（非0）"):
            journey_first = checker.redis.get(redis_key_journey_first)
            data = json.loads(journey_first)
            assert_equal(int(data['position_status']['longitude']), 0)
            assert_equal(int(data['position_status']['latitude']), 0)
            journey_end = checker.redis.get(redis_key_journey_last)
            data = json.loads(journey_end)
            assert_equal(int(data['position_status']['longitude']), 0)
            assert_equal(int(data['position_status']['latitude']), 0)
            # 验证proto小于18的版本，不会生成trip
            assert checker.redis.get(redis_key_trip_first) is None
            assert checker.redis.get(redis_key_trip_last) is None

    def test_journey_update_position_0_redis_0_v18(self, checker, env, publish_msg_by_kafka, redis_key_front, vid,
                                                   redis):
        """
        校验上报行程周期事件，
            1. proto version >= 18，redis不再创建journey_first、journey_last缓存，用trip_first、trip_last缓存
            2. proto version < 18，redis不创建trip_first、trip_last缓存,仍以journey_first、journey_last缓存
        """
        remote_vehicle_key_front = redis_key_front['remote_vehicle']
        vid = env['vehicles']['vehicle_history_2']['vehicle_id']
        vin = env['vehicles']['vehicle_history_2']['vin']
        journey_id = int(time.time())
        # 验证proto大于18的版本，不生成journey
        redis_key_journey_first = f'{remote_vehicle_key_front}:journey_first:{vid}:{journey_id}'
        redis_key_journey_last = f'{remote_vehicle_key_front}:journey_last:{vid}:{journey_id}'

        # 验证proto大于18的版本，生成trip
        redis_key_trip_first = f'{remote_vehicle_key_front}:trip_first:{vid}:{journey_id}'
        redis_key_trip_last = f'{remote_vehicle_key_front}:trip_last:{vid}:{journey_id}'

        # 构造并上报消息
        publish_msg_by_kafka('journey_start_event', protobuf_v=18, vid=vid, vin=vin, journey_id=str(journey_id))

        publish_msg_by_kafka('periodical_journey_update', protobuf_v=18, vid=vid, vin=vin, journey_id=str(journey_id),
                             sample_points=[{'position_status': {'longitude': 1, 'latitude': 1},
                                             'trip_status': {'trip_id': str(journey_id), 'trip_state': 2, 'trip_odometer': 0}}])

        publish_msg_by_kafka('journey_end_event', protobuf_v=18, vid=vid, vin=vin, journey_id=str(journey_id))

        with allure.step("校验redis存储逻辑，journey update数据存入redis时，不进行经纬度的判断，直接存入，当需要补偿数据时才进行经纬度有效判断（非0）"):
            trip_first = checker.redis.get(redis_key_trip_first)
            data = json.loads(trip_first)
            assert_equal(int(data['position_status']['longitude']), 1)
            assert_equal(int(data['position_status']['latitude']), 1)
            trip_last = checker.redis.get(redis_key_trip_last)
            data = json.loads(trip_last)
            assert_equal(int(data['position_status']['longitude']), 1)
            assert_equal(int(data['position_status']['latitude']), 1)
            # 验证proto大于18的版本，不会生成journey
            assert checker.redis.get(redis_key_journey_first) is None
            assert checker.redis.get(redis_key_journey_last) is None

    def test_journey_id_not_merge_if_swap(self, env, checker, publish_msg, tag, tsp_agent_once):
        """
        运行本case需保证与上一次运行相隔至少5分钟，或将数据库中记录的5分钟内的相同journey_id的数据条目删除
        """
        vid = env['vehicles']['vehicle_history_2']['vehicle_id']
        vin = env['vehicles']['vehicle_history_2']['vin']
        # 第一次上报行程
        checker.mysql.fetch('const_wti', where_model={"wti_enabled": 0}, fields=['wti_code'])
        journey_id_1st = int(time.time())
        nextev_message_start_1st, journey_start_message_1st = publish_msg('journey_start_event',
                                                                          tsp_agent=tsp_agent_once,
                                                                          vid=vid, vin=vin,
                                                                          journey_id=str(journey_id_1st),
                                                                          sleep_time=3)
        nextev_message_end_1st, journey_end_message_end_1st = publish_msg('journey_end_event',
                                                                          tsp_agent=tsp_agent_once,
                                                                          vid=vid, vin=vin,
                                                                          journey_id=str(journey_id_1st),
                                                                          sleep_time=20)

        # 上报换电开始
        nextev_message, obj = publish_msg('specific_event', tsp_agent=tsp_agent_once,
                                          vid=vid, vin=vin, event_type='power_swap_start',
                                          sleep_time=20)

        # 上报换电结束
        nextev_message, obj = publish_msg('specific_event', tsp_agent=tsp_agent_once,
                                          vid=vid, vin=vin, event_type='power_swap_end',
                                          sleep_time=20)

        # 5分钟之内第二次上报行程
        journey_id_2nd = int(time.time())
        nextev_message_start_2nd, journey_start_message_2nd = publish_msg('journey_start_event',
                                                                          tsp_agent=tsp_agent_once,
                                                                          vid=vid, vin=vin,
                                                                          journey_id=str(journey_id_2nd),
                                                                          sleep_time=3)
        nextev_message_end_2nd, journey_end_message_2nd = publish_msg('journey_end_event',
                                                                      tsp_agent=tsp_agent_once,
                                                                      vid=vid, vin=vin,
                                                                      journey_id=str(journey_id_2nd),
                                                                      sleep_time=30)
        # 校验第二次上报消息后Mysql中存储的journey_id为journey_id_2nd
        with allure.step("校验 journey_start和end 存入 vehicle_journey_history"):
            journey_id_in_mysql = checker.mysql.fetch('vehicle_journey_history',
                                                      {"vehicle_id": vid,
                                                       "process_id": str(journey_id_2nd)},
                                                      fields=['journey_id'])[0]
            assert_equal(journey_id_in_mysql['journey_id'], str(journey_id_2nd))

        # 5分钟之内第三次上报行程
        journey_id_3rd = int(time.time())
        nextev_message_start_2nd, journey_start_message_2nd = publish_msg('journey_start_event',
                                                                          tsp_agent=tsp_agent_once,
                                                                          vid=vid, vin=vin,
                                                                          journey_id=str(journey_id_3rd),
                                                                          sleep_time=3)
        nextev_message_end_2nd, journey_end_message_2nd = publish_msg('journey_end_event',
                                                                      tsp_agent=tsp_agent_once,
                                                                      vid=vid, vin=vin,
                                                                      journey_id=str(journey_id_3rd),
                                                                      sleep_time=3)
        # 校验第二次上报消息后Mysql中存储的journey_id为journey_id_2nd
        with allure.step("校验 journey_start和end 存入 vehicle_journey_history"):
            journey_id_in_mysql = checker.mysql.fetch('vehicle_journey_history',
                                                      {"vehicle_id": vid,
                                                       "process_id": str(journey_id_3rd)},
                                                      fields=['journey_id'])[0]
            assert_equal(journey_id_in_mysql['journey_id'], str(journey_id_2nd))

    def test_vehicle_journey_history_v18(self, env, vid, redis_key_front, checker, publish_msg_by_kafka, mysql):
        """
        proto版本大于等于18的journeyevent不再存分表
        """
        vid = env['vehicles']['vehicle_history_2']['vehicle_id']
        vin = env['vehicles']['vehicle_history_2']['vin']
        journey_id = int(time.time())
        remote_vehicle_redis_key_front = redis_key_front['remote_vehicle']

        # 构造并上报消息
        nextev_message, journey_start_message = publish_msg_by_kafka('journey_start_event', protobuf_v=18,
                                                                     vid=vid, vin=vin,
                                                                     journey_id=str(journey_id))

        for i in range(3):
            nextev_message, journey_update_message = publish_msg_by_kafka('periodical_journey_update', protobuf_v=18,
                                                                          journey_id=str(journey_id),
                                                                          vid=vid, vin=vin)
            nextev_message, driving_behaviour_obj = publish_msg_by_kafka('driving_behaviour_event', protobuf_v=18,
                                                                         vid=vid, vin=vin)

        with allure.step("journey_end事件不上报soc/dump_energy/mileage时,等待5秒左右服务调用journey/summary来获取补齐相应数据"):
            nextev_message, journey_end_message = publish_msg_by_kafka('journey_end_event', protobuf_v=18,
                                                                       vid=vid, vin=vin,
                                                                       journey_id=str(journey_id),
                                                                       sleep_time=5,
                                                                       clear_fields=['vehicle_status.mileage',
                                                                                     'soc_status.soc',
                                                                                     'soc_status.dump_enrgy'])

        vehicle_journey_in_mysql = mysql['sharding'].fetch_one(f'vehicle_journey_history_{vid[:2]}',
                                                               {"vehicle_id": vid,
                                                                "process_id": str(journey_id)})

        assert vehicle_journey_in_mysql is None

    @pytest.mark.skip("Manual")
    def test_user_switch(self, checker, env, publish_msg_by_kafka, redis_key_front, vid, redis):
        # remote_vehicle_key_front = redis_key_front['remote_vehicle']
        """
        app端打开或关闭行程开关

        验证行程开关为开时，行程开始后，会在vehicle_journey_history表中对应journey_id插入车主account_id与user_switch=1
        验证行程开关为关时，行程开始后，会在vehicle_journey_history表中对应journey_id插入account_id与user_switch=0，再开启行程开关后user_switch=1
        验证无论行程开关为开或关，行程开始后，vehicle_journey_history表中对应journey_id插入account_id与user_switch，再开启或关闭行程switch都为1
        验证无论行程开关为开或关，行程结束后，vehicle_journey_history表中对应journey_id插入user_switch为用户当前旅程开关状态
        """
