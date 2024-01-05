"""
    basic_info.json
    path: /etc/ssl/station
"""

import json
from utils.log import log


def get_station_authority():
    authority = 'https://' + get_host()
    # log.debug(f"<Cgw> <basic_info> get_station_authority:{authority}")
    return authority


def get_resource_id():
    with open('/etc/ssl/station/basic_info.json') as basic_info:
        """
        {"resource_id":"PS-NIO-a6352e19-3f143b8b",
        "secret_code":"dummy-pass",
        "wifi_ssid":"NIO-DXomQNx1",
        "wifi_password":"Htu0Las2CzJEwiG8",
        "cert_type":"stg"}
        """
        content = json.load(basic_info)
        # log.debug(f"<Cgw> <basic_info> basic_info.json content:{content}")
        resource_id = json.dumps(content['resource_id'])
        # log.debug(f"<Cgw> <basic_info> get resource id: {resource_id}")  # "PS-NIO-a6352e19-3f143b8b"
    return resource_id.strip('"')


def get_host():
    host = get_resource_id() + '.nio-pe-local.com'
    return host



