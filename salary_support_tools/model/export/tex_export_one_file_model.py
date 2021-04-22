#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   gz_export_model.py
@Time    :   2021/02/20 17:17:34
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from salary_support_tools.model.export.base_excel_export_model import BaseExcelExportModel, TexInfoConventor, TexSpecialInfoConventor
from salary_support_tools.model.export.export_column import ExportColumn
from salary_support_tools.model.export.tex_export_model import TexExport, TexSpecialExport


class TexOneFileExport(BaseExcelExportModel):

    def __init__(self, period, datas):
        super().__init__(period, TexExport(period, datas).cols(),
                         datas, convertor=TexInfoConventor())

    def export_by_depart(self):
        for tex_depart, datas_by_tex_depart in self._datas.items():
            filepath = self.get_datas_by_tex_depart_export_path(tex_depart)
            self.create_excel_file(
                self.get_datas_by_tex_depart(
                    tex_depart), filepath, '{}_{}_{}'.format(self._period.period, tex_depart, self.get_filename()), self._cols)

    def get_filename(self):
        return "工资薪金所得"


class TexSpecialOneFileExport(BaseExcelExportModel):

    def __init__(self, period, datas):
        super().__init__(period, TexSpecialExport(period, datas).cols(),
                         datas, convertor=TexSpecialInfoConventor())

    def export_by_depart(self):
        for tex_depart, datas_by_tex_depart in self._datas.items():
            filepath = self.get_datas_by_tex_depart_export_path(tex_depart)
            self.create_excel_file(
                self.get_datas_by_tex_depart(
                    tex_depart), filepath, '{}_{}_{}'.format(self._period.period, tex_depart, self.get_filename()), self._cols)

    def get_filename(self):
        return "全年一次性奖金收入"
