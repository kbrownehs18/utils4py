# coding: utf-8
from setuptools import setup, find_packages

setup(
    name='myutil',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/LastSync/myutil',
    license='MPL',
    author='last911',
    author_email='last911@qq.com',
    description='Python tools',
    install_requires=[
        'sqlalchemy',
        'pycrypto'
    ]
)
