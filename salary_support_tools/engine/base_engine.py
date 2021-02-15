#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   base_engine.py
@Time    :   2021/02/13 09:08:53
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


class BaseEngine:
    """
    导入模板基类，定义引擎名称及根目录
    """

    def __init__(self, engine_name=""):
        self.__engine_name: str = engine_name  # 模型名称

    @property
    def engine_name(self):
        """
        返回engine名称
        """
        name = self.__engine_name
        if name is None or len(name.strip()) == 0:
            raise ValueError("对象名称为空")
        return name.strip()
