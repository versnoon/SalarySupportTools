#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   base_model_cov.py
@Time    :   2021/02/18 08:44:35
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


class BaseModelConventor:

    def cov(self, datas, period, departs):
        """
        默认直接返回查询数据
        """
        return datas

    def _get_depart_byfullname(self, depart_fullname, departinfos):
        departs = depart_fullname.split("\\")
        if len(departs) < 2:
            raise ValueError("{},机构信息异常".format(depart_fullname))
        depart_name = departs[1]
        for ds, depart in departinfos.items():
            if depart.is_depart(depart_name):
                depart_name = depart.get_depart_salaryScope_and_name()
                break

        return departs[0], depart_name
