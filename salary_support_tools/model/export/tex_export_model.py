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


class TexExport(BaseExcelExportModel):

    def __init__(self, period, datas):
        super().__init__(period, self.cols(), datas, convertor=TexInfoConventor())

    def cols(self):
        cols = []
        cols.append(ExportColumn(code="_code", name="工号"))
        cols.append(ExportColumn(code="_name", name="*姓名"))
        cols.append(ExportColumn(code="_certificateType", name="*证件类型"))
        cols.append(ExportColumn(code="_idno", name="*证件号码"))
        cols.append(ExportColumn(code="_totalpayable", name="本期收入"))
        cols.append(ExportColumn(code="_notexpay", name="本期免税收入"))
        cols.append(ExportColumn(code="_yl", name="基本养老保险费"))
        cols.append(ExportColumn(code="_yil", name="基本医疗保险费"))
        cols.append(ExportColumn(code="_sy", name="失业保险费"))
        cols.append(ExportColumn(code="_gjj", name="住房公积金"))
        cols.append(ExportColumn(code="_znjj", name="累计子女教育"))
        cols.append(ExportColumn(code="_jxjj", name="累计继续教育"))
        cols.append(ExportColumn(code="_zfdkll", name="累计住房贷款利息"))
        cols.append(ExportColumn(code="_zfzj", name="累计住房租金"))
        cols.append(ExportColumn(code="_ljsylr", name="累计赡养老人"))
        cols.append(ExportColumn(code="_nj", name="企业(职业)年金"))
        cols.append(ExportColumn(code="_syjkx", name="商业健康保险"))
        cols.append(ExportColumn(code="_syylbx", name="税延养老保险"))
        cols.append(ExportColumn(code="_qt", name="其他"))
        cols.append(ExportColumn(code="_zykc", name="准予扣除的捐赠额"))
        cols.append(ExportColumn(code="_jmse", name="减免税额"))
        cols.append(ExportColumn(code="_bz", name="备注"))
        return cols

    def export(self):
        self.export_by_depart("{}_{}".format(
            self._period.period, "税款计算_工资薪金所得"))


class TexSpecialExport(BaseExcelExportModel):

    def __init__(self, period, datas):
        super().__init__(period, self.cols(),
                         datas, convertor=TexSpecialInfoConventor())

    def cols(self):
        cols = []
        cols.append(ExportColumn(code="_code", name="工号"))
        cols.append(ExportColumn(code="_name", name="*姓名"))
        cols.append(ExportColumn(code="_certificateType", name="*证件类型"))
        cols.append(ExportColumn(code="_idno", name="*证件号码"))
        cols.append(ExportColumn(code="_totalpayable", name="*全年一次性奖金额"))
        cols.append(ExportColumn(code="_notexpay", name="免税收入"))
        cols.append(ExportColumn(code="_qt", name="其他"))
        cols.append(ExportColumn(code="_zykc", name="准予扣除的捐赠额"))
        cols.append(ExportColumn(code="_jmse", name="减免税额"))
        cols.append(ExportColumn(code="_bz", name="备注"))
        return cols

    def export(self):
        self.export_by_depart("{}_{}".format(
            self._period.period, "税款计算_全年一次性奖金收入"))
