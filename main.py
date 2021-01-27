#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2021/01/20 11:18:31
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from salary_support_tools import ehr_engine
from salary_support_tools import ehr_engine_two

if __name__ == "__main__":
    # persons, period, departs = ehr_engine.EhrEngine().initven()
    # if len(persons) > 0:
    #     ehr_engine.EhrEngine().start(persons, period, departs)
    engine = ehr_engine_two.EhrEngineTwo()
    period, depart = engine.initven()
    persons, banks = engine.loadBaseDatas(period)
    if len(persons) > 0:
        gz_datas, jj_datas = engine.loadAuditedDatas(period, depart)
        gzm, jjm = engine.split_salary_data_by_depart(
            depart, gz_datas, jj_datas)
        # gzvm, jjvm = engine.validator(period, gzm, jjm)
        engine.copy_to_depart_folder(period, gzm, jjm)
        engine_audit = ehr_engine.EhrEngine()
        engine_audit.start(persons, period, depart, banks)
