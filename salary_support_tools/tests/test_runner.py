#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_runner.py
@Time    :   2021/02/23 17:29:21
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

import pytest

# from salary_support_tools.runner.runner import Runner
# from salary_support_tools.model.salary_period import SalaryPeriod
# from salary_support_tools.model.salary_tex import SalaryTex
# from salary_support_tools.model.sap_salary_info import SapSalaryInfo
# from salary_support_tools.model.err_message import ErrMessage
# from salary_support_tools.model.export.base_excel_export_model import BaseExcelExportModel
# from salary_support_tools.model.export.err_message_export_model import ErrMessageExport
# from salary_support_tools.engine.load_tpls_engine import LoadTplEngine
from salary_support_tools.runner.tex_runner import TexRunner


class TestRunner:

    def test_compare_tex(self):
        runner = TexRunner()
        runner.run()
