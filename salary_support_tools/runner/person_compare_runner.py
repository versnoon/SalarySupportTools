#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   person_compare_runner.py
@Time    :   2021/02/25 13:42:53
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from salary_support_tools.engine.load_tpls_engine import LoadTplEngine
from salary_support_tools.engine.person_compare_engine import PersonCompareEngine
from salary_support_tools.excel.model_2_xls import ModelToXls
from salary_support_tools.model.export.person_compare_export_model import PersonCompareExport


class PersonCompareRunner:

    def run(self):
        load_engine = LoadTplEngine()
        period, _ = load_engine.load_current_period_departs()
        person_compare_engine = PersonCompareEngine()
        datas = person_compare_engine.compare()

        # 执行导出
        util = ModelToXls([PersonCompareExport(period, datas)])
        util.export()
        print("ok")
