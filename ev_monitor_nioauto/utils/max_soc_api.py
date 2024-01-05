import json,time
from utils.httptool import request

def set_max_soc_100(host,vid,account_id):
    api = '/api/1/in/vehicle/{vehicle_id}/reset_max_soc'.format(vehicle_id=vid)
    params = {
        'app_id': '10001',

    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'value': '100',
        'account_id': account_id
    }

    res = request('POST', url=host + api, data=data,headers=headers, params=params)
    return res

def query_max_soc(host,vid):
    api = '/api/1/in/vehicle/{vehicle_id}/status'.format(vehicle_id=vid)
    params = {
        'app_id': '10016',
        'field': 'soc'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    res = request('GET', url=host + api, params=params)
    return res


if __name__ == '__main__':
    # res = set_max_soc_100('https://tsp-test-int.nio.com','84d3457edb0a4bad8f76607f880cb2be','74452317')
    res = query_max_soc('https://tsp-test-int.nio.com','84d3457edb0a4bad8f76607f880cb2be')
    print(res.json())
