#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   base_import_engine.py
@Time    :   2021/02/13 15:37:53
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


from salary_support_tools.engine.base_period_engine import BasePeriodEngine
from salary_support_tools.model.salary_period import SalaryPeriod
from salary_support_tools.exl_to_clazz import ExlToClazz, ExlsToClazz


class BaseImportEngine(BasePeriodEngine):
    """
    导入引擎默认加入单文件导入和多文件导入
    """

    def __init__(self, period: SalaryPeriod, filename: str, filename_prefix: str, clazz, cols):
        super().__init__("导入模块", period)
        self.__filename = filename  # 文件名
        self.__filename_prefix = filename_prefix  # 文件名前缀
        self.__clazz = clazz  # 对应模型
        self.__cols = cols  # 列定义

    def load_data(self):
        """
        载入单个文件
        """
        # load = ExlToClazz(self.__clazz, dict(), self.base_folder_path)

    def batch_load_data(self):
        """
        载入多个文件
        """
        # gz_load = ExlsToClazz(
        #     SalaryGzInfo, gz.getColumnDef(), self.get_exl_tpl_folder_path_batch(), "工资信息")
        pass
