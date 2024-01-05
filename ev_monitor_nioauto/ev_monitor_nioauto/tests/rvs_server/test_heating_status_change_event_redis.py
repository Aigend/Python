""" 
@author:dun.yuan
@time: 2022/3/13 4:19 PM
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""


class TestHeatingChangeMsg(object):
    def test_heating_status_change_event_redis(self, checker, publish_msg_by_kafka):
        # 构造并上报消息
        nextev_message, heating_change_obj = publish_msg_by_kafka('heating_status_change_event', platform_type=1)

        # 校验
        keys = ['HeatingStatus']
        checker.check_redis(heating_change_obj, keys,
                            event_name='heating_status_change_event',
                            sample_ts=heating_change_obj['sample_ts'])
