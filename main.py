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
    persons, salaryGzs, salaryJjs = ehr_engine.EhrEngine().start()
    print(persons[0])
    print(salaryGzs[0])
    print(salaryJjs[0])
