# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_vehicle_jounery.py
# @Author : qiangwei.zhang.o
# @CreateTime : 2021/3/25 6:34 下午
# @Description :

import time
import random
from datetime import datetime

import pytest

# from tests.data_statistics.lat_long import LAT_LONG
# from tests.data_statistics.latitude_longitude import LA_LONG_NEW as LAT_LONG
from utils.logger import logger


def get_data(file):
    with open(file, 'r')as f:
        data = []
        for line in f.readlines():
            line = line[:-1]  # 去掉'\n'
            # latitude 纬度  longitude 经度
            location = {'longitude': float(line.split(',')[0]), 'latitude': float(line.split(',')[1])}
            data.append(location)
        return data


def get_data_new():
    # with open('./YCSYC_XC001.txt', 'r')as f:
    with open('./location_data_file/new_t6_road.txt', 'r')as f:
        data = []
        keys = []
        for line in f.readlines():
            new_line = {}
            line = line[:-1]  # 去掉'\n'
            # latitude 纬度  longitude 经度
            dict_line = eval(line)
            new_line[dict_line['sample_ts']] = f"{dict_line['longitude']},{dict_line['latitude']}"
            keys.append(dict_line['sample_ts'])
            data.append(new_line)
        keys.sort()
        for key in keys:
            for data_dict in data:
                location = data_dict.get(key, None)
                if location:
                    with open(f'./location_data_file/YCSYC_XC_t6_road_{len(keys)}.txt', 'a')as f2:
                        f2.write(f'{location}\n')
                    break


