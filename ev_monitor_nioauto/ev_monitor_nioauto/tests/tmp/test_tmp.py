#!/usr/bin/env python
# coding=utf-8
import copy
import csv
import json
import time

from tests.tmp.lat_long import LAT_LONG
from utils.assertions import assert_equal
from utils.coordTransform import wgs84_to_gcj02
from utils.time_parse import utc_strtime_to_timestamp
from utils.httptool import request
# from config.cert import web_cert

class TestTmp(object):
    def test_add_client_id(self, mysql):
        all_data = mysql['quality'].fetch('performance_data', where_model={'id!=': 3})
        for item in all_data:
            c_10005 = mysql['message_test_tsp'].fetch_one('clients', where_model={'device_id': item['vid'], 'app_id': 10005})['client_id']
            c_10107 = mysql['message_test_tsp'].fetch_one('clients', where_model={'device_id': item['vid'], 'app_id': 10107})['client_id']

            mysql['quality'].update('performance_data',
                                    where_model={'vid': item['vid'], 'vin': item['vin']},
                                    fields_with_data={'client_id_10005': c_10005, 'client_id_10107': c_10107})

    def test_mv_data_txt(self, mysql):
        all_data = mysql['quality'].fetch('performance_data', where_model={'id!=': 0}, fields=['vin', 'vid', 'client_id_10005', 'client_id_10107'])
        with open('vehicles_10000.txt', 'w') as f:
            for item in all_data:
                f.write('{},{},{},{}\n'.format(item['vin'], item['vid'], item['client_id_10005'], item['client_id_10107']))

    def test_diff(self):
        aa = {
            "id": "SQETEST0909054497",
            "version": 17,
            "sample_ts": 1567069668302,
            "light_status": {
                "hi_beam_on": 1,
                "lo_beam_on": 2,
                "head_light_on": 3
            }
        }
        bb = {
            "id": "SQETEST0909054497",
            "version": 17,
            "sample_ts": 1567069668302,
            "light_status": {
                "hi_beam_on": 1,
                "lo_beam_on": 2,
                "head_light_on": 4
            }
        }
        aa = '11'
        bb = '11'

        # aa=[11]
        # bb=[22]

        assert_equal(aa, bb)

    def test_add_journey(self, publish_msg_by_kafka):
        vid = '74361e94a61846e2a690d2e2a9bf591d'
        vin = 'SQETEST0796767218'

        start_ts = 1621476000000
        # start_ts = int(time.time()) * 1000
        # end_ts = 1565778510000
        journey_id = '2021052000001'
        journey_update_num = 600

        publish_rate = 10000  # ms

        mileage = 20  # +
        soc = 70  # -
        remaining_range = 70  # -

        # start
        po_s = {"latitude": LAT_LONG[0]['latitude'], "longitude": LAT_LONG[0]['longitude'], "posng_valid_type": 0}
        sample_ts = start_ts
        nextev_message, obj = publish_msg_by_kafka('journey_start_event',
                                                   vid=vid, vin=vin,
                                                   journey_id=journey_id,
                                                   sample_ts=sample_ts,
                                                   position_status=po_s,
                                                   soc_status={"remaining_range": remaining_range, 'soc': soc},
                                                   vehicle_status={"mileage": mileage, "soc": soc},
                                                   sleep_time=0.01
                                                   )

        # update
        for i, item in enumerate(LAT_LONG[1:journey_update_num], start=1):
            tmp = {
                "journey_id": journey_id,
                "sample_points": [
                    {
                        "sample_ts": start_ts + i * publish_rate,
                        "position_status": {
                            "posng_valid_type": 0,
                            "longitude": item['longitude'],
                            "latitude": item['latitude']
                        },
                        "vehicle_status": {"speed": 100, "mileage": mileage + i, "soc": soc - i * 0.01},
                        "soc_status": {"remaining_range": remaining_range - i * 0.01, "soc": soc - i * 0.01},

                    }
                ]
            }
            publish_msg_by_kafka('periodical_journey_update', journey_id=journey_id, sample_points=tmp['sample_points'],
                                 vid=vid, vin=vin, sleep_time=0.01)

        # end
        po_s = {"latitude": LAT_LONG[journey_update_num]['latitude'], "longitude": LAT_LONG[journey_update_num]['longitude'], "posng_valid_type": 0}
        sample_ts = start_ts + journey_update_num * publish_rate
        nextev_message, obj = publish_msg_by_kafka('journey_end_event',
                                                   vid=vid, vin=vin,
                                                   journey_id=journey_id,
                                                   sample_ts=sample_ts,
                                                   position_status=po_s,
                                                   soc_status={"remaining_range": remaining_range - journey_update_num * 0.01, 'soc': soc - journey_update_num * 0.01},
                                                   vehicle_status={"mileage": mileage + journey_update_num, "soc": soc - journey_update_num * 0.01},
                                                   sleep_time=0.01,
                                                   )

    def test_handle_adas_data(self, cassandra,publish_msg_by_kafka):
        """
        获取adas数据
        cqlsh -k adas_data 10.125.235.51 -e "select * from  aeb_edr where vehicle_id='34da4860ce6b4adea4ad56ef26e44647' and sample_ts>1574053170363 and sample_ts<1574669799406 allow filtering;" > output1.txt

        #adas 数据接口
        curl -X POST   http://smart-vehicle-test.nioint.com/trident/v1/in/adas/data/all_edrs -H 'Content-Type: application/x-www-form-urlencoded'   -d 'vid=74361e94a61846e2a690d2e2a9bf591d&start_ts=1574053170363&end_ts=1574073170000'

        """


        # 报一段行程
        vid = '74361e94a61846e2a690d2e2a9bf591d'
        vin = 'SQETEST0796767218'
        utc_time = '2021-05-22 02:00:00.000'
        journey_id = '2021052200001'

        start_ts = utc_strtime_to_timestamp(utc_time)
        journey_update_num = 600

        publish_rate = 10*1000  # ms

        mileage = 20  # +
        soc = 70  # -
        remaining_range = 70  # -

        # start
        po_s = {"latitude": LAT_LONG[0]['latitude'], "longitude": LAT_LONG[0]['longitude'], "posng_valid_type": 0}
        sample_ts = start_ts
        nextev_message, obj = publish_msg_by_kafka('journey_start_event',
                                                   vid=vid, vin=vin,
                                                   journey_id=journey_id,
                                                   sample_ts=sample_ts,
                                                   position_status=po_s,
                                                   soc_status={"remaining_range": remaining_range, 'soc': soc},
                                                   vehicle_status={"mileage": mileage, "soc": soc},
                                                   sleep_time=0.01
                                                   )

        # update
        for i, item in enumerate(LAT_LONG[1:journey_update_num], start=1):
            tmp = {
                "journey_id": journey_id,
                "sample_points": [
                    {
                        "sample_ts": start_ts + i * publish_rate,
                        "position_status": {
                            "posng_valid_type": 0,
                            "longitude": item['longitude'],
                            "latitude": item['latitude']
                        },
                        "vehicle_status": {"speed": 100, "mileage": mileage + i, "soc": soc - i * 0.01},
                        "soc_status": {"remaining_range": remaining_range - i * 0.01, "soc": soc - i * 0.01},

                    }
                ]
            }
            publish_msg_by_kafka('periodical_journey_update', journey_id=journey_id, sample_points=tmp['sample_points'],
                                 vid=vid, vin=vin, sleep_time=0.01)

        # end
        po_s = {"latitude": LAT_LONG[journey_update_num]['latitude'], "longitude": LAT_LONG[journey_update_num]['longitude'], "posng_valid_type": 0}
        sample_ts = start_ts + journey_update_num * publish_rate
        nextev_message, obj = publish_msg_by_kafka('journey_end_event',
                                                   vid=vid, vin=vin,
                                                   journey_id=journey_id,
                                                   sample_ts=sample_ts,
                                                   position_status=po_s,
                                                   soc_status={"remaining_range": remaining_range - journey_update_num * 0.01, 'soc': soc - journey_update_num * 0.01},
                                                   vehicle_status={"mileage": mileage + journey_update_num, "soc": soc - journey_update_num * 0.01},
                                                   sleep_time=0.01,
                                                   )





        #上报adas数据 adas数据时间段位于上报的行程数据内

        # Get the all the lines in file in a list
        header = None
        count = 0
        start_num = 4
        final_num = 40000 #实际可能没这么多数据。此处给个大数表示所有数据一定都能读到
        # final_num = 20
        with open("/Users/li.liu2/workspace/ev_monitor_nioauto/data/adas_output1.txt", "r") as f:
            for line in f:
                count += 1
                # listOfLines.append(line.strip())
                value = [x.strip() for x in line.split('|')]

                if count == 2:
                    header = value
                elif count >= start_num and count <= final_num:
                    d = dict(zip(header, value))

                    # delete null key
                    dd = copy.deepcopy(d)
                    for k in d:
                        if d[k] == 'null':
                            del dd[k]
                    # edit values
                    dd['vehicle_id'] = vid

                    try:
                        # 此处处理adas output的samle_ts和update_ts
                        # 第一条 samle_ts=1574053176163000  update_ts=2019-11-18 06:41:57.774000+0000
                        dd['sample_ts'] = int(dd['sample_ts'])//1000 + (start_ts-1574053176163)+10*60*1000
                        dd['update_ts'] = dd['sample_ts']


                        if 'acc_inhibition_data' in dd:
                            dd['acc_inhibition_faults'] = "[{field: 'e_accsc_uactprev_mp', bits: [0,1,2,3,4,5]}]"
                            dd.pop('acc_inhibition_fault', '')
                        if 'pilot_inhibition_data' in dd:
                            dd['pilot_inhibition_faults'] = "[{field: 'e_accsc_uactprev_mp', bits: [0,1,2,3,4,5]}]"
                            dd.pop('pilot_inhibition_fault', '')

                        dd['alc_inhibition_faults'] = "[{field: 'e_accsc_uactprev_mp', bits: [0,1,2,3,4,5]}]"
                        dd.pop('alc_inhibition_fault', '')

                    except Exception as e:
                        print(f'Exception: {e}')
                        continue

                    result = cassandra['adas'].insert('aeb_edr', model=dd)

                elif count > final_num:
                    break



    def test_qc_env(self, env, publish_msg):
        nextev_message, charge_port_obj = publish_msg('charge_port_event')

    def test_ntest(self, publish_msg_by_kafka):
        nextev_message, charge_port_obj = publish_msg_by_kafka('charge_start_event', vehicle_status={
            'ntester': 1
        })

    def test_navigator(self):
        # test
        # vid = 'eb84d28cb0924cf6b8bf7d0c5cb36542'
        # account_id = 589874282
        # navigation_report(env['host']['tsp'], vid, account_id)

        # stg
        # # es8
        # vid = '25613b71b0d14a258d743c94f14f8039'
        # account_id = 718218691
        # self.navigation_report('https://tsp-stg.nio.com', vid, account_id)

        # # es6
        # vid = 'e699260be9034542adbeb483fa2f486e'
        # account_id = 555116995
        # self.navigation_report('https://tsp-stg.nio.com', vid, account_id)

        # test
        vid = '77c817f946014690b126a6d70be0f858'
        vid = '4e18c0f0ab734805a802b845a02ad824'
        account_id = 540059404
        account_id = 212409581
        api = '/api/1/data/report'

        # event = json.dumps([{"longitude": "131.996161",
        #                      "app_ver": "1.0.82.01",
        #                      "city": "武汉市",
        #                      "area_code": "131081",
        #                      "app_id": "30009",
        #                      "nation": "中国",
        #                      "district": "青山区",
        #                      "event_type": "nav_period",
        #                      "latitude": "30.63136",
        #                      "timestamp": int(time.time() * 1000),
        #                      "province": "湖北省",
        #                      "roadName": "旅大街"}])
        # data = {
        #     'model': 'ES8',
        #     'os': 'android',
        #     'os_ver': '1.0.0',
        #     'os_lang': 'unknown',
        #     'os_timezone': 'unknown',
        #     'client_timestamp': str(int(time.time() - 8 * 3600)),
        #     'network': 'unknwon',
        #     'user_id': uid,
        #     'vid': vid,
        #     'events': event
        #
        # }
        event = json.dumps([{"longitude": "121.230858",
                             "app_ver": "1.0.82.01",
                             "city": "上海市",
                             "area_code": "310104",
                             "app_id": "30009",
                             "nation": "中国",
                             "district": "闵行区",
                             "event_type": "nav_period",
                             "latitude": "31.316501",
                             "timestamp": int(time.time() * 1000),
                             "province": "上海市",
                             "roadName": "合川路"}])
        data = {
            'model': 'ES8',
            'os': 'android',
            'os_ver': '1.0.0',
            'os_lang': 'unknown',
            'os_timezone': 'unknown',
            'client_timestamp': str(int(time.time() - 8 * 3600)),
            'network': 'unknwon',
            'user_id': account_id,
            'vid': vid,
            'events': event

        }

        res = request('POST', url='https://tsp-test.nio.com' + api, data=data)
        return res


    def test_qc(self, publish_msg):
        nextev_message, obj = publish_msg('charge_start_event')
        # nextev_message, obj = publish_msg('periodical_charge_update')
        # nextev_message, obj = publish_msg('charge_end_event')
        #
        #
        # nextev_message, obj = publish_msg('journey_start_event')
        # nextev_message, obj = publish_msg('periodical_journey_update')
        # nextev_message, obj = publish_msg('journey_end_event')

        # nextev_message, obj = publish_msg('light_change_event')
        # nextev_message, window_change_event_obj = publish_msg('window_change_event')
        # nextev_message, hvac_change_obj = publish_msg('hvac_change_event')
        #
        # nextev_message, door_status_obj = publish_msg('door_change_event')

    def navigation_report(self, host, vid, uid, chg=False):
        api = '/api/1/data/report'

        # event = json.dumps([{"longitude": "131.996161",
        #                      "app_ver": "1.0.82.01",
        #                      "city": "武汉市",
        #                      "area_code": "131081",
        #                      "app_id": "30009",
        #                      "nation": "中国",
        #                      "district": "青山区",
        #                      "event_type": "nav_period",
        #                      "latitude": "30.63136",
        #                      "timestamp": int(time.time() * 1000),
        #                      "province": "湖北省",
        #                      "roadName": "旅大街"}])
        # data = {
        #     'model': 'ES8',
        #     'os': 'android',
        #     'os_ver': '1.0.0',
        #     'os_lang': 'unknown',
        #     'os_timezone': 'unknown',
        #     'client_timestamp': str(int(time.time() - 8 * 3600)),
        #     'network': 'unknwon',
        #     'user_id': uid,
        #     'vid': vid,
        #     'events': event
        #
        # }

        event = json.dumps([{"longitude": "109.601166",
                             "app_ver": "1.0.82.01",
                             "city": "武汉市",
                             "area_code": "131081",
                             "app_id": "30009",
                             "nation": "中国",
                             "district": "青山区",
                             "event_type": "nav_period",
                             "latitude": "18.184050",
                             "timestamp": int(time.time() * 1000),
                             "province": "湖北省",
                             "roadName": "旅大街"}])
        data = {
            'model': 'ES6',
            'os': 'android',
            'os_ver': '1.0.0',
            'os_lang': 'unknown',
            'os_timezone': 'unknown',
            'client_timestamp': str(int(time.time() - 8 * 3600)),
            'network': 'unknwon',
            'user_id': uid,
            'vid': vid,
            'events': event

        }

        res = request('POST', url=host + api, data=data)
        return res

    def test_graphql(self):

        url = "https://tsp-test.nioint.com/api/1/in/battery/graphql"
        query = """
        {vehicles(page:1,page_size:100, vin: "", vehicle_id: "", status: -1){list {
      vin
      create_time
      update_time
      status
      account_id
      vehicle_id
      license_plate
      veh_model_name
      vehicle_type
      offline_production_time
      sale_time
      sale_area
      owner_name
      epname
      epaddress
      idnum
      epcode
      vehicle_brand
      code
      veh_type_name
      vehicle_name
    },
    page
    page_size
    total}}
        
        """

        querystring = {'app_id': '100078', 'query': '{vehicles(page:1,page_size:100, vin: "", vehicle_id: "", status: -1){list {vin}}}'}
        # querystring = {'app_id': 100078, 'query': query}
        #
        # headers = {
        #     'Accept': "*/*",
        #     'Host': "tsp-test.nioint.com",
        #     'Accept-Encoding': "gzip, deflate",
        #     'Connection': "keep-alive",
        # }

        response = request("GET", url, params=querystring)

        print(response.text)

    def test_graphql_o(self):

        # url = "https://tsp-test.nioint.com/api/1/in/battery/graphql"
        url = "https://tsp-test.nioint.com/api/1/in/battery/graphql"


        querystring = {
            'app_id': '100078',
        }
        data = json.dumps({"query": """{ vehicles(page:1,page_size:10, vin: "", vehicle_id: "", status:3) { list {vin}, page page_size  total }}"""})
        # data = "{\"query\":\"{ vehicles(page:1,page_size:10, vin: \\\"\\\", vehicle_id: \\\"\\\", status:3) { list {vin}, page page_size  total }} \"}"
        headers = {'Content-Type': 'application/json'}
        response = request("POST", url=url,  params=querystring, data=data,headers=headers)
        # response = request("POST", url, data=data)

        print(response.text)

    def test_ooo(self):
        import requests

        url = "https://tsp-test.nioint.com/api/1/in/battery/graphql?sign=5ab5783408025ac58309549c401d8b6d&app_id=100078&timestamp=1587643136&"

        payload = "{\"query\":\"{ vehicles(page:1,page_size:10, vin: \\\"\\\", vehicle_id: \\\"\\\", status:3) { list {vin}, page page_size  total }} \"}"
        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text.encode('utf8'))

    def test_message_api_notify(self):
        url = "https://tsp-test-int.nio.com/api/1/in/message/notify"

        params = {'app_id': '10013', 'region': 'cn', 'lang': 'zh-cn'}

        data = {'nonce': 'MrVIRwkCLBKySgCG',
                'async': False,
                'scenario': 'fs_system',
                'client_ids': 'ChDaRLq8_tbIqc0iNNSEKddPEAEY9cUBIJVOKAI=',
                'ttl': 1000,
                'target_app_ids': 10001,
                'payload': json.dumps({"target_link": "http://www.niohome.com", "description": "test description", "title": "test title"})
                }

        response = request("POST", url, params=params, data=data).json()

        print(response)

    def test_message_api_command(self):
        url = "https://tsp-test-int.nio.com/api/1/in/message/command"
        params = {'app_id': '10005'}

        data = {'nonce': 'nondceafadfdasfadfa',
                'scenario': 'rvs_set_doorlock',
                'device_ids': '4e18c0f0ab734805a802b845a02ad824',
                # client_id是 ChDaRLq8_tbIqc0iNNSEKddPEAEY9cUBIJVOKAI=
                'ttl': 10000,
                'target_app_id': 10005,
                # command_id 需要是一个vehicle control 产生的comamnd_id
                # doorlock 1 关，2 开，  对应status_door表vehicle_lock_status 1 全关，0 开
                'payload': json.dumps({"command_id": 90390704, "doorlock": 2, "max_duration": "20"})

                # 'device_ids': '43701c7ac3004cd68d3549451f42e424',
                # client_id是 "ChA-D55KfVWzGCb6CjoxXLGlEAEY9RgglU4oAg=="
                # 'payload': json.dumps({"command_id": 90389231, "doorlock": 1, "max_duration": "20"})

                }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = request("POST", url, params=params, data=data, headers=headers).json()

        print(response)

    def test_message_api_register_client(self):
        url = "https://tsp-test-int.nio.com/api/1/message/register_client"
        params = {'app_id': '10005', 'region': 'cn', 'lang': 'zh_cn'}
        data = {
            'app_version': '1.3.4',
            'brand': 'xiaomi',
            'device_type': 'vehicle',
            'device_token': '',
            'device_id': '4e18c0f0ab734805a802b845a02ad824',
            'os': 'android',
            'os_version': '6.0',
            'nonce': 'nondceafadfdasfadfa'
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = request("POST", url, params=params, data=data, headers=headers).json()

        print(response)

    def test_move_forward(self):
        http = {
            "host": "https://tsp-stg-int.nio.com:4430",
            "uri": "/api/1/vehicle/85563dd863a54c929e8458280e9a3dda/command/nbs/move_forward",
            "method": "POST",
            "headers": {
                "authorization": "Bearer 2.0G9H6UMQZhlfCm2r4+sj/HM2t4zXo0JQ+vRE2pAAflcE=",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "params": {
                "app_id": "10005"
            },
        }
        web_cert=('/Users/li.liu2/workspace/ev_monitor_nioauto/config/cert/web_tsp-test-int/web_tsp-test-int.cert', '/Users/li.liu2/workspace/ev_monitor_nioauto/config/cert/web_tsp-test-int/web_tsp-test-int.key')
        response = request(http['method'], url=http['host'] + http['uri'], params=http['params'], headers=http['headers'], cert=web_cert,verify=False).json()


    def test_wgs84_to_gcj02(self):

        gcj02_coord = wgs84_to_gcj02(77.186910, 38.889753)
        print(gcj02_coord)