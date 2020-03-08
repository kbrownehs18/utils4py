#!/usr/bin/env python
# coding: utf-8

from datetime import date, datetime

from flask import jsonify, request
from flask.json import JSONEncoder
from flask_wtf import FlaskForm

from .utils import get_items


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


def get_json(force=True, silent=True, cache=True):
    """
    wrap flask request get_json
    """
    return request.get_json(force=force, silent=silent, cache=cache)


class Form(FlaskForm):
    def get_error_message(self):
        """
        return first error message
        """
        messages = get_items(self.errors)
        return None if not messages else messages[0]
