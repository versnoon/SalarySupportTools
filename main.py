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
from salary_support_tools import person_engine
from salary_support_tools import person_salary_engine

if __name__ == "__main__":
    # persons, period, departs = ehr_engine.EhrEngine().initven()
    # if len(persons) > 0:
    #     ehr_engine.EhrEngine().start(persons, period, departs)

    engine = ehr_engine_two.EhrEngineTwo()
    period, depart = engine.initven()
    personss, banks = engine.loadBaseDatas(period, depart)
    persons = personss["c"]
    if len(persons) > 0:
        engine.clear_file(period, depart)
        gz_datas, jj_datas = engine.loadAuditedDatas(period, depart)
        gzm, jjm = engine.split_salary_data_by_depart(
            depart, gz_datas, jj_datas)
        err_msgs = engine.validate(period, persons, banks, depart, gzm, jjm)
        # 将审核结果写入相应得文件目录
        errs_mgs = dict()
        errs_mgs = engine.err_info_write_to_depart_folder(period, err_msgs)
        engine.copy_to_depart_folder(period, gzm, jjm, errs_mgs)
        # engine.write_audited_info(period, gzm, jjm, errs_mgs)
        engine_audit = ehr_engine.EhrEngine()
        engine_audit.start(persons, period, depart, banks)

        # 载入区间信息

        # 载入单位信息

        # 载入人员信息

        # 载入工资信息

        # 载入奖金信息

        # 完成 信息 汇总 及 错误检查
        merge_engine = person_salary_engine.PersonSalaryEngine(
            period, personss, gz_datas, jj_datas, banks)
        has_err, err_msgs, datas = merge_engine.start()

        # 载入所得税信息

        # 验证当期所得税

        # 输出

        # 数据汇总

        # 固定格式报表生成
