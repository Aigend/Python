#!/usr/bin/env python
# coding=utf-8

import redis
import json

from sshtunnel import SSHTunnelForwarder
from rediscluster import StrictRedisCluster
from utils.logger import logger
from config.settings import jump_machine_config_file


class RedisManager(object):
    def __init__(self, host=None, port=None, cluster_nodes: list = None, password=None, jump=None):
        """
        连接redis
        """
        try:
            if jump:
                ssh_config_file = jump_machine_config_file()
                if cluster_nodes:
                    # 首先打开一个tunnel用于startup_nodes寻找redis所有集群的ip
                    tunnels = [(i['host'], i['port']) for i in cluster_nodes]
                    ssh_tunnel = SSHTunnelForwarder(jump, ssh_config_file=ssh_config_file, remote_bind_addresses=tunnels)
                    ssh_tunnel.start()
                    cluster_nodes = [{'host': '127.0.0.1', 'port': i} for i in ssh_tunnel.local_bind_ports]
                    self.client = StrictRedisCluster(startup_nodes=cluster_nodes, skip_full_coverage_check=True,
                                                     nodemanager_follow_cluster=True, password=password)
                    # 取出收集到的集群node信息，保存在nodes和slots两个变量里，nodes是ip和port的对应信息，slots是key和nodes的对应信息
                    real_nodes = self.client.connection_pool.nodes.nodes
                    real_slots = self.client.connection_pool.nodes.slots
                    # 最后用取出的node信息再次开通tunnel用于取得对应key的value
                    tunnels = [(i['host'], i['port']) for i in real_nodes.values()]
                    ssh_tunnel2 = SSHTunnelForwarder(jump, ssh_config_file=ssh_config_file, remote_bind_addresses=tunnels)
                    ssh_tunnel2.start()
                    tunnel_bindings = {k[0]: v[1] for k, v in ssh_tunnel2.tunnel_bindings.items()}
                    # 使用binding的tunnel地址替换掉nodes和slots中的地址
                    cluster_nodes = {}
                    for port in ssh_tunnel2.local_bind_ports:
                        host = '127.0.0.1'
                        name = f'{host}:{port}'
                        cluster_nodes[name] = {'host': host, 'port': port, 'name': name, 'server_type': 'master'}
                    self.client.connection_pool.nodes.nodes = cluster_nodes
                    for slots in real_slots.values():
                        for slot in slots:
                            real_host = slot['host']
                            if real_host in tunnel_bindings:
                                slot['host'] = '127.0.0.1'
                                slot['port'] = tunnel_bindings[real_host]
                                slot['name'] = f'127.0.0.1:{tunnel_bindings[real_host]}'
                else:
                    ssh_tunnel = SSHTunnelForwarder(jump, ssh_config_file=ssh_config_file, remote_bind_address=(host, port))
                    ssh_tunnel.start()
                    pool = redis.ConnectionPool(host='127.0.0.1', port=ssh_tunnel.local_bind_port)
                    self.client = redis.Redis(connection_pool=pool)
            else:
                if cluster_nodes:
                    self.client = StrictRedisCluster(startup_nodes=cluster_nodes, skip_full_coverage_check=True,
                                                     nodemanager_follow_cluster=True, password=password)
                else:
                    pool = redis.ConnectionPool(host=host, port=port)
                    self.client = redis.Redis(connection_pool=pool)

        except Exception as e:
            logger.debug("Redis Error: %s" % e)

    def string_set(self, name, value, time=None):
        """
        参数：
             ex，过期时间（秒）
             px，过期时间（毫秒）
             nx，如果设置为True，则只有name不存在时，当前set操作才执行
             xx，如果设置为True，则只有name存在时，当前set操作才执行
        """
        try:
            result = self.client.set(name, value, time)
            # if result == True:
            #     return "set success!"
            # elif result == False:
            #     return "ser error!"
            return result
        except Exception as e:
            logger.debug("Redis Error: %s" % (e,))

    def keys(self, pattern):
        """
        获取key
        """
        try:
            if pattern == '*':
                return False
            result = self.client.keys(pattern)
            lis = [str(x, encoding='utf-8') for x in result]
            return lis
        except Exception as e:
            logger.debug("Redis Error: %s" % (e,))

    def get(self, key):
        """
        获取key的值
        """
        try:
            result = self.client.get(key)
            logger.debug(f"Redis get: {key}")
            logger.debug(f"Redis result: {result}")
            if result:
                return result.decode()
        except Exception as e:
            logger.debug("Redis Error: %s" % (e,))

    def delete(self, *key):
        """
        删除键值
        """
        try:
            tag = self.client.exists(*key)
            if tag:
                logger.debug(f"Redis delete: {key}")
                result = self.client.delete(*key)
                logger.debug(f"Redis result: {result}")
                return result
            else:
                return tag
        except Exception as e:
            logger.debug("Redis Error: %s" % (e,))

    def hash_set(self, name, key, value):
        """
        # 参数：
        # name，redis的name
        # key，name对应的hash中的key
        # value，name对应的hash中的value
        """
        try:
            result = self.client.hset(name, key, value)
            if result == True:
                return "set success!"
            elif result == False:
                return "set error!"
        except Exception as e:
            logger.debug("Redis Error: %s" % (e,))

    def hash_get_keys(self, name):
        """
        # 获取name对应的hash中所有的key的值
        """
        try:
            result = self.client.hkeys(name)
            return result

        except Exception as e:
            logger.debug("Redis Error: %s" % (e,))

    def hash_hget(self, name, key):
        """
        获取name下的key的值
        """
        try:
            result = self.client.hget(name, key)
            logger.debug(f"Redis hget: {name} {key}")
            logger.debug(f"Redis result: {result}")
            if result:
                return result.decode()
        except Exception as e:
            logger.debug("Redis Error: %s" % (e,))

    def get_sis_member(self, key_name, value):
        """
        获取name下的value是否存在，存在返回True否则返回False
        """
        try:
            result = self.client.sismember(key_name, value)
            logger.debug(f"Redis hget: {key_name} {value}")
            logger.debug(f"Redis result: {result}")
            return result
        except Exception as e:
            logger.debug("Redis Error: %s" % (e,))

    def hash_hdel(self, name, *keys):
        """
        # 将name对应的hash中指定key的键值对删除
        """
        try:
            result = self.client.hdel(name, *keys)
            if result:
                return "delete success!"
            else:
                return "delete error!"
        except Exception as e:
            logger.debug("Redis Error: %s" % (e,))

    def list_lpush(self, name, values):
        """
        # 在name对应的list中添加元素，每个新的元素都添加到列表的最左边

        # 如：
        # r.lpush('oo', 11,22,33)
        # 保存顺序为: 33,22,11
        """
        try:
            result = self.client.lpush(name, values)
            if result == True:
                return "push success!"
            elif result == False:
                return "push error!"
        except Exception as e:
            logger.debug("Redis Error: %s" % (e,))

    def list_lset(self, name, index, value):
        """
        # 对name对应的list中的某一个索引位置重新赋值
        # 参数：
            # name，redis的name
            # index，list的索引位置
            # value，要设置的值
        """
        try:
            result = self.client.lset(name, index, value)
            if result == True:
                return "set success!"
            elif result == False:
                return "set error!"
        except Exception as e:
            logger.debug("Redis Error: %s" % (e,))

    def list_lrem(self, name, value, num):
        """
        # 参数：
        # name，redis的name
        # value，要删除的值
        # num，  num=0，删除列表中所有的指定值；
        # num=2,从前到后，删除2个；
        # num=-2,从后向前，删除2个
        """
        try:
            result = self.client.lrem(name, value, num)
            if result == 1:
                return "del success!"
            elif result == 0:
                return "del error!"
        except Exception as e:
            logger.debug("Redis Error: %s" % (e,))

    def list_lindex(self, name, index):
        """
        #在name对应的列表中根据索引获取列表元素
        """
        try:
            result = self.client.lindex(name, index)
            return result
        except Exception as e:
            logger.debug("Redis Error: %s" % (e,))

    def set_sadd(self, name, value):
        """
        # name对应的集合中添加元素
        """
        try:
            result = self.client.sadd(name, value)
            if result == True:
                return "add success!"
            elif result == False:
                return "add error!"
        except Exception as e:
            logger.debug("Redis Error: %s" % (e,))

    def clean_redis(self):
        """
        清空redis
        :return:
        """
        self.client.flushdb()  # 清空 redis
        logger.debug('清空redis成功！')
        return 0

    def move(self, name, db):
        """
        将redis的某个值移动到指定的db下
        :return:
        """
        try:
            self.client.move(name, db)
        except Exception as e:
            logger.debug("Redis Error: %s" % (e,))

    def zset_zrange(self, name, start=0, end=-1):
        """
        # 获取name对应的zset中所有的key的值
        0 最小
        -1 代表最后一个
        """
        try:
            logger.debug(f"redis_zset:zrange {name} {start} {end}")
            result = self.client.zrange(name, start=start, end=end)
            logger.debug(f"zset result:{result}")
            return result
        except Exception as e:
            logger.debug("Redis Error: %s" % (e,))

    def hgetall(self, name):
        """
        """
        try:
            logger.debug(f"hgetall {name}")
            result = self.client.hgetall(name)
            logger.debug(f"hgetall result:{result}")
            return result
        except Exception as e:
            logger.debug("Redis Error: %s" % (e,))

    def publish(self, channel, value):
        """
        # 获取name对应的zset中所有的key的值
        0 最小
        -1 代表最后一个
        """
        try:
            # logger.debug(f"redis_zset:zrange {name} {start} {end}")
            result = self.client.publish(channel, value)
            logger.debug(f"zset result:{result}")
            return result
        except Exception as e:
            logger.debug("Redis Error: %s" % (e,))


if __name__ == '__main__':
    pass
    # RedisManager()
    # c = RedisManager('d-bj-cs-evmonitor-01.dsh08y.0001.cnn1.cache.amazonaws.com.cn', 6379)
    # pprint(c.keys('remote_vehicle_dev*'))
    # pprint(c.get('remote_vehicle_dev:vehicle_status:866c718a4b934275ab22d974637041b3:ExtremumData'))
    # pprint(msg['sample_time'])
    # pprint(c.delete('remote_vehicle_dev:vehicle_status:00013e63048b441eb24cd8c787a16af1:ExteriorStatus'))
    # pprint(c.string_set('1', '2'))
    # pprint(c.keys('1'))
    # pprint(c.get('1'))
    # print(c.String_Get('remote_vehicle_test:vehicle_status:3351c612c90a42dda68ffbde156fe863:ExteriorStatus'))
    # print(c.String_Set('2', '2'))
    # print(str(c.String_Delete('1')))
