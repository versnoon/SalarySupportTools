#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tex_xls_2_model.util.py
@Time    :   2021/02/18 16:51:35
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from collections import OrderedDict

from salary_support_tools.model.base_excel_import_model import BaseExcelImportModel
from salary_support_tools.model.salary_tex import SalaryTex
from salary_support_tools.excel.xls_2_model_util import XlsToModelUtil


class TexXlsToModelUtil:

    def __init__(self, period, departs, persons, gzs, jjs):
        self.period = period
        self.departs = departs
        self.persons = persons
        self.gzs = gzs
        self.jjs = jjs

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
        texes = util.load_tpls()
        return self.get_person_tex_info(texes, self.persons, self.gzs, self.jjs)

    def get_tex_departs(self, departs):
        # 从机构信息中获取税务机构信息并分组
        res = dict()
        for depart in departs.values():
            if depart.texdepart not in res:
                res[depart.texdepart] = depart.texdepart
        return res

    def get_person_tex_info(self, texes, persons, gzs, jjs):
        person_by_code = persons[0]  # 按照职工代码分组
        person_by_idno = persons[1]  # 按照身份证分组
        res_tex_depart = OrderedDict()
        res_depart = OrderedDict()
        for data_key, datas in texes.items():
            # 获取税务机构信息
            tex_depart = ""
            if data_key.startswith("s_tex_"):
                tex_depart = data_key[len("s_tex_"):]
            if data_key.startswith("s_one_tex_"):
                tex_depart = data_key[len("s_one_tex_"):]
            for data in datas:
                vs_tex_depart = dict()
                vs_depart = dict()
                vs = dict()
                idno = data._idno  # 身份证信息
                depart, person = self.get_person_by_idno(
                    tex_depart, idno, person_by_idno)  # 机构和人员信息
                if tex_depart in res_tex_depart:
                    vs_tex_depart = res_tex_depart[tex_depart]
                person_key = idno

                if person:
                    person_key = person._code

                if not depart:
                    depart = self.get_person_depart_name(
                        tex_depart, person_key, gzs, jjs)
                if depart in res_depart:
                    vs_depart = res_depart[depart]

                if person_key in vs_depart:
                    vs = vs_depart[person_key]
                if data_key.startswith("s_tex_"):
                    vs["s_tex"] = data
                if data_key.startswith("s_one_tex_"):
                    vs["s_one_tex"] = data
                vs_depart[person_key] = vs
                vs_tex_depart[depart] = vs_depart
                res_depart[depart] = vs_depart
                res_tex_depart[tex_depart] = vs_tex_depart
        return res_tex_depart

    def get_person_by_idno(self, tex_depart, idno, persons_by_idno):
        if tex_depart in persons_by_idno:
            persons = persons_by_idno[tex_depart]
            for depart, persons_by_depart in persons.items():
                if idno in persons_by_depart:
                    return depart, persons_by_depart[idno]
        # 在减员类找
        if "unknow" in persons_by_idno:
            if "unknow" in persons_by_idno["unknow"]:
                if idno in persons_by_idno["unknow"]["unknow"]:
                    return "", persons_by_idno["unknow"]["unknow"][idno]
        return "", None

    def get_person_depart_name(self, tex_depart, code, gzs, jjs):
        depart_name = "unknow"
        if tex_depart in gzs:
            for tex_depart, gzs_tex_depart in gzs.items():
                for depart, gzs_depart in gzs_tex_depart.items():
                    if code in gzs_depart:
                        depart_name = depart
                        break
        if depart_name == "unknow":
            if tex_depart in jjs:
                for tex_depart, jjs_tex_depart in jjs.items():
                    for depart, jjs_depart in jjs_tex_depart.items():
                        if code in jjs_depart:
                            depart_name = depart
                            break
        return depart_name