# @pytest.mark.skip('Manual')
class TestVehicleStatisticsDaily(object):
    keys = 'road,vid,vin,start_time,end_time,start_num,journey_update_num,des'
    today = time.strftime("%Y-%m-%d", time.localtime())
    values = [
        # ('t3', '3013fe4eceaa483faeefe34056f93484', 'SQETEST0291187341', f"{today} 18:00:00", f"{today} 18:10:00", 0, 93, 'stg_mp环境'),
        # ('t3', '314859ba44f74948a296e19350631b16', 'SQETEST0860956362', f"{today} 08:00:00", f"{today} 08:10:00", 0, 93, '正常车辆，不跨天的行程在盐城试验场'),
        # ('t3', '314859ba44f74948a296e19350631b16', 'SQETEST0860956362', f"{today} 15:20:00", f"{today} 15:30:00", 0, 93, '正常车辆，不跨天的行程在盐城试验场'),
        ('t3', '314859ba44f74948a296e19350631b16', 'SQETEST0860956362', f"{today} 08:00:00", f"{today} 08:40:00", 0, 80, '正常车辆，不跨天的行程在盐城试验场'),
        # ('t6', '314859ba44f74948a296e19350631b16', 'SQETEST0860956362', f"{today} 16:10:00", f"{today} 16:20:00", 0, 33, '正常车辆，不跨天的行程在盐城试验场'),
        # ('t4', '2385a6a1f97d45468aee67455874caf6', 'SQETEST0006730031', f"{today} 17:50:00", f"{today} 18:00:00", 0, 200, '正常车辆，跨天的行程在盐城试验场'),
        # ('t6', '8e4995843e464d9095d6778f3fcfaf60', 'SQETEST0000103672', f"{today} 07:00:00", f"{today} 07:10:00", 0, 33, '正常车辆，不跨天的行程在盐城试验场'),
        # ('t7', '40a0e30eea104e79b9ff9634d9b98aac', 'SQETEST0001014095', f"{today} 12:00:00", f"{today} 12:10:00", 0, 92, '正常车辆，不跨天的行程在盐城试验场'),
        # ('t10', 'a0f3a832a10f40d9be5b6e5e65bc5bc0', 'SQETEST0016402464', f"{today} 13:00:00", f"{today} 13:10:00", 0, 48, '正常车辆，不跨天的行程不在盐城试验场'),
        # ('t3', 'a0f3a832a10f40d9be5b6e5e65bc5bc0', 'SQETEST0016402464', f"{today} 14:00:00", f"{today} 14:10:00", 0, 92, '不在列表内的车辆，有盐城试验场的行程'),
        # ('t3', '0559803010374eca92b7be8a20d51e30', 'SQETEST0258558967', f"{today} 08:00:00", f"{today} 14:00:00", 0, 1000, 'dev在列表内的车辆，有盐城试验场的行程'),
        # ('t3', '0559803010374eca92b7be8a20d51e30', 'SQETEST0258558967', f"{today} 08:00:00", f"{today} 14:00:00", 0, 1000, 'dev在列表内的车辆，有盐城试验场的行程'),
    ]

    @pytest.mark.parametrize(keys, values)
    def test_journey_daily(self, publish_msg_by_kafka, road, mysql, vid, vin, start_time, end_time, start_num, journey_update_num, des):
        """
        select * from vehicle_data where vehicle_id='0559803010374eca92b7be8a20d51e30' and sample_date='2021-03' allow filtering;
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
        file_path = {"t3": './location_data_file/YCSYC_XC_t3_road_94.txt',
                     "t4": './location_data_file/YCSYC_XC_t4_road_204.txt',
                     "t6": './location_data_file/YCSYC_XC_t6_road_44.txt',
                     "t7": './location_data_file/YCSYC_XC_t7_road_94.txt',
                     "t10": './location_data_file/YCSYC_XC_t10_road_50.txt',
                     "tt": './location_data_file/OTHER_ROAD_816.txt',
                     }
        LAT_LONG = get_data(file_path.get(road, './location_data_file/YCSYC_XC_t4_road_204.txt'))
        len_list = len(LAT_LONG) - 2
        logger.debug(f'vid{vid}vin{vin}start_time{start_time}end_time{end_time}start_num{start_num}journey_update_num{journey_update_num}des{des}')
        start_ts = int(time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))) * 1000
        end_ts = int(time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S"))) * 1000
        journey_id = datetime.utcfromtimestamp(int(time.time())).strftime('%Y%m%d%H%M%S')[0:-1]
        logger.debug(f'行程id:{journey_id}')
        publish_rate = int((end_ts - start_ts) / journey_update_num)  # ms 事件上报频率
        if publish_rate < 0:
            assert 1 == 0
        mileage_rate = int(journey_update_num / 500) + 1
        soc = 98  # -
        dump_enrgy = 70  # -
        remaining_range = 500  # -
        logger.debug(f'开始时间{start_ts}结束时间{start_ts + publish_rate * journey_update_num}上报条数{journey_update_num}上报频率{publish_rate}')
        mileage_list = mysql['rvs'].fetch('status_vehicle', {"id": vid}, ['mileage'])
        mileage = mileage_list[0]['mileage'] if mileage_list else 0
        po_s = {"latitude": LAT_LONG[0]['latitude'], "longitude": LAT_LONG[start_num]['longitude'], "posng_valid_type": 0}
        sample_ts = start_ts
        nextev_message, obj = publish_msg_by_kafka('journey_start_event',
                                                   vid=vid, vin=vin,
                                                   journey_id=journey_id,
                                                   sample_ts=sample_ts,
                                                   position_status=po_s,
                                                   soc_status={"remaining_range": remaining_range, 'soc': soc, 'dump_enrgy': dump_enrgy},
                                                   vehicle_status={"mileage": mileage, "soc": soc},
                                                   sleep_time=0.01
                                                   )
        # update
        for i, item in enumerate(LAT_LONG[start_num + 1:start_num + journey_update_num], start=1):
            longitude, latitude = item['longitude'], item['latitude']
            ls = [0, 1]
            random.sample(ls, 1)
            can_value = f"{random.sample(ls, 1)[0]}{random.sample(ls, 1)[0]}{random.sample(ls, 1)[0]}{random.sample(ls, 1)[0]}{random.sample(ls, 1)[0]}{random.sample(ls, 1)[0]}{random.sample(ls, 1)[0]}{random.sample(ls, 1)[0]}{random.sample(ls, 1)[0]}{random.sample(ls, 1)[0]}{random.sample(ls, 1)[0]}{random.sample(ls, 1)[0]}{random.sample(ls, 1)[0]}{random.sample(ls, 1)[0]}"

            logger.debug(f"can_value:{can_value}")
            # can_value_bytes = bytes(can_value, 'utf-8')
            # logger.debug(f"can_value_bytes:{can_value_bytes}")
            tmp = {
                "journey_id": journey_id,
                "sample_points": [
                    {
                        "sample_ts": start_ts + i * publish_rate,
                        "position_status": {
                            "posng_valid_type": 0,
                            "longitude": longitude,
                            "latitude": latitude
                        },
                        "vehicle_status": {"speed": 80, "mileage": mileage + int(i / mileage_rate), "soc": soc - i * 0.01},
                        "soc_status": {"remaining_range": remaining_range - i * 0.1,
                                       "soc": soc - i * 0.01,
                                       "dump_enrgy": dump_enrgy - i * 0.01,
                                       'btry_paks': [{'sin_btry_voltage': random.sample(range(10, 80), random.randint(1, 30)),
                                                      'prb_temp_lst': random.sample(range(10, 80), random.randint(1, 30)),
                                                      'sin_btry_voltage_inv': [6],
                                                      'prb_temp_lst_inv': random.sample(range(10, 80), random.randint(1, 30))},
                                                     {'sin_btry_voltage': random.sample(range(10, 80), random.randint(1, 30)),
                                                      'prb_temp_lst': random.sample(range(10, 80), random.randint(1, 30)),
                                                      'sin_btry_voltage_inv': random.sample(range(10, 80), random.randint(1, 30)),
                                                      'prb_temp_lst_inv': random.sample(range(10, 80), random.randint(1, 30))}]},
                    },

            ]
            }
            publish_msg_by_kafka('periodical_journey_update', journey_id=journey_id, sample_points=tmp['sample_points'],
                                 vid=vid, vin=vin, sleep_time=0.01)

        # end
        po_s = {"latitude": LAT_LONG[journey_update_num]['latitude'], "longitude": LAT_LONG[start_num + journey_update_num]['longitude'], "posng_valid_type": 0}
        sample_ts = start_ts + journey_update_num * publish_rate
        logger.debug(f'结束时间{start_ts}')
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

    @pytest.mark.skip('manual')
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
