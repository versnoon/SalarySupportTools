#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   gz_export_model.py
@Time    :   2021/02/20 17:17:34
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from salary_support_tools.model.export.base_excel_export_model import BaseExcelExportModel
from salary_support_tools.model.export.export_column import ExportColumn


class JjExport(BaseExcelExportModel):

    def __init__(self, period, datas):
        super().__init__(period, self.cols(), datas)

    def cols(self):
        cols = []
        cols.append(ExportColumn(code="_code", name="员工通行证"))
        cols.append(ExportColumn(code="_name", name="员工姓名"))
        cols.append(ExportColumn(code="_depart_fullname", name="机构"))
        cols.append(ExportColumn(code="_distributionMark", name="是否代发工资"))
        cols.append(ExportColumn(code="_ysjse", name="应税计算额(优惠税率)"))
        cols.append(ExportColumn(code="_bonusTwo", name="单项奖2"))
        cols.append(ExportColumn(code="_gtsyj", name="个调税(应缴)"))
        cols.append(ExportColumn(code="_pay", name="实发"))
        cols.append(ExportColumn(code="_jjhj", name="奖金合计"))
        cols.append(ExportColumn(code="_jsjseptsl", name="应税计算额(普通税率)"))
        cols.append(ExportColumn(code="_jbjj", name="基本奖金"))
        cols.append(ExportColumn(code="_gts", name="个调税"))
        cols.append(ExportColumn(code="_bonusOne", name="单项奖1"))
        cols.append(ExportColumn(code="_bonusThree", name="单项奖3"))
        cols.append(ExportColumn(code="_yseyhsl", name="应税额(优惠税率)"))
        cols.append(ExportColumn(code="_bonusThree", name="单项奖3"))
        cols.append(ExportColumn(code="_yseyhsl", name="应税额"))
        cols.append(ExportColumn(code="_totalPayable", name="应发"))
        cols.append(ExportColumn(code="_gstz", name="个税调整"))
        cols.append(ExportColumn(code="_gcjj", name="工程津贴"))
        cols.append(ExportColumn(code="_jssc", name="技术输出"))
        cols.append(ExportColumn(code="_qt", name="争取国家政策奖"))
        cols.append(ExportColumn(code="_nddx", name="年底兑现奖"))
        cols.append(ExportColumn(code="_jsjj", name="计税奖金"))
        cols.append(ExportColumn(code="_zxj", name="重点工作专项奖"))
        cols.append(ExportColumn(code="_ryj", name="荣誉类奖"))
        return cols

    def get_filename(self):
        return "奖金信息"
