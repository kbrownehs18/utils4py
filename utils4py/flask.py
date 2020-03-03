#!/usr/bin/env python
# coding: utf-8

from datetime import date, datetime

from flask import jsonify
from flask.json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):
    """
    JSON Encoder format
    """

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(obj, date):
                return obj.strftime("%Y-%m-%d")
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)

        return JSONEncoder.default(self, obj)
