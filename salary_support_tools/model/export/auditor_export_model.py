#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   gz_export_model.py
@Time    :   2021/02/20 17:17:34
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from salary_support_tools.model.export.base_excel_export_model import BaseExcelExportModel, SapInfoConventor
from salary_support_tools.model.export.export_column import ExportColumn
from salary_support_tools.model.person_salary_cov import PersonSalaryConventor


class AuditorExport(BaseExcelExportModel):

    def __init__(self, period, datas):
        super().__init__(period, self.cols(), datas, convertor=SapInfoConventor())

    def cols(self):
        cols = []
        cols.append(ExportColumn(code="period", name="发薪期间"))
        cols.append(ExportColumn(code="salaryScope", name="工资范围"))
        cols.append(ExportColumn(code="_code", name="员工编号"))
        cols.append(ExportColumn(code="_name", name="员工姓名"))
        cols.append(ExportColumn(code="_gwgz", name="岗位工资"))
        cols.append(ExportColumn(code="_blgz", name="保留工资"))
        cols.append(ExportColumn(code="_nggz", name="年功工资"))
        cols.append(ExportColumn(code="_fzgz", name="辅助工资"))
        cols.append(ExportColumn(code="_shbz", name="生活补助"))
        cols.append(ExportColumn(code="_khgz", name="考核工资"))
        cols.append(ExportColumn(code="_gzbt", name="工资补退"))
        cols.append(ExportColumn(code="_qtgz", name="其他工资"))
        cols.append(ExportColumn(code="_ntjbgz", name="内退基本工资"))
        cols.append(ExportColumn(code="_ntzz", name="内退增资"))
        cols.append(ExportColumn(code="_ntglgz", name="内退工龄工资"))
        cols.append(ExportColumn(code="_djsj", name="代缴三金"))
        cols.append(ExportColumn(code="_wjbt", name="物价补贴"))
        cols.append(ExportColumn(code="_ybjt", name="夜班津贴"))
        cols.append(ExportColumn(code="_jsjt", name="技师津贴"))
        cols.append(ExportColumn(code="_yzdnjt",
                                 name="一专多能工津贴"))  # 包含 计生 纪检 津贴
        cols.append(ExportColumn(code="_ksjt", name="矿山津贴"))
        cols.append(ExportColumn(code="_xjjt", name="下井津贴"))
        cols.append(ExportColumn(code="_zwjt", name="教、护龄津贴"))
        cols.append(ExportColumn(code="_hszjt", name="护士长津贴"))
        cols.append(ExportColumn(code="_wyjt", name="外语津贴"))
        cols.append(ExportColumn(code="_bzzjt", name="班组长津贴"))
        cols.append(ExportColumn(code="_kjjt", name="科技津贴"))
        cols.append(ExportColumn(code="_nsjt", name="能手津贴"))
        cols.append(ExportColumn(code="_totaljj", name="奖金合计"))
        cols.append(ExportColumn(code="_totaljbf", name="加班费合计"))
        cols.append(ExportColumn(code="_totalqq", name="缺勤扣款合计"))
        cols.append(ExportColumn(code="_gjj", name="公积金"))
        cols.append(ExportColumn(code="_yl", name="养老保险"))
        cols.append(ExportColumn(code="_yil", name="医疗保险缴"))
        cols.append(ExportColumn(code="_sy", name="失业保险"))
        cols.append(ExportColumn(code="_yl_bj", name="养老保险补缴"))
        cols.append(ExportColumn(code="_yil_bj", name="医疗保险补缴"))
        cols.append(ExportColumn(code="_sy_bj", name="失业保险补缴"))
        cols.append(ExportColumn(code="_nj", name="年金"))
        cols.append(ExportColumn(code="_totalsdj", name="工资税收"))
        cols.append(ExportColumn(code="_sljj", name="水利基金"))
        cols.append(ExportColumn(code="_cwkk", name="财务扣款"))
        cols.append(ExportColumn(code="_df", name="电费"))
        cols.append(ExportColumn(code="_fz", name="房租"))
        cols.append(ExportColumn(code="_dsf", name="收视费"))
        cols.append(ExportColumn(code="_qjf", name="清洁费"))
        cols.append(ExportColumn(code="_ccf", name="乘车费用"))
        cols.append(ExportColumn(code="_cwbt", name="财务补退"))
        cols.append(ExportColumn(code="_wybt", name="物业补贴"))
        cols.append(ExportColumn(code="_bjf", name="保健费"))
        cols.append(ExportColumn(code="_db", name="独补"))
        cols.append(ExportColumn(code="_txf", name="通讯费"))
        cols.append(ExportColumn(code="_gwf", name="防暑降温"))
        cols.append(ExportColumn(code="_hm", name="回民"))
        cols.append(ExportColumn(code="_jj", name="纪检津贴"))
        cols.append(ExportColumn(code="_js", name="计生津贴"))
        cols.append(ExportColumn(code="_wc", name="误餐补贴"))
        cols.append(ExportColumn(code="_ksryj", name="矿山荣誉金"))
        cols.append(ExportColumn(code="_xf", name="信访津贴"))
        cols.append(ExportColumn(code="_scjt", name="伤残津贴"))
        cols.append(ExportColumn(code="_zwbt", name="职务补贴"))
        cols.append(ExportColumn(code="_kyxm", name="科研项目津贴"))
        cols.append(ExportColumn(code="_jsgg", name="技术攻关津贴"))
        cols.append(ExportColumn(code="_fgzjtbf", name="非工资性津贴补发"))

        cols.append(ExportColumn(code="_totalpayable", name="工资应发"))
        cols.append(ExportColumn(code="_totalpay", name="实发工资"))
        cols.append(ExportColumn(code="_jyjf", name="教育经费"))
        cols.append(ExportColumn(code="_gcjj", name="工程津贴"))
        cols.append(ExportColumn(code="_jssc", name="技术输出"))
        cols.append(ExportColumn(code="_qt", name="其他"))
        cols.append(ExportColumn(code="_gsxyj", name="公司效益奖"))
        cols.append(ExportColumn(code="_gsxyjpay", name="上卡效益奖"))
        cols.append(ExportColumn(code="_gsxyjtex", name="效益奖所得税"))
        cols.append(ExportColumn(code="_nddxj", name="年底兑现奖"))
        cols.append(ExportColumn(code="_nddxjpay", name="年终奖实发"))
        cols.append(ExportColumn(code="_nddxjtex", name="年终奖所得税"))
        cols.append(ExportColumn(code="_jsjj", name="计税奖金"))
        cols.append(ExportColumn(code="_yznx", name="预支年薪"))
        cols.append(ExportColumn(code="_zygz", name="执业工资"))
        cols.append(ExportColumn(code="_bankno1", name="银行卡1"))
        cols.append(ExportColumn(code="_bankinfo1", name="银行1"))
        cols.append(ExportColumn(code="_bankno2", name="银行卡2"))
        cols.append(ExportColumn(code="_bankinfo2", name="银行2"))
        cols.append(ExportColumn(code="_gzpay", name="上卡工资"))
        cols.append(ExportColumn(code="_nddxjpay1", name="上卡年终奖"))
        cols.append(ExportColumn(code="_jjpay", name="上卡基本奖"))
        cols.append(ExportColumn(code="_sfhd", name="实发核对"))
        cols.append(ExportColumn(code="_ygz", name="员工组"))
        cols.append(ExportColumn(code="_ygzz", name="员工子组"))
        cols.append(ExportColumn(code="_err01", name="事假旷工天数"))
        cols.append(ExportColumn(code="_err02", name="病假天数"))
        return cols

    def get_filename(self):
        return "审核表数据"
