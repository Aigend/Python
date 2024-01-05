"""
功能：云端收集数据完成运营类的管理
需求来源：https://nio.feishu.cn/wiki/wikcnLJJ6TIJ48i2eDAfiDG8tEd
上报时机：通过车端CDM上报版本消息及触发时间消息，触发事件，其中包括高优事件：撞车,翻车，安全气囊弹出的消息上报。
上报频率：实时通信
支持版本：NT2
应用方：AA
showdoc：https://nio.feishu.cn/wiki/wikcnbuhcPQESHLXLtIstKSqFAd
"""
import time
import uuid
import datetime
from nio_messages import pb2, pbjson
from nio_messages.data_unit import gen_adas_header, gen_upload_info
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2.cdm_app_upload_pb2 import CdmAppUpload


def generate_message(vin, vid, event_type, sample_ts=None, protobuf_v=pb2.VERSION,
                     adas_header_data=None, cdm_app_upload_data=None):
    """
    :param event_type:
    :param cdm_app_upload_data:
    :param sample_ts:
    :param protobuf_v:
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param adas_header_data: adas header数据
    :return: 包含np事件事件的nextev_msg以及feature_status_update本身
    """
    if cdm_app_upload_data is None:
        cdm_app_upload_data = {}
    cdm_app_upload_info = CdmAppUpload()

    cdm_app_upload_info.uuid = cdm_app_upload_data.get('uuid', str(uuid.uuid1()))
    cdm_app_upload_info.adc_version = cdm_app_upload_data.get('adc_version', 'BL061')
    cdm_app_upload_info.cdm_version = cdm_app_upload_data.get('cdm_version', 'cdm_v061.1.1')
    cdm_app_upload_info.utc_nano_timestamp = cdm_app_upload_data.get('utc_nano_timestamp', round(time.time()))
    cdm_app_upload_info.ptp_nano_timestamp = cdm_app_upload_data.get('ptp_nano_timestamp', round(time.time()))
    cdm_app_upload_info.vehicle_id = cdm_app_upload_data.get('vehicle_id', vid)
    cdm_app_upload_info.vehicle_type = cdm_app_upload_data.get('vehicle_type', 'ET7')
    cdm_app_upload_info.rules_info.append(cdm_app_upload_data.get('rules_info', 'rule1,version0.0.1'))
    cdm_app_upload_info.models_info.append(cdm_app_upload_data.get('models_info', 'model1,version0.0.1'))
    cdm_app_upload_info.coapp_name = cdm_app_upload_data.get('coapp_name', 'coapp name')
    cdm_app_upload_info.coapp_version = cdm_app_upload_data.get('coapp_version', 'coapp version')
    cdm_app_upload_info.app_uuid = cdm_app_upload_data.get('app_uuid', str(uuid.uuid1()))
    cdm_app_upload_info.build_date = cdm_app_upload_data.get('build_date', str(datetime.date.today()))
    if event_type == 'report_cdm_exception':
        cdm_app_upload_info.upload_info.MergeFrom(gen_upload_info(cdm_app_upload_data.get('upload_info', None)))

    if sample_ts is None:
        sample_ts = round(time.time() * 1000)
    adas_header = gen_adas_header(adas_header_data, sample_ts)

    cdm_app_upload_event = {'AdasHeader': adas_header, event_type: cdm_app_upload_info}

    # type为DATA_REPORT  sub_type为FeatureStatusUpdate
    # header的params的key为AdasHeader
    # status的params的key为FeatureStatusUpdate

    nextev_msg = gen_nextev_message(event_type,
                                    cdm_app_upload_event,
                                    sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    cdm_app_upload_obj = {
        'AdasHeader': pbjson.pb2dict(adas_header),
        'CdmAppUpload': pbjson.pb2dict(cdm_app_upload_info)
    }
    return nextev_msg, cdm_app_upload_obj
