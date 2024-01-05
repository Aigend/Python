#!/usr/bin/env python
# coding=utf-8


import random
import time
import json
import pytest
import allure

from nio_messages import wti
from utils.assertions import assert_equal

index_names = [['WTI-BMS-2', 'WTI-BC-6', 'WTI-ADAS-11'], ['WTI-EP-17', 'WTI-EP-2', 'WTI-BMS-4'], ['WTI-CT-1','WTI-CT-2','WTI-PA-15'],
               ['WTI-BMS-3', 'WTI-BSD-1', 'WTI-FCTA-1'], ['WTI-FCTA-2', 'WTI-SA-1', 'WTI-BMS-8'],
               ['WTI-TPMS-28', 'WTI-TPMS-27', 'WTI-EP-31'], ['WTI-TPMS-26', 'WTI-TPMS-25', 'WTI-SCM-1'],
               ['WTI-SB-1', 'WTI-LGHT-65', 'WTI-LGHT-66'], ['WTI-VSTS-7', 'WTI-VSTS-8', 'WTI-ECTRL-3'],
               ['WTI-SA-7','WTI-SA-8','WTI-SA-9'],['WTI-SA-10','WTI-PBRK-7','WTI-PBRK-8'],['WTI-PBRK-12','WTI-PBRK-13','WTI-PBRK-14']]


