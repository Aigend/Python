#!/usr/bin/env python
# coding=utf-8

"""
:author: li.liu
"""
import time
import allure

from utils.assertions import assert_equal


class TestDidUpdateMsg(object):
    def test_did_update_redis(self, redis_key_front, redis, vid, publish_msg):
        # 构造并上报消息
        nextev_message, did_update_obj = publish_msg('did_update_event',  did_data_num=1)
        redis = redis['cluster']

        # 校验redis
        with allure.step("验证did 存入 redis"):
            data_collection_key_front = redis_key_front['data_collection']
            name = f'{data_collection_key_front}:did_data:{vid}'
            for item in did_update_obj['did_data'][0]['dids']:
                did_in_redis = redis.hash_hget(name=name, key=did_update_obj['did_data'][0]['ecu'] + '_' + item['id'])
                assert_equal(did_in_redis, item['value'])

    def test_invalid_value_format(self, vid, mysql, publish_msg, redis, redis_key_front):
        redis = redis['cluster']

        with allure.step("校验 Redis数据库中存储F110/F118/F130/F140须满足零件号规范:一个大写字母+7个数字+空格+2个大写字母"):
            # 原始
            did_in_redis_orig = {}
            did_in_redis_orig.update(self._get_redis_did_value('VCU', ('F110', 'F118', 'F130'), vid, redis_key_front, redis))
            did_in_redis_orig.update(self._get_redis_did_value('CGW', ('F110', 'F118', 'F140'), vid, redis_key_front, redis))

            # 上报
            sample_ts = int(time.time() * 1000)
            did_data_list = [{"ecu": "VCU",
                              "dids": [{"id": "F110", "value": "p1234001 AA", "sample_ts": sample_ts},
                                       {"id": "F118", "value": "P123400 AA", "sample_ts": sample_ts},
                                       {"id": "F130", "value": "P1234004 a", "sample_ts": sample_ts}]
                              },
                             {"ecu": "CGW",
                              "dids": [{"id": "F110", "value": "P2234331 AAA", "sample_ts": sample_ts},
                                       {"id": "F118", "value": "P2234332AA", "sample_ts": sample_ts},
                                       {"id": "F140", "value": "P22343344 AA", "sample_ts": sample_ts}]
                              }]
            nextev_message, obj = publish_msg('did_update_event', did_data_list=did_data_list)

            # 新值
            did_in_redis_new = {}
            did_in_redis_new.update(self._get_redis_did_value('VCU', ('F110', 'F118', 'F130'), vid, redis_key_front, redis))
            did_in_redis_new.update(self._get_redis_did_value('CGW', ('F110', 'F118', 'F140'), vid, redis_key_front, redis))

            # 校验含非法数值时上报不成功
            assert_equal(did_in_redis_orig, did_in_redis_new)

    def test_invalid_value_empty(self, vid, mysql, publish_msg, redis, redis_key_front):
        redis = redis['cluster']

        with allure.step("校验 Redis数据库中不存储空值"):
            # 原始
            did_in_redis_orig = {}
            did_in_redis_orig.update(self._get_redis_did_value('VCU', ('F110', 'F118', 'F18C', 'F130'), vid, redis_key_front, redis))
            did_in_redis_orig.update(self._get_redis_did_value('CGW', ('F110', 'F118', 'F140',
                                                                      'F141', 'F190', 'F100'), vid, redis_key_front, redis))

            # 上报
            sample_ts = int(time.time() * 1000)
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

            # 新值
            did_in_redis_new = {}
            did_in_redis_new.update(self._get_redis_did_value('VCU', ('F110', 'F118', 'F18C', 'F130'), vid, redis_key_front, redis))
            did_in_redis_new.update(self._get_redis_did_value('CGW', ('F110', 'F118', 'F140',
                                                                      'F141', 'F190', 'F100'), vid, redis_key_front, redis))

            # 校验含空数值的数据redis不会存储
            assert_equal(did_in_redis_orig, did_in_redis_new)

            # 校验同时上传的非空合法字符redis会存储
            did_in_redis_F18C =self._get_redis_did_value('CGW', ['F18C'], vid, redis_key_front, redis)['CGW_F18C']
            did_in_msg_F18C = obj['did_data'][1]['dids'][2]['value']
            assert_equal(did_in_redis_F18C, did_in_msg_F18C)

    def test_invalid_value_non_ascii(self, vid, mysql, publish_msg, redis_key_front, redis):
        redis = redis['cluster']

        with allure.step("校验 Redis数据库中存储F120/F141必须是ASCII字符"):
            # 原始
            did_in_redis_orig = {}
            did_in_redis_orig.update(self._get_redis_did_value('BMS', ('F110', 'F118', 'F120'), vid, redis_key_front, redis))
            did_in_redis_orig.update(self._get_redis_did_value('CGW', ('F110', 'F118', 'F141'), vid, redis_key_front, redis))

            # 上报
            sample_ts = int(time.time() * 1000)
            did_data_list = [{"ecu": "BMS",
                              "dids": [{"id": "F110","value": "P2234011 AD","sample_ts": sample_ts},
                                       {"id": "F118","value": "P2234012 AD","sample_ts": sample_ts},
                                       {"id": "F120","value": "非ASCII","sample_ts": sample_ts}]
                              },
                             {"ecu": "CGW",
                              "dids": [{"id": "F110", "value": "P2234331 AA", "sample_ts": sample_ts},
                                       {"id": "F118", "value": "P2234332 AA", "sample_ts": sample_ts},
                                       {"id": "F141", "value": "非ASCII", "sample_ts": sample_ts}]
                              }
                             ]
            nextev_message, obj = publish_msg('did_update_event', did_data_list=did_data_list)

            #新值
            did_in_redis_new = {}
            did_in_redis_new.update(self._get_redis_did_value('BMS', ('F110', 'F118', 'F120'), vid, redis_key_front, redis))
            did_in_redis_new.update(self._get_redis_did_value('CGW', ('F110', 'F118', 'F141'), vid, redis_key_front, redis))

            # 校验非法数值上报不成功
            assert_equal(did_in_redis_orig['BMS_F120'], did_in_redis_new['BMS_F120'])
            assert_equal(did_in_redis_orig['CGW_F141'], did_in_redis_new['CGW_F141'])



    def _get_redis_did_value(self, ecu, did_ids, vid, redis_key_front, redis_client):
        dids_in_redis = {}
        data_collection_key_front = redis_key_front['data_collection']
        name = f'{data_collection_key_front}:did_data:{vid}'
        for did_id in did_ids:
            key = ecu +'_'+ did_id
            dids_in_redis[key] = redis_client.hash_hget(name=name, key=key)

        return dids_in_redis


