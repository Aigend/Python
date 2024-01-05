#!/usr/bin/env python
# coding=utf-8

"""
@author: chunming.liu
@Date: 2019/3/4
@Feature: 1)evm_server消费swc-tsp-data_report-{}-evm_internal_command的数据，对行为做出改变
          2)数据表vehicle_config_mock添加数据，ack=0，则mock_server不处理ack=-1的数据
"""
import datetime
import allure
import time,os
import requests
import pytest

from utils import time_parse
from utils.commonlib import show_json
import json
from utils.commonlib import get_test_data1


# Read test data
test_data = os.path.join(os.path.dirname(__file__).split(os.sep + 'test', 1)[0] + os.sep + 'data', 'evm_server', 'evm_notify.json')
case, precondition, parameter = get_test_data1(test_data)

class TestProcessEVMNotifyMessages(object):
    @pytest.fixture(scope='function', autouse=True)
    def prepare(self, mysql, env, request):
        # 查询数据表vehicle_config_mock,如果不存在，就插入数据
        mysql_data = mysql['rvs'].fetch('vehicle_config_mock',
                                        {"vin in": (env['vehicles']['sh_private']['vin'], env['vehicles']['sh_public']['vin']),
                                         "command": 2,
                                         "ack": 0,
                                         "port": 5555
                                         }
                                        )
        if len(mysql_data) == 0:
            mysql['rvs'].insert('vehicle_config_mock', {
                "vin": env['vehicles']['sh_private']['vin'],
                "command": 2,
                "ack": 0,
                "port": 5555
            })
            mysql['rvs'].insert('vehicle_config_mock', {
                "vin": env['vehicles']['sh_public']['vin'],
                "command": 2,
                "ack": 0,
                "port": 5555
            })

        def fin():
            mysql['rvs'].delete('vehicle_config_mock',{"vin": env['vehicles']['sh_private']['vin'],
                "command": 2,
                "ack": 0,
                "port": 5555})
            mysql['rvs'].delete('vehicle_config_mock', {"vin": env['vehicles']['sh_public']['vin'],
                "command": 2,
                "ack": 0,
                "port": 5555})

        request.addfinalizer(fin)

    @pytest.mark.parametrize("checkpoint,headers,querystring,payload,expected", parameter)
    # evm/notify接口 clean_unsent_evm_message 事件只在 stg 环境生效
    @pytest.mark.skip()
    def test_set_ack_to_2_when_receiving_clean_unsent_evm_message(self, env, api, cmdopt, cassandra, checkpoint, headers, querystring, payload, expected):
        #请求periodical_charge_update接口，向kafka插入数据,插入两条数据
        url1 = env['host']['mock'] + api['mock']['publish_periodical_charge_update']
        querystring1 = {'vin': env['vehicles']['sh_private']['vin'], 'vid': env['vehicles']['sh_private']['vehicle_id'], 'env' : cmdopt}
        querystring2 = {'vin': env['vehicles']['sh_public']['vin'], 'vid': env['vehicles']['sh_public']['vehicle_id'], 'env' : cmdopt}
        headers1 = precondition['headers']
        payload1 = precondition['payload']
        with allure.step("第一条数据：发布sh_private到kafka"):
            r1 = requests.request("POST", url1, params=querystring1, data=json.dumps(payload1), headers=headers1)
            charge_update_osh1 = (r1.json())['data']
            sample_ts1 = charge_update_osh1['sample_points'][0]['sample_ts']
        with allure.step("第二条数据：发布sh_public到kafka"):
            r2 = requests.request("POST", url1, params=querystring2, data=json.dumps(payload1), headers=headers1)
            charge_update_osh = (r2.json())['data']
            insert_date = time_parse.utc_to_local(timestamp=charge_update_osh['sample_points'][0]['sample_ts'] / 1000.0, offset_hour=8)

        with allure.step("查询Cassandra数据库中的数据, sh_private数据"):
            gb_evm_message_in_cassandra1 = cassandra['datacollection'].fetch('evm_message',
                                                                            {'vin': env['vehicles']['sh_private']['vin'],
                                                                             'insert_date': insert_date,
                                                                             'attribution': 156
                                                                             },
                                                                            ["vin", "ack", "type", "attribution", "domain",
                                                                             "blobAsBigint(timestampAsBlob(sample_ts)) as sample_ts",
                                                                             "blobAsBigint(timestampAsBlob(insert_ts)) as insert_ts"
                                                                             ],
                                                                            )
        with allure.step("查询Cassandra数据库中的数据, sh_public数据"):
            gb_evm_message_in_cassandra2 = cassandra['datacollection'].fetch('evm_message',
                                                                            {'vin': env['vehicles']['sh_public']['vin'],
                                                                             'insert_date': insert_date,
                                                                             'attribution': 156
                                                                             },
                                                                            ["vin", "ack", "type", "attribution", "domain",
                                                                             "blobAsBigint(timestampAsBlob(sample_ts)) as sample_ts",
                                                                             "blobAsBigint(timestampAsBlob(insert_ts)) as insert_ts"
                                                                             ],
                                                                            )
        with allure.step("校验Cassandra数据库的evm_message表中,sh_private数据的ack是-1"):
            allure.attach(show_json(gb_evm_message_in_cassandra1),"sh_private,evm_message内容")
            assert gb_evm_message_in_cassandra1[-1]['vin'] == env['vehicles']['sh_private']['vin']
            assert gb_evm_message_in_cassandra1[-1]['domain'] == env['vehicles']['sh_private']['domain']
            assert gb_evm_message_in_cassandra1[-1]['attribution'] == 156
            assert gb_evm_message_in_cassandra1[-1]['ack'] == -1
            assert gb_evm_message_in_cassandra1[-1]['type'] == 2
            assert gb_evm_message_in_cassandra1[-1]['sample_ts'] == sample_ts1
        with allure.step("校验Cassandra数据库的evm_message表中,sh_public数据的ack是-1"):
            allure.attach(show_json(gb_evm_message_in_cassandra2),"sh_public,evm_message内容")
            assert gb_evm_message_in_cassandra2[-1]['vin'] == env['vehicles']['sh_public']['vin']
            assert gb_evm_message_in_cassandra2[-1]['domain'] == env['vehicles']['sh_public']['domain']
            assert gb_evm_message_in_cassandra2[-1]['attribution'] == 156
            assert gb_evm_message_in_cassandra2[-1]['ack'] == -1
            assert gb_evm_message_in_cassandra2[-1]['type'] == 2
            assert gb_evm_message_in_cassandra2[-1]['sample_ts'] == charge_update_osh['sample_points'][0]['sample_ts']

        with allure.step("调用evm/notify接口, start_ts 和end_ts必须包含insert_ts时间，start_ts <= insert_ts < end_ts"):
            url = env['host']['tsp_in'] + api['vms']['evm_notify']
            payload['events'][0]['cleans'][0]['start_ts'] = gb_evm_message_in_cassandra1[-1]['insert_ts']
            payload['events'][0]['cleans'][0]['end_ts'] = gb_evm_message_in_cassandra2[-1]['insert_ts'] + 500
            payload['events'] = json.dumps(payload['events'])
            response = requests.request("POST", url, params=querystring, data=payload, headers=headers)
            if (response.json())['result_code'] == 'success':
                pass
            else:
                assert "调用notify接口失败"
            time.sleep(1)

        with allure.step("再次查询Cassandra数据库中的数据，sh_private数据"):
            gb_evm_message_in_cassandra1 = cassandra['datacollection'].fetch('evm_message',
                                                                            {'vin': env['vehicles']['sh_private']['vin'],
                                                                             'insert_date': insert_date,
                                                                             'attribution': 156
                                                                             },
                                                                            ["vin", "ack", "type", "attribution", "domain",
                                                                             "blobAsBigint(timestampAsBlob(sample_ts)) as sample_ts",
                                                                             "blobAsBigint(timestampAsBlob(insert_ts)) as insert_ts"
                                                                             ],
                                                                            )
        with allure.step("再次查询Cassandra数据库中的数据，sh_publick数据"):
            gb_evm_message_in_cassandra2 = cassandra['datacollection'].fetch('evm_message',
                                                                             {'vin': env['vehicles']['sh_public']['vin'],
                                                                              'insert_date': insert_date,
                                                                              'attribution': 156
                                                                              },
                                                                             ["vin", "ack", "type", "attribution", "domain",
                                                                              "blobAsBigint(timestampAsBlob(sample_ts)) as sample_ts",
                                                                              "blobAsBigint(timestampAsBlob(insert_ts)) as insert_ts"
                                                                              ],
                                                                             )

        with allure.step("校验Cassandra数据库的evm_message表中sh_private数据的ack变成了2"):
            allure.attach(show_json(gb_evm_message_in_cassandra1),"evm_message内容")
            assert gb_evm_message_in_cassandra1[-1]['vin'] == env['vehicles']['sh_private']['vin']
            assert gb_evm_message_in_cassandra1[-1]['domain'] == env['vehicles']['sh_private']['domain']
            assert gb_evm_message_in_cassandra1[-1]['attribution'] == 156
            assert gb_evm_message_in_cassandra1[-1]['ack'] == 2
            assert gb_evm_message_in_cassandra1[-1]['type'] == 2
            assert gb_evm_message_in_cassandra1[-1]['sample_ts'] == sample_ts1
        with allure.step("校验Cassandra数据库的evm_message表中sh_publick数据的ack仍为-1"):
            allure.attach(show_json(gb_evm_message_in_cassandra2),"evm_message内容")
            assert gb_evm_message_in_cassandra2[-1]['vin'] == env['vehicles']['sh_public']['vin']
            assert gb_evm_message_in_cassandra2[-1]['domain'] == env['vehicles']['sh_public']['domain']
            assert gb_evm_message_in_cassandra2[-1]['attribution'] == 156
            assert gb_evm_message_in_cassandra2[-1]['ack'] == -1
            assert gb_evm_message_in_cassandra2[-1]['type'] == 2
            assert gb_evm_message_in_cassandra2[-1]['sample_ts'] == charge_update_osh['sample_points'][0]['sample_ts']


