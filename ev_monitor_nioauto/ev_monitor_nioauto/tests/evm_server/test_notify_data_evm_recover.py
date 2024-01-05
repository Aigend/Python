""" 
@author:dun.yuan
@time: 2021/2/4 5:42 下午
@contact: dun.yuan@nio.com
@description:
    data report提测： http://venus.nioint.com/#/detailWorkflow/wf-20210202155053-f5
    evm server提测：  http://venus.nioint.com/#/detailWorkflow/wf-20210202160114-x6
    通过data report的Notify EVM接口设定事件类型data_recover_by_time发送请求，来通知evm按vid和时间范围补发充电和行程的数据
@showdoc：http://showdoc.nevint.com/index.php?s=/datareport&page_id=2288
"""
import allure
import datetime
import time
import pytest
from utils import evm_nofity


@pytest.mark.skip('Manual')
class TestProcessEVMNotifyMessages(object):
    def test_evm_notify_recover_by_time(self, cmdopt, vid, vin, cassandra):
        with allure.step("统计要恢复的消息条数"):
            charge_events = cassandra['datacollection'].fetch('vehicle_data',
                                                              where_model={'vehicle_id': vid,
                                                                           'sample_ts>': '2021-02-02 10:00:00',
                                                                           'sample_ts<': '2021-02-03 00:00:00',
                                                                           'msg_type': 'periodical_charge_update'
                                                                           })
            time.sleep(1)
            journey_events = cassandra['datacollection'].fetch('vehicle_data',
                                                               where_model={'vehicle_id': vid,
                                                                            'sample_ts>': '2021-02-02 10:00:00',
                                                                            'sample_ts<': '2021-02-03 00:00:00',
                                                                            'msg_type': 'periodical_journey_update'
                                                                            })
            count = len(charge_events) + len(journey_events)
        with allure.step("向data report发送请求，恢复指定时间段的数据"):
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            events = [
                {
                    "type": "data_recover_by_time",
                    "data_recover_by_time": [
                        {
                            "vin": vin,
                            "start_time": 1612231200000,
                            "end_time": 1612281600000
                        }
                    ]
                }]
            evm_nofity.evm_nofify_api(cmdopt=cmdopt, events=events)
        with allure.step("查询生成evm message的条目数"):
            time.sleep(5)
            evm_msgs = cassandra['datacollection'].fetch('evm_message',
                                                         where_model={'vin': vin,
                                                                      'insert_ts>': dt
                                                                      })
            assert len(evm_msgs) == count
