#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   report_excel_export.py
@Time    :   2021/03/18 13:07:02
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


import xlwt


class ReportExcelExport:
    """
    报表导出，用于各类汇总表和明细表导出
    """

    EXT = '.xls'

    MAX_COL_NO = 27

    def __init__(self, title, sapinfos):
        self.title = title
        self.datas = sapinfos

    def filename(self):
        return self.title

    def report_title(self, sheet):
        """
        标题单元格定义
        """
        title_def = CellDef(self.title, 0, 0, 0, self.MAX_COL_NO)
        self.write_cell(sheet, self.head_styles(), title_def)

    def write_cell(self, sheet, styles, *cells):
        for cell in cells:
            row_start_no = cell.row_start_no
            col_start_no = cell.col_start_no
            if not styles:
                styles = self.default_styles()

            # 单元格其实坐标为-1 时报错
            if row_start_no == -1 or col_start_no == -1:
                raise ValueError(
                    f'cell Coordinates err: row_no{row_start_no},col_no{col_start_no}')
            if cell.col_offset == 0 and cell.row_offset == 0:
                sheet.write(row_start_no, col_start_no,
                            cell.get_contant(), styles)
            else:
                sheet.write_merge(row_start_no, row_start_no+cell.row_offset,
                                  col_start_no, col_start_no+cell.col_offset, cell.get_contant(), styles)

    def sheetname(self):
        """
        报表工作部名
        """
        return "Sheet1"

    def dw_cols(self):
        return ["机构名称", "人数"]

    def gz_cols(self):
        """
        工资列名
        """
        return ["岗位工资", "保留工资", "年功工资", "辅助工资", "工资补退", "其它津贴", "职务补贴", "夜班津贴", "奖金", "预支年薪", "加班工资", "考勤扣发", "其它", "应发合计"]

    def df_cols(self):
        """
        代发列名
        """
        return ["财务补退", "独生子女费", "教育经费", "驻外补贴", "其它扣款"]

    def dj_cols(self):
        """
        代缴列名
        """
        return ["公积金", "养老", "医疗", "失业", "年金", "所得税"]

    def sf_cols(self):
        """
        实发列名
        """
        return ["实发合计"]

    def default_styles(self):
        return xlwt.XFStyle()

    def head_styles(self):
        style = xlwt.XFStyle()  # 创建一个样式对象，初始化样式
        al = xlwt.Alignment()
        al.horz = 0x02      # 设置水平居中
        al.vert = 0x01      # 设置垂直居中
        style.alignment = al
        fnt = xlwt.Font()
        fnt.name = u'微软雅黑'  # 设置其字体为微软雅黑
        fnt.colour_index = 0  # 设置其字体颜色黑色
        fnt.bold = True  # 加粗
        fnt.height = 20*18  # 字体大小
        style.font = fnt
        return style

    def min_height_styles(self):
        return xlwt.easyxf(r'font:height {};'.format(20*3))

    def title_styles(self):
        style = xlwt.XFStyle()  # 创建一个样式对象，初始化样式
        al = xlwt.Alignment()
        al.horz = 0x02      # 设置水平居中
        al.vert = 0x01      # 设置垂直居中
        al.wrap = 1  # 自动换行
        style.alignment = al
        fnt = xlwt.Font()
        fnt.name = u'Arial'  # 设置其字体为微软雅黑
        fnt.colour_index = 0  # 设置其字体颜色黑色
        fnt.bold = True  # 加粗
        fnt.height = 20*10  # 字体大小
        style.font = fnt
        borders = xlwt.Borders()
        borders.left = 1
        borders.top = 1
        borders.right = 1
        borders.bottom = 1
        style.borders = borders
        return style

    def create_report_create_info(self, sheet):
        # 编报定义
        bb = CellDef("编报:人力资源服务中心薪酬发放室", 2, 0)
        # 日期
        rq = CellDef("发放日期:2021年03月16日", 2, self.MAX_COL_NO - 1)

        self.write_cell(sheet, None, bb, rq)
        # 空行
        self.blank_row(3, sheet)

    def blank_row(self, row_no, sheet):
        sheet.row(row_no).set_style(self.min_height_styles())

    def create_columns(self, sheet):

        # 机构
        dw_def = CellDef("机构名称", 4, 0, 1)

        # 人数
        rs_def = CellDef("人数", 4, 1, 1)

        # 薪酬项目分组
        xc_group_def = CellDef("薪酬", 4, 2, 0, 1)

        # 岗位工资
        gw_def = CellDef("岗位工资", 5, 2)
        # 保留工资
        bl_def = CellDef("保留工资", 5, 3)

        # 年功工资
        ng_def = CellDef("年功工资", 5, 4)

        self.write_cell(sheet, self.title_styles(), dw_def,
                        rs_def, xc_group_def, gw_def, bl_def, ng_def)
        # columns_row_index = 5
        # # # 写入单位标题
        # for i, v in enumerate(self.dw_cols()):
        #     sheet.write_merge(columns_row_index-1,
        #                       columns_row_index, i, i, v, self.title_styles())
        # # # 写入工资标题
        # for i, v in enumerate(self.gz_cols()):
        #     sheet.write(columns_row_index, i+len(self.dw_cols()),
        #                 v, self.title_styles())
        # # 写入代发标题
        # for i, v in enumerate(self.df_cols()):
        #     sheet.write(columns_row_index, i+len(self.dw_cols())+len(self.gz_cols()),
        #                 v, self.title_styles())
        # # 写入代扣标题
        # for i, v in enumerate(self.dj_cols()):
        #     sheet.write(columns_row_index, i + len(self.dw_cols()) +
        #                 len(self.gz_cols()) + len(self.df_cols()), v, self.title_styles())
        # # 写入实发标题
        # for i, v in enumerate(self.sf_cols()):
        #     sheet.write_merge(columns_row_index-1, columns_row_index, i + len(self.dw_cols()) + len(self.gz_cols()) +
        #                       len(self.df_cols()) + len(self.dj_cols()), i + len(self.dw_cols()) + len(self.gz_cols()) +
        #                       len(self.df_cols()) + len(self.dj_cols()), v, self.title_styles())
        # self.set_width(sheet,
        #                self.gz_cols()+self.df_cols()+self.dj_cols()+self.sf_cols())

    def set_width(self, sheet, columns):
        for i in range(len(columns)):
            col = sheet.col(i)
            width = 180 * 20
            if i == 0:
                width = 640 * 20
            col.width = width

    def create_datas(self, sheet):
        """
        创建数据信息
        """
        pass

    def grouyby_depart(self):
        """
        根据单位分组统计
        """

    def create_report_excel_file(self):
        """
        创建excel
        """
        b = xlwt.Workbook(encoding='uft-8')
        s = b.add_sheet(self.sheetname())

        # 标题行
        self.report_title(s)

        # 报表创建信息行
        self.create_report_create_info(s)

        # 列名
        self.create_columns(s)

        # 数据
        self.create_datas(s)

        b.save(r'{}{}'.format(self.filename(), self.EXT))


class CellDef:
    """
    单元格定义
    """

    def __init__(self, contant=None, row_start_no=-1, col_start_no=-1, row_offset=0, col_offset=0):
        # 显示得内容
        self.contant = contant
        self.row_start_no = row_start_no
        self.row_offset = row_offset
        self.col_start_no = col_start_no
        self.col_offset = col_offset
        # 内容格式 默认为 字符型 S
        self.contant_type = "S"

    def get_contant(self):
        """
        根据内容格式获取标准化输出
        """
        if self.contant:
            if self.contant_type == "S" and isinstance(self.contant, str):
                return self.get_str_val()
            elif self.contant_type == "I" and isinstance(self.contant, int):
                return self.get_int_val()
            elif self.contant_type == "F" and isinstance(self.contant, float):
                return self.get_float_val()
            else:
                return self.get_default_val()
        else:
            return ""

    def get_str_val(self):
        """
        获取字符串显示
        """
        return self.contant.strip()

    def get_int_val(self):
        return self.get_default_val()

    def get_float_val(self):
        """
        默认保留两位
        """
        return round(self.contant, 2)

    def get_default_val(self):
        return self.contant
