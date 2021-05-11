#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   jg_summary_report_data.py
@Time    :   2021/05/08 15:41:05
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from collections import OrderedDict

from salary_support_tools.model.sap_salary_info import SapSalaryInfo


class ReportData:

    def __init__(self, sapinfo: SapSalaryInfo):
        self.sapinfo = sapinfo

    def is_gf(self):
        # 判断是股份本部
        return self.sapinfo.two == "马鞍山钢铁股份有限公司（总部）"

    def is_jt_jg(self):
        # 判断是集团机关
        return self.sapinfo.depart == "01_集团机关"

    def is_gf_jg(self):
        return self.sapinfo.depart == "02_股份机关"


class JgReportSalaryInfo(ReportData):

    def __init__(self, sapinfo: SapSalaryInfo):
        super().__init__(sapinfo)
        # 岗位工资
        self.gwgz = self.sapinfo._gwgz
        # 保留工资
        self.blgz = self.sapinfo._blgz
        # 年功工资
        self.nggz = self.sapinfo._nggz
        # 辅助工资
        self.fzgz = self.sapinfo._fzgz
        # 增补工资
        self.zbgz = self.sapinfo._gzbt
        # 其他津贴
        # 物价补贴 + 技师津贴 +一转多能津贴(纪检 计生 信访)+ 矿山津贴 + 下井津贴 + 护士长津贴
        # + 外语津贴 + 班组长津贴 + 科技津贴 + 能手津贴 + 物业补贴 + 保健费 + 通讯费 + 回民 + 误餐费
        # + 矿山荣誉金 + 伤残津贴 + 科研项目津贴 + 技术攻关津贴 +
        self.qtjt = self.sapinfo._wjbt + self.sapinfo._jsjt + self.sapinfo._yzdnjt + self.sapinfo._ksjt + self.sapinfo._xjjt + self.sapinfo._hszjt + self.sapinfo._wyjt + self.sapinfo._bzzjt + self.sapinfo._kjjt + self.sapinfo._nsjt + \
            self.sapinfo._wybt + self.sapinfo._bjf + self.sapinfo._txf + self.sapinfo._hm + self.sapinfo._wcf + \
            self.sapinfo._ksryj + self.sapinfo._scjt + self.sapinfo._kyxm + \
            self.sapinfo._jsgg + self.sapinfo._fgzjtbf
        # 预支年薪
        self.yznx = self.sapinfo._yznx
        # 职务补贴
        self.zwbt = self.sapinfo._zwbt
        # 夜班津贴
        self.ybjt = self.sapinfo._ybjt
        # 奖金
        # 基本奖金 + 单项奖1 + 单项奖2 + 单项奖3 + 公司效益奖 + 年底兑现奖
        # + 计税奖金 + 工程津贴 + 技术输出 + 其它 + 重点工作奖 + 荣誉类奖 + 员工精益改善奖
        self.jj = self.sapinfo._jbjj+self.sapinfo._onejj + self.sapinfo._twojj + self.sapinfo._threejj + self.sapinfo._gsxyj + self.sapinfo._nddxj + \
            self.sapinfo._jsjj + self.sapinfo._gcjt + self.sapinfo._jssc + \
            self.sapinfo._qt + self.sapinfo._zxj + self.sapinfo._ryj + self.sapinfo._jyj
        # 加班费
        self.jbgz = self.sapinfo._fd_jbf + self.sapinfo._gxr_jbf + self.sapinfo._ps_jbf
        # 假期扣发
        self.jqkf = self.sapinfo._totalqq
        # 其他
        # 其他工资 + 内退基本工资 + 内退增资 + 内退工龄工资 + 代缴三金 + 生活补助 + 考核工资
        self.qt = self.sapinfo._qtgz + self.sapinfo._ntjbgz + \
            self.sapinfo._ntzz + self.sapinfo._ntglgz + \
            self.sapinfo._djsj + self.sapinfo._shbz + self.sapinfo._khgz
        # 高温费
        self.gwf = self.sapinfo._gwf
        # 应发合计 (工资总额同口径)
        self.yfhj = self.sapinfo._totalpayable + self.sapinfo._nddxj
        # 公积金
        self.gjj = 0 - self.sapinfo._gjj
        # 养老
        self.yangl = 0 - self.sapinfo._yl
        # 医疗
        self.yil = 0 - self.sapinfo._yil
        # 失业
        self.sy = 0 - self.sapinfo._sy
        # 年金
        self.nj = 0 - self.sapinfo._nj
        # 所得税
        self.sds = 0 - self.sapinfo._totalsdj
        # 独补
        self.db = self.sapinfo._db
        # 驻外津贴
        self.zwjt = self.sapinfo._zwjt
        # 财务补退(经常性)
        self.cwbtjcx = self.sapinfo._cwbt_jcx
        # 其他财务补退 + 财务扣款
        self.cwbtqt = self.sapinfo._cwbt_qt + self.sapinfo._cwkk
        # 司法扣款
        self.sfkk = self.sapinfo._sfkk
        # 实发合计
        self.sfhj = self.sapinfo._totalpay


