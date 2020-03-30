#!/usr/bin/env python
# coding: utf-8

import logging
import time
import unittest

from utils4py import utils


class TestUtils(unittest.TestCase):
    def test_utils(self):
        self.assertEqual("png" == utils.extension("image.png"), True)

        self.assertEqual(utils.check_phone_number("13000000000"), True)

    def test_aes(self):
        content = "jintian shige haotianqi buzhidao duibudui?"
        en = utils.encrypt(content)
        de = utils.decrypt(en)
        self.assertEqual(de == content, True)

        key = utils.md5(str(time.time()))
        en = utils.encrypt(content, key=key)
        de = utils.decrypt(en, key=key)
        self.assertEqual(de == content, True)

        en = utils.encrypt(content, key="abcde", expires=-1)
        de = utils.decrypt(en, key="abcde")
        self.assertEqual(de == content, False)

        en = utils.encrypt(content, key="abcde", expires=10)
        de = utils.decrypt(en, key="abcde")
        self.assertEqual(de == content, True)

        en = utils.encrypt(content, key="abcde", expires=2)
        time.sleep(3)
        de = utils.decrypt(en, key="abcde")
        self.assertEqual(de == content, False)

    def test_md5bytes(self):
        en = utils.md5bytes("abc".encode())

        self.assertEqual(en == utils.md5("abc"), True)

    def test_get_items(self):
        m = {"name": "scnjl", "age": 40}
        print(utils.get_items(m))

        errors = {"password": ["请输入密码"], "username": ["请输入用户名"]}
        print(utils.get_items(errors))

        a = [
            [(55736,)],
            [(55739,)],
            [(55740,), (55801,)],
            [(55748,)],
            [(55783,), (55786,), (55787,), (55788,)],
            [(55817,), (55821,)],
            [(55818,)],
        ]
        print(utils.get_items(a))
    
    def test_captcha(self):
        r, img = utils.captcha()

        print(r, img)


if __name__ == "__main__":
    unittest.main()
