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

from salary_support_tools.exl_to_clazz import ExlToClazz


class BonusTplEngine(object):

    """
    考勤模板
    """

    def __init__(self, period, departs):
        self._name = "bonus_tpl_op"
        self._period = period
        self._departs = departs
        self._folder_path = r'd:\薪酬审核文件夹'

    def start(self):
        return self.load_data()

    def load_data(self):
        """
        加载模板
        """
        bonus_info = BonusInfo()
        # 集团机关
        bonus_jt_load = ExlToClazz(
            BonusInfo, bonus_info.get_jt_columns(), self.get_exl_tpl_file_path("集团机关"), 0, True)
        jt_datas = self.group_by_company_depart_info(bonus_jt_load.loadTemp())
        # 教培
        bonus_jp_load = ExlToClazz(
            BonusInfo, bonus_info.get_jp_columns(), self.get_exl_tpl_file_path("教培"), 0, True)
        jp_datas = self.group_by_company_depart_info(bonus_jp_load.loadTemp())
        # 新闻
        bonus_xw_load = ExlToClazz(
            BonusInfo, bonus_info.get_xw_columns(), self.get_exl_tpl_file_path("新闻"), 0, True)
        xw_datas = self.group_by_company_depart_info(bonus_xw_load.loadTemp())
        # 离退
        bonus_lt_load = ExlToClazz(
            BonusInfo, bonus_info.get_lt_columns(), self.get_exl_tpl_file_path("离退休"), 0, True)
        lt_datas = self.group_by_company_depart_info(bonus_lt_load.loadTemp())
        # 保卫部
        bonus_bwb_load = ExlToClazz(
            BonusInfo, bonus_info.get_bwb_columns(), self.get_exl_tpl_file_path("保卫部"), 0, True)
        bwb_datas = self.group_by_company_depart_info(
            bonus_bwb_load.loadTemp())
        # 股份
        bonus_gf_load = ExlToClazz(
            BonusInfo, bonus_info.get_gf_columns(), self.get_exl_tpl_file_path("股份"), 0, True)
        gf_datas = self.group_by_company_depart_info(bonus_gf_load.loadTemp())
        return jt_datas, jp_datas, xw_datas, lt_datas, bwb_datas, gf_datas

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

    def get_exl_tpl_file_path(self, filename):
        return r'{}\{}\{}\{}-{}.xls'.format(self._folder_path, self._period, "考勤奖金模板", "奖金模板", filename)

    def get_exl_tpl_file_name_prefix(self):
        return "奖金模板"


class BonusInfo(object):

    def __init__(self):
        self._code = ""  # 员工通行证
        self._name = ""  # 员工姓名
        self._depart_fullname = ""  # 所在机构
        self._depart_desc = 0  # 发放机构(默认为员工所在机构)
        self._nddx = 0  # 年底兑现奖
        self._dj1 = 0  # 单项奖1
        self._dj2 = 0  # 单项奖2
        self._dj3 = 0  # 单项奖3
        self._jbj = 0  # 基本奖金
        self._gstz = 0  # 个税调整
        self._jsj = 0  # 计税奖金

    def get_gf_columns(self) -> dict:
        """
        股份本部
        """
        columns = dict()
        columns["_code"] = "员工通行证"
        columns["_name"] = "员工姓名"
        columns["_depart_fullname"] = "所在机构"
        columns["_depart_desc"] = "发放机构(默认为员工所在机构)"
        columns["_nddx"] = "年底兑现奖(2652347)"
        columns["_dj1"] = "单项奖1(2652349)"
        columns["_dj2"] = "单项奖2(2652343)"
        columns["_dj3"] = "单项奖3(2652350)"
        columns["_jbj"] = "基本奖金(2652344)"
        columns["_gstz"] = "个税调整(2653810)"
        columns["_jsj"] = "计税奖金(2652342)"
        return columns

    def get_jt_columns(self) -> dict:
        """
        集团机关
        """
        columns = dict()
        columns["_code"] = "员工通行证"
        columns["_name"] = "员工姓名"
        columns["_depart_fullname"] = "所在机构"
        columns["_depart_desc"] = "发放机构(默认为员工所在机构)"
        columns["_nddx"] = "年底兑现奖(2652030)"
        columns["_dj1"] = "单项奖1(2652026)"
        columns["_dj2"] = "单项奖2(2652027)"
        columns["_dj3"] = "单项奖3(2652028)"
        columns["_jbj"] = "基本奖金(2652029)"
        columns["_gstz"] = "个税调整(2653745)"
        columns["_jsj"] = "计税奖金(2652031)"
        return columns

    def get_jp_columns(self) -> dict:
        """
        教培
        """
        columns = dict()
        columns["_code"] = "员工通行证"
        columns["_name"] = "员工姓名"
        columns["_depart_fullname"] = "所在机构"
        columns["_depart_desc"] = "发放机构(默认为员工所在机构)"
        columns["_nddx"] = "年底兑现奖(2652356)"
        columns["_dj1"] = "单项奖1(2652358)"
        columns["_dj2"] = "单项奖2(2652352)"
        columns["_dj3"] = "单项奖3(2652359)"
        columns["_jbj"] = "基本奖金(2652353)"
        columns["_gstz"] = "个税调整(2653811)"
        columns["_jsj"] = "计税奖金(2652351)"
        return columns

    def get_xw_columns(self) -> dict:
        """
        新闻
        """
        columns = dict()
        columns["_code"] = "员工通行证"
        columns["_name"] = "员工姓名"
        columns["_depart_fullname"] = "所在机构"
        columns["_depart_desc"] = "发放机构(默认为员工所在机构)"
        columns["_nddx"] = "年底兑现奖(2652374)"
        columns["_dj1"] = "单项奖1(2652376)"
        columns["_dj2"] = "单项奖2(2652370)"
        columns["_dj3"] = "单项奖3(2652377)"
        columns["_jbj"] = "基本奖金(2652371)"
        columns["_gstz"] = "个税调整(2653812)"
        columns["_jsj"] = "计税奖金(2652369)"
        return columns

    def get_lt_columns(self) -> dict:
        """
        离退休
        """
        columns = dict()
        columns["_code"] = "员工通行证"
        columns["_name"] = "员工姓名"
        columns["_depart_fullname"] = "所在机构"
        columns["_depart_desc"] = "发放机构(默认为员工所在机构)"
        columns["_nddx"] = "年底兑现奖(2652365)"
        columns["_dj1"] = "单项奖1(2652367)"
        columns["_dj2"] = "单项奖2(2652361)"
        columns["_dj3"] = "单项奖3(2652368)"
        columns["_jbj"] = "基本奖金(2652362)"
        columns["_gstz"] = "个税调整(2653813)"
        columns["_jsj"] = "计税奖金(2652360)"
        return columns

    def get_bwb_columns(self) -> dict:
        """
        保卫部
        """
        columns = dict()
        columns["_code"] = "员工通行证"
        columns["_name"] = "员工姓名"
        columns["_depart_fullname"] = "所在机构"
        columns["_depart_desc"] = "发放机构(默认为员工所在机构)"
        columns["_nddx"] = "年底兑现奖(2652392)"
        columns["_dj1"] = "单项奖1(2652394)"
        columns["_dj2"] = "单项奖2(2652388)"
        columns["_dj3"] = "单项奖3(2652395)"
        columns["_jbj"] = "基本奖金(2652389)"
        columns["_gstz"] = "个税调整(2653814)"
        columns["_jsj"] = "计税奖金(2652387)"
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
        return self.split_depart_fullname(0)

    def depart_name(self):
        """
        获取部门名称
        """
        return self.split_depart_fullname(1)
