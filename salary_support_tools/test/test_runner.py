#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_runner.py
@Time    :   2021/01/19 11:16:03
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''
import pytest
from  salary_support_tools import runner 


class TestRunner(object):
    """
    docstring
    """
    assert runner.start() == "func runner"