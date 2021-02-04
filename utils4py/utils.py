#!/usr/bin/env python
# coding: utf-8

import base64
import hashlib
import os
import random
import re
import time

from Crypto import Random
from Crypto.Cipher import AES
from sqlalchemy import DateTime, Numeric


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


def sha256bytes(bs):
    """
    sha256
    """
    hash = hashlib.sha256()
    hash.update(bs)
    return hash.hexdigest()


def sha256(strs):
    return sha256bytes(strs.encode("utf-8"))


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
    return True if re.match("^1[3-9]{1}[0-9]{9}$", phone_number) else False


def model_to_dict(model):
    """
    model to dict
    """

    def convert_datetime(value):
        return (
            (
                value.strftime("%Y-%m-%d %H:%M:%S")
                if hasattr(value, "strftime")
                else value
            )
            if value
            else ""
        )

    data = {}
    for col in model.__table__.columns:
        value = getattr(model, col.name)
        if isinstance(col.type, DateTime):
            value = convert_datetime(value)
        elif isinstance(col.type, Numeric):
            value = str(value)
             
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


pad = lambda s: (
    s
    + (
        AES.block_size
        - (
            16
            if (len(s) % AES.block_size == 0 and len(s) != 0)
            else (len(s) % AES.block_size)
        )
    )
    * chr(0)
).encode("utf-8")


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


def get_items(items) -> list:
    """
    get all items
    """

    def calculate(lst):
        t = type(lst)
        if t in [list, tuple]:
            for item in lst:
                calculate(item)
        elif t == dict:
            for _, item in lst.items():
                calculate(item)
        else:
            result.append(lst)
            return

    result = []
    calculate(items)
    return result

