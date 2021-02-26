#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   person_compare_export_model.py
@Time    :   2021/02/25 15:56:58
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   gz_export_model.py
@Time    :   2021/02/20 17:17:34
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''




from os.path import join, exists
from os import makedirs
from salary_support_tools.model.export.base_excel_export_model import BaseExcelExportModel, SapInfoConventor
from salary_support_tools.model.export.export_column import ExportColumn
from salary_support_tools.model.export.sh003_export_model import Sh003Export
class PersonCompareExport(BaseExcelExportModel):

    def __init__(self, period, datas):
        super().__init__(period, self.cols(),
                         datas)

    def cols(self):
        cols = []
        cols.append(ExportColumn(code="_depart_str", name="单位"))
        cols.append(ExportColumn(code="_full_departname", name="机构"))
        cols.append(ExportColumn(code="_code", name="职工编码"))
        cols.append(ExportColumn(code="_name", name="姓名"))
        cols.append(ExportColumn(code="_idno", name="身份证号"))
        cols.append(ExportColumn(code="_tel", name="电话号码"))
        cols.append(ExportColumn(code="_changeinfo", name="*变化类别"))
        return cols

    def export_by_depart(self):
        for tex_depart, datas_by_tex_depart in self._datas[0].items():
            filepath = self.get_datas_by_tex_depart_export_path(tex_depart)
            self.create_excel_file(
                self.get_datas_by_tex_depart_2(
                    tex_depart, self._datas[0]), filepath, '{}_{}_{}'.format(self._period.period, tex_depart, "人员增加表"), self._cols)

        for tex_depart, datas_by_tex_depart in self._datas[1].items():
            filepath = self.get_datas_by_tex_depart_export_path(tex_depart)
            self.create_excel_file(
                self.get_datas_by_tex_depart_2(
                    tex_depart, self._datas[1]), filepath, '{}_{}_{}'.format(self._period.period, tex_depart, "人员减少表"), self._cols)

        for tex_depart, datas_by_tex_depart in self._datas[2].items():
            for depart, datas_by_depart in datas_by_tex_depart.items():
                filepath = self.get_export_path(depart)
                self.create_excel_file(
                    self.get_datas_2(self._datas[2],
                                     tex_depart, depart), filepath, '{}_{}_{}'.format(self._period.period, depart, "人员增加表"), self._cols)

        for tex_depart, datas_by_tex_depart in self._datas[3].items():
            for depart, datas_by_depart in datas_by_tex_depart.items():
                filepath = self.get_export_path(depart)
                self.create_excel_file(
                    self.get_datas_2(self._datas[3],
                                     tex_depart, depart), filepath, '{}_{}_{}'.format(self._period.period, depart, "人员减少表"), self._cols)

    def get_datas_by_tex_depart_export_path(self, foldername):
        path = self.base_export_folder_path_prefix()
        period = self._period.period
        path = join(path, period, "人员变化相关数据")
        if foldername:
            path = join(path, foldername)
        if not exists(path):
            makedirs(path)
        return path

    def get_export_path(self, foldername):
        path = self.base_export_folder_path_prefix()
        period = self._period.period
        path = join(path, period, "人员变化相关数据")
        if foldername:
            path = join(path, foldername)
        if not exists(path):
            makedirs(path)
        return path
