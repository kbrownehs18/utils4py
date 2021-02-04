#!/usr/bin/python
# coding: utf-8

import os
import random
from captcha.image import ImageCaptcha
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from .utils import random_string
from io import BytesIO

def captcha(size=4, width=240, height=60, font=None, font_size=36, noise=True):
    """
    验证码
    @param width default: 240
    @param height default: 60
    """
    image = Image.new("RGB", (width, height), (255, 255, 255))
    font = ImageFont.truetype(
        font=font
        if font
        else os.path.join(os.path.abspath(os.path.dirname(__file__)), "Arial.ttf"),
        size=font_size,
    )
    draw = ImageDraw.Draw(image)
    if noise:
        for x in range(width):
            for y in range(height):
                if random.randint(0, 1):
                    draw.point(
                        (x, y),
                        fill=(
                            random.randint(64, 255),
                            random.randint(64, 255),
                            random.randint(64, 255),
                        ),
                    )
    code = []
    remainder = width % size
    unit = int((width - remainder) / size)
    y = int((height - font_size) / 2)
    offset_x = int(remainder / 2)
    for t in range(size):
        c = random_string(1)
        code.append(c)
        draw.text(
            (unit * t + offset_x, y),
            c,
            font=font,
            fill=(
                random.randint(32, 127),
                random.randint(32, 127),
                random.randint(32, 127),
            ),
        )
    image = image.filter(ImageFilter.BLUR)

    img_io = BytesIO()
    image.save(img_io, "PNG")
    img_io.seek(0)

    return "".join(code), img_io


def captcha2():
    code = random_string(4)
    image = ImageCaptcha().generate_image(code)

    img_io = BytesIO()
    image.save(img_io, "JPEG", quality=70)
    img_io.seek(0)

    return code, img_io
