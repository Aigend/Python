import json
import time

# @pytest.mark.skip('Manual')
from utils.httptool import request


class TestInterestingData(object):
    def test_navigator(self):
        # stg
        # # es8
        # vid = '25613b71b0d14a258d743c94f14f8039'
        # account_id = 718218691
        # self.navigation_report('https://tsp-stg.nio.com', vid, account_id)

        # es6
        vid = 'e699260be9034542adbeb483fa2f486e'
        account_id = 555116995
        model = 'ES6'
        api = '/api/1/data/report'
        host = 'https://tsp-stg.nio.com'

        event = json.dumps([{"longitude": "109.601166",
                             "app_ver": "1.0.82.01",
                             "city": "三亚",
                             "area_code": "572099",
                             "app_id": "30009",
                             "nation": "中国",
                             "district": "吉阳区",
                             "event_type": "nav_period",
                             # 最南，latitude最小
                             "latitude": "18.184049",
                             "timestamp": int(time.time() * 1000),
                             "province": "海南省",
                             "roadName": "旅大街"}])
        data = {
            'model': model,
            'os': 'android',
            'os_ver': '1.0.0',
            'os_lang': 'unknown',
            'os_timezone': 'unknown',
            'client_timestamp': str(int(time.time() - 8 * 3600)),
            'network': 'unknwon',
            'user_id': account_id,
            'vid': vid,
            'events': event

        }

        request('POST', url=host + api, data=data)
