#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tex_runner.py
@Time    :   2021/03/01 22:31:14
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from salary_support_tools.engine.tex_compare_engine import TexCompareEngine


class TexRunner:

    def run(self):
        engine = TexCompareEngine()
        engine.compare()
