# coding: utf-8
from setuptools import find_packages, setup

setup(
    name="utils4py",
    version="0.0.31",
    packages=find_packages(),
    include_package_data=True,
    url="https://github.com/kbrownehs18/utils4py",
    license="MPL",
    author="last911",
    author_email="scnjl@qq.com",
    description="Python tools",
    install_requires=["sqlalchemy", "pycryptodome", "flask-wtf", "pillow", "captcha"],
)
