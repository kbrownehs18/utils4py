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


def response(code=0, data={}, msg="", http_code=200, **kwargs):
    """
    return flask json response
    """
    rtn = {"code": code}
    if data:
        rtn["data"] = data

    if msg:
        rtn["msg"] = msg

    if kwargs:
        rtn = rtn.update(kwargs)

    return jsonify(rtn), http_code
