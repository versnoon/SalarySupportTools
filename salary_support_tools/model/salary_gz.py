#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   SalaryPeriod.py
@Time    :   2021/02/13 11:48:32
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


from collections import OrderedDict

from salary_support_tools.engine.base_period_engine import BasePeriodEngine
from salary_support_tools.model.base_model_cov import BaseModelConventor


class SalaryGz(BasePeriodEngine):
    """
    员工工资相关信息
    """

    NAME = "salary_gz"

    def __init__(self):
        super().__init__(None)
        self.depart = ""  # 单位文件夹名称
        self.tex_depart = ""  # 税务机构
        self._code = ""  # 员工通行证
        self._name = ""  # 员工姓名
        self._depart_fullname = ""  # 机构
        self._departLevelTow = ""  # 二级机构
        self._branchLevelThree = ""  # 三级机构
        self._salaryModel = ""  # 薪酬模式
        self._jobName = ""  # 岗位名称
        self._postPrice = ""  # 岗位价值
        self._distributionMark = ""  # 是否代发工资
        self._fzZxkc = 0  # 累计住房租金支出
        self._fdZxkc = 0  # 累计住房贷款利息支出
        self._jxjyZxkc = 0  # 累计继续教育支出
        self._znjyZxkc = 0  # 累计子女教育支出
        self._sylrZxkc = 0  # 累计赡养老人支出
        self._zxnf = 0
        self._gsgl = 0
        self._lxgl = 0
        self._bjbl = 0
        self._gwxs = 0
        self._gwxbz = 0
        self._gwgz = 0
        self._blgz = 0
        self._glgz = 0
        self._jbx = 0
        self._qtblgz = 0
        self._gdgz = 0   # 固定工资
        self._dtxgz = 0  # 待退休工资
        self._gwx = 0  # 岗位薪
        self._zlx = 0  # 资历薪酬
        self._yfjxnx = 0
        self._shf = 0
        self._jbgzdy = 0
        self._rpjgzkk = 0
        self._rpjgzjk = 0
        # 津贴
        self._zyb_jt = 0
        self._jn_jt = 0
        self._jggz_jt = 0
        self._gzz_jt = 0
        self._kjyx_jt = 0
        self._czns_jt = 0
        self._xl_jt = 0
        self._tx_jt = 0
        self._cq_jt = 0
        self._gw_jt = 0
        self._mz_jt = 0
        self._wc_jt = 0
        self._gs_jt = 0
        self._gshl_jt = 0
        self._js_jt = 0
        self._tsgx_jt = 0
        self._zw_jt = 0  # 驻外津贴
        self._hsz_jt = 0  # 护士长津贴
        self._gongw_jt = 0  # 公务津贴
        self._gexbt_jt = 0  # 各项补贴
        self._sdqnwy_jt = 0  # 水电气暖物业补贴
        self._shbt_jt = 0   # 生活补贴
        self._shfbc_jt = 0  # 生活费补差
        self._gxbt_jt = 0  # 岗薪补贴
        self._total_jt = 0  # 津贴合计
        # 工资补退
        self._rpjgz = 0    # 日平均工资3(津贴)
        self._qtnssr = 0  # 其他纳税收入
        self._ygdxz = 0  # 月固定工资
        self._jxgz = 0  # 绩效工资
        self._jdfdyyz = 0  # 季度浮动月预支
        self._khfd = 0  # 考核浮动
        self._shfbt = 0  # 生活费补贴
        self._dsznf = 0  # 独生子女费
        self._jkdjf = 0  # 兼课带教费

        self._qtdf = 0   # 其他代发
        self._gztz = 0  # 工资调整
        self._qtbf = 0  # 其它补发
        self._qtkk = 0  # 其它扣款
        self._qtdkk = 0  # 其他代扣款
        # 加班
        self._fd_jbgz = 0
        self._xxr_jbgz = 0
        self._ps_jbgz = 0
        self._total_jbgz = 0

        # 扣款
        self._bjkk_kk = 0
        self._sjkk_kk = 0
        self._kgkk_kk = 0
        self._total_kk = 0

        # 社保公积金年金
        self._yl_bx = 0  # 养老
        self._yil_bx = 0  # 医疗
        self._sy_bx = 0  # 失业
        self._gjj_bx = 0  # 公积金
        self._nj_bx = 0  # 年金
        self._gjjbz_bx = 0  # 公积金补助

        self._totalPayable = 0  # 应发
        self._yse = 0  # 应发额
        self._gts = 0  # 个调税
        self._dfxm = 0  # 代发项目
        self._bfone = 0  # 补发1
        self._bftwo = 0  # 补发2
        self._total_dk = 0  # 代扣合计
        self._pay = 0  # 实发

        # 企业部分
        self._yl_qybx = 0  # 养老
        self._yl_bj_qybx = 0  # 养老补缴
        self._yil_qybx = 0  # 医疗
        self._yil_bj_qybx = 0  # 医疗补缴
        self._sy_qybx = 0  # 失业
        self._sy_bj_qybx = 0  # 失业补缴
        self._shy_qybx = 0  # 生育
        self._gs_qybx = 0  # 工伤
        self._gjj_qybx = 0  # 公积金
        self._nj_qybx = 0  # 年金

    def __str__(self):
        return '员工工资信息: 机构 {} - 二级机构 {} - 三级机构 {} - 工号 {} - 姓名 {} - 岗位 {} - 应发 {}'.format(self._depart_fullname, self._departLevelTow, self._branchLevelThree, self._code, self._name, self._jobName, self._totalPayable)

    @classmethod
    def cols(self):
        cols = dict()
        cols["_code"] = "员工通行证"
        cols["_name"] = "员工姓名"
        cols["_depart_fullname"] = "机构"
        cols["_departLevelTow"] = "二级机构"
        cols["_branchLevelThree"] = "三级机构"
        cols["_salaryModel"] = "薪酬模式"
        cols["_jobName"] = "岗位名称"
        cols["_postPrice"] = "岗位价值"
        cols["_distributionMark"] = "是否代发工资"
        cols["_fzZxkc"] = "累计住房租金支出"
        cols["_fdZxkc"] = "累计住房贷款利息支出"
        cols["_jxjyZxkc"] = "累计继续教育支出"
        cols["_znjyZxkc"] = "累计子女教育支出"

        cols["_sylrZxkc"] = "累计赡养老人支出"
        cols["_zxnf"] = "执行年份"
        cols["_gsgl"] = "公司工龄"
        cols["_lxgl"] = "连续工龄"
        cols["_bjbl"] = "病假扣款比例"
        cols["_gwxs"] = "岗位系数"
        cols["_gwxbz"] = "岗位薪标准"
        cols["_gwgz"] = "岗位工资"
        cols["_blgz"] = "保留工资"
        cols["_glgz"] = "工龄工资"
        cols["_jbx"] = "基本薪"
        cols["_qtblgz"] = "其他保留工资"
        cols["_gdgz"] = "固定工资"
        cols["_dtxgz"] = "待退休工资"
        cols["_gwx"] = "岗位薪"
        cols["_zlx"] = "资历薪"
        cols["_yfjxnx"] = "预发绩效年薪"
        cols["_shf"] = "生活费"
        cols["_jbgzdy"] = "基本工资单元"
        cols["_rpjgzkk"] = "日平均工资(扣款)"
        cols["_rpjgzjk"] = "日平均工资2(加款)"

        cols["_zyb_jt"] = "中夜班津贴"
        cols["_jn_jt"] = "技能津贴"
        cols["_jggz_jt"] = "兼岗工资"
        cols["_gzz_jt"] = "班组长津贴"
        cols["_kjyx_jt"] = "科技优秀津贴"
        cols["_czns_jt"] = "操作能手津贴"
        cols["_xl_jt"] = "学历津贴"
        cols["_tx_jt"] = "通讯补贴"
        cols["_cq_jt"] = "出勤津贴"
        cols["_gw_jt"] = "高温津贴"
        cols["_mz_jt"] = "民族津贴"
        cols["_wc_jt"] = "误餐补助"
        cols["_gs_jt"] = "工伤津贴"
        cols["_gshl_jt"] = "工伤护理费"
        cols["_js_jt"] = "技术津贴"
        cols["_tsgx_jt"] = "特殊贡献津贴"
        cols["_zw_jt"] = "驻外津贴"  # 驻外津贴
        # cols["_hsz_jt"] = "护士长津贴"

        cols["_gongw_jt"] = "公务车贴"
        cols["_gexbt_jt"] = "各项补贴"
        cols["_sdqnwy_jt"] = "水电气暖物业补贴"
        cols["_shbt_jt"] = "生活补贴"
        cols["_shfbc_jt"] = "生活费补差"
        cols["_gxbt_jt"] = "岗薪补贴"
        cols["_total_jt"] = "津贴合计"
        cols["_rpjgz"] = "日平均工资3(津贴)"
        cols["_qtnssr"] = "其它纳税收入"
        cols["_ygdxz"] = "月固定薪资"
        cols["_jxgz"] = "绩效工资"
        cols["_jdfdyyz"] = "季度浮动月预支"
        cols["_khfd"] = "考核浮动"
        cols["_shfbt"] = "生活费补贴"
        cols["_dsznf"] = "独生子女费"
        cols["_jkdjf"] = "兼课带教费"

        cols["_qtdf"] = "其他代发"
        cols["_gztz"] = "工资调整"
        cols["_qtbf"] = "其它补发"
        cols["_qtkk"] = "其它扣款"
        cols["_qtdkk"] = "其他代扣款"

        cols["_fd_jbgz"] = "法定假日加班工资"
        cols["_xxr_jbgz"] = "休息日加班工资"
        cols["_ps_jbgz"] = "平常加班工资"
        cols["_total_jbgz"] = "加班工资单元"

        cols["_bjkk_kk"] = "病假扣款"
        cols["_sjkk_kk"] = "事假扣款"
        cols["_kgkk_kk"] = "旷工扣款"
        cols["_total_kk"] = "缺勤扣款单元"

        cols["_yl_bx"] = "养老保险个人额度"
        cols["_sy_bx"] = "失业保险个人额度"
        cols["_yil_bx"] = "医疗保险个人额度"
        cols["_gjj_bx"] = "公积金个人额度"
        cols["_nj_bx"] = "企业年金个人额度"

        cols["_gjjbz_bx"] = "公积金补助"
        cols["_totalPayable"] = "应发"
        cols["_yse"] = "应税额"
        cols["_gts"] = "个调税"
        cols["_dfxm"] = "代发项目"
        cols["_bfone"] = "补发一"

        cols["_bftwo"] = "补发二"
        cols["_total_dk"] = "代扣合计"
        cols["_pay"] = "实发"
        cols["_yl_qybx"] = "养老保险企业额度"
        cols["_sy_qybx"] = "失业保险企业额度"
        cols["_yil_qybx"] = "医疗保险企业额度"
        cols["_shy_qybx"] = "生育保险企业额度"
        cols["_gs_qybx"] = "工伤保险企业额度"
        cols["_gjj_qybx"] = "公积金企业额度"
        cols["_nj_qybx"] = "企业年金企业额度"
        return cols


class SalaryGzConventor(BaseModelConventor):

    def cov(self, datas, period, departs):
        res = OrderedDict()
        for data in datas:
            data.period = period
            company, depart_str = self._get_depart_byfullname(
                data._depart_fullname, departs)
            code = data._code
            vs = OrderedDict()
            vs_depart = OrderedDict()
            if company in res:
                vs = res[company]
            if depart_str in vs:
                vs_depart = vs[depart_str]
            vs_depart[code] = data
            vs[depart_str] = vs_depart
            res[company] = vs
        return res
