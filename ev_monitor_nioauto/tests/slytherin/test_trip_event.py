""" 
@author:dun.yuan
@time: 2021/6/7 11:22 上午
@contact: dun.yuan@nio.com
@description: 1.从protobuf版本18开始处理trip，proto msg版本和event中版本同时更新为18
2.trip按vehicle_id分表，存入rvs_data_test库中
3.proto版本小于18的处理逻辑不变；大于等于18的journeyevent不再存分表，只写主表用于统计；大于等于18的行程周期性事件，按"%s:trip_first:%s:%s"和"%s:trip_last:%s:%s"写周期性状态到redis;大于等于18的驾驶行为事件，数据更新到trip中
4.trip事件不做聚合，需存储tripstatus数据
5.新增trip事件补数据job
@showdoc：
"""
import json
import random
import time
import allure
import pytest
from utils.http_client import TSPRequest as hreq
from utils.assertions import assert_equal
from utils.time_parse import timestamp_to_utc_strtime


class TestTripEvent(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, mysql):
        original_mileage_in_mysql = mysql['rvs'].fetch_one('status_vehicle', {"id": vid})['mileage']

        return {'original_mileage': original_mileage_in_mysql}

    def test_trip_event_as_entire_trip(self, vid, checker, publish_msg, kafka, mysql, prepare, redis_key_front):
        """

        :param vid:
        :param checker:
        :param publish_msg:
        :param kafka:
        :param mysql:
        :param prepare:
        :param redis_key_front:
        :return:
        上报一个完整的trip事件，用同一个trip_id
            1. 上报trip_start事件，验证rvs_data库trip_history表生成一条新记录，校验行程开始相关字段
            2. trip进行中上报一个行程周期事件，校验redis中trip_first缓存数据
            3. 上报trip_end事件，验证rvs_data库trip_history表的本条trip记录，校验行程结束相关字段补全
        """
        trip_id = str(round(time.time()))
        with allure.step("上报事件trip_start_event, protobuf版本18"):
            start_remaining_range = round(random.randint(500, 2000) * 0.5)
            nextev_message, trip_start_obj = publish_msg('trip_start_event', protobuf_v=18,
                                                         vehicle_status={'mileage': prepare['original_mileage']},
                                                         trip_status={'trip_id': trip_id, 'trip_state': 2},
                                                         soc_status={
                                                             'remaining_range': start_remaining_range})  # rvs_data 表增加start_remaining_range字段

        with allure.step("检验mysql rvs_data数据库的存储"):
            trip_in_mysql = mysql['rvs_data'].fetch_one(f'vehicle_trip_history_{vid[:2]}',
                                                        {'trip_id': trip_id},
                                                        suffix=' and `start_soc` is not NULL')
            assert trip_in_mysql['start_soc'] == trip_start_obj['soc_status']['soc']
            assert trip_in_mysql['start_dump_energy'] == round(trip_start_obj['soc_status']['dump_enrgy'], 1)
            assert trip_in_mysql['start_mileage'] == trip_start_obj['vehicle_status']['mileage']
            # trip_in_mysql存储的经纬度是longitude_gcj02和latitude_gcj02，在Cassandra
            # assert trip_in_mysql['start_longitude'] == trip_start_obj['position_status']['longitude']
            # assert trip_in_mysql['start_latitude'] == trip_start_obj['position_status']['latitude']
            assert trip_in_mysql['is_end'] is None
            assert trip_in_mysql['start_remaining_range'] == start_remaining_range
            assert trip_in_mysql['end_remaining_range'] is None

        with allure.step("上报周期行程事件"):
            nextev_message, journey_update_obj = publish_msg('periodical_journey_update', protobuf_v=18,
                                                             sample_points=[{
                                                                 'sample_ts': round(time.time() * 1000)+11000,
                                                                 'vehicle_status': {
                                                                     "mileage": prepare['original_mileage'] + 1},
                                                                 'trip_status': {'trip_id': trip_id, 'trip_state': 2}

                                                             }, {
                                                                 'sample_ts': round(time.time() * 1000) + 12000,
                                                                 "vehicle_status": {
                                                                     "mileage": prepare['original_mileage'] + 2},
                                                                 'trip_status': {'trip_id': trip_id}

                                                             }])

        with allure.step("检查redis trip first缓存数据"):
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            key_first = f'{remote_vehicle_key_front}:trip_first:{vid}:{trip_id}'
            trip_first = checker.redis.get(key_first)
            data = json.loads(trip_first)

            assert data['soc_status']['soc'] == journey_update_obj['sample_points'][0]['soc_status']['soc']
            assert data['vehicle_status']['mileage'] == journey_update_obj['sample_points'][0]['vehicle_status'][
                'mileage']
            assert round(data['position_status']['longitude']) == round(
                journey_update_obj['sample_points'][0]['position_status']['longitude'])
            assert round(data['position_status']['latitude']) == round(
                journey_update_obj['sample_points'][0]['position_status']['latitude'])
            assert data['sample_time'] == journey_update_obj['sample_points'][0]['sample_ts'] // 1000
            assert round(data['driving_data']['average_speed']) == round(
                journey_update_obj['sample_points'][0]['driving_data']['average_speed'])
            assert round(data['driving_data']['max_speed']) == round(
                journey_update_obj['sample_points'][0]['driving_data']['max_speed'])
            assert round(data['driving_data']['min_speed']) == round(
                journey_update_obj['sample_points'][0]['driving_data']['min_speed'])
            data['trip_status'].pop('sample_time')
            journey_update_obj['sample_points'][0]['trip_status'].pop('trip_id')
            journey_update_obj['sample_points'][0]['trip_status'].pop('user_id')
            assert_equal(data['trip_status'], journey_update_obj['sample_points'][0]['trip_status'])

        with allure.step("上报事件trip_end_event, protobuf版本18"):
            end_remaining_range = round(random.randint(0, 500) * 0.5)
            nextev_message, trip_end_obj = publish_msg('trip_end_event', protobuf_v=18,
                                                       sample_ts=round(time.time() * 1000) + 15000,
                                                       vehicle_status={'mileage': prepare['original_mileage'] + 3},
                                                       trip_status={'trip_id': trip_id, 'trip_state': 2},
                                                       soc_status={
                                                           'remaining_range': end_remaining_range})  # rvs_data 表增加end_remaining_range字段

        with allure.step("检验mysql rvs_data数据库的存储"):
            trip_in_mysql = mysql['rvs_data'].fetch_one(f'vehicle_trip_history_{vid[:2]}',
                                                        {'trip_id': trip_id},
                                                        suffix=' and `end_soc` is not NULL')

            assert trip_in_mysql['end_soc'] == trip_end_obj['soc_status']['soc']
            assert trip_in_mysql['end_dump_energy'] == round(trip_end_obj['soc_status']['dump_enrgy'], 1)
            assert trip_in_mysql['end_mileage'] == trip_end_obj['vehicle_status']['mileage']
            assert trip_in_mysql['trip_odometer'] == trip_end_obj['trip_status']['trip_odometer']
            assert trip_in_mysql['trip_eng'] == trip_end_obj['trip_status']['trip_eng']
            assert trip_in_mysql['hv_ass_eng_pct'] == trip_end_obj['trip_status']['hv_ass_eng_pct']
            assert trip_in_mysql['lv_ass_eng_pct'] == trip_end_obj['trip_status']['lv_ass_eng_pct']
            assert trip_in_mysql['dri_eng_pct'] == trip_end_obj['trip_status']['dri_eng_pct']
            assert trip_in_mysql['reg_eng_pct'] == trip_end_obj['trip_status']['reg_eng_pct']
            assert trip_in_mysql['hvh_eng_pct'] == trip_end_obj['trip_status']['hvh_eng_pct']
            assert trip_in_mysql['is_end'] == 1
            assert trip_in_mysql['start_remaining_range'] == start_remaining_range
            assert trip_in_mysql['end_remaining_range'] == end_remaining_range
            # 检查mysql 速度的更新
            period = (trip_end_obj['sample_ts'] - trip_start_obj['sample_ts']) // 1000
            assert trip_in_mysql['avg_speed'] == round(3600 * trip_in_mysql['trip_odometer'] / period, 1)
            assert trip_in_mysql['max_speed'] == round(data['driving_data']['max_speed'], 1)
            assert trip_in_mysql['min_speed'] == round(data['driving_data']['min_speed'], 1)

    def test_journey_update_trip_redis(self, env, vid, redis_key_front, checker, publish_msg, mysql, prepare):
        """

        :param env:
        :param vid:
        :param redis_key_front:
        :param checker:
        :param publish_msg:
        :param mysql:
        :param prepare:
        :return:

        校验在一个完整的trip事件中，多次上报行程周期事件，trip redis能正确更新
            1. 第一次上报行程周期事件，校验trip_first和trip_last都有缓存
            2. 第二次上报行程周期事件，但采样时间小于第一次，校验trip_first的缓存被更新
            3. 第三次上报行程周期事件，采样时间最大，校验trip_last的缓存被更新
            4. 上报trip_end事件，结束行程，校验数据库记录的最大最小速度为trip last的缓存数据
        """
        trip_id = str(round(time.time()))
        with allure.step("上报事件trip_start_event, protobuf版本18"):
            nextev_message, trip_start_obj = publish_msg('trip_start_event', protobuf_v=18,
                                                         vehicle_status={'mileage': prepare['original_mileage']},
                                                         trip_status={'trip_id': trip_id, 'trip_state': 2,
                                                                      'trip_odometer': 0})

        with allure.step("第一次上报周期行程事件"):
            sample_ts = round(time.time() * 1000)+14000
            nextev_message, journey_update_obj = publish_msg('periodical_journey_update', protobuf_v=18,
                                                             sample_points=[{
                                                                 'sample_ts': sample_ts,
                                                                 'vehicle_status': {
                                                                     "mileage": prepare['original_mileage'] + 1},
                                                                 'trip_status': {'trip_id': trip_id, 'trip_state': 2,
                                                                                 'trip_odometer': 10},
                                                                 'driving_data': {
                                                                     'max_speed': 99.0,
                                                                     'min_speed': 10.0
                                                                 }}])

        with allure.step("检查redis trip last缓存数据"):
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            key_first = f'{remote_vehicle_key_front}:trip_first:{vid}:{trip_id}'
            key_last = f'{remote_vehicle_key_front}:trip_last:{vid}:{trip_id}'
            trip = checker.redis.get(key_last)
            data = json.loads(trip)

            assert data['soc_status']['soc'] == journey_update_obj['sample_points'][0]['soc_status']['soc']
            assert data['vehicle_status']['mileage'] == journey_update_obj['sample_points'][0]['vehicle_status'][
                'mileage']
            assert round(data['position_status']['longitude']) == round(
                journey_update_obj['sample_points'][0]['position_status']['longitude'])
            assert round(data['position_status']['latitude']) == round(
                journey_update_obj['sample_points'][0]['position_status']['latitude'])
            assert data['sample_time'] == journey_update_obj['sample_points'][0]['sample_ts'] // 1000
            assert data['driving_data']['max_speed'] == 99.0
            assert data['driving_data']['min_speed'] == 10.0
            data['trip_status'].pop('sample_time')
            journey_update_obj['sample_points'][0]['trip_status'].pop('trip_id')
            journey_update_obj['sample_points'][0]['trip_status'].pop('user_id')
            assert_equal(data['trip_status'], journey_update_obj['sample_points'][0]['trip_status'])

        with allure.step("补报周期行程事件"):
            nextev_message, journey_update_obj = publish_msg('periodical_journey_update', protobuf_v=18,
                                                             sample_points=[{
                                                                 'sample_ts': sample_ts - 2000,
                                                                 'vehicle_status': {
                                                                     "mileage": prepare['original_mileage']},
                                                                 'trip_status': {'trip_id': trip_id, 'trip_state': 2,
                                                                                 'trip_odometer': 5},
                                                                 'driving_data': {
                                                                     'max_speed': 119.0,
                                                                     'min_speed': 5.0
                                                                 }
                                                             }])

        with allure.step("检查redis trip first缓存数据"):
            trip = checker.redis.get(key_first)
            data = json.loads(trip)

            assert data['soc_status']['soc'] == journey_update_obj['sample_points'][0]['soc_status']['soc']
            assert data['vehicle_status']['mileage'] == journey_update_obj['sample_points'][0]['vehicle_status'][
                'mileage']
            assert round(data['position_status']['longitude']) == round(
                journey_update_obj['sample_points'][0]['position_status']['longitude'])
            assert round(data['position_status']['latitude']) == round(
                journey_update_obj['sample_points'][0]['position_status']['latitude'])
            assert data['sample_time'] == journey_update_obj['sample_points'][0]['sample_ts'] // 1000
            assert data['driving_data']['max_speed'] == 119.0
            assert data['driving_data']['min_speed'] == 5.0
            data['trip_status'].pop('sample_time')
            journey_update_obj['sample_points'][0]['trip_status'].pop('trip_id')
            journey_update_obj['sample_points'][0]['trip_status'].pop('user_id')
            assert_equal(data['trip_status'], journey_update_obj['sample_points'][0]['trip_status'])

        with allure.step("第二次上报周期行程事件"):
            nextev_message, journey_update_obj = publish_msg('periodical_journey_update', protobuf_v=18,
                                                             sample_points=[{
                                                                 'sample_ts': sample_ts + 10000,
                                                                 'vehicle_status': {
                                                                     "mileage": prepare['original_mileage'] + 1},
                                                                 'trip_status': {'trip_id': trip_id, 'trip_state': 2,
                                                                                 'trip_odometer': 15},
                                                                 'driving_data': {
                                                                     'max_speed': 110.0,
                                                                     'min_speed': 8.0
                                                                 }
                                                             }])

        with allure.step("检查redis trip last缓存数据"):
            trip = checker.redis.get(key_last)
            data = json.loads(trip)

            assert data['soc_status']['soc'] == journey_update_obj['sample_points'][0]['soc_status']['soc']
            assert data['vehicle_status']['mileage'] == journey_update_obj['sample_points'][0]['vehicle_status'][
                'mileage']
            assert round(data['position_status']['longitude']) == round(
                journey_update_obj['sample_points'][0]['position_status']['longitude'])
            assert round(data['position_status']['latitude']) == round(
                journey_update_obj['sample_points'][0]['position_status']['latitude'])
            assert data['sample_time'] == journey_update_obj['sample_points'][0]['sample_ts'] // 1000
            assert data['driving_data']['max_speed'] == 110.0
            assert data['driving_data']['min_speed'] == 8.0
            data['trip_status'].pop('sample_time')
            journey_update_obj['sample_points'][0]['trip_status'].pop('trip_id')
            journey_update_obj['sample_points'][0]['trip_status'].pop('user_id')
            assert_equal(data['trip_status'], journey_update_obj['sample_points'][0]['trip_status'])

        with allure.step("上报事件trip_end_event, protobuf版本18"):
            nextev_message, trip_end_obj = publish_msg('trip_end_event', protobuf_v=18, sleep_time=4,
                                                       vehicle_status={'mileage': prepare['original_mileage'] + 3},
                                                       trip_status={'trip_id': trip_id, 'trip_state': 2,
                                                                    'trip_odometer': 20})

        with allure.step("检验mysql rvs_data数据库的存储"):
            trip_in_mysql = mysql['rvs_data'].fetch_one(f'vehicle_trip_history_{vid[:2]}',
                                                        {"vehicle_id": vid,
                                                         'trip_id': trip_id},
                                                        suffix=' and `max_speed` is not NULL')
            # 检查mysql 速度的更新
            assert trip_in_mysql['max_speed'] == round(data['driving_data']['max_speed'], 1)
            assert trip_in_mysql['min_speed'] == round(data['driving_data']['min_speed'], 1)

    def test_driving_behaviour_as_entire_trip(self, env, redis_key_front, checker, publish_msg_by_kafka, mysql):
        """

        :param env:
        :param redis_key_front:
        :param checker:
        :param publish_msg_by_kafka:
        :param mysql:
        :return:

        校验在trip中的，上报驾驶行为事件，会被保存到本条行程记录中：
            在行程中上报三次periodical_journey_update和driving_behaviour_event，
            在上报trip_end之后，校验该条行程记录的rapid_swerve rapid_deceleration rapid_acceleratio的次数
        """
        vid = env['vehicles']['vehicle_history_2']['vehicle_id']
        vin = env['vehicles']['vehicle_history_2']['vin']
        trip_id = str(round(time.time()))
        mileage = mysql['rvs'].fetch_one('status_vehicle', {"id": vid})['mileage']

        # 构造并上报消息
        publish_msg_by_kafka('journey_start_event', protobuf_v=18, vid=vid, vin=vin, journey_id=trip_id)

        publish_msg_by_kafka('trip_start_event', protobuf_v=18, vid=vid, vin=vin,
                             vehicle_status={'mileage': mileage},
                             trip_status={'trip_id': trip_id, 'trip_state': 2, 'trip_odometer': 0})

        # 上报周期行程事件和驾驶行为事件
        rapid_swerve, rapid_deceleration, rapid_acceleration = 0, 0, 0
        for i in range(3):
            publish_msg_by_kafka('periodical_journey_update', protobuf_v=18, vid=vid, vin=vin,
                                 sample_points=[{'vehicle_status': {"mileage": mileage + 1},
                                                 'trip_status': {'trip_id': trip_id, 'trip_state': 2,
                                                                 'trip_odometer': i}}])

            nextev_message, driving_behaviour_obj = publish_msg_by_kafka('driving_behaviour_event', protobuf_v=18,
                                                                         vid=vid, vin=vin)

            if driving_behaviour_obj['behaviour'][0] == 0:
                rapid_swerve += 1
            elif driving_behaviour_obj['behaviour'][0] == 1:
                rapid_deceleration += 1
            elif driving_behaviour_obj['behaviour'][0] == 2:
                rapid_acceleration += 1

        # 上报trip_end消息
        publish_msg_by_kafka('trip_end_event', protobuf_v=18, vid=vid, vin=vin,
                             vehicle_status={'mileage': mileage},
                             trip_status={'trip_id': trip_id, 'trip_state': 2, 'trip_odometer': 5})

        publish_msg_by_kafka('journey_end_event', protobuf_v=18, vid=vid, vin=vin, journey_id=trip_id)

        vehicle_trip_in_mysql = mysql['rvs_data'].fetch_one(f'vehicle_trip_history_{vid[:2]}',
                                                            {"trip_id": trip_id},
                                                            suffix='and `max_speed` is not NULL')

        with allure.step("校验vehicle_journey_history会记录行程中急加速等的次数"):
            assert_equal(rapid_swerve, vehicle_trip_in_mysql.pop('rapid_swerve'))
            assert_equal(rapid_deceleration, vehicle_trip_in_mysql.pop('rapid_deceleration'))
            assert_equal(rapid_acceleration, vehicle_trip_in_mysql.pop('rapid_acceleration'))

    def test_journey_update_trip_redis_negative(self, env, vid, redis_key_front, checker, publish_msg, mysql, prepare):
        """

        :param env:
        :param vid:
        :param redis_key_front:
        :param checker:
        :param publish_msg:
        :param mysql:
        :param prepare:
        :return:

        1.上报行程中的周期性事件，只有odometer不小于上一次上报的值是才会更新redis中的trip_status，否则沿用前次上报的trip_status数据
        2.上报行程周期事件中，判断trip_status中的字段trip_state=2(行程开启)的时候才会尝试更新, 否则本次trip_status整体丢弃
        3.补报行程周期事件，trip_first<sample_ts<trip_last这种情况,既不更新trip_first,也不更新trip_last
        """
        trip_id = str(round(time.time()))
        with allure.step("上报事件trip_start_event, protobuf版本18"):
            nextev_message, trip_start_obj = publish_msg('trip_start_event', protobuf_v=18,
                                                         vehicle_status={'mileage': prepare['original_mileage']},
                                                         trip_status={'trip_id': trip_id, 'trip_state': 2,
                                                                      'trip_odometer': 0})

        with allure.step("第一次上报周期行程事件"):
            sample_ts = round(time.time() * 1000)+12000
            nextev_message, journey_update_obj0 = publish_msg('periodical_journey_update', protobuf_v=18,
                                                             sample_points=[{
                                                                 'sample_ts': sample_ts,
                                                                 'vehicle_status': {
                                                                     "mileage": prepare['original_mileage'] + 1},
                                                                 'trip_status': {'trip_id': trip_id, 'trip_state': 2,
                                                                                 'trip_odometer': 10},
                                                                 'driving_data': {
                                                                     'max_speed': 99.0,
                                                                     'min_speed': 10.0
                                                                 }

                                                             }])

        with allure.step("检查redis trip last缓存数据"):
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            key_first = f'{remote_vehicle_key_front}:trip_first:{vid}:{trip_id}'
            key_last = f'{remote_vehicle_key_front}:trip_last:{vid}:{trip_id}'
            trip = checker.redis.get(key_last)
            data = json.loads(trip)

            assert data['soc_status']['soc'] == journey_update_obj0['sample_points'][0]['soc_status']['soc']
            assert data['vehicle_status']['mileage'] == journey_update_obj0['sample_points'][0]['vehicle_status'][
                'mileage']
            assert round(data['position_status']['longitude']) == round(
                journey_update_obj0['sample_points'][0]['position_status']['longitude'])
            assert round(data['position_status']['latitude']) == round(
                journey_update_obj0['sample_points'][0]['position_status']['latitude'])
            assert data['sample_time'] == journey_update_obj0['sample_points'][0]['sample_ts'] // 1000
            assert data['driving_data']['max_speed'] == 99.0
            assert data['driving_data']['min_speed'] == 10.0
            data['trip_status'].pop('sample_time')
            journey_update_obj0['sample_points'][0]['trip_status'].pop('trip_id')
            journey_update_obj0['sample_points'][0]['trip_status'].pop('user_id')
            trip_first = journey_update_obj0['sample_points'][0]['trip_status']
            assert_equal(data['trip_status'], trip_first)

        with allure.step("上报周期行程事件,odometer值小于上次"):
            nextev_message, journey_update_obj = publish_msg('periodical_journey_update', protobuf_v=18,
                                                             sample_points=[{
                                                                 'sample_ts': sample_ts + 2000,
                                                                 'vehicle_status': {
                                                                     "mileage": prepare['original_mileage'] + 1},
                                                                 'trip_status': {'trip_id': trip_id, 'trip_state': 2,
                                                                                 'trip_odometer': 9},
                                                                 'driving_data': {
                                                                     'max_speed': 110.0,
                                                                     'min_speed': 8.0
                                                                 }
                                                             }])

        with allure.step("检查redis trip last中trip_status数据没有改变"):
            trip = checker.redis.get(key_last)
            data = json.loads(trip)

            assert data['soc_status']['soc'] == journey_update_obj['sample_points'][0]['soc_status']['soc']
            assert data['vehicle_status']['mileage'] == journey_update_obj['sample_points'][0]['vehicle_status'][
                'mileage']
            assert round(data['position_status']['longitude']) == round(
                journey_update_obj['sample_points'][0]['position_status']['longitude'])
            assert round(data['position_status']['latitude']) == round(
                journey_update_obj['sample_points'][0]['position_status']['latitude'])
            assert data['sample_time'] == journey_update_obj['sample_points'][0]['sample_ts'] // 1000
            assert data['driving_data']['max_speed'] == 110.0
            assert data['driving_data']['min_speed'] == 8.0
            data['trip_status'].pop('sample_time')
            journey_update_obj['sample_points'][0]['trip_status'].pop('trip_id')
            journey_update_obj['sample_points'][0]['trip_status'].pop('user_id')
            assert_equal(data['trip_status'], trip_first)

        with allure.step("上报周期行程事件,trip_state状态没有开启"):
            nextev_message, journey_update_obj1 = publish_msg('periodical_journey_update', protobuf_v=18,
                                                              sample_points=[{
                                                                  'sample_ts': sample_ts + 4000,
                                                                  'vehicle_status': {
                                                                      "mileage": prepare['original_mileage'] + 2},
                                                                  'trip_status': {'trip_id': trip_id,
                                                                                  'trip_state': random.choice([1, 3]),
                                                                                  'trip_odometer': 19},
                                                                  'driving_data': {
                                                                      'max_speed': 120.0,
                                                                      'min_speed': 5.0
                                                                  }
                                                              }])

        with allure.step("检查redis trip last整个缓存数据没有改变"):
            trip = checker.redis.get(key_last)
            data = json.loads(trip)

            assert data['soc_status']['soc'] == journey_update_obj['sample_points'][0]['soc_status']['soc']
            assert data['vehicle_status']['mileage'] == journey_update_obj['sample_points'][0]['vehicle_status'][
                'mileage']
            assert round(data['position_status']['longitude']) == round(
                journey_update_obj['sample_points'][0]['position_status']['longitude'])
            assert round(data['position_status']['latitude']) == round(
                journey_update_obj['sample_points'][0]['position_status']['latitude'])
            assert data['sample_time'] == journey_update_obj['sample_points'][0]['sample_ts'] // 1000
            assert data['driving_data']['max_speed'] == journey_update_obj['sample_points'][0]['driving_data'][
                'max_speed']
            assert data['driving_data']['min_speed'] == journey_update_obj['sample_points'][0]['driving_data'][
                'min_speed']
            data['trip_status'].pop('sample_time')
            assert_equal(data['trip_status'], trip_first)

        with allure.step("补报周期行程事件，trip_first<sample_ts<trip_last"):
            nextev_message, journey_update_obj2 = publish_msg('periodical_journey_update', protobuf_v=18,
                                                              sample_points=[{
                                                                  'sample_ts': sample_ts + 1000,
                                                                  'vehicle_status': {
                                                                      "mileage": prepare['original_mileage']},
                                                                  'trip_status': {'trip_id': trip_id, 'trip_state': 2,
                                                                                  'trip_odometer': 5},
                                                                  'driving_data': {
                                                                      'max_speed': 119.0,
                                                                      'min_speed': 5.0
                                                                  }
                                                              }])

        with allure.step("检查redis trip last整个缓存数据没有改变"):
            trip = checker.redis.get(key_last)
            data = json.loads(trip)

            assert data['soc_status']['soc'] == journey_update_obj['sample_points'][0]['soc_status']['soc']
            assert data['vehicle_status']['mileage'] == journey_update_obj['sample_points'][0]['vehicle_status'][
                'mileage']
            assert round(data['position_status']['longitude']) == round(
                journey_update_obj['sample_points'][0]['position_status']['longitude'])
            assert round(data['position_status']['latitude']) == round(
                journey_update_obj['sample_points'][0]['position_status']['latitude'])
            assert data['sample_time'] == journey_update_obj['sample_points'][0]['sample_ts'] // 1000
            assert data['driving_data']['max_speed'] == journey_update_obj['sample_points'][0]['driving_data'][
                'max_speed']
            assert data['driving_data']['min_speed'] == journey_update_obj['sample_points'][0]['driving_data'][
                'min_speed']
            data['trip_status'].pop('sample_time')
            assert_equal(data['trip_status'], trip_first)

        with allure.step("上报事件trip_end_event, protobuf版本18"):
            nextev_message, trip_end_obj = publish_msg('trip_end_event', protobuf_v=18, sleep_time=4,
                                                       vehicle_status={'mileage': prepare['original_mileage'] + 3},
                                                       trip_status={'trip_id': trip_id, 'trip_state': 2,
                                                                    'trip_odometer': 20})

        with allure.step("检验mysql rvs_data数据库的存储"):
            trip_in_mysql = mysql['rvs_data'].fetch_one(f'vehicle_trip_history_{vid[:2]}',
                                                        {"vehicle_id": vid,
                                                         'trip_id': trip_id},
                                                        suffix=' and `max_speed` is not NULL')
            # 检查mysql 速度的更新
            assert trip_in_mysql['max_speed'] == round(data['driving_data']['max_speed'], 1)
            assert trip_in_mysql['min_speed'] == round(data['driving_data']['min_speed'], 1)

    def test_journey_remedy_trip_redis_negative(self, env, vid, redis_key_front, checker, publish_msg, mysql, prepare):
        """

        :param env:
        :param vid:
        :param redis_key_front:
        :param checker:
        :param publish_msg:
        :param mysql:
        :param prepare:
        :return:


        1.补报行程周期事件中，判断trip_status中的字段trip_state=2(行程开启)的时候才会尝试更新, 否则本次trip_status整体丢弃
        2.补报行程周期事件，samplets<first, 当前逻辑无论odometer值大小都会更新整个trip first
        """
        trip_id = str(round(time.time()))
        with allure.step("上报事件trip_start_event, protobuf版本18"):
            nextev_message, trip_start_obj = publish_msg('trip_start_event', protobuf_v=18,
                                                         vehicle_status={'mileage': prepare['original_mileage']},
                                                         trip_status={'trip_id': trip_id, 'trip_state': 2,
                                                                      'trip_odometer': 0})

        with allure.step("第一次上报周期行程事件"):
            sample_ts = round(time.time() * 1000)+14000
            nextev_message, journey_update_obj0 = publish_msg('periodical_journey_update', protobuf_v=18,
                                                             sample_points=[{
                                                                 'sample_ts': sample_ts,
                                                                 'vehicle_status': {
                                                                     "mileage": prepare['original_mileage'] + 1},
                                                                 'trip_status': {'trip_id': trip_id, 'trip_state': 2,
                                                                                 'trip_odometer': 10},
                                                                 'driving_data': {
                                                                     'max_speed': 99.0,
                                                                     'min_speed': 10.0
                                                                 }

                                                             }])

        with allure.step("检查redis trip last缓存数据"):
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            key_first = f'{remote_vehicle_key_front}:trip_first:{vid}:{trip_id}'
            key_last = f'{remote_vehicle_key_front}:trip_last:{vid}:{trip_id}'
            trip = checker.redis.get(key_last)
            data = json.loads(trip)

            assert data['soc_status']['soc'] == journey_update_obj0['sample_points'][0]['soc_status']['soc']
            assert data['vehicle_status']['mileage'] == journey_update_obj0['sample_points'][0]['vehicle_status'][
                'mileage']
            assert round(data['position_status']['longitude']) == round(
                journey_update_obj0['sample_points'][0]['position_status']['longitude'])
            assert round(data['position_status']['latitude']) == round(
                journey_update_obj0['sample_points'][0]['position_status']['latitude'])
            assert data['sample_time'] == journey_update_obj0['sample_points'][0]['sample_ts'] // 1000
            assert data['driving_data']['max_speed'] == 99.0
            assert data['driving_data']['min_speed'] == 10.0
            data['trip_status'].pop('sample_time')
            journey_update_obj0['sample_points'][0]['trip_status'].pop('trip_id')
            journey_update_obj0['sample_points'][0]['trip_status'].pop('user_id')
            trip_first = journey_update_obj0['sample_points'][0]['trip_status']
            assert_equal(data['trip_status'], trip_first)

        with allure.step("补报周期行程事件,trip_state状态没有开启"):
            nextev_message, journey_update_obj1 = publish_msg('periodical_journey_update', protobuf_v=18,
                                                              sample_points=[{
                                                                  'sample_ts': sample_ts - 2000,
                                                                  'vehicle_status': {
                                                                      "mileage": prepare['original_mileage'] + 2},
                                                                  'trip_status': {'trip_id': trip_id,
                                                                                  'trip_state': random.choice([1, 3]),
                                                                                  'trip_odometer': 19},
                                                                  'driving_data': {
                                                                      'max_speed': 120.0,
                                                                      'min_speed': 5.0
                                                                  }
                                                              }])

        with allure.step("检查redis trip first整个缓存数据没有改变"):
            trip = checker.redis.get(key_first)
            data = json.loads(trip)

            assert data['soc_status']['soc'] == journey_update_obj0['sample_points'][0]['soc_status']['soc']
            assert data['vehicle_status']['mileage'] == journey_update_obj0['sample_points'][0]['vehicle_status'][
                'mileage']
            assert round(data['position_status']['longitude']) == round(
                journey_update_obj0['sample_points'][0]['position_status']['longitude'])
            assert round(data['position_status']['latitude']) == round(
                journey_update_obj0['sample_points'][0]['position_status']['latitude'])
            assert data['sample_time'] == journey_update_obj0['sample_points'][0]['sample_ts'] // 1000
            assert data['driving_data']['max_speed'] == journey_update_obj0['sample_points'][0]['driving_data'][
                'max_speed']
            assert data['driving_data']['min_speed'] == journey_update_obj0['sample_points'][0]['driving_data'][
                'min_speed']
            data['trip_status'].pop('sample_time')
            assert_equal(data['trip_status'], trip_first)

        with allure.step("补报周期行程事件, odometer大于first"):
            nextev_message, journey_update_obj = publish_msg('periodical_journey_update', protobuf_v=18,
                                                             sample_points=[{
                                                                 'sample_ts': sample_ts - 2000,
                                                                 'vehicle_status': {
                                                                     "mileage": prepare['original_mileage']},
                                                                 'trip_status': {'trip_id': trip_id, 'trip_state': 2,
                                                                                 'trip_odometer': 11},
                                                                 'driving_data': {
                                                                     'max_speed': 90.0,
                                                                     'min_speed': 80.0
                                                                 }
                                                             }])

        with allure.step("检查redis trip first缓存数据仍更新"):
            trip = checker.redis.get(key_first)
            data = json.loads(trip)

            assert data['soc_status']['soc'] == journey_update_obj['sample_points'][0]['soc_status']['soc']
            assert data['vehicle_status']['mileage'] == journey_update_obj['sample_points'][0]['vehicle_status'][
                'mileage']
            assert round(data['position_status']['longitude']) == round(
                journey_update_obj['sample_points'][0]['position_status']['longitude'])
            assert round(data['position_status']['latitude']) == round(
                journey_update_obj['sample_points'][0]['position_status']['latitude'])
            assert data['sample_time'] == journey_update_obj['sample_points'][0]['sample_ts'] // 1000
            assert data['driving_data']['max_speed'] == journey_update_obj0['sample_points'][0]['driving_data'][
                'max_speed']
            assert data['driving_data']['min_speed'] == journey_update_obj0['sample_points'][0]['driving_data'][
                'min_speed']
            data['trip_status'].pop('sample_time')
            journey_update_obj['sample_points'][0]['trip_status'].pop('trip_id')
            journey_update_obj['sample_points'][0]['trip_status'].pop('user_id')
            assert_equal(data['trip_status'], journey_update_obj['sample_points'][0]['trip_status'])

        with allure.step("上报事件trip_end_event, protobuf版本18"):
            nextev_message, trip_end_obj = publish_msg('trip_end_event', protobuf_v=18, sleep_time=4,
                                                       vehicle_status={'mileage': prepare['original_mileage'] + 3},
                                                       trip_status={'trip_id': trip_id, 'trip_state': 2,
                                                                    'trip_odometer': 20})

        with allure.step("检验mysql rvs_data数据库的存储"):
            trip_in_mysql = mysql['rvs_data'].fetch_one(f'vehicle_trip_history_{vid[:2]}',
                                                        {"vehicle_id": vid,
                                                         'trip_id': trip_id},
                                                        suffix=' and `max_speed` is not NULL')
            # 检查mysql 速度的更新
            assert trip_in_mysql['max_speed'] == round(data['driving_data']['max_speed'], 1)
            assert trip_in_mysql['min_speed'] == round(data['driving_data']['min_speed'], 1)

    def test_trip_event_lack_trip_end(self, vid, checker, publish_msg, kafka, mysql, prepare, redis_key_front):
        """

        :param vid:
        :param checker:
        :param publish_msg:
        :param kafka:
        :param mysql:
        :param prepare:
        :param redis_key_front:
        :return:
        上报trip_end事件，如果odometer值不存在或等于0，trip_status的数据不会写入rvs_data数据库的trip_history表，由redis last trip数据补写
        """
        trip_id = str(round(time.time()))
        with allure.step("上报事件trip_start_event, protobuf版本18"):
            start_remaining_range = round(random.randint(500, 2000) * 0.5)
            nextev_message, trip_start_obj = publish_msg('trip_start_event', protobuf_v=18,
                                                         vehicle_status={'mileage': prepare['original_mileage']},
                                                         trip_status={'trip_id': trip_id, 'trip_state': 2},
                                                         soc_status={
                                                             'remaining_range': start_remaining_range})  # rvs_data 表增加start_remaining_range字段

        with allure.step("检验mysql rvs_data数据库的存储"):
            trip_in_mysql = mysql['rvs_data'].fetch_one(f'vehicle_trip_history_{vid[:2]}',
                                                        {'trip_id': trip_id},
                                                        suffix=' and `start_soc` is not NULL')
            assert trip_in_mysql['start_soc'] == trip_start_obj['soc_status']['soc']
            assert trip_in_mysql['start_dump_energy'] == round(trip_start_obj['soc_status']['dump_enrgy'], 1)
            assert trip_in_mysql['start_mileage'] == trip_start_obj['vehicle_status']['mileage']
            # trip_in_mysql存储的经纬度是longitude_gcj02和latitude_gcj02，在Cassandra
            # assert trip_in_mysql['start_longitude'] == trip_start_obj['position_status']['longitude']
            # assert trip_in_mysql['start_latitude'] == trip_start_obj['position_status']['latitude']
            assert trip_in_mysql['is_end'] is None
            assert trip_in_mysql['start_remaining_range'] == start_remaining_range
            assert trip_in_mysql['end_remaining_range'] is None

        with allure.step("上报周期行程事件"):
            nextev_message, journey_update_obj = publish_msg('periodical_journey_update', protobuf_v=18,
                                                             sample_points=[{
                                                                 'sample_ts': round(time.time() * 1000)+13000,
                                                                 'vehicle_status': {
                                                                     "mileage": prepare['original_mileage'] + 1},
                                                                 'trip_status': {'trip_id': trip_id, 'trip_state': 2}

                                                             }, {
                                                                 'sample_ts': round(time.time() * 1000) + 14000,
                                                                 "vehicle_status": {
                                                                     "mileage": prepare['original_mileage'] + 2},
                                                                 'trip_status': {'trip_id': trip_id}

                                                             }])

        with allure.step("检查redis trip first缓存数据"):
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            key_first = f'{remote_vehicle_key_front}:trip_first:{vid}:{trip_id}'
            trip_first = checker.redis.get(key_first)
            data = json.loads(trip_first)

            assert data['soc_status']['soc'] == journey_update_obj['sample_points'][0]['soc_status']['soc']
            assert data['vehicle_status']['mileage'] == journey_update_obj['sample_points'][0]['vehicle_status'][
                'mileage']
            assert round(data['position_status']['longitude']) == round(
                journey_update_obj['sample_points'][0]['position_status']['longitude'])
            assert round(data['position_status']['latitude']) == round(
                journey_update_obj['sample_points'][0]['position_status']['latitude'])
            assert data['sample_time'] == journey_update_obj['sample_points'][0]['sample_ts'] // 1000
            assert round(data['driving_data']['average_speed']) == round(
                journey_update_obj['sample_points'][0]['driving_data']['average_speed'])
            assert round(data['driving_data']['max_speed']) == round(
                journey_update_obj['sample_points'][0]['driving_data']['max_speed'])
            assert round(data['driving_data']['min_speed']) == round(
                journey_update_obj['sample_points'][0]['driving_data']['min_speed'])
            data['trip_status'].pop('sample_time')
            journey_update_obj['sample_points'][0]['trip_status'].pop('trip_id')
            journey_update_obj['sample_points'][0]['trip_status'].pop('user_id')
            assert_equal(data['trip_status'], journey_update_obj['sample_points'][0]['trip_status'])

        with allure.step("上报事件trip_end_event, odometer值不存在或等于0"):
            end_remaining_range = round(random.randint(0, 500) * 0.5)
            nextev_message, trip_end_obj = publish_msg('trip_end_event', protobuf_v=18,
                                                       vehicle_status={'mileage': prepare['original_mileage'] + 3},
                                                       trip_status={'trip_id': trip_id, 'trip_state': 2, 'trip_odometer': 0},
                                                       soc_status={'remaining_range': end_remaining_range})  # rvs_data 表增加end_remaining_range字段

        with allure.step("检验mysql rvs_data数据库的存储"):
            trip_in_mysql = mysql['rvs_data'].fetch_one(f'vehicle_trip_history_{vid[:2]}',
                                                        {'trip_id': trip_id},
                                                        suffix=' and `end_soc` is not NULL')

            assert trip_in_mysql['end_soc'] == trip_end_obj['soc_status']['soc']
            assert trip_in_mysql['end_dump_energy'] == round(trip_end_obj['soc_status']['dump_enrgy'], 1)
            assert trip_in_mysql['end_mileage'] == trip_end_obj['vehicle_status']['mileage']
            assert trip_in_mysql['trip_odometer'] == data['trip_status']['trip_odometer']
            assert trip_in_mysql['trip_eng'] == data['trip_status']['trip_eng']
            assert trip_in_mysql['hv_ass_eng_pct'] == data['trip_status']['hv_ass_eng_pct']
            assert trip_in_mysql['lv_ass_eng_pct'] == data['trip_status']['lv_ass_eng_pct']
            assert trip_in_mysql['dri_eng_pct'] == data['trip_status']['dri_eng_pct']
            assert trip_in_mysql['reg_eng_pct'] == data['trip_status']['reg_eng_pct']
            assert trip_in_mysql['hvh_eng_pct'] == data['trip_status']['hvh_eng_pct']
            assert trip_in_mysql['is_end'] == 1
            assert trip_in_mysql['start_remaining_range'] == start_remaining_range
            assert trip_in_mysql['end_remaining_range'] == end_remaining_range
            # 检查mysql 速度的更新
            period = (trip_end_obj['sample_ts'] - trip_start_obj['sample_ts']) // 1000
            assert trip_in_mysql['avg_speed'] == round(3600 * trip_in_mysql['trip_odometer'] / period, 1)
            assert trip_in_mysql['max_speed'] == round(data['driving_data']['max_speed'], 1)
            assert trip_in_mysql['min_speed'] == round(data['driving_data']['min_speed'], 1)

    def test_trip_event_filter_first_odometer_not_zero(self, vid, checker, publish_msg, kafka, mysql, prepare, redis_key_front):
            """

            :param vid:
            :param checker:
            :param publish_msg:
            :param kafka:
            :param mysql:
            :param prepare:
            :param redis_key_front:
            :return:
            上报第一帧update事件，如果在trip start开始11秒之内并且odometer值大于0，则丢弃，等于0则保存。超过11s之后，按原有逻辑处理。
            """
            trip_id = str(round(time.time()))
            with allure.step("上报事件trip_start_event, protobuf版本18"):
                start_remaining_range = round(random.randint(500, 2000) * 0.5)
                nextev_message, trip_start_obj = publish_msg('trip_start_event', protobuf_v=18,
                                                             vehicle_status={'mileage': prepare['original_mileage']},
                                                             trip_status={'trip_id': trip_id, 'trip_state': 2},
                                                             soc_status={
                                                                 'remaining_range': start_remaining_range})  # rvs_data 表增加start_remaining_range字段

            with allure.step("检验mysql rvs_data数据库的存储"):
                trip_in_mysql = mysql['rvs_data'].fetch_one(f'vehicle_trip_history_{vid[:2]}',
                                                            {'trip_id': trip_id},
                                                            suffix=' and `start_soc` is not NULL')
                assert trip_in_mysql['start_soc'] == trip_start_obj['soc_status']['soc']
                assert trip_in_mysql['start_dump_energy'] == round(trip_start_obj['soc_status']['dump_enrgy'], 1)
                assert trip_in_mysql['start_mileage'] == trip_start_obj['vehicle_status']['mileage']
                # trip_in_mysql存储的经纬度是longitude_gcj02和latitude_gcj02，在Cassandra
                # assert trip_in_mysql['start_longitude'] == trip_start_obj['position_status']['longitude']
                # assert trip_in_mysql['start_latitude'] == trip_start_obj['position_status']['latitude']
                assert trip_in_mysql['is_end'] is None
                assert trip_in_mysql['start_remaining_range'] == start_remaining_range
                assert trip_in_mysql['end_remaining_range'] is None

            with allure.step("第一次上报周期行程事件"):
                nextev_message, journey_update_obj = publish_msg('periodical_journey_update', protobuf_v=18,
                                                                 sample_points=[{
                                                                     'sample_ts': round(time.time() * 1000),
                                                                     'vehicle_status': {
                                                                         "mileage": prepare['original_mileage'] + 1},
                                                                     'trip_status': {'trip_id': trip_id,
                                                                                     'trip_odometer': 1,
                                                                                     'trip_state': 2}}])

            with allure.step("检查redis trip first缓存数据，由于10s内odometer值大于0丢弃"):
                remote_vehicle_key_front = redis_key_front['remote_vehicle']
                key_first = f'{remote_vehicle_key_front}:trip_first:{vid}:{trip_id}'
                trip_first = checker.redis.get(key_first)
                assert trip_first is None

            with allure.step("第二次上报周期行程事件"):
                nextev_message, journey_update_obj = publish_msg('periodical_journey_update', protobuf_v=18,
                                                                 sample_points=[{
                                                                     'sample_ts': round(time.time() * 1000),
                                                                     'vehicle_status': {
                                                                         "mileage": prepare['original_mileage']},
                                                                     'trip_status': {'trip_id': trip_id,
                                                                                     'trip_odometer': 0.0,
                                                                                     'trip_state': 2},
                                                                     'driving_data': {
                                                                         'max_speed': 29.0,
                                                                         'min_speed': 18.0
                                                                     }}])

            with allure.step("检查redis trip first缓存数据，由于10s内odometer值等于0保存"):
                trip_first = checker.redis.get(key_first)
                data = json.loads(trip_first)

                assert data['soc_status']['soc'] == journey_update_obj['sample_points'][0]['soc_status']['soc']
                assert data['vehicle_status']['mileage'] == journey_update_obj['sample_points'][0]['vehicle_status'][
                    'mileage']
                assert round(data['position_status']['longitude']) == round(
                    journey_update_obj['sample_points'][0]['position_status']['longitude'])
                assert round(data['position_status']['latitude']) == round(
                    journey_update_obj['sample_points'][0]['position_status']['latitude'])
                assert data['sample_time'] == journey_update_obj['sample_points'][0]['sample_ts'] // 1000
                assert round(data['driving_data']['average_speed']) == round(
                    journey_update_obj['sample_points'][0]['driving_data']['average_speed'])
                assert round(data['driving_data']['max_speed']) == round(
                    journey_update_obj['sample_points'][0]['driving_data']['max_speed'])
                assert round(data['driving_data']['min_speed']) == round(
                    journey_update_obj['sample_points'][0]['driving_data']['min_speed'])
                data['trip_status'].pop('sample_time')
                journey_update_obj['sample_points'][0]['trip_status'].pop('trip_id')
                journey_update_obj['sample_points'][0]['trip_status'].pop('user_id')
                assert_equal(data['trip_status'], journey_update_obj['sample_points'][0]['trip_status'])

            with allure.step("第三次上报周期行程事件"):
                nextev_message, journey_update_obj1 = publish_msg('periodical_journey_update', protobuf_v=18,
                                                                  sample_points=[{
                                                                     'sample_ts': round(time.time() * 1000),
                                                                     'vehicle_status': {
                                                                         "mileage": prepare['original_mileage'] + 1},
                                                                     'trip_status': {'trip_id': trip_id,
                                                                                     'trip_odometer': 0.4,
                                                                                     'trip_state': 2}}])

            with allure.step("检查redis last first缓存数据，由于10s内odometer值大于0不保存"):
                remote_vehicle_key_front = redis_key_front['remote_vehicle']
                key_last = f'{remote_vehicle_key_front}:trip_last:{vid}:{trip_id}'
                trip_last = checker.redis.get(key_last)
                data = json.loads(trip_last)

                assert data['soc_status']['soc'] == journey_update_obj['sample_points'][0]['soc_status']['soc']
                assert data['vehicle_status']['mileage'] == journey_update_obj['sample_points'][0]['vehicle_status'][
                    'mileage']
                assert round(data['position_status']['longitude']) == round(
                    journey_update_obj['sample_points'][0]['position_status']['longitude'])
                assert round(data['position_status']['latitude']) == round(
                    journey_update_obj['sample_points'][0]['position_status']['latitude'])
                assert data['sample_time'] == journey_update_obj['sample_points'][0]['sample_ts'] // 1000
                assert round(data['driving_data']['average_speed']) == round(
                    journey_update_obj['sample_points'][0]['driving_data']['average_speed'])
                assert round(data['driving_data']['max_speed']) == round(
                    journey_update_obj['sample_points'][0]['driving_data']['max_speed'])
                assert round(data['driving_data']['min_speed']) == round(
                    journey_update_obj['sample_points'][0]['driving_data']['min_speed'])
                data['trip_status'].pop('sample_time')
                assert_equal(data['trip_status'], journey_update_obj['sample_points'][0]['trip_status'])

            with allure.step("补报周期行程事件"):
                nextev_message, journey_update_obj1 = publish_msg('periodical_journey_update', protobuf_v=18,
                                                                  sample_points=[{
                                                                     'sample_ts': round(time.time() * 1000)-10000,
                                                                     'vehicle_status': {
                                                                         "mileage": prepare['original_mileage'] + 1},
                                                                     'trip_status': {'trip_id': trip_id,
                                                                                     'trip_odometer': 0.3,
                                                                                     'trip_state': 2}}])

            with allure.step("检查redis trip first缓存数据，由于在行程开始10s之内不更新"):
                trip_first = checker.redis.get(key_first)
                data = json.loads(trip_first)

                assert data['soc_status']['soc'] == journey_update_obj['sample_points'][0]['soc_status']['soc']
                assert data['vehicle_status']['mileage'] == journey_update_obj['sample_points'][0]['vehicle_status'][
                    'mileage']
                assert round(data['position_status']['longitude']) == round(
                    journey_update_obj['sample_points'][0]['position_status']['longitude'])
                assert round(data['position_status']['latitude']) == round(
                    journey_update_obj['sample_points'][0]['position_status']['latitude'])
                assert data['sample_time'] == journey_update_obj['sample_points'][0]['sample_ts'] // 1000
                assert round(data['driving_data']['average_speed']) == round(
                    journey_update_obj['sample_points'][0]['driving_data']['average_speed'])
                assert round(data['driving_data']['max_speed']) == round(
                    journey_update_obj['sample_points'][0]['driving_data']['max_speed'])
                assert round(data['driving_data']['min_speed']) == round(
                    journey_update_obj['sample_points'][0]['driving_data']['min_speed'])
                data['trip_status'].pop('sample_time')
                assert_equal(data['trip_status'], journey_update_obj['sample_points'][0]['trip_status'])

            with allure.step("第四次上报周期行程事件"):
                nextev_message, journey_update_obj0 = publish_msg('periodical_journey_update', protobuf_v=18,
                                                                  sample_points=[{
                                                                     'sample_ts': round(time.time() * 1000)+18000,
                                                                     'vehicle_status': {
                                                                         "mileage": prepare['original_mileage'] + 1},
                                                                     'trip_status': {'trip_id': trip_id,
                                                                                     'trip_odometer': 15,
                                                                                     'trip_state': 2},
                                                                     'driving_data': {
                                                                         'max_speed': 99.0,
                                                                         'min_speed': 10.0
                                                                     }}])

            with allure.step("检查redis trip last缓存数据，由于已超过行程开始10s不过滤"):
                trip_last = checker.redis.get(key_last)
                data = json.loads(trip_last)

                assert data['soc_status']['soc'] == journey_update_obj0['sample_points'][0]['soc_status']['soc']
                assert data['vehicle_status']['mileage'] == journey_update_obj0['sample_points'][0]['vehicle_status'][
                    'mileage']
                assert round(data['position_status']['longitude']) == round(
                    journey_update_obj0['sample_points'][0]['position_status']['longitude'])
                assert round(data['position_status']['latitude']) == round(
                    journey_update_obj0['sample_points'][0]['position_status']['latitude'])
                assert data['sample_time'] == journey_update_obj0['sample_points'][0]['sample_ts'] // 1000
                assert round(data['driving_data']['average_speed']) == round(
                    journey_update_obj0['sample_points'][0]['driving_data']['average_speed'])
                assert round(data['driving_data']['max_speed']) == round(
                    journey_update_obj0['sample_points'][0]['driving_data']['max_speed'])
                assert round(data['driving_data']['min_speed']) == round(
                    journey_update_obj0['sample_points'][0]['driving_data']['min_speed'])
                data['trip_status'].pop('sample_time')
                journey_update_obj0['sample_points'][0]['trip_status'].pop('trip_id')
                journey_update_obj0['sample_points'][0]['trip_status'].pop('user_id')
                assert_equal(data['trip_status'], journey_update_obj0['sample_points'][0]['trip_status'])

            with allure.step("上报事件trip_end_event"):
                end_remaining_range = round(random.randint(0, 500) * 0.5)
                nextev_message, trip_end_obj = publish_msg('trip_end_event', protobuf_v=18,
                                                           sample_ts=round(time.time() * 1000) + 14000,
                                                           vehicle_status={'mileage': prepare['original_mileage'] + 3},
                                                           trip_status={'trip_id': trip_id, 'trip_state': 2,
                                                                        'trip_odometer': 0},
                                                           soc_status={
                                                               'remaining_range': end_remaining_range})  # rvs_data 表增加end_remaining_range字段

            with allure.step("检验mysql rvs_data数据库的存储"):
                trip_in_mysql = mysql['rvs_data'].fetch_one(f'vehicle_trip_history_{vid[:2]}',
                                                            {'trip_id': trip_id},
                                                            suffix=' and `end_soc` is not NULL')

                assert trip_in_mysql['end_soc'] == trip_end_obj['soc_status']['soc']
                assert trip_in_mysql['end_dump_energy'] == round(trip_end_obj['soc_status']['dump_enrgy'], 1)
                assert trip_in_mysql['end_mileage'] == trip_end_obj['vehicle_status']['mileage']
                assert trip_in_mysql['trip_odometer'] == data['trip_status']['trip_odometer']
                assert trip_in_mysql['trip_eng'] == data['trip_status']['trip_eng']
                assert trip_in_mysql['hv_ass_eng_pct'] == data['trip_status']['hv_ass_eng_pct']
                assert trip_in_mysql['lv_ass_eng_pct'] == data['trip_status']['lv_ass_eng_pct']
                assert trip_in_mysql['dri_eng_pct'] == data['trip_status']['dri_eng_pct']
                assert trip_in_mysql['reg_eng_pct'] == data['trip_status']['reg_eng_pct']
                assert trip_in_mysql['hvh_eng_pct'] == data['trip_status']['hvh_eng_pct']
                assert trip_in_mysql['is_end'] == 1
                assert trip_in_mysql['start_remaining_range'] == start_remaining_range
                assert trip_in_mysql['end_remaining_range'] == end_remaining_range
                # 检查mysql 速度的更新
                period = (trip_end_obj['sample_ts'] - trip_start_obj['sample_ts']) // 1000
                assert trip_in_mysql['avg_speed'] == round(3600 * trip_in_mysql['trip_odometer'] / period, 1)
                assert trip_in_mysql['max_speed'] == round(data['driving_data']['max_speed'], 1)
                assert trip_in_mysql['min_speed'] == round(data['driving_data']['min_speed'], 1)

    def test_trip_end_event_region(self, env, mysql, publish_msg_by_kafka):
        """
        http://venus.nioint.com/#/detailWorkflow/wf-20211101171107-tB
        slytherin版本1.0.172.1bdca2b之后，充电结束时，调gis接口用充电结束上报的经纬度来获取区域位置信息，填充vehicle_trip_history表中的area code字段
        gis接口：http://showdoc.nevint.com/index.php?s=/sas&page_id=13065
        :param env:
        :param mysql:
        :param publish_msg_by_kafka:
        :return:
        """
        vid = env['vehicles']['v_statistic_1']['vehicle_id']
        vin = env['vehicles']['v_statistic_1']['vin']
        trip_id = str(round(time.time()))
        mileage = mysql['rvs'].fetch_one('status_vehicle', {"id": vid})['mileage']
        # 上报行程开始
        publish_msg_by_kafka('trip_start_event', protobuf_v=18, vid=vid, vin=vin,
                             vehicle_status={'mileage': mileage},
                             trip_status={'trip_id': trip_id, 'trip_state': 2, 'trip_odometer': 0})
        # 上报journey update
        publish_msg_by_kafka('periodical_journey_update', protobuf_v=18, vid=vid, vin=vin,
                             sample_points=[{'vehicle_status': {"mileage": mileage + 1},
                                             'trip_status': {'trip_id': trip_id, 'trip_state': 2,
                                                             'trip_odometer': 1}}])
        # 上报行程结束
        nextev_message, trip_end_obj = publish_msg_by_kafka('trip_end_event', protobuf_v=18, vid=vid, vin=vin,
                                                            vehicle_status={'mileage': mileage},
                                                            trip_status={'trip_id': trip_id, 'trip_state': 2, 'trip_odometer': 5})
        with allure.step("从vehicle_trip_history表中查询行程记录"):
            vehicle_trip_in_mysql = mysql['rvs_data'].fetch_one(f'vehicle_trip_history_{vid[:2]}',
                                                                {"trip_id": trip_id},
                                                                suffix='and `end_area_code` is not NULL')
            vehicle_navigation_in_mysql = mysql['rvs'].fetch_one('vehicle_navigation',
                                                        {"id": vid, 'update_time>': timestamp_to_utc_strtime(trip_end_obj['sample_ts'])})

        with allure.step("调用gis接口，用经纬度来查询区域信息"):
            inputs = {
                "host": env['host']['gis_in'],
                "method": "GET",
                "path": "/v2/in/map/local/rgeo",
                "params": {
                    'app_id': 10001,
                    'location': f"{vehicle_trip_in_mysql['start_longitude']},{vehicle_trip_in_mysql['start_latitude']}",
                    "sign": ''
                }
            }
            region_data = hreq.request(env, inputs)

            assert_equal(vehicle_trip_in_mysql['start_area_code'], region_data['data']['area_code'])
            inputs = {
                "host": env['host']['gis_in'],
                "method": "GET",
                "path": "/v2/in/map/local/rgeo",
                "params": {
                    'app_id': 10001,
                    'location': f"{vehicle_trip_in_mysql['end_longitude']},{vehicle_trip_in_mysql['end_latitude']}",
                    "sign": ''
                }
            }
            region_data = hreq.request(env, inputs)
            assert_equal(vehicle_trip_in_mysql['end_area_code'], region_data['data']['area_code'])

        with allure.step("验证vehicle_navigation表中区域信息按照gis接口返回更新"):
            assert_equal(vehicle_navigation_in_mysql['province'], region_data['data']['province'])
            assert_equal(vehicle_navigation_in_mysql['city'], region_data['data']['city'])
            assert_equal(vehicle_navigation_in_mysql['district'], region_data['data']['district'])

    def test_trip_end_event_region_no_position(self, env, mysql, publish_msg_by_kafka):
        """
        http://venus.nioint.com/#/detailWorkflow/wf-20211101171107-tB
        slytherin版本1.0.172.1bdca2b之后，行程结束时，调gis接口用行程结束上报的经纬度来获取区域位置信息，填充vehicle_trip_history表中的area code字段
        如果结束未上报经纬度或经纬度非法，则调用data report接口来替代。
        :param env:
        :param mysql:
        :param publish_msg_by_kafka:
        :return:
        """
        vid = env['vehicles']['v_statistic_1']['vehicle_id']
        vin = env['vehicles']['v_statistic_1']['vin']
        trip_id = str(round(time.time()))
        mileage = mysql['rvs'].fetch_one('status_vehicle', {"id": vid})['mileage']
        # 上报行程开始
        start_time = int(time.time() * 1000)
        publish_msg_by_kafka('trip_start_event', protobuf_v=18, vid=vid, vin=vin,
                             vehicle_status={'mileage': mileage},
                             clear_fields=['position_status.longitude', 'position_status.latitude'],
                             trip_status={'trip_id': trip_id, 'trip_state': 2, 'trip_odometer': 0})

        # 校验调用接口补充开始位置数据
        inputs = {
            "host": env['host']['tsp_in'],
            "method": "GET",
            "path": f"/api/1/in/data/vehicle/{vid}/journey/track/newest",
            "params": {
                'app_id': 10001,
                'inquire_time': start_time // 1000,
                "sign": ''
            },
            "timeout": 5.0
        }
        start_data = hreq.request(env, inputs)

        # 上报journey update
        publish_msg_by_kafka('periodical_journey_update', protobuf_v=18, vid=vid, vin=vin,
                             sample_points=[{'vehicle_status': {"mileage": mileage + 1},
                                             'trip_status': {'trip_id': trip_id, 'trip_state': 2,
                                                             'trip_odometer': 1}}])

        # 上报行程结束
        end_time = int(time.time() * 1000)
        nextev_message, trip_end_obj = publish_msg_by_kafka('trip_end_event', protobuf_v=18, vid=vid, vin=vin,
                                                            vehicle_status={'mileage': mileage},
                                                            clear_fields=['position_status.longitude', 'position_status.latitude'],
                                                            trip_status={'trip_id': trip_id, 'trip_state': 2, 'trip_odometer': 5})
        # 校验调用接口补充结束位置数据
        inputs = {
            "host": env['host']['tsp_in'],
            "method": "GET",
            "path": f"/api/1/in/data/vehicle/{vid}/journey/track/newest",
            "params": {
                'app_id': 10001,
                'inquire_time': end_time // 1000,
                "sign": ''
            }
        }
        end_data = hreq.request(env, inputs)

        with allure.step("从vehicle_trip_history表中查询行程记录"):
            vehicle_trip_in_mysql = mysql['rvs_data'].fetch_one(f'vehicle_trip_history_{vid[:2]}',
                                                                {"trip_id": trip_id},
                                                                suffix='and `end_area_code` is not NULL')
            vehicle_navigation_in_mysql = mysql['rvs'].fetch_one('vehicle_navigation',
                                                        {"id": vid, 'update_time>': timestamp_to_utc_strtime(trip_end_obj['sample_ts'])})

        with allure.step("验证补充位置数据正确"):
            assert_equal(vehicle_trip_in_mysql['start_longitude'], start_data['data']['track'][0]['longitude'])
            assert_equal(vehicle_trip_in_mysql['start_latitude'], start_data['data']['track'][0]['latitude'])
            assert_equal(vehicle_trip_in_mysql['end_longitude'], end_data['data']['track'][0]['longitude'])
            assert_equal(vehicle_trip_in_mysql['end_latitude'], end_data['data']['track'][0]['latitude'])

        with allure.step("调用gis接口，用经纬度来查询区域信息"):
            inputs = {
                "host": env['host']['gis_in'],
                "method": "GET",
                "path": "/v2/in/map/local/rgeo",
                "params": {
                    'app_id': 10001,
                    'location': f"{vehicle_trip_in_mysql['start_longitude']},{vehicle_trip_in_mysql['start_latitude']}",
                    "sign": ''
                }
            }
            region_data = hreq.request(env, inputs)

            assert_equal(vehicle_trip_in_mysql['start_area_code'], region_data['data']['area_code'])
            inputs = {
                "host": env['host']['gis_in'],
                "method": "GET",
                "path": "/v2/in/map/local/rgeo",
                "params": {
                    'app_id': 10001,
                    'location': f"{vehicle_trip_in_mysql['end_longitude']},{vehicle_trip_in_mysql['end_latitude']}",
                    "sign": ''
                }
            }
            region_data = hreq.request(env, inputs)
            assert_equal(vehicle_trip_in_mysql['end_area_code'], region_data['data']['area_code'])

        with allure.step("验证vehicle_navigation表中区域信息按照gis接口返回更新"):
            assert_equal(vehicle_navigation_in_mysql['province'], region_data['data']['province'])
            assert_equal(vehicle_navigation_in_mysql['city'], region_data['data']['city'])
            assert_equal(vehicle_navigation_in_mysql['district'], region_data['data']['district'])

    @pytest.mark.skip('manual')
    def test_remedy_trip(self):
        """
        slytherin会有定时job每天执行，补全过去12小时到24小时之间的trip记录
        也可以进入slytherin pod，调用接口来触发job执行
        wget http://localhost:8061/remedy/trip
        :return:
        """

    @pytest.mark.skip('manual')
    def test_remedy_trip_by_cassandra(self, env, redis_key_front, checker, publish_msg_by_kafka, mysql):
        """
        trip数据补偿https://jira.nioint.com/browse/CVS-15929
        redis分布式key remote_vehicle_test:trip_remedy:{{vidPrefix}}(redis单机上)
        hot config key : rvs.trip.remedy

        从Cassandra补数据

        config map:
        开始时间：trip.remedy.start.timestamp
        结束时间：trip.remedy.end.timestamp(毫秒级时间戳)
        test用多个pod测试

        测试步骤：
        1.先运行本条测试用例，上报trip行程
        2.将mysql rvs_data数据库中刚才上报的trip数据导出，然后从数据库中删除这些数据
        3.更改hot config key : rvs.trip.remedy 为true
        4.删除redis key remote_vehicle_test:trip_remedy:0（vid的第一位数）
        5.在config map设置trip.remedy.{start|end}.timestamp要补数据所在的时间段
        6.重新发布slytherin服务
        7.检查刚才删除的trip数据是否被恢复，其中车速、区域码不做恢复
        8.与之前导出的数据逐条比较恢复的数据是否正确
        """
        vids = ['010274764cc24db981d91801732d6b3b','020578ebe1804535ad4a88f6d11a76a3','0302954b03634f58976b348ddb0c76f2','0404d3fc5493400c8f3b39d67d4e6421','052cf0f481e643d68133b5675eca555a']
        vins = ['SQETEST0365844412','SQETEST0664204474','SQETEST0042503256','SQETEST0006659610','SQETEST0160191785']
        for i in range(60):
            vid = vids[i % 5]
            vin = vins[i % 5]
            trip_id = str(round(time.time()))
            mileage = mysql['rvs'].fetch('status_vehicle', {"id": vid}, retry_num=0)[0]['mileage']

            # 构造并上报消息
            publish_msg_by_kafka('journey_start_event', protobuf_v=18, vid=vid, vin=vin, journey_id=trip_id)

            publish_msg_by_kafka('trip_start_event', protobuf_v=18, vid=vid, vin=vin,
                                 vehicle_status={'mileage': mileage},
                                 trip_status={'trip_id': trip_id, 'trip_state': 2, 'trip_odometer': 0})

            # 上报周期行程事件和驾驶行为事件
            rapid_swerve, rapid_deceleration, rapid_acceleration = 0, 0, 0
            for i in range(3):
                publish_msg_by_kafka('periodical_journey_update', protobuf_v=18, vid=vid, vin=vin,
                                     sample_points=[{'vehicle_status': {"mileage": mileage + 1},
                                                     'trip_status': {'trip_id': trip_id, 'trip_state': 2,
                                                                     'trip_odometer': i}}])

                nextev_message, driving_behaviour_obj = publish_msg_by_kafka('driving_behaviour_event', protobuf_v=18,
                                                                             vid=vid, vin=vin)

                if driving_behaviour_obj['behaviour'][0] == 0:
                    rapid_swerve += 1
                elif driving_behaviour_obj['behaviour'][0] == 1:
                    rapid_deceleration += 1
                elif driving_behaviour_obj['behaviour'][0] == 2:
                    rapid_acceleration += 1

            # 上报trip_end消息
            publish_msg_by_kafka('trip_end_event', protobuf_v=18, vid=vid, vin=vin,
                                 vehicle_status={'mileage': mileage},
                                 trip_status={'trip_id': trip_id, 'trip_state': 2, 'trip_odometer': 50})

            publish_msg_by_kafka('journey_end_event', protobuf_v=18, vid=vid, vin=vin, journey_id=trip_id)
