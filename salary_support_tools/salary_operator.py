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


class SalaryOperator(object):

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
        # 输出工资奖金文件
        self.export_gz_jj_datas()
        # 错误信息输出
        self.err_info_write_to_depart_folder()
        # 审核表 格式输出
        self.export_auditor_excel()
        # sh002 格式输出
        self.export_sh002_excel()
        # sh003 格式输出
        self.export_sh003_excel()

        # 审核结果输出
        self.export_audited_info()

    def export_gz_jj_datas(self):
        """
        写入相应的单位文件夹
        """
        gzs, jjs = self.split_salary_data_by_depart()
        # 清理已有文件
        gz = SalaryGzInfo()
        gz_columndef = gz.getColumnDef()
        for k, v in gzs.items():
            if self.exportable(k):
                self.createExcel(self._period, k, "工资信息", v, gz_columndef)
        jj = SalaryJjInfo()
        jj_columndef = jj.getColumnDef()
        for k, v in jjs.items():
            if self.exportable(k):
                self.createExcel(self._period, k, "奖金信息", v, jj_columndef)

    def createExcel(self, period, depart_folder_name, file_name, datas, columndefs):
        """
        创建excel
        """
        b = xlwt.Workbook(encoding='uft-8')
        s = b.add_sheet('Sheet1')

        # 写入标题
        for i, v in enumerate(columndefs.values()):
            s.write(0, i, v)
        for i, v in enumerate(datas):
            for j, propertyName in enumerate(columndefs.keys()):
                try:
                    s.write(
                        i+1, j, getattr(datas[i], propertyName, 0))
                except TypeError:
                    print(propertyName)

        path = r'{}\{}\{}'.format(
            self._folder_path, self._period, depart_folder_name)
        if not exists(path):
            makedirs(path)
        b.save(r'{}\{}{}'.format(path, file_name, ".xls"))

    def split_salary_data_by_depart(self):
        """
        将载入的工资数据和奖金数据根据单位信息分类
        """
        gz_map = OrderedDict()

        # 按照文件夹名称分类
        for gz in self._gz_datas:
            gz_values = []
            k = gz.depart
            if k in gz_map:
                gz_values = gz_map[k]
            gz_values.append(gz)
            if self._need_audit_by_depart(k):
                gz_map[k] = gz_values
        jj_map = OrderedDict()

        for jj in self._jj_datas:
            jj_values = []
            k = jj.depart
            if k in jj_map:
                jj_values = jj_map[k]
            jj_values.append(jj)
            if self._need_audit_by_depart(k):
                jj_map[k] = jj_values
        return gz_map, jj_map

    def _need_audit_by_depart(self, departname):
        """
        当为空的时候不进行操作
        """
        for k, v in self._departs.items():
            if departname == v.get_depart_salaryScope_and_name():
                return v.status is not None and v.status != ''
        return False

    def err_info_write_to_depart_folder(self):
        """
        写入相应得文件夹
        """
        for i, v in self._err_msgs.items():
            path = r'{}\{}\{}\{}'.format(
                self._folder_path, self._period, i, "错误信息.txt")
            if exists(path):
                remove(path)
            if len(v) > 0:
                with open(path, 'a', encoding='utf-8') as f:
                    for i in range(len(v)):
                        msg = v[i]
                        f.write('{} {}'.format(i + 1, msg + '\n'))

    def auditor_columns(self):
        columns = OrderedDict()
        columns["period"] = "发薪期间"
        columns["salaryScope"] = "工资范围"
        columns["_code"] = "员工编号"
        columns["_name"] = "员工姓名"
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
        columns["_yzdnjt"] = "一专多能工津贴"  # 包含 计生 纪检 津贴
        columns["_ksjt"] = "矿山津贴"
        columns["_xjjt"] = "下井津贴"
        columns["_zwjt"] = "教、护龄津贴"
        columns["_hszjt"] = "护士长津贴"
        columns["_wyjt"] = "外语津贴"
        columns["_bzzjt"] = "班组长津贴"
        columns["_kjjt"] = "科技津贴"
        columns["_nsjt"] = "能手津贴"
        columns["_totaljj"] = "奖金合计"
        columns["_totaljbf"] = "加班费合计"
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
        columns["_bankno1"] = "银行卡1"
        columns["_bankinfo1"] = "银行1"
        columns["_bankno2"] = "银行卡2"
        columns["_bankinfo2"] = "银行2"
        columns["_gzpay"] = "上卡工资"
        columns["_nddxjpay1"] = "上卡年终奖"
        columns["_jjpay"] = "上卡基本奖"
        columns["_sfhd"] = "实发核对"
        columns["_ygz"] = "员工组"
        columns["_ygzz"] = "员工子组"
        columns["_err01"] = "事假旷工天数"
        columns["_err02"] = "病假天数"

        return columns

    def export_auditor_excel(self):
        """
        创建excel
        """
        columndefs = self.auditor_columns()
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
                        s.write(
                            i+1, j, getattr(v, propertyName, 0))
                    except TypeError:
                        print(propertyName)

            path = r'{}\{}\{}\导出文件'.format(
                self._folder_path, self._period, depart)
            if not exists(path):
                makedirs(path)
            b.save(r'{}\{}_{}_{}'.format(
                path, depart, self._period, "审核表数据.xls"))

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

    def create_auditorInfos(self):
        auditorInfos = dict()
        for depart, psis in self._person_salary_infos.items():
            if self.exportable(depart):  # 如果有错误信息就跳过
                continue
            a = AuditorInfo()
            a.period = self._period
            a.depart = depart
            a.numofpers = len(psis)
            for code, pis in psis.items():
                gz = pis._gz
                jj = pis._jj
                if gz is not None:
                    a.totalpayable += gz._totalPayable
                    a.pay += gz._pay
                    a.tex += 0 - gz._gts
                    a.gjj_gr += 0 - gz._gjj_bx
                    a.gjj_qy += 0 - gz._gjj_qybx
                    a.yl_gr += 0 - gz._yl_bx
                    a.yl_qy += 0 - gz._yl_qybx
                    a.sy_gr += 0 - gz._sy_bx
                    a.sy_qy += 0 - gz._sy_qybx
                    a.yil_gr += 0 - gz._yil_bx
                    a.yil_qy += 0 - gz._yil_qybx
                    a.nj_gr += 0 - gz._nj_bx
                    a.nj_qy += 0 - gz._nj_qybx
                    a.shy_qy += 0 - gz._shy_qybx
                    a.gs_qy += 0 - gz._gs_qybx
                if jj is not None:
                    a.totalpayable += jj._totalPayable
                    a.pay += jj._pay
                    a.tex += 0 - jj._gts + 0 - jj._gstz
            auditorInfos[depart] = a
        return auditorInfos

    def export_audited_info(self):
        """
        将审核结果写入txt文件
        """
        aus = self.create_auditorInfos()
        for k, vs in aus.items():
            otherStyleStr = time.strftime(
                "%Y%m%d%H%M%S", time.localtime(int(time.time())))
            path = r'{}\{}\{}\{}{}{}'.format(
                self._folder_path, self._period, k, "审核结果", otherStyleStr, ".txt")
            with open(path, 'a', encoding='utf-8') as f:
                f.write('{}'.format(vs))

    def exportable(self, depart):
        if depart in self._err_msgs:  # 如果有错误信息就跳过
            return False or self._exportable
        return True


