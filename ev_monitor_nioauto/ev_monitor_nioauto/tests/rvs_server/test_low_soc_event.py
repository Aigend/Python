""" 
@author:dun.yuan
@time: 2020/12/25 7:19 下午
@contact: dun.yuan@nio.com
@description: 提测 http://venus.nioint.com/#/detailWorkflow/wf-20201223160011-LM
             CDC上报低电量事件到kafka topic 30007
             低电量推送kafka条件：本次状态值大于上一次
@showdoc：push_event kafka http://showdoc.nevint.com/index.php?s=/11&page_id=24395
"""
import allure
import json
import pytest
from utils.assertions import assert_equal


class TestLowSocEvent(object):
    @pytest.fixture(scope='function', autouse=True)
    def prepare(self, env, publish_msg_cdc, request):
        def fin():
            publish_msg_cdc('low_soc_event', low_soc_range={'low_soc_status': 0})

        request.addfinalizer(fin)

    def test_low_soc_event_redis(self, vid, redis_key_front, publish_msg_cdc, checker, kafka):
        # 重置offset
        kafka['cvs'].set_offset_to_end(kafka['topics']['push_event'])

        # 构造并上报黄色告警
        nextev_message, low_soc_obj = publish_msg_cdc('low_soc_event', low_soc_range={'low_soc_status': 1})

        with allure.step("校验redis内SpecialStatus会记录low soc以及low_soc_sample_time"):
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            key = remote_vehicle_key_front + ':vehicle_status:' + vid + ':SpecialStatus'
            status_soc_in_redis = json.loads(checker.redis.get(key))
            assert_equal(status_soc_in_redis['low_soc'], low_soc_obj['low_soc_range']['low_soc_status'])
            assert_equal(status_soc_in_redis['low_soc_sample_time'], low_soc_obj['sample_ts'] // 1000)

        with allure.step('校验 {}'.format(kafka['topics']['push_event'])):
            is_push = False
            for data in kafka['cvs'].consume(kafka['topics']['push_event'], timeout=10):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                if kafka_msg['data']['sample_time'] // 1000 == status_soc_in_redis['low_soc_sample_time'] and vid == \
                        kafka_msg['vehicle_id']:
                    assert_equal(status_soc_in_redis['low_soc'], kafka_msg['data']['low_soc_status'])
                    is_push = True
            assert is_push

        # 构造并上报红色告警
        nextev_message, low_soc_obj = publish_msg_cdc('low_soc_event', low_soc_range={'low_soc_status': 2})

        with allure.step("校验redis内SpecialStatus会记录low soc以及low_soc_sample_time"):
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            key = remote_vehicle_key_front + ':vehicle_status:' + vid + ':SpecialStatus'
            status_soc_in_redis1 = json.loads(checker.redis.get(key))
            assert_equal(status_soc_in_redis1['low_soc'], low_soc_obj['low_soc_range']['low_soc_status'])
            assert_equal(status_soc_in_redis1['low_soc_sample_time'], low_soc_obj['sample_ts'] // 1000)

        with allure.step('校验 {}'.format(kafka['topics']['push_event'])):
            is_push = False
            for data in kafka['cvs'].consume(kafka['topics']['push_event'], timeout=10):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                if kafka_msg['data']['sample_time'] // 1000 == status_soc_in_redis1['low_soc_sample_time'] and vid == \
                        kafka_msg['vehicle_id']:
                    assert_equal(status_soc_in_redis1['low_soc'], kafka_msg['data']['low_soc_status'])
                    is_push = True
            assert is_push

        # 再次构造并上报红色告警
        publish_msg_cdc('low_soc_event', low_soc_range={'low_soc_status': 2})

        with allure.step("校验redis内SpecialStatus不会更新"):
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            key = remote_vehicle_key_front + ':vehicle_status:' + vid + ':SpecialStatus'
            status_soc_in_redis = json.loads(checker.redis.get(key))
            assert_equal(status_soc_in_redis['low_soc_sample_time'], status_soc_in_redis1['low_soc_sample_time'])

        # 构造并上报无告警
        nextev_message, low_soc_obj = publish_msg_cdc('low_soc_event', low_soc_range={'low_soc_status': 0})

        with allure.step("校验redis内SpecialStatus会记录low soc以及low_soc_sample_time"):
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            key = remote_vehicle_key_front + ':vehicle_status:' + vid + ':SpecialStatus'
            status_soc_in_redis = json.loads(checker.redis.get(key))
            assert_equal(status_soc_in_redis['low_soc'], low_soc_obj['low_soc_range']['low_soc_status'])
            assert_equal(status_soc_in_redis['low_soc_sample_time'], low_soc_obj['sample_ts'] // 1000)

        with allure.step('校验 {}不会收到推送'.format(kafka['topics']['push_event'])):
            for data in kafka['cvs'].consume(kafka['topics']['push_event'], timeout=10):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                if kafka_msg['data']['sample_time'] // 1000 == status_soc_in_redis['low_soc_sample_time']:
                    assert False
            assert True
