#!/usr/bin/env python
# coding=utf-8

"""
:file: kafka_client.py
:author: chunming.liu
:contact: Chunming.liu@nextev.com
:Date: Created on 2016/12/29 下午1:37
:Description: 
"""
import time

from confluent_kafka.cimpl import Consumer, Producer, TopicPartition

try:
    from utils.logger import logger
except Exception:
    import logging

    logger = logging.getLogger(__name__)


class KafkaClient(object):
    def __init__(self, **kwargs):
        self.c = Consumer(**kwargs)
        self.p = Producer(**kwargs)
        self.loop = True

    def consume(self, topics, timeout=None):
        """

        :param topics: need to consumed kafka topic
        :param timeout: consume wait second
        :return:
        """
        self.c.subscribe([topics])

        if timeout is None:
            while self.loop:
                msg = self.c.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    print("Consumer error: {}".format(msg.error()))
                    continue
                # logger.debug('===={} {}'.format(msg.partition(), msg.offset()))
                yield msg.value()
        elif isinstance(timeout, int):
            deadline = time.time() + timeout
            while time.time() < deadline:
                # poll every second to consume messages
                msg = self.c.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    print("Consumer error: {}".format(msg.error()))
                    continue
                # logger.debug('===={} {}'.format(msg.partition(), msg.offset()))
                # logger.debug(f'{msg.value()}')
                yield msg.value()

        else:
            logger.error('Consume error')

    def stop(self):
        self.loop = False

    def produce(self, topic, value):
        self.p.produce(topic, value, callback=self.send_callback)
        self.p.poll(0)
        self.p.flush()

    @staticmethod
    def send_callback(err, msg):
        if err:
            logger.error("Fail:send fail cause:{0}".format(err))
        else:
            logger.debug("Successfully send to [{}], Data is:\n {}".format(msg.topic(), msg.value()))

    def set_offset_to_end(self, topic):
        # self.c.subscribe([topic])
        #
        # # 循环poll，直到可以得到topic的partition信息
        # while not self.c.assignment():
        #     msg = self.c.poll(1.0)
        #     self.c.commit()
        #
        # for index, topic_partition in enumerate(self.c.assignment()):

        # 在连续调用set_offset_to_end时，有几率会发生如下Error：
        # KafkaError{code=UNKNOWN_MEMBER_ID,val=25,str="Commit failed: Broker: Unknown member"}
        # 暂时还没发现问题原因在哪里，尝试更换一种方式来获取topic partition信息，尽量减少显示的subscribe，poll和commit
        # 参考https://stackoverflow.com/questions/62115122/how-to-programmatically-get-latest-offset-per-kafka-topic-partition-in-python
        # 暂时保留了之前的获取方式，如果无效或造成了别的问题，再换回之前的获取方式
        topics = self.c.list_topics(topic=topic)
        partitions = self.c.committed([TopicPartition(topic, partition) for partition in list(topics.topics[topic].partitions.keys())])
        tp_news = []
        for index, topic_partition in enumerate(partitions):
            # 获取offset最大最小值
            watermark_offsets = self.c.get_watermark_offsets(topic_partition)
            logger.debug('watermark_offsets {}'.format(watermark_offsets))

            # 直接将offset置为logsize,跳过未消费的数据
            logsize = watermark_offsets[1]
            if logsize > topic_partition.offset:
                tp_news.append(TopicPartition(topic, index, int(logsize)))
        if len(tp_news) > 0:
            try:
                self.c.commit(offsets=tp_news, asynchronous=False)
            except Exception as e:
                logger.warning(e)


