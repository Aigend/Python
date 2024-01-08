import time
from datetime import datetime as da

import pytz
from kafka import KafkaConsumer

from log_util import log
from mongo_util import MongodbUtil
from mongo_util import databases
from oss import message_pb2
from oss.southbound.device2cloud import PowerDevice_pb2

log.info("### begin to init mongodb client ###")
mongo_util = MongodbUtil()
mongo_util.init()
log.info("*** begin to consume kafka data ***")
stations = set(databases[1:])
topics = [
    'PE-staging-power-device_event',
    'PE-staging-power-device_basic',
    'PE-staging-power-device_realtime',
    'PE-staging-power-device_alarm',
    'PE-staging-power-device_response',
    'PE-staging-power-device_configuration',
]

servers = ["pe-kafka-01-stg.nioint.com:9092", "pe-kafka-02-stg.nioint.com:9092", "pe-kafka-03-stg.nioint.com:9092"]
username = "kmbmanXC"
password = "ZsbEYEDwGjPNwmKG"

consumer = KafkaConsumer(
    group_id='test_group_50',
    bootstrap_servers=servers,
    auto_offset_reset='latest',  # 重置偏移量，earliest移到最早的可用消息，latest最新的消息，默认为latest
    enable_auto_commit=True,  # 每过一段时间自动提交所有已消费的消息（在迭代时提交）
    auto_commit_interval_ms=5000,  # 自动提交的周期（毫秒）
    sasl_mechanism="PLAIN",
    security_protocol='SASL_PLAINTEXT',
    sasl_plain_username=username,
    sasl_plain_password=password,
    api_version=(2, 0, 2))
consumer.subscribe(topics=topics)  # #订阅要消费的主题
try:
    count = 0
    tmp = []
    for message in consumer:
        try:
            msg = message_pb2.Message()
            msg.ParseFromString(message.value)
            log.info(f"consuming--->>>server_msg_id:{msg.server_msg_id}, {msg.sub_type}")
            if msg.sub_type != "oss_scanario_1":
                continue
            account_id = ""
            value = ""
            for param in msg.params:
                if param.key == "account_id":
                    if param.value.decode() not in stations:
                        break
                    account_id = param.value.decode()
                elif param.key == "PowerDeviceMessage":  # 三代站由PowerSwapMessage变成PowerDeviceMessage
                    value = param.value
            if account_id and value:
                count += 1
                p = PowerDevice_pb2.PowerDeviceMessage()
                p.ParseFromString(value)
                ts = time.time()
                expire_at = da.fromtimestamp(ts, tz=pytz.timezone('Asia/Shanghai'))
                # consume_ts = expire_at.strftime('%Y-%m-%d %H:%M:%S.%f')
                log.info(
                    f"msg_topic:{message.topic}, device_id:{p.device_id}, device_timestamp:{p.timestamp}, server_receive_ts: {msg.server_receive_ts}, server_publish_ts:{msg.server_publish_ts}, consume_ts:{int(ts*1000)}")
                data = {
                    "server_msg_id": msg.server_msg_id,
                    "timestamp": p.timestamp,
                    # "message_time": da.fromtimestamp(p.timestamp / 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f'),
                    "server_receive_ts": msg.server_receive_ts,
                    "server_publish_ts": msg.server_publish_ts,
                    "topic": message.topic,
                    "account_id": account_id,
                    "value": value,
                    'expire_at': expire_at
                }
                tmp.append(data)
                ty = message.topic.split("_")[-1]
                mongo_util.insert_one(p.device_id, ty, data)
                log.info("data deal success, begin to consumer next data")
                if count == 100:
                    count = 0
                else:
                    continue
                mongo_util.insert_many('PS-NIO-ALL_DATA', 'alldata', tmp)
                tmp.clear()
                log.info("insert 100 consume message to PS-NIO-ALL_DATA.alldata collection success")
        except Exception as e:
            log.error(f"main func happen error, {e}")
except Exception as e:
    log.error(e)
