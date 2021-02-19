#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   excel_tpl_2_model_util.py
@Time    :   2021/02/13 16:19:35
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from os.path import join, exists
from os import listdir

import xlrd

from salary_support_tools.model.base_excel_import_model import BaseExcelImportModel


class XlsToModelUtil:
    """
    excel xls 格式 导入工具
    单个单个导入批量文件导入2选一
    如果BaseExcelImportModel定义了单个导入文件名即为单文件导入
    如果BaseExcelImportModel中单个导入文件名为空，导入文件前缀不为空即为批量导入
    """

    EXT = '.xls'

    def __init__(self, modelinfos: tuple):
        self.__model_infos = modelinfos  # BaseExcelImportModel 类型切片

    def load_tpls(self) -> dict:
        """
        加载模板信息
        """
        res = dict()
        for modelinfo in self.__model_infos:
            res[modelinfo.modelkey] = self.load_tpl(modelinfo)
        return res

    def load_tpl(self, modelinfo: BaseExcelImportModel):
        """
        加载数据
        """
        filepath_prefix = modelinfo.test_tpl_path()  # 测试环境
        # filepath_prefix = modelinfo.tpl_path_prefix()  # 正式环境
        filename = modelinfo.filename
        filename_prefix = modelinfo.filename_prefix
        clazz = modelinfo.clazz
        cols = modelinfo.cols
        sheet_index = modelinfo.sheet_index
        title_row = modelinfo.title_row
        skipable = modelinfo.skip_load_with_no_file  # 导入文件不存在时是否跳过
        conventor = modelinfo.conventor
        period = modelinfo.period
        departs = modelinfo.departs
        filepaths = self.get_tpl_file_paths(
            filepath_prefix, filename, filename_prefix)
        res = []
        for filepath, exist in filepaths.items():
            if not exist:
                if not skipable:
                    raise (FileNotFoundError(
                        "文件不存在{}，不能执行导入操作".format(filepath)))
                else:
                    continue
            res.extend(self.read_tpl(clazz, filepath,
                                     sheet_index, title_row, cols))
        return conventor.cov(res, period, departs)

    def get_tpl_file_paths(self, filepath_prefix: str, filename: str, filename_prefix: str) -> dict:
        paths = dict()
        if filename:
            filename_path, file_exist = self.get_tpl_exist_info(
                self.get_tplfile_path(filepath_prefix, filename, self.EXT))
            paths[filename_path] = file_exist
        else:
            file_list = listdir(filepath_prefix)
            for file_name in file_list:
                file_path = self.get_tplfile_path(filepath_prefix, file_name)
                file_ext = file_name.rsplit('.', maxsplit=1)
                if len(file_ext) != 2:
                    # 没有后缀名
                    continue
                if file_ext[1].lower() != self.EXT[1:]:
                    # 不是excel2003文件
                    continue
                # 判断已特定名称开头的文件
                if file_name.startswith(filename_prefix):
                    paths[file_path] = True
        return paths

    def get_tplfile_path(self, filepath_prefix: str, filename: str, fileext: str = None) -> str:
        """
        获取前缀路径下特定的模板文件路径
        """
        if fileext:
            return join(filepath_prefix, r'{}{}'.format(filename.split()[0], fileext))
        return join(filepath_prefix, r'{}'.format(filename.split()[0]))

    def get_tpl_exist_info(self, path):
        file_exist = exists(path)
        return path, file_exist

    def read_tpl(self, clazz, filepath, sheetindex, titlerow, cols) -> []:
        # 读取模板文件
        book = xlrd.open_workbook(filepath)
        # 读取第一个sheet 工作簿
        sheet = book.sheet_by_index(sheetindex)
        # 获取列头
        titles = sheet.row_slice(titlerow)
        # 反射生成
        res = []
        for r in range(sheet.nrows):
            if r > titlerow:
                row = sheet.row_slice(r)
                ins = clazz()
                for i in range(len(titles)):
                    propertyName = self.get_model_property_name(
                        titles[i].value, cols)
                    if "" != propertyName:
                        if row[i] != None:
                            if row[i].value != None and row[i].value != '':
                                setattr(ins, propertyName, row[i].value)
                res.append(ins)
        return res

    def get_model_property_name(self, titlename, cols):
        for pn, tn in cols.items():
            if tn == titlename:
                return pn
        return ""
