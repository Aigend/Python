#!/usr/bin/env python
# coding=utf-8

import time
import allure
import pytest
import json
import random
from utils.assertions import assert_equal
from nio_messages import wti


class TestChargePushKafka(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, mysql):
        original_mileage_in_mysql = mysql['rvs'].fetch('status_vehicle',
                                                       {"id": vid
                                                        },
                                                       ['mileage']
                                                       )[0]['mileage']

        return {'original_mileage': original_mileage_in_mysql}

    @pytest.mark.marcopolo_skip
    def test_charge_push_kafka(self, vid, publish_msg, kafka, prepare, mysql):
        # 马可波罗服务需跳过@pytest.mark.skip('marcopolo charging topic')
        """
        推送充电事件到Kafka: swc-cvs-tsp-${env}-80001-charging
        http://showdoc.nevint.com/index.php?s=/11&page_id=23851

        下游：PE（Power Express）消费

        充电数据推送Kafka的时机与充电提醒用户app相同
            1、当SoC>90%时，不推送开始充电的消息，也不推送此次充电结束的消息
            2、如果充电开始数据是补发数据，且补发时间距离当前超过10分钟，则对应开始充电的提醒不再发送
            3、如果充电结束数据是补发数据，且补发时间距离当前超过10分钟，则对应结束充电的提醒不再发送
            4、如果充电开始数据滞后于对应的充电结束数据，那么该充电开始的提醒不再发送
            5、在充电开始之后等待1分钟，再根据车辆状态数据向车辆主用车人推送充电提醒
            6、如果两分钟时已停止充电，则不再提醒
        """
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['charging'])
        kafka['comn'].set_offset_to_end(kafka['topics']['wti_can_signal'])
        time.sleep(5)
        charge_id = time.strftime("%Y%m%d%M%S", time.localtime())
        # 在充电开始之后等待1分钟，再根据车辆状态数据向车辆主用车人推送充电提醒。如果1分钟时已停止充电，则不再提醒。
        sample_ts = int(round(time.time() * 1000)) - 1 * 60 * 1000
        # 构造并上报 charge_start 事件消息
        nextev_message, charge_start_obj = publish_msg('charge_start_event', charge_id=charge_id, sample_ts=sample_ts,
                                                       vehicle_status={"mileage": prepare['original_mileage'] + 1},
                                                       soc_status={"soc": 10}, sleep_time=5)

        # 上报 periodical_charge_update 事件
        nextev_message, charge_update_obj = publish_msg('periodical_charge_update', charge_id=charge_id,
                                                        sample_points=[{'vehicle_status': {
                                                            "mileage": prepare['original_mileage'] + 2},
                                                            'soc_status': {"soc": 10}}])
        msg = None
        is_found = False
        for data in kafka['comn'].consume(kafka['topics']['charging'], timeout=60):
            msg = eval(str(data, encoding="utf-8"))
            if msg['event_data']['sample_time'] == int(charge_start_obj['sample_ts'] // 1000) and vid == msg['vehicle_id']:
                is_found = True
                break

        with allure.step('校验 {}'.format(kafka['topics']['charging'])):
            assert_equal(is_found, True)

        with allure.step('上报alarm_signal_update_event，携带告警信号'):
            _, obj = publish_msg('alarm_signal_update_event', alarm_signal={'signal_int': [random.choice(wti.SIGNAL)]})

        with allure.step('校验 {}'.format(kafka['topics']['wti_can_signal'])):
            kafka_msg = None
            is_found = False
            for data in kafka['comn'].consume(kafka['topics']['wti_can_signal'], timeout=30):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                if vid == kafka_msg['vehicle_id'] and kafka_msg['sample_time'] == int(obj['sample_ts']):
                    is_found = True
                    break
            print(kafka_msg)
            assert_equal(is_found, True)
            assert kafka_msg['vehicle_status']['bid'] == mysql['rvs'].fetch_one('status_btry_packs', where_model={'id': vid})['bid']

    @pytest.mark.skip('与上条case合并')
    def test_charge_push_kafka_with_bid(self, vid, publish_msg, kafka, prepare, mysql):
        # 选取电池编码
        pack = mysql['battery_trace'].fetch_one('sys_battery_pack_entity', where_model={'status': -3},
                                                order_by='create_time desc')
        kafka['comn'].set_offset_to_end(kafka['topics']['wti_can_signal'])
        with allure.step('上报charge_start_event，指定nio_encoding'):
            nextev_message, charge_start_obj = publish_msg('charge_start_event',
                                                           vehicle_status={"mileage": prepare['original_mileage'] + 1},
                                                           battery_package_info={"btry_pak_encoding": [
                                                               {
                                                                   "nio_encoding": pack['nio_encoding'],
                                                               }
                                                           ]})

        with allure.step('上报charge_start_event，携带告警信号'):
            publish_msg('alarm_signal_update_event', alarm_signal={'signal_int': [random.choice(wti.SIGNAL)]}, )

        with allure.step('校验 {}'.format(kafka['topics']['wti_can_signal'])):
            kafka_msg = None
            is_found = False
            for data in kafka['comn'].consume(kafka['topics']['wti_can_signal'], timeout=10):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                if vid == kafka_msg['vehicle_id']:
                    is_found = True
                    break
            assert_equal(is_found, True)
            print(kafka_msg)
            assert kafka_msg['vehicle_status']['bid'] == pack['bid']

        with allure.step('上报charge_start_event，还原nio_encoding'):
            nextev_message, charge_start_obj = publish_msg('charge_start_event',
                                                           vehicle_status={"mileage": prepare['original_mileage']})
