import time
from datetime import datetime

from tests.data_statistics.lat_long import LAT_LONG


# @pytest.mark.skip('Manual')
class TestVehicleStatisticsDaily(object):
    def test_end_energy_and_comsume_energy(self, publish_msg_by_kafka):
        """
        该方法为造数据方法，具体的统计校验见testlink
        TestLink： http://testlink.fareast.nevint.com/linkto.php?tprojectPrefix=DSts&item=testcase&id=DSts-391

        """
        vid = 'ed37c834509248b7914c9498c4d2129a'
        vin = 'SQETEST0596093473'

        ts = round(time.time() * 1000)
        nextev_message, obj = publish_msg_by_kafka('specific_event', event_type='power_swap_start', vid=vid, vin=vin, data={'dump_enrgy': 15, 'sample_ts': ts})
        nextev_message, obj = publish_msg_by_kafka('specific_event', event_type='power_swap_end', vid=vid, vin=vin, data={'dump_enrgy': 35, 'sample_ts': ts + 3 * 60 * 1000})
        nextev_message, obj = publish_msg_by_kafka('charge_start_event', soc_status={'dump_enrgy': 10}, vid=vid, vin=vin, sample_ts=ts + 4 * 60 * 1000)
        nextev_message, obj = publish_msg_by_kafka('charge_end_event', soc_status={'dump_enrgy': 30}, vid=vid, vin=vin, sample_ts=ts + 12 * 60 * 1000)
        nextev_message, obj = publish_msg_by_kafka('journey_end_event', soc_status={'dump_enrgy': 35}, vid=vid, vin=vin, sample_ts=ts + 13 * 60 * 1000)

    def test_invalid_gps(self, publish_msg_by_kafka):
        """
        TODO 注意是stg的车！
        posng_valid_type = 2 表示 gps失效 GPS_MALFUNCTION = 2
        一、行程统计相关

            统计基于journey(聚合后的行程)
            单次行程时长：>0小时， <= 10小时
            单次行程距离：>0KM，<= 500KM
            开始和结束时间不能为空
            结束时间>开始时间
            结束里程>开始里程
            开始电量>=结束电量
            开始预估剩余里程 > 结束预估剩余里程
            跨天的行程，统计到开始时间所在日中
        :return:
        期望 gps_invalid_count=2, gps_invalid_duration=240, gps_driving_invalid_count=2, gps_driving_invalid_duration=240
        """

        vid = '7c5b58dc76a440938320a6dcac56b275'
        vin = 'SQETEST0941216147'

        ts = round(time.time() * 1000)

        posi = [{"latitude": 31.273119, "longitude": 104.163170},
                {"latitude": 31.269964, "longitude": 104.162092},
                {"latitude": 31.266805, "longitude": 104.165893},
                {"latitude": 31.266251, "longitude": 104.171764},
                {"latitude": 31.275262, "longitude": 104.168295},
                {"latitude": 31.264943, "longitude": 104.170044},
                {"latitude": 31.265004, "longitude": 104.170169},
                {"latitude": 31.265144, "longitude": 104.170417},
                {"latitude": 31.265293, "longitude": 104.170626},
                {"latitude": 31.265449, "longitude": 104.170795},
                {"latitude": 31.265613, "longitude": 104.170939},
                {"latitude": 31.265780, "longitude": 104.171077},
                {"latitude": 31.265928, "longitude": 104.171210},

                ]

        # 第一段行程
        # start
        journey_id = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d') + '0001'
        mileage = 2  # +
        soc = 20  # -
        remaining_range = 40  # -
        po_s = {"latitude": posi[0]['latitude'], "longitude": posi[0]['longitude'], "posng_valid_type": 0}
        sample_ts = ts + 0 * 60 * 1000  # +
        nextev_message, obj = publish_msg_by_kafka('journey_start_event',
                                                   vid=vid, vin=vin,
                                                   journey_id=journey_id,
                                                   sample_ts=sample_ts, soc_status={"remaining_range": remaining_range, 'soc': soc},
                                                   position_status=po_s, vehicle_status={"mileage": mileage, "soc": soc},
                                                   )

        # 无效
        mileage = 3
        soc = 18
        remaining_range = 38
        po_s = {"latitude": posi[1]['latitude'], "longitude": posi[1]['longitude'], "posng_valid_type": 2}
        sample_ts = ts + 1 * 60 * 1000
        nextev_message, obj = publish_msg_by_kafka('periodical_journey_update',
                                                   vid=vid, vin=vin,
                                                   journey_id=journey_id,
                                                   sample_points=[{
                                                       "vehicle_status": {"mileage": mileage, "soc": soc},
                                                       "soc_status": {"remaining_range": remaining_range, "soc": soc, },
                                                       "position_status": po_s,
                                                       "sample_ts": sample_ts,
                                                   }]
                                                   )

        # 无效
        mileage = 4  # +
        soc = 17  # -
        remaining_range = 37  # -
        po_s = {"latitude": posi[2]['latitude'], "longitude": posi[2]['longitude'], "posng_valid_type": 2}
        sample_ts = ts + 2 * 60 * 1000  # +
        nextev_message, obj = publish_msg_by_kafka('periodical_journey_update',
                                                   vid=vid, vin=vin,
                                                   journey_id=journey_id,
                                                   sample_points=[{
                                                       "vehicle_status": {"mileage": mileage, "soc": soc},
                                                       "soc_status": {"remaining_range": remaining_range, "soc": soc},
                                                       "position_status": po_s,
                                                       "sample_ts": sample_ts,
                                                   }])

        # end
        mileage = 5  # +
        soc = 16  # -
        remaining_range = 36  # -
        po_s = {"latitude": posi[3]['latitude'], "longitude": posi[3]['longitude'], "posng_valid_type": 0}
        sample_ts = ts + 3 * 60 * 1000  # +
        nextev_message, obj = publish_msg_by_kafka('journey_end_event',
                                                   vid=vid, vin=vin,
                                                   journey_id=journey_id,
                                                   sample_ts=sample_ts, soc_status={"remaining_range": remaining_range, 'soc': soc},
                                                   position_status=po_s, vehicle_status={"mileage": mileage, "soc": soc},
                                                   )

        # 第二段行程
        # start
        journey_id = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d') + '0002'
        mileage = 6  # +
        soc = 15  # -
        remaining_range = 35  # -
        po_s = {"latitude": posi[4]['latitude'], "longitude": posi[4]['longitude'], "posng_valid_type": 0}
        sample_ts = ts + 12 * 60 * 1000  # +
        nextev_message, obj = publish_msg_by_kafka('journey_start_event',
                                                   vid=vid, vin=vin,
                                                   journey_id=journey_id,
                                                   sample_ts=sample_ts, soc_status={"remaining_range": remaining_range, 'soc': soc},
                                                   position_status=po_s, vehicle_status={"mileage": mileage, "soc": soc},
                                                   )

        # 无效
        mileage = 7
        soc = 14
        remaining_range = 34
        po_s = {"latitude": posi[5]['latitude'], "longitude": posi[5]['longitude'], "posng_valid_type": 2}
        sample_ts = ts + 13 * 60 * 1000
        nextev_message, obj = publish_msg_by_kafka('periodical_journey_update',
                                                   vid=vid, vin=vin,
                                                   journey_id=journey_id,
                                                   sample_points=[{
                                                       "vehicle_status": {"mileage": mileage, "soc": soc},
                                                       "soc_status": {"remaining_range": remaining_range, "soc": soc, },
                                                       "position_status": po_s,
                                                       "sample_ts": sample_ts,
                                                   }]
                                                   )

        # 无效
        mileage = 8  # +
        soc = 13  # -
        remaining_range = 33  # -
        po_s = {"latitude": posi[6]['latitude'], "longitude": posi[6]['longitude'], "posng_valid_type": 2}
        sample_ts = ts + 14 * 60 * 1000  # +
        nextev_message, obj = publish_msg_by_kafka('periodical_journey_update',
                                                   vid=vid, vin=vin,
                                                   journey_id=journey_id,
                                                   sample_points=[{
                                                       "vehicle_status": {"mileage": mileage, "soc": soc},
                                                       "soc_status": {"remaining_range": remaining_range, "soc": soc},
                                                       "position_status": po_s,
                                                       "sample_ts": sample_ts,
                                                   }])

        # end
        mileage = 9  # +
        soc = 12  # -
        remaining_range = 32  # -
        po_s = {"latitude": posi[7]['latitude'], "longitude": posi[7]['longitude'], "posng_valid_type": 0}
        sample_ts = ts + 15 * 60 * 1000  # +
        nextev_message, obj = publish_msg_by_kafka('journey_end_event',
                                                   vid=vid, vin=vin,
                                                   journey_id=journey_id,
                                                   sample_ts=sample_ts, soc_status={"remaining_range": remaining_range, 'soc': soc},
                                                   position_status=po_s, vehicle_status={"mileage": mileage, "soc": soc},
                                                   )

    def test_journey_daily(self, publish_msg_by_kafka, publish_msg_by_kafka_adas, mysql):
        """
        该方法造行程数据
            统计基于journey(聚合后的行程)
            单次行程时长：>0小时， <= 10小时
            单次行程距离：>0KM，<= 500KM
            开始和结束时间不能为空
            结束时间>开始时间
            结束里程>开始里程
            开始电量>=结束电量
            开始预估剩余里程 > 结束预估剩余里程
            跨天的行程，统计到开始时间所在日中
        """

        vid = 'cdf124b457794d59b236795fb61106b4'
        vin = mysql['rvs'].fetch('vehicle_profile',{"id": vid},['vin'])[0]['vin']


        # start_ts = 1575993499000
        # end_ts = 1574056350000

        start_ts = int(time.time()) * 1000
        # end_ts = 1565778510000
        journey_id = datetime.utcfromtimestamp(int(start_ts) / 1000.0).strftime('%Y%m%d') + '00005'
        # journey_id = '2019090500003'

        journey_update_num = 10  # update事件上报的数量 不能超过800条
        publish_rate = 60000  # ms 事件上报频率

        soc = 98  # -
        dump_enrgy = 70  # -
        remaining_range = 500  # -

        mileage = mysql['rvs'].fetch('status_vehicle',{"id": vid},['mileage'])[0]['mileage']


        # start
        po_s = {"latitude": LAT_LONG[0]['latitude'], "longitude": LAT_LONG[0]['longitude'], "posng_valid_type": 0}
        sample_ts = start_ts
        nextev_message, obj = publish_msg_by_kafka('journey_start_event',
                                                   vid=vid, vin=vin,
                                                   journey_id=journey_id,
                                                   sample_ts=sample_ts,
                                                   position_status=po_s,
                                                   soc_status={"remaining_range": remaining_range, 'soc': soc, 'dump_enrgy': dump_enrgy},
                                                   vehicle_status={"mileage": mileage, "soc": soc},
                                                   sleep_time=0.01)

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
                        "soc_status": {"remaining_range": remaining_range - i * 0.1,
                                       "soc": soc - i * 0.01,
                                       "dump_enrgy": dump_enrgy - i * 0.01},

                    }
                ]
            }
            publish_msg_by_kafka('periodical_journey_update', journey_id=journey_id, sample_points=tmp['sample_points'],
                                 vid=vid, vin=vin, sleep_time=0.01)

            publish_msg_by_kafka_adas('feature_status_update',
                                      vid=vid, vin=vin,
                                      adas_header_data={
                                          'timestamp': start_ts + i * publish_rate,
                                          'mileage': mileage + i
                                      },
                                      feature_status_data={'timestamp': (start_ts + (1 if i < 3 else 3) * publish_rate) // 1000,
                                                           'acc_np_sts': 3 if i < 3 else 5
                                                           },
                                      sample_ts=start_ts + i * publish_rate,
                                      sleep_time=0.5)

        # end
        po_s = {"latitude": LAT_LONG[journey_update_num]['latitude'], "longitude": LAT_LONG[journey_update_num]['longitude'], "posng_valid_type": 0}
        sample_ts = start_ts + journey_update_num * publish_rate
        nextev_message, obj = publish_msg_by_kafka('journey_end_event',
                                                   vid=vid, vin=vin,
                                                   journey_id=journey_id,
                                                   sample_ts=sample_ts,
                                                   position_status=po_s,
                                                   soc_status={"remaining_range": remaining_range - journey_update_num * 0.1,
                                                               'soc': soc - journey_update_num * 0.01,
                                                               'dump_enrgy': dump_enrgy - journey_update_num * 0.01},
                                                   vehicle_status={"mileage": mileage + journey_update_num, "soc": soc - journey_update_num * 0.01},
                                                   sleep_time=0.01,
                                                   )

    def test_charge_daily(self, publish_msg_by_kafka):
        """
        该方法造充电数据和换电数据。符合如下统计规则

        充电时长：>5分钟，<=36小时
        开始和结束时间不能为空
        结束时间>开始时间
        结束电量>开始电量
        充电开始时间大于车辆激活时间
        充电电量、充电时长、充电次数以结束时间统计

        """
        vid = 'ed37c834509248b7914c9498c4d2129a'
        vin = 'SQETEST0596093473'

        ts = round(time.time() * 1000)
        charge_id = datetime.utcfromtimestamp(int(ts) / 1000.0).strftime('%Y%m%d') + '0001'
        # nextev_message, obj = publish_msg_by_kafka('specific_event', event_type='power_swap_start', vid=vid, vin=vin, data={'dump_enrgy': 15, 'sample_ts': ts})
        # nextev_message, obj = publish_msg_by_kafka('specific_event', event_type='power_swap_end', vid=vid, vin=vin, data={'dump_enrgy': 35, 'sample_ts': ts + 3 * 60 * 1000})
        nextev_message, obj = publish_msg_by_kafka('charge_start_event',
                                                   charge_id=charge_id,
                                                   soc_status={'dump_enrgy': 10, 'soc': 12},
                                                   charging_info={'charger_type': 2},
                                                   vid=vid, vin=vin, sample_ts=ts + 4 * 60 * 1000)
        nextev_message, obj = publish_msg_by_kafka('charge_end_event',
                                                   charge_id=charge_id,
                                                   soc_status={'dump_enrgy': 80, 'soc': 100},
                                                   charging_info={'charger_type': 2},
                                                   vid=vid, vin=vin, sample_ts=ts + 12 * 60 * 1000)

    def test_trip_daily(self, publish_msg_by_kafka, publish_msg_by_kafka_adas, mysql):
        """
        该方法造行程数据
            统计基于journey(聚合后的行程)
            单次行程时长：>0小时， <= 10小时
            单次行程距离：>0KM，<= 500KM
            开始和结束时间不能为空
            结束时间>开始时间
            结束里程>开始里程
            开始电量>=结束电量
            开始预估剩余里程 > 结束预估剩余里程
            跨天的行程，统计到开始时间所在日中
        """

        vid = '74361e94a61846e2a690d2e2a9bf591d'
        vin = mysql['rvs'].fetch('vehicle_profile', {"id": vid}, ['vin'])[0]['vin']


        # start_ts = 1575993499000
        # end_ts = 1574056350000

        start_ts = int(time.time()) * 1000
        # end_ts = 1565778510000
        trip_id = str(int(start_ts/1000))
        # journey_id = '2019090500003'

        journey_update_num = 10  # update事件上报的数量 不能超过800条
        publish_rate = 60000  # ms 事件上报频率

        soc = 98  # -
        dump_enrgy = 70  # -
        remaining_range = 500  # -

        mileage = mysql['rvs'].fetch('status_vehicle', {"id": vid}, ['mileage'])[0]['mileage']


        # start
        po_s = {"latitude": LAT_LONG[0]['latitude'], "longitude": LAT_LONG[0]['longitude'], "posng_valid_type": 0}
        sample_ts = start_ts
        publish_msg_by_kafka('trip_start_event',
                             vid=vid, vin=vin,
                             protobuf_v=18,
                             sample_ts=sample_ts,
                             trip_status={"trip_id": trip_id},
                             position_status=po_s,
                             soc_status={"remaining_range": remaining_range, 'soc': soc, 'dump_enrgy': dump_enrgy},
                             vehicle_status={"mileage": mileage, "soc": soc},
                             sleep_time=0.01)

        # update
        for i, item in enumerate(LAT_LONG[1:journey_update_num], start=1):
            tmp = {
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
                        "trip_status": {"trip_id": trip_id}
                    }
                ]
            }
            publish_msg_by_kafka('periodical_journey_update',
                                 vid=vid, vin=vin,
                                 protobuf_v=18,
                                 sample_points=tmp['sample_points'],
                                 sleep_time=0.01)

            publish_msg_by_kafka_adas('feature_status_update',
                                      vid=vid, vin=vin,
                                      protobuf_v=18,
                                      adas_header_data={
                                          'timestamp': start_ts + i * publish_rate,
                                          'mileage': mileage + i
                                      },
                                      feature_status_data={'timestamp': (start_ts + (1 if i < 3 else 3) * publish_rate) // 1000,
                                                           'acc_np_sts': 3 if i < 3 else 5
                                                           },
                                      sample_ts=start_ts + i * publish_rate,
                                      sleep_time=0.5)

        # end
        po_s = {"latitude": LAT_LONG[journey_update_num]['latitude'], "longitude": LAT_LONG[journey_update_num]['longitude'], "posng_valid_type": 0}
        sample_ts = start_ts + journey_update_num * publish_rate
        publish_msg_by_kafka('trip_end_event',
                             vid=vid, vin=vin,
                             protobuf_v=18,
                             sample_ts=sample_ts,
                             trip_status={"trip_id": trip_id},
                             position_status=po_s,
                             soc_status={"remaining_range": remaining_range - journey_update_num,
                                         'soc': soc - journey_update_num,
                                         'dump_enrgy': dump_enrgy - journey_update_num},
                             vehicle_status={"mileage": mileage + journey_update_num, "soc": soc - journey_update_num},
                             sleep_time=0.01)
