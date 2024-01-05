# !/usr/bin/python
# coding=utf-8
"""
"""
import os
import string
import time
from pprint import pprint
import random

import pytest
from utils.httptool import request as rq
from config.cert import web_cert

cur_dir = os.path.dirname(os.path.realpath(__file__))

# vid = '4e18c0f0ab734805a802b845a02ad824'
# account_id = '212409581'
# cmdopt = 'test'
#
# mobile='98762667410'
# vc_code='112233'


vid = '4e18c0f0ab734805a802b845a02ad824'
account_id = '212409581'
cmdopt = 'test'

mobile = '98762667410'
vc_code = '112233'

"""
    vehicle_id: 4e18c0f0ab734805a802b845a02ad824
    client_id: "ChDaRLq8_tbIqc0iNNSEKddPEAEY9cUBIJVOKAI="
    vin: SQETEST0514819462
    account_id: 212409581
    phone: 98762667410
"""


def get_mobile_cert(app_id='10001', origin_app_id='10000',cmdopt=cmdopt, account_id=account_id):
    http = {
        "host": f"https://tsp-{cmdopt}-int.nio.com:4430",
        "uri": f"/api/1/sec/in/mobile/user_device_cert",
        "method": "POST",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        "params": {
            'app_id': app_id
        },
        "data": {
            'device_id': '123456',
            'account_id': account_id,
            'origin_app_id': origin_app_id
        }
    }
    res = rq(method=http['method'], url=http['host'] + http['uri'],
             params=http['params'], data=http['data'], headers=http['headers'],
             verify=False, cert=web_cert
             ).json()
    if res['result_code'] == 'success':
        # 目录不存在创建目录
        if not os.path.exists(f'./mobile_cert/{origin_app_id}_{account_id}'):
            os.makedirs(f'./mobile_cert/{origin_app_id}_{account_id}')
        for k, v in res['data'].items():
            with open(f'./mobile_cert/{origin_app_id}_{account_id}/{k}', 'w') as f:
                f.write(v)

        return (f'{cur_dir}/mobile_cert/{origin_app_id}_{account_id}/tls_cert', f'{cur_dir}/mobile_cert/{app_id}_{account_id}/tls_private_key')

    return (None, None)



def test_get_mobile_cert():
    mobile_cert = get_mobile_cert(account_id='992241258',origin_app_id='10000')


def refresh_token(cmdopt=cmdopt,mobile=mobile,vc_code=vc_code,app_id='10001'):
    http = {
        "host": f'https://app-{cmdopt}.nio.com',
        "uri": f"/acc/2/login",
        "method": "POST",
        "headers": {'content-type': 'application/x-www-form-urlencoded',
                    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BLN-AL20 Build/HONORBLN-AL20)/2.9.5-Lifestyle-Android'
                    },
        "params": {
            'region': 'cn',
            'lang': 'zh-cn',
            'app_id': app_id,
            'nonce': 'abcdefefef' + random.choice(string.ascii_letters)
        },
        "data": {
            'mobile': mobile,
            'verification_code': vc_code,
            'country_code': '86',
            'authentication_type': 'mobile_verification_code',
            'device_id': 'adnkjadfnvcnak',
            "terminal": '{"name":"我的华为手机","model":"HUAWEI P10"}',
        }
    }

    res = rq(http['method'], url=http['host'] + http['uri'],
             params=http['params'], data=http['data'], headers=http['headers']).json()
    if res.get('result_code') == 'success':
        token = 'Bearer ' + res['data']['access_token']
        print(f"\n======token======\n{token}")
        return token
    else:
        raise Exception("Failed to refresh access token")
def test_refresh_token():
    cmdopt = 'test'
    mobile = '98762749922'
    vc_code = '112233'
    app_id = '10001'

    token = refresh_token(cmdopt=cmdopt,mobile=mobile,vc_code=vc_code,app_id=app_id)



