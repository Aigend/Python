#!/usr/bin/env python
# coding=utf-8

"""
:file: nextev_msg.py
:author: chunming.liu
:contact: Chunming.liu@nextev.com
:Date: Created on 2017/1/9 下午5:17
:Description: 负责生成和解析Nextev Message
"""
import importlib
import random
import zlib
import time
from pprint import pprint

from nio_messages import pb2
from nio_messages.pb2 import nextev_msg_pb2


def parse_nextev_message(message):
    """
    解析nextev消息，生成一个字典
    :param message: nextev消息的proto格式数据
    :return: 包含nextev消息各个字段的字典
    """
    nextev_message = nextev_msg_pb2.Message()
    data = nextev_message.FromString(message)
    tsp_msg = {}
    for param in data.params:
        if param.key in ['vehicle_status', 'AdasHeader', 'FeatureStatusUpdate']:
            module = importlib.import_module('nio_messages.' + data.sub_type, ".")
            gen_function = getattr(module, "parse_message")
            value = gen_function(param.value)
        else:
            value = param.value.decode()
        tsp_msg.update({param.key: value})

    parsed_message = {"publish_ts": data.publish_ts,
                      "type": data.type,
                      "ttl": data.ttl,
                      "version": data.version,
                      "sub_type": data.sub_type,
                      "qos": data.qos,
                      "platform_type": data.platform_type,
                      "target": data.target,
                      "params": tsp_msg}
    return parsed_message


def gen_nextev_message(sub_type, data, publish_ts, account_id, qos=1, version=pb2.VERSION, msg_type=3, ttl=1000):
    """
    生成nextev消息
    :param platform_type:
    :param target:
    :param qos:
    :param version: message protocol version
    :param publish_ts: message publish time(server time) ,必须填毫秒
    :param msg_type: 消息类型，例如NOTIFICATION = 0;CONTROL_COMMAND = 1;COMMAND_RESULT = 2;DATA_REPORT = 3;CLIENT_STATUS = 4;
    :param sub_type: 子类型，业务自己定义
    :param data: 消息内容
    :param account_id: vid值
    :param ttl: message expiration (second)
    :return: nextev的protobuf格式消息
    """
    nextev_msg = nextev_msg_pb2.Message()
    nextev_msg.version = version
    nextev_msg.publish_ts = publish_ts
    nextev_msg.ttl = ttl
    nextev_msg.type = msg_type
    nextev_msg.sub_type = sub_type
    nextev_msg.qos = qos

    if msg_type == 3:
        if sub_type == 'rvs_events_report':
            params1 = nextev_msg.params.add()
            params1.key = 'event_type'
            params1.value = str(data.pop('specific_event_type')).encode()

            params2 = nextev_msg.params.add()
            params2.key = 'event_data'
            params2.value = str(data).encode()

            params3 = nextev_msg.params.add()
            params3.key = 'vehicle_id'
            params3.value = str(account_id).encode()

        elif isinstance(data, dict) and 'AdasHeader' in data.keys():
            params1 = nextev_msg.params.add()
            params1.key = 'AdasHeader'
            params1.value = data['AdasHeader'].SerializeToString()

            params2 = nextev_msg.params.add()
            params2.key = sub_type
            params2.value = zlib.compress(data[sub_type].SerializeToString())

            params3 = nextev_msg.params.add()
            params3.key = 'account_id'
            params3.value = str(account_id).encode()

            params4 = nextev_msg.params.add()
            params4.key = 'original_length'
            params4.value = str(len(data[sub_type].SerializeToString())).encode()

        else:
            params1 = nextev_msg.params.add()
            params1.key = 'vehicle_status'
            params1.value = zlib.compress(data.SerializeToString(), 9)
            params2 = nextev_msg.params.add()
            params2.key = 'original_length'
            params2.value = str(len(data.SerializeToString())).encode()
            if account_id:
                params3 = nextev_msg.params.add()
                params3.key = 'account_id'
                params3.value = str(account_id).encode()
    elif msg_type == 0:
        pass
    elif msg_type == 1:
        pass
    elif msg_type == 2:
        pass
    elif msg_type == 4:
        params1 = nextev_msg.params.add()
        params1.key = 'account_id'
        params1.value = str(account_id).encode()
        params2 = nextev_msg.params.add()
        params2.key = 'status'
        params2.value = data.get("status", random.choice(["CONNECTION_LOST", "OFFLINE", "ONLINE"])).encode()
        params3 = nextev_msg.params.add()
        params3.key = 'port'
        params3.value = data.get("port", random.choice(['20083', '20084'])).encode()

    else:
        pass
    nextev_message = nextev_msg.SerializeToString()
    return nextev_message


