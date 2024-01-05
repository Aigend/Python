# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/1/28 16:16
# @File: oss_utils.py
import pymongo
from oss.southbound.device2cloud import PowerDevice_pb2


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
                # log.error(str(data.value_string))
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


def get_oss_data_alarm(resource_id,
                       target_key,
                       query_alarm, ):
    res = {
        "key": target_key,
        'type': -1,
        'value': -1
    }
    try:
        client = pymongo.MongoClient(host='10.112.12.153', port=27017, username="opman", password="N7102io")
        collection = client[resource_id]['alarm']
    except Exception as e:
        # log.error(f"<OSS>:connect mongodb error, {traceback.format_exc()}")
        res['message'] = f"connect mongodb error, {e}"
        return res
    for data in collection.find().sort("timestamp", -1):
        try:
            pow_msg = PowerDevice_pb2.PowerDeviceMessage()
            pow_msg.ParseFromString(data["value"])
        except Exception as e:
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


def get_oss_data_real_time(resource_id: str, target_key: str) -> dict:
    res = {
        "key": target_key,
        'type': -1,
        'value': -1
    }
    try:
        client = pymongo.MongoClient(host='10.112.12.153', port=27017, username="opman", password="N7102io")
        collection = client[resource_id]['realtime']
    except Exception as e:
        # log.error(f"<OSS>:connect mongodb error, {traceback.format_exc()}")
        res['message'] = f"connect mongodb error, {e}"
        return res
    for data in collection.find().sort("timestamp", -1):
        try:
            pow_msg = PowerDevice_pb2.PowerDeviceMessage()
            pow_msg.ParseFromString(data["value"])
            # if data['topic'] == "PE-staging-power-device_basic":
            #     log.info(data['topic'])
            #     log.info(pow_msg.basic.data)
        except Exception as e:
            # log.error(f"<OSS>:parse real_time pb data error, {e}")
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


def get_oss_data_event(resource_id: str, target_key: str):
    """

    :param resource_id: 站ID
    :param target_key: 换电事件ID
    :return:
    """
    res = {
        "event_id": target_key,
        "timestamp": 0,
        "data": []
    }
    try:
        client = pymongo.MongoClient(host='10.112.12.153', port=27017, username="opman", password="N7102io")
        # collection = client["PS-NIO-ALL_DATA"]['alldata']
        collection = client[resource_id]['event']
    except Exception as e:
        # log.error(f"<OSS>:connect mongodb error, {traceback.format_exc()}")
        res['message'] = f"connect mongodb error, {e}"
        return res
    for data in collection.find().sort("timestamp", -1):
    # for data in collection.find({"topic": "PE-staging-power-device_event"}).sort("timestamp", 1):
        try:
            pow_msg = PowerDevice_pb2.PowerDeviceMessage()
            pow_msg.ParseFromString(data["value"])
        except Exception as e:
            # log.error(f"<OSS>:parse event pb data error, {e}")
            continue
        if pow_msg.event and pow_msg.event.event_id == target_key:
            res["timestamp"] = pow_msg.event.timestamp
            for d in pow_msg.event.data:
                tmp = {}
                for des, val in d.ListFields():
                    if des.__dict__.get("name") == "value_string" and isinstance(val, bytes):
                        val = val.decode()
                    tmp[des.__dict__.get("name")] = val
                res["data"].append(tmp)
            client.close()
            return res
    client.close()
    return


if __name__ == '__main__':
    pass

    # print(get_oss_data_alarm("PS-NIO-ad1100b5-98123ce6", "714010", query_alarm=True))
    print(get_oss_data_alarm("PS-NIO-ad1100b5-98123ce6", "722670", query_alarm=False))

    # print(get_oss_data_real_time("PS-NIO-ad1100b5-98123ce6", "1535"))

    # print(get_oss_data_real_time("PS-NIO-35014021-268699c2", "1001"))
