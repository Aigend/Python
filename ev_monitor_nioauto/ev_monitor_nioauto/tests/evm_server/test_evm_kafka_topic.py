#!/usr/bin/env python
# coding=utf-8

import pytest


class TestEVMKafkaTopic(object):
    @pytest.mark.skip('manual')
    def test_evm_kafka_topic(self):
        """
        evm_server具有持久化Cassandra和向政府平台report两个任务

        1.evm_server持久化Cassandra的相关线程的Kafka topic为swc-tsp-evm-{env}-evm_msg

        2.evm_server向政府平台上报时的Kafka topic为以下
        国家平台：swc-tsp-evm-{env}-evm_msg_156
        北京平台：swc-tsp-evm-{env}-evm_msg_110000
        上海平台：swc-tsp-evm-{env}-evm_msg_310000
        其余的地方平台：swc-tsp-evm-{env}-evm_msg_area

        比如一个北京的车，evm_server会把车辆上报的信息交给三个Kafka，分别为
        swc-tsp-evm-{env}-evm_msg_156以上报国家平台
        swc-tsp-evm-{env}-evm_msg_110000以上报北京平台
        swc-tsp-evm-{env}-evm_msg以进行Cassandra持久化

        持久化和report并没有先后顺序，report政府平台之后，若返回了ack，evm_server会将返回信息发给swc-tsp-evm-{env}-evm_msg
        持久化任务消费该topic，对Cassandra进行update操作。

        """

        pass
