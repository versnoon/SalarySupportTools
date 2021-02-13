#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   base_period_engine.py
@Time    :   2021/02/13 15:13:57
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from salary_support_tools.engine.base_engine import BaseEngine
from salary_support_tools.model.salary_period import SalaryPeriod


class BasePeriodEngine(BaseEngine):

    def __init__(self, name: str, period: SalaryPeriod):
        super().__init__(name)
        self.__period = period

    @property
    def period(self):
        return self.__period
