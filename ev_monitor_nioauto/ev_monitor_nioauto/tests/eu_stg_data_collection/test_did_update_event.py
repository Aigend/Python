""" 
@author:dun.yuan
@time: 2021/6/19 11:52 下午
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import datetime
import allure

from utils import message_formator
from utils.assertions import assert_equal


class TestDidUpdateMsg(object):
    def test_history_did_data(self, vid, publish_msg, checker,redis_key_front, redis):
        # 构造并上报消息
        nextev_message, did_update_obj = publish_msg('did_update_event', did_data_num=1, sleep_time=30)

        # 校验 history_did_data
        with allure.step("校验 did_update_in_message 存入 history_did_data表"):
            sample_date = datetime.datetime.fromtimestamp(did_update_obj['did_data'][0]['dids'][0]['sample_ts'] / 1000).strftime('%Y-%m')
            did_update_in_cassandra = checker.cassandra.fetch('history_did_data',
                                                                        {'vehicle_id': vid,
                                                                         'sample_date': str(sample_date),
                                                                         'tag': did_update_obj['did_tag']
                                                                         },
                                                                        ['ecu',
                                                                         'did_id',
                                                                         'value',
                                                                         'sample_ts'
                                                                         ]
                                                                        )
            cassandra_formator = message_formator.MsgToCassandraFormator(vid)
            did_update_in_message = cassandra_formator.to_cassandra_history_did(did_update_obj)

            cass_sorted = sorted(did_update_in_cassandra, key=lambda x: x['ecu'] + x['did_id'])
            msg_sorted = sorted(did_update_in_message, key=lambda x: x['ecu'] + x['did_id'])
            assert_equal(cass_sorted, msg_sorted)

        # 校验status_did
        tables = ['status_did']
        checker.check_mysql_tables(did_update_obj, tables)

        # 校验redis 需用欧洲堡垒机
        # with allure.step("验证did 存入 redis"):
        #     data_collection_key_front = redis_key_front['data_collection']
        #     name = f'{data_collection_key_front}:did_data:{vid}'
        #     for item in did_update_obj['did_data'][0]['dids']:
        #         did_in_redis = redis.hash_hget(name=name, key=did_update_obj['did_data'][0]['ecu'] + '_' + item['id'])
        #         assert_equal(did_in_redis, item['value'])