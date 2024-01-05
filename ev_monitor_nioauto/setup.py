#!/usr/bin/python
# coding=utf-8
import os

import setuptools

with open(os.path.join(os.path.dirname(__file__), 'nio_message_readme.md')) as readme:
    README = readme.read()

setuptools.setup(
    name='nio_messages',
    version='0.1.36',
    keywords='nio_messages',
    description='nio protobuf packages',
    long_description=README,
    author='li.liu',
    author_email='li.liu2@nio.com',

    url='',
    packages=setuptools.find_packages(),
    license='BSD License',
    zip_safe=True,  # 设定项目包为安全，不用每次都检测其安全性
    include_package_data=True,  # 启用清单文件MANIFEST.in,打包其中的非py的静态资源
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: >3.0'],
    python_requires='>=3',
    install_requires=[
        'protobuf>=3.6.1',
        'PyYAML==5.1',
        'confluent-kafka==0.11.6',
        'requests',
        'paho-mqtt==1.2'
    ]
)