def test_preset_vehicle_status(publish_msg_by_kafka, mysql):
    """
    该方法为预置车辆初始状态

    """
    vin = mysql['rvs'].fetch('vehicle_profile', {"id": vid}, ['vin'])[0]['vin']

    sample_ts = int(time.time()) * 1000
    # 车辆状态为停车未充电
    publish_msg_by_kafka('charge_end_event', vid=vid, vin=vin,
                         vehicle_status={'vehl_state': 2, 'chrg_state': 3},
                         clear_fields=['soc_status', 'charging_info'],
                         sleep_time=2)
    # 关闭所有车门
    door_status = {
        "charge_port_status": [
            {
                "ajar_status": 1,
                "charge_port_sn": 0
            },
            {
                "ajar_status": 1,
                "charge_port_sn": 1
            }
        ],
        "door_ajars": {
            "door_ajar_frnt_le_sts": 1,
            "door_ajar_frnt_ri_sts": 1,
            "door_ajar_re_le_sts": 1,
            "door_ajar_re_ri_sts": 1
        },
        "door_locks": {
            "access_mode": 30,
            "door_lock_frnt_le_sts": 1,
            "door_lock_frnt_ri_sts": 1,
            "entry_meth": 1,
            "user_id": 2602
        },
        "engine_hood_status": {
            "ajar_status": 1
        },
        "tailgate_status": {
            "ajar_status": 1
        },
        "vehicle_lock_status": 1
    }
    publish_msg_by_kafka('door_change_event', vid=vid, vin=vin, door_status=door_status, sleep_time=2)

    # 关闭所有车窗
    window_status = {
        "sun_roof_positions": {
            "sun_roof_posn": 0,
            "sun_roof_shade_posn": 0,
            "sun_roof_posn_sts": 0
        },
        "window_positions": {
            "win_frnt_le_posn": 0,
            "win_frnt_ri_posn": 0,
            "win_re_le_posn": 0,
            "win_re_ri_posn": 0,
        }
    }
    publish_msg_by_kafka('window_change_event', vid=vid, vin=vin, window_status=window_status, sleep_time=2)

    # 关闭空调
    hvac_status = {
        "air_con_on": 0,
        "amb_temp_c": -26.5,
        "outside_temp_c": 22.0,
        "pm_2p5_cabin": 19,
        "pm_2p5_filter_active": 0,
        "cbn_pre_sts": 0,
        "ccu_cbn_pre_aqs_ena_sts": 0
    }
    publish_msg_by_kafka('hvac_change_event', vid=vid, vin=vin, hvac_status=hvac_status, sleep_time=2)

def test_lock_doors():


    http = {
        "host": f"https://tsp-{cmdopt}-int.nio.com:4430",
        "uri": f"/api/1/vehicle/{vid}/command/lock_doors",
        "method": "POST",
        "headers": {
            "authorization": test_refresh_token(),
            "Content-Type": "application/x-www-form-urlencoded"
        },
        "params": {
            "region": "cn",
            "lang": "zh-cn",
            "app_id": "10001",
            "nonce": 'abcdefefef' + random.choice(string.ascii_letters)
        },
        "data": {
        }
    }
    mobile_cert = get_mobile_cert()
    # mobile_cert = (f"{cur_dir}/mobile_cert/{account_id}_tls_cert", f"{cur_dir}/mobile_cert/{account_id}_tls_private_key")

    response = rq(http['method'], url=http['host'] + http['uri'],
                  params=http['params'], data=http['data'], headers=http['headers'],
                  verify=False, cert=mobile_cert).json()



# def test_get_mobile_cert(device='', account_id='',
#                     env='test', app_id='10001', origin_app_id='10005'):
#     params = {
#         'app_id': app_id
#     }
#     data = {
#         'device_id': device,
#         'account_id': account_id,
#         'origin_app_id': origin_app_id
#     }
#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded',
#     }
#     api = '/api/1/sec/in/mobile/user_device_cert'
#     host = 'https://tsp-{env}-int.nio.com:4430'.format(env=env)
#     res = rq.request('POST', url=host + api, headers=headers, params=params, data=data,
#                     verify=simple.verify_web_test, cert=simple.cert_web_test
#                     )
#     return res


# if __name__ == '__main__':
#
#     res = get_mobile_cert(env='stg',
#         device='1151057182',
#         account_id='1151057182', origin_app_id='10001')
#     pprint(res.json())
#     filecert = res.json()
#     if filecert['result_code'] == 'success':
#         for k, v in filecert['data'].items():
#             with open(k, 'w') as f:
#                 f.write(v)
#
#     # pprint(res.json())
#     # pprint(res.text)
#     # import sys
#     # pprint(sys.path)

