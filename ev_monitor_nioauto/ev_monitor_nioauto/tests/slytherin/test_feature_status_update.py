#!/usr/bin/env python
# coding=utf-8

"""
:Description: Adas feature_status_update事件上报

feature_status_update的上报机制是状态变化则立即上报，状态不变时隔30s上报一次

新增proto版本升到18以后，用trip事件来替代journey事件后，adas上报的case
"""
import json
import time
import random

import allure
from datetime import datetime

import pytest

from data.lat_long import LAT_LONG
from utils.assertions import assert_equal


class TestFeatureStatusUpdate(object):
    @pytest.mark.skip
    # https://nio.feishu.cn/docs/doccnrcIme501Hh9VfpoO0ZN94c 2021.10.09优化后不再更新
    def test_status_adas(self, vid, checker, publish_msg_by_kafka_adas):
        """
        是否落库到mysql的status_adas表主要看
        1.feature_ts，只有大于等于数据库里的feature_ts才落库
        2. np_status（值为0,1,2，详见下面解释）, 只有np_status改变才会落库
            np_status   SYSTEM_OFF=0, ACC_ACTIVE=1, PILOT_ACTIVE=2
            acc_np_sts：ACC_SYSTEM_OFF=0;SYSTEM_PASSIVE=1;SYSTEM_READY=2;ACC_ACTIVE=3;ACC_STANDBY=4;PILOT_ACTIVE=5;LATERAL_UNAVAILABLE=6;PILOT_STANDBY=7;
            np_status与acc_np_sts关系如右：0=0,1,2,4,7  1=3  2=5,6
        3. nop_satus对应nop_sts
            nop_status SYSTEM_OFF=0, NOP_ACTIVE=1
            nop_sts(0-7) NOP_OFF=0;NOP_STANDBY=1;NOP_READY=2;NOP_ACTIVE=3;NOP_PASSIVE=4;NOP_STS_RESERVED0=5;NOP_STS_RESERVED1=6;NOP_STS_RESERVED2=7;
            nop_status与nop_sts关系如右：0=0,1,2,4,5,6,7  1=3

        AdasHeader.timestamp落到库中是sample_time，FeatureStatus.timestamp落库到库中是feature_time
        这里注意，feature_status_update事件有三个ts,除了上面的2个，FeatureStatus外层还有个timestamp，但是tsp完全没有处理它

        在redis中加入缓冲，当数据有变化时会同步更新redis和mysql，读取数据是先度redis，后读mysql。没有ttl
        加缓冲主要是为了以后需要时可控制mysql的写入频率，防止mysql负担太重
        key: get remote_vehicle_test:adas_status:{vehicle_id}
        """
        np_status_map = ((0, 1, 2, 4, 7), (3,), (5, 6))
        nop_status_map = ((0, 1, 2, 4, 5, 6, 7), (3,))

        origin_np = checker.mysql.fetch('status_adas', {"id": vid}, exclude_fields=['update_time'])[0]

        ts = int(time.time()) * 1000
        nextev_message, obj = publish_msg_by_kafka_adas('feature_status_update', protobuf_v=18,
                                                        adas_header_data={'timestamp': ts},
                                                        feature_status_data={'timestamp': ts // 1000},
                                                        sample_ts=ts, sleep_time=30)

        # 校验
        # 只有np_status或acc_np_sts改变才会落库
        # np_status没变
        if (obj['FeatureStatusUpdate']['feature_status']['acc_np_sts'] in np_status_map[origin_np['np_status']]
                and obj['FeatureStatusUpdate']['feature_status']['nop_sts'] in nop_status_map[origin_np['nop_status']]):
            new_np = checker.mysql.fetch('status_adas', {"id": vid}, exclude_fields=['update_time'])[0]
            assert_equal(new_np, origin_np)
        # np_status变化
        else:
            tables = ['status_adas']
            checker.check_mysql_tables(obj, tables, event_name='feature_status_update', sample_ts=obj['AdasHeader']['timestamp'])

    @pytest.mark.parametrize('tag, ver', [('vehicle_history_1', 17), ('vehicle_history_2', 18)])
    def test_np(self, env, mysql, publish_msg_by_kafka, publish_msg_by_kafka_adas, tag, ver):
        """
        当行程数据里有np的feature_status_update事件事件上报时，会在redis里记录每一次np_status变化情况，
        当行程结束时，将redis中的np数据整理后落库到mysql的history_adas_journey表，并清空redis数据。
        np数据可以比行程的start事件采样时间早<=5秒。
        灾备环境目前不消费np事件。

        np数据每30s就会有一次上报（车端没有开关，所以只要车在就会报np数据上来）
        AdasHeader.timestamp 反映的是事件的采样时间，即30s间隔。单位是毫秒
        feature_status_update.FeatureStatusUpdate.timestamp反映的是acc_np_sts发生变化的事件。注意单位是秒
        feature_status_update.timestamp这个时间没有用处

        例如：行程过程中有一段np数据，np1-np4每30s（AdasHeader.ts）报一次。
            np1和np2的feature_status.ts一样，np3和np4的feature_status.ts一样。因为它们的状态都没变
        上报start，np事件具体如下：
            event   ts/AdasHeader.ts       mileage/np_mileage          feature_status.ts  acc_np_sts
            obj_sta 1582098493000               2953
            obj_np1 1582098523000               2954                    1582098523          3
            obj_np2 1582098553000               2955                    1582098523          3
            obj_np3 1582098583000               2956                    1582098583          5
            obj_np4 1582098613000               2957                    1582098583          5

        Redis记录：
            hgetall remote_vehicle_test:adas_journey:4e18c0f0ab734805a802b845a02ad824:202002190748130001
            1) "1582098583000"
            2) "{\"acc_np_sts\":2,\"mileage\":2956,\"feature_time\":1582098583000,\"sample_time\":1582098583000}"
            3) "1582098523000"
            4) "{\"acc_np_sts\":1,\"mileage\":2954,\"feature_time\":1582098523000,\"sample_time\":1582098523000}"

            此时没报end事件前，redis里会记录np1和np3两个np数据，因为这两数据是np状态是最早发送变化的数据
            redis key:remote_vehicle_test:adas_journey:vid:process_id

            注意：redis里记录的时np数据最早发生变化的点,会过滤不符合条件的数据例如：
            1. np_mileage小于journey_start的数据不记录
            2. reids里的acc_np_sts其实是np_status
                np_status（0-2）   SYSTEM_OFF=0, ACC_ACTIVE=1, PILOT_ACTIVE=2
                acc_np_sts（0-7）  ACC_SYSTEM_OFF=0;SYSTEM_PASSIVE=1;SYSTEM_READY=2;ACC_ACTIVE=3;ACC_STANDBY=4;PILOT_ACTIVE=5;LATERAL_UNAVAILABLE=6;PILOT_STANDBY=7;
                np_status与acc_np_sts关系如右：0=0,1,2,4,7  1=3  2=5,6
            3.不同header_ts但相同feature_ts时，记录最小header_ts的np点
            4. 不同的feature_ts且不同header_ts时，会根据np_status(0,1,2)记录最早的feature_ts的那条 例如：
                event   ts/AdasHeader.ts    mileage/np_mileage      feature_status.ts       acc_np_sts
                obj_sta 1581410605000       2696
                obj_np1 1581410605020       2696                    1581410605020           5
                obj_np2 1581410605030       2706                    1581410605010           3
                obj_np3 1581410605040       2716                    1581410605040           5
                obj_end 1581410615000       2726
                记录的是np1， np2，np3在np_status=2中feature_status.ts排在了np1之后，所以没有记录进redis中。

        上报end事件具体如下：
            obj_end 1582098643000  2962

        mysql记录：
            history_adas_journey表
            journey_id	        process_id	        np_mileage	np_duration	np_status_list
	        202002190748130001	202002190748130001	8	        120	        {"1582098523000":1,"1582098583000":2,"1582098643000":0}

            1. 当journey_end数据上报时，redis的记录会清除，数据会写到mysql的history_adas_journey表中。
            2. mysql里会把redis里的np数据按照时间顺序记录下来。并看最后一条的np_status是不是0(状态结束点),如果不是的话，
                补一条np点（np_status=0,np_ts=journey_end_event.ts）到np_status_list中。
            3. np_duration单位是秒
            4. 会过滤调np_list为空或者np_list所有点的np_status=0的记录
            5. 未结束行程不会落库到history_adas_journey表里

        API：
            1.旅程detail api: /api/1/vehicle/{vehicle_id}/journey/{journey_id}
                http://showdoc.nevint.com/index.php?s=/11&page_id=2428
                涉及np_mileage,np_duration,np_status三个字段

                np_duration取history_adas_journey里的np_duration计算。
                注意：1）api里返回的duration单位为分钟。且向下取整（2.9取2）
                     2）根据journey_id做group可能返回history_adas_journey表的多条数据
                     3）未结束的行程也会计算。此时history_adas_journey表里没有记录。
                        ！！但是接口能正常返回数据，因为会利用redis数据，伪造一个行程结束，计算一遍数值返回。
                     4）track里的点是start和update事件的值，来自于journey/track接口 /api/1/in/data/vehicle/{vehicle_id}/journey/track
                     5）track里的np_status的取值如下：
                        想象np点根据feature_ts连成线段，track的行程点根据ts散落在线段上,
                        track数据的np_status是离它左边最近的np点状态值,如果它左边没有np点，则默认为0
                     6) track数据只有start和update的点，没有end的。
                     7) 在app上不会显示np点，只会根据np点的范围去设置track点的状态
            2.旅程月报api: /api/1/vehicle/{vehicle_id}/month_detail：
                http://showdoc.nevint.com/index.php?s=/11&page_id=20289
                涉及np_mileage,np_duration两个字段

                np_mileage,np_duration的取值来自与统计数据库的vehicle_stat_monthly表

                vehicle_stat_monthly表取值来自vehicle_stat_daily表的当月累加
                vehicle_stat_daily表取值来自history_adas_journey表。跨天不做截断。未结束行程不统计

                最终返回的np_mileage会和月报表的mileage做一个比较，返回较小的哪个。
            3.np版本api: /api/1/vehicle/config/get_config
                http://showdoc.nevint.com/index.php?s=/11&page_id=22005
                涉及np_type字段

                np_type取值来自vehicle_profile的material_num的第17位。
                np_type值 0表示未购买，2表示基础包，1表示完整包，默认值0

        """
        vid = env['vehicles'][tag]['vehicle_id']
        vin = env['vehicles'][tag]['vin']
        with allure.step("校验adas np数据能正常落库到history_adas_journey表"):
            # vid = '140a70c2efc74d9c8706ece46c66291c'
            # vin = 'LJ1E6A3U9K7716734'
            start_ts = int(time.time()) * 1000
            if ver == 17:
                journey_id = datetime.utcfromtimestamp(int(start_ts) / 1000.0).strftime('%Y%m%d%H%M%S') + '0001'
            else:
                journey_id = str(start_ts//1000)
                journey_id0 = datetime.utcfromtimestamp(int(start_ts) / 1000.0).strftime('%Y%m%d%H%M%S') + '0001'

            journey_update_num = 5  # update事件上报的数量 不能超过800条
            publish_rate = 30000  # ms 事件上报频率 30s

            soc = 98  # -
            dump_enrgy = 70  # -
            remaining_range = 500  # -

            mileage = mysql['rvs'].fetch('status_vehicle', {"id": vid}, ['mileage'])[0]['mileage']

            # start
            po_s = {"latitude": LAT_LONG[0]['latitude'], "longitude": LAT_LONG[0]['longitude'], "posng_valid_type": 0}
            if ver == 17:
                nextev_message, obj_start = publish_msg_by_kafka('journey_start_event',
                                                                 vid=vid, vin=vin,
                                                                 journey_id=journey_id,
                                                                 sample_ts=start_ts,
                                                                 position_status=po_s,
                                                                 soc_status={"remaining_range": remaining_range, 'soc': soc, 'dump_enrgy': dump_enrgy},
                                                                 vehicle_status={"mileage": mileage, "soc": soc},
                                                                 sleep_time=0.5
                                                                 )
            else:
                nextev_message, obj_start = publish_msg_by_kafka('trip_start_event', protobuf_v=18,
                                                                 vid=vid, vin=vin,
                                                                 sample_ts=start_ts,
                                                                 position_status=po_s,
                                                                 soc_status={"remaining_range": remaining_range, 'soc': soc, 'dump_enrgy': dump_enrgy},
                                                                 vehicle_status={"mileage": mileage, "soc": soc},
                                                                 trip_status={'trip_id': journey_id},
                                                                 sleep_time=0.5
                                                                 )
                publish_msg_by_kafka('journey_start_event', protobuf_v=18,
                                     vid=vid, vin=vin,
                                     journey_id=journey_id0,
                                     sample_ts=start_ts,
                                     position_status=po_s,
                                     soc_status={"remaining_range": remaining_range, 'soc': soc, 'dump_enrgy': dump_enrgy},
                                     vehicle_status={"mileage": mileage, "soc": soc},
                                     sleep_time=0.5
                                     )

            obj_np_list = []
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
                            "vehicle_status": {"speed": 100, "mileage": mileage + i, "soc": soc - i},
                            "soc_status": {"remaining_range": remaining_range - i,
                                           "soc": soc - i,
                                           "dump_enrgy": dump_enrgy - i},

                        }
                    ]
                }
                publish_msg_by_kafka('periodical_journey_update', protobuf_v=ver, journey_id=journey_id, sample_points=tmp['sample_points'],
                                     vid=vid, vin=vin, sleep_time=0.5)

                nextev_message, obj_np = publish_msg_by_kafka_adas('feature_status_update', protobuf_v=ver,
                                                                   adas_header_data={
                                                                       'timestamp': start_ts + i * publish_rate,
                                                                       'mileage': mileage + i
                                                                   },
                                                                   feature_status_data={'timestamp': (start_ts + (1 if i < 3 else 3) * publish_rate) // 1000,
                                                                                        'acc_np_sts': 3 if i < 3 else 5
                                                                                        },
                                                                   sample_ts=start_ts + i * publish_rate,
                                                                   vid=vid, vin=vin,
                                                                   )

                obj_np_list.append(obj_np)

            # end
            po_s = {"latitude": LAT_LONG[journey_update_num]['latitude'], "longitude": LAT_LONG[journey_update_num]['longitude'], "posng_valid_type": 0}
            if ver == 17:
                nextev_message, obj_end = publish_msg_by_kafka('journey_end_event',
                                                               vid=vid, vin=vin,
                                                               journey_id=journey_id,
                                                               sample_ts=start_ts + journey_update_num * publish_rate,
                                                               position_status=po_s,
                                                               soc_status={"remaining_range": remaining_range - journey_update_num,
                                                                           'soc': soc - journey_update_num,
                                                                           'dump_enrgy': dump_enrgy - journey_update_num},
                                                               vehicle_status={"mileage": mileage + journey_update_num, "soc": soc - journey_update_num},
                                                               )
            else:
                nextev_message, obj_end = publish_msg_by_kafka('trip_end_event', protobuf_v=18,
                                                               vid=vid, vin=vin,
                                                               sample_ts=start_ts + journey_update_num * publish_rate,
                                                               position_status=po_s,
                                                               soc_status={"remaining_range": remaining_range - journey_update_num,
                                                                           'soc': soc - journey_update_num,
                                                                           'dump_enrgy': dump_enrgy - journey_update_num},
                                                               vehicle_status={"mileage": mileage + journey_update_num, "soc": soc - journey_update_num},
                                                               trip_status={'trip_id': journey_id}
                                                               )
                publish_msg_by_kafka('journey_end_event', protobuf_v=18,
                                     vid=vid, vin=vin,
                                     journey_id=journey_id0,
                                     sample_ts=start_ts + journey_update_num * publish_rate,
                                     position_status=po_s,
                                     soc_status={"remaining_range": remaining_range - journey_update_num,
                                                 'soc': soc - journey_update_num,
                                                 'dump_enrgy': dump_enrgy - journey_update_num},
                                     vehicle_status={"mileage": mileage + journey_update_num, "soc": soc - journey_update_num},
                                     )
            # print for debug
            print("******")
            print(f'vid {vid}')
            print(f'obj_sta {obj_start["sample_ts"]}  {obj_start["vehicle_status"]["mileage"]}')
            for i in range(len(obj_np_list)):
                print(
                    f'obj_np{i} {obj_np_list[i]["AdasHeader"]["timestamp"]} \
                                {obj_np_list[i]["AdasHeader"]["mileage"]} \
                                {obj_np_list[i]["FeatureStatusUpdate"]["feature_status"]["timestamp"]}  \
                                {obj_np_list[i]["FeatureStatusUpdate"]["feature_status"]["acc_np_sts"]}')
            print(f'obj_end {obj_end["sample_ts"]}  {obj_end["vehicle_status"]["mileage"]}')

            history_adas_mysql = mysql['rvs'].fetch('history_adas_journey', where_model={'process_id': journey_id, 'vehicle_id': vid})[0]
            print(f'np_mileage:{history_adas_mysql["np_mileage"]} np_duration:{history_adas_mysql["np_duration"]} np_list:{history_adas_mysql["np_status_list"]}')

            # check
            status_map = {0: 0, 1: 0, 2: 0, 3: 1, 4: 0, 5: 2, 6: 2, 7: 0}
            np_ts_list = [obj_np_list[0]["FeatureStatusUpdate"]["feature_status"]["timestamp"]]
            np_status_list = [status_map[obj_np_list[0]["FeatureStatusUpdate"]["feature_status"]["acc_np_sts"]]]
            np_mileage_list = [obj_np_list[0]["AdasHeader"]["mileage"]]
            np_duration = 0
            np_mileage = 0
            for i, item in enumerate(obj_np_list, start=1):
                ts = item["FeatureStatusUpdate"]["feature_status"]["timestamp"]
                status = status_map[item["FeatureStatusUpdate"]["feature_status"]["acc_np_sts"]]
                mileage = item["AdasHeader"]["mileage"]
                if status != np_status_list[-1]:
                    np_ts_list.append(ts)
                    np_status_list.append(status)
                    np_mileage_list.append(mileage)
                    np_duration += np_ts_list[-1] - np_ts_list[-2]
                    np_mileage += np_mileage_list[-1] - np_mileage_list[-2]

            # 判断最后的一个status是不是0，不是0的话，把journey_end的值也加入到np list中
            if np_status_list[-1] != 0:
                np_ts_list.append(obj_end["sample_ts"] // 1000)
                np_status_list.append(0)
                np_mileage_list.append(obj_end["vehicle_status"]["mileage"])
                np_duration += np_ts_list[-1] - np_ts_list[-2]
                np_mileage += np_mileage_list[-1] - np_mileage_list[-2]

            assert_equal(history_adas_mysql['np_duration'], np_duration)
            assert_equal(history_adas_mysql['np_mileage'], np_mileage)

            np_status_dict = {str(np_ts_list[i] * 1000): np_status_list[i] for i in range(len(np_ts_list))}
            assert_equal(json.loads(history_adas_mysql['np_status_list']), np_status_dict)

    @pytest.mark.parametrize('tag, ver', [('vehicle_history_1', 17), ('vehicle_history_2', 18)])
    def test_sapa_status(self, env, mysql, publish_msg_by_kafka, publish_msg_by_kafka_adas, tag, ver):
        """
        sapa_status标记的是自动泊车状态。值的取值范围为0-15。具体含义看见proto定义。从任何状态切到6(PARKING_FINISHED)即算为一次泊车结束 sapa_count+1

        同样当行程数据里有np的feature_status_update事件事件上报时，会在redis里记录每一次np_status变化情况，
        当行程结束时，将redis中的np数据整理后落库到mysql的history_adas_journey表，并清空redis数据。

        """
        vid = env['vehicles'][tag]['vehicle_id']
        vin = env['vehicles'][tag]['vin']
        with allure.step("校验adas 泊车数据acc_np_sts能正常落库到history_adas_journey表"):
            # vid = '857bdcec079845cf9e64e328a7b2c282'
            # vin = 'SQETEST0387987190'
            start_ts = int(time.time()) * 1000
            if ver == 17:
                journey_id = datetime.utcfromtimestamp(int(start_ts) / 1000.0).strftime('%Y%m%d%H%M%S') + '0001'
            else:
                journey_id = str(start_ts // 1000)
                journey_id0 = datetime.utcfromtimestamp(int(start_ts) / 1000.0).strftime('%Y%m%d%H%M%S') + '0001'

            journey_update_num = 5  # update事件上报的数量 不能超过800条
            publish_rate = 30000  # ms 事件上报频率 30s

            soc = 98  # -
            dump_enrgy = 70  # -
            remaining_range = 500  # -

            mileage = mysql['rvs'].fetch('status_vehicle', {"id": vid}, ['mileage'])[0]['mileage']

            # start
            po_s = {"latitude": LAT_LONG[0]['latitude'], "longitude": LAT_LONG[0]['longitude'], "posng_valid_type": 0}
            if ver == 17:
                nextev_message, obj_start = publish_msg_by_kafka('journey_start_event',
                                                                 vid=vid, vin=vin,
                                                                 journey_id=journey_id,
                                                                 sample_ts=start_ts,
                                                                 position_status=po_s,
                                                                 soc_status={"remaining_range": remaining_range, 'soc': soc, 'dump_enrgy': dump_enrgy},
                                                                 vehicle_status={"mileage": mileage, "soc": soc},
                                                                 sleep_time=0.5
                                                                 )
            else:
                nextev_message, obj_start = publish_msg_by_kafka('trip_start_event', protobuf_v=ver,
                                                                 vid=vid, vin=vin,
                                                                 sample_ts=start_ts,
                                                                 position_status=po_s,
                                                                 soc_status={"remaining_range": remaining_range, 'soc': soc, 'dump_enrgy': dump_enrgy},
                                                                 vehicle_status={"mileage": mileage, "soc": soc},
                                                                 trip_status={'trip_id': journey_id},
                                                                 sleep_time=0.5
                                                                 )
                publish_msg_by_kafka('journey_start_event', protobuf_v=ver,
                                     vid=vid, vin=vin,
                                     journey_id=journey_id0,
                                     sample_ts=start_ts,
                                     position_status=po_s,
                                     soc_status={"remaining_range": remaining_range, 'soc': soc, 'dump_enrgy': dump_enrgy},
                                     vehicle_status={"mileage": mileage, "soc": soc},
                                     sleep_time=0.5
                                     )
            obj_np_list = []
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
                            "vehicle_status": {"speed": 100, "mileage": mileage + i, "soc": soc - i},
                            "soc_status": {"remaining_range": remaining_range - i,
                                           "soc": soc - i,
                                           "dump_enrgy": dump_enrgy - i},

                        }
                    ]
                }
                publish_msg_by_kafka('periodical_journey_update', protobuf_v=ver, journey_id=journey_id, sample_points=tmp['sample_points'],
                                     vid=vid, vin=vin, sleep_time=0.5)

                # sapa 有两次从0变为6
                nextev_message, obj_np = publish_msg_by_kafka_adas('feature_status_update', protobuf_v=ver,
                                                                   adas_header_data={
                                                                       'timestamp': start_ts + i * publish_rate,
                                                                       'mileage': mileage + i
                                                                   },
                                                                   feature_status_data={
                                                                       'timestamp': (start_ts + i * publish_rate) // 1000,
                                                                       'acc_np_sts': 0,
                                                                       'sapa_status': 6 if i == 1 or i == 3 else 0
                                                                   },
                                                                   sample_ts=start_ts + i * publish_rate,
                                                                   vid=vid, vin=vin,
                                                                   )

                obj_np_list.append(obj_np)

            # end
            po_s = {"latitude": LAT_LONG[journey_update_num]['latitude'], "longitude": LAT_LONG[journey_update_num]['longitude'], "posng_valid_type": 0}
            if ver==17:
                nextev_message, obj_end = publish_msg_by_kafka('journey_end_event',
                                                               vid=vid, vin=vin,
                                                               journey_id=journey_id,
                                                               sample_ts=start_ts + journey_update_num * publish_rate,
                                                               position_status=po_s,
                                                               soc_status={"remaining_range": remaining_range - journey_update_num,
                                                                           'soc': soc - journey_update_num,
                                                                           'dump_enrgy': dump_enrgy - journey_update_num},
                                                               vehicle_status={"mileage": mileage + journey_update_num, "soc": soc - journey_update_num},
                                                               )
            else:
                nextev_message, obj_end = publish_msg_by_kafka('trip_end_event', protobuf_v=18,
                                                               vid=vid, vin=vin,
                                                               sample_ts=start_ts + journey_update_num * publish_rate,
                                                               position_status=po_s,
                                                               soc_status={"remaining_range": remaining_range - journey_update_num,
                                                                           'soc': soc - journey_update_num,
                                                                           'dump_enrgy': dump_enrgy - journey_update_num},
                                                               vehicle_status={"mileage": mileage + journey_update_num, "soc": soc - journey_update_num},
                                                               trip_status={'trip_id': journey_id}
                                                               )
                publish_msg_by_kafka('journey_end_event', protobuf_v=ver,
                                     vid=vid, vin=vin,
                                     journey_id=journey_id0,
                                     sample_ts=start_ts + journey_update_num * publish_rate,
                                     position_status=po_s,
                                     soc_status={"remaining_range": remaining_range - journey_update_num,
                                                 'soc': soc - journey_update_num,
                                                 'dump_enrgy': dump_enrgy - journey_update_num},
                                     vehicle_status={"mileage": mileage + journey_update_num, "soc": soc - journey_update_num},
                                     )
            # print for debug
            print("******")
            print(f'vid {vid}')
            print(f'obj_sta {obj_start["sample_ts"]}  {obj_start["vehicle_status"]["mileage"]}')
            for i in range(len(obj_np_list)):
                print(
                    f'obj_np{i} {obj_np_list[i]["AdasHeader"]["timestamp"]} \
                                {obj_np_list[i]["FeatureStatusUpdate"]["feature_status"]["timestamp"]}  \
                                {obj_np_list[i]["FeatureStatusUpdate"]["feature_status"]["sapa_status"]}')
            print(f'obj_end {obj_end["sample_ts"]}  {obj_end["vehicle_status"]["mileage"]}')

            history_adas_mysql = mysql['rvs'].fetch('history_adas_journey', where_model={'process_id': journey_id, 'vehicle_id': vid})[0]

            # check
            assert_equal(history_adas_mysql['sapa_count'], 2)

    @pytest.mark.parametrize('tag, ver', [('vehicle_history_1', 17), ('vehicle_history_2', 18)])
    def test_nop(self, env, mysql, publish_msg_by_kafka, publish_msg_by_kafka_adas, tag, ver):
        """
        nop需求文档： https://confluence.nioint.com/pages/viewpage.action?pageId=293031595
        nop_sts标记的是领航辅助状态。值的取值范围为0-7。。状态3(NOP_ACTIVE)算领航激活，其他状态算领航未激活
            nop_sts(0-7) NOP_OFF=0;NOP_STANDBY=1;NOP_READY=2;NOP_ACTIVE=3;NOP_PASSIVE=4;NOP_STS_RESERVED0=5;NOP_STS_RESERVED1=6;NOP_STS_RESERVED2=7;
            nop_status与nop_sts关系如右 1=3  0=1,2,4,5,6,7


        * 同样当行程数据里有np的feature_status_update事件事件上报时，会在redis里记录每一次np_status变化情况，
        * 当行程结束时，将redis中的np数据整理后落库到mysql的history_adas_journey表，并清空redis数据。

        * 注意：nop状态上报能落库的条件是np是开启的，即acc_np_sts=3或5

        """
        vid = env['vehicles'][tag]['vehicle_id']
        vin = env['vehicles'][tag]['vin']
        with allure.step("校验领航辅助nop数据能正常落库到history_adas_journey表"):
            # vid = '857bdcec079845cf9e64e328a7b2c282'
            # vin = 'SQETEST0387987190'
            start_ts = int(time.time()) * 1000
            if ver == 17:
                journey_id = datetime.utcfromtimestamp(int(start_ts) / 1000.0).strftime('%Y%m%d%H%M%S') + '0001'
            else:
                journey_id = str(start_ts // 1000)
                journey_id0 = datetime.utcfromtimestamp(int(start_ts) / 1000.0).strftime('%Y%m%d%H%M%S') + '0001'

            journey_update_num = 5  # update事件上报的数量 不能超过800条
            publish_rate = 30000  # ms 事件上报频率 30s

            soc = 98  # -
            dump_enrgy = 70  # -
            remaining_range = 500  # -

            mileage = mysql['rvs'].fetch('status_vehicle', {"id": vid}, ['mileage'])[0]['mileage']

            # start
            po_s = {"latitude": LAT_LONG[0]['latitude'], "longitude": LAT_LONG[0]['longitude'], "posng_valid_type": 0}
            if ver == 17:
                nextev_message, obj_start = publish_msg_by_kafka('journey_start_event',
                                                                 vid=vid, vin=vin,
                                                                 journey_id=journey_id,
                                                                 sample_ts=start_ts,
                                                                 position_status=po_s,
                                                                 soc_status={"remaining_range": remaining_range, 'soc': soc, 'dump_enrgy': dump_enrgy},
                                                                 vehicle_status={"mileage": mileage, "soc": soc},
                                                                 sleep_time=0.5
                                                                 )
            else:
                publish_msg_by_kafka('journey_start_event', protobuf_v=18,
                                     vid=vid, vin=vin,
                                     journey_id=journey_id0,
                                     sample_ts=start_ts,
                                     position_status=po_s,
                                     soc_status={"remaining_range": remaining_range, 'soc': soc,
                                                 'dump_enrgy': dump_enrgy},
                                     vehicle_status={"mileage": mileage, "soc": soc},
                                     )

                nextev_message, obj_start = publish_msg_by_kafka('trip_start_event', protobuf_v=18,
                                                                 vid=vid, vin=vin,
                                                                 sample_ts=start_ts,
                                                                 position_status=po_s,
                                                                 soc_status={"remaining_range": remaining_range, 'soc': soc, 'dump_enrgy': dump_enrgy},
                                                                 vehicle_status={"mileage": mileage, "soc": soc},
                                                                 trip_status={'trip_id': journey_id},
                                                                 sleep_time=0.5
                                                                 )

            obj_nop_list = []
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
                            "vehicle_status": {"speed": 100, "mileage": mileage + i, "soc": soc - i},
                            "soc_status": {"remaining_range": remaining_range - i,
                                           "soc": soc - i,
                                           "dump_enrgy": dump_enrgy - i},

                        }
                    ]
                }
                publish_msg_by_kafka('periodical_journey_update', protobuf_v=ver, journey_id=journey_id, sample_points=tmp['sample_points'],
                                     vid=vid, vin=vin, sleep_time=0.5)

                nextev_message, obj_nop = publish_msg_by_kafka_adas('feature_status_update', protobuf_v=ver,
                                                                    adas_header_data={
                                                                        'timestamp': start_ts + i * publish_rate,
                                                                        'mileage': mileage + i
                                                                    },
                                                                    feature_status_data={'timestamp': (start_ts + (1 if i < 3 else 3) * publish_rate) // 1000,
                                                                                         'nop_sts': 3 if i < 3 else 4,
                                                                                         'acc_np_sts': 5,
                                                                                         'sapa_status': 0
                                                                                         },
                                                                    sample_ts=start_ts + i * publish_rate,
                                                                    vid=vid, vin=vin,
                                                                    )
                obj_nop_list.append(obj_nop)

            # end
            po_s = {"latitude": LAT_LONG[journey_update_num]['latitude'], "longitude": LAT_LONG[journey_update_num]['longitude'], "posng_valid_type": 0}
            if ver==17:
                nextev_message, obj_end = publish_msg_by_kafka('journey_end_event',
                                                               vid=vid, vin=vin,
                                                               journey_id=journey_id,
                                                               sample_ts=start_ts + journey_update_num * publish_rate,
                                                               position_status=po_s,
                                                               soc_status={"remaining_range": remaining_range - journey_update_num,
                                                                           'soc': soc - journey_update_num,
                                                                           'dump_enrgy': dump_enrgy - journey_update_num},
                                                               vehicle_status={"mileage": mileage + journey_update_num, "soc": soc - journey_update_num},
                                                               )
            else:
                publish_msg_by_kafka('journey_end_event', protobuf_v=ver,
                                     vid=vid, vin=vin,
                                     journey_id=journey_id0,
                                     sample_ts=start_ts + journey_update_num * publish_rate,
                                     position_status=po_s,
                                     soc_status={"remaining_range": remaining_range - journey_update_num,
                                                 'soc': soc - journey_update_num,
                                                 'dump_enrgy': dump_enrgy - journey_update_num},
                                     vehicle_status={"mileage": mileage + journey_update_num,
                                                     "soc": soc - journey_update_num})

                nextev_message, obj_end = publish_msg_by_kafka('trip_end_event', protobuf_v=18,
                                                               vid=vid, vin=vin,
                                                               sample_ts=start_ts + journey_update_num * publish_rate,
                                                               position_status=po_s,
                                                               soc_status={"remaining_range": remaining_range - journey_update_num,
                                                                           'soc': soc - journey_update_num,
                                                                           'dump_enrgy': dump_enrgy - journey_update_num},
                                                               vehicle_status={"mileage": mileage + journey_update_num, "soc": soc - journey_update_num},
                                                               trip_status={'trip_id': journey_id}
                                                               )
            # print for debug
            print("******")
            print(f'vid {vid}')
            print(f'obj_sta {obj_start["sample_ts"]}  {obj_start["vehicle_status"]["mileage"]}')
            for i in range(len(obj_nop_list)):
                print(
                    f'obj_nop{i} {obj_nop_list[i]["AdasHeader"]["timestamp"]} \
                                {obj_nop_list[i]["AdasHeader"]["mileage"]} \
                                {obj_nop_list[i]["FeatureStatusUpdate"]["feature_status"]["timestamp"]}  \
                                {obj_nop_list[i]["FeatureStatusUpdate"]["feature_status"]["nop_sts"]}')
            print(f'obj_end {obj_end["sample_ts"]}  {obj_end["vehicle_status"]["mileage"]}')

            history_adas_mysql = mysql['rvs'].fetch('history_adas_journey', where_model={'process_id': journey_id, 'vehicle_id': vid})[0]
            print(f'nop_mileage:{history_adas_mysql["nop_mileage"]} nop_duration:{history_adas_mysql["nop_duration"]} nop_list:{history_adas_mysql["nop_status_list"]}')

            # check
            status_map = {0: 0, 1: 0, 2: 0, 3: 1, 4: 0, 5: 0, 6: 0, 7: 0}
            nop_ts_list = [obj_nop_list[0]["FeatureStatusUpdate"]["feature_status"]["timestamp"]]
            nop_status_list = [status_map[obj_nop_list[0]["FeatureStatusUpdate"]["feature_status"]["nop_sts"]]]
            nop_mileage_list = [obj_nop_list[0]["AdasHeader"]["mileage"]]
            nop_duration = 0
            nop_mileage = 0
            for i, item in enumerate(obj_nop_list, start=1):
                ts = item["FeatureStatusUpdate"]["feature_status"]["timestamp"]
                status = status_map[item["FeatureStatusUpdate"]["feature_status"]["nop_sts"]]
                mileage = item["AdasHeader"]["mileage"]
                if status != nop_status_list[-1]:
                    nop_ts_list.append(ts)
                    nop_status_list.append(status)
                    nop_mileage_list.append(mileage)
                    nop_duration += nop_ts_list[-1] - nop_ts_list[-2]
                    nop_mileage += nop_mileage_list[-1] - nop_mileage_list[-2]

            # 判断最后的一个status是不是0，不是0的话，把journey_end的值也加入到np list中
            if nop_status_list[-1] != 0:
                nop_ts_list.append(obj_end["sample_ts"] // 1000)
                nop_status_list.append(0)
                nop_mileage_list.append(obj_end["vehicle_status"]["mileage"])
                nop_duration += nop_ts_list[-1] - nop_ts_list[-2]
                nop_mileage += nop_mileage_list[-1] - nop_mileage_list[-2]

            assert_equal(history_adas_mysql['nop_duration'], nop_duration)
            assert_equal(history_adas_mysql['nop_mileage'], nop_mileage)

            # 判断没有sapa的情况下，sapa_count会记为0，而不是NULL
            assert_equal(history_adas_mysql['sapa_count'], 0)
            nop_status_dict = {str(nop_ts_list[i] * 1000): nop_status_list[i] for i in range(len(nop_ts_list))}
            assert_equal(json.loads(history_adas_mysql['nop_status_list']), nop_status_dict)
