#!/usr/bin/env python3

from argparse import ArgumentParser
from urllib.parse import urljoin
from configparser import ConfigParser
import subprocess
import os
import json
import logging

import requests
from terminaltables import SingleTable

logging.basicConfig(level=logging.INFO)

parser = ArgumentParser()
parser.add_argument('-c', '--config', default='vpnapi.ini', help='配置文件')
action = parser.add_subparsers(dest='op', help='功能')
ssh = action.add_parser('ssh', help='使用ssh 连接vpn 指定客户端')
ssh.add_argument('cert', help='证书名称')
ssh.add_argument('-u', '--user', default='opman', help='ssh 用户')
ssh.add_argument('-p', '--port', type=int, default=22, help='ssh 端口')

listall = action.add_parser('list', help='列出在线的客户端')
listall.add_argument('-F', '--format', choices=['table', 'json'], default='table', help='输出格式，默认是table')

tag = action.add_parser('tag', help='添加证书描述')
tag.add_argument('cert', help='证���名称')
tag_op = tag.add_mutually_exclusive_group()
tag_op.add_argument('-t', '--tag', help='证书描述')
tag_op.add_argument('-d', '--delete', action='store_true')

scp = action.add_parser('scp', help='使用scp上传下载文件')
scp.add_argument('action', choices=['upload', 'download'], default='upload', help='上传或者下载')
scp.add_argument('cert', help='证书名称')
scp.add_argument('data', help='要上传或下载的文件路径')
scp.add_argument('-u', '--user', default='opman', help='ssh 用户')
scp.add_argument('-p', '--port', type=int, default=22, help='ssh 端口')

args = parser.parse_args()
config_file = args.config
config = ConfigParser()
config.read(config_file)
api = config['api']['url']
api_user = config['api']['user']
api_pass = config['api']['password']

client_url = urljoin(api, '/clients/')
cert_url = urljoin(api, '/cert/')
op = args.op
if op in ('ssh', 'scp'):
    cert = args.cert
    try:
        ret = requests.get(client_url, auth=(api_user, api_pass), params={'client': cert})
    except Exception as e:
        logging.error(f'api 错误: {str(e)}')
        exit(128)
    data = json.loads(ret.content)
    if not data:
        logging.error('客户端不在线或不存在')
        exit(1)
    client = data[0]
    host = client['virtual_ip']
    proxy = client['server']
    user = args.user
    port = args.port
    corkscrew = '/usr/local/bin/corkscrew'
    if not os.path.isfile(corkscrew):
        logging.error('需要安装corkscrew到/usr/local/bin/corkscrew, 见https://github.com/bryanpkc/corkscrew.git')
        exit(2)
    if op == 'ssh':
        subprocess.call(f'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o ProxyCommand="/usr/local/bin/corkscrew {proxy} 3128 %h %p" {user}@{host} -p {port}',
                        shell=True)
    elif op == 'scp':
        scp_op = args.action
        data = args.data
        if scp_op == 'upload':
            subprocess.call(
                f'scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o ProxyCommand="/usr/local/bin/corkscrew {proxy} 3128 %h %p" -r -P {port} {data} {user}@{host}:', shell=True)
        elif scp_op == 'download':
            subprocess.call(
                f'scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o ProxyCommand="/usr/local/bin/corkscrew {proxy} 3128 %h %p" -r -P {port} {user}@{host}:{data} .', shell=True)

elif op == 'list':
    format = args.format
    try:
        ret = requests.get(client_url, auth=(api_user, api_pass))
    except Exception as e:
        logging.error(f'api 错误: {str(e)}')
        exit(128)
    data = json.loads(ret.content)
    if format == 'json':
        print(json.dumps(data, indent=True))
    else:
        table_data = [('证书', '描述', 'openvpn server', '连接时间', '虚拟ip', '真实ip', '上传流量(字节)', '下载流量(字节)')]
        for client in data:
            table_data.append((
                client['common_name'], client['description'], client['server'], client['connected_since'],
                client['virtual_ip'], client['real_ip'], client['bytes_sent'], client['bytes_received']))
        table_ins = SingleTable(table_data, title='在线客户端')
        table_ins.justify_columns[2] = 'right'
        print(table_ins.table)
elif op == 'tag':
    cert = args.cert
    if args.delete:
        try:
            requests.delete(urljoin(cert_url, cert), auth=(api_user, api_pass))
        except Exception as e:
            logging.error(f'api 错误: {str(e)}')
            exit(128)
    else:
        tag = args.tag
        try:
            requests.post(cert_url, json={'common_name': cert, 'description': tag}, auth=(api_user, api_pass))
        except Exception as e:
            logging.error(f'api 错误: {str(e)}')
