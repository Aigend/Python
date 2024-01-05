#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:chunming.liu 
@time: 2020/06/18 21:26
@contact: chunming.liu@nio.com
@description: TSP使用的各种加密算法实现。http://showdoc.nevint.com/index.php?s=/123&page_id=4802
"""
import base64
import string
import time
import random
import hashlib
import pyDes
import requests
import unpaddedbase64
from utils.signature import moatkeeper_signature
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP as PKCS, PKCS1_v1_5
from Crypto.Hash import SHA3_256
from Crypto.Hash import SHA256
from Crypto.Signature.pss import MGF1

consts = [
    "2976ae25f6b04f719f351e2fd890fa50",
    "ed8abe8d1fc3456a8a1e366151c2a6b7",
    "6b10b3f89d1c4bfa8199ff3f74aa2887",
    "a76d51834a4f4609a38d1a0f5e3d6465",
    "e6be849e07c64511a17b777743021af3",
    "3edb5e23e8b34f848af4888feb169e9b",
    "c527b8e5816346c6a586e7ea9db27fa5",
    "bb719cd4f60d4567a19103187e855b30",
    "85c9ff17d6cf46bbbea8e8671d25a944",
    "9341dc8b84bb422598a890273a28fe09"
]


def get_encryption(env, app_id=10000):
    host, path, method = env["host"]['tsp_ex'], '/api/1/poseidon/account/get_encryption', "GET"
    url_params = {"hash_type": 'sha256', "app_id": app_id, "timestamp": int(time.time())}
    inputs = {"path": path, "method": method, "params": url_params}
    url_params['sign'] = moatkeeper_signature(inputs, env["secret"][int(app_id)])
    res = requests.request(method, host + path, params=url_params)
    response = res.json()
    return response['data']['key_id'], response['data']['key']


def checkedPassword(password, key):
    salt = consts[ord(password[0]) % len(consts)]
    sh = SHA3_256.new()
    password = str.encode(password + salt)
    sh.update(password)
    ps = sh.hexdigest()
    return rsa(ps, key)


def encrypt(password, key):
    """
    通过get_encryption_account获取的key,加密明文password/pin_code，获得password_e;
    注意事项：
    1、在account_center服务中，应用场景：注册获取密码加密、修改密码加密、pin_code获取密码加密；
    """
    keyDER = unpaddedbase64.decode_base64(key)
    keyPub = RSA.importKey(keyDER)
    cipher = PKCS.new(keyPub, SHA3_256, lambda x, y: MGF1(x, y, SHA256))
    cipher_text = cipher.encrypt(password.encode())
    return base64.urlsafe_b64encode(cipher_text)


def rsa(raw, key):
    """
    RSA加密
    :param raw: 明文密码或者pin_code
    :param key: 用来RSA加密的public key，会在一定时间内失效，请在实际使用时通过get_encryption2获取。
    :return: rsa加密后的字符串
    """
    keyDER = unpaddedbase64.decode_base64(key)
    keyPub = RSA.importKey(keyDER)
    cipher = PKCS.new(keyPub, SHA3_256, lambda x, y: MGF1(x, y, SHA256))
    cipher_text = cipher.encrypt(raw.encode())
    return base64.urlsafe_b64encode(cipher_text)


def sha3256(raw):
    """
    SHA3-256算法
    :param raw: 待加密的字符串。
    :return: SHA3-256加密后的字符串
    """
    salt = consts[ord(raw[0]) % len(consts)]
    sh = SHA3_256.new()
    sh.update((raw + salt).encode("utf-8"))
    return sh.hexdigest()


def rsa_pkcs_key_pair(bits=2048):
    """
    PKCS格式的RSA密钥对，public key in pkcs8 , private key in pkcs1
    :param bits:
    :return:
    """
    key = RSA.generate(bits)
    pub_key_pkcs = base64.b64encode(key.publickey().exportKey(pkcs=8)).decode()
    prv_key_pkcs = base64.b64encode(key.exportKey(pkcs=1)).decode()
    return pub_key_pkcs, prv_key_pkcs


def rsa_encrypt(s, public_key):
    """
    :param s: 原字符串
    :param public_key: unicode bytes or PEM encode的字符串
    :return: base64编码bytes string
    """
    key = RSA.importKey(public_key)
    cipher = PKCS1_v1_5.new(key)
    cipher_text = base64.b64encode(cipher.encrypt(bytes(s, 'utf-8')))
    return cipher_text


def rsa_decrypt(s, private_key):
    """
    :param s: base64编码bytes string
    :param private_key: bytes or PEM encode的字符串
    :return: string
    """
    key = RSA.importKey(private_key)
    cipher = PKCS1_v1_5.new(key)
    raw_text = cipher.decrypt(base64.b64decode(s), None).decode()
    return raw_text


def des3_encrypt(s, key):
    """
    :param s: 原字符串
    :param key: unicode bytes or PEM encode的字符串
    :return: base64编码bytes string
    """
    m5 = hashlib.md5()
    m5.update(key.encode('utf-8'))
    key_m = m5.digest()
    key_m += key_m[0:8]
    k = pyDes.triple_des(key_m, pyDes.CBC, IV="\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    d = k.encrypt(s)
    return base64.b64encode(d).decode()


if __name__ == '__main__':
    pass
    # key_id, key = get_encryption("https://tsp-test.nio.com", app_id=10000)
    # password = rsa("112233", key).decode("utf-8")  # 加密密码
    # print("key_id=", key_id)
    # encode_pin = rsa(sha3256("112233"), key).decode("utf-8")
    # print(encode_pin)
    print(des3_encrypt('FOTAtest1234567', '1qaz2wsX'))