class JgSummaryReportData(JgReportSalaryInfo):
    """
    机关汇总表数据定义
    """

    def __init__(self, sapinfo: SapSalaryInfo):
        super().__init__(sapinfo)
        # 审核单位
        self.audit_depart = self.sapinfo.depart
        # 单位
        self.depart = self.sapinfo.two
        if self.is_gf():
            self.depart = self.sapinfo.three
        if not self.depart:
            self.depart = "未知单位"
        # 科室
        self.ks = self.sapinfo.three
        if self.is_gf():
            self.ks = self.sapinfo.four
        if not self.ks:
            self.ks = "未知科室"
        # 机构信息
        self.depart_info = f'{self.depart}_{self.ks}'
        # 人数
        self.p_count = 1

    def add(self, o):
        self.p_count = self.p_count + 1
        self.gwgz = self.gwgz + o.gwgz
        self.blgz = self.blgz + o.blgz
        self.nggz = self.nggz + o.nggz
        self.fzgz = self.fzgz + o.fzgz
        self.zbgz = self.zbgz + o.zbgz
        self.ybjt = self.ybjt + o.ybjt
        self.qtjt = self.qtjt + o.qtjt
        self.yznx = self.yznx + o.yznx
        self.zwbt = self.zwbt + o.zwbt
        self.jj = self.jj + o.jj

        self.jbgz = self.jbgz + o.jbgz
        self.jqkf = self.jqkf + o.jqkf
        self.qt = self.qt + o.qt
        self.gwf = self.gwf + o.gwf
        self.yfhj = self.yfhj + o.yfhj

        self.gjj = self.gjj + o.gjj
        self.yangl = self.yangl + o.yangl
        self.yil = self.yil + o.yil
        self.sy = self.sy + o.sy
        self.nj = self.nj + o.nj
        self.sds = self.sds + o.sds

        self.db = self.db + o.db
        self.zwjt = self.zwjt + o.zwjt
        self.cwbtjcx = self.cwbtjcx + o.cwbtjcx
        self.cwbtqt = self.cwbtqt + o.cwbtqt
        self.sfkk = self.sfkk + o.sfkk
        self.sfhj = self.sfhj + o.sfhj


class JgSummaryReportDataGroupByDepartConventer:
    """
    sapsalaryinfos 按照单位分组
    """

    def __init__(self, sap_salary_infos=[]):
        self.sap_salary_infos = sap_salary_infos

    def groupby_ks(self):
        """
        分组到科室
        """
        res_audit = OrderedDict()
        for sap_salary_info in self.sap_salary_infos:
            report_data = JgSummaryReportData(sap_salary_info)
            audit_depart = report_data.audit_depart
            depart = report_data.depart
            ks = report_data.ks
            res_depart = OrderedDict()
            res_ks = OrderedDict()
            if not audit_depart in res_audit:
                res_ks[ks] = report_data
                res_depart[depart] = res_ks
            else:
                res_depart = res_audit[audit_depart]
                ks_data = OrderedDict()
                if depart in res_depart:
                    ks_data = res_depart[depart]
                    if ks in ks_data:
                        val = ks_data[ks]
                        val.add(report_data)
                    else:
                        ks_data[ks] = report_data
                else:
                    ks_data[ks] = report_data
                res_depart[depart] = ks_data
            res_audit[audit_depart] = res_depart
        return res_audit

    def groupby_depart(self):
        """
        分组到单位
        """
        res_audit = OrderedDict()
        for sap_salary_info in self.sap_salary_infos:
            report_data = JgSummaryReportData(sap_salary_info)
            audit_depart = report_data.audit_depart
            depart = report_data.depart
            res_depart = OrderedDict()
            if not audit_depart in res_audit:
                res_depart[depart] = report_data
            else:
                res_depart = res_audit[audit_depart]
                if depart in res_depart:
                    report_data_c = res_depart[depart]
                    report_data_c.add(report_data)
                    res_depart[depart] = report_data_c
                else:
                    res_depart[depart] = report_data
            res_audit[audit_depart] = res_depart
        return res_audit


class JgPersonDetailReportData(JgReportSalaryInfo):
    def __init__(self, sapinfo: SapSalaryInfo):
        super().__init__(sapinfo)
        # 审核单位
        self.audit_depart = self.sapinfo.depart
        # 单位
        self.depart = self.sapinfo.two
        if self.is_gf():
            self.depart = self.sapinfo.three
        if not self.depart:
            self.depart = "未知单位"
        # 科室
        self.ks = self.sapinfo.three
        if self.is_gf():
            self.ks = self.sapinfo.four
        if not self.ks:
            self.ks = "未知科室"
        self.depart_info = f'{self.depart}_{self.ks}'
        # 职工编码
        self.code = self.sapinfo._code

        # 姓名
        self.name = self.sapinfo._name


class JgPersonDetailReportDataConventer:
    """
    机关格式人员报表格式转换
    """

    def __init__(self, sap_salary_infos=[]):
        self.sap_salary_infos = sap_salary_infos

    def groupby_person(self):
        """
        分组到个人明细
        """
        res_audit = OrderedDict()
        for sap_salary_info in self.sap_salary_infos:
            report_data = JgPersonDetailReportData(sap_salary_info)
            audit_depart = report_data.audit_depart
            depart = report_data.depart
            ks = report_data.ks
            res_depart = OrderedDict()
            res_ks = OrderedDict()
            if not audit_depart in res_audit:
                res_ks[ks] = [report_data]
                res_depart[depart] = res_ks
            else:
                res_depart = res_audit[audit_depart]
                ks_data = OrderedDict()
                if depart in res_depart:
                    ks_data = res_depart[depart]
                    if ks in ks_data:
                        val = ks_data[ks]
                        val.append(report_data)
                    else:
                        ks_data[ks] = [report_data]
                else:
                    ks_data[ks] = [report_data]
                res_depart[depart] = ks_data
            res_audit[audit_depart] = res_depart
        return res_audit
