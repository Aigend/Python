#!/usr/bin/env python
# coding=utf-8
import json
import random
import time
import allure
import pytest

from nio_messages import wti
from utils.assertions import assert_equal
from utils.time_parse import timestamp_to_utc_strtime, now_time_sec


class TestAlarmSignalUpdateWhenPeriodicalEvent(object):
    """
    不管sn变不变化，history_wti_alarm、status_wti_alarm表都只在wti开始和结束时更新，
    同一个WTI的持续上报中，sn在现实中应该是不变的，为故障开始发生的时间点。
    """
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, checker):
        sql_result = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])
        return {'original_mileage': sql_result[0]['mileage'] if sql_result else 0}

    @pytest.fixture(scope='function', autouse=False)
    def tag(self):
        return 'vehicle_for_repair'

    @pytest.mark.parametrize("event_name", ['periodical_charge_update', 'periodical_journey_update'])
    def test_alarm_signal_update(self, event_name, vid, vin, checker, publish_msg_by_kafka, prepare, kafka):
        publish_msg_by_kafka(event_name, sample_points=[{'alarm_signal': {'signal_int': []},
                                                         "vehicle_status": {"mileage": prepare['original_mileage'] + 1}
                                                         }])
        # here we want to choose alarm which is wti_enabled
        signal_int = []
        kafka['comn'].set_offset_to_end(kafka['topics']['wti_data'])
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
        nextev_message, obj = publish_msg_by_kafka(event_name=event_name,
                                                   sample_points=[{'alarm_signal': {'signal_int': signal_int}}])

        # 校验
        tables = ['status_wti_alarm', 'history_wti_alarm']
        checker.check_mysql_tables(obj, tables, event_name=event_name, sample_ts=obj['sample_points'][0]['sample_ts'],
                                   extra=signal_int)

        # 校验向wti_data推送的告警信息中不包含胎压信息
        kafka_msg = None
        is_found = False
        for data in kafka['comn'].consume(kafka['topics']['wti_data'], timeout=10):
            kafka_msg = json.loads(str(data, encoding='utf-8'))
            if vid == kafka_msg['vehicle_id'] and obj['sample_points'][0]['sample_ts'] == kafka_msg['sample_time']:
                is_found = True
                break
        with allure.step('校验 {}'.format(kafka['topics']['wti_data'])):
            assert_equal(is_found, True)
            assert 'tyre_status' not in kafka_msg['wti_entity']

    @pytest.mark.parametrize("event_name", ['periodical_charge_update', 'periodical_journey_update'])
    def test_history_wti_alarm_endtime_will_update(self, vid, vin, checker, publish_msg_by_kafka, event_name, cmdopt):
        with allure.step("校验 上报两次alarm_signal时，history_wti_alarm中会更新第一次报，且不再在第二次继续上报的wti对应条目的end_time"):
            # 例如第一次的为（wti_1,wti_2）,第二次的为（wti_1,wti_3）
            # 则history_wti_alarm表中wti_2对应的条目的end_time会更新,但是wti_1不会更新，因为第二次继续报了wti_1
            # 实际车机端上报时，故障开始上报了一个时间戳后，后面周期上报时该故障如果还有，一直报的还是最早的那个时间戳，一个车在发生某个故障从开始到结束这个时间段，sn都是一样的

            # 清空
            publish_msg_by_kafka(event_name, sample_points=[{'alarm_signal': {'signal_int': []}}], sleep_time=10)
            # 准备数据
            first_sn = str(round(time.time() * 1000))
            first_alarm_signal = [
                {'sn': first_sn, 'name': 'ABSFailLampReq', 'value': 1, 'alarm_level': 1, 'wti_code': 'WTI-BC-1',
                 "alarm_id": f"{vid if 'marcopolo' in cmdopt else vin}-{first_sn}-BC-1-WTI"}
            ]

            time.sleep(2)
            second_sn = str(round(time.time() * 1000))
            second_alarm_signal = [
                {'sn': first_sn, 'name': 'EBDFailLampReq', 'value': 1, 'alarm_level': 1, 'wti_code': 'WTI-BC-4',
                 "alarm_id": f"{vid if 'marcopolo' in cmdopt else vin}-{second_sn}-BC-4-WTI"}
            ]

            # 第一次上报，检查history_wti_alarm中wti的start_time为上报的sn值，end_time为null
            nextev_message, obj = publish_msg_by_kafka(event_name=event_name,
                                                       sample_points=[
                                                           {'alarm_signal': {'signal_int': first_alarm_signal}}])

            old_wti_in_mysql = checker.mysql.fetch('history_wti_alarm',
                                                   {"vehicle_id": vid,
                                                    'alarm_id': first_alarm_signal[0]['alarm_id']},
                                                   fields=['start_time', 'end_time'])[0]

            start_time = timestamp_to_utc_strtime(first_alarm_signal[0]['sn'], adjust=True)

            assert_equal(start_time, old_wti_in_mysql['start_time'])
            assert_equal(None, old_wti_in_mysql['end_time'])

            # 第二次上报，检查history_wti_alarm中wti的start_time保持不变为第一次上报的sn值，end_time值依据第二次上报的sample_ts进行更新
            nextev_message, obj = publish_msg_by_kafka(event_name=event_name,
                                                       sample_points=[{'alarm_signal': {'signal_int': second_alarm_signal}}])
            new_wti_in_mysql = checker.mysql.fetch('history_wti_alarm',
                                                   {"vehicle_id": vid,
                                                    'alarm_id': first_alarm_signal[0]['alarm_id']},
                                                   suffix=" and end_time is not NULL",
                                                   fields=['start_time', 'end_time'])[0]

            end_time = timestamp_to_utc_strtime(obj['sample_points'][0]['sample_ts'], adjust=True)
            assert_equal(start_time, new_wti_in_mysql['start_time'])
            assert_equal(end_time, new_wti_in_mysql['end_time'])

    @pytest.mark.parametrize("event_name", ['periodical_charge_update', 'periodical_journey_update'])
    def test_alarm_level_will_update(self, vin, vid, publish_msg_by_kafka, checker, event_name, cmdopt):
        """
        校验 上报两次alarm_signal时，status_wti_alarm 中会更新第一次报，且不再在第二次继续上报的wti对应条目的alarm_level为0
        例如第一次的为（wti_1,wti_2）,第二次的为（wti_1,wti_3）
        则status_wti_alarm表中wti_2对应的条目的alarm_level会更新为0,表示该条alarm结束了。

        并且wti_2除alarm_level与update_time之外的记录仍为第一次的数值，不会更新为第二次的数值。
        wti_1的所有数据则始终是第一次上报的值
        实际车机端上报时，故障开始上报了一个时间戳后，后面周期上报时该故障如果还有，一直报的还是最早的那个时间戳，一个车在发生某个故障从开始到结束这个时间段，sn都是一样的
        """
        with allure.step("校验上报两次alarm_signal时，status_wti_alarm 中会更新第一次报，且不再在第二次继续上报的wti对应条目的alarm_level为0"):
            # 清空
            publish_msg_by_kafka(event_name, sample_points=[{'alarm_signal': {'signal_int': []}}], sleep_time=10)
            # 准备数据
            first_sn = str(round(time.time() * 1000))
            first_alarm_signal = [
                {'sn': first_sn, 'name': 'VCUHVILError', 'value': 1, 'alarm_level': 1, 'wti_code': 'WTI-EP-15',
                 "alarm_id": f"{vid if 'marcopolo' in cmdopt else vin}-{first_sn}-EP-15-WTI"}
            ]

            second_sn = str(round(time.time() * 1000))
            second_alarm_signal = [
                {'sn': first_sn, 'name': 'VCUImdStopDriving', 'value': 1, 'alarm_level': 1, 'wti_code': 'WTI-EP-16',
                 "alarm_id": f"{vid if 'marcopolo' in cmdopt else vin}-{first_sn}-EP-16-WTI"}
            ]

            # 第一次上报，检查status_wti_alarm中wti的alarm_level为上报的level值
            nextev_message, obj = publish_msg_by_kafka(event_name=event_name,
                                                       sample_points=[{'alarm_signal': {'signal_int': first_alarm_signal}}])

            status_wti_alarm_mysql_first = \
                checker.mysql.fetch('status_wti_alarm',
                                    {"id": vid, 'wti_code': first_alarm_signal[0]['wti_code'],
                                     'sample_time': timestamp_to_utc_strtime(obj['sample_points'][0]['sample_ts'])})[0]
            assert_equal(status_wti_alarm_mysql_first['alarm_level'], first_alarm_signal[0]['alarm_level'])

            # 第二次上报，检查status_wti_alarm中第一次那条的wti的alarm_level值为0，表示该alarm已经终止
            nextev_message, obj = publish_msg_by_kafka(event_name=event_name, sample_points=[
                {'alarm_signal': {'signal_int': second_alarm_signal}}])
            status_wti_alarm_mysql_second = \
                checker.mysql.fetch('status_wti_alarm',
                                    {"id": vid, 'wti_code': first_alarm_signal[0]['wti_code'],
                                     'sample_time': timestamp_to_utc_strtime(obj['sample_points'][0]['sample_ts'])})[0]
            assert_equal(status_wti_alarm_mysql_second['alarm_level'], 0)

    @pytest.mark.skip('EVM alarm TODO')
    def test_reported_national_tag(self, publish_msg_by_kafka, checker, vid, vin):
        """
        校验 上报update 事件时，alarm_signal如果在evm范围内，
        并且vehicle_platform_activated表中alarm_enable=1时，
        并且const_wti表中wti_enabled=1时，
        国家平台接受该alarm后，evm server会把数据推送到alarm_signals_reported kafka topic里，
        并且rvs server 会把history_wti_alarm里的reported_national_tag置为1。

        注意：目前有个bug，当周期性只报一次的时候，可能国家平台返回ack的时候，我们这边故障还没有落库，导致mysql的'更新'操作失败。
        如果周期性事件连续上报该alarm两次以上，则能看到reported_national_tag=1
        """

        event_name = 'periodical_journey_update'

        # 准备alarm wti-17属于EVM范围内的报警
        sn = str(round(time.time() * 1000))
        signal_int = [
            {
                'sn': sn,
                "name": "BMS_VCU_AE:BMSPackOverTemp",
                "value": 1,
                "wti_code": "WTI-17",
                "alarm_id": vin + '-' + sn + '-17',
                "alarm_level": 1
            }

        ]

        # 确保alarm_enable==1，才会推送给evm
        is_send_to_evm_enable = checker.mysql.fetch('vehicle_platform_activated', {'vehicle_id': vid},
                                                    fields=['alarm_enable'])[0]['alarm_enable']
        assert is_send_to_evm_enable == 1

        # 确保 wti_enable=1
        is_wti_enabled = checker.mysql.fetch('const_wti',
                                             where_model={"wti_code": signal_int[0]['wti_code']},
                                             fields=['wti_enabled'])[0]['wti_enabled']
        assert is_wti_enabled == 1

        # 先上报一个非WTI-17的报警，从而清空WTI-17报警。
        other_alarm = [{
            "name": "BMS_VCU_272:BMSSOCOverUnder",
            "value": 2,
            "alarm_level": 1,
            "wti_code": "WTI-462"
        }]
        nextev_message, obj = publish_msg_by_kafka(event_name=event_name,
                                                   sample_points=[{'alarm_signal': {'signal_int': other_alarm}}],
                                                   sleep_time=2)

        # 报2次，因为有个bug见函数头注释
        nextev_message, obj = publish_msg_by_kafka(event_name=event_name,
                                                   sample_points=[{'alarm_signal': {'signal_int': signal_int}}],
                                                   sleep_time=2)
        nextev_message, obj = publish_msg_by_kafka(event_name=event_name,
                                                   sample_points=[{'alarm_signal': {'signal_int': signal_int}}],
                                                   sleep_time=2)

        # 校验mysql
        with allure.step('校验mysql history_wti_alarm 中reported_national_tag ==1，表示已经上报国家平台'):
            reported_national_tag_in_mysql = checker.mysql.fetch('history_wti_alarm',
                                                                 {"vehicle_id": vid,
                                                                  'alarm_id': signal_int[0]['alarm_id']},
                                                                 fields=['reported_national_tag'])[0][
                'reported_national_tag']

            assert_equal(reported_national_tag_in_mysql, 1)

    @pytest.mark.marcopolo_skip
    @pytest.mark.test
    @pytest.mark.parametrize("event_name", ['periodical_charge_update', 'periodical_journey_update'])
    def test_alarm_periodical_update_history_tag_all_1(self, event_name, env, tag, tsp_agent_once, publish_msg, checker, kafka):
        # 马克波罗服务需要跳过@pytest.mark.skip('marcopolo do server')
        vid = env['vehicles']['vehicle_for_repair']['vehicle_id']
        vin = env['vehicles']['vehicle_for_repair']['vin']
        # 清空 WTI 告警
        publish_msg(event_name, tsp_agent=tsp_agent_once, vin=vin, vid=vid, sample_points=[{'alarm_signal': {'signal_int': []}}], sleep_time=2)
        # here we want to choose alarm which is wti_enabled
        signal_int = []
        while True:
            s = random.choice(wti.SIGNAL)
            # 带note标记的都是比较特殊的wti，此处随机选一个的时候不选它
            if 'note' in s:
                continue
            is_wti_enabled = checker.mysql.fetch('const_wti', where_model={"wti_code": s['wti_code']},
                                                 fields=['wti_enabled'])[0]['wti_enabled']
            if is_wti_enabled == 0:
                continue

            signal_int.append(s)
            break

        with allure.step('上报维修工单开始信息'):
            ts = int(time.time())
            vehicle_repair_order = json.dumps({
                "owner_phone": "13761473462", "order_status_name": "维修开始", "som_order_no": "BSHHB00020180720001113",
                "account_id": "1112538414", "receipt_type": "", "booking_order_no": "BSHHB00020180720001113",
                "order_status_code": '5', "update_at": ts, "ro_no": "BSHHB00020180720001113", "update_by": "用户代表",
                "vehicle_id": vid,
                "order_type": "101210034", "timestamp": ts, "status": 5,
                "repair_order_no": "BSHHB00020180720001113"
            })
            kafka['do'].produce(kafka['topics']['repair'], vehicle_repair_order)
            time.sleep(2)
        with allure.step('设置为换电中，换电事件由rvs处理'):
            power_swap_id = now_time_sec()
            publish_msg('specific_event', tsp_agent=tsp_agent_once, vin=vin, vid=vid, event_type='power_swap_start',
                        data={'power_swap_id': power_swap_id}, sleep_time=2)
        with allure.step('周期性事件上报alarm，且设置为诊断状态，fota升级中'):
            nextev_message, obj = publish_msg(event_name, tsp_agent=tsp_agent_once, vid=vid, vin=vin, sleep_time=2,
                                              sample_points=[{'vehicle_status': {'ntester': True, 'vehl_state': 4},
                                                             'alarm_signal': {'signal_int': signal_int}}])
        with allure.step('校验四个tag均为1'):
            sn = obj['sample_points'][0]['alarm_signal']['signal_int'][0]['sn']
            alarm_id = '{}-{}-{}-WTI'.format(vin, sn, signal_int[0]['wti_code'][4:])
            actual_tags = checker.mysql.fetch('history_wti_alarm', {"vehicle_id": vid, 'alarm_id': alarm_id, 'fota_tag': 1},
                                              ["fota_tag", 'diag_tag', 'soc_tag', 'repair_tag'])[0]
            expect_tags = {'fota_tag': 1, 'diag_tag': 1, 'soc_tag': 1, 'repair_tag': 1}
            assert_equal(actual_tags, expect_tags)
        with allure.step('case测试完毕，结束换电，结束维修状态'):
            publish_msg('specific_event', tsp_agent=tsp_agent_once, vin=vin, vid=vid, event_type='power_swap_end',
                        data={'power_swap_id': power_swap_id}, sleep_time=2)
            ts = int(time.time())
            vehicle_repair_order = json.dumps({
                "owner_phone": "13761473462", "order_status_name": "维修结束", "som_order_no": "BSHHB00020180720001113",
                "account_id": "1112538414", "receipt_type": "", "booking_order_no": "BSHHB00020180720001113",
                "order_status_code": '10', "update_at": ts, "ro_no": "BSHHB00020180720001113", "update_by": "用户代表",
                "vehicle_id": vid,
                "order_type": "101210034", "timestamp": ts, "status": 10,
                "repair_order_no": "BSHHB00020180720001113"
            })
            kafka['do'].produce(kafka['topics']['repair'], vehicle_repair_order)

    @pytest.mark.marcopolo_skip
    @pytest.mark.test
    @pytest.mark.parametrize("event_name", ['periodical_charge_update', 'periodical_journey_update'])
    def test_alarm_periodical_update_history_tag_all_0(self, event_name, env, publish_msg_by_kafka, checker, kafka):
        # 马克波罗服务需要跳过@pytest.mark.skip('marcopolo do server')
        vid = env['vehicles']['vehicle_for_repair']['vehicle_id']
        vin = env['vehicles']['vehicle_for_repair']['vin']
        # 清空 WTI 告警
        publish_msg_by_kafka(event_name, vin=vin, vid=vid, sample_points=[{'alarm_signal': {'signal_int': []}}], sleep_time=2)
        # here we want to choose alarm which is wti_enabled
        signal_int = []
        while True:
            s = random.choice(wti.SIGNAL)
            # 带note标记的都是比较特殊的wti，此处随机选一个的时候不选它
            if 'note' in s:
                continue
            is_wti_enabled = checker.mysql.fetch('const_wti', where_model={"wti_code": s['wti_code']},
                                                 fields=['wti_enabled'])[0]['wti_enabled']
            if is_wti_enabled == 0:
                continue

            signal_int.append(s)
            break

        with allure.step('上报结束维修状态信息'):
            ts = int(time.time())
            vehicle_repair_order = json.dumps({
                "owner_phone": "13761473462", "order_status_name": "维修结束", "som_order_no": "BSHHB00020180720001113",
                "account_id": "1112538414", "receipt_type": "", "booking_order_no": "BSHHB00020180720001113",
                "order_status_code": '10', "update_at": ts, "ro_no": "BSHHB00020180720001113", "update_by": "用户代表",
                "vehicle_id": vid,
                "order_type": "101210034", "timestamp": ts, "status": 10,
                "repair_order_no": "BSHHB00020180720001113"
            })
            kafka['do'].produce(kafka['topics']['repair'], vehicle_repair_order)
        with allure.step('设置为充电中'):
            charge_id = now_time_sec()
            publish_msg_by_kafka('charge_start_event', vin=vin, vid=vid, charge_id=charge_id, sleep_time=2)
        with allure.step('周期性事件上报alarm，且设置为非诊断状态，驾驶中'):
            nextev_message, obj = publish_msg_by_kafka(event_name, vid=vid, vin=vin, sleep_time=2,
                                                       sample_points=[{'vehicle_status': {'ntester': False, 'vehl_state': 1},
                                                                       'alarm_signal': {'signal_int': signal_int}}])
        with allure.step('校验四个tag均为0'):
            sn = obj['sample_points'][0]['alarm_signal']['signal_int'][0]['sn']
            alarm_id = '{}-{}-{}-WTI'.format(vin, sn, signal_int[0]['wti_code'][4:])
            actual_tags = checker.mysql.fetch('history_wti_alarm', {"vehicle_id": vid, 'alarm_id': alarm_id, 'fota_tag': 0},
                                              ["fota_tag", 'diag_tag', 'soc_tag', 'repair_tag'])[0]
            expect_tags = {'fota_tag': 0, 'diag_tag': 0, 'soc_tag': 0, 'repair_tag': 0}
            assert_equal(actual_tags, expect_tags)
        with allure.step('case测试完毕，结束充电'):
            publish_msg_by_kafka('charge_end_event', vin=vin, vid=vid, charge_id=charge_id, sleep_time=2)

    @pytest.mark.test
    @pytest.mark.parametrize("event_name", ['periodical_charge_update', 'periodical_journey_update'])
    def test_alarm_periodical_update_history_tag_soc_1(self, event_name, env, tag, tsp_agent_once, publish_msg, checker, kafka, cmdopt):
        vid = env['vehicles']['vehicle_for_repair']['vehicle_id']
        vin = env['vehicles']['vehicle_for_repair']['vin']
        # 清空 WTI 告警
        publish_msg(event_name, tsp_agent=tsp_agent_once, vin=vin, vid=vid, sample_points=[{'alarm_signal': {'signal_int': []}}], sleep_time=2)
        # here we want to choose alarm which is wti_enabled
        signal_int = []
        while True:
            s = random.choice(wti.SIGNAL)
            # 带note标记的都是比较特殊的wti，此处随机选一个的时候不选它
            if 'note' in s:
                continue
            is_wti_enabled = checker.mysql.fetch('const_wti', where_model={"wti_code": s['wti_code']},
                                                 fields=['wti_enabled'])[0]['wti_enabled']
            if is_wti_enabled == 0:
                continue

            signal_int.append(s)
            break
        with allure.step('换电事件由rvs处理，校验 end_time为默认值为:1970-01-01 00:00:00.001时,可以正常记录soc_tag=1'):
            # 设置为换电中
            power_swap_id = now_time_sec()
            publish_msg('specific_event', tsp_agent=tsp_agent_once, vin=vin, vid=vid, event_type='power_swap_start',
                        data={'power_swap_id': power_swap_id}, sleep_time=2)
            nextev_message, obj = publish_msg(event_name, tsp_agent=tsp_agent_once, vid=vid, vin=vin, sleep_time=2,
                                              sample_points=[{'vehicle_status': {'ntester': False, 'vehl_state': 1},
                                                             'alarm_signal': {'signal_int': signal_int}}])
            with allure.step('校验soc_tag为1'):
                sn = obj['sample_points'][0]['alarm_signal']['signal_int'][0]['sn']
                alarm_id = '{}-{}-{}-WTI'.format(vid if 'marcopolo' in cmdopt else vin, sn, signal_int[0]['wti_code'][4:])
                actual_tags = checker.mysql.fetch('history_wti_alarm', {"vehicle_id": vid, 'alarm_id': alarm_id, 'fota_tag': 0},
                                                  ["fota_tag", 'diag_tag', 'soc_tag', 'repair_tag'])[0]
                expect_tags = {'fota_tag': 0, 'diag_tag': 0, 'soc_tag': 1, 'repair_tag': 0}
                assert_equal(actual_tags, expect_tags)
            # 结束换电事件
            publish_msg('specific_event', tsp_agent=tsp_agent_once, vin=vin, vid=vid, event_type='power_swap_end',
                        data={'power_swap_id': power_swap_id}, sleep_time=2)

    @pytest.mark.parametrize("event_name", ['periodical_charge_update', 'periodical_journey_update'])
    def test_wti_not_save(self, event_name, vid, vin, checker, publish_msg_by_kafka, mysql, cmdopt):
        with allure.step('周期性事件，若evm_flag=false 并且充电中, 不处理wti'):
            publish_msg_by_kafka(event_name, sample_points=[{'alarm_signal': {'signal_int': []}}], sleep_time=2)
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

            nextev_message, obj = publish_msg_by_kafka(event_name=event_name,
                                                       sample_points=[{'alarm_signal': {'signal_int': signal_int},
                                                                       'soc_status': {'chrg_state': 1},
                                                                       'evm_flag': False}],
                                                       sleep_time=2)
            # 校验 history_wti_alarm 表
            sn = obj['sample_points'][0]['alarm_signal']['signal_int'][0]['sn']
            alarm_id = '{}-{}-{}-WTI'.format(vid if 'marcopolo' in cmdopt else vin, sn, signal_int[0]['wti_code'][4:])
            history_wti_mysql = checker.mysql.fetch('history_wti_alarm',
                                                    {"vehicle_id": vid,
                                                     'alarm_id': alarm_id}, retry_num=5)
            # 此处报错排查一下
            assert_equal(len(history_wti_mysql), 0)
            # 校验 status_wti_alarm 表
            sample_time = timestamp_to_utc_strtime(obj['sample_points'][0]['sample_ts'])
            status_wti_mysql = checker.mysql.fetch('status_wti_alarm',
                                                   {"id": vid, 'sample_time': sample_time}, retry_num=5)
            assert_equal(len(status_wti_mysql), 0)

    @pytest.mark.parametrize("event_name", ['periodical_charge_update', 'periodical_journey_update'])
    def test_same_wti_wont_change(self, vin, vid, event_name, publish_msg_by_kafka, checker, cmdopt):
        """
        验证上报周期性事件故障信息，两次上报信息一致，但sn不同，之前上报的故障信息没有变化
        """
        # 清空WTI
        publish_msg_by_kafka(event_name, sample_points=[{'alarm_signal': {'signal_int': []}}], sleep_time=2)
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
        nextev_message_1st, obj_1st = publish_msg_by_kafka(event_name=event_name,
                                                           sample_points=[{'alarm_signal': {'signal_int': signal_int}}],
                                                           sleep_time=2)

        sn_1st = obj_1st['sample_points'][0]['alarm_signal']['signal_int'][0]['sn']
        alarm_id_1st = '{}-{}-{}-WTI'.format(vid if 'marcopolo' in cmdopt else vin, sn_1st, signal_int[0]['wti_code'][4:])
        original_update_time = checker.mysql.fetch('history_wti_alarm', {"vehicle_id": vid, 'alarm_id': alarm_id_1st})[0]['update_time']

        nextev_message_2nd, obj_2nd = publish_msg_by_kafka(event_name=event_name,
                                                           sample_points=[{'alarm_signal': {'signal_int': signal_int}}],
                                                           sleep_time=2)
        with allure.step('校验第二次上报的sn的wti没有落库'):
            sn_2nd = obj_2nd['sample_points'][0]['alarm_signal']['signal_int'][0]['sn']
            alarm_id_2nd = '{}-{}-{}-WTI'.format(vin, sn_2nd, signal_int[0]['wti_code'][4:])
            wti_2nd = checker.mysql.fetch('history_wti_alarm', {"vehicle_id": vid, 'alarm_id': alarm_id_2nd}, retry_num=5)
            assert_equal(bool(wti_2nd), False)
        with allure.step('校验第一次上报的wti没有变动'):
            new_update_time = checker.mysql.fetch('history_wti_alarm', {"vehicle_id": vid, 'alarm_id': alarm_id_1st})[0]['update_time']
            assert_equal(original_update_time, new_update_time)

    @pytest.mark.parametrize("event_name", ['periodical_charge_update', 'periodical_journey_update'])
    def test_supplement_vehicle_status(self, vin, vid, publish_msg_by_kafka, event_name, checker, redis_key_front, cmdopt):
        """
        验证 alarm、journey、charge update event事件时，
        若未上报车辆状态数据，应查询rds最后一次车辆上报的状态进行补充(history_wti_alarm表)
        """
        # 清空WTI
        publish_msg_by_kafka(event_name, sample_points=[{'alarm_signal': {'signal_int': []}}], sleep_time=2)
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
        nextev_message, obj = publish_msg_by_kafka(event_name=event_name,
                                                   sample_points=[{'alarm_signal': {'signal_int': signal_int}}],
                                                   clear_fields=["sample_points[0].soc_status"],
                                                   sleep_time=2)

        with allure.step('校验会用redis中的SocStatus数据补全history_wti_alarm'):
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            key = f'{remote_vehicle_key_front}:vehicle_status:{vid}:SocStatus'
            status_soc_in_redis = json.loads(checker.redis.get(key))
            sn = obj['sample_points'][0]['alarm_signal']['signal_int'][0]['sn']
            alarm_id = '{}-{}-{}-WTI'.format(vid if 'marcopolo' in cmdopt else vin, sn, signal_int[0]['wti_code'][4:])
            charger_type = checker.mysql.fetch('history_wti_alarm', {"vehicle_id": vid, 'alarm_id': alarm_id})[0]['soc']
            assert_equal(charger_type, status_soc_in_redis['soc'])

    @pytest.mark.parametrize("event_name", ['periodical_charge_update', 'periodical_journey_update'])
    def test_false_alarm(self, vin, vid, publish_msg_by_kafka, event_name, checker, cmdopt):
        """
        验证 journey/charge/alarm update上报故障时，若消息中故障为假故障，history wti alarm表中未结束的故障更新为结束
        """
        # 清空WTI
        publish_msg_by_kafka(event_name, sample_points=[{'alarm_signal': {'signal_int': []}}], sleep_time=2)
        # 随机选一个上报正确的WTI故障上报
        signal_int_true = []
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

            signal_int_true.append(s)
            break
        signal_int_true = [{'name': 'ABSFailLampReq', 'value': 1, 'alarm_level': 1, 'wti_code': 'WTI-BC-1'}]
        nextev_message_1st, obj_1st = publish_msg_by_kafka(event_name=event_name,
                                                           sample_points=[{'alarm_signal': {'signal_int': signal_int_true}}],
                                                           sleep_time=2)
        # 上报不存在的WTI故障
        signal_int_false = [{'name': 'XXXXXXXX', 'value': 1, 'alarm_level': 1}]
        nextev_message_2nd, obj_2nd = publish_msg_by_kafka(event_name=event_name,
                                                           sample_points=[{'alarm_signal': {'signal_int': signal_int_false}}],
                                                           clear_fields=["sample_points[0].alarm_signal.signal_int"],
                                                           sleep_time=2)

        with allure.step('校验history wti alarm表中未结束的故障更新为结束'):
            sn_1st = obj_1st['sample_points'][0]['alarm_signal']['signal_int'][0]['sn']
            alarm_id_1st = '{}-{}-{}-WTI'.format(vid if 'marcopolo' in cmdopt else vin, sn_1st, signal_int_true[0]['wti_code'][4:])
            end_time = checker.mysql.fetch('history_wti_alarm', {"vehicle_id": vid, 'alarm_id': alarm_id_1st},
                                           suffix="and end_time is not NULL")[0]['end_time']
            assert_equal(end_time is not None, True)
