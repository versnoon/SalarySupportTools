#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tex_xls_2_model.util.py
@Time    :   2021/02/18 16:51:35
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from salary_support_tools.model.base_excel_import_model import BaseExcelImportModel
from salary_support_tools.model.salary_tex import SalaryTex
from salary_support_tools.excel.xls_2_model_util import XlsToModelUtil


class TexXlsToModelUtil:

    def __init__(self, period, departs):
        self.period = period
        self.departs = departs

    def load_tex_tpls(self):
        """
        加载税务系统数据
        """
        tex_departs = self.get_tex_departs(self.departs)
        res = dict()
        for tex_depart in tex_departs:
            res = dict(res, **self.load_tex_tpl(tex_depart))
        return res

    def load_tex_tpl(self, tex_depart):
        """
        加载单个公司税务数据
        """
        s_tex_model = BaseExcelImportModel(
            "s_tex_{}".format(tex_depart), SalaryTex, SalaryTex.cols(), '{}_税款计算_工资薪金所得'.format(self.period.period), '',  period=self.period, departs=self.departs, filefoldername=r'{}\{}'.format('税务相关数据', tex_depart))
        s_one_tex_model = BaseExcelImportModel(
            "s_one_tex_{}".format(tex_depart), SalaryTex, SalaryTex.cols(), '{}_税款计算_全年一次性奖金收入'.format(self.period.period), '', period=self.period, departs=self.departs, filefoldername=r'{}\{}'.format('税务相关数据', tex_depart))
        util = XlsToModelUtil([s_tex_model, s_one_tex_model])
        return util.load_tpls()

    def get_tex_departs(self, departs):
        # 从机构信息中获取税务机构信息并分组
        res = dict()
        for depart in departs.values():
            if depart.texdepart not in res:
                res[depart.texdepart] = depart.texdepart
        return res
