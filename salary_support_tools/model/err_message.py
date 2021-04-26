#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   err_message.py
@Time    :   2021/02/23 08:28:44
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


from salary_support_tools.engine.base_period_engine import BasePeriodEngine
from salary_support_tools.model.person_salary import PersonSalaryInfo
from salary_support_tools.model.sap_salary_info import SapSalaryInfo
from salary_support_tools.model.salary_tex import SalaryTex


class ErrMessage(BasePeriodEngine):

    def __init__(self):
        super().__init__(None)
        self.depart = ""  # 单位文件夹名称
        self.tex_depart = ""  # 税务机构
        self._code = ""  # 员工通行证
        self._name = ""  # 员工姓名
        self._ygzz = ""  # 在职状态
        self._depart_fullname = ""  # 机构
        self._err_messages = []  # 错误信息
        self._descript = ""  # 备注

    def validate(self, person_salary_info: PersonSalaryInfo, sap_info: SapSalaryInfo):
        """
        验证员工相关数据
        """
        self.period = person_salary_info.period
        self.tex_depart = person_salary_info._tex_depart
        self.depart = person_salary_info._depart
        self._depart_fullname = person_salary_info._depart_fullname
        self._code = person_salary_info._code
        self._name = sap_info._name
        self._ygzz = sap_info._ygzz
        gz = person_salary_info._gz
        jj = person_salary_info._jj
        banks = person_salary_info._banks
        texes = person_salary_info._texes
        self._err_messages = []
        if gz is not None:
            # 实发小于0
            if gz._pay is not None and gz._pay < 0:
                self._err_messages.append(self.err_mss(
                    "工资信息错误", "工资实发小于0，实发金额{}".format(gz._pay)))
            # 缺少工资银行卡号
            if gz._pay > 0:
                if banks is None or "gz" not in banks:
                    self._err_messages.append(self.err_mss(
                        "银行卡信息错误", "缺少工资卡信息"))
            # 缺少岗位工资
            if gz._salaryModel.startswith("岗位绩效工资制") and gz._gwgz == 0:
                self._err_messages.append(self.err_mss(
                    "工资信息错误", "岗位工资异常：缺少岗位工资信息"))
        if jj is not None:
            # 实发小于0
            if jj._pay is not None and jj._pay < 0:
                self._err_messages.append(self.err_mss(
                    "奖金信息错误", "奖金实发小于0，实发金额{}".format(jj._pay)))
            # 缺少工资银行卡号
            if jj._pay > 0:
                if banks is None or "jj" not in banks:
                    self._err_messages.append(self.err_mss(
                        "银行卡信息错误", "缺少奖金卡信息"))
        if texes is not None:
            s_tex: SalaryTex = None
            if "s_tex" in texes:
                s_tex = texes["s_tex"]
            s_one_tex: SalaryTex = None
            if "s_one_tex" in texes:
                s_one_tex = texes["s_one_tex"]
            if s_tex:
                # 当期收入
                _tex_total_payable = round(s_tex._totalpayable, 2)
                # 特殊优惠税率奖励
                _one_tex_total_payable = 0
                # ehr 当期收入（不含年底兑现）
                _total_payable = round(sap_info.get_totalable(), 2)
                # ehr 年底兑现
                _one_total_payable = sap_info._nddxj
                # 当期综合税
                _tex_total_tex = round(s_tex._tex, 2)
                # 当期优惠税率
                _one_tex_total_tex = 0

                # ehr
                _total_tex = round(sap_info._totalsdj, 2)
                if s_one_tex:
                    _one_tex_total_payable = round(s_one_tex._totalpayable, 2)
                    _one_tex_total_tex = round(s_one_tex._tex, 2)

                if _tex_total_payable + _one_tex_total_payable != _total_payable + _one_total_payable:
                    self._err_messages.append(self.err_mss(
                        "本期收入异常", "税务系统当期综合计税收入金额{:.2f} + 一次性奖金收入金额{:.2f} 不等于 宝武EHR当期综合计税收入金额{:.2f} + 一次性奖金收入金额{:.2f}".format(_tex_total_payable, _one_tex_total_payable, _total_payable, _one_total_payable)))
                if round(_tex_total_tex + _one_tex_total_tex - _total_tex, 0) != 0:  # 当期所得税不匹配
                    self._err_messages.append(self.err_mss(
                        "所得税异常", "税务系统当期综合计税个税金额{:.2f} + 一次性奖金个税金额{:.2f} 不等于 宝武EHR个调税金额{:.2f}".format(_tex_total_tex, _one_tex_total_tex, _total_tex)))
                    # 个税调整差额
                    self._descript = round(
                        _total_tex - (_tex_total_tex + _one_tex_total_tex), 2)

    def err_mss(self, err_type, message) -> str:
        return '错误类型 {} - 错误信息 {}'.format(err_type, message)
