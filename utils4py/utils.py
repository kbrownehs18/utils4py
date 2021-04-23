#!/usr/bin/env python
# coding: utf-8

import base64
import hashlib
import os
import random
import re
import time
import json

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


def json_encode(data):
    return json.dumps(data, ensure_ascii=False)


def json_decode(s):
    return json.loads(s)


def authcode(text, decrypt=True, key="", expiry=0, ckey_length=0):
    """
    Discuz authcode
    Default: Decrypt
    """
    # 动态密钥长度
    ckey_length = ckey_length or 8
    # 生成密钥
    key = md5(
        ("" if key == "nil" else key) if key else "abcdefghijklmnopqrstuvwxyz0123456789"
    )
    # 密钥A用于加密
    key_a = md5(key[0:16])
    # 密钥B用于验证
    key_b = md5(key[16:])
    # 密钥C，生成动态密码部分
    # 解密的时候获取需要解密的字符串前面的ckey_length长度字符串
    # 加密的时候，用当前时间戳的微妙数md5加密的最后ckey_length长度字符串
    key_c = text[0:ckey_length] if decrypt else md5(str(time.time()))[-ckey_length:]
    # 用于计算的密钥
    crypt_key = key_a + md5(key_a + key_c)
    key_length = len(crypt_key)

    text = (
        base64_decode(text[ckey_length:], "unicode-escape", errors="ignore")
        if decrypt
        else (
            ("%010d" % ((int(time.time()) + expiry) if expiry else 0))
            + md5(text + key_b)[0:16]
            + text
        )
    )

    text_length = len(text)
    box = list(range(256))

    result = ""
    rndkey = [ord(crypt_key[i % key_length]) for i in range(256)]

    j = 0
    for i in range(256):
        j = (j + box[i] + rndkey[i]) % 256
        box[i], box[j] = box[j], box[i]

    a, j = 0, 0
    for i in range(text_length):
        a = (a + 1) % 256
        j = (j + box[a]) % 256
        box[a], box[j] = box[j], box[a]
        result += chr(ord(text[i]) ^ (box[(box[a] + box[j]) % 256]))

    if decrypt:
        t = int(result[0:10])
        return (
            result[26:]
            if (t == 0 or (t - int(time.time())) > 0)
            and result[10:26] == md5(result[26:] + key_b)[0:16]
            else ""
        )

    return key_c + base64.b64encode(bytes([ord(c) for c in result])).decode()


def base64_pad(text):
    x = len(text) * 3 % 4
    text += "=" * x if x in [1, 2] else ""

    return text


def base64_encode(text, encoding="utf-8", errors="strict"):
    return base64.b64encode(text.encode(encoding, errors)).decode(encoding, errors)


def base64_decode(text, encoding="utf-8", errors="strict"):
    return base64.b64decode(base64_pad(text).encode(encoding, errors)).decode(
        encoding, errors
    )
