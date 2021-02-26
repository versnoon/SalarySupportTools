#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   person_compare_runner.py
@Time    :   2021/02/25 13:42:53
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from salary_support_tools.engine.person_compare_engine import PersonCompareEngine


class PersonCompareRunner:

    def run(self):
        compare_engine = PersonCompareEngine()
        datas = compare_engine.compare()
        print("ok")
