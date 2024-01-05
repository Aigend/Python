"""
@Project: full
@File: test_aa_12206.py
@Author: wenlong.jin
@Time: 2023/11/29 16:30
@version: 1.0.0
@Description:
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest


@pytest.fixture(scope="session", autouse=False)
def prepare():
    print("prepare")


@pytest.fixture(params=[str(107000 + i) for i in range(151)], scope="function", autouse=False)
def check_point(request, charge):
    """

    :param request:
    :param charge:
    :return:
    """
    return request.param


# def test_bbb_14028(prepare, check_point):
#     """
#
#     :param check_point:
#     :return:
#     """
#     print("test 0000", prepare, "djsf")
#     print(test_bbb_14028.__doc__)