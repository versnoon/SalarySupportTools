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
from salary_support_tools import tex_engine
from salary_support_tools import salary_period_engine
from salary_support_tools import salary_depart_engine
from salary_support_tools import salary_bank_engine
from salary_support_tools import salary_gz_engine
from salary_support_tools import salary_jj_engine
from salary_support_tools import tex_operator
from salary_support_tools import salary_operator

if __name__ == "__main__":
    # persons, period, departs = ehr_engine.EhrEngine().initven()
    # if len(persons) > 0:
    #     ehr_engine.EhrEngine().start(persons, period, departs)

    # engine = ehr_engine_two.EhrEngineTwo()
    # period, depart = engine.initven()
    # personss, banks = engine.loadBaseDatas(period, depart)
    # persons = personss["c"]
    # if len(persons) > 0:
    #     engine.clear_file(period, depart)
    #     gz_datas, jj_datas = engine.loadAuditedDatas(period, depart)
    #     gzm, jjm = engine.split_salary_data_by_depart(
    #         depart, gz_datas, jj_datas)
    #     err_msgs = engine.validate(period, persons, banks, depart, gzm, jjm)
    #     # 将审核结果写入相应得文件目录
    #     errs_mgs = dict()
    #     errs_mgs = engine.err_info_write_to_depart_folder(period, err_msgs)
    #     engine.copy_to_depart_folder(period, gzm, jjm, errs_mgs)
    #     # engine.write_audited_info(period, gzm, jjm, errs_mgs)
    #     engine_audit = ehr_engine.EhrEngine()
    #     engine_audit.start(persons, period, depart, banks)

    # 载入区间信息
    # 解析审核日期
    period_engine = salary_period_engine.SalaryPeriodEngine()
    period, _ = period_engine.start()
    # 解析单位信息模板

    depart_engine = salary_depart_engine.SalaryDepartEngine(period)
    departs = depart_engine.start()

    # 载入人员信息

    p_engine = person_engine.PersonEngine(period)
    persons = p_engine.load_data()
    # 解析银行卡信息数据

    banks_engine = salary_bank_engine.SalaryBankEngine(period, departs)
    banks = banks_engine.load_data()

    # 载入工资信息
    gz_engine = salary_gz_engine.SalaryGzEngine(period)
    gz_datas = gz_engine.batch_load_data(departs)

    # 载入奖金信息
    jj_engine = salary_jj_engine.SalaryJjEngine(period)
    jj_datas = jj_engine.batch_load_data(departs)

    # 完成 信息 汇总 及 错误检查 输出审核结果
    merge_engine = person_salary_engine.PersonSalaryEngine(
        period, persons, gz_datas, jj_datas, banks)
    err_msgs, datas, sap_datas = merge_engine.start()

    # 验证当期所得税并输出审核结果
    tex_engine = tex_engine.TexEngine(period, datas, departs)
    tex_err_msgs, tex_datas = tex_engine.start()

    # 输出

    # 工资奖金文件输出
    salary_op = salary_operator.SalaryOperator(
        period, departs, gz_datas, jj_datas, datas, sap_datas, err_msgs)
    salary_op.export()
    # 税务相关文件输出
    tex_op = tex_operator.TexExport(period, sap_datas, tex_datas, tex_err_msgs)
    tex_op.export()
    # 数据汇总

    # 固定格式报表生成
