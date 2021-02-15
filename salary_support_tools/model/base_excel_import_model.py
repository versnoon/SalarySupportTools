#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   base_bunisness_model.py
@Time    :   2021/02/13 16:05:09
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


class BaseExcelImportModel:
    """
    导入业务模型基类
    """

    def __init__(self, modelkey, clazz, cols, filepath_prefix, filename, filename_prefix, sheetindex=0, titlerow=0, func=None):
        self.__modelkey = modelkey  # 数据标示
        self.__clazz = clazz  # 模型
        self.__cols = cols  # excel列与模型属性之间得对应数组
        self.__filename = filename  # 单个文件导入，文件的文件名称
        self.__filename_prefix = filename_prefix  # 多文件导入 文件名称前缀
        self.__filepath_prefix = filepath_prefix  # 模板存放路径前缀
        self.__skip_load_with_no_file = True  # 当不存在导入文件是否跳过运行
        self.__sheetindex = sheetindex  # 工作部索引
        self.__titlerow_index = titlerow  # 标题行索引
        self.__func = func  # 回调函数

    @property
    def skip_load_with_no_file(self):
        return self.__skip_load_with_no_file

    @skip_load_with_no_file.setter
    def skip_load_with_no_file(self, skipable):
        self.__skip_load_with_no_file = skipable

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
    def filepath_prefix(self):
        return self.__filepath_prefix

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
    def func(self):
        return self.__func