class TestAlarmSignalUpdate(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, mysql):
        original_mileage_in_mysql = mysql['rvs'].fetch('status_vehicle',
                                                       {"id": vid
                                                        },
                                                       ['mileage']
                                                       )[0]['mileage']

        return {'original_mileage': original_mileage_in_mysql}

    def test_wont_update_status(self, vid, checker, redis_key_front, publish_msg, prepare):
        with allure.step("校验alarm signal update事件的position等不落库到redis，因为它的数据不能保证正确性"):
            # 支持staging环境
            # cmdopt = 'staging' if cmdopt == 'stg' else cmdopt
            keys = ['PositionStatus', 'DrivingData', 'TyreStatus',
                    'OccupantStatus', 'BmsStatus', 'SocStatus', 'HvacStatus',
                    'ExteriorStatus', 'ExtremumData', 'DrivingMotor']
            # 支持马克波罗服务测试
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            key_front = f'{remote_vehicle_key_front}:vehicle_status:{vid}'
            old_status = {key: checker.redis.get(f'{key_front}:{key}') for key in keys}

            # 构造并上报消息
            nextev_message, alarm_signal_update_obj = publish_msg('alarm_signal_update_event',
                                                                  sample_points={'vehicle_status': {
                                                                      "mileage": prepare['original_mileage'] + 1}},
                                                                  sleep_time=2
                                                                  )
            new_status = {key: checker.redis.get(f'{key_front}:{key}') for key in keys}
            # 校验
            assert_equal(new_status, old_status)

    @pytest.mark.skip  # opened_wti redis key已废弃，不做处理
    def test_opened_wti(self, checker, vid, publish_msg_by_kafka, redis_key_front):
        """
        当calarm_signal为空时，只会关闭开启时间在上报时间sample_time之前的wti，
        只有全部打开的wti都关闭时，才将has_wti_tag(remote_vehicle_{env}:opened_wti:{vid})置为0。
        若只关闭部分，仍为1
        """
        with allure.step("校验alarm wti不为空时，redis中opened_wti的值为1"):
            # here we want to choose alarm which is wti_enabled
            signal_int = []
            sample_ts = round(time.time() * 1000)
            for i in range(3):
                while True:
                    s = random.choice(wti.SIGNAL)
                    # 带note标记的都是比较特殊的wti，此处随机选一个的时候不选它
                    if 'note' in s or s in signal_int:
                        continue
                    is_wti_enabled = checker.mysql.fetch('const_wti',
                                                         where_model={"wti_code": s['wti_code']},
                                                         fields=['wti_enabled'])[0]['wti_enabled']
                    if is_wti_enabled == 0:
                        continue
                    s['sn'] = str(sample_ts - 1000 * i)
                    signal_int.append(s)
                    break
            # 构造并上报消息
            publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': signal_int},
                                 sample_ts=sample_ts)
            # 检验
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            keyword = remote_vehicle_key_front + ':opened_wti:' + vid
            opened_wti_in_redis = checker.redis.get(keyword)
            assert_equal(opened_wti_in_redis, "1")

        with allure.step("校验alarm wti为空时，只会关闭开启时间在上报时间sample_time之前的，redis中opened_wti的值仍然为1"):
            # 关闭了一个最早的wti
            publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': []},
                                 sample_ts=sample_ts - 1500)
            # 检验
            opened_wti_in_redis = checker.redis.get(keyword)
            assert_equal(opened_wti_in_redis, "1")

        with allure.step("校验alarm wti为空时，且将wti全部关闭时，redis中opened_wti的值为0"):
            # 关闭所有的wti
            publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': []})
            # 检验
            opened_wti_in_redis = checker.redis.get(keyword)
            assert_equal(opened_wti_in_redis, "0")

    def test_ignore_wti(self, vin, vid, publish_msg_by_kafka, checker, redis, redis_key_front):
        """
        wti针对指定车的指定wti的过滤
        redis key remote_vehicle_{env}:ignore_wti:{vid}
        """
        # here we want to choose alarm which is wti_enabled
        signal_int = []
        while True:
            s = random.choice(wti.SIGNAL)
            # 带note标记的都是比较特殊的wti，此处随机选一个的时候不选它
            if 'note' in s:
                continue
            is_wti_enabled = checker.mysql.fetch('const_wti',
                                                 where_model={"wti_code": s['wti_code']},
                                                 fields=['wti_enabled'])[0]['wti_enabled']
            if is_wti_enabled == 0:
                continue

            signal_int.append(s)
            break
        remote_vehicle_key_front = redis_key_front['remote_vehicle']
        key = f"{remote_vehicle_key_front}:ignore_wti:{vid}"
        redis['cluster'].set_sadd(key, signal_int[0]['wti_code'])
        nextev_message, obj_start = publish_msg_by_kafka('alarm_signal_update_event',
                                                         alarm_signal={'signal_int': signal_int}, sleep_time=2)

        # 清除WTI
        nextev_message, obj_end = publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': []},
                                                       sleep_time=2)
        with allure.step('校验该wti不会存history_wti_alarm表'):
            sn = obj_start['alarm_signal']['signal_int'][0]['sn']
            alarm_id = '{}-{}-{}-WTI'.format(vin, sn, signal_int[0]['wti_code'][4:])
            history_wti = checker.mysql.fetch('history_wti_alarm', {"vehicle_id": vid, 'alarm_id': alarm_id})
            assert_equal(len(history_wti), 0)

        # case结束后清除redis里忽略的wti
        redis['cluster'].delete(key)

    def test_alarm_signal_update_by_index(self, vin, vid, redis_key_front, publish_msg_by_kafka, checker, cmdopt):
        signal_names = random.choice(index_names)
        # here we want to traversal all wti report with index
        signal_int = []
        sample_ts = round(time.time() * 1000)
        for i in range(3):
            s = list(filter(lambda x: x['name'] == signal_names[i], wti.SIGNAL))
            s[0]['sn'] = str(sample_ts - 1000 * i)
            signal_int.append(s[0])
        # 构造并上报消息
        nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': signal_int},
                                                   sample_ts=sample_ts)

        # 检验
        alarm_id_list = [
            '{}-{}-{}-WTI'.format(vid if 'marcopolo' in cmdopt else vin,
                                  obj['alarm_signal']['signal_int'][i]['sn'], item['wti_code'][4:])
            for i, item in enumerate(signal_int)]
        alarm_id_list.sort()
        remote_vehicle_key_front = redis_key_front['remote_vehicle']
        keyword = remote_vehicle_key_front + ':happen_wti:' + vid
        for i in range(10):
            time.sleep(2)
            happen_wti_in_redis = json.loads(checker.redis.get(keyword))
            happen_wti_in_redis.sort()
            if alarm_id_list == happen_wti_in_redis:
                assert True
                break
            if i == 9:
                assert False

        with allure.step("校验alarm wti为空时，只会关闭开启时间在上报时间sample_time之前的，redis中happen_wti更新"):
            # 关闭了一个最早的wti
            publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': []},
                                 sample_ts=sample_ts - 1500)
            # 检验
            del(signal_int[2])
            alarm_id_list = [
                '{}-{}-{}-WTI'.format(vid if 'marcopolo' in cmdopt else vin,
                                      obj['alarm_signal']['signal_int'][i]['sn'], item['wti_code'][4:])
                for i, item in enumerate(signal_int)]
            alarm_id_list.sort()
            for i in range(10):
                time.sleep(2)
                happen_wti_in_redis = json.loads(checker.redis.get(keyword))
                happen_wti_in_redis.sort()
                if alarm_id_list == happen_wti_in_redis:
                    assert True
                    break
                if i == 9:
                    assert False

        with allure.step("校验alarm wti为空时，且将wti全部关闭时，redis中happen_wti为空"):
            # 关闭所有的wti
            publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': []})
            # 检验
            happen_wti_in_redis = checker.redis.get(keyword)
            for i in range(10):
                time.sleep(2)
                if len(json.loads(happen_wti_in_redis)) == 0:
                    assert True
                    break
                if i == 9:
                    assert False

    def test_happen_wti(self, checker, vin, vid, publish_msg_by_kafka, redis_key_front, mysql, cmdopt):
        """
        wti查询已开启故障，改为读redis，key为："redis_key_front:happen_wti:vid"
        查询已开启故障逻辑：如果redis的结果为null，从mysql读，然后将alarm_id写入redis，每次关闭和开启故障，均需向redis中删除和插入alarm_id
        """
        with allure.step("校验alarm wti开启时，redis中happen_wti的值保存alarm id"):
            # here we want to choose alarm which is wti_enabled
            signal_int = []
            sample_ts = round(time.time() * 1000)
            for i in range(2):
                while True:
                    s = random.choice(wti.SIGNAL)
                    # 带note标记的都是比较特殊的wti，此处随机选一个的时候不选它
                    if 'note' in s or s in signal_int:
                        continue
                    is_wti_enabled = checker.mysql.fetch('const_wti',
                                                         where_model={"wti_code": s['wti_code']},
                                                         fields=['wti_enabled'])[0]['wti_enabled']
                    if is_wti_enabled == 0:
                        continue
                    s['sn'] = str(sample_ts - 1000 * i)
                    signal_int.append(s)
                    break
            # 构造并上报消息
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': signal_int},
                                                       sample_ts=sample_ts)
            # 检验
            alarm_id_list = [
                '{}-{}-{}-WTI'.format(vid if 'marcopolo' in cmdopt else vin,
                                      obj['alarm_signal']['signal_int'][i]['sn'], item['wti_code'][4:])
                for i, item in enumerate(signal_int)]
            alarm_id_list.sort()
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            keyword = remote_vehicle_key_front + ':happen_wti:' + vid
            for i in range(10):
                time.sleep(2)
                happen_wti_in_redis = json.loads(checker.redis.get(keyword))
                happen_wti_in_redis.sort()
                if alarm_id_list == happen_wti_in_redis:
                    assert True
                    break
                if i == 9:
                    assert False

        with allure.step("校验alarm wti更新时，redis中happen_wti的值保存alarm id更新"):
            # here we want to choose alarm which is wti_enabled
            signal_int.clear()
            sample_ts = round(time.time() * 1000)
            for i in range(3):
                while True:
                    s = random.choice(wti.SIGNAL)
                    # 带note标记的都是比较特殊的wti，此处随机选一个的时候不选它
                    if 'note' in s or s in signal_int:
                        continue
                    is_wti_enabled = checker.mysql.fetch('const_wti',
                                                         where_model={"wti_code": s['wti_code']},
                                                         fields=['wti_enabled'])[0]['wti_enabled']
                    if is_wti_enabled == 0:
                        continue
                    s['sn'] = str(sample_ts - 1000 * i)
                    signal_int.append(s)
                    break
            # 构造并上报消息
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': signal_int},
                                                       sample_ts=sample_ts)
            # 检验
            alarm_id_list = [
                '{}-{}-{}-WTI'.format(vid if 'marcopolo' in cmdopt else vin,
                                      obj['alarm_signal']['signal_int'][i]['sn'], item['wti_code'][4:])
                for i, item in enumerate(signal_int)]
            alarm_id_list.sort()
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            keyword = remote_vehicle_key_front + ':happen_wti:' + vid
            for i in range(10):
                time.sleep(2)
                happen_wti_in_redis = json.loads(checker.redis.get(keyword))
                happen_wti_in_redis.sort()
                if alarm_id_list == happen_wti_in_redis:
                    assert True
                    break
                if i == 9:
                    assert False

        with allure.step("校验alarm wti为空时，且将wti全部关闭时，redis中happen_wti为空"):
            # 关闭所有的wti
            publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': []})
            # 检验
            time.sleep(2)
            happen_wti_in_redis = checker.redis.get(keyword)
            assert len(json.loads(happen_wti_in_redis)) == 0

    @pytest.mark.skip('manual')
    def test_happen_wti_expired(self, checker, vin, vid, publish_msg_by_kafka, redis_key_front, mysql):
        """
        wti查询已开启故障，key为："redis_key_front:happen_wti:vid，有效期时长为5分钟，超过有效期自动删除"
        """
        with allure.step("校验alarm wti开启时，redis中happen_wti的值保存alarm id"):
            # here we want to choose alarm which is wti_enabled
            signal_int = []
            sample_ts = round(time.time() * 1000)
            for i in range(3):
                while True:
                    s = random.choice(wti.SIGNAL)
                    # 带note标记的都是比较特殊的wti，此处随机选一个的时候不选它
                    if 'note' in s or s in signal_int:
                        continue
                    is_wti_enabled = checker.mysql.fetch('const_wti',
                                                         where_model={"wti_code": s['wti_code']},
                                                         fields=['wti_enabled'])[0]['wti_enabled']
                    if is_wti_enabled == 0:
                        continue
                    s['sn'] = str(sample_ts - 1000 * i)
                    signal_int.append(s)
                    break
            # 构造并上报消息
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': signal_int},
                                                       sample_ts=sample_ts)
            # 检验
            alarm_id_list = [
                '{}-{}-{}-WTI'.format(vin, obj['alarm_signal']['signal_int'][i]['sn'], item['wti_code'][4:])
                for i, item in enumerate(signal_int)]
            alarm_id_list.sort()
            time.sleep(302)
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            keyword = remote_vehicle_key_front + ':happen_wti:' + vid
            assert checker.redis.get(keyword) is None

        with allure.step("校验alarm wti为空时，且将wti全部关闭时，redis中happen_wti为空"):
            # 关闭所有的wti
            publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': []})
            # 检验
            time.sleep(2)
            happen_wti_in_redis = checker.redis.get(keyword)
            assert len(json.loads(happen_wti_in_redis)) == 0
