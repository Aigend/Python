#!/usr/bin/env python
# coding=utf-8

"""
:Description: ecall事件上报校验
"""
import time
import pytest
import random

events = ['charge_start_event', 'charge_end_event', 'journey_start_event', 'journey_end_event']


@pytest.mark.skip('此功能已废弃')
class TestEcall(object):
    @pytest.fixture(scope='class', autouse=True)
    def get_vid(self, vid, mysql, checker, request):
        checker.vid = mysql['rvs'].fetch_one('status_package_version', {'package_part_number<': 'V0001541 BT'})['id']

        def fin():
            checker.vid = vid

        request.addfinalizer(fin)

    @pytest.mark.parametrize("event_name", ['periodical_charge_update', 'periodical_journey_update'])
    def test_ecall_by_update_event_charge(self, event_name, checker, publish_msg_by_kafka):
        """
        urgt_prw_shtdwn 从0切到1会触发ecall的事件包括： 两个update， instant_status_resp。
        注意， alarm_signal_update_event不会触发ecall, 因为 alarm_signal_update_event里面的数据不能保证正确性，因此不消费它了
        保证车机版本在200（V0001541 BT）以下，从status_package_version的package_part_number字段验证
        """

        nextev_message, obj = publish_msg_by_kafka(vid=checker.vid,
                                                   event_name=random.choice(events),
                                                   vehicle_status={"urgt_prw_shtdwn": 0})

        nextev_message, obj = publish_msg_by_kafka(vid=checker.vid, sleep_time=60,
                                                   event_name=event_name,
                                                   sample_points=[{
                                                       "vehicle_status": {"urgt_prw_shtdwn": 1}
                                                   }])
        # 校验
        tables = ['ecall_event']
        checker.check_mysql_tables(obj, tables, event_name=event_name, sample_ts=obj['sample_points'][0]['sample_ts'])

    @pytest.mark.skip('bug exist')
    def test_ecall_by_instant_event(self, checker, publish_msg_by_kafka):
        """
        bug: 门窗读的老的reids+mysql存ecall_data, 而不是有当前instant上报的数据。 先rvs_server落库ecall_event,然后data collection再把数据门窗数据更新，
        开发回应： 先这样吧，目前真实情况下 发生ecall应该不会从 instance上报，而只会由update事件或者alarm事件报

        """
        time.sleep(62)
        event_name = 'instant_status_resp'
        nextev_message, obj = publish_msg_by_kafka(event_name='charge_start_event',
                                                   vehicle_status={"urgt_prw_shtdwn": 0}
                                                   )

        nextev_message, obj = publish_msg_by_kafka(event_name='instant_status_resp',

                                                   sample_point={
                                                       "vehicle_status": {"urgt_prw_shtdwn": 1}
                                                   })

        # 校验
        tables = ['ecall_event']
        checker.check_mysql_tables(obj, tables, event_name=event_name, sample_ts=obj['sample_point']['sample_ts'])

    @pytest.mark.skip('duplicate')
    def test_urgt_prw_shtdwn_switch_no_matter_first_event(self, checker, publish_msg_by_kafka):
        nextev_message, obj = publish_msg_by_kafka(vid='2a5a0434d5724117a4a9a551e766171f',
                                                   event_name='charge_start_event',
                                                   vehicle_status={"urgt_prw_shtdwn": 0}
                                                   )

        nextev_message, obj = publish_msg_by_kafka(vid='2a5a0434d5724117a4a9a551e766171f',
                                                   event_name='periodical_journey_update',
                                                   sample_points=[{
                                                       "vehicle_status": {"urgt_prw_shtdwn": 1}
                                                   }])
        time.sleep(2)
        # 校验
        checker.vid = '2a5a0434d5724117a4a9a551e766171f'
        tables = ['ecall_event']
        checker.check_mysql_tables(obj, tables, event_name='periodical_journey_update',
                                   sample_ts=obj['sample_points'][0]['sample_ts'])
