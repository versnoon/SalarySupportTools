#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   salary_operator.py
@Time    :   2021/02/01 21:02:34
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from os.path import exists
from os import remove, makedirs
import time


from collections import OrderedDict

import xlwt

from salary_support_tools.salary_jj_engine import SalaryJjInfo
from salary_support_tools.salary_gz_engine import SalaryGzInfo


class SalaryReportOperator(object):

    """
    # 薪酬数据相关表格输出
    # 1 工资文件输出
    # 2 奖金文件输出
    # 3 审核结果输出
    # 4 Sh003 格式输出
    # 5 Sh002 格式输出

    """

    def __init__(self, period, departs, gz_datas, jj_datas, person_salary_infos, sap_infos, err_msgs):
        self._period = period
        self._departs = departs
        self._gz_datas = gz_datas
        self._jj_datas = jj_datas
        self._sap_infos = sap_infos
        self._person_salary_infos = person_salary_infos
        self._err_msgs = err_msgs
        self._folder_path = r'd:\薪酬审核文件夹'
        self._exportable = False  # 导出开关 如果为True 无论验证结果 都导出

    def export(self):
        # sh002 格式输出
        self.export_sh002_excel()
        # sh003 格式输出
        self.export_sh003_excel()

    def sh002_columns(self):
        columns = dict()
        columns["_sfhd"] = "实发核对"
        columns["one"] = "一级组织"
        columns["two"] = "二级组织"
        columns["three"] = "三级组织"
        columns["four"] = "四级组织"
        columns["five"] = "五级组织"
        columns["_code"] = "员工编号"
        columns["_name"] = "员工姓名"
        columns["_idno"] = "身份证"
        columns["salaryScope"] = "工资范围"
        columns["rsfw"] = "人事范围"
        columns["_ygz"] = "员工组"
        columns["_ygzz"] = "员工子组"
        columns["zw"] = "职位"
        columns["zz"] = "职族"

        columns["_gwgz"] = "岗位工资"
        columns["_blgz"] = "保留工资"
        columns["_nggz"] = "年功工资"
        columns["_fzgz"] = "辅助工资"
        columns["_shbz"] = "生活补助"
        columns["_khgz"] = "考核工资"
        columns["_gzbt"] = "工资补退"
        columns["_qtgz"] = "其他工资"
        columns["_ntjbgz"] = "内退基本工资"
        columns["_ntzz"] = "内退增资"
        columns["_ntglgz"] = "内退工龄工资"
        columns["_djsj"] = "代缴三金"
        columns["_wjbt"] = "物价补贴"
        columns["_ybjt"] = "夜班津贴"
        columns["_jsjt"] = "技师津贴"
        columns["_yzdnjt"] = "一专多能工津贴"
        columns["_ksjt"] = "矿山津贴"
        columns["_xjjt"] = "下井津贴"
        columns["_zwjt"] = "教、护龄津贴"
        columns["_hszjt"] = "护士长津贴"
        columns["_wyjt"] = "外语津贴"
        columns["_bzzjt"] = "班组长津贴"
        columns["_kjjt"] = "科技津贴"
        columns["_nsjt"] = "能手津贴"

        columns["_jbjj"] = "基本奖金"
        columns["_onejj"] = "单项奖1"
        columns["_twojj"] = "单项奖2"
        columns["_threejj"] = "单项奖3"
        columns["_fd_jbf"] = "法定节日加班工资"
        columns["_gxr_jbf"] = "公休日加班工资"
        columns["_ps_jbf"] = "平时加班工资"
        columns["_totalqq"] = "缺勤扣款合计"
        columns["_gjj"] = "公积金"
        columns["_yl"] = "养老保险"
        columns["_yil"] = "医疗保险缴"
        columns["_sy"] = "失业保险"
        columns["_yl_bj"] = "养老保险补缴"
        columns["_yil_bj"] = "医疗保险补缴"
        columns["_sy_bj"] = "失业保险补缴"
        columns["_nj"] = "年金"
        columns["_totalsdj"] = "工资税收"
        columns["_sljj"] = "水利基金"
        columns["_cwkk"] = "财务扣款"
        columns["_df"] = "电费"
        columns["_fz"] = "房租"
        columns["_dsf"] = "收视费"
        columns["_qjf"] = "清洁费"
        columns["_ccf"] = "乘车费用"
        columns["_cwbt"] = "财务补退"
        columns["_wybt"] = "物业补贴"
        columns["_bjf"] = "保健费"
        columns["_db"] = "独补"
        columns["_txf"] = "通讯费"
        columns["_gwf"] = "防暑降温"
        columns["_hm"] = "回民"
        columns["_jj"] = "纪检津贴"
        columns["_js"] = "计生津贴"
        columns["_wc"] = "误餐补贴"
        columns["_ksryj"] = "矿山荣誉金"
        columns["_xf"] = "信访津贴"
        columns["_scjt"] = "伤残津贴"
        columns["_zwbt"] = "职务补贴"
        columns["_kyxm"] = "科研项目津贴"
        columns["_jsgg"] = "技术攻关津贴"
        columns["_fgzjtbf"] = "非工资性津贴补发"

        columns["_totalpayable"] = "工资应发"
        columns["_totalpay"] = "实发工资"
        columns["_jyjf"] = "教育经费"
        columns["_gcjj"] = "工程津贴"
        columns["_jssc"] = "技术输出"
        columns["_qt"] = "其他"
        columns["_gsxyj"] = "公司效益奖"
        columns["_gsxyjpay"] = "上卡效益奖"
        columns["_gsxyjtex"] = "效益奖所得税"
        columns["_nddxj"] = "年底兑现奖"
        columns["_nddxjpay"] = "年终奖实发"
        columns["_nddxjtex"] = "年终奖所得税"
        columns["_jsjj"] = "计税奖金"
        columns["_yznx"] = "预支年薪"
        columns["_zygz"] = "执业工资"

        columns["_gzpay"] = "上卡工资"
        columns["_nddxjpay1"] = "上卡年终奖"
        columns["_jjpay"] = "上卡基本奖"
        columns["_bankno1"] = "银行卡1"
        columns["_bankinfo1"] = "银行1"
        columns["_bankno2"] = "银行卡2"
        columns["_bankinfo2"] = "银行2"
        columns["_znjy"] = "子女教育"
        columns["_jxjy"] = "继续教育"
        columns["_zfdk"] = "住房贷款利息"
        columns["_zffz"] = "住房租金"
        columns["_sylr"] = "赡养老人"
        columns["_mggl"] = "马钢工龄"
        columns["_gl"] = "工龄"
        columns["_cwdf"] = "财务代发计税项"
        columns["_cwdff"] = "财务代发非计税项"
        columns["_ljyf"] = "累计应发"
        columns["_ljwx"] = "累计五险两金"
        columns["_ljqt"] = "累计其他计税"
        columns["_ljjm"] = "累计标准免税额"
        columns["_ljtex"] = "累计个税"

        return columns

    def export_sh002_excel(self):
        """
        创建excel
        """
        columndefs = self.sh002_columns()
        for depart, vs in self._sap_infos.items():
            if not self.exportable(depart):  # 如果有错误信息就跳过
                continue
            datas = vs.values()
            b = xlwt.Workbook(encoding='uft-8')
            s = b.add_sheet('Sheet1')

            # 写入标题
            for i, v in enumerate(columndefs.values()):
                s.write(0, i, v)
            for i, v in enumerate(datas):
                for j, propertyName in enumerate(columndefs.keys()):
                    try:
                        if propertyName == "one":
                            s.write(
                                i + 1, j, "马钢集团")
                        elif propertyName == "two" and getattr(v, "one", 0) != "马钢（集团）控股有限公司(总部)":
                            s.write(
                                i + 1, j, getattr(datas[i], "one", 0))
                        elif propertyName == "three" and getattr(v, "one", 0) != "马钢（集团）控股有限公司(总部)":
                            s.write(
                                i + 1, j, getattr(v, "two", 0))
                        elif propertyName == "four" and getattr(v, "one", 0) != "马钢（集团）控股有限公司(总部)":
                            s.write(
                                i + 1, j, getattr(v, "three", 0))
                        elif propertyName == "five" and getattr(v, "one", 0) != "马钢（集团）控股有限公司(总部)":
                            s.write(
                                i + 1, j, getattr(v, "four", 0))
                        else:
                            s.write(
                                i+1, j, getattr(v, propertyName, 0))
                    except TypeError:
                        print(propertyName)

            path = r'{}\{}\{}\导出文件'.format(
                self._folder_path, self._period, depart)
            if not exists(path):
                makedirs(path)
            b.save(r'{}\{}_{}_{}'.format(
                path, depart, self._period, "SAPSH002.xls"))

    def sh003_columns(self):
        columns = dict()
        columns["_sfhd"] = "实发核对"
        columns["one"] = "一级组织"
        columns["two"] = "二级组织"
        columns["three"] = "三级组织"
        columns["four"] = "四级组织"
        columns["five"] = "五级组织"
        columns["_code"] = "员工编号"
        columns["_name"] = "员工姓名"
        columns["_idno"] = "身份证"
        columns["salaryScope"] = "工资范围"
        columns["rsfw"] = "人事范围"
        columns["_ygz"] = "员工组"
        columns["_ygzz"] = "员工子组"
        columns["zw"] = "职位"
        columns["zz"] = "职族"

        columns["_gwgz"] = "岗位工资"
        columns["_blgz"] = "保留工资"
        columns["_nggz"] = "年功工资"
        columns["_fzgz"] = "辅助工资"
        columns["_shbz"] = "生活补助"
        columns["_khgz"] = "考核工资"
        columns["_gzbt"] = "工资补退"
        columns["_qtgz"] = "其他工资"
        columns["_ntjbgz"] = "内退基本工资"
        columns["_ntzz"] = "内退增资"
        columns["_ntglgz"] = "内退工龄工资"
        columns["_djsj"] = "代缴三金"
        columns["_wjbt"] = "物价补贴"
        columns["_ybjt"] = "夜班津贴"
        columns["_jsjt"] = "技师津贴"
        columns["_yzdnjt"] = "一专多能工津贴"
        columns["_ksjt"] = "矿山津贴"
        columns["_xjjt"] = "下井津贴"
        columns["_zwjt"] = "教、护龄津贴"
        columns["_hszjt"] = "护士长津贴"
        columns["_wyjt"] = "外语津贴"
        columns["_bzzjt"] = "班组长津贴"
        columns["_kjjt"] = "科技津贴"
        columns["_nsjt"] = "能手津贴"

        columns["_jbjj"] = "基本奖金"
        columns["_onejj"] = "单项奖1"
        columns["_twojj"] = "单项奖2"
        columns["_threejj"] = "单项奖3"
        columns["_fd_jbf"] = "法定节日加班工资"
        columns["_gxr_jbf"] = "公休日加班工资"
        columns["_ps_jbf"] = "平时加班工资"
        columns["_totalqq"] = "缺勤扣款合计"
        columns["_gjj"] = "公积金"
        columns["_yl"] = "养老保险"
        columns["_yil"] = "医疗保险缴"
        columns["_sy"] = "失业保险"
        columns["_yl_bj"] = "养老保险补缴"
        columns["_yil_bj"] = "医疗保险补缴"
        columns["_sy_bj"] = "失业保险补缴"
        columns["_nj"] = "年金"
        columns["_totalsdj"] = "工资税收"
        columns["_sljj"] = "水利基金"
        columns["_cwkk"] = "财务扣款"
        columns["_df"] = "电费"
        columns["_fz"] = "房租"
        columns["_dsf"] = "收视费"
        columns["_qjf"] = "清洁费"
        columns["_ccf"] = "乘车费用"
        columns["_cwbt"] = "财务补退"
        columns["_wybt"] = "物业补贴"
        columns["_bjf"] = "保健费"
        columns["_db"] = "独补"
        columns["_txf"] = "通讯费"
        columns["_gwf"] = "防暑降温"
        columns["_hm"] = "回民"
        columns["_jj"] = "纪检津贴"
        columns["_js"] = "计生津贴"
        columns["_wc"] = "误餐补贴"
        columns["_ksryj"] = "矿山荣誉金"
        columns["_xf"] = "信访津贴"
        columns["_scjt"] = "伤残津贴"
        columns["_zwbt"] = "职务补贴"
        columns["_kyxm"] = "科研项目津贴"
        columns["_jsgg"] = "技术攻关津贴"
        columns["_fgzjtbf"] = "非工资性津贴补发"

        columns["_totalpayable"] = "工资应发"
        columns["_totalpay"] = "实发工资"
        columns["_jyjf"] = "教育经费"
        columns["_gcjj"] = "工程津贴"
        columns["_jssc"] = "技术输出"
        columns["_qt"] = "其他"
        columns["_gsxyj"] = "公司效益奖"
        columns["_gsxyjpay"] = "上卡效益奖"
        columns["_gsxyjtex"] = "效益奖所得税"
        columns["_nddxj"] = "年底兑现奖"
        columns["_nddxjpay"] = "年终奖实发"
        columns["_nddxjtex"] = "年终奖所得税"
        columns["_jsjj"] = "计税奖金"
        columns["_yznx"] = "预支年薪"
        columns["_zygz"] = "执业工资"

        columns["_gzpay"] = "上卡工资"
        columns["_nddxjpay1"] = "上卡年终奖"
        columns["_jjpay"] = "上卡基本奖"
        columns["_bankno1"] = "银行卡1"
        columns["_bankinfo1"] = "银行1"
        columns["_bankno2"] = "银行卡2"
        columns["_bankinfo2"] = "银行2"
        columns["_znjy"] = "子女教育"
        columns["_jxjy"] = "继续教育"
        columns["_zfdk"] = "住房贷款利息"
        columns["_zffz"] = "住房租金"
        columns["_sylr"] = "赡养老人"
        columns["_mggl"] = "马钢工龄"
        columns["_gl"] = "工龄"
        columns["_cwdf"] = "财务代发计税项"
        columns["_cwdff"] = "财务代发非计税项"
        columns["_ljyf"] = "累计应发"
        columns["_ljwx"] = "累计五险两金"
        columns["_ljqt"] = "累计其他计税"
        columns["_ljjm"] = "累计标准免税额"
        columns["_ljtex"] = "累计个税"
        columns["period"] = "发薪期间"

        return columns

    def export_sh003_excel(self):
        """
        创建excel
        """
        columndefs = self.sh003_columns()
        for depart, vs in self._sap_infos.items():
            if not self.exportable(depart):  # 如果有错误信息就跳过
                continue
            datas = vs.values()
            b = xlwt.Workbook(encoding='uft-8')
            s = b.add_sheet('Sheet1')

            # 写入标题
            for i, v in enumerate(columndefs.values()):
                s.write(0, i, v)
            for i, v in enumerate(datas):
                for j, propertyName in enumerate(columndefs.keys()):
                    try:
                        if propertyName == "one":
                            s.write(
                                i + 1, j, "马钢集团")
                        elif propertyName == "two" and getattr(v, "one", 0) != "马钢（集团）控股有限公司(总部)":
                            s.write(
                                i + 1, j, getattr(datas[i], "one", 0))
                        elif propertyName == "three" and getattr(v, "one", 0) != "马钢（集团）控股有限公司(总部)":
                            s.write(
                                i + 1, j, getattr(v, "two", 0))
                        elif propertyName == "four" and getattr(v, "one", 0) != "马钢（集团）控股有限公司(总部)":
                            s.write(
                                i + 1, j, getattr(v, "three", 0))
                        elif propertyName == "five" and getattr(v, "one", 0) != "马钢（集团）控股有限公司(总部)":
                            s.write(
                                i + 1, j, getattr(v, "four", 0))
                        else:
                            s.write(
                                i+1, j, getattr(v, propertyName, 0))
                    except TypeError:
                        print(propertyName)

            path = r'{}\{}\{}\导出文件'.format(
                self._folder_path, self._period, depart)
            if not exists(path):
                makedirs(path)
            b.save(r'{}\{}_{}_{}'.format(
                path, depart, self._period, "SAPSH003.xls"))

    def exportable(self, depart):
        if depart in self._err_msgs:  # 如果有错误信息就跳过
            return False or self._exportable
        return True
