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


from salary_support_tools.report.report import Report, ReportColumn


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
        r = Report(datas=datas)
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


class ReportData:

    def __init__(self, depart, p_count, gwgz, blgz, qt1, qt2, other):
        self.depart = depart
        self.p_count = p_count
        self.gwgz = gwgz
        self.blgz = blgz
        self.qt1 = qt1
        self.qt2 = qt2
        self.other = other
