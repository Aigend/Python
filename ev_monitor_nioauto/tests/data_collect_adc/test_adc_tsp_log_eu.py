""" 
@author:dun.yuan
@time: 2021/12/4 3:20 下午
@contact: dun.yuan@nio.com
@description: https://nio.feishu.cn/docs/doccnlnIZ8juTQWVqgoysqlJNpg# data_collect_adc 消费欧洲环境上报adc数据
@showdoc：
"""
import allure
import time
import pytest


@pytest.mark.marcopolo
class TestAdcTspLog(object):
    def test_adc_tsp_log_to_s3(self, env, publish_msg_by_kafka_adas, s3):
        with allure.step('检查当前文件数量'):
            date = time.strftime("%Y%m%d")
            print(s3['sqe'].list_object_by_prefix(f'vehicle_logs_adc/10107/{date}/'))
            num = 0 if s3['sqe'].list_object_by_prefix(f'vehicle_logs_adc/10107/{date}/') is None \
                else len(s3['sqe'].list_object_by_prefix(f'vehicle_logs_adc/10107/{date}/'))
        with allure.step('根据当前规则，十个上报消息存为一个文件，故上报十次'):
            for i in range(10):
                publish_msg_by_kafka_adas('tsp_log', sleep_time=0.02)
        with allure.step('根据文件数量增加，验证生成了新文件'):
            time.sleep(2)
            print(s3['sqe'].list_object_by_prefix(f'vehicle_logs_adc/10107/{date}/'))
            assert len(s3['sqe'].list_object_by_prefix(f'vehicle_logs_adc/10107/{date}/')) == num+1