if __name__ == '__main__':
    import os
    import yaml
    import sys
    import zlib
    import importlib

    base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../')
    sys.path.append(base_dir)
    from nio_messages.nextev_msg import parse_nextev_message

    from nio_messages.pb2 import light_change_msg_pb2, charge_start_msg_pb2, alarm_signal_update_msg_pb2

    config_path = '{0}/config/{1}/{1}_config.yml'.format(base_dir, 'stg')
    with open(config_path) as f:
        env_config = yaml.load(f, Loader=yaml.FullLoader)

    # ## comn kafka
    # configs = env_config['kafka']['comn']
    # configs['bootstrap.servers'] = ','.join(configs['bootstrap.servers'])
    # configs['group.id'] = 'liliu_group'
    # configs.pop('topics')
    #
    # # topic = 'swc-cvs-tsp-test-80001-ecall'
    # # topic = 'swc-cvs-tsp-test-80001-power_swap'
    # topic = 'swc-tsp-data_collection-test-vehicle_data'
    # # topic = 'swc-cvs-tsp-test-80001-wti_can_signal'
    #
    # client = KafkaClient(**configs)
    # print('listening on {0}'.format(configs))
    # print('topic: {0}'.format(topic))
    # client.set_offset_to_end(topic)
    # for data in client.consume(topic):
    #     # 非proto数据
    #     print(data)

    ### cvs kafka
    configs = env_config['kafka']['comn']
    configs['bootstrap.servers'] = ','.join(configs['bootstrap.servers'])
    configs['group.id'] = 'liliu_group'
    configs.pop('topics')

    topic = 'swc-cvs-tsp-stg-80001-usual_place'

    # topic = 'swc-tsp-data_report-test-evm_log'
    client = KafkaClient(**configs)
    print('listening on {0}'.format(configs))
    print('topic: {0}'.format(topic))

    client.set_offset_to_end(topic)
    for data in client.consume(topic):
        # # 非proto数据
        print(type(data))
        print(data)
        # print(f'len {len(data)}  {repr(data)}')

        # # proto 数据
        # msg = parse_nextev_message(data)
        # # print(msg)
        #
        # #
        # event_name = msg['sub_type']
        # #
        # if event_name == 'light_change_event':
        #     event = light_change_msg_pb2.LightChangeEvent()
        #
        #     vehicle_status = event.FromString(zlib.decompress(msg['params']['vehicle_status']))
        #     print('====', msg)
        #     b = str(vehicle_status)
        #     print('b', repr(b))
        #
        # if event_name == 'alarm_signal_update_event':
        #     event = alarm_signal_update_msg_pb2.AlarmSignalUpdateEvent()
        #
        #     vehicle_status = event.FromString(zlib.decompress(msg['params']['vehicle_status']))
        #     # print('====', msg)
        #
        # if event_name == 'charge_start_event':
        #     print('====', msg)
        #     event = charge_start_msg_pb2.ChargeStartEvent()
        #     vehicle_status = event.FromString(zlib.decompress(msg['params']['vehicle_status']))
        #
        #     b = str(vehicle_status)
        #     print('b', repr(b))

    # ### qc kafka
    # configs = env_config['kafka']['qc']
    # configs['bootstrap.servers'] = ','.join(configs['bootstrap.servers'])
    # configs['group.id'] = 'liliu_group'
    # configs.pop('topics')
    #
    # topic = 'swc-tsp-data_collection-prod-vehicle_data'
    # # topic = 'swc-cvs-tsp-prod-80001-ecall'
    # # topic = 'swc-cvs-tsp-prod-80001-power_swap'
    # # topic = 'swc-cvs-tsp-prod-80001-wti_can_signal'
    #
    #
    #
    # client = KafkaClient(**configs)
    # print('listening on {0}'.format(configs))
    # print('topic: {0}'.format(topic))
    #
    # client.set_offset_to_end(topic)
    # for data in client.consume(topic):
    #     # # 非proto数据
    #
    #     print(data)
    #
    #     # # # proto 数据
    #     # msg = parse_nextev_message(data)
    #     # print(msg)

    # ## adas kafka
    # from nio_messages.pb2 import adas_header_pb2, feature_status_update_pb2
    # configs = env_config['kafka']['adas']
    # configs['bootstrap.servers'] = ','.join(configs['bootstrap.servers'])
    # configs['group.id'] = 'liliu_group'
    # configs.pop('topics')
    #
    # # topic = 'swc-cvs-tsp-test-80001-ecall'
    # # topic = 'swc-cvs-tsp-test-80001-power_swap'
    # # topic = 'swc-adas-nmp-test_tsp-10107-data_report'
    # topic = 'swc-adas-nmp-stg_tsp-10107-data_report'
    # # topic = 'swc-cvs-tsp-test-80001-wti_can_signal'
    #
    # client = KafkaClient(**configs)
    # print('listening on {0}'.format(configs))
    # print('topic: {0}'.format(topic))
    # client.set_offset_to_end(topic)
    # for data in client.consume(topic):
    #     # # 非proto数据
    #     # print(data)
    #
    #     # # proto 数据
    #     msg = parse_nextev_message(data)
    #     print(msg)
    #
    #     event_name = msg['sub_type']
    #
    #
    #     if event_name == 'FeatureStatusUpdate':
    #         if 'AdasHeader' in msg['params'] and 'FeatureStatusUpdate' in msg['params']:
    #             print('====\n', msg)
    #             event_header = adas_header_pb2.AdasHeader()
    #
    #             AdasHeader = event_header.FromString(msg['params']['AdasHeader'])
    #             print('AdasHeader:\n', AdasHeader)
    #
    #
    #             event_status_update = feature_status_update_pb2.FeatureStatusUpdate()
    #             FeatureStatusUpdate = event_status_update.FromString(msg['params']['FeatureStatusUpdate'])
    #             # FeatureStatusUpdate = event_status.FromString(zlib.decompress(msg['params']['FeatureStatusUpdate']))
    #             print('FeatureStatusUpdate:\n', FeatureStatusUpdate)
    #         #
    #         # elif 'FeatureStatusUpdate' in msg['params']:
    #         #
    #         #     print('****\n', msg)
    #         #
    #         #     aa = feature_status_pb2.FeatureStatus()
    #         #     bb = aa.FromString()
    #         #     print('FeatureStatusUpdate:\n', bb)
