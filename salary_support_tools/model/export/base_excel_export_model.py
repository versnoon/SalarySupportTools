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

from salary_support_tools.model.person_salary_cov import PersonSalaryConventor


class BaseExcelExportModel:
    """
    导出业务模型基类
    """

    NAME = "export"

    def __init__(self, cols, datas, foldername="", filename="", convertor: PersonSalaryConventor = None, period=None, departs=None):
        self._cols = cols  # excel列与模型属性之间得对应数组
        self._foldername = foldername  # 导出文件的文件夹名称
        self._filename = filename  # 导出文件名称
        if not convertor:
            convertor = PersonSalaryConventor()
        self._convertor = convertor  # 转换函数
        self._period = period  # 期间
        self._datas = datas  # 原始数据

    def base_export_folder_path_prefix(self):
        return r'd:\薪酬审核文件夹'

    def get_export_path(self):
        path = self.base_export_folder_path_prefix()
        period = self._period.period
        path = join(path, period)
        foldername = self._foldername
        if foldername:
            path = join(path, foldername)
        if not exists(path):
            makedirs(path)
        return path
