#!/usr/bin/env python
# coding=utf-8
"""
Message Platform SCR: https://confluence.nioint.com/display/CVS/Message+Platform

Message Platform整体介绍: https://confluence.nioint.com/display/CVS/Messaging+Platform
    1) Message Server: https://confluence.nioint.com/display/CVS/Message+Server
    2) Message Tracer: https://confluence.nioint.com/display/CVS/Message+Tracer
    3) Message API: https://confluence.nioint.com/display/CVS/Message+API

Messaging Platform Architecture: https://confluence.nioint.com/display/CVS/Messaging+Platform+Architecture
    1) NMP Client Logic: https://confluence.nioint.com/display/CVS/NMP+Client+Logic
    2) Keep Client Alive https://confluence.nioint.com/display/CVS/Keep+Client+Alive
    3) NMP环境和域名：https://confluence.nioint.com/pages/viewpage.action?pageId=74090751

消息平台连接返回含义:
    消息平台ConnAckMessage类型          byte值          描述                                                         场景
    --------------------------------------------------------------------------------------------------------------------------------------------
    CONNECTION_ACCEPTED               0x00          连接成功

    UNNACEPTABLE_PROTOCOL_VERSION     0x01          表示服务端支持的mqtt协议和客户端不匹配，使用backoff 的方式重连

    IDENTIFIER_REJECTED               0x02          ClientID 不正确，可以尝试重新获取client ID，使用backoff 的方式重连    1. 证书cn域不在白名单中;
                                                                                                                  2. clientId为空，或无效;
                                                                                                                  3. clientId与证书中deviceId不匹配;

    SERVER_UNAVAILABLE                0x03          服务端暂时不可用，此时可以使用backoff 的方式重连


    BAD_USERNAME_OR_PASSWORD          0x04          用户名密码不正确，对于车机端而言，不涉及到这个配置，
                                                    因此不会收到这样的错误。使用backoff 的方式重连

    NOT_AUTHORIZED                    0x05          表明这个客户端没有权限连接服务端，使用backoff 的方式重连。              1. 在设备连接黑名单中;
                                                                                                                  2. RVS设备有效性校验失败;

    FREQUENT_OPERATION                0x07          表示连接次数超过频次控制，使用backoff 重连，降低连接的次数              连接频次超过限制


"""

import time
import allure
import pytest
import os
from utils.assertions import assert_equal
from utils.logger import logger
from utils.mqtt_client import MqttClient

RC = -1


def on_connect(client, userdata, flags, rc):
    global RC
    RC = rc


