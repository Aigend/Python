#!/usr/bin/env python
# coding=utf-8

"""
:file: cassandra_client.py.py
:author: chunming.liu
:contact: Chunming.liu@nextev.com
:Date: Created on 2016/12/27 下午6:32
:Description: 
"""

import json
import traceback

from utils.logger import logger
from utils.commonlib import show_json
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from sshtunnel import SSHTunnelForwarder
from config.settings import jump_machine_config_file


class CassandraManager(object):
    def __init__(self, nodes, keyspace, port, user, password, jump_machine=None):
        try:
            if jump_machine:
                tunnel_nodes = [(i, port) for i in nodes]
                ssh_config_file = jump_machine_config_file()
                ssh_tunnel = SSHTunnelForwarder(jump_machine, ssh_config_file=ssh_config_file, remote_bind_addresses=tunnel_nodes)
                ssh_tunnel.start()
                connect_nodes = ssh_tunnel.local_bind_addresses
            else:
                connect_nodes = nodes
            auth_provider = PlainTextAuthProvider(username=user, password=password)
            cluster = Cluster(connect_nodes, port=port, auth_provider=auth_provider)
            self.session = cluster.connect(keyspace=keyspace)
        except Exception as e:
            print("Cassandra Error: %s" % (e,))

    def fetch(self, table, where_model: dict, fields: list = None, order_by: str = None):
        """
        从Cassandra中查询记录
        :param table:被查询表
        :param where_model: 查询条件
        :param fields:，查询的字段，可为整型或字符串，默认查询全部字段
        :param order_by:排序
        :return:查询获得的数据，json格式的列表
        """
        logger.debug('table: {}'.format(table))
        logger.debug('where_model: {}'.format(where_model))

        try:
            if fields is None:
                fields = '*'

            where = ''
            for k, v in where_model.items():
                # k could be like 'sample_ts' or include operator like 'sample_ts>'
                symbol = '='
                for i in ['>=', '<=', '!=', '>', '<', ' in']:
                    if i in k:
                        symbol = i
                        k = k.split(symbol)[0]
                        break

                if isinstance(v, int):
                    where += "{0}{1}{2}".format(k, symbol, v) + " and "
                elif isinstance(v, str):
                    where += "{0}{1}'{2}'".format(k, symbol, v) + " and "
                elif isinstance(v, list):
                    where += "{0}{1} {2}".format(k, symbol, tuple(v)) + " and "
            if order_by:
                if 'desc' in order_by or 'DESC' in order_by or 'asc' in order_by or 'ASC' in order_by:
                    sql = "select JSON %s from %s where %s order by %s allow filtering;" % (
                        ",".join(fields), table, where[:-4], order_by)
                else:
                    # default desc
                    sql = "select JSON %s from %s where %s order by %s desc allow filtering;" % (
                        ",".join(fields), table, where[:-4], order_by)
            else:
                sql = "select JSON %s from %s where %s allow filtering;" % (",".join(fields), table, where[:-4])
            logger.debug('Cassandra cql: {}'.format(sql))
            rows = self.session.execute(sql, timeout=10.0)
            result = []
            if rows:
                for item in rows:
                    result.append(json.loads(item.json))
            logger.debug('Cassandra [{0}]中{1}字段的数据是:\n{2}'.format(table, fields, show_json(result)))
            return result

        except Exception as e:
            print("Cassandra Error %s: " % (e,))

    def insert(self, table, model: dict):
        """
        insert data into table
        :param model: <dict> key与数据库field一致
        :param table: table name
        :return: The result of insert cql execute
        """

        fields, values = [], []
        for k, v in model.items():
            fields.append(k)
            if isinstance(v, int):
                values.append("%s" % v)
            elif isinstance(v, str) and not v.startswith('{') and not v.startswith('['):
                values.append("'%s'" % v)
            else:
                values.append("%s" % v)
                # values.append("%s" % v)
        sql = "insert into %s (%s) values (%s)" % (table, ",".join(fields), ",".join(values))
        try:
            logger.debug('Cassandra cql: {}'.format(sql))
            result = self.session.execute(sql)
            return result

        except Exception as e:
            # self.close()
            logger.error(traceback.format_exc())


if __name__ == '__main__':
    cassandra = CassandraManager(['10.125.232.151', '10.125.232.153', '10.125.232.152'],
                                 'data_collection_test',
                                 port=9042,
                                 user='data_collection_test_r',
                                 password='qjxkiPpuYnpsJEBLT9sDykwK'
                                 )
    cassandra.fetch('vehicle_data',
                    {'vehicle_id': '84d3457edb0a4bad8f76607f880cb2be',
                     # 'sample_date': '2018-09',
                     # 'tag': 'did_tag1537498475',
                     # 'ecu': 'CGW'
                     'sample_ts': 1547448304810
                     },
                    ['vehicle_id']
                    )
