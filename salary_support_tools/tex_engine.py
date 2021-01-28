#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tex_engine.py
@Time    :   2021/01/28 14:29:05
@Author  :   Tong tan 
@Version :   1.0
@Contact :   tongtan@gmail.com
'''

from salary_support_tools.ehr_engine import ExlToClazz


class TexEngine(object):
    """
    所得税核对及拆分
    """

    def __init__(self, period, persons):
        self._name = "tex"
        self._period = period
        self._folder_path = r'd:\薪酬审核文件夹'

    def get_tpl_path(self):
        return r'{}\{}'.format(self._folder_path, "202101_税款计算_工资薪金所得.xls")

    def start(self):
        pass

    def load_data(self):

        tex = TexSysStruct()
        tex_load = ExlToClazz(TexSysStruct, tex.getColumnDef(),
                              self.get_tpl_path())
        datas = tex_load.loadTemp()


class TexSysStruct(object):
    """
    税务系统信息对象
    """

    def __init__(self):
        self._code = ""  # 工号
        self._name = ""  # 姓名
        self._idtype = "居民身份证"  # 证件类型
        self._idno = ""  # 证件号码
        self._itemname = "正常工资薪金"  # 所得项目
        self._totalpayable = 0  # 应发合计
        self._tex = 0  # 所得税合计
        self._gjj_gr = 0  # 公积金个人
        self._yl_gr = 0  # 养老保险个人
        self._sy_gr = 0  # 失业保险个人
        self._yil_gr = 0  # 医疗保险个人
        self._nj_gr = 0  # 年金个人

    def getColumnDef(self) -> dict:
        columns = dict()
        columns["_code"] = "工号"
        columns["_name"] = "姓名"

        columns["_idno"] = "证件号码"
        columns["totalpayable"] = "本期收入"
        columns["_tex"] = "累计应补(退)税额"
        columns["_yl_gr"] = "本期基本养老保险费"
        columns["_yil_gr"] = "本期基本医疗保险费"
        columns["_sy_gr"] = "本期失业保险费"
        columns["_gjj_gr"] = "本期住房公积金"
        columns["_nj_gr"] = "本期企业(职业)年金"
        return columns
