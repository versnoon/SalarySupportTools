#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   salary_jj_engine.py
@Time    :   2021/01/29 09:08:16
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from salary_support_tools.exl_to_clazz import ExlsToClazz, ExlToClazz


class SalaryJjEngine(object):
    def __init__(self, period, depart=""):
        self._name = "salary_jj"
        self._period = period
        self._depart = depart
        self._folder_prefix = r'd:\薪酬审核文件夹'

    def start(self):
        if self._depart == "":
            raise ValueError("缺少单位信息")
        jj = SalaryJjInfo()
        return jj.to_map(self.load_data(), self._period, self._depart)

    def batch_load_data(self, departs):
        jj = SalaryJjInfo()
        jj_load = ExlsToClazz(
            SalaryJjInfo, jj.getColumnDef(), self.get_exl_tpl_folder_path_batch(), "奖金信息")
        jj_datas = jj_load.loadTemp()
        return self.set_period_and_depart(self._period, departs, jj_datas)

    def load_data(self):
        jj = SalaryJjInfo()
        jj_load = ExlToClazz(
            SalaryJjInfo, jj.getColumnDef(), self.get_exl_tpl_folder_path(), 0, True)
        return jj_load.loadTemp()

    def set_period_and_depart(self, period, departs, jjs):
        """
        设置工资信息的期间信息和单位信息
        """
        for jj in jjs:
            jj.period = self._period
            di = jj._get_depart_from_departfullinfo(departs)
            if di is not None:
                jj.depart = di.get_depart_salaryScope_and_name()
        return jjs

    def get_exl_tpl_folder_path_batch(self):
        return r"{}\{}\{}".format(self._folder_prefix, self._period, "工资奖金数据")

    def get_exl_tpl_folder_path(self):
        return r"{}\{}\{}\{}".format(self._folder_prefix, self._period, self._depart, "奖金信息.xls")


class SalaryJjInfo(object):
    """
    奖金信息
    """

    def __init__(self, code="", name="", departfullinfo="", distributionMark="", ysjse=0, bonusTow=0, gtsyj=0, pay=0, jjhj=0, totalPayable=0, jsjseptsl=0, jbjj=0, gts=0, bonusOne=0, bonusThree=0, yseyhsl=0, yse=0, gstz=0, gcjj=0, jssc=0, nddxj=0, jsjj=0, qt=0, gsxyj=0):
        self.period = ""
        self.depart = ""  # 审批单位文件夹名称
        self._code = code
        self._name = name
        self._departfullinfo = departfullinfo
        self._distributionMark = distributionMark
        self._ysjse = ysjse
        self._bonusTwo = bonusTow
        self._gtsyj = gtsyj
        self._pay = pay
        self._jjhj = jjhj
        self._jsjseptsl = jsjseptsl
        self._jbjj = jbjj
        self._gts = gts
        self._bonusOne = bonusOne
        self._bonusThree = bonusThree
        self._yseyhsl = yseyhsl
        self._yse = yse
        self._totalPayable = totalPayable
        self._gstz = gstz
        self._gcjj = gcjj
        self._jssc = jssc
        self._nddxj = nddxj
        self._jsjj = jsjj
        self._qt = qt
        self._gsxyj = gsxyj

    def _get_departLevelTow(self, i=1):
        departs = self._departfullinfo.split("\\")
        if len(departs) < 2:
            raise ValueError(
                "机构信息错误：{}-{}".format(self._code, self._departfullinfo))
        return departs[i]

    def _get_depart_from_departfullinfo(self, departs):
        for k, v in departs.items():
            relativeUnits = v.get_departs()
            for ru in relativeUnits:
                i = 1
                if k == '49':  # 投资工资 取 1
                    i = 0
                if self._get_departLevelTow(i) == ru:
                    return v
        return None

    def __str__(self):
        return '员工奖金信息: 机构 {} - 工号 {} - 姓名 {} - 应发 {} - 实发 {}'.format(self._departfullinfo, self._code, self._name, self._totalPayable, self._pay)

    def getColumnDef(self) -> dict:
        columns = dict()
        columns["_code"] = "员工通行证"
        columns["_name"] = "员工姓名"
        columns["_departfullinfo"] = "机构"
        columns["_distributionMark"] = "是否代发工资"
        columns["_ysjse"] = "应税计算额(优惠税率)"
        columns["_bonusTwo"] = "单项奖2"
        columns["_gtsyj"] = "个调税(应缴)"
        columns["_pay"] = "实发"
        columns["_jjhj"] = "奖金合计"
        columns["_jsjseptsl"] = "应税计算额(普通税率)"
        columns["_jbjj"] = "基本奖金"
        columns["_gts"] = "个调税"
        columns["_bonusOne"] = "单项奖1"
        columns["_bonusThree"] = "单项奖3"
        columns["_yseyhsl"] = "应税额(优惠税率)"
        columns["_bonusThree"] = "单项奖3"
        columns["_yseyhsl"] = "应税额"
        columns["_totalPayable"] = "应发"
        columns["_gstz"] = "个税调整"
        columns["_gcjj"] = "工程津贴"
        columns["_jssc"] = "技术输出"
        columns["_qt"] = "争取国家政策奖"
        columns["_nddx"] = "年底兑现奖"
        columns["_jsjj"] = "计税奖金"
        return columns

    def to_map(self, datas, period, depart):
        m = dict()
        if datas is not None and len(datas) > 0:
            for i in range(len(datas)):
                info = datas[i]
                info._period = period
                info._dpeart = depart
                if info._code in m:
                    info.to_sum(m[info._code])
                m[info._code] = info
        return m

    def to_sum(self, jj):
        self._ysjse += jj._ysjse
        self._bonusTwo += jj._bonusTwo
        self._gtsyj += jj._gtsyj
        self._pay += jj._pay
        self._jjhj += jj._jjhj
        self._jsjseptsl += jj._jsjseptsl
        self._jbjj += jj._jbjj
        self._gts += jj._gts
        self._bonusOne += jj._bonusOne
        self._bonusThree += jj._bonusThree
        self._yseyhsl += jj._yseyhsl
        self._totalPayable += jj._totalPayable
        self._gstz += jj._gstz
        self._gcjj += jj._gcjj
        self._jssc += jj._jssc
        self._qt += jj._qt
        self._nddxj += jj._nddxj
        self._jsjj += jj._jsjj

    def get_exl_tpl_folder_path_prefix(self):
        return r'd:\薪酬审核文件夹\{}\{}'.format(self.period, self.depart)

    def get_exl_tpl_file_name_prefix(self):
        return '奖金信息'
