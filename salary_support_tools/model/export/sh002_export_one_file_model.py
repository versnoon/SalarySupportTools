#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   gz_export_model.py
@Time    :   2021/02/20 17:17:34
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from salary_support_tools.model.export.base_excel_export_model import BaseExcelExportModel, SapInfoConventor
from salary_support_tools.model.export.export_column import ExportColumn
from salary_support_tools.model.export.sh002_export_model import Sh002Export


class Sh002OneFileExport(BaseExcelExportModel):

    def __init__(self, period, datas):
        super().__init__(period, Sh002Export(period, datas).cols(),
                         datas, convertor=SapInfoConventor())

    def export_by_depart(self):

        filepath = self.get_datas_by_tex_depart_export_path("")
        self.create_excel_file(
            self.get_datas_all(), filepath, '{}_{}'.format(self._period.period, self.get_filename()), self._cols)

    def get_filename(self):
        return "sh002"
