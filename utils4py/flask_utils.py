#!/usr/bin/env python
# coding: utf-8

from datetime import date, datetime

from flask import jsonify, request
from flask.json import JSONEncoder
from flask_wtf import FlaskForm
from wtforms.validators import StopValidation

from .utils import get_items
from decimal import Decimal

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
            elif isinstance(obj, Decimal):
                return float(obj)
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
        rtn.update(kwargs)

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


def validate(validate_form=None, upload=False):
    """
    form validate decorator
    """

    def form_check(fn):
        def wrapper(*args, **kwargs):
            form = validate_form(
                data=request.args
                if request.method == "GET"
                else (get_json() if not upload else request.form)
            )

            if not form.validate():
                return response(code=90001, msg=form.get_error_message())
            kwargs.update({"form": form})
            return fn(*args, **kwargs)

        return wrapper

    return form_check


def form_validate(validate_form=None, methods=["POST"]):
    """
    form validate decorator
    """

    def form_check(fn):
        def wrapper(*args, **kwargs):
            if request.method not in methods:
                return fn(*args, **kwargs)

            form = validate_form(
                data=request.args if request.method == "GET" else get_json()
            )
            if not form.validate():
                return response(code=999, msg=form.get_error_message())

            kwargs.update({"form": form})
            return fn(*args, **kwargs)

        return wrapper

    return form_check


class NotEmpty(object):
    field_flags = ("not_empty",)

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if "password" not in field.name and isinstance(field.data, str):
            field.data = field.data.strip()

        if not field.data:
            if self.message is None:
                message = field.gettext("This field is be not empty.")
            else:
                message = self.message

            field.errors[:] = []
            raise StopValidation(message)
