#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   err_message_export_model.py
@Time    :   2021/02/23 08:43:50
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


from salary_support_tools.model.export.base_excel_export_model import BaseExcelExportModel

from salary_support_tools.model.export.export_column import ExportColumn
from salary_support_tools.model.export.base_excel_export_model import ErrorMessageConventor


class ErrMessageExport(BaseExcelExportModel):

    def __init__(self, period, datas):
        super().__init__(period, self.cols(), datas, convertor=ErrorMessageConventor())

    def cols(self):
        cols = []
        cols.append(ExportColumn(code="depart", name="单位文件夹名称"))
        cols.append(ExportColumn(code="tex_depart", name="税务机构"))
        cols.append(ExportColumn(code="_code", name="员工通行证"))
        cols.append(ExportColumn(code="_name", name="员工姓名"))
        cols.append(ExportColumn(code="_ygzz", name="在职状态"))
        cols.append(ExportColumn(code="_depart_fullname", name="机构"))
        cols.append(ExportColumn(code="_err_messages", name="错误信息"))
        cols.append(ExportColumn(code="_descript", name="备注"))
        return cols

    def get_filename(self):
        return "审核错误信息"
