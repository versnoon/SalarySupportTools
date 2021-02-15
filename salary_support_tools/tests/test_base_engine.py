#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_base_engine.py
@Time    :   2021/02/13 14:44:00
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

import pytest

from salary_support_tools.engine.base_engine import BaseEngine
from salary_support_tools.engine.base_period_engine import BasePeriodEngine
from salary_support_tools.model.salary_period import SalaryPeriod


class TestBaseEngine(object):

    def test_create_base_engine(self):
        engine = BaseEngine()
        with pytest.raises(ValueError):
            engine.name

    def test_base_engine(self):
        name = "基类"
        engine = BaseEngine(name)
        assert name == engine.name

    def test_base_period_engine(self):
        period = SalaryPeriod(2021, 2)
        name = "期间引擎"
        engine = BasePeriodEngine(name, period)
        assert name == engine.name
        assert engine.period.year == 2021
        assert engine.period.month == 2
