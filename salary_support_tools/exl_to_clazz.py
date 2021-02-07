#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   exl_to_clazz.py
@Time    :   2021/01/28 15:33:41
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from os.path import isfile, join, exists
from os import listdir

import xlrd


class ExlToClazz(object):
    """
    模板
    """

    def __init__(self, clazz, columnsDef, filePath, titleindex=0, noneable=False):
        self.clazz = clazz
        self.columnsDef = columnsDef
        self.filePath = filePath
        self.titleindex = titleindex
        self.noneable = noneable

    def loadTemp(self) -> []:
        if not isfile(self.filePath):
            # 跳过异常
            if self.noneable:
                return
            raise FileNotFoundError("文件路径 {0} 不存在".format(self.filePath))
        # 读取模板文件
        book = xlrd.open_workbook(self.filePath)
        # 读取第一个sheet 工作簿
        sheet = book.sheet_by_index(0)
        # 获取列头
        titles = sheet.row_slice(self.titleindex)
        # 反射生成
        res = []
        for r in range(sheet.nrows):
            if r > self.titleindex:
                row = sheet.row_slice(r)
                ins = self.clazz()
                for i in range(len(titles)):
                    propertyName = self.getPropertyName(titles[i].value)
                    if "" != propertyName:
                        if row[i] != None:
                            if row[i].value != None and row[i].value != '':
                                setattr(ins, propertyName, row[i].value)
                res.append(ins)

        return res

    def getPropertyName(self, columnName) -> str:
        """
        docstring
        """
        columns = self.columnsDef
        for key in columns.keys():
            if columns[key] == columnName:
                return key
        return ""


class ExlsToClazz(object):
    """
    多个excel转class
    """

    def __init__(self, clazz, columnsDef, filepath_prefix, filename_prefix, titleindex=0, noneable=False):
        self.clazz = clazz
        self.columnsDef = columnsDef
        self.filepath_prefix = filepath_prefix
        self.filename_prefix = filename_prefix
        self.titleindex = titleindex
        self.noneable = noneable

    def loadTemp(self) -> []:
        if not exists(self.filepath_prefix):
            return []
        file_list = listdir(self.filepath_prefix)
        # for base_path, folder_list, file_list in walk(self.filepath_prefix):
        datas = []
        for file_name in file_list:
            file_path = join(self.filepath_prefix, file_name)
            file_ext = file_name.rsplit('.', maxsplit=1)
            if len(file_ext) != 2:
                # 没有后缀名
                continue
            if file_ext[1].lower() != 'xls':
                # 不是excel2003文件
                continue
            name = file_ext[0]
            # 判断已特定名称开头的文件
            if name.startswith(self.filename_prefix):
                clazz = ExlToClazz(
                    self.clazz, self.columnsDef, file_path, 0, True)
                t = clazz.loadTemp()
                if len(t) > 0:
                    datas.extend(t)
        return datas
