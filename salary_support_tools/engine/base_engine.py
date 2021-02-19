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

    NAME = "base"

    @classmethod
    def name_key(cls):
        """
        返回engine名称
        """
        return cls.NAME
