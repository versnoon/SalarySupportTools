#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   runner.py
@Time    :   2021/02/23 13:52:45
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


from salary_support_tools.excel.model_2_xls import ModelToXls
from salary_support_tools.model.export.base_excel_export_model import BaseExcelExportModel
from salary_support_tools.model.export.gz_export_model import GzExport
from salary_support_tools.model.export.jj_export_model import JjExport
from salary_support_tools.model.export.auditor_export_model import AuditorExport
from salary_support_tools.model.export.sh002_export_model import Sh002Export
from salary_support_tools.model.export.sh003_export_model import Sh003Export
from salary_support_tools.model.export.tex_export_model import TexExport, TexSpecialExport
from salary_support_tools.model.export.err_message_export_model import ErrMessageExport
from salary_support_tools.model.export.sh003_export_by_tex_depart_model import Sh003ByTexDepartExport
from salary_support_tools.engine.load_tpls_engine import LoadTplEngine


class Runner:

    def run(self):
        load_engine = LoadTplEngine()
        period, departs = load_engine.load_current_period_departs()
        # 准备数据
        period, departs, persons, jobs, gzs, jjs, banks, texes, merge_infos = load_engine.load_tpl_by_period(
            period)

        # 执行导出
        util = ModelToXls([GzExport(period, gzs), JjExport(
            period, jjs), AuditorExport(period, merge_infos), Sh002Export(period, merge_infos), Sh003Export(period, merge_infos), TexExport(period, merge_infos), TexSpecialExport(period, merge_infos), ErrMessageExport(period, merge_infos), Sh003ByTexDepartExport(period, merge_infos)])
        util.export()
