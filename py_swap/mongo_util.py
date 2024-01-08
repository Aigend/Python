#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/16 16:07
# @Author  : wenlong.jin@nio.com
# @File    : utils.py
# @Software: ps20
import time

import pymongo

from log_util import log
from oss.southbound.device2cloud import PowerDevice_pb2

databases = ['PS-NIO-ALL_DATA', 'PS-NIO-ad1100b5-98123ce6', 'PS-NIO-35014021-268699c2', 'PS-NIO-3e8d86f7-59924bcf']
collections = ['event', 'basic', 'realtime', 'alarm', 'alarm', 'response', 'configuration']


class MongodbUtil:

    def __init__(self, host='10.112.12.153', port=27017, username="opman", password="N7102io"):
        self.client = None
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def init(self):
        try:
            self.connect()
            for database in databases:
                for collection in collections:
                    if database == "PS-NIO-ALL_DATA":
                        collection = "alldata"
                        expire_time = 60 * 60 * 48
                    else:
                        # expire_time = 120 if collection == "realtime" else 1800
                        if collection == "realtime":
                            expire_time = 120
                        elif collection == "event":
                            expire_time = 60 * 60 * 24
                        else:
                            expire_time = 1800
                    self.client[database][collection].drop_indexes()
                    self.client[database][collection].create_index([("timestamp", pymongo.DESCENDING)],
                                                                   name="timestamp", )
                    self.client[database][collection].create_index(
                        [("expire_at", pymongo.DESCENDING)],
                        name="expire_at",
                        expireAfterSeconds=expire_time)
                    if database == "PS-NIO-ALL_DATA":
                        break
        except Exception as e:
            log.error(f"create mongodb collecation happen error, {e}")
            time.sleep(10)
            raise e

    def connect(self):
        self.client = pymongo.MongoClient(host=self.host, port=self.port, username=self.username,
                                          password=self.password)

    def re_connect(self):
        self.client = pymongo.MongoClient(host=self.host, port=self.port, username=self.username,
                                          password=self.password)

    def get_client(self):
        if not isinstance(self.client, pymongo.MongoClient):
            self.connect()
        return self.client

    def insert_one(self, database, collection, data):
        try:
            self.client[database][collection].insert_one(data)
        except Exception as e:
            log.error(f"database {database}, collection {collection}, insert data happen error: {e}")

    def insert_many(self, database, collection, data):
        try:
            self.client[database][collection].insert_many(data)
        except Exception as e:
            log.error(f"database {database}, collection {collection}, insert data happen error: {e}")

    def get_value(self, data):
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

    def parse_msg_event(self, database, collection):
        # PS-NIO-ad1100b5-98123ce6
        # PS-NIO-35014021-268699c2
        for data in self.client[database][collection].find(
                {"topic": "PE-staging-power-device_event"}).sort("timestamp",
                                                                                                           -1):
        # for data in self.client[database][collection].find(
        #         {"topic": "PE-staging-power-device_event", "account_id": "PS-NIO-ad1100b5-98123ce6"}).sort("timestamp", -1):
            try:
                pow_msg = PowerDevice_pb2.PowerDeviceMessage()
                pow_msg.ParseFromString(data["value"])
                ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(pow_msg.event.timestamp / 1000)))
                # print(pow_msg.event.event_id, ts)
                if len(pow_msg.event.event_id) > 0 and pow_msg.event.event_id in ["800000", "800001", "800002"]:
                # if len(pow_msg.event.event_id) > 0 and pow_msg.event.event_id in ["800001",]:
                    # print(type(pow_msg.event.event_id), pow_msg.event.event_id)  # str
                    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(pow_msg.event.timestamp / 1000)))
                    print(pow_msg.event.event_id, ts, pow_msg.event.timestamp)
                    # log.info(f"{pow_msg.event.event_id}, {ts}, {pow_msg.event.timestamp},{pow_msg.event.data}")
                    # break
                    # print(pow_msg.event.data)
                    # for d in pow_msg.event.data:
                    #     print(d)
            except Exception as e:
                continue
        self.client.close()

    def parse_msg_realtime(self, database, collection):
        for data in self.client[database][collection].find().sort("timestamp", -1):
            try:
                pow_msg = PowerDevice_pb2.PowerDeviceMessage()
                pow_msg.ParseFromString(data["value"])
                log.info("power device message parse success")
                for realtime_data in pow_msg.realtime.data:
                    res = self.get_value(realtime_data)
                    print(realtime_data.key, realtime_data.type, res['value'])
            except Exception as e:
                print(e)
                continue
        self.client.close()

    def parse_msg_alarm(self, database, collection):
        for data in self.client[database][collection].find().sort("timestamp", -1):
            try:
                pow_msg = PowerDevice_pb2.PowerDeviceMessage()
                pow_msg.ParseFromString(data["value"])
                print("power device message parse success")
                for alarm_data in pow_msg.alarm.alarm:
                    print(alarm_data)
            except Exception as e:
                print(e)
                continue
        self.client.close()

    def parse_msg_all_data_alarm(self, database, collection):
        doc = self.client[database][collection].find(
            {"topic": "PE-staging-power-device_alarm", "account_id": "PS-NIO-ad1100b5-98123ce6"})
        for data in doc.sort("timestamp", -1):
            try:
                pow_msg = PowerDevice_pb2.PowerDeviceMessage()
                pow_msg.ParseFromString(data["value"])
                print("power device message parse success")
                for alarm_data in pow_msg.alarm.alarm:
                    print(alarm_data)
            except Exception as e:
                print(e)
                continue
        self.client.close()


if __name__ == '__main__':
    pass
    mongo_util = MongodbUtil()
    mongo_util.connect()
    # mongo_util.parse_msg_event('PS-NIO-ALL_DATA', 'alldata')
    # mongo_util.parse_msg_event('PS-NIO-35014021-268699c2', 'event')
    # mongo_util.parse_msg_all_data_alarm('PS-NIO-ALL_DATA', 'alldata')

    # mongo_util.parse_msg_realtime('PS-NIO-ad1100b5-98123ce6', 'realtime')
    # mongo_util.parse_msg_alarm('PS-NIO-ad1100b5-98123ce6', 'alarm')

    # mongo_util.parse_msg_event('PS-NIO-ALL_DATA', 'alldata')

    mongo_util.parse_msg_event('PS-NIO-35014021-268699c2', 'event')

