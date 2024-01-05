# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/1/28 16:16
# @File: oss_utils.py
import time

import pymongo

from oss.southbound.device2cloud import PowerDevice_pb2
# from utils.log import log

HOST = '10.112.12.153'
PORT = 27017
USERNAME = "opman"
PASSWORD = "N7102io"


def get_value(data):
    """

    :param data:
    :return:
    """
    res = dict()
    res["key"] = data.key
    res["type"] = data.type
    if data.type == 1:
        res["value"] = data.value_bool
    elif data.type == 2:
        res["value"] = data.value_int
    elif data.type == 4:
        res["value"] = round(data.value_float, 2)
    elif data.type == 6:
        temp = data.value_string
        if isinstance(temp, bytes):
            try:
                res["value"] = data.value_string.decode()
            except Exception as e:
                res['value'] = str(data.value_string)
    elif data.type == 3:
        res["value"] = round(data.value_long, 2)
    elif data.type == 5:
        res["value"] = round(data.value_double, 2)
    elif data.type == 7:
        res["value"] = data.value_bytes
    else:
        res["value"] = -1
    return res


def get_oss_alarm_data(resource_id,
                       target_key,
                       query_alarm, ):
    """

    :param resource_id:
    :param target_key:
    :param query_alarm:
    :return:
    """
    res = {
        "key": target_key,
        'type': -1,
        'value': -1
    }
    try:
        client = pymongo.MongoClient(host=HOST, port=PORT, username=USERNAME, password=PASSWORD)
        collection = client[resource_id]['alarm']
    except Exception as e:
        res['message'] = f"connect mongodb error, {e}"
        return res
    for data in collection.find().sort("timestamp", -1):
        try:
            pow_msg = PowerDevice_pb2.PowerDeviceMessage()
            pow_msg.ParseFromString(data["value"])
        except Exception as e:
            # log.error(f"<OSS>:power device alarm message parse fail:{data}")
            continue
        for alarm_data in pow_msg.alarm.alarm:
            if alarm_data.alarm_type_id == target_key and alarm_data.alarm_state == query_alarm:
                client.close()
                return {"key": alarm_data.alarm_type_id,
                        "type": 1,
                        "value": query_alarm,
                        "timestamp": alarm_data.alarm_timestamp}
    client.close()
    return res


def get_oss_real_time_data(resource_id: str, target_key: str) -> dict:
    """

    :param resource_id:
    :param target_key:
    :return:
    """
    res = {
        "key": target_key,
        'type': -1,
        'value': -1
    }
    try:
        client = pymongo.MongoClient(host=HOST, port=PORT, username=USERNAME, password=PASSWORD)
        collection = client[resource_id]['realtime']
    except Exception as e:
        res['message'] = f"connect mongodb error, {e}"
        return res
    for data in collection.find().sort("timestamp", -1):
        try:
            pow_msg = PowerDevice_pb2.PowerDeviceMessage()
            pow_msg.ParseFromString(data["value"])
        except Exception as e:
            # log.error(f"<OSS>:power device real time message parse fail:{data}")
            continue
        if pow_msg.realtime:
            for real_data in pow_msg.realtime.data:
                if real_data.key == target_key:
                    client.close()
                    return get_value(real_data)
        elif pow_msg.basic:
            for real_data in pow_msg.basic.data:
                if real_data.key == target_key:
                    client.close()
                    return get_value(real_data)
    client.close()
    return res


def get_oss_event_data(resource_id: str, target_key: str, select, timestamp=0):
    """

    :param resource_id: 站ID
    :param target_key: 换电事件ID
    :param select:筛选具体的事件
    :param timestamp:数据库过滤条件
    :return:
    """
    res = {
        "event_id": target_key,
        "timestamp": 0,
        "data": []
    }
    try:
        client = pymongo.MongoClient(host=HOST, port=PORT, username=USERNAME, password=PASSWORD)
        collection = client[resource_id]['event']
    except Exception as e:
        res['message'] = f"connect mongodb error, {e}"
        return res
    if timestamp == 0:
        result_set = collection.find().sort("timestamp", -1)
    else:
        result_set = collection.find({"timestamp": {"$gt": int(timestamp)}}).sort("timestamp", -1)
    for data in result_set:
        try:
            pow_msg = PowerDevice_pb2.PowerDeviceMessage()
            pow_msg.ParseFromString(data["value"])
        except Exception as e:
            # log.error(f"<OSS>:power device event message parse fail:{data}")
            continue
        if pow_msg.event and pow_msg.event.event_id == target_key:
            res["timestamp"] = pow_msg.event.timestamp
            res["datatime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(pow_msg.event.timestamp // 1000))
            flag = False
            for d in pow_msg.event.data:
                tmp = {}
                for des, val in d.ListFields():
                    if des.__dict__.get("name") == "value_string" and isinstance(val, bytes):
                        val = val.decode()
                    tmp[des.__dict__.get("name")] = val
                res["data"].append(tmp)
                if not flag and select:  # 这里根据传入的过滤条件筛选
                    _data = get_value(d)
                    # 不同数据类型统一按照字符串处理: str(_data.get("value", ""))
                    if _data.get("key", "") == select.get("key") and str(_data.get("value", "")) == select.get("value"):
                        flag = True
            if select and not flag:  # 有筛选条件，但具体内容不符合的数据过滤掉
                res["data"].clear()
                res.pop("timestamp")
                res.pop("datatime")
            elif not select or flag:  # 未添加筛选条件，或添加筛选条件并找到内容符合的数据，返回
                client.close()
                return res
    client.close()
    return


if __name__ == '__main__':
    pass

    # print(get_oss_data_alarm("PS-NIO-ad1100b5-98123ce6", "714010", query_alarm=True))

    # print(get_oss_data_alarm("PS-NIO-ad1100b5-98123ce6", "722670", query_alarm=False))

    # print(get_oss_data_real_time("PS-NIO-ad1100b5-98123ce6", "1535"))

    # print(get_oss_data_real_time("PS-NIO-35014021-268699c2", "1001"))

    # print(get_oss_data_event("PS-NIO-35014021-268699c2", "800000", 1699325575853))

    print(get_oss_event_data("PS-NIO-35014021-268699c2", "800000", {'key': '107002', 'value': '10'}, 1701147849658))
