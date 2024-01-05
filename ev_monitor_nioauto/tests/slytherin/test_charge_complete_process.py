#!/usr/bin/env python
# coding=utf-8

"""
:file:
:author: yry
:Date: Created on 2016/11/11
:Description: 充电开始事件
"""
import pytest
import time
import allure


@pytest.mark.skip("outdate case")
class TestChargeCompleteProcess(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self,mysql, vid):
        original_max_soc_in_mysql = mysql['rvs'].fetch('status_soc',
                                                       {"id": vid
                                                        },
                                                       ['max_soc']
                                                       )[0]['max_soc']

        return {'original_max_soc_in_mysql': original_max_soc_in_mysql}

    def test_charge_process_wont_impact_max_soc(self, vid, publish_msg, checker, prepare):

        # 构造并上报消息
        for i in range(4):
            charge_id = str(int(time.time()))
            soc = 30
            remain_mileage = 100
            dump_enrgy = 60
            nextev_message, charge_start_obj = publish_msg('charge_start_event', soc_status={
                                                                                                "soc":soc,
                                                                                                "remaining_range":remain_mileage,
                                                                                                "dump_enrgy":dump_enrgy
                                                                                            },
                                                                                battery_package_info= {
                                                                                    "btry_pak_encoding": [
                                                                                        {
                                                                                            "btry_pak_sn": 5,
                                                                                            "nio_encoding": "AZUOLMQGSK053HTPY8C7",
                                                                                            "re_encoding": "FWE1J7VD29XI6C8YPTH37"
                                                                                        }
                                                                                    ]
                                                                                },
                                                                                charge_id= charge_id,
                                                                                charging_info= {
                                                                                    "charger_type": 2,
                                                                                    "estimate_chrg_time": 1108,
                                                                                    "in_volt_ac": 8215.2,
                                                                                    "in_volt_dc": 322.45
                                                                                },
                                                                                position_status={
                                                                                    "longitude_uncertainty":0,
                                                                                    "latitude_uncertainty":0,
                                                                                    "altitude_uncertainty":0,
                                                                                    "posng_valid_type":0,
                                                                                    "longitude":116.458847,
                                                                                    "latitude": 40.01946,})
            remain_mileage = 130
            dump_enrgy = 40
            nextev_message, charge_start_obj = publish_msg('charge_end_event', charge_id= charge_id,
                                                                                soc_status= {
                                                                                    "soc": 82,
                                                                                    "remaining_range": remain_mileage,
                                                                                    "dump_enrgy":dump_enrgy
                                                                                },
                                                                                charging_info= {
                                                                                    "charger_type": 3,
                                                                                    "estimate_chrg_time": 1070,
                                                                                    "in_volt_ac": 34292.0,
                                                                                    "in_volt_dc": 35390.96
                                                                                },
                                                                                position_status= {
                                                                                    "longitude_uncertainty":0,
                                                                                    "latitude_uncertainty":0,
                                                                                    "altitude_uncertainty":0,
                                                                                    "posng_valid_type":0,
                                                                                    "longitude":116.458847,
                                                                                    "latitude": 40.01946
                                                                                    # "longitude": 0,
                                                                                    # "latitude": 0
                                                                                })

            time.sleep(3)
            finally_max_soc_in_mysql = checker.mysql.fetch('status_soc',
                                                           {"id": vid
                                                            },
                                                           ['max_soc']
                                                           )[0]['max_soc']
            time.sleep(3)
            assert finally_max_soc_in_mysql == prepare['original_max_soc_in_mysql']






