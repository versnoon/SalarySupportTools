#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   gz_export_model.py
@Time    :   2021/02/20 17:17:34
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from salary_support_tools.model.export.base_excel_export_model import BaseExcelExportModel
from salary_support_tools.model.export.export_column import ExportColumn
from salary_support_tools.model.salary_gz import SalaryGz


class GzExport(BaseExcelExportModel):

    def __init__(self, period, datas):
        super().__init__(period, SalaryGz.cols(), datas)

    def cols(self):
        cols = []
        cols.append(ExportColumn(code="_code", name="员工通行证"))
        cols.append(ExportColumn(code="_name", name="员工姓名"))
        cols.append(ExportColumn(code="_depart_fullname", name="机构"))
        cols.append(ExportColumn(code="_departLevelTow", name="二级机构"))
        cols.append(ExportColumn(code="_branchLevelThree", name="三级机构"))
        cols.append(ExportColumn(code="_salaryModel", name="薪酬模式"))
        cols.append(ExportColumn(code="_jobName", name="岗位名称"))
        cols.append(ExportColumn(code="_postPrice", name="岗位价值"))
        cols.append(ExportColumn(code="_distributionMark", name="是否代发工资"))
        cols.append(ExportColumn(code="_fzZxkc", name="累计住房租金支出"))
        cols.append(ExportColumn(code="_fdZxkc", name="累计住房贷款利息支出"))
        cols.append(ExportColumn(code="_jxjyZxkc", name="累计继续教育支出"))
        cols.append(ExportColumn(code="_znjyZxkc", name="累计子女教育支出"))
        cols.append(ExportColumn(code="_sylrZxkc", name="累计赡养老人支出"))
        cols.append(ExportColumn(code="_zxnf", name="执行年份"))
        cols.append(ExportColumn(code="_gsgl", name="公司工龄"))
        cols.append(ExportColumn(code="_lxgl", name="连续工龄"))
        cols.append(ExportColumn(code="_bjbl", name="病假扣款比例"))
        cols.append(ExportColumn(code="_gwxs", name="岗位系数"))
        cols.append(ExportColumn(code="_gwxbz", name="岗位薪标准"))
        cols.append(ExportColumn(code="_gwgz", name="岗位工资"))
        cols.append(ExportColumn(code="_blgz", name="保留工资"))
        cols.append(ExportColumn(code="_glgz", name="工龄工资"))
        cols.append(ExportColumn(code="_jbx", name="基本薪"))
        cols.append(ExportColumn(code="_qtblgz", name="其他保留工资"))
        cols.append(ExportColumn(code="_gdgz", name="固定工资"))
        cols.append(ExportColumn(code="_dtxgz", name="待退休工资"))
        cols.append(ExportColumn(code="_gwx", name="岗位薪"))
        cols.append(ExportColumn(code="_zlx", name="资历薪"))
        cols.append(ExportColumn(code="_yfjxnx", name="预发绩效年薪"))
        cols.append(ExportColumn(code="_shf", name="生活费"))
        cols.append(ExportColumn(code="_jbgzdy", name="基本工资单元"))
        cols.append(ExportColumn(code="_rpjgzkk", name="日平均工资(扣款)"))
        cols.append(ExportColumn(code="_rpjgzjk", name="日平均工资2(加款)"))
        cols.append(ExportColumn(code="_zyb_jt", name="中夜班津贴"))
        cols.append(ExportColumn(code="_jn_jt", name="技能津贴"))
        cols.append(ExportColumn(code="_jggz_jt", name="兼岗工资"))
        cols.append(ExportColumn(code="_gzz_jt", name="班组长津贴"))
        cols.append(ExportColumn(code="_kjyx_jt", name="科技优秀津贴"))
        cols.append(ExportColumn(code="_czns_jt", name="操作能手津贴"))
        cols.append(ExportColumn(code="_xl_jt", name="学历津贴"))
        cols.append(ExportColumn(code="_tx_jt", name="通讯补贴"))
        cols.append(ExportColumn(code="_cq_jt", name="出勤津贴"))
        cols.append(ExportColumn(code="_gw_jt", name="高温津贴"))
        cols.append(ExportColumn(code="_mz_jt", name="民族津贴"))
        cols.append(ExportColumn(code="_wc_jt", name="误餐补助"))
        cols.append(ExportColumn(code="_gs_jt", name="工伤津贴"))
        cols.append(ExportColumn(code="_gshl_jt", name="工伤护理费"))
        cols.append(ExportColumn(code="_js_jt", name="技术津贴"))
        cols.append(ExportColumn(code="_tsgx_jt", name="特殊贡献津贴"))
        cols.append(ExportColumn(code="_zw_jt", name="驻外津贴"))  # 驻外津贴
        # cols.appenExportColumn(d(code="_hsz_jt",name = "护士长津贴"
        cols.append(ExportColumn(code="_gongw_jt", name="公务车贴"))
        cols.append(ExportColumn(code="_gexbt_jt", name="各项补贴"))
        cols.append(ExportColumn(code="_sdqnwy_jt", name="水电气暖物业补贴"))
        cols.append(ExportColumn(code="_shbt_jt", name="生活补贴"))
        cols.append(ExportColumn(code="_shfbc_jt", name="生活费补差"))
        cols.append(ExportColumn(code="_gxbt_jt", name="岗薪补贴"))
        cols.append(ExportColumn(code="_total_jt", name="津贴合计"))
        cols.append(ExportColumn(code="_rpjgz", name="日平均工资3(津贴)"))
        cols.append(ExportColumn(code="_qtnssr", name="其它纳税收入"))
        cols.append(ExportColumn(code="_ygdxz", name="月固定薪资"))
        cols.append(ExportColumn(code="_jxgz", name="绩效工资"))
        cols.append(ExportColumn(code="_jdfdyyz", name="季度浮动月预支"))
        cols.append(ExportColumn(code="_khfd", name="考核浮动"))
        cols.append(ExportColumn(code="_shfbt", name="生活费补贴"))
        cols.append(ExportColumn(code="_dsznf", name="独生子女费"))
        cols.append(ExportColumn(code="_jkdjf", name="兼课带教费"))
        cols.append(ExportColumn(code="_qtdf", name="其他代发"))
        cols.append(ExportColumn(code="_gztz", name="工资调整"))
        cols.append(ExportColumn(code="_qtbf", name="其它补发"))
        cols.append(ExportColumn(code="_qtkk", name="其它扣款"))
        cols.append(ExportColumn(code="_qtdkk", name="其他代扣款"))
        cols.append(ExportColumn(code="_fd_jbgz", name="法定假日加班工资"))
        cols.append(ExportColumn(code="_xxr_jbgz", name="休息日加班工资"))
        cols.append(ExportColumn(code="_ps_jbgz", name="平常加班工资"))
        cols.append(ExportColumn(code="_total_jbgz", name="加班工资单元"))
        cols.append(ExportColumn(code="_bjkk_kk", name="病假扣款"))
        cols.append(ExportColumn(code="_sjkk_kk", name="事假扣款"))
        cols.append(ExportColumn(code="_kgkk_kk", name="旷工扣款"))
        cols.append(ExportColumn(code="_total_kk", name="缺勤扣款单元"))
        cols.append(ExportColumn(code="_yl_bx", name="养老保险个人额度"))
        cols.append(ExportColumn(code="_sy_bx", name="失业保险个人额度"))
        cols.append(ExportColumn(code="_yil_bx", name="医疗保险个人额度"))
        cols.append(ExportColumn(code="_gjj_bx", name="公积金个人额度"))
        cols.append(ExportColumn(code="_nj_bx", name="企业年金个人额度"))
        cols.append(ExportColumn(code="_gjjbz_bx", name="公积金补助"))
        cols.append(ExportColumn(code="_totalPayable", name="应发"))
        cols.append(ExportColumn(code="_yse", name="应税额"))
        cols.append(ExportColumn(code="_gts", name="个调税"))
        cols.append(ExportColumn(code="_dfxm", name="代发项目"))
        cols.append(ExportColumn(code="_bfone", name="补发一"))
        cols.append(ExportColumn(code="_bftwo", name="补发二"))
        cols.append(ExportColumn(code="_total_dk", name="代扣合计"))
        cols.append(ExportColumn(code="_pay", name="实发"))
        cols.append(ExportColumn(code="_yl_qybx", name="养老保险企业额度"))
        cols.append(ExportColumn(code="_sy_qybx", name="失业保险企业额度"))
        cols.append(ExportColumn(code="_yil_qybx", name="医疗保险企业额度"))
        cols.append(ExportColumn(code="_shy_qybx", name="生育保险企业额度"))
        cols.append(ExportColumn(code="_gs_qybx", name="工伤保险企业额度"))
        cols.append(ExportColumn(code="_gjj_qybx", name="公积金企业额度"))
        cols.append(ExportColumn(code="_nj_qybx", name="企业年金企业额度"))
        return cols

    def export(self):
        for tex_depart, datas_by_tex_depart in self._datas.items():
            for depart, datas_by_depart in datas_by_tex_depart.items():
                filepath = self.get_test_export_path(depart)
                self.create_excel_file(
                    self.get_datas(tex_depart, depart), filepath, "工资信息", self.cols())
