#!/usr/bin/env python
# coding=utf-8

"""
:file: mysql_tool.py <br/>
:author: zhiqiang.zhu <br/>
:contact: zhiqiang.zhu@nio.com <br/>
:Date: Created on 2018/2/7 下午6:24 <br/>
:Feature: 定义查询操作mysql数据库的方法<br/>
"""
import time
import traceback

import pymysql
from decimal import Decimal
import datetime

from sqlalchemy import create_engine
from sshtunnel import SSHTunnelForwarder

from utils.logger import logger
from config.settings import BASE_DIR, jump_machine_config_file


def jump_machine_mysql(host, port, user, password, database, sql, **kwargs):
    """
    vi ~/.ssh/config
        Host jump
        HostName 10.128.245.27
        User li.liu2
        Port 2222
        ForwardAgent yes
        ProxyCommand /usr/local/bin/ncat --idle-timeout 10h --proxy proxy.nioint.com:8080 --proxy-type http %h %p
        IdentityFile /Users/li.liu2/.ssh/li.liu2.private_key

    """
    with SSHTunnelForwarder("jump", remote_bind_address=(host, port), ) as tunnel:
        connection_string = 'mysql+pymysql://' + user + ':' + password + '@' + '127.0.0.1' + ':' + str(tunnel.local_bind_port) + '/' + database

        engine = create_engine(connection_string)
        connection = engine.connect()
        result = connection.execute(sql)

        connection.close()

    return result


