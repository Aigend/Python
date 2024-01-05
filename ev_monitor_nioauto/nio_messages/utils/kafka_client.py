#!/usr/bin/env python
# coding=utf-8

"""
:file: kafka_client.py
:author: chunming.liu
:contact: Chunming.liu@nextev.com
:Date: Created on 2016/12/29 下午1:37
:Description:
"""

from confluent_kafka.cimpl import Producer
import logging


class KafkaProduct(object):
    def __init__(self):
        self.configs = {
            'auto.offset.reset': 'latest',
            'sasl.mechanisms': 'PLAIN',
            'security.protocol': 'sasl_plaintext',
        }
        self.sender = None

    @staticmethod
    def send_callback(err, msg):
        if err:
            logging.error("Fail:send fail cause:{0}".format(err))
        else:
            logging.info("Success:[{}] send success to [{}]".format(msg.value(), msg.topic()))

    def product(self, cluster):
        self.configs.update(cluster)
        self.sender = Producer(**self.configs)

    def send(self, topic, value=None, key=None):
        print("[{0}] send: {1}".format(topic, value))
        self.sender.produce(topic, value, callback=self.send_callback)
        self.sender.poll(0)
        self.sender.flush()
