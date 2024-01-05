""" 
@author:dun.yuan
@time: 2021/6/1 12:56 上午
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import allure
from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestGdReportEvent:
    def test_gd_report_event(self, vid, kafka, publish_msg, mysql):
        with allure.step("上报绿龙gd_report_event"):
            nextev_message, gd_report_obj = publish_msg('gd_report_event', mon_window_sec=60,
                                                        event_items=[{'event_type': 1}, {'event_type': 2},
                                                                     {'event_type': 3}, {'event_type': 0}])

        with allure.step("验证rvs数据库存储结果"):
            for it in gd_report_obj['event_items']:
                history_gd_info_mysql = mysql['rvs'].fetch_one('history_gd_report',
                                                               {'vehicle_id': vid, 'event_type': it['event_type']},
                                                               order_by='id desc')
                assert it['can_id'] == history_gd_info_mysql['can_id']
                assert it['can_bus_id'] == history_gd_info_mysql['can_bus']
                assert it['counter'] == history_gd_info_mysql['counter']

        with allure.step(f"验证topic{kafka['topics']['green_dragon']}收到消息"):
            msg = None
            for data in kafka['comn'].consume(kafka['topics']['green_dragon'], timeout=60):
                msg = parse_nextev_message(data)
                if msg['publish_ts'] == gd_report_obj['sample_ts']:
                    break
            assert_equal(msg, parse_nextev_message(nextev_message))

    def test_gd_report_event_periodical(self, vid, publish_msg, mysql, kafka):
        """
        rvs以上报事件内的字段mon_window_sec是否缺省，来判断是周期上报事件，新事件触发上报不带mon_window_sec，只过滤为counter为1的事件保存
        携带mon_window_sec为周期事件，所有事件都会保存。
        :param vid:
        :param publish_msg:
        :param mysql:
        :param kafka:
        :return:
        """
        with allure.step("模拟新触发上报绿龙gd_report_event"):
            nextev_message, gd_report_obj = publish_msg('gd_report_event',
                                                        event_items=[{'event_type': 1, 'counter': 1},
                                                                     {'event_type': 2, 'counter': 5},
                                                                     {'event_type': 3, 'counter': 3},
                                                                     {'event_type': 0, 'counter': 1}])

        with allure.step("验证rvs数据库存储结果"):
            for it in gd_report_obj['event_items']:
                history_gd_info_mysql = mysql['rvs'].fetch_one('history_gd_report',
                                                               {'vehicle_id': vid, 'event_type': it['event_type'],
                                                                'can_id': it['can_id']},
                                                               order_by='id desc')
                if it['counter'] > 1:
                    assert history_gd_info_mysql is None
                else:
                    assert it['can_id'] == history_gd_info_mysql['can_id']
                    assert it['can_bus_id'] == history_gd_info_mysql['can_bus']
                    assert it['counter'] == history_gd_info_mysql['counter']

        with allure.step(f"验证topic{kafka['topics']['green_dragon']}收到消息"):
            msg = None
            for data in kafka['comn'].consume(kafka['topics']['green_dragon'], timeout=60):
                msg = parse_nextev_message(data)
                if msg['publish_ts'] == gd_report_obj['sample_ts']:
                    break
            assert_equal(msg, parse_nextev_message(nextev_message))

        with allure.step("模拟周期触发上报绿龙gd_report_event"):
            nextev_message, gd_report_obj = publish_msg('gd_report_event', mon_window_sec=60,
                                                        event_items=[{'event_type': 1, 'counter': 2},
                                                                     {'event_type': 2, 'counter': 6},
                                                                     {'event_type': 3, 'counter': 4},
                                                                     {'event_type': 0, 'counter': 2}])

        with allure.step("验证rvs数据库存储结果"):
            for it in gd_report_obj['event_items']:
                history_gd_info_mysql = mysql['rvs'].fetch_one('history_gd_report',
                                                               {'vehicle_id': vid, 'event_type': it['event_type']},
                                                               order_by='id desc')

                assert it['can_id'] == history_gd_info_mysql['can_id']
                assert it['can_bus_id'] == history_gd_info_mysql['can_bus']
                assert it['counter'] == history_gd_info_mysql['counter']

        with allure.step(f"验证topic{kafka['topics']['green_dragon']}收到消息"):
            msg = None
            for data in kafka['comn'].consume(kafka['topics']['green_dragon'], timeout=20):
                print(data)
                msg = parse_nextev_message(data)
                if msg['publish_ts'] == gd_report_obj['sample_ts']:
                    break
            assert_equal(msg, parse_nextev_message(nextev_message))
