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
    persons, salaryGzs, salaryJjs, salaryBanks = ehr_engine.EhrEngine().start()
    print(persons['MA8837'])
    print(salaryGzs['MA8837'])
    print(salaryJjs['MA8837'])
    print(salaryBanks['MA8837']['gz'])
    print(salaryBanks['MA8837']['jj'])
