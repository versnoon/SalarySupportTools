#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   salary_gz_engine.py
@Time    :   2021/01/29 08:18:35
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


from collections import OrderedDict

from salary_support_tools.exl_to_clazz import ExlsToClazz, ExlToClazz


class SalaryGzEngine(object):
    def __init__(self, period, depart=""):
        self._name = "salary_gz"
        self._period = period
        self._depart = depart
        self._folder_prefix = r'd:\薪酬审核文件夹'

    def start(self):
        if self._depart == "":
            raise ValueError("缺少单位信息")
        gz = SalaryGzInfo()
        gz_load = ExlToClazz(
            SalaryGzInfo, gz.getColumnDef(), self.get_exl_tpl_folder_path(), 0, True)
        return gz.to_map(gz_load.loadTemp(), self._period, self._depart)

    def batch_load_data(self, departs):
        gz = SalaryGzInfo()
        gz_load = ExlsToClazz(
            SalaryGzInfo, gz.getColumnDef(), self.get_exl_tpl_folder_path_batch(), "工资信息")
        gz_datas = gz_load.loadTemp()
        return self.set_period_and_depart(self._period, departs, gz_datas)

    def load_data(self):
        gz = SalaryGzInfo()
        gz_load = ExlToClazz(
            SalaryGzInfo, gz.getColumnDef(), self.get_exl_tpl_folder_path(), 0, True)
        return gz_load.loadTemp()

    def set_period_and_depart(self, period, departs, gzs):
        """
        设置工资信息的期间信息和单位信息
        """
        for gz in gzs:
            gz.period = self._period
            di = gz._get_depart_from_departLevelTow(departs)
            if di is not None:
                gz.depart = di.get_depart_salaryScope_and_name()
        return gzs

    def get_exl_tpl_folder_path_batch(self):
        return r"{}\{}\{}".format(self._folder_prefix, self._period, "工资奖金数据")

    def get_exl_tpl_folder_path(self):
        return r"{}\{}\{}\{}".format(self._folder_prefix, self._period, self._depart, "工资信息.xls")


