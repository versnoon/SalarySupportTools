#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tex_compare_engine.py
@Time    :   2021/03/01 22:31:51
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''
from salary_support_tools.model.salary_period import SalaryPeriod
from salary_support_tools.model.salary_tex import SalaryTex
from salary_support_tools.model.sap_salary_info import SapSalaryInfo
from salary_support_tools.model.err_message import ErrMessage
from salary_support_tools.model.export.base_excel_export_model import BaseExcelExportModel
from salary_support_tools.model.export.err_message_export_model import ErrMessageExport
from salary_support_tools.engine.load_tpls_engine import LoadTplEngine


class TexCompareEngine:
    """
    所得税对比
    """

    def compare(self):
        load_engine = LoadTplEngine()
        current_period, _ = load_engine.load_current_period_departs()
        infos = load_engine.load_tpl_by_year(
            current_period.year)
        # current = load_engine.load_tpl_by_period(current_period)
        # 2月份数据
        # two_period, two_departs, two_persons, two_jobs, two_gzs, two_jjs, two_banks, two_texes, two_merge_infos = load_engine.load_tpl_by_period(
        # SalaryPeriod(2021, 2))

        # 1月份数据
        # one_period, one_departs, one_persons, one_jobs, one_gzs, one_jjs, one_banks, one_texes, one_merge_infos = load_engine.load_tpl_by_period(
        # SalaryPeriod(2021, 1))

        # errs = self.compare(two[7], one[8], two[8])
        errs = self.compare_all(
            infos[current_period.month - 1][7], current_period.month, infos)

        BaseExcelExportModel(current_period, ErrMessageExport(current_period, None).cols(),
                             None, filename="所得税效验").export_datas_by_depart(errs)

    def compare_all(self, current_texes, current_month, merge_infos):
        res_tex_depart = dict()
        res_depart = dict()
        for tex_depart, datas_by_tex_depart in current_texes.items():
            for depart, datas_by_depart in datas_by_tex_depart.items():
                vs_tex_depart = dict()
                vs_depart = dict()
                if tex_depart in res_tex_depart:
                    vs_tex_depart = res_tex_depart[tex_depart]
                if depart in res_depart:
                    vs_depart = res_depart[depart]
                for code, texes_by_code in datas_by_depart.items():
                    err = self.compareall_tex_by_code(code, tex_depart, depart,
                                                      texes_by_code, current_month, merge_infos)
                    if err:
                        vs_depart[code] = err
                        vs_tex_depart[depart] = vs_depart
                        res_depart[depart] = vs_depart
                        res_tex_depart[tex_depart] = vs_tex_depart

        return res_tex_depart

    def compareall_tex_by_code(self, code, tex_depart, depart, texex, current_month, merge_infos):
        ljsr, ljkc, ljznjy, ljjxjy, ljzfdk, ljzfzz, ljsylr, ljjc, tex_tex, tex_ynse = self.get_texes_info(
            texex)
        ygzz, name, ehr_full_departname, ehr_totalpayable, ehr_totalkc, ehr_tex, ehr_two_tex, ehr_ljznjy, ehr_ljjxjy, ehr_ljzfdk, ehr_ljzfzz, ehr_ljsylr, ehr_ynse = self.get_sap_all_tex_info_by_code(
            code, ljjc, current_month, merge_infos)
        err = self.create_err_info(tex_depart, depart, code, name, ehr_full_departname, ygzz, ehr_ynse, tex_ynse, ljsr, ehr_totalpayable, ljkc,
                                   ehr_totalkc, ehr_ljznjy, ljznjy, ehr_ljjxjy, ljjxjy, ehr_ljzfdk, ljzfdk, ehr_ljzfzz, ljzfzz, ehr_ljsylr, ljsylr, ehr_tex, tex_tex)
        return err

    def get_texes_info(self, texex):
        tex: SalaryTex = texex['s_tex']
        one_tex: SalaryTex = None
        ycxjj = 0
        ycxjj_tex = 0
        ljsr = tex._ljsr  # 累计收入
        if 's_one_tex' in texex:
            one_tex = texex['s_one_tex']
            ycxjj = one_tex._totalpayable  # 一次性奖励
            ycxjj_tex = one_tex._tex  # 一次性奖励所得税
        ljjc = tex._ljjc  # 累计减除费用

        ljkc = tex._ljzx + tex._ljqtkc  # 累计专项，+累计其它 （公积金保险年金）
        ljyk = tex._ljykj  # 累计应扣
        ljyyj = tex._ljynse2  # 累计预缴
        ljznjy = tex._ljznjy  # 累计子女教育
        ljjxjy = tex._ljjxjy  # 累计继续教育
        ljzfdk = tex._ljzfdk  # 累计住房贷款
        ljzfzz = tex._ljzfzz  # 累计住房租金
        ljsylr = tex._ljsylr  # 累计赡养老人
        tex_tex = ljyk
        if ljyk < ljyyj:
            tex_tex = ljyyj
        tex_tex += ycxjj_tex  # 加入年底兑现奖金
        tex_ynse = self.get_ynse(
            ljsr, ljkc, ljznjy, ljjxjy, ljzfdk, ljzfzz, ljsylr)
        return ljsr, ljkc, ljznjy, ljjxjy, ljzfdk, ljzfzz, ljsylr, ljjc, tex_tex, tex_ynse

    def compare_tex_by_code(self, code, tex_depart, depart, texex, one_merge_infos, two_merge_infos):

        ljsr, ljkc, ljznjy, ljjxjy, ljzfdk, ljzfzz, ljsylr, ljjc, tex_tex, tex_ynse = self.get_texes_info(
            texex)

        ygzz, name, ehr_full_departname, ehr_totalpayable, ehr_totalkc, ehr_tex, ehr_two_tex, ehr_ljznjy, ehr_ljjxjy, ehr_ljzfdk, ehr_ljzfzz, ehr_ljsylr, ehr_ynse = self.get_sap_tex_info_by_code(
            code, one_merge_infos, two_merge_infos, ljjc)

        err = self.create_err_info(tex_depart, depart, code, name, ehr_full_departname, ygzz, ehr_ynse, tex_ynse, ljsr, ehr_totalpayable, ljkc,
                                   ehr_totalkc, ehr_ljznjy, ljznjy, ehr_ljjxjy, ljjxjy, ehr_ljzfdk, ljzfdk, ehr_ljzfzz, ljzfzz, ehr_ljsylr, ljsylr, ehr_tex, tex_tex)
        # err.tex_depart = tex_depart
        # err.depart = depart
        # err._code = code
        # err._name = name
        # err._depart_fullname = ehr_full_departname
        # err._ygzz = ygzz
        # err._err_messages = []
        # if round(ehr_ynse, 2) != round(tex_ynse, 2):  # 累计收入不等
        #     err_msgs = "累计应税额不匹配，宝武ehr金额{:2f},税务系统金额{:2f},差额{:2f}".format(
        #         ehr_ynse, tex_ynse, ehr_ynse - tex_ynse)
        #     if round(ljsr, 2) != round(ehr_totalpayable, 2):
        #         err._err_messages.append(
        #             "累计收入不匹配，宝武ehr金额{:2f},税务系统金额{:2f},差额{:2f}".format(ehr_totalpayable, ljsr, ehr_totalpayable - ljsr))
        #     if round(ljkc, 2) != round(ehr_totalkc, 2):
        #         err._err_messages.append(
        #             "累计扣缴不匹配，宝武ehr金额{:2f},税务系统金额{:2f},差额{:2f}".format(ehr_totalkc, ljkc, ehr_totalkc - ljkc))
        #     if round(ehr_ljznjy, 2) != round(ljznjy, 2) or round(ehr_ljjxjy, 2) != round(ljjxjy, 2) or round(ehr_ljzfdk, 2) != round(ljzfdk, 2) or round(ehr_ljzfzz, 2) != round(ljzfzz, 2) or round(ehr_ljsylr, 2) != round(ljsylr, 2):
        #         err._err_messages.append(
        #             "专项附件扣除项目不匹配，累计子女教育:宝武ehr金额{:2f}-税务系统金额{:2f},累计继续教育:宝武ehr金额{:2f}-税务系统金额{:2f},累计住房贷款:宝武ehr金额{:2f}-税务系统金额{:2f},累计住房租金:宝武ehr金额{:2f}-税务系统金额{:2f},累计赡养老人宝武ehr金额{:2f}-税务系统金额{:2f}".format(ehr_ljznjy, ljznjy, ehr_ljjxjy, ljjxjy, ehr_ljzfdk, ljzfdk, ehr_ljzfzz, ljzfzz, ehr_ljsylr, ljsylr))
        # if round(ehr_tex, 2) != round(tex_tex, 2):
        #     err._err_messages.append(
        #         "个税不匹配，宝武ehr系统金额{:2f},税务系统金额{:2f},差额{:2f}".format(ehr_tex, tex_tex, ehr_tex - tex_tex))
        # if len(err._err_messages) > 0:
        #     return err
        return err

    def create_err_info(self, tex_depart, depart, code, name, ehr_full_departname, ygzz, ehr_ynse, tex_ynse, ljsr, ehr_totalpayable, ljkc, ehr_totalkc, ehr_ljznjy, ljznjy, ehr_ljjxjy, ljjxjy, ehr_ljzfdk, ljzfdk, ehr_ljzfzz, ljzfzz, ehr_ljsylr, ljsylr, ehr_tex, tex_tex):
        err = ErrMessage()
        err.tex_depart = tex_depart
        err.depart = depart
        err._code = code
        err._name = name
        err._depart_fullname = ehr_full_departname
        err._ygzz = ygzz
        err._err_messages = []
        if round(ehr_ynse, 2) != round(tex_ynse, 2):  # 累计收入不等
            if round(ljsr, 2) != round(ehr_totalpayable, 2):
                err._err_messages.append(
                    "累计收入不匹配，宝武ehr金额{:.2f},税务系统金额{:.2f},差额{:.2f}".format(ehr_totalpayable, ljsr, ehr_totalpayable - ljsr))
            if round(ljkc, 2) != round(ehr_totalkc, 2):
                err._err_messages.append(
                    "累计扣缴不匹配，宝武ehr金额{:.2f},税务系统金额{:.2f},差额{:.2f}".format(ehr_totalkc, ljkc, ehr_totalkc - ljkc))
            if round(ehr_ljznjy, 2) != round(ljznjy, 2) or round(ehr_ljjxjy, 2) != round(ljjxjy, 2) or round(ehr_ljzfdk, 2) != round(ljzfdk, 2) or round(ehr_ljzfzz, 2) != round(ljzfzz, 2) or round(ehr_ljsylr, 2) != round(ljsylr, 2):
                err._err_messages.append(
                    "专项附件扣除项目不匹配，累计子女教育:宝武ehr金额{:.2f}-税务系统金额{:.2f},累计继续教育:宝武ehr金额{:.2f}-税务系统金额{:.2f},累计住房贷款:宝武ehr金额{:.2f}-税务系统金额{:.2f},累计住房租金:宝武ehr金额{:.2f}-税务系统金额{:.2f},累计赡养老人宝武ehr金额{:.2f}-税务系统金额{:.2f}".format(ehr_ljznjy, ljznjy, ehr_ljjxjy, ljjxjy, ehr_ljzfdk, ljzfdk, ehr_ljzfzz, ljzfzz, ehr_ljsylr, ljsylr))
        if round(ehr_tex, 2) != round(tex_tex, 2):
            err._err_messages.append(
                "个税不匹配，宝武ehr系统金额{:.2f},税务系统金额{:.2f},差额{:.2f}".format(ehr_tex, tex_tex, ehr_tex - tex_tex))
        if len(err._err_messages) > 0:
            return err
        return None

    def get_ynse(self, totalpayable, total_kk, ljznjy, ljjxjy, ljzfdk, ljzfzz, ljsylr):
        return totalpayable - total_kk - ljznjy - ljjxjy - ljzfdk - ljzfzz - ljsylr

    def get_sap_all_tex_info_by_code(self, code, ljjc, current_month, merge_infos):
        """
        根据税务系统的累计减除费用查询
        """
        name = ""
        ygzz = ""  # 员工子组
        totalpayable = 0
        tex = 0
        two_tex = 0
        totalkc = 0
        ljznjy = 0
        ljjxjy = 0
        ljzfdk = 0
        ljzfzz = 0
        ljsylr = 0

        current_sap_info, current_full_departname = self.get_merge_info_by_month(
            current_month, code, merge_infos)
        if current_sap_info:
            totalpayable = current_sap_info.get_totalable()
            name = current_sap_info._name
            ygzz = current_sap_info._ygzz
            full_departname = current_sap_info.depart
            tex = current_sap_info._totalsdj
            current_tex = tex
            totalkc = current_sap_info.get_total_kc()
            ljznjy = current_sap_info._znjy
            ljjxjy = current_sap_info._jxjy
            ljzfdk = current_sap_info._zfdk
            ljzfzz = current_sap_info._zffz
            ljsylr = current_sap_info._sylr
        step = round(ljjc / 5000, 0)

        pre_sap_info = None
        for i in range(int(step)):
            if current_month - i - 1 > 0:
                pre_sap_info, _ = self.get_merge_info_by_month(
                    current_month - i - 1, code, merge_infos)
                if pre_sap_info:
                    totalpayable += pre_sap_info.get_totalable()
                    tex += pre_sap_info._totalsdj
                    totalkc += pre_sap_info.get_total_kc()

        ehr_ynse = self.get_ynse(totalpayable, totalkc,
                                 ljznjy, ljjxjy, ljzfdk, ljzfzz, ljsylr)

        return ygzz, name, current_full_departname, totalpayable, totalkc, tex, two_tex, ljznjy, ljjxjy, ljzfdk, ljzfzz, ljsylr, ehr_ynse

    def get_merge_info_by_month(self, month, code, merge_infos):
        if merge_infos:
            merge_info = None
            if month <= len(merge_infos):
                merge_info = merge_infos[month - 1][8]
            if merge_info:
                return self.get_person_sap_info_by_code(
                    merge_info, code)
        return None, ""

    def get_sap_tex_info_by_code(self, code, one_merge_infos, two_merge_infos, ljjc):
        one_sap_info, one_full_departname = self.get_person_sap_info_by_code(
            one_merge_infos, code)
        two_sap_info, full_departname = self.get_person_sap_info_by_code(
            two_merge_infos, code)

        name = ""
        ygzz = ""  # 员工子组
        totalpayable = 0
        tex = 0
        two_tex = 0
        totalkc = 0
        ljznjy = 0
        ljjxjy = 0
        ljzfdk = 0
        ljzfzz = 0
        ljsylr = 0
        if two_sap_info != None:
            totalpayable = two_sap_info.get_totalable()
            name = two_sap_info._name
            ygzz = two_sap_info._ygzz
            full_departname = two_sap_info.depart
            tex = two_sap_info._totalsdj
            # + two_sap_info._tex_special
            two_tex = tex
            totalkc = two_sap_info.get_total_kc()
            ljznjy = two_sap_info._znjy
            ljjxjy = two_sap_info._jxjy
            ljzfdk = two_sap_info._zfdk
            ljzfzz = two_sap_info._zffz
            ljsylr = two_sap_info._sylr

        if ljjc > 5000:
            if one_sap_info != None:
                totalpayable += one_sap_info.get_totalable()
                tex += one_sap_info._totalsdj
                totalkc += one_sap_info.get_total_kc()
        ehr_ynse = self.get_ynse(totalpayable, totalkc,
                                 ljznjy, ljjxjy, ljzfdk, ljzfzz, ljsylr)
        return ygzz, name, full_departname, totalpayable, totalkc, tex, two_tex, ljznjy, ljjxjy, ljzfdk, ljzfzz, ljsylr, ehr_ynse

    def get_person_sap_info_by_code(self, merge_infos, code):
        for tex_depart, datas_by_tex_depart in merge_infos.items():
            for depart, datas_by_depart in datas_by_tex_depart.items():
                if code in datas_by_depart:
                    # 合并后sap信息
                    return datas_by_depart[code][1], datas_by_depart[code][0]._depart_fullname
        return None, ""
