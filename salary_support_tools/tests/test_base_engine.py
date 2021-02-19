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

    def test_base_engine(self):
        name = "base"
        engine = BaseEngine()
        assert name == engine.NAME

    def test_base_period_engine(self):
        period = SalaryPeriod(2021, 2)
        name = "base_period"
        engine = BasePeriodEngine(period)
        assert name == engine.NAME
        assert engine.period.year == 2021
        assert engine.period.month == 2