class SalaryGzInfo(object):
    """
    工资信息
    """

    def __init__(self, code="", name="", departfullinfo="", depart="", branch="", salaryModel="", jobName="", postPrice="", distributionMark="", fzZxkc=0, fdZxkc=0, jxjyZxkc=0, znjyZxkc=0, sylrZxkc=0, zxnf=0, gsgl=0, lxgl=0, bjbl=0, gwxs=0, gwxbz=0, gwgz=0, blgz=0, glgz=0, jbx=0, qtblgz=0, gdgz=0, dtxgz=0, gwx=0, zlx=0, yfjxnx=0, shf=0, jbgzdy=0, rpjgzkk=0, rpjgzjk=0, zybjt=0, jnjt=0, jggzjt=0, gzzjt=0, kjyxjt=0, cznsjt=0, xljt=0, txjt=0, cqjt=0, gwjt=0, mzjt=0, wcjt=0, gsjt=0, gshljt=0, jsjt=0, tsgxjt=0, zwjt=0, gongwjt=0, gxbtjt=0, sdqnwyjt=0, shbtjt=0, shfbcjt=0, totaljt=0, rpjgz=0, qtnssr=0, ygdxz=0, jxgz=0, jdfdyyz=0, khfd=0, shfbt=0, dsznf=0, jkdjf=0, qtdf=0, kdjf=0, gztz=0, qtbf=0, qtkk=0, qtdkk=0, fdjbgz=0, xxrjbgz=0, psjbgz=0, totaljbgz=0, bjkk=0, sjkk=0, kgkk=0, totalkk=0, yl=0, yil=0, sy=0, gjj=0, nj=0, gjjbz=0, yse=0, gts=0, dfxm=0, bfone=0, bftwo=0, totaldk=0, pay=0, ylqybx=0, yilqybx=0, syqybx=0, shyqybx=0, gsqybx=0, gjjqybx=0, njqybx=0, totalPayable=0):
        self.period = ""
        self.depart = ""  # 单位文件夹名称
        self._code = ""  # 员工通行证
        self._name = name  # 员工姓名
        self._departfullinfo = departfullinfo  # 机构
        self._departLevelTow = depart  # 二级机构
        self._branchLevelThree = branch  # 三级机构
        self._salaryModel = salaryModel  # 薪酬模式
        self._jobName = jobName  # 岗位名称
        self._postPrice = postPrice  # 岗位价值
        self._distributionMark = distributionMark  # 是否代发工资
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
        return '员工工资信息: 机构 {} - 二级机构 {} - 三级机构 {} - 工号 {} - 姓名 {} - 岗位 {} - 应发 {}'.format(self._departfullinfo, self._departLevelTow, self._branchLevelThree, self._code, self._name, self._jobName, self._totalPayable)

    def _get_departLevelTow(self, i=1):
        departs = self._departfullinfo.split("\\")
        if len(departs) < 2:
            raise ValueError(
                "机构信息错误：{}-{}".format(self._code, self._departfullinfo))
        return departs[i]

    def _get_depart_from_departLevelTow(self, departs):
        for k, v in departs.items():
            relativeUnits = v.get_departs()
            for ru in relativeUnits:
                i = 1
                if k == '49':  # 投资工资 取 1
                    i = 0
                if self._get_departLevelTow(i) == ru:
                    return v
        return None

    def getColumnDef(self) -> dict:
        columns = OrderedDict()
        columns["_code"] = "员工通行证"
        columns["_name"] = "员工姓名"
        columns["_departfullinfo"] = "机构"
        columns["_departLevelTow"] = "二级机构"
        columns["_branchLevelThree"] = "三级机构"
        columns["_salaryModel"] = "薪酬模式"
        columns["_jobName"] = "岗位名称"
        columns["_postPrice"] = "岗位价值"
        columns["_distributionMark"] = "是否代发工资"
        columns["_fzZxkc"] = "累计住房租金支出"
        columns["_fdZxkc"] = "累计住房贷款利息支出"
        columns["_jxjyZxkc"] = "累计继续教育支出"
        columns["_jxjyZxkc"] = "累计子女教育支出"

        columns["_sylrZxkc"] = "累计赡养老人支出"
        columns["_zxnf"] = "执行年份"
        columns["_gsgl"] = "公司工龄"
        columns["_lxgl"] = "连续工龄"
        columns["_bjbl"] = "病假扣款比例"
        columns["_gwxs"] = "岗位系数"
        columns["_gwxbz"] = "岗位薪标准"
        columns["_gwgz"] = "岗位工资"
        columns["_blgz"] = "保留工资"
        columns["_glgz"] = "工龄工资"
        columns["_jbx"] = "基本薪"
        columns["_qtblgz"] = "其他保留工资"
        columns["_gdgz"] = "固定工资"
        columns["_dtxgz"] = "待退休工资"
        columns["_gwx"] = "岗位薪"
        columns["_zlx"] = "资历薪"
        columns["_yfjxnx"] = "预发绩效年薪"
        columns["_shf"] = "生活费"
        columns["_jbgzdy"] = "基本工资单元"
        columns["_rpjgzkk"] = "日平均工资(扣款)"
        columns["_rpjgzjk"] = "日平均工资2(加款)"

        columns["_zyb_jt"] = "中夜班津贴"
        columns["_jn_jt"] = "技能津贴"
        columns["_jggz_jt"] = "兼岗工资"
        columns["_gzz_jt"] = "班组长津贴"
        columns["_kjyx_jt"] = "科技优秀津贴"
        columns["_czns_jt"] = "操作能手津贴"
        columns["_xl_jt"] = "学历津贴"
        columns["_tx_jt"] = "通讯补贴"
        columns["_cq_jt"] = "出勤津贴"
        columns["_gw_jt"] = "高温津贴"
        columns["_mz_jt"] = "民族津贴"
        columns["_wc_jt"] = "误餐补助"
        columns["_gs_jt"] = "工伤津贴"
        columns["_gshl_jt"] = "工伤护理费"
        columns["_js_jt"] = "技术津贴"
        columns["_tsgx_jt"] = "特殊贡献津贴"
        columns["_zw_jt"] = "驻外津贴"  # 驻外津贴
        # columns["_hsz_jt"] = "护士长津贴"

        columns["_gongw_jt"] = "公务车贴"
        columns["_gexbt_jt"] = "各项补贴"
        columns["_sdqnwy_jt"] = "水电气暖物业补贴"
        columns["_shbt_jt"] = "生活补贴"
        columns["_shfbc_jt"] = "生活费补差"
        columns["_gxbt_jt"] = "岗薪补贴"
        columns["_total_jt"] = "津贴合计"
        columns["_rpjgz"] = "日平均工资3(津贴)"
        columns["_qtnssr"] = "其它纳税收入"
        columns["_ygdxz"] = "月固定薪资"
        columns["_jxgz"] = "绩效工资"
        columns["_jdfdyyz"] = "季度浮动月预支"
        columns["_khfd"] = "考核浮动"
        columns["_shfbt"] = "生活费补贴"
        columns["_dsznf"] = "独生子女费"
        columns["_jkdjf"] = "兼课带教费"

        columns["_qtdf"] = "其他代发"
        columns["_gztz"] = "工资调整"
        columns["_qtbf"] = "其它补发"
        columns["_qtkk"] = "其它扣款"
        columns["_qtdkk"] = "其他代扣款"

        columns["_fd_jbgz"] = "法定假日加班工资"
        columns["_xxr_jbgz"] = "休息日加班工资"
        columns["_ps_jbgz"] = "平常加班工资"
        columns["_total_jbgz"] = "加班工资单元"

        columns["_bjkk_kk"] = "病假扣款"
        columns["_sjkk_kk"] = "事假扣款"
        columns["_kgkk_kk"] = "旷工扣款"
        columns["_total_kk"] = "缺勤扣款单元"

        columns["_yl_bx"] = "养老保险个人额度"
        columns["_sy_bx"] = "失业保险个人额度"
        columns["_yil_bx"] = "医疗保险个人额度"
        columns["_gjj_bx"] = "公积金个人额度"
        columns["_nj_bx"] = "企业年金个人额度"

        columns["_gjjbz_bx"] = "公积金补助"
        columns["_totalPayable"] = "应发"
        columns["_yse"] = "应税额"
        columns["_gts"] = "个调税"
        columns["_dfxm"] = "代发项目"
        columns["_bfone"] = "补发一"

        columns["_bftwo"] = "补发二"
        columns["_total_dk"] = "代扣合计"
        columns["_pay"] = "实发"
        columns["_yl_qybx"] = "养老保险企业额度"
        columns["_sy_qybx"] = "失业保险企业额度"
        columns["_yil_qybx"] = "医疗保险企业额度"
        columns["_shy_qybx"] = "生育保险企业额度"
        columns["_gs_qybx"] = "工伤保险企业额度"
        columns["_gjj_qybx"] = "公积金企业额度"
        columns["_nj_qybx"] = "企业年金企业额度"

        return columns

    def to_map(self, datas, period, depart):
        m = dict()
        if datas is not None and len(datas) > 0:
            for i in range(len(datas)):
                info = datas[i]
                info._period = period
                info._depart = depart
                m[info._code] = info
        return m