def extend_nextev_message_header(msg, **kwargs):
    nextev_message = nextev_msg_pb2.Message()
    data = nextev_message.FromString(msg)
    if 'platform_type' in kwargs:
        data.platform_type = kwargs['platform_type']
    if 'qos' in kwargs:
        data.qos = kwargs['qos']
    if 'target' in kwargs:
        data.target = kwargs['target']
    nextev_message = data.SerializeToString()
    return nextev_message

if __name__ == '__main__':
    from nio_messages import periodical_journey_update, window_change_event
    message = b'\x08\x11\x18\xe0\xf3\xc9\xb0\xae. \xe8\x07(\x032\x13window_change_event:y\n\x0evehicle_status\x12gx\xda\xe3\x12\x0c\x0et\rq\r\x0e10\xb7437372\xb4\x10\x10\x94x\xf0\xf9\xe4\x86uzJq\\\x16\x1cL\x022\x12f\n\xd1F|\x1c\x0c\x02\x8c\x12\x0c\n\x8c\x1a\x8c\x06\x8c\x16\x0cV >\x03\x90\xcf\x00\xe1;!\xf8\x0c\x06\x0c\x16\x8cBJ\x1cF\x02\xb2\x12,J<\x1c\x8c`} qF-\x1e\xb8)@U\x00K\xf7\x10k:\x16\n\x0foriginal_length\x12\x03124:.\n\naccount_id\x12 74361e94a61846e2a690d2e2a9bf591d'
    # message = b'\x08\x11\x18\xfe\x87\xca\xb0\xae. d(\x032\x19periodical_journey_update:\xa2\x04\n\x0evehicle_status\x12\x8f\x04x\x9c\xed\x95\xcfk\xd3`\x18\xc7\x9f\'A\xf6.t\x90\x94\xc1\xd2J\xc5\xea\xa5\xabP\xde\xc4\xa6K\xc4\xb9\xb7\xce0;;t\x8e\x1e\x06R\x99x\xd0\xd3f/\xce)X\xf1\xe2<\xe8\xa4\x97y\x9b\xe8a\x82HN\xc3\x9b\x99\xbbH\x11\xf1\x17(\x9e\xa6\'=M\x11\xb7\n\xb5\xf5Ml\xaa\xfe\tB\xbf$\xdf|\xf8>\xcf\xfb\xf0\xbe\x977\x92\x92\x1f\xd5l;[(P\xfbxn\x98R\xaa\xcb\xa0*\xbbB:\xd5)54\x93\'Z\xb2\xd7\xb4\xcc\x0c\xd5\x87-\xcb\xd4\x06\xf6R\xdd02\x86\xa1;!R\xbeZu\x1e\xa6\xc2\x15\x91\x80Ry\xb0\xf6\xb2\x90/\xb2HI\xbc]k\x8c\x0c\xb1\xf8\xbd\x99A\xe9\xed]\x85\xf5\xdf|\xf2=q\xe2\xe8\x11\xa6\xad|\xfb\xf9f\xf6\xf3\xc7!\xab~\xff\xeb\xab\xb1S\xe5\xc7lc\xe3\xd9\xd6\xb6\x9c\xdf\xb9\xfd4\x1b\x0f`r\xb5z\xc7^\xd9]dS|\x02\xcfDv\x16<\x1d\xb8\xc1J\xfb\tD\x15\xd2#\xe7\xd5B\xdc\x0f\x81\xb2\x04D\xc3$&\xcf\x0b\xea\x9eVfx\x99Bv\xc8L\xedkE\x19\x1e\xcd\x8ae\x84\xeb\xf8\x01\xbb\xa1%%\x80\x88\xef\xc5\xf7,\x1e$\xfd\x01h\x01X\x01d\x03\xc8\x050\x1e\xc0\xa4\xef\xeb\xe7\xd9\x94\x0f\x87*\xad\xbd_Zc\xe7\xf8\xc7]hNg/\xf8\xe39\\A\x0e\xac\xa71\x9d\x9dG\xbf\xeb\xa2\xc3na0j\x11a\ta\x19\xc1Ax\x84\xe0"<E|\x81\xf0\x0ea\x1d\xe1\x13\xc2\x17\x84\x1aBY\x80k\x02,\x08\xb0(\xc0\x92\x00\xcb\x028\x02D{\t\xaax\x06\xe6\xba\xed\t\xf3\xe4@\xcaH\xa5\xf9\xd1\x93\xaf\xbb\xf6U\xbb\x08R\x17Md.\x8eA\xf3\xf2H\xc7:\xd6\xb1\xff\xd2\x0e\xd7\xc5cuQW\x92`x\x17\xc6\xa0g\xb6g\x07\x89$\x10\xe4\xaf0\x1a&(c\xcc\xeb\xde\x89\t4<\x98\x81\xb9\x92\x14#\x8d\x1f\xcd\xdf\xc2\xb0\xccoz\x9aI\xd3\xb6\xa4\x08y^k\x97CZ\x9a\xff\x0et\x8dz\x0f_\xb9Z\xfbw\xe5\xdf\x92\xfa\x88\xbb\xd9.K\x7f\n&\xfc\x02\xa5\x027&:\x17\n\x0foriginal_length\x12\x041648:.\n\naccount_id\x12 bbeeac3554c54f2d96caf6bae7ba2fa9'
    # message = b'\x08\x11\x18\xfe\x87\xca\xb0\xae. d(\x032\x19periodical_journey_update:\x93\x04\n\x0evehicle_status\x12\x80\x04x\x9c\xed\x94\xcfk\x13A\x14\xc7\xdf\x9b%\xcddk`w\t\xb8\x8dT\x8c^\xd2\x08avu\x93]\xb1vb]jj\x8aV\xc9\xa1P"\x95\x1e\xf4\xd4\xda\x8b\xb5\nF\xbdX\x0fZ\xc9\xa5\xde*z\xa8 \x12<\x14o]\xedE\x82\x07\x7f\x81\xd2S\xf5\xa4\xa7*\xa5\xd8Cl\xdd]3\x7f\x84\x90\x07\xf3\x9d\x0f\x9fy<f.#\xab\xa5A\xc3u\x0b\xe52s\xcf\x16\xfb\x19c\xa6\x02\xba\xba\x7f\x97\xc9L\xc6,\xc3\xf6\x8d\x91I\xd8\x8e\x9dcf\xbf\xe3\xd8F\xfe\x103-+gY\xe6f\'\xad\xden\xd4\x9fg\xb5\x9aDA\xad=[y_.Ux\xd7\x94\xf4pk{\xa0\x8f\xa7\x9eL\xf6\xca\x9f\x1f\xab\xbc\xe7\xfe\xeb\xcd\xf4\xe8\xe9S\xdcX\xda\xf8\xf3i\xfa\xc7\xb7>\xa7\xf9\xf4\xd7\x87\xa1\x0b\xd5e\xbe\xbe\xfe\xf6w\xa4\x18v\xee\x19\xe7\xc3\x02F^5\x1e\xb9K\x07*|\xcc\x9f\xe0;\x89_\x82\xa0\x8e\xdd\xe3SG)$U\x1aWJz9\x15J`<\rI\x8dv+\xb3D?\xd8rV\xe0T\xbaW\xe1\xfa\xee\x96\xca\xf9jZ\xaa"\xdc\xc5\xaf\x18\x83V\xa9\x02\xba\xc2\xac\xac\xf2\x940=\x02\x0c\x01\x8e\x80\x82\x80\xa2\x80a\x01#a\xae]\xe1c!\x9c\xa8\xb5\xee~}\x85_\xf67ong\xa2p5\x1c\xef\xc3M\xf4\x81\xc7\xb7\'\n\xb3\x18v]\xab\xf3\x07(F\xcd#, ,"\xd4\x11^"x\x08o\x10\xdf!|AXC\xf8\x8e\xf0\x13a\x0b\xa1J\xe0\x0e\x819\x02\xf3\x04\x16\x08,\x12\xa8\x13H&(\xeax\x11fb\xee9\xfb|>ke\x0f\xfbO\xcf|\x8c\x1eiD)2\x0fm\xe4\x1e\x0e\xc1\xce\x8d\x81v\xb4\xa3\x1d\xffe\x9clJg\x9a\x92\xa9f\xc0\n>\x8c\xde \xdc \x8eS\x99P\xf4\x17\x19\xd4(*\xd8\x1dt\xef\xc34Z\x01L\xc2L^\x8e\xd3[\x1d\x1a\x05\x18\x0f\xff\x1a\xb9\x93\xbe\x88j\x1d\x89\x88\xa6\xa4\x88\x7f\xb6\x1c\r\xce\xfe\x95,S/\xa6EB\xb6\xe1/r\xe5\r\x1a:\x17\n\x0foriginal_length\x12\x041589:.\n\naccount_id\x12 bbeeac3554c54f2d96caf6bae7ba2fa9'
    # message = gen_nextev_message("", {"status": "ONLINE"}, int(time.time())*1000, msg_type=4, account_id="123")
    parse = parse_nextev_message(message)
    pprint(parse)
