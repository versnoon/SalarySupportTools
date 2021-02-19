#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   salary_tex.py
@Time    :   2021/02/18 15:48:50
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from salary_support_tools.engine.base_period_engine import BasePeriodEngine
from salary_support_tools.model.base_model_cov import BaseModelConventor


class SalaryTex(BasePeriodEngine):
    """
    税务系统相关信息
    """
    NAME = "salary_tex"

    def __init__(self):
        super().__init__(None)
        self._code = ""  # 工号
        self._name = ""  # 姓名
        self._idtype = "居民身份证"  # 证件类型
        self._idno = ""  # 证件号码
        self._skssqq = ""  # 税款所属期起
        self._skssqz = ""  # 税款所属期止
        self._itemname = "正常工资薪金"  # 所得项目
        self._totalpayable = 0  # 应发合计
        self._bqfy = 0  # 本期费用
        self._bqmssr = 0  # 本期免税收入
        self._tex = 0  # 累计应补(退)税额
        self._gjj_gr = 0  # 公积金个人
        self._yl_gr = 0  # 养老保险个人
        self._sy_gr = 0  # 失业保险个人
        self._yil_gr = 0  # 医疗保险个人
        self._nj_gr = 0  # 年金个人
        self._sujkbx = 0  # 本期商业健康保险费
        self._syyl = 0  # 本期税延养老保险费
        self._qtkc = 0  # 本期其他扣除(其他)
        self._ljsr = 0  # 累计收入额
        self._ljms = 0  # 累计免税收入
        self._ljjc = 0  # 累计减除费用
        self._ljzx = 0  # 累计专项扣除
        self._ljznjy = 0  # 累计子女教育支出扣除
        self._ljjxjy = 0  # 累计继续教育支出扣除
        self._ljzfdk = 0  # 累计住房贷款利息支出扣除
        self._ljzfzz = 0  # 累计住房租金支出扣除
        self._ljsylr = 0  # 累计赡养老人支出扣除
        self._ljqtkc = 0  # 累计其他扣除
        self._ljzykc = 0  # 累计准予扣除的捐赠
        self._ljynse = 0  # 累计应纳税所得额
        self._sl = 0  # 税率
        self._sskc = 0  # 速算扣除数
        self._ljynse1 = 0  # 累计应纳税额
        self._ljjm = 0  # 累计减免税额
        self._ljykj = 0  # 累计应扣缴税额
        self._ljynse2 = 0  # 累计已预缴税额

        self._ehr_person = None  # ehr系统人员信息
        self._ehr_gz = None  # ehr系统工资信息
        self._ehr_jj = None  # ehr 系统奖金信息

    def __str__(self):
        return '员工税务系统信息: 身份证号 {} - 姓名 {} - 应发 {} - 累计应扣缴税额 {} - 累计已预缴税额 {} - 累计应补(退)税额 {}'.format(self._idno, self._name, self._totalpayable, self._ljykj, self._ljynse2, self._tex)

    @classmethod
    def cols(self):
        cols = dict()
        cols["_code"] = "工号"
        cols["_name"] = "姓名"
        cols["_idtype"] = "证件类型"
        cols["_idno"] = "证件号码"
        cols["_skssqq"] = "税款所属期起"
        cols["_skssqz"] = "税款所属期止"
        cols["_itemname"] = "所得项目"

        cols["_totalpayable"] = "本期收入"
        cols["_bqfy"] = "本期费用"

        cols["_bqmssr"] = "本期免税收入"
        cols["_yl_gr"] = "本期基本养老保险费"
        cols["_yil_gr"] = "本期基本医疗保险费"
        cols["_sy_gr"] = "本期失业保险费"
        cols["_gjj_gr"] = "本期住房公积金"
        cols["_nj_gr"] = "本期企业(职业)年金"

        cols["_sujkbx"] = "本期商业健康保险费"
        cols["_syyl"] = "本期税延养老保险费"
        cols["_qtkc"] = "本期其他扣除"
        cols["_ljsr"] = "累计收入额"
        cols["_ljms"] = "累计免税收入"

        cols["_ljjc"] = "本累计减除费用"
        cols["_ljzx"] = "累计专项扣除"
        cols["_ljznjy"] = "累计子女教育支出扣除"
        cols["_ljjxjy"] = "累计继续教育支出扣除"
        cols["_ljzfdk"] = "累计住房贷款利息支出扣除"
        cols["_ljzfzz"] = "累计住房租金支出扣除"
        cols["_ljsylr"] = "累计赡养老人支出扣除"

        cols["_ljqtkc"] = "累计其他扣除"
        cols["_ljzykc"] = "累计准予扣除的捐赠"
        cols["_ljynse"] = "累计应纳税所得额"
        cols["_sl"] = "税率"
        cols["_sskc"] = "速算扣除数"
        cols["_ljynse1"] = "累计应纳税额"
        cols["_ljjm"] = "累计减免税额"
        cols["_ljykj"] = "累计应扣缴税额"
        cols["_ljynse2"] = "累计已预缴税额"
        cols["_tex"] = "累计应补(退)税额"
        return cols
