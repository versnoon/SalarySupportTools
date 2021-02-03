#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   attendence_split_operator.py
@Time    :   2021/02/03 10:22:22
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from os.path import exists
from os import makedirs

from salary_support_tools.exl_to_clazz import ExlsToClazz


class AttendanceTplEngine(object):

    """
    考勤模板
    """

    def __init__(self, period, departs):
        self._name = "attendance_tpl_op"
        self._period = period
        self._departs = departs
        self._folder_path = r'd:\薪酬审核文件夹'

    def start(self):
        datas = self.load_data()
        return self.group_by_company_depart_info(datas)

    def load_data(self):
        """
        加载模板
        """
        attendance_info = AttendanceInfo()
        attendance_load = ExlsToClazz(
            AttendanceInfo, attendance_info.getColumnDef(), self.get_exl_tpl_folder_path_prefix(), self.get_exl_tpl_file_name_prefix(), 0, True)
        return attendance_load.loadTemp()

    def group_by_company_depart_info(self, datas):
        """
        将考勤模板数据按照单位部门分组
        """
        res = dict()
        for info in datas:
            self.group_by_depart_info(info, res)
        return res

    def group_by_depart_info(self, attendance_info, res: dict):
        for dcode, depart in self._departs.items():
            res_key = depart.get_depart_salaryScope_and_name()
            # 加入对机关的判断
            if depart.is_depart(attendance_info.company_name()):
                vss = dict()
                if res_key in res:
                    vss = res[res_key]
                vss_key = attendance_info.depart_name()
                if depart.contain_relativeunits():
                    vss_key = attendance_info.company_name()
                vs = []
                if vss_key in vss:
                    vs = vss[vss_key]
                vs.append(attendance_info)

                vss[vss_key] = vs
                res[res_key] = vss

    def get_exl_tpl_folder_path_prefix(self):
        path = r'{}\{}\{}'.format(self._folder_path, self._period, "考勤奖金模板")
        if not exists(path):
            makedirs(path)
        return path

    def get_exl_tpl_file_name_prefix(self):
        return "考勤模板"


class AttendanceInfo(object):

    def __init__(self):
        self._code = ""  # 员工通行证
        self._name = ""  # 员工姓名
        self._depart_fullname = ""  # 员工部门
        self._dyb = 0  # 大夜班天数

        self._bj = 0  # 病假天数
        self._hj = 0  # 婚假天数
        self._shj = 0  # 事假天数
        self._sj = 0  # 丧假天数
        self._fdjb = 0  # 法定假日加班天数
        self._gxrjb = 0  # 公休日加班天数
        self._btj = 0  # 保胎假天数
        self._tqj = 0  # 探亲假
        self._xyb = 0  # 小夜班天数
        self._gs = 0  # 工伤假
        self._cj = 0  # 产假

        self._hlj = 0  # 护理假天数
        self._baoj = 0  # 保健天数
        self._zb = 0  # 值班个数
        self._dsb = 0  # 大三班天数

        self._kg = 0  # 旷工天数
        self._nxj = 0  # 年休假

    def getColumnDef(self) -> dict:
        columns = dict()
        columns["_code"] = "员工通行证"
        columns["_name"] = "员工姓名"
        columns["_depart_fullname"] = "员工部门"
        columns["_dyb"] = "大夜班天数"
        columns["_bj"] = "病假天数"
        columns["_hj"] = "婚假天数"
        columns["_shj"] = "事假天数"
        columns["_sj"] = "丧假天数"
        columns["_fdjb"] = "法定假日加班天数"
        columns["_gxrjb"] = "公休日加班天数"
        columns["_btj"] = "保胎假天数"
        columns["_tqj"] = "探亲假"
        columns["_xyb"] = "小夜班天数"
        columns["_gs"] = "工伤假"
        columns["_cj"] = "产假"
        columns["_hlj"] = "护理假天数"
        columns["_baoj"] = "保健天数"
        columns["_zb"] = "值班个数"
        columns["_dsb"] = "大三班天数"
        columns["_kg"] = "旷工天数"
        columns["_nxj"] = "年休假"
        return columns

    def split_depart_fullname(self, levelno: int):
        depart_strs = self._depart_fullname.split('\\')
        max_level = len(depart_strs) - 1
        if levelno > max_level:
            levelno = max_level
        return depart_strs[levelno]

    def company_name(self):
        """
        获取单位名称
        """
        return self.split_depart_fullname(1)

    def depart_name(self):
        """
        获取部门名称
        """
        return self.split_depart_fullname(2)
