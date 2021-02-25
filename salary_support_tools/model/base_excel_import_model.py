#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   base_bunisness_model.py
@Time    :   2021/02/13 16:05:09
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from os.path import join

from salary_support_tools.engine.base_engine import BaseEngine
from salary_support_tools.model.base_model_cov import BaseModelConventor


class BaseExcelImportModel:
    """
    导入业务模型基类
    """

    def __init__(self, modelkey, clazz: BaseEngine, cols, filename, filename_prefix, sheetindex=0, titlerow=0, convertor: BaseModelConventor = None, period=None, departs=None, filefoldername=""):
        self.__modelkey = modelkey  # 数据标示
        self.__clazz = clazz  # 模型
        self.__cols = cols  # excel列与模型属性之间得对应数组
        self.__filename = filename  # 单个文件导入，文件的文件名称
        self.__filename_prefix = filename_prefix  # 多文件导入 文件名称前缀
        self.__skip_load_with_no_file = True  # 当不存在导入文件是否跳过运行
        self.__sheetindex = sheetindex  # 工作部索引
        self.__titlerow_index = titlerow  # 标题行索引
        self.__convertor = convertor  # 回调函数
        self.__period = period  # 期间
        self.__departs = departs  # 审核单位
        self.__filefoldername = filefoldername  # 模板文件存放目录

    @property
    def skip_load_with_no_file(self):
        return self.__skip_load_with_no_file

    @skip_load_with_no_file.setter
    def skip_load_with_no_file(self, skipable):
        self.__skip_load_with_no_file = skipable

    @property
    def period(self):
        return self.__period

    @period.setter
    def period(self, period):
        self.__period = period

    @property
    def departs(self):
        return self.__departs

    @departs.setter
    def departs(self, departs):
        self.__departs = departs

    @property
    def modelkey(self):
        return self.__modelkey

    @property
    def clazz(self):
        return self.__clazz

    @property
    def cols(self):
        return self.__cols

    @property
    def filename(self):
        return self.__filename

    @property
    def filename_prefix(self):
        return self.__filename_prefix

    @property
    def sheet_index(self):
        return self.__sheetindex

    @property
    def title_row(self):
        return self.__titlerow_index

    @property
    def conventor(self):
        if not self.__convertor:
            return BaseModelConventor()
        return self.__convertor

    @property
    def filefoldername(self):
        return self.__filefoldername

    def base_tpl_folder_path(self):
        return r'd:\薪酬审核文件夹\test'

    def tpl_path_prefix(self):
        path = self.base_tpl_folder_path()
        if self.period:
            path = join(path, self.period.period)
        if self.filefoldername:
            path = join(path, self.filefoldername)
        return path
