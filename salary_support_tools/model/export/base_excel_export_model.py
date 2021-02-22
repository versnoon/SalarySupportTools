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
        print("导出逻辑")

    def export_by_depart(self, filename):
        for tex_depart, datas_by_tex_depart in self._datas.items():
            for depart, datas_by_depart in datas_by_tex_depart.items():
                filepath = self.get_test_export_path(depart)
                self.create_excel_file(
                    self.get_datas(
                        tex_depart, depart), filepath, filename, self._cols)

    def base_export_folder_path_prefix(self):
        return r'd:\薪酬审核文件夹'

    def base_test_export_folder_path_prefix(self):
        return r'{}\{}'.format(self.base_export_folder_path_prefix(), 'test')

    def get_test_export_path(self, foldername):
        path = self.base_test_export_folder_path_prefix()
        period = self._period.period
        path = join(path, period)
        if foldername:
            path = join(path, foldername)
        if not exists(path):
            makedirs(path)
        return path

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
        datas = []
        if tex_depart in self._datas:
            if depart in self._datas[tex_depart]:
                datas = self._datas[tex_depart][depart].values()
        return datas

    def create_excel_file(self, datas, filepath, filename, cols):
        """
        创建excel
        """
        b = xlwt.Workbook(encoding='uft-8')
        s = b.add_sheet('Sheet1')

        # 写入标题
        for i, v in enumerate(cols):
            s.write(0, i, v._name)
        for i, v in enumerate(datas):
            data = self._convertor.cov(v)
            for j, col in enumerate(cols):
                propertyName = col._code
                try:
                    s.write(
                        i+1, j, getattr(data, propertyName, 0))
                except TypeError:
                    pass
        b.save(r'{}\{}{}'.format(filepath, filename, self.EXT))


class SapInfoConventor(PersonSalaryConventor):

    def cov(self, data):
        return data[1]