class AuditorInfo(object):
    """
    审核结果
    """

    def __init__(self):
        self.period = ""  # 薪酬期间
        self.depart = ""  # 单位信息
        self.numofpers = 0  # 发薪人数
        self.totalpayable = 0  # 应发合计
        self.pay = 0  # 实发合计
        self.tex = 0  # 所得税合计
        self.gjj_gr = 0  # 公积金个人
        self.yl_gr = 0  # 养老保险个人
        self.sy_gr = 0  # 失业保险个人
        self.yil_gr = 0  # 医疗保险个人
        self.nj_gr = 0  # 年金个人
        self.gjj_qy = 0  # 公积金企业
        self.yl_qy = 0  # 养老保险企业
        self.sy_qy = 0  # 失业保险企业
        self.yil_qy = 0  # 医疗保险企业
        self.nj_qy = 0  # 年金企业
        self.gs_qy = 0  # 工伤保险企业
        self.shy_qy = 0  # 生育企业

    def __str__(self):
        return '审核结果:  基本信息--> 发薪期间 {} - 发薪单位 {} - 发薪人数 {} | 薪酬信息 - -> 应发合计 {:.2f} - 实发合计 {:.2f} - 代缴信息 -->  所得税 {:.2f} - 公积金个人 {:.2f} - 公积金企业 {:.2f} - 养老个人 {:.2f} - 养老企业 {:.2f} - 失业个人 {:.2f} - 失业企业 {:.2f} - 医疗个人 {:.2f} - 医疗企业 {:.2f} - 年金个人 {:.2f} - 年金企业 {:.2f} - 生育企业 {:.2f} - 工伤企业 {:.2f}'.format(self.period, self.depart, self.numofpers, self.totalpayable, self.pay, self.tex, self.gjj_gr, self.gjj_qy, self.yl_gr, self.yl_qy, self.sy_gr, self.sy_qy, self.yil_gr, self.yil_qy, self.nj_gr, self.nj_qy, self.shy_qy, self.gs_qy)
