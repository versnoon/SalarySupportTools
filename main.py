#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2021/01/20 11:18:31
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from salary_support_tools import ehr_engine

if __name__ == "__main__":
    persons, period, departs = ehr_engine.EhrEngine().initven()
    if len(persons) > 0:
        ehr_engine.EhrEngine().start(persons, period, departs)
