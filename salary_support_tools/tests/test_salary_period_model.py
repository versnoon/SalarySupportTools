#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_salary_period_model.py
@Time    :   2021/02/13 11:55:07
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

import pytest

from salary_support_tools.model.salary_period import SalaryPeriod


class TestSalaryPeriod(object):

    def test_create_salary_period(self):
        model = SalaryPeriod(2021, 2)
        assert model.year == 2021
        assert model.month == 2
        assert model.period == '202102'
        assert model.get_period_str(model.year, model.month)

    def test_create_salary_period_with_bad_yearmonth(self):
        model = SalaryPeriod(-1, 13)
        with pytest.raises(ValueError):
            model.year
        with pytest.raises(ValueError):
            model.month
        with pytest.raises(ValueError):
            model.year
        assert model.period is None
