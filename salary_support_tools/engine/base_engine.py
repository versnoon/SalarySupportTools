#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   base_engine.py
@Time    :   2021/02/13 09:08:53
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


class BaseEngine(object):
    """
    导入模板基类，定义引擎名称及根目录
    """

    def __init__(self, name=""):
        self.__name: str = name  # 模型名称
        self.__base_folder_path: str = r'd:\薪酬审核文件夹'

    @property
    def name(self):
        """
        返回engine名称
        """
        name = self.__name
        if name is None or len(name.strip()) == 0:
            raise ValueError("对象名称为空")
        return name.strip()

    @property
    def base_folder_path(self):
        return self.__base_folder_path
