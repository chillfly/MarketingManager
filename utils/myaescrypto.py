
"""
采用AES对称加密算法
"""

import base64
from Crypto.Cipher import AES
from configs import settings


def add_to_16(value):
    """
    str不是16的倍数那就补足为16的倍数
    :param value:
    :return:
    """
    while len(value) % 16 != 0:
        value += '\0'

    # 返回bytes
    return str.encode(value)


def aes_encrypt(text=""):
    """
    加密方法
    :param text: 待加密字符串
    :return:
    """
    # 秘钥
    key = settings.WEIBO_AES_KEY
    # 初始化加密器
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    # 先进行aes加密
    encrypt_aes = aes.encrypt(add_to_16(text))
    # 用base64转成字符串形式
    base64_str = base64.encodebytes(encrypt_aes)
    # 执行加密并转码返回bytes
    encrypted_text = str(base64_str, encoding='utf-8')
    return encrypted_text


def aes_decrypt(text=""):
    """
    解密方法
    :param text: 密文
    :return:
    """
    # 秘钥
    key = settings.WEIBO_AES_KEY
    # 初始化加密器
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    # 优先逆向解密base64成bytes
    base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
    # 执行解密密并转码返回str
    decrypted_text = str(aes.decrypt(base64_decrypted), encoding='utf-8').replace('\0', '')
    return decrypted_text
