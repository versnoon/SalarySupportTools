#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_runner.py
@Time    :   2021/01/19 11:16:03
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''
from salary_support_tools import runner


class TestRunner(object):
    """
    docstring
    """

    def test_start(self):
        assert "running" == runner.start()
