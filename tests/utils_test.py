#!/usr/bin/env python
# coding: utf-8

import logging
import time
import unittest

from utils4py import utils


class TestUtils(unittest.TestCase):
    def test_utils(self):
        self.assertEqual("png" == utils.extension("image.png"), True)

        self.assertEqual(utils.check_phone_number("13550009575"), True)

    def test_aes(self):
        content = "scnjl"
        en = utils.encrypt(content)
        de = utils.decrypt(en)
        self.assertEqual(de == content, True)

        en = utils.encrypt(content, key="abcde")
        de = utils.decrypt(en, key="abcde")
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


if __name__ == "__main__":
    unittest.main()
