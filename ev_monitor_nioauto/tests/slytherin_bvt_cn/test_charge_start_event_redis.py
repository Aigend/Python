#!/usr/bin/env python
# coding=utf-8

"""
:file:
:author: yry
:Date: Created on 2016/11/11
:Description: 充电开始事件
"""
import time

import pytest
import allure
import json
from utils.assertions import assert_equal


class TestChargeStartMsg(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, mysql):
        original_mileage_in_mysql = mysql['rvs'].fetch('status_vehicle',
                                                       {"id": vid
                                                        },
                                                       ['mileage']
                                                       )[0]['mileage']

        return {'original_mileage': original_mileage_in_mysql}


    @pytest.mark.marcopolo_skip
    def test_charge_start_event(self, vid, publish_msg, checker, prepare, redis_key_front):
        # 马克波罗服务需要跳过@pytest.mark.skip('marcopolo app server')
        # 清除redis 缓存
        remote_vehicle_key_front = redis_key_front['remote_vehicle']
        for key in ['PositionStatus', 'SocStatus', 'ExteriorStatus']:
            checker.redis.delete(f'{remote_vehicle_key_front}:vehicle_status:{vid}:{key}')
        """
        当充电事件push到app后，会往redis的charge_push_xxx_start/charge_push_xxx_end 记录一个sample_ts.
        如果该key有值了，就认为该event_id对应的充电事件已经推送过，不再往APP推送。
        当sample_ts与当前时间比较超过10分钟的话，不再往APP做推送，同时也不更新charge_push_xxx_start/charge_push_xxx_end

        redis往charge_push:{vid}:{event_id}:start key存数据时，会进行一个判断，
        如果mysql的vehicle_soc_history表的end_time字段值=1970***(0)，则认为充电事件未完成，此时会存储新值
        如果>0时，则认为充电事件已然完成，此时不会存储新值。

        此处我们设置 charge_ID(即event_id)值，是因为test_charge_end_redis case 在此case之前，
        已然往ehicle_soc_history落库了end_time>0.故redis不会存储相同的event_id的start的值。
        """
        charge_id = time.strftime("%Y%m%d%M%S", time.localtime())
        # 在充电开始之后等待1分钟，再根据车辆状态数据向车辆主用车人推送充电提醒。如果1分钟时已停止充电，则不再提醒。
        sample_ts = int(round(time.time() * 1000)) - 1 * 60 * 1000
        # 构造并上报 charge_start 事件消息
        soc = 10
        nextev_message, charge_start_obj = publish_msg('charge_start_event', charge_id=charge_id, sample_ts=sample_ts,
                                                       vehicle_status={"mileage": prepare['original_mileage'], 'soc': soc},
                                                       # 当SoC>90%时，不推送开始充电的消息，也不推送此次充电结束的消息
                                                       soc_status={'soc': soc})
        # 校验 charge_start 事件落入Redis库
        keys = ['PositionStatus', 'SocStatus', 'ExteriorStatus']
        checker.check_redis(charge_start_obj, keys, event_name='charge_start_event', clear_none=True)
        # 上报 periodical_charge_update 事件
        time.sleep(2)
        nextev_message, charge_update_obj = publish_msg('periodical_charge_update', charge_id=charge_id,
                                                        sample_points=[{'vehicle_status': {"mileage": prepare['original_mileage'], 'soc': soc+1}, "soc_status": {'soc': soc+1}}])
        # 校验 charge_push 的Redis
        # 车辆处于维修模式，charge_push的redis不会落库。应确保上报的ntester=false，且mysql中的维修工单vehicle_repair_order表的order_status_code为10。
        keys = ['charge_push_start.{event}'.format(event=charge_update_obj['charge_id'])]  # event为充电的event_id
        checker.check_redis(charge_update_obj, keys, event_name='charge_start_event', clear_none=True)