class MysqlManager(object):
    def __init__(self, **kwargs):
        try:
            self.retry_num = kwargs.pop('retry_num') if 'retry_num' in kwargs.keys() else 0
            if 'jump_machine' in kwargs.keys():
                logger.debug(f"Start SSHTunnel:{kwargs}")
                jump_machine_name = kwargs.pop('jump_machine')
                new_path = jump_machine_config_file()
                host, port = kwargs['host'], kwargs['port']
                self.server = SSHTunnelForwarder(jump_machine_name, ssh_config_file=new_path, remote_bind_address=(host, port))
                self.server.start()
                logger.debug(f"SSHTunnel:{self.server.local_bind_address} bind to {host}:{port}")
                kwargs['host'], kwargs['port'] = '127.0.0.1', self.server.local_bind_port
            else:
                self.server = ''
            self.connection = pymysql.connect(**kwargs)
            self.cursor = self.connection.cursor(cursor=pymysql.cursors.DictCursor)
        except pymysql.Error as e:
            logger.error(traceback.format_exc())
            logger.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def fetch(self, table, where_model, fields=None, exclude_fields=None, order_by: str = None, suffix: str = None, retry_num=0):
        """
        :param table:表名
        :param where_model:查询条件，字典格式
        :param fields:查询的字段，默认查询全部字段
        :param exclude_files: 排除字段
        :order_by: 排序 desc或者asc
        :return:查询获得的数据
        """
        self.connection.ping(reconnect=True)
        if retry_num == 0:
            retry_num = self.retry_num
        if exclude_fields is None:
            exclude_fields = []
        try:
            if fields is None:
                fields = "*"
            where = ''
            for k, v in where_model.items():
                # k could be like 'sample_ts' or include operator like 'sample_ts>'
                symbol = '='
                for i in ['>=', '<=', '!=', '>', '<', ' in', ' like']:
                    if i in k:
                        symbol = i
                        k = k.split(symbol)[0]
                        break

                if isinstance(v, int):
                    where += "`{0}`{1}{2}".format(k, symbol, v) + " and "
                elif isinstance(v, str):
                    where += "`{0}`{1}'{2}'".format(k, symbol, pymysql.escape_string(v)) + " and "
                elif isinstance(v, list):
                    in_str = str(v).replace('[', '(').replace(']', ')')
                    where += "`{0}`{1} {2}".format(k, symbol, in_str) + " and "
            if order_by:
                order_by = ','.join(
                    [f"{item[0]} {' '.join(item[1:])}" if item[0].upper() == 'NULL' else f"`{item[0]}` {' '.join(item[1:])}" for item in
                     [item.strip().split() for item in order_by.split(',')]])
                sql = "select %s from `%s` where %s order by %s" % (",".join(fields), table, where[:-4], order_by)
            else:
                sql = "select %s from `%s` where %s" % (",".join(fields), table, where[:-4])
            if suffix:
                sql = sql + " " + suffix
            logger.info(sql)
            if retry_num > 0:
                i = 0
                while retry_num > 0:
                    self.cursor.execute(sql)
                    data = _format(self.cursor.fetchall())
                    i += 1
                    if data:
                        logger.debug(f'查询第{i}次，Mysql中[{table}]表中的数据是:\n{data}')
                        break
                    if i > retry_num:
                        logger.debug(f'重复查询{i}次，Mysql中[{table}]表中的数据为空')
                        break
                    time.sleep(1)
                    logger.debug(f'计划查询{retry_num},查询第{i}次未查到数据;sql:{sql}')
            else:
                self.cursor.execute(sql)
                data = _format(self.cursor.fetchall())
            logger.debug('Mysql中[{0}]表中的数据是:\n{1}'.format(table, data))
            if exclude_fields:
                for i in range(len(data)):
                    for item in exclude_fields:
                        data[i].pop(item, None)

            return data
        except pymysql.Error as e:
            # self.close()
            logger.error(traceback.format_exc())

    def fetch_one(self, table, where_model, fields=None, exclude_fields=None, order_by: str = None, suffix: str = None):
        if exclude_fields is None:
            exclude_fields = []
        try:
            if fields is None:
                fields = "*"
            where = ''
            for k, v in where_model.items():
                # k could be like 'sample_ts' or include operator like 'sample_ts>'
                symbol = '='
                for i in ['>=', '<=', '!=', '>', '<', ' in', ' like']:
                    if i in k:
                        symbol = i
                        k = k.split(symbol)[0]
                        break

                if isinstance(v, int):
                    where += "`{0}`{1}{2}".format(k, symbol, v) + " and "
                elif isinstance(v, str):
                    where += "`{0}`{1}'{2}'".format(k, symbol, pymysql.escape_string(v)) + " and "
                elif isinstance(v, list):
                    in_str = str(v).replace('[', '(').replace(']', ')')
                    where += "`{0}`{1} {2}".format(k, symbol, in_str) + " and "
            if order_by:
                order_by = ','.join([f"`{item[0]}` {' '.join(item[1:])}" for item in [item.strip().split() for item in order_by.split(',')]])
                sql = "select %s from `%s` where %s order by %s" % (",".join(fields), table, where[:-4], order_by)
            else:
                sql = "select %s from `%s` where %s" % (",".join(fields), table, where[:-4])
            if suffix:
                sql = sql + suffix
            sql += ' limit 1'
            logger.info(sql)
            if self.retry_num > 0:
                i = 0
                while self.retry_num > 0:
                    self.cursor.execute(sql)
                    data = _format(self.cursor.fetchone())
                    i += 1
                    if data:
                        logger.debug(f'查询第{i}次，Mysql中[{table}]表中的数据是:\n{data}')
                        break
                    if i > self.retry_num:
                        logger.debug(f'重复查询{i}次，Mysql中[{table}]表中的数据为空')
                        break
                    time.sleep(1)
                    logger.debug(f'计划查询{self.retry_num},查询第{i}次未查到数据;sql:{sql}')
            else:
                self.cursor.execute(sql)
                data = _format(self.cursor.fetchone())
            # data = self.cursor.fetchall()
            logger.debug('Mysql中[{0}]表中的数据是:\n{1}'.format(table, data))
            if exclude_fields:
                for item in exclude_fields:
                    data.pop(item)
            return data
        except pymysql.Error as e:
            # self.close()
            # print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
            logger.error(traceback.format_exc())

    def fetch_by_sql(self, sql):
        try:
            logger.info(sql)
            self.cursor.execute(sql)
            data = _format(self.cursor.fetchall())
            logger.debug(f'Mysql中的数据是:\n{data}')
            return data
        except pymysql.Error as e:
            # self.close()
            # print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
            logger.error(traceback.format_exc())

    def delete(self, table, where_model):
        """
        从数据库删除记录
        :param table:
        :param where_model:查询条件，字典格式
        :param fields:查询的字段，默认查询全部字段
        :return:查询获得的数据，json格式的列表
        """
        try:
            where = " and ".join(["`%s`='%s'" % (k, v) for k, v in where_model.items()])
            sql = "delete from `%s` where %s" % (table, where)
            self.cursor.execute(sql)
        except pymysql.Error as e:
            # self.close()
            # print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
            logger.error(traceback.format_exc())

    def insert(self, table, model: dict):
        """
        insert data into table
        :param model: <dict> key与数据库field一致
        :param table: table name
        :return: The result of insert sql execute
        """

        fields, values, values_formatter = [], (), []
        for k, v in model.items():
            fields.append(k)
            values += (v, )
            values_formatter.append('%s')
        sql = "insert into `%s` (`%s`) values (%s)" % (table, "`,`".join(fields), ",".join(values_formatter))
        try:
            logger.info(sql)
            return self.cursor.execute(sql, values)
        except pymysql.Error as e:
            # self.close()
            logger.error(traceback.format_exc())

    def update(self, table, where_model: dict, fields_with_data: dict):
        """
        更新
        :param table: 表名
        :param fields_with_data: <dict>key与数据库field一致
        :param where_model: 条件，类型与model相同
        :return:
        """

        if where_model and isinstance(where_model, dict):
            where = ''
            for k, v in where_model.items():
                symbol = '='
                if isinstance(v, int):
                    where += "`{0}`{1}{2}".format(k, symbol, v) + " and "
                elif isinstance(v, str):
                    where += "`{0}`{1}'{2}'".format(k, symbol, pymysql.escape_string(v)) + " and "
                elif isinstance(v, list):
                    where += "`{0}`{1} {2}".format(k, symbol, tuple(v)) + " and "
        else:
            raise Exception('where_model can not be empty, and it should be a dict')

        if fields_with_data and isinstance(fields_with_data, dict):
            set = ''
            for k, v in fields_with_data.items():
                symbol = '='
                if isinstance(v, str):
                    set += "`{0}`{1}'{2}'".format(k, symbol, pymysql.escape_string(v)) + ","
                elif v == None:
                    set += "`{0}`{1}{2}".format(k, symbol, 'null') + ","
                elif isinstance(v, int):
                    set += "`{0}`{1}{2}".format(k, symbol, v) + ","
                else:
                    raise Exception('key {0} value {1}, value type is wrong'.format(k, v))

        else:
            raise Exception('fields_with_data can not be empty, and it should be a dict')
        sql = 'update `%s` set %s where' ' %s ' % (table, set[:-1], where[:-4])
        try:
            logger.debug('Mysql sql: {}'.format(sql))
            return self.cursor.execute(sql)

        except Exception as e:
            raise Exception("Mysql update error {}".format(e))

    def close(self):
        self.cursor.close()
        self.connection.close()

    def raw_sql(self, context):
        try:
            self.cursor.execute(context)
            data = self.cursor.fetchall()
            return data
        except pymysql.Error as e:
            logger.error(traceback.format_exc())


def _format(data):
    if isinstance(data, dict):
        for k in data:
            if type(data[k]) is Decimal:
                data[k] = float(data[k])
            if type(data[k]) is datetime.datetime:
                data[k] = str(data[k])

    elif isinstance(data, list):
        for d in data:
            _format(d)
    return data


if __name__ == '__main__':
    # mysql = MysqlManager(host='t-awsbj-quality-platform.clap5vvkrarj.rds.cn-north-1.amazonaws.com.cn',
    #                      port=3306,
    #                      user='quality_platform',
    #                      passwd='rJH4jHbT8CocxO42Ou',
    #                      db='quality_platform')
    # mysql.fetch('kafka_message',
    #             {"topic": 'swc-tsp-data_collection-test-vehicle_data',
    #              "create_time": '1530158603589'
    #              })

    # check use jump machine

    sql = 'select * from clients where id=45'
    result = jump_machine_mysql(sql=sql,
                                host='stage-cs.cw00om4rxgzj.rds.cn-north-1.amazonaws.com.cn',
                                port=3306,
                                user='user_message',
                                password='gzNw1ZNehIY',
                                database='message_staging_new'
                                )
    for row in result:
        print(row)
