#!/usr/bin/env python
# coding=utf-8

"""
:file: publish_msg.py.py
:author: chunming.liu
:contact: Chunming.liu@nextev.com
:Date: Created on 2016/12/21 上午11:35
:Description: 
"""

import ssl
import paho.mqtt.client as mqtt

try:
    from utils.logger import logger
except Exception:
    import logging

    logger = logging.getLogger(__name__)


class MqttClient(object):
    def __init__(self, client_id, trust_chain, cert, key,tls_insecure_set=False):
        self.client_id = client_id
        self.client = mqtt.Client(client_id=self.client_id,
                                  clean_session=True,
                                  userdata=None,
                                  transport="tcp")
        self.client.on_message = on_message
        self.client.on_connect = on_connect
        self.client.on_publish = on_publish
        self.client.on_subscribe = on_subscribe
        self.client.on_disconnect = on_disconnect
        # self.client.on_log = on_log
        self.client.tls_set(trust_chain,
                            certfile=cert,
                            keyfile=key,
                            cert_reqs=ssl.CERT_REQUIRED,
                            tls_version=ssl.PROTOCOL_TLSv1,
                            ciphers=None)
        self.client.tls_insecure_set(tls_insecure_set)

    def connect(self, host, port, keep_alive=120):
        logger.debug("Mqtt connecting to {0}:{1}".format(host, port))
        self.client.connect("{host}".format(host=host), port, keep_alive)

    def loop_start(self):
        self.client.loop_start()

    def loop_stop(self, force=False):
        self.client.loop_stop(force=force)

    def publish(self, data):
        logger.debug("Mqtt publish to {0}, Data is\n {1}".format(self.client_id, data))
        self.client.publish('/clients/{0}/outbox'.format(self.client_id), data, qos=1)

    def disconnect(self):
        logger.debug("Mqtt disconnecting")
        self.client.disconnect()

    def connect_async(self, host, port, keep_alive=120):
        self.client.connect_async(host, port, keepalive=keep_alive)

    def loop_forever(self, timeout=1.0, max_packets=1, retry_first_connection=False):
        self.client.loop_forever(timeout=timeout, max_packets=max_packets, retry_first_connection=retry_first_connection)

    def tls_insecure_set(self, value):
        self.client.tls_insecure_set(value=value)


def on_connect(client, userdata, flags, rc):
    if rc != 0:
        logger.error(f" Mqtt {client._client_id} on_connect failed: {rc} {mqtt.connack_string(rc)}")
    else:
        logger.info(f"Mqtt {client._client_id} on_connect success: {rc} {mqtt.connack_string(rc)}")


def on_message(client, userdata, message):
    # logger.debug(f'Mqtt {client._client_id} on_message {message.topic} {str(message.qos)} {str(message.payload)}')
    pass


def on_publish(client, userdata, mid):
    # logger.debug(f"Mqtt {client._client_id} on_publish {userdata} {mid}")
    pass


def on_subscribe(client, userdata, mid, granted_qos):
    # logger.debug("Mqtt on_subscribe " + str(mid) + " " + str(granted_qos))
    pass


def on_disconnect(client, userdata, rc):
    if rc != 0:
        logger.error(f"Mqtt {client._client_id} on_disconnect failed: {rc}")
    else:
        logger.info(f"Mqtt {client._client_id} on_disconnect success: {rc}")

def on_log(mqttc, obj, level, string):
    logger.debug(f"Mqtt on_log {string}")


if __name__ == '__main__':

    # 车辆在线
    import os, sys
    base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../')
    sys.path.append(base_dir)

    env = 'test'
    host = f'tsp-nmp-{env}.nioint.com'
    port = 20083

    client_id = 'ChDaRLq8_tbIqc0iNNSEKddPEAEY9cUBIJVOKAI='
    vid= '4e18c0f0ab734805a802b845a02ad824'
    vin= 'SQETEST0514819462'

    cert_path = f'{base_dir}/config/{env}/{client_id}/'

    print(f'connecting to {host}')
    print(f'vid: {vid}\n vin: {vin} \n client_id: {client_id}')

    client = MqttClient(client_id,
                        cert_path + "ca/tls_tsp_trustchain.pem",
                        cert_path + "client/tls_lion_cert.pem",
                        cert_path + "client/tls_lion_priv_key.pem")

    client.tls_insecure_set(False)
    client.connect(host, 20083)

    client.loop_forever()