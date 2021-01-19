#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_ehr_engine.py
@Time    :   2021/01/19 15:37:35
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''
from salary_support_tools import ehr_engine

class TestEhrEngine(object):
    """
    docstring
    """
    def test_engine_name(self, ):
        """
        docstring
        """
        engine = ehr_engine.EhrEngine()
        assert 'ehr'==engine._name

    def test_engine_start(self, ):
        """
        docstring
        """
        engine = ehr_engine.EhrEngine()
        assert 'tt'==engine.start()