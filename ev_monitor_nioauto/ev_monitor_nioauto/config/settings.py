# -*- coding: utf-8 -*-
# @Project : cvs_basic_autotest
# @File : settings.py
# @Author : qiangwei.zhang.o
# @CreateTime : 2021/1/11 3:06 下午
# @Description : 读取证书文件

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def web_auth(cmdopt, vehicle_id):
    cert_dir = os.sep.join([BASE_DIR, 'config', cmdopt, 'cert', vehicle_id])
    cdc_cert = (os.sep.join([cert_dir, "client", "tls_airbender_cert.pem"]), os.sep.join([cert_dir, "client", "tls_airbender_priv_key.pem"]))
    ca_chain = os.sep.join([cert_dir, "ca", "trust_chain.pem"])
    return {'cdc_cert': cdc_cert, 'ca_chain': ca_chain}


def tsp_vehicle_auth(cmdopt, vehicle_id, platform='NT1'):
    cert_dir = os.sep.join([BASE_DIR, 'config', cmdopt, 'cert', vehicle_id])
    ca_chain = os.sep.join([cert_dir, "ca", "trust_chain.pem"])
    if platform == "NT1":
        cdc_cert = (os.sep.join([cert_dir, "client", "tls_airbender_cert.pem"]), os.sep.join([cert_dir, "client", "tls_airbender_priv_key.pem"]))
        adc_cert = (os.sep.join([cert_dir, "client", "tls_asimov_cert.pem"]), os.sep.join([cert_dir, "client", "tls_asimov_priv_key.pem"]))
        cgw_cert = (os.sep.join([cert_dir, "client", "tls_lion_cert.pem"]), os.sep.join([cert_dir, "client", "tls_lion_priv_key.pem"]))
        return {'ca_chain': ca_chain, 'cdc_cert': cdc_cert,  'adc_cert': adc_cert, 'cgw_cert': cgw_cert}
    elif platform == "NT2":
        cdc_cert = (os.sep.join([cert_dir, "client", "tls_cdc_cert.pem"]), os.sep.join([cert_dir, "client", "tls_cdc_priv_key.pem"]))
        adc_cert = (os.sep.join([cert_dir, "client", "tls_adc_cert.pem"]), os.sep.join([cert_dir, "client", "tls_adc_priv_key.pem"]))
        bgw_cert = (os.sep.join([cert_dir, "client", "tls_bgw_cert.pem"]), os.sep.join([cert_dir, "client", "tls_bgw_priv_key.pem"]))
        sa_cert = (os.sep.join([cert_dir, "client", "tls_sa_cert.pem"]), os.sep.join([cert_dir, "client", "tls_sa_priv_key.pem"]))
        # sa_cert = (os.sep.join([cert_dir, "client", "sa_cert.pem"]), os.sep.join([cert_dir, "client", "sa_priv_key.pem"]))
        return {'ca_chain': ca_chain, 'cdc_cert': cdc_cert, 'adc_cert': adc_cert, 'bgw_cert': bgw_cert, 'sa_cert': sa_cert}



def app_auth(cmdopt, account_id, app_id='10000'):
    cert_dir = os.sep.join([BASE_DIR, 'config', cmdopt, 'cert', str(app_id), str(account_id)])
    app_cert = (os.sep.join([cert_dir, "client", "tls_cert.pem"]), os.sep.join([cert_dir, "client", "tls_private_key.pem"]))
    # ca_chain = os.sep.join([cert_dir, "ca", "trust_chain.pem"])
    return app_cert


def tsp_auth(cmdopt):
    cert_dir = os.sep.join([BASE_DIR, 'config', cmdopt, 'cert', ])
    tsp_cert = (os.sep.join([cert_dir, "web_tsp-test-int", "web_tsp-test-int.cert"]), os.sep.join([cert_dir, "web_tsp-test-int", "web_tsp-test-int.key"]))
    tsp_chain = os.sep.join([cert_dir, "web_tsp-test-int", "web_tsp-test-int.trustchain"])
    return {'tsp_cert': tsp_cert, 'tsp_chain': tsp_chain}


def jump_machine_config_file():
    path = f'{BASE_DIR}/config/ssh/config'
    with open(path, 'r+') as f:
        s = f.read()
        s_new = s.replace('{BASE_DIR}', BASE_DIR)
        new_path = f'{BASE_DIR}/config/ssh/config_tmp'
        new_fo = open(new_path, 'w+', encoding='UTF-8')
        new_fo.write(s_new)
        new_fo.close()
    return new_path
