#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   SalaryPeriod.py
@Time    :   2021/02/13 11:48:32
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


class SalaryPeriod(object):
    """
    期间信息 包含 年 月
    """

    def __init__(self, year: int, month: int):
        self.__year: int = year  # 年
        self.__month: int = month  # 月

    @property
    def year(self):
        if not self.year_validator(self.__year):
            raise(ValueError("期间设置错误,年信息出错{}".format(self.__year)))
        return self.__year

    @ property
    def month(self):
        if not self.month_validator(self.__month):
            raise(ValueError("期间设置错误,月信息出错{}".format(self.__month)))
        return self.__month

    @ property
    def period(self):
        return self.get_period_str(self.__year, self.__month)

    def get_period_str(self, year: int, month: int):
        """
        返回yyyyMM格式化期间字符串
        """
        if self.year_validator(year) and self.month_validator(month):
            return "{:0>4d}{:0>2d}".format(year, month)
        return None

    def year_validator(self, year):
        if year < 0:
            return False
        return True

    def month_validator(self, month):
        if self.__month < 0 or self.__month > 12:
            return False
        return True

    def __str__(self):
        return self.get_period_str(self.__year, self.__month)
