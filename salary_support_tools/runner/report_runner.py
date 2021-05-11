#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   report_runner.py
@Time    :   2021/05/11 18:40:03
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from salary_support_tools.engine.load_tpls_engine import LoadTplEngine
from salary_support_tools.report.report import Report, ReportColumn
from salary_support_tools.report.report_data import JgSummaryReportDataGroupByDepartConventer, JgPersonDetailReportDataConventer


class ReportRunner:

    def run(self):
        load_engine = LoadTplEngine()
        period, _ = load_engine.load_current_period_departs()
        # 准备数据
        period, _, _, _, _, _, _, _, merge_infos = load_engine.load_tpl_by_period(
            period)

        saps = []
        tex_departs = merge_infos.keys()
        for tex_depart in tex_departs:
            audit_vals = merge_infos[tex_depart]
            for vals in audit_vals.values():
                for val in vals.values():
                    if val[1]:
                        saps.append(val[1])

        self.do_summary_report_export(period, saps)
        self.do_detail_report_export(period, saps)
        self.do_jg_summary_report_export(period, saps)

    def do_summary_report_export(self, period, saps):
        cov = JgSummaryReportDataGroupByDepartConventer(saps)
        group_infos = cov.groupby_ks()
        for audit_depart, depart_vals in group_infos.items():
            for depart, vals in depart_vals.items():
                name = f"{audit_depart}-{depart}-{period}-工资汇总表"
                datas = []
                datas.extend(vals.values())
                r = Report(period=period, name=name,
                           title=name, datas=datas)
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

    def do_detail_report_export(self, period, saps):
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

    def do_jg_summary_report_export(self, period, saps):
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
                r.export([audit_depart])
