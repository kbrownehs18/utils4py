#!/usr/bin/env python
# coding: utf-8

import base64
import datetime
import hashlib
import hmac
import os
import random
import re
import time
from binascii import a2b_hex, b2a_hex

from Crypto import Random
from Crypto.Cipher import AES
from sqlalchemy import Date, DateTime, Numeric


def md5bytes(bs):
    """
    md5bytes
    @param bs bytes
    """
    m = hashlib.md5()
    m.update(bs)
    return m.hexdigest()


def md5(strs):
    """
    md5
    """
    return md5bytes(strs.encode(encoding="utf-8"))


def extension(filename):
    """
    file extension
    """
    ext = os.path.splitext(filename)[1]
    if ext == "":
        ext = os.path.splitext(filename)[0]
    if ext.startswith("."):
        ext = ext[1:]
    return ext


def check_phone_number(phone_number):
    """
    check if the phone number valid
    """
    return (
        True if re.compile(r"^1(3|4|5|6|7|8|9)[\d]{9}$").match(phone_number) else False
    )


def model_to_dict(model):
    """
    model to dict
    """

    def convert_datetime(value):
        if value:
            return value.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return ""

    data = {}
    for col in model.__table__.columns:
        if isinstance(col.type, DateTime):
            value = convert_datetime(getattr(model, col.name))
        elif isinstance(col.type, Numeric):
            value = str(getattr(model, col.name))
        else:
            value = getattr(model, col.name)

        data[col.name] = value

    return data


def random_string(len=5):
    """
    random string
    0-9 a-z A-Z
    """
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars = []
    for i in range(len):
        chars.append(random.choice(ALPHABET))

    return "".join(chars)


pad = lambda s: s + (AES.block_size - len(s) % AES.block_size) * chr(0)


def encrypt(content, key="1234567890", expires=0):
    """
    加密
    @param content 加密内容
    @param key 
    @param expires 过期时间
    """
    iv = Random.new().read(AES.block_size)
    cryptor = AES.new(pad(key), AES.MODE_CBC, iv)
    ciphertext = cryptor.encrypt(pad(content))

    return base64.urlsafe_b64encode(
        iv
        + (str(int(time.time() + expires)) if expires else str(0) * 10).encode()
        + ciphertext
    ).decode()


def decrypt(content, key="1234567890"):
    """
    解密
    @param 解密内容
    @param key
    """
    ciphertext = base64.urlsafe_b64decode(content)
    iv = ciphertext[0 : AES.block_size]
    expires = int(ciphertext[AES.block_size : AES.block_size + 10])
    if expires and expires <= int(time.time()):
        return ""

    ciphertext = ciphertext[AES.block_size + 10 : len(ciphertext)]
    cryptor = AES.new(pad(key), AES.MODE_CBC, iv)
    plaintext = cryptor.decrypt(ciphertext).decode()

    return plaintext.rstrip(chr(0))
