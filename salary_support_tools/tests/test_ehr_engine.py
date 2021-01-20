#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_ehr_engine.py
@Time    :   2021/01/19 15:37:35
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

import pytest
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
        assert 'ehr' == engine._name

    def test_getColumnDef(self, ):
        """
        docstring
        """
        personInfo = ehr_engine.PersonInfo()
        columns = personInfo.getColumnDef()
        assert len(columns) > 0
        assert columns['_code'] == "职工编码"
        with pytest.raises(KeyError):
            columns['code']

    def test_getPropertyName(self,):
        personInfo = ehr_engine.PersonInfo()
        propertyName = personInfo.getPropertyName("职工编码")
        assert '_code' == propertyName

        errProperName = personInfo.getPropertyName("映射以外的说明")
        assert '' == errProperName
