#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test.report.py
@Time    :   2021/05/07 14:13:53
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

import pytest

from salary_support_tools.model.salary_period import SalaryPeriod
from salary_support_tools.report.report import Report, ReportColumn
from salary_support_tools.model.sap_salary_info import SapSalaryInfo
from salary_support_tools.report.report_data import JgSummaryReportData, JgSummaryReportDataGroupByDepartConventer, JgPersonDetailReportDataConventer
from salary_support_tools.engine.load_tpls_engine import LoadTplEngine


class TestReport:

    def test_init_report(self):
        report = Report()
        assert report.name == "报表名称"
        assert report.title == "标题"

        report = Report(name="报表名称测试", title="报表标题测试")
        assert report.name == "报表名称测试"
        assert report.title == "报表标题测试"

    def test_add_column(self):
        r = Report()
        r.add_column(ReportColumn(["薪酬项目", "岗位工资"], 0, "jg"))
        assert len(r.report_columns()) == 1

        with pytest.raises(TypeError):
            r.add_column("")
        assert len(r.report_columns()) == 0
        with pytest.raises(TypeError):
            r.add_columns([ReportColumn(["薪酬项目", "岗位工资"], 0, "jg"), ""])
        assert len(r.report_columns()) == 0
        r.add_columns([ReportColumn(["薪酬项目", "岗位工资"], 0, "gwgz"),
                       ReportColumn(["薪酬项目", "保留工资"], 1, "blgz")])
        assert len(r.report_columns()) == 2

    def test_parse_report(self):
        r = Report()
        r.add_column(ReportColumn(["薪酬项目", "岗位工资"], 0, "gwgz"))
        title_showable, max_clo_no, max_row_no, col_name_size = r.parse_report()
        assert title_showable
        assert max_clo_no == 1
        assert max_row_no == 2
        assert "薪酬项目" in col_name_size
        assert col_name_size["薪酬项目"] == 1
        assert "岗位工资" in col_name_size
        assert col_name_size["岗位工资"] == 1
        r.add_column(ReportColumn(["薪酬项目", "保留工资"], 1, "blgz"))
        title_showable, max_clo_no, max_row_no, col_name_size = r.parse_report()
        assert "薪酬项目" in col_name_size
        assert col_name_size["薪酬项目"] == 2
        assert col_name_size["保留工资"] == 1

    def test_create_complex_col_report(self):
        datas = [ReportData("纪委（审计稽查部、巡察办公室）1", 35, 70080,
                            9655, 36460, 17850, 430), ReportData("党委工作部（企业文化部）1", 32, 70080,
                                                                 9655, 36460, 17850, 430)]
        r = Report(period=SalaryPeriod(2021, 4), datas=datas)
        r.add_column(ReportColumn(["机构信息"], 0, "depart"))
        r.add_column(ReportColumn(["人数"], 1, "p_count"))
        r.add_column(ReportColumn(["薪酬项目", "岗位工资"], 2, "gwgz"))
        r.add_column(ReportColumn(["薪酬项目", "保留工资"], 3, "blgz"))
        r.add_column(ReportColumn(["薪酬项目", "津贴", "其它"], 4, "qt1"))
        r.add_column(ReportColumn(["薪酬项目", "津贴", "其它2"], 5, "qt2"))
        r.add_column(ReportColumn(["薪酬项目", "测试", "测试其它"], 6, "other"))
        r.export()

        r.name = "测试报表"
        r.title_showable = False
        r.export()

    def test_create_report_user_report_data(self):
        s1 = SapSalaryInfo()
        s1.depart = '01_集团机关'
        s1.two = '人力资源服务中心'
        s1._gwgz = 1680.05
        s1._totalpayable = 20000
        s1._totalpay = 10000
        r_data = JgSummaryReportData(s1)
        r = Report(period=SalaryPeriod(2021, 4), datas=[r_data])
        r.add_column(ReportColumn(["机构信息"], 0, "depart"))
        r.add_column(ReportColumn(["人数"], 1, "p_count"))
        r.add_column(ReportColumn(["薪酬项目", "岗位工资"], 2, "gwgz"))
        r.add_column(ReportColumn(["薪酬项目", "应发合计"], 3, "yfhj"))
        r.add_column(ReportColumn(["实发合计"], 4, "sfhj"))
        r.export()

    def test_create_report_current(self):
        load_engine = LoadTplEngine()
        period, _ = load_engine.load_current_period_departs()
        # 准备数据
        period, _, _, _, _, _, _, _, merge_infos = load_engine.load_tpl_by_period(
            period)
        saps = []
        tex_departs = merge_infos.keys()
        for tex_depart in tex_departs:
            audit_vals = merge_infos[tex_depart]
            for audit_depart, vals in audit_vals.items():
                for code, val in vals.items():
                    if val[1]:
                        saps.append(val[1])

        cov = JgSummaryReportDataGroupByDepartConventer(saps)
        group_infos = cov.groupby_ks()
        for audit_depart, depart_vals in group_infos.items():
            name = f"{audit_depart}-{period}-工资汇总表"
            datas = []
            for depart, vals in depart_vals.items():
                datas.extend(vals.values())
            r = Report(period=period, name=name, title=name, datas=datas)
            r.add_column(ReportColumn(["机构信息"], 0, "ks"))
            r.add_column(ReportColumn(["人数"], 1, "p_count"))
            r.add_column(ReportColumn(["薪酬项目", "岗位工资"], 2, "gwgz"))
            r.add_column(ReportColumn(["薪酬项目", "应发合计"], 3, "yfhj"))
            r.add_column(ReportColumn(["实发合计"], 4, "sfhj"))
            r.export()

    def test_create_jg_report(self):
        load_engine = LoadTplEngine()
        period, _ = load_engine.load_current_period_departs()
        # 准备数据
        period, _, _, _, _, _, _, _, merge_infos = load_engine.load_tpl_by_period(
            period)
        saps = []
        tex_departs = merge_infos.keys()
        for tex_depart in tex_departs:
            audit_vals = merge_infos[tex_depart]
            for audit_depart, vals in audit_vals.items():
                for code, val in vals.items():
                    if val[1]:
                        saps.append(val[1])

        cov = JgSummaryReportDataGroupByDepartConventer(saps)
        group_infos = cov.groupby_depart()
        for audit_depart, depart_vals in group_infos.items():
            if audit_depart == "01_集团机关" or audit_depart == "02_股份机关":
                name = f"{audit_depart}-{period}-工资汇总表"
                datas = []
                datas.extend(depart_vals.values())
                r = Report(period=period, name=name, title=name, datas=datas)
                r.add_column(ReportColumn(["机构信息"], 0, "depart"))
                r.add_column(ReportColumn(["人数"], 1, "p_count"))
                r.add_column(ReportColumn(["薪酬项目", "岗位工资"], 2, "gwgz"))
                r.add_column(ReportColumn(["薪酬项目", "保留工资"], 3, "blgz"))
                r.add_column(ReportColumn(["薪酬项目", "年功工资"], 4, "nggz"))
                r.add_column(ReportColumn(["薪酬项目", "辅助工资"], 5, "fzgz"))
                r.add_column(ReportColumn(["薪酬项目", "工资补退"], 6, "zbgz"))
                r.add_column(ReportColumn(["薪酬项目", "其他津贴"], 7, "qtjt"))
                r.add_column(ReportColumn(["薪酬项目", "预支年薪"], 8, "yznx"))
                r.add_column(ReportColumn(["薪酬项目", "职务补贴"], 9, "zwbt"))
                r.add_column(ReportColumn(["薪酬项目", "夜班津贴"], 10, "ybjt"))
                r.add_column(ReportColumn(["薪酬项目", "奖金"], 11, "jj"))
                r.add_column(ReportColumn(["薪酬项目", "加班费"], 12, "jbgz"))
                r.add_column(ReportColumn(["薪酬项目", "假期扣发"], 13, "jqkf"))
                r.add_column(ReportColumn(["薪酬项目", "其他"], 14, "qt"))
                r.add_column(ReportColumn(["薪酬项目", "高温费"], 15, "gwf"))
                r.add_column(ReportColumn(["薪酬项目", "应发合计"], 16, "yfhj"))

                r.add_column(ReportColumn(["三险两金所得税", "公积金"], 17, "gjj"))
                r.add_column(ReportColumn(["三险两金所得税", "养老保险"], 18, "yangl"))
                r.add_column(ReportColumn(["三险两金所得税", "医疗保险"], 19, "yil"))
                r.add_column(ReportColumn(["三险两金所得税", "失业保险"], 20, "sy"))
                r.add_column(ReportColumn(["三险两金所得税", "年金"], 21, "nj"))
                r.add_column(ReportColumn(["三险两金所得税", "所得税"], 22, "sds"))

                r.add_column(ReportColumn(["其他代发代扣", "独补"], 23, "db"))
                r.add_column(ReportColumn(["其他代发代扣", "驻外补贴"], 24, "zwjt"))
                r.add_column(ReportColumn(
                    ["其他代发代扣", "财务补退(经常性)"], 25, "cwbtjcx"))
                r.add_column(ReportColumn(
                    ["其他代发代扣", "其他财务补退"], 26, "cwbtqt"))
                r.add_column(ReportColumn(
                    ["其他代发代扣", "司法扣款"], 27, "sfkk"))

                r.add_column(ReportColumn(["实发合计"], 28, "sfhj"))
                r.export()

    def test_create_jg_person_report(self):
        load_engine = LoadTplEngine()
        period, _ = load_engine.load_current_period_departs()
        # 准备数据
        period, _, _, _, _, _, _, _, merge_infos = load_engine.load_tpl_by_period(
            period)
        saps = []
        tex_departs = merge_infos.keys()
        for tex_depart in tex_departs:
            audit_vals = merge_infos[tex_depart]
            for audit_depart, vals in audit_vals.items():
                for code, val in vals.items():
                    if val[1]:
                        saps.append(val[1])

        cov = JgPersonDetailReportDataConventer(saps)
        group_infos = cov.groupby_person()
        for audit_depart, depart_vals in group_infos.items():
            if audit_depart == "01_集团机关" or audit_depart == "02_股份机关":
                for depart, vals in depart_vals.items():
                    for ks, vs in vals.items():
                        name = f"{audit_depart}-{depart}-{ks}-{period}-工资明细表"
                        datas = vs
                        r = Report(period=period, name=name,
                                   title=name, datas=datas)
                        r.add_column(ReportColumn(["机构信息"], 0, "depart_info"))
                        r.add_column(ReportColumn(["职工编码"], 1, "code"))
                        r.add_column(ReportColumn(["新明"], 2, "name"))
                        r.add_column(ReportColumn(["薪酬项目", "岗位工资"], 3, "gwgz"))
                        r.add_column(ReportColumn(["薪酬项目", "保留工资"], 4, "blgz"))
                        r.add_column(ReportColumn(["薪酬项目", "年功工资"], 5, "nggz"))
                        r.add_column(ReportColumn(["薪酬项目", "辅助工资"], 6, "fzgz"))
                        r.add_column(ReportColumn(["薪酬项目", "工资补退"], 7, "zbgz"))
                        r.add_column(ReportColumn(["薪酬项目", "其他津贴"], 8, "qtjt"))
                        r.add_column(ReportColumn(["薪酬项目", "预支年薪"], 9, "yznx"))
                        r.add_column(ReportColumn(
                            ["薪酬项目", "职务补贴"], 10, "zwbt"))
                        r.add_column(ReportColumn(
                            ["薪酬项目", "夜班津贴"], 11, "ybjt"))
                        r.add_column(ReportColumn(["薪酬项目", "奖金"], 12, "jj"))
                        r.add_column(ReportColumn(["薪酬项目", "加班费"], 13, "jbgz"))
                        r.add_column(ReportColumn(
                            ["薪酬项目", "假期扣发"], 14, "jqkf"))
                        r.add_column(ReportColumn(["薪酬项目", "其他"], 15, "qt"))
                        r.add_column(ReportColumn(["薪酬项目", "高温费"], 16, "gwf"))
                        r.add_column(ReportColumn(
                            ["薪酬项目", "应发合计"], 17, "yfhj"))

                        r.add_column(ReportColumn(
                            ["三险两金所得税", "公积金"], 18, "gjj"))
                        r.add_column(ReportColumn(
                            ["三险两金所得税", "养老保险"], 19, "yangl"))
                        r.add_column(ReportColumn(
                            ["三险两金所得税", "医疗保险"], 20, "yil"))
                        r.add_column(ReportColumn(
                            ["三险两金所得税", "失业保险"], 21, "sy"))
                        r.add_column(ReportColumn(["三险两金所得税", "年金"], 22, "nj"))
                        r.add_column(ReportColumn(
                            ["三险两金所得税", "所得税"], 23, "sds"))

                        r.add_column(ReportColumn(["其他代发代扣", "独补"], 24, "db"))
                        r.add_column(ReportColumn(
                            ["其他代发代扣", "驻外补贴"], 25, "zwjt"))
                        r.add_column(ReportColumn(
                            ["其他代发代扣", "财务补退(经常性)"], 26, "cwbtjcx"))
                        r.add_column(ReportColumn(
                            ["其他代发代扣", "其他财务补退"], 27, "cwbtqt"))
                        r.add_column(ReportColumn(
                            ["其他代发代扣", "司法扣款"], 28, "sfkk"))

                        r.add_column(ReportColumn(["实发合计"], 29, "sfhj"))
                        r.export([audit_depart, depart, ks])

    def test_create_ks_summary_report(self):
        load_engine = LoadTplEngine()
        period, _ = load_engine.load_current_period_departs()
        # 准备数据
        period, _, _, _, _, _, _, _, merge_infos = load_engine.load_tpl_by_period(
            period)
        saps = []
        tex_departs = merge_infos.keys()
        for tex_depart in tex_departs:
            audit_vals = merge_infos[tex_depart]
            for audit_depart, vals in audit_vals.items():
                for code, val in vals.items():
                    if val[1]:
                        saps.append(val[1])

        cov = JgSummaryReportDataGroupByDepartConventer(saps)
        group_infos = cov.groupby_ks()
        for audit_depart, depart_vals in group_infos.items():
            # if audit_depart == "01_集团机关" or audit_depart == "02_股份机关":
            for depart, vals in depart_vals.items():
                name = f"{audit_depart}-{depart}-{period}-工资汇总表"
                datas = []
                datas.extend(vals.values())
                r = Report(period=period, name=name, title=name, datas=datas)
                r.add_column(ReportColumn(["机构信息"], 0, "depart_info"))
                r.add_column(ReportColumn(["人数"], 1, "p_count"))
                r.add_column(ReportColumn(["薪酬项目", "岗位工资"], 2, "gwgz"))
                r.add_column(ReportColumn(["薪酬项目", "保留工资"], 3, "blgz"))
                r.add_column(ReportColumn(["薪酬项目", "年功工资"], 4, "nggz"))
                r.add_column(ReportColumn(["薪酬项目", "辅助工资"], 5, "fzgz"))
                r.add_column(ReportColumn(["薪酬项目", "工资补退"], 6, "zbgz"))
                r.add_column(ReportColumn(["薪酬项目", "其他津贴"], 7, "qtjt"))
                r.add_column(ReportColumn(["薪酬项目", "预支年薪"], 8, "yznx"))
                r.add_column(ReportColumn(["薪酬项目", "职务补贴"], 9, "zwbt"))
                r.add_column(ReportColumn(["薪酬项目", "夜班津贴"], 10, "ybjt"))
                r.add_column(ReportColumn(["薪酬项目", "奖金"], 11, "jj"))
                r.add_column(ReportColumn(["薪酬项目", "加班费"], 12, "jbgz"))
                r.add_column(ReportColumn(["薪酬项目", "假期扣发"], 13, "jqkf"))
                r.add_column(ReportColumn(["薪酬项目", "其他"], 14, "qt"))
                r.add_column(ReportColumn(["薪酬项目", "高温费"], 15, "gwf"))
                r.add_column(ReportColumn(["薪酬项目", "应发合计"], 16, "yfhj"))

                r.add_column(ReportColumn(["三险两金所得税", "公积金"], 17, "gjj"))
                r.add_column(ReportColumn(["三险两金所得税", "养老保险"], 18, "yangl"))
                r.add_column(ReportColumn(["三险两金所得税", "医疗保险"], 19, "yil"))
                r.add_column(ReportColumn(["三险两金所得税", "失业保险"], 20, "sy"))
                r.add_column(ReportColumn(["三险两金所得税", "年金"], 21, "nj"))
                r.add_column(ReportColumn(["三险两金所得税", "所得税"], 22, "sds"))

                r.add_column(ReportColumn(["其他代发代扣", "独补"], 23, "db"))
                r.add_column(ReportColumn(["其他代发代扣", "驻外补贴"], 24, "zwjt"))
                r.add_column(ReportColumn(
                    ["其他代发代扣", "财务补退(经常性)"], 25, "cwbtjcx"))
                r.add_column(ReportColumn(
                    ["其他代发代扣", "其他财务补退"], 26, "cwbtqt"))
                r.add_column(ReportColumn(
                    ["其他代发代扣", "司法扣款"], 27, "sfkk"))

                r.add_column(ReportColumn(["实发合计"], 28, "sfhj"))
                r.export([audit_depart, depart])


class ReportData:

    def __init__(self, depart, p_count, gwgz, blgz, qt1, qt2, other):
        self.depart = depart
        self.p_count = p_count
        self.gwgz = gwgz
        self.blgz = blgz
        self.qt1 = qt1
        self.qt2 = qt2
        self.other = other
