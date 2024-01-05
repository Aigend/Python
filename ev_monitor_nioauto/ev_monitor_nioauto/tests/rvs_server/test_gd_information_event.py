""" 
@author:dun.yuan
@time: 2021/5/30 5:52 下午
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import allure
from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestGdSystemInfo:
    def test_gd_system_info(self, vid, publish_msg, mysql, kafka):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['green_dragon'])

        with allure.step("上报绿龙gd_information_event"):
            nextev_message, gd_information_obj = publish_msg('gd_information_event',
                                                             mon_window_sec=60,
                                                             sys_info_items=[{'key': 'mem_usage'},
                                                                             {'key': 'disk_usage'},
                                                                             {'key': 'emmc_life'},
                                                                             {'key': 'cpu_usage'}])

        with allure.step("验证rvs数据库存储结果"):
            status_gd_in_mysql = mysql['rvs'].fetch_one('status_gd', {'id': vid})
            history_gd_info_mysql = mysql['rvs'].fetch_one('history_gd_info', {'vehicle_id': vid}, order_by='id desc')

            for it in gd_information_obj['sys_info_items']:
                assert int(it['value']) == int(status_gd_in_mysql[it['key']])
                assert int(it['value']) == int(history_gd_info_mysql[it['key']])

        with allure.step(f"验证topic{kafka['topics']['green_dragon']}收到消息"):
            msg = None
            for data in kafka['comn'].consume(kafka['topics']['green_dragon'], timeout=60):
                msg = parse_nextev_message(data)
                if msg['publish_ts'] == gd_information_obj['sample_ts']:
                    break
            assert_equal(msg, parse_nextev_message(nextev_message))
