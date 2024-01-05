#!/usr/bin/env python
# coding=utf-8
import copy
from operator import mod
import time

import yaml

from utils.cassandra_client import CassandraManager
from utils.kafka_client import KafkaClient
from utils.logger import logger
from utils.mongodb_client import MongodbManager
from utils.mysql_client import MysqlManager
from base_dir import base_dir
from utils.redis_client import RedisManager
from utils.s3_client import S3Manager


class LazyProperty(object):
    # 使得属性只初始化一次，而@perperty装饰符每次都初始化属性
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value


def singleton(cls):
    def _singleton(*args, **kwargs):
        instance = cls(*args, **kwargs)
        instance.__call__ = lambda: instance
        return instance

    return _singleton


@singleton
class DB(object):
    def __init__(self, cmdopt):
        config_path = '{0}/config/{1}/{1}_config.yml'.format(base_dir, cmdopt)
        with open(config_path, mode="r", encoding="utf-8") as f:
            self.env = yaml.load(f, Loader=yaml.FullLoader)

    # def __del__(self):
    #     for k, v in self.kafka.items():
    #         if k != 'topics':
    #             self.kafka[k].stop()
    #             self.kafka[k].c.close()
    #
    #     for k, v in self.mysql.items():
    #         self.mysql[k].close()

    @LazyProperty
    def mysql(self):
        mysql_dict = dict()
        try:
            for k, v in self.env.get('mysql', {}).items():
                mysql_dict[k] = MysqlManager(**v)
        except Exception as e:
            logger.error(e)
            raise ConnectionError(e)

        return mysql_dict

    @LazyProperty
    def cassandra(self):
        cass_dict = dict()
        try:
            for k, v in self.env.get('cassandra', {}).items():
                cass_dict[k] = CassandraManager(**v)
        except Exception as e:
            logger.error(e)
            raise ConnectionError(e)

        return cass_dict

    @LazyProperty
    def mongodb(self):
        mongodb_dict = dict()
        try:
            for k, v in self.env.get('mongodb', {}).items():
                mongodb_dict[k] = MongodbManager(**v)
        except Exception as e:
            logger.debug(e)
            raise ConnectionError(e)

        return mongodb_dict

    @LazyProperty
    def redis(self):
        redis_dict = dict()
        try:
            for k, v in self.env.get('redis', {}).items():
                if isinstance(v, dict):
                    host = v.get('host', None)
                    port = v.get('port', None)
                    nodes = v.get('nodes', None)
                    password = v.get('password', None)
                    jump = v.get('jump_machine', None)
                    redis_dict[k] = RedisManager(host=host, port=port, cluster_nodes=nodes, password=password, jump=jump)
        except Exception as e:
            logger.error(e)
            raise ConnectionError(e)

        return redis_dict

    @LazyProperty
    def kafka(self):
        kafka_dict = dict()
        kafka_dict['topics'] = {}
        conf = copy.deepcopy(self.env.get('kafka', {}))
        try:
            for k, v in conf.items():
                v['bootstrap.servers'] = ','.join(v['bootstrap.servers'])
                kafka_dict['topics'].update(v.pop('topics'))
                kafka_dict[k] = KafkaClient(**v)

        except Exception as e:
            logger.error(e)
            raise ConnectionError(e)

        return kafka_dict

    @LazyProperty
    def s3(self):
        s3_dict = dict()
        try:
            for k, v in self.env.get('s3', {}).items():
                s3_dict[k] = S3Manager(v['aws_access_key_id'],
                                       v['aws_secret_access_key'],
                                       v['region_name'],
                                       v['bucket'])
        except Exception as e:
            logger.error(e)

        return s3_dict