class TestNMPConnection(object):
    def test_cdc_connection_success(self, env, cmdopt):
        """
        stg环境注意区分内网（Wi-Fi: NIO）和外网（Wi-Fi: NIO-GUEST）
        运维经常会配置为NIO网络不可连接，此时内网连接会报以下错误:
        "ssl.SSLEOFError: EOF occurred in violation of protocol (_ssl.c:777)"
        """
        with allure.step("Connection successful"):
            client_id = env['vehicles']['normal']['client_id']
            cert_path = os.path.join(os.path.dirname(__file__).split(os.sep + 'tests', 1)[0], 'config/{0}/{1}/'.format(cmdopt, client_id))
            client = MqttClient(env['vehicles']['normal']['cdc_client_id'],
                                cert_path + "ca/tls_tsp_trustchain.pem",
                                cert_path + "client/tls_airbender_cert.pem",
                                cert_path + "client/tls_airbender_priv_key.pem")
            client.client.on_connect = on_connect
            client.connect(env['message']['host_public'], env['message']['port_public'])
            client.loop_start()
            time.sleep(1)
            client.loop_stop()
            client.disconnect()
            assert_rc(RC, 0)

    def test_mqtt_0(self, env, cmdopt):
        with allure.step("Connection successful"):
            client_id = env['vehicles']['normal']['client_id']
            cert_path = os.path.join(os.path.dirname(__file__).split(os.sep + 'tests', 1)[0], 'config/{0}/{1}/'.format(cmdopt, client_id))
            client = MqttClient(client_id,
                                cert_path + "ca/tls_tsp_trustchain.pem",
                                cert_path + "client/tls_lion_cert.pem",
                                cert_path + "client/tls_lion_priv_key.pem")
            client.client.on_connect = on_connect
            client.connect(env['message']['host'], env['message']['port'])
            client.loop_start()
            time.sleep(1)
            client.loop_stop()
            client.disconnect()
            assert_rc(RC, 0)

    @pytest.mark.skip('manul')
    def test_mqtt_1(self, env, cmdopt):
        """
        mqtt version与服务端不匹配
        由于client._send_connect()函数会把非MQTTv311或MQTTv31的版本自动变为MQTTv311，所以本case需手工改动client的_send_connect()源码
        """
        with allure.step("校验mqtt版本不匹配时，返回1"):
            client_id = env['vehicles']['normal']['client_id']
            cert_path = os.path.join(os.path.dirname(__file__).split(os.sep + 'tests', 1)[0], 'config/{0}/{1}/'.format(cmdopt, client_id))
            client = MqttClient(client_id,
                                cert_path + "ca/tls_tsp_trustchain.pem",
                                cert_path + "client/tls_lion_cert.pem",
                                cert_path + "client/tls_lion_priv_key.pem")
            """
            1、将paho.mqtt.client的_send_connect()函数以下部分注释
            # if self._protocol == MQTTv31:
            #     protocol = PROTOCOL_NAMEv31
            #     proto_ver = 3
            # else:
            #     protocol = PROTOCOL_NAMEv311
            #     proto_ver = 4
            2、更改为以下两行代码(proto_ver 传入非3、4的证整数，使版本不一致)
            protocol = PROTOCOL_NAMEv31
            proto_ver = 6
            """
            client.client.on_connect = on_connect
            client.connect(env['message']['host'], env['message']['port'])
            client.loop_start()
            time.sleep(1)
            client.loop_stop()
            client.disconnect()
            assert_rc(RC, 1)

    def test_mqtt_2(self, env, cmdopt):
        """
        1、client_id与证书不匹配
        2、clients数据库里不存在但client_id格式合法

        clientId构造方法：
        ID id = ID.newBuilder().setIndex(this.id).setSig(this.sig).setVersion(this.version).setAppId((long)Integer.parseInt(this.appId)).setDeviceType(com.nio.message.protobuf.NmpClient.DeviceType.valueOf(this.deviceType.name())).build();
        this.clientId = new String(Base64.getUrlEncoder().encode(id.toByteArray()), StandardCharsets.UTF_8);
        """
        with allure.step("校验client_id合法，但数据库中不存在时，返回2"):
            client_id = env['vehicles']['normal']['client_id']
            cert_path = os.path.join(os.path.dirname(__file__).split(os.sep + 'tests', 1)[0], 'config/{0}/{1}/'.format(cmdopt, client_id))
            # client_id = 'ChAHRQ5bVLLSWLt53mxl2KLBEAEY_sUBIJVOKAA='合法，但数据库中不存在
            client = MqttClient('ChAHRQ5bVLLSWLt53mxl2KLBEAEY_sUBIJVOKAA=',
                                cert_path + "ca/tls_tsp_trustchain.pem",
                                cert_path + "client/tls_lion_cert.pem",
                                cert_path + "client/tls_lion_priv_key.pem")
            client.client.on_connect = on_connect
            client.connect(env['message']['host'], env['message']['port'])
            client.loop_start()
            time.sleep(1)
            client.loop_stop()
            client.disconnect()
            assert_rc(RC, 2)

        with allure.step("校验client_id与证书不匹配时，返回2"):
            client_id = env['vehicles']['normal']['client_id']
            cert_path = os.path.join(os.path.dirname(__file__).split(os.sep + 'tests', 1)[0], 'config/{0}/{1}/'.format(cmdopt, client_id))
            # 证书是normal的车，client_id是gb_private的车
            client = MqttClient(env['vehicles']['gb_private']['client_id'],
                                cert_path + "ca/tls_tsp_trustchain.pem",
                                cert_path + "client/tls_lion_cert.pem",
                                cert_path + "client/tls_lion_priv_key.pem")
            client.client.on_connect = on_connect
            client.connect(env['message']['host'], env['message']['port'])
            client.loop_start()
            time.sleep(1)
            client.loop_stop()
            client.disconnect()
            assert_rc(RC, 2)

    def test_mqtt_3(self, env, cmdopt):
        """
        client_id不存在且不合法
        """
        with allure.step("校验clirnt_id不存在且不合法时，返回3"):
            client_id = env['vehicles']['normal']['client_id']
            cert_path = os.path.join(os.path.dirname(__file__).split(os.sep + 'tests', 1)[0], 'config/{0}/{1}/'.format(cmdopt, client_id))
            client = MqttClient('ANotExistClientId',
                                cert_path + "ca/tls_tsp_trustchain.pem",
                                cert_path + "client/tls_lion_cert.pem",
                                cert_path + "client/tls_lion_priv_key.pem")
            client.client.on_connect = on_connect
            client.connect(env['message']['host'], env['message']['port'])
            client.loop_start()
            time.sleep(1)
            client.loop_stop()
            client.disconnect()
            assert_rc(RC, 3)

    @pytest.mark.skip('manul')
    def test_mqtt_7(self, env, cmdopt):
        """
        test环境配置：600秒内同一个client_id连接大于300次
        prod环境无此配置
        """
        with allure.step("校验60秒内同一个client_id连接大于30次，返回7"):
            client_id = env['vehicles']['normal']['client_id']
            cert_path = os.path.join(os.path.dirname(__file__).split(os.sep + 'tests', 1)[0], 'config/{0}/{1}/'.format(cmdopt, client_id))
            client = MqttClient(client_id,
                                cert_path + "ca/tls_tsp_trustchain.pem",
                                cert_path + "client/tls_lion_cert.pem",
                                cert_path + "client/tls_lion_priv_key.pem")
            timer = int(time.time())
            client.client.on_connect = on_connect
            # 1分钟的时间窗口内，重复connect-disconnect次数大于30
            # netstat -an|grep 20083 查看20083端口的连接数不会多于1个
            for i in range(300):
                client.connect(env['message']['host'], env['message']['port'])
                client.loop_start()
                time.sleep(0.1)
                client.loop_stop()
                client.disconnect()
                logger.debug("Mqtt on_connect code {}".format(RC))
            assert_rc(RC, 7)

    @pytest.mark.skip('manual')
    def test_ocsp(self):
        """
        在线证书状态协议（ocsp） 可在服务端校验车辆证书有效与否
        以这辆车做例子：
        vehicle_id: 8dd0af9d5e734691845757be77d42852
        client_id: "ChDqskktQbCDoYSu9YNljL3eEAEYpBMglU4oAg=="
        vin: SQETEST0055267515

        python mqtt.py stg cgw 8dd0af9d5e734691845757be77d42852 ChDqskktQbCDoYSu9YNljL3eEAEYpBMglU4oAg==


        1.stg环境 OCSP验证开关保持关闭。
        2.将车（台架）的GGW的证书，进行备份。
        3.用该证书尝试连接nmp，能连接成功
        4.BD连接到车（台架），点击拆解ECU，拆解ADC\CDC\CGW的证书，这时证书会在服务器端标记为无效。
        openssl ocsp -header Host shaolin.sec-stg.nio.com -issuer Ica_Vehicle_test.pem -CAfile Ica_Vehicle_test-chain.pem -cert client/tls_lion_cert.pem -url http://shaolin.sec-stg.nio.com/status/ocsp

        Response verify OK
        client/tls_lion_cert.pem: revoked
        This Update: Nov  8 02:58:34 2019 GMT
        Reason: superseded
        Revocation Time: Nov  6 08:39:56 2019 GMT


        5.重新用该备份的证书连接车，此时OCSP验证开关仍保持关闭，预期仍可以用该证书连接成功
        5.打开OCSP验证开关
        6.尝试重新用该证书连接消息平台，预期不能连接成功

        kibana: swc-cvs-nmp-stg_tsp-serer-log-json 关键字：ocsp
        clientId:ChDqskktQbCDoYSu9YNljL3eEAEYpBMglU4oAg== offset:295,904,959 level:ERROR
        input_type:log source:/data/app/greatwall_messaging_server/log/server.log
        env:stg_tsp message:[TSP_CONNECT] certCN TlsLion_8dd0af9d5e734691845757be77d42852_test ocsp status is not OK



        """
        pass

    @pytest.mark.skip('manual')
    def test_expired_certs(self):
        """
        校验ADC的过期证书
        APP_ID: 10107
        VIN: LNBSCC3H1GF316827
        VID: 0016927189f4441d9f7e168b10416b35
        CLIENT_ID: ChAQy46aypllnmjkFQ6aM8dxEAEY6boDIPtOKAI=

        测试过期证书能连上tsp 消息平台
        python mqtt.py stg adc 0016927189f4441d9f7e168b10416b35 ChAQy46aypllnmjkFQ6aM8dxEAEY6boDIPtOKAI=

        """


def assert_rc(reslut, expect):
    if reslut == 0:
        logger.debug("Mqtt on_connect success code {}: Connection successful".format(reslut))
    elif reslut == 1:
        logger.error("Mqtt on_connect refused code {}: incorrect protocol version".format(reslut))
    elif reslut == 2:
        logger.error("Mqtt on_connect refused code {}: invalid client identifier".format(reslut))
    elif reslut == 3:
        logger.error("Mqtt on_connect refused code {}: server unavailable".format(reslut))
    elif reslut == 4:
        logger.error("Mqtt on_connect refused code {}: bad username or password".format(reslut))
    elif reslut == 5:
        logger.error("Mqtt on_connect refused code {}: not authorised".format(reslut))
    else:
        logger.error("Mqtt on_connect failed code {}: Currently unused".format(reslut))
    assert_equal(reslut, expect)


