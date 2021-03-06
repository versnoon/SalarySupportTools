#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   base_excel_export_model.py
@Time    :   2021/02/20 15:19:10
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from os.path import join, exists
from os import makedirs

import xlwt

from salary_support_tools.model.person_salary_cov import PersonSalaryConventor


class BaseExcelExportModel:
    """
    导出业务模型基类
    """

    NAME = "export"
    EXT = ".xls"

    def __init__(self, period, cols, datas, foldername="", filename="", convertor: PersonSalaryConventor = None, departs=None):
        self._cols = cols  # excel列与模型属性之间得对应数组
        self._foldername = foldername  # 导出文件的文件夹名称
        self._filename = filename  # 导出文件名称
        if not convertor:
            convertor = PersonSalaryConventor()
        self._convertor = convertor  # 转换函数
        self._period = period  # 期间
        self._datas = datas  # 原始数据

    def export(self):
        self.export_by_depart()

    def export_by_depart(self):
        for tex_depart, datas_by_tex_depart in self._datas.items():
            for depart, datas_by_depart in datas_by_tex_depart.items():
                datas = self.get_datas(
                    tex_depart, depart)
                if len(datas) > 0:
                    filepath = self.get_export_path(depart)
                    self.create_excel_file(
                        datas, filepath, '{}_{}_{}'.format(self._period.period, depart, self.get_filename()), self._cols)

    def export_datas_by_depart(self, datas):
        for tex_depart, datas_by_tex_depart in datas.items():
            for depart, datas_by_depart in datas_by_tex_depart.items():
                ds = self.get_datas_1(datas,
                                      tex_depart, depart)
                if len(ds) > 0:
                    filepath = self.get_export_path(depart)

                    self.create_excel_file(ds, filepath, '{}_{}_{}'.format(
                        self._period.period, depart, self.get_filename()), self._cols)

    def base_export_folder_path_prefix(self):
        return r'd:\薪酬审核文件夹'

    def get_filename(self):
        if self._filename:
            return self._filename
        return "导出文件"

    def get_sheetname(self):
        return "Sheet1"

    def get_export_path(self, foldername):
        path = self.base_export_folder_path_prefix()
        period = self._period.period
        path = join(path, period)
        if foldername:
            path = join(path, foldername)
        if not exists(path):
            makedirs(path)
        return path

    def get_datas(self, tex_depart, depart):
        return self.get_datas_1(self._datas, tex_depart, depart)

    def get_datas_1(self, datas, tex_depart, depart):
        res = []
        if tex_depart in datas:
            if depart in datas[tex_depart]:
                res = datas[tex_depart][depart].values()
        return res

    def get_datas_2(self, datas, tex_depart, depart):
        res = []
        if tex_depart in datas:
            if depart in datas[tex_depart]:
                res = datas[tex_depart][depart]
        return res

    def get_datas_by_tex_depart_export_path(self, foldername):
        path = self.base_export_folder_path_prefix()
        period = self._period.period
        path = join(path, period, "汇总数据")
        if foldername:
            path = join(path, foldername)
        if not exists(path):
            makedirs(path)
        return path

    def get_datas_all(self):
        datas = []
        for tex_depart, datas_by_tex_depart in self._datas.items():
            for depart, datas_by_departs in datas_by_tex_depart.items():
                datas.extend(self._datas[tex_depart][depart].values())
        return datas

    def get_datas_by_tex_depart(self, tex_depart, datas=None):
        if not datas:
            datas = self._datas
        ds = []
        if tex_depart in datas:
            for depart, datas_by_departs in datas[tex_depart].items():
                ds.extend(datas[tex_depart][depart].values())
        return ds

    def get_datas_by_tex_depart_2(self, tex_depart, datas=None):
        if not datas:
            datas = self._datas
        ds = []
        if tex_depart in datas:
            ds.extend(datas[tex_depart])
        return ds

    def create_excel_file(self, datas, filepath, filename, cols):
        """
        创建excel
        """
        b = xlwt.Workbook(encoding='uft-8')
        s = b.add_sheet(self.get_sheetname())

        # 写入标题
        for i, v in enumerate(cols):
            s.write(0, i, v._name)
        row_index = 0
        for v in datas:
            data = self._convertor.cov(v)
            if data:
                for j, col in enumerate(cols):
                    propertyName = col._code
                    try:
                        if data:
                            s.write(
                                row_index + 1, j, getattr(data, propertyName, 0))
                    except TypeError:
                        pass
                row_index += 1
        b.save(r'{}\{}{}'.format(filepath, filename, self.EXT))


class SapInfoConventor(PersonSalaryConventor):

    def cov(self, data):
        return data[1]


class TexInfoConventor(PersonSalaryConventor):

    def cov(self, data):
        return data[2]


class TexSpecialInfoConventor(PersonSalaryConventor):

    def cov(self, data):
        return data[3]


class ErrorMessageConventor(PersonSalaryConventor):

    def cov(self, data):
        return data[4]
