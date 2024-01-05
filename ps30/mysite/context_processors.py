#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: wenlong.jin
@File: context_processors.py.py
@Project: ps30
@Time: 2023/7/3 13:43
"""
from django.conf import settings


def global_site_name(request):
    return {'site_name': settings.SITE_NAME, }
