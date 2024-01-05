#!/usr/bin/env python
# coding=utf-8

"""
:author: li.liu
"""
import copy
import datetime
import random
import time
import allure
import pytest

from utils.assertions import assert_equal
from utils.time_parse import timestamp_to_utc_strtime


class TestDidUpdateMsg(object):
    def test_did_update_msg(self, checker, publish_msg):
        # 构造并上报消息
        nextev_message, did_update_obj = publish_msg('did_update_event', did_data_num=1)

        # 校验status_did
        tables = ['status_did']
        checker.check_mysql_tables(did_update_obj, tables)

    def test_invalid_value_format(self, vid, checker, publish_msg):

        with allure.step("校验 RVS数据库中存储F110/F118/F130/F140须满足零件号规范:一个大写字母+7个数字+空格+2个大写字母"):
            # 原始
            did_in_mysql_cgw_orig = checker.mysql.fetch('status_did', {"vid": vid, "ecu": 'CGW', "didid!=": 'F18C'})
            did_in_mysql_vcu_orig = checker.mysql.fetch('status_did', {"vid": vid, "ecu": 'VCU', "didid!=": 'F18C'})
            # 上报
            sample_ts = int(time.time() * 1000)
            sample_time = timestamp_to_utc_strtime(sample_ts)[:-3]
            did_data_list = [{"ecu": "VCU",
                              "dids": [{"id": "F110", "value": "p1234001 AA", "sample_ts": sample_ts},
                                       {"id": "F118", "value": "P123400 AA", "sample_ts": sample_ts},
                                       {"id": "F18C", "value": "P{:0>7} AB".format(random.randint(0, 9999999)), "sample_ts": sample_ts},
                                       {"id": "F130", "value": "P1234004 a", "sample_ts": sample_ts}]
                              },
                             {"ecu": "CGW",
                              "dids": [{"id": "F110", "value": "P2234331 AAA", "sample_ts": sample_ts},
                                       {"id": "F118", "value": "P2234332AA", "sample_ts": sample_ts},
                                       {"id": "F18C", "value": "P{:0>7} AB".format(random.randint(0, 9999999)), "sample_ts": sample_ts},
                                       {"id": "F140", "value": "P22343344 AA", "sample_ts": sample_ts}]
                              }]
            nextev_message, obj = publish_msg('did_update_event', did_data_list=did_data_list)

            # 校验含非法数值时上报不成功
            # did_in_mysql_cgw_new = checker.mysql.fetch('status_did', {"vid": vid, 'sample_time': sample_time, "ecu": 'CGW', "didid!=": 'F18C'})
            did_in_mysql_cgw_new = checker.mysql.fetch('status_did', {"vid": vid,  "ecu": 'CGW', "didid!=": 'F18C'})
            # did_in_mysql_vcu_new = checker.mysql.fetch('status_did', {"vid": vid, 'sample_time': sample_time, "ecu": 'VCU', "didid!=": 'F18C'})
            did_in_mysql_vcu_new = checker.mysql.fetch('status_did', {"vid": vid,  "ecu": 'VCU', "didid!=": 'F18C'})
            assert_equal(did_in_mysql_cgw_orig, did_in_mysql_cgw_new)
            assert_equal(did_in_mysql_vcu_orig, did_in_mysql_vcu_new)

            # 校验同时上传的合法字符上报成功
            for i in range(len(did_data_list)):
                did_in_mysql_F18C = checker.mysql.fetch('status_did', {"vid": vid, 'sample_time': sample_time, "ecu": did_data_list[i]['ecu'], "didid": 'F18C'}, fields=['didid as id', 'value', 'sample_time'])[0]
                did_in_msg_F18C = obj['did_data'][i]['dids'][2]
                did_in_msg_F18C['sample_time'] = str(datetime.datetime.utcfromtimestamp(int(did_in_msg_F18C.pop('sample_ts')) / 1000.0))
                del(did_in_msg_F18C['err_code'])
                assert_equal(did_in_mysql_F18C, did_in_msg_F18C)

    def test_invalid_value_empty(self, vid, checker, publish_msg):
        with allure.step("校验 RVS数据库status_did表不存储空值"):
            # 原始
            did_in_mysql_cgw_orig = checker.mysql.fetch('status_did', {"vid": vid, "ecu": 'CGW', "didid!=": 'F18C'})
            did_in_mysql_vcu_orig = checker.mysql.fetch('status_did', {"vid": vid, "ecu": 'VCU'})
            # 上报
            sample_ts = int(time.time() * 1000)
            sample_time = timestamp_to_utc_strtime(sample_ts)[:-3]
            did_data_list = [{"ecu": "VCU",
                              "dids": [{"id": "F110", "value": "", "sample_ts": sample_ts},
                                       {"id": "F118", "value": "", "sample_ts": sample_ts},
                                       {"id": "F18C", "value": "", "sample_ts": sample_ts},
                                       {"id": "F130", "value": "", "sample_ts": sample_ts}]
                              },
                             {"ecu": "CGW",
                              "dids": [{"id": "F110", "value": "", "sample_ts": sample_ts},
                                       {"id": "F118", "value": "", "sample_ts": sample_ts},
                                       {"id": "F18C", "value": "P2234333 AD", "sample_ts": sample_ts},
                                       {"id": "F140", "value": "", "sample_ts": sample_ts},
                                       {"id": "F141", "value": "", "sample_ts": sample_ts},
                                       {"id": "F190", "value": "", "sample_ts": sample_ts},
                                       {"id": "F100", "value": "", "sample_ts": sample_ts}]
                              }]
            nextev_message, obj = publish_msg('did_update_event', did_data_list=did_data_list)

            # 校验含空数值时status_did表不存储
            did_in_mysql_cgw_new = checker.mysql.fetch('status_did', {"vid": vid, "ecu": 'CGW', "didid!=": 'F18C'})
            did_in_mysql_vcu_new = checker.mysql.fetch('status_did', {"vid": vid,  "ecu": 'VCU'})
            assert_equal(did_in_mysql_cgw_orig, did_in_mysql_cgw_new)
            assert_equal(did_in_mysql_vcu_orig, did_in_mysql_vcu_new)

            # 校验同时上传的非空合法字符status_did表存储
            did_in_mysql_F18C = checker.mysql.fetch('status_did', {"vid": vid, 'sample_time': sample_time, "ecu": did_data_list[1]['ecu'], "didid": 'F18C'}, fields=['didid as id', 'value', 'sample_time'])[0]
            did_in_msg_F18C = obj['did_data'][1]['dids'][2]
            did_in_msg_F18C['sample_time'] = str(datetime.datetime.utcfromtimestamp(int(did_in_msg_F18C.pop('sample_ts')) / 1000.0))
            del (did_in_msg_F18C['err_code'])
            assert_equal(did_in_mysql_F18C, did_in_msg_F18C)

    def test_invalid_value_non_ascii(self, vid, checker, publish_msg):
        with allure.step("校验 RVS数据库中存储F120/F141必须是ASCII字符"):
            # 原始
            did_in_mysql_bms_orig = checker.mysql.fetch('status_did', {"vid": vid, "ecu": 'BMS', "didid": 'F120'})
            did_in_mysql_cgw_orig = checker.mysql.fetch('status_did', {"vid": vid, "ecu": 'CGW', "didid": 'F141'})
            # 上报
            sample_ts = int(time.time() * 1000)
            sample_time = timestamp_to_utc_strtime(sample_ts)[:-3]
            did_data_list = [{"ecu": "BMS",
                              "dids": [{"id": "F110", "value": "P{:0>7} AD".format(random.randint(0, 9999999)), "sample_ts": sample_ts},
                                       {"id": "F118", "value": "P{:0>7} AD".format(random.randint(0, 9999999)), "sample_ts": sample_ts},
                                       {"id": "F18C", "value": "P{:0>7} AA".format(random.randint(0, 9999999)), "sample_ts": sample_ts},
                                       {"id": "F120", "value": "非ASCII", "sample_ts": sample_ts}]
                              },
                             {"ecu": "CGW",
                              "dids": [{"id": "F110", "value": "P{:0>7} AA".format(random.randint(0, 9999999)), "sample_ts": sample_ts},
                                       {"id": "F118", "value": "P{:0>7} AA".format(random.randint(0, 9999999)), "sample_ts": sample_ts},
                                       {"id": "F18C", "value": "P{:0>7} AA".format(random.randint(0, 9999999)), "sample_ts": sample_ts},
                                       {"id": "F141", "value": "非ASCII", "sample_ts": sample_ts}]
                              }
                             ]
            nextev_message, obj = publish_msg('did_update_event', did_data_list=did_data_list)

            # 校验含非法数值时上报不成功
            did_in_mysql_bms_new = checker.mysql.fetch('status_did', {"vid": vid, "ecu": 'BMS', "didid": 'F120'})
            did_in_mysql_cgw_new = checker.mysql.fetch('status_did', {"vid": vid, "ecu": 'CGW', "didid": 'F141'})
            assert_equal(did_in_mysql_bms_orig, did_in_mysql_bms_new)
            assert_equal(did_in_mysql_cgw_orig, did_in_mysql_cgw_new)

            # 校验同时上传的合法字符上报成功
            for i in range(len(did_data_list)):
                did_in_mysql_F110 = checker.mysql.fetch('status_did', {"vid": vid, 'sample_time': sample_time, "ecu": did_data_list[i]['ecu'], "didid": 'F110'}, fields=['didid as id', 'value', 'sample_time'])[0]
                did_in_msg_F110 = obj['did_data'][i]['dids'][0]
                del (did_in_msg_F110['err_code'])
                did_in_msg_F110['sample_time'] = str(datetime.datetime.utcfromtimestamp(int(did_in_msg_F110.pop('sample_ts')) / 1000.0))
                assert_equal(did_in_mysql_F110, did_in_msg_F110)

                did_in_mysql_F118 = checker.mysql.fetch('status_did', {"vid": vid, 'sample_time': sample_time, "ecu": did_data_list[i]['ecu'], "didid": 'F118'}, fields=['didid as id', 'value', 'sample_time'])[0]
                did_in_msg_F118 = obj['did_data'][i]['dids'][1]
                del (did_in_msg_F118['err_code'])
                did_in_msg_F118['sample_time'] = str(datetime.datetime.utcfromtimestamp(int(did_in_msg_F118.pop('sample_ts')) / 1000.0))
                assert_equal(did_in_mysql_F118, did_in_msg_F118)

                did_in_mysql_F18C = checker.mysql.fetch('status_did', {"vid": vid, 'sample_time': sample_time, "ecu": did_data_list[i]['ecu'], "didid": 'F18C'}, fields=['didid as id', 'value', 'sample_time'])[0]
                did_in_msg_F18C = obj['did_data'][i]['dids'][2]
                del (did_in_msg_F18C['err_code'])
                did_in_msg_F18C['sample_time'] = str(datetime.datetime.utcfromtimestamp(int(did_in_msg_F18C.pop('sample_ts')) / 1000.0))
                assert_equal(did_in_mysql_F18C, did_in_msg_F18C)

    @pytest.mark.test
    def test_log_did_data(self, vid, checker, redis, redis_key_front, publish_msg):
        # sample_ts = int(time.time() * 1000)
        # did_data_list = [{"ecu": "VCU",
        #                   "dids": [{"id": "F110", "value": "P1234001 AD", "sample_ts": sample_ts},
        #                            {"id": "F118", "value": "P1234002 AD", "sample_ts": sample_ts},
        #                            {"id": "F18C", "value": "P1234003 AA", "sample_ts": sample_ts},
        #                            {"id": "F130", "value": "P1234004 AD", "sample_ts": sample_ts}]
        #                   }
        #                  ]

        # First publish
        nextev_message, obj_old = publish_msg('did_update_event', did_data_num=1)
        # obj_old = publish_msg('did_update_event', did_data_list=did_data_list)

        # Change did data, change the did value except the last dids index
        did_data_list = copy.deepcopy(obj_old['did_data'])
        ts = int(time.time() * 1000)
        for i, item in enumerate(did_data_list[0]['dids']):
            item['sample_ts'] = ts
            if i < len(did_data_list[0]['dids'])-1:
                item['value'] = item['value'][:-2] + 'XX'

        # Random to choose deleting redis data
        # 注意，内存里也存了一份值，取旧值做比较时，旧值的查找顺序是 内存->redis->mysql， 如果要让内存中不存在该值，可以重启服务。
        del_redis_flag = random.choice((True, False))
        if del_redis_flag:
            data_collection_key_front = redis_key_front['data_collection']
            kerwords = f'{data_collection_key_front}:did_data:{vid}'
            redis['cluster'].delete(kerwords)

        # Second publish
        nextev_message, obj_new = publish_msg('did_update_event', did_data_list=did_data_list)

        # 校验 log_did_data
        with allure.step("校验 did_update_in_message 将与第一次上报不同的的数据存入 log_did_data"):
            for i, item in enumerate(obj_new['did_data'][0]['dids']):
                sample_time = str(datetime.datetime.utcfromtimestamp(int(item['sample_ts']) / 1000.0))
                dids_in_mysql = checker.mysql.fetch('log_did_data',
                                                    where_model={"vid": vid,
                                                                 "ecu": obj_new['did_data'][0]['ecu'],
                                                                 "did_id": item['id'],
                                                                 'sample_time': sample_time},
                                                    fields=['did_id as id', 'value', 'sample_time', 'previous_value'],
                                                    retry_num=10
                                                    )

                item['sample_time'] = sample_time
                item.pop('sample_ts')
                item.pop('err_code')
                item['previous_value'] = obj_old['did_data'][0]['dids'][i]['value']

                # Did data will be added to mysql except last one
                if i != len(obj_new['did_data'][0]['dids']) - 1:
                    assert len(dids_in_mysql) == 1
                    assert_equal(dids_in_mysql[0], item)
                # The last one won't add to mysql cause its value didn't changed compared with first publish
                elif i == len(obj_new['did_data'][0]['dids']) - 1:
                    assert len(dids_in_mysql) == 0

    @pytest.mark.test
    def test_log_did_data_when_sample_ts_less_than_db(self, publish_msg, checker, vid):
        with allure.step("校验当sample_ts小于当前数据库里的sample_ts时，did数据不落log_did_data表"):
            # 第一次 publish
            nextev_message, obj_old = publish_msg('did_update_event', did_data_num=1, sleep_time=5)

            # 更新did data数据，并且使sample_ts小于第一次publish时的sample_ts
            did_data_list = copy.deepcopy(obj_old['did_data'])
            second_ts = did_data_list[0]['dids'][0]['sample_ts'] - 3000
            for item in did_data_list[0]['dids']:
                item['value'] = item['value'][:-2] + 'XX'
                item['sample_ts'] = second_ts

            # 第二次 publish
            nextev_message, obj_new = publish_msg('did_update_event', did_data_list=did_data_list)

            # 校验第二次publish后,数据没有落库
            for i, item in enumerate(obj_new['did_data'][0]['dids']):
                sample_time = str(datetime.datetime.utcfromtimestamp(second_ts / 1000.0))
                dids_in_mysql_new = checker.mysql.fetch('log_did_data', retry_num=10,
                                                        where_model={"vid": vid,
                                                                     "ecu": obj_new['did_data'][0]['ecu'],
                                                                     "did_id": item['id'],
                                                                     'sample_time': sample_time}
                                                        )

                assert_equal(len(dids_in_mysql_new), 0)

    @pytest.mark.skip('manual')
    def test_log_did_data_while_not_exist_in_status_did(self, publish_msg_by_kafka, checker, redis, cmdopt):
        """
        校验上报的数据不在mysql.status_did表中时，不仅status_did会更新，log_did_data表也会更新
        bug fix：https://jira.nevint.com/browse/CVS-7415

        该case只能手工运行，因为不能直接删除mysql里的数据来模拟数据不存在status_did表的情况。
        更新mysql的时候会有缓存和redis检测的操作，如果相应的数据存在的话会用更新语句进行更新，而不是用插入语句。
        例如删除了CDC的F110条目数据，上报后，mysql中只更新了F118和F18C两条纪录，而不插入F110
        """
        with allure.step("寻找一个不存在于mysql.status_did的vid与ecu, 然后上报，注意，选取的vid和ecu组合要保证不重复"):
            vid = '31a456088a0f4701868ee6481dc6e372'
            vin = 'SQETEST0899871103'
            sample_ts = int(time.time() * 1000)
            did_data_list = [{"ecu": "CDC",
                              "dids": [{"id": "F110", "value": "P1234001 AD", "sample_ts": sample_ts},
                                       {"id": "F118", "value": "P1234002 AD", "sample_ts": sample_ts},
                                       {"id": "F18C", "value": "P1234003 AA", "sample_ts": sample_ts}]
                              }
                             ]
            # 例如如下sql语句返回null
            """
            select * from status_did where vid='31a456088a0f4701868ee6481dc6e372' and ecu='CDC'
            select * from log_did_data where vid='31a456088a0f4701868ee6481dc6e372' and ecu='CDC'
            """

            # 上报
            publish_msg_by_kafka('did_update_event', vin=vin, vid=vid, did_data_list=did_data_list)

        with allure.step("校验status_did表有完整的更新"):
            """
            select * from status_did where vid='31a456088a0f4701868ee6481dc6e372' and ecu='CDC' 
            
            id	                vid	                                tag	                ecu	didid	value	    sample_time	update_time
            8232710239530500079	31a456088a0f4701868ee6481dc6e372	did_tag1554796377	CDC	F110	P1234001 AD	2019-04-09 07:52:57.197	2019-04-09 07:52:58.678
            8232710239530500079	31a456088a0f4701868ee6481dc6e372	did_tag1554796377	CDC	F118	P1234002 AD	2019-04-09 07:52:57.197	2019-04-09 07:52:58.680
            8232710239530500077	31a456088a0f4701868ee6481dc6e372	did_tag1554796377	CDC	F18C	P1234003 AA	2019-04-09 07:52:57.197	2019-04-09 07:52:58.674
            """
            pass
        with allure.step("校验log_did_data表有完整的更新"):
            """
            select * from log_did_data where vid='31a456088a0f4701868ee6481dc6e372' and ecu='CDC'
            
            id	    vid	                                tag	                ecu	did_id	value	    sample_time	update_time	previous_value
            7300	31a456088a0f4701868ee6481dc6e372	did_tag1554795894	CDC	F110	P1234001 AD	2019-04-09 07:44:54.915	2019-04-09 07:44:57.208	NULL
            7301	31a456088a0f4701868ee6481dc6e372	did_tag1554795894	CDC	F118	P1234002 AD	2019-04-09 07:44:54.915	2019-04-09 07:44:57.211	NULL
            7302	31a456088a0f4701868ee6481dc6e372	did_tag1554795894	CDC	F18C	P1234003 AA	2019-04-09 07:44:54.915	2019-04-09 07:44:57.215	NULL
            """

    def test_status_package_version(self, vid, checker, publish_msg_by_kafka):

        with allure.step("校验 CGW 上报的F140， F141的值会写入mysql的status_package_version表中相应的 package_part_number, package_global_version"):
            sample_ts = int(time.time() * 1000)
            sample_time = str(datetime.datetime.utcfromtimestamp(int(sample_ts) / 1000.0))
            did_data_list = [
                {"ecu": random.choice(['CGW', 'BGW']),
                 "dids": [{"id": "F110", "value": "P2234331 AD", "sample_ts": sample_ts},
                          {"id": "F118", "value": "P2234332 AD", "sample_ts": sample_ts},
                          {"id": "F140", "value": "P2234334 AD", "sample_ts": sample_ts},
                          {"id": "F141", "value": "P2234335 AD", "sample_ts": sample_ts}
                          ]
                 }]
            nextev_message, obj = publish_msg_by_kafka('did_update_event', did_data_list=did_data_list)
            did_in_status_package_version = checker.mysql.fetch('status_package_version', {"id": vid, 'sample_time': sample_time},
                                                                fields=['id', 'package_part_number as F140', 'package_global_version as F141', 'sample_time'])[0]

            did_in_msg = {
                'id': vid,
                'F140': obj['did_data'][0]['dids'][2]['value'],
                'F141': obj['did_data'][0]['dids'][3]['value'],
                'sample_time': sample_time
            }

            assert_equal(did_in_status_package_version, did_in_msg)

    def test_status_package_version_invalid_value(self, vid, checker, publish_msg_by_kafka):
        ecu = random.choice(['CGW', 'BGW'])
        with allure.step("校验 status_package_version表不存储空值"):
            # 原始
            did_in_mysql_orig = checker.mysql.fetch('status_package_version', {"id": vid})[0]
            # 上报
            sample_ts = int(time.time() * 1000)
            sample_time = str(datetime.datetime.utcfromtimestamp(int(sample_ts) / 1000.0))
            did_data_list = [
                {"ecu": ecu,
                 "dids": [{"id": "F110", "value": "", "sample_ts": sample_ts},
                          {"id": "F118", "value": "", "sample_ts": sample_ts},
                          {"id": "F140", "value": "", "sample_ts": sample_ts},
                          {"id": "F141", "value": "", "sample_ts": sample_ts},
                          ]
                 }]
            nextev_message, obj = publish_msg_by_kafka('did_update_event', did_data_list=did_data_list, sleep_time=5 if checker.cmdopt == 'stg' else 2)

            # 校验含空数值时status_did表不存储
            did_in_mysql_new = checker.mysql.fetch('status_package_version', {"id": vid})[0]
            assert_equal(did_in_mysql_orig, did_in_mysql_new)

        with allure.step("校验 status_package_version存储F140须满足零件号规范:一个大写字母+7个数字+空格+2个大写字母"):
            # 原始
            did_in_mysql_orig = checker.mysql.fetch('status_package_version', {"id": vid,},
                                                    fields=['id', 'package_part_number as F140', 'package_global_version as F141', 'sample_time'])[0]
            # 上报
            sample_ts = int(time.time() * 1000)
            sample_time = str(datetime.datetime.utcfromtimestamp(int(sample_ts) / 1000.0))
            did_data_list = [
                {"ecu": ecu,
                 "dids": [{"id": "F110", "value": "", "sample_ts": sample_ts},
                          {"id": "F118", "value": "", "sample_ts": sample_ts},
                          {"id": "F140", "value": "Invalid", "sample_ts": sample_ts},
                          {"id": "F141", "value": "valid", "sample_ts": sample_ts},
                          ]
                 }]
            nextev_message, obj = publish_msg_by_kafka('did_update_event', did_data_list=did_data_list)

            did_in_mysql_new = checker.mysql.fetch('status_package_version', {"id": vid, 'sample_time': sample_time},
                                                   fields=['id', 'package_part_number as F140', 'package_global_version as F141', 'sample_time'])[0]

            # F140 没存入数据库
            assert_equal(did_in_mysql_new['F140'], did_in_mysql_orig['F140'])
            # F141 存入了数据库，且sample_ts更新了
            assert_equal(did_in_mysql_new['F141'], obj['did_data'][0]['dids'][3]['value'])
            assert_equal(did_in_mysql_new['sample_time'], sample_time)

        with allure.step("校验 status_package_version中存储F141必须是ASCII字符"):
            # 原始
            did_in_mysql_orig = checker.mysql.fetch('status_package_version', {"id": vid},
                                                    fields=['id', 'package_part_number as F140', 'package_global_version as F141', 'sample_time'])[0]
            # 上报
            sample_ts = int(time.time() * 1000)
            sample_time = str(datetime.datetime.utcfromtimestamp(int(sample_ts) / 1000.0))
            did_data_list = [
                {"ecu": ecu,
                 "dids": [{"id": "F110", "value": "", "sample_ts": sample_ts},
                          {"id": "F118", "value": "", "sample_ts": sample_ts},
                          {"id": "F140", "value": "P2234011 AD", "sample_ts": sample_ts},
                          {"id": "F141", "value": "非ASCII", "sample_ts": sample_ts},
                          ]
                 }]
            nextev_message, obj = publish_msg_by_kafka('did_update_event', did_data_list=did_data_list)

            did_in_mysql_new = checker.mysql.fetch('status_package_version', {"id": vid, 'sample_time': sample_time},
                                                   fields=['id', 'package_part_number as F140', 'package_global_version as F141', 'sample_time'])[0]

            # F141 没存入数据库
            assert_equal(did_in_mysql_new['F141'], did_in_mysql_orig['F141'])

            # F140 存入了数据库，且sample_ts更新了
            assert_equal(did_in_mysql_new['F140'], obj['did_data'][0]['dids'][2]['value'])
            assert_equal(did_in_mysql_new['sample_time'], sample_time)
