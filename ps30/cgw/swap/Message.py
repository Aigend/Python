import os
from utils.log import log


'''
     message for transfer 
'''


class Message:
    def __init__(self, body=''):
        self._body = body
        self._cert_file = ''
        self._private_key_file = ''
        self._trust_chain_file = ''
        self._url = ''
        self._session_id = ''

    def set_body(self, body=''):
        log.info(f'body>>>>>>>>>>:{body}')
        self._body = body

    def get_body(self):
        return self._body

    def set_url(self, url=''):
        self._url = url

    def get_url(self):
        return self._url

    def set_session_id(self, session_id=''):
        self._session_id = session_id

    def get_session_id(self):
        return self._session_id

    def set_certs(self, cert='', private_key='', trust_chain=''):
        self._cert_file = cert
        self._private_key_file = private_key
        self._trust_chain_file = trust_chain

    def get_cert_file(self):
        return self._cert_file

    def get_private_key_file(self):
        return self._private_key_file

    def get_trust_chain_file(self):
        return self._trust_chain_file
