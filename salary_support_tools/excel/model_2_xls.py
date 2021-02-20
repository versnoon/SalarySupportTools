#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   model_2_xls.py
@Time    :   2021/02/20 15:14:38
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''
from os.path import exists, join
from os import makedirs

import xlwt

from salary_support_tools.model.export.base_excel_export_model import BaseExcelExportModel


class ModelToXls:
    """
    将模型输出到Xls
    """

    EXT = '.xls'

    def __init__(self, modelinfos: tuple):
        self.__model_infos = modelinfos

    def export(self):
        for model_info in self.__model_infos:
            self.do_export(model_info)

    def do_export(self, model_info: BaseExcelExportModel):
        model_datas = model_info._datas
        convertor = model_info._convertor
        datas = convertor.cov(model_datas)
        filepath = model_info.get_export_path()
        cols = model_info._cols
        filename = model_info._filename
        self.create_excel_file(datas, filepath, filename, cols)

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
            for j, col in enumerate(cols):
                propertyName = col._code
                try:
                    s.write(
                        i+1, j, getattr(datas[i], propertyName, 0))
                except TypeError:
                    pass
        b.save(r'{}\{}{}'.format(filepath, filename, self.EXT))
