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
            model_info.export()
