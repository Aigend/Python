# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/10/14 13:29
# @File:swap_status.py
import http.client
import ssl
import json
from cgw.swap import Message, ssl_cert_info, basic_info
from utils.log import log


def perform(msg=Message.Message()):
    log.info("<Cgw> <swap_status> enter cgw swap_status perform function")
    session_id = msg.get_session_id()

    # Defining parts of the HTTP request
    request_url = basic_info.get_station_authority() + '/v1/api/swap_status' + '?session_id=' + session_id
    log.debug(f"<Cgw> <swap_status> request_url:{request_url}")
    request_headers = {
        'Content-Type': 'application/json'
    }

    # Define the client certificate settings for https connection
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.load_verify_locations(cafile=ssl_cert_info.get_trust_chain())
    # Create a connection to submit HTTP requests
    connection = http.client.HTTPSConnection(host='192.168.43.1', port=443, key_file=ssl_cert_info.get_private_key(),
                                             cert_file=ssl_cert_info.get_cert(), context=context, timeout=60)

    # Use connection to submit a HTTP GET request
    connection.request(method="GET", url=request_url, headers=request_headers)

    # Print the HTTP response from the IOT service endpoint
    response = connection.getresponse()
    log.debug(f"<Cgw> <swap_status> response code:{response.status}, response reason:{response.reason}")
    data = response.read()
    log.debug(f"<Cgw> <swap_status> response data:{str(data)}")
    rep_json = json.loads(data)
    #return data
    return rep_json
