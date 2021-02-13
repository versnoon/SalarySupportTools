#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tex_engine.py
@Time    :   2021/01/28 14:29:05
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


from os.path import isfile, exists
from os import makedirs, listdir, remove

from salary_support_tools.exl_to_clazz import ExlToClazz


class TexEngine(object):
    """
    所得税核对及拆分
    """

    def __init__(self, period, person_salarys, person_salarys_idno, departs):
        self._name = "tex"
        self._period = period  # 期间信息
        self._departs = departs  # 审核机构信息
        self._person_salarys = person_salarys  # 人员薪酬信息
        self._person_salarys_idno = person_salarys_idno  # 人员薪酬信息根据身份证汇总
        self._folder_path = r'd:\薪酬审核文件夹'

    def get_tpl_path(self, tex_depart):
        path = r'{}\{}\{}\{}'.format(
            self._folder_path, self._period, "税务相关数据", tex_depart)
        if not exists(path):
            makedirs(path)
        return r'{}\{}_{}'.format(path, self._period,  "税款计算_工资薪金所得.xls")

    def start(self):
        tex_datas = self.load_data()
        tex_datas_split_by_depart = self.split_tex_data_by_depart(tex_datas)
        _, err_msgs = self.validate(tex_datas)

        return err_msgs, tex_datas_split_by_depart

    def load_data(self):

        tex_datas = dict()
        for tex_depart in self.get_tex_departs().keys():

            tex = TexSysStruct()

            tex_load = ExlToClazz(TexSysStruct, tex.getColumnDef(),
                                  self.get_tpl_path(tex_depart), noneable=True)
            datas = tex_load.loadTemp()
            tex_datas[tex_depart] = datas
        return tex_datas

    def get_tex_departs(self):
        # 从机构信息中获取税务机构信息并分组
        res = dict()
        for depart in self._departs.values():
            if depart.texdepart not in res:
                res[depart.texdepart] = depart.texdepart
        return res

    def get_person_salary_info_by_idno_two(self, tex_depart, idno):
        # 通过身份证号获取员工的薪酬信息
        _total_payable = 0  # 应发
        _total_tex = 0  # 当期所得税
        person = None  # 人员信息
        depart = ""  # 文件夹信息
        for depart, person_salary_infos in self._person_salarys_idno.items():
            if idno in person_salary_infos:
                # 相同税务机构
                person_salary_info = person_salary_infos[idno]
                if tex_depart == person_salary_info._tex_depart:
                    person = person_salary_info._person
                    if person is not None:
                        if idno == person._idNo:  # 身份证号相同
                            gz = person_salary_info._gz    # 工资
                            jj = person_salary_info._jj  # 奖金

                            if gz is not None:
                                _total_payable += gz._totalPayable + gz._jkdjf  # 应发+教育经费
                                _total_tex += 0 - gz._gts
                                depart = gz.depart
                            if jj is not None:
                                _total_payable += jj._totalPayable - jj._nddxj  # 去除一次性优惠税率
                                _total_tex += 0 - jj._gts + 0 - jj._gstz
                                depart = jj.depart
                            return person, depart, _total_payable, _total_tex
        return None, "", _total_payable, _total_tex

        #     for idno, person_salary_info in person_salary_infos.items():
        #         if tex_depart == person_salary_info._tex_depart:  # 相同税务机构
        #             person = person_salary_info._person
        #             if person is not None:
        #                 if idno == person._idNo:  # 身份证号相同
        #                     gz = person_salary_info._gz  # 工资
        #                     jj = person_salary_info._jj  # 奖金

        #                     if gz is not None:
        #                         _total_payable += gz._totalPayable
        #                         _total_tex += 0 - gz._gts
        #                         depart = gz.depart
        #                     if jj is not None:
        #                         _total_payable += jj._totalPayable - jj._nddxj  # 去除一次性优惠税率
        #                         _total_tex += 0 - jj._gts + 0 - jj._gstz
        #                         depart = jj.depart
        #                     return person, depart, _total_payable, _total_tex
        # return None, "", _total_payable, _total_tex

    def get_person_salary_info_by_idno(self, tex_depart, idno):
        # 通过身份证号获取员工的薪酬信息
        _total_payable = 0  # 应发
        _total_tex = 0  # 当期所得税
        person = None  # 人员信息
        depart = ""  # 文件夹信息
        for depart, person_salary_infos in self._person_salarys.items():
            for code, person_salary_info in person_salary_infos.items():
                if tex_depart == person_salary_info._tex_depart:  # 相同税务机构
                    person = person_salary_info._person
                    if person is not None:
                        if idno == person._idNo:  # 身份证号相同
                            gz = person_salary_info._gz  # 工资
                            jj = person_salary_info._jj  # 奖金

                            if gz is not None:
                                _total_payable += gz._totalPayable
                                _total_tex += 0 - gz._gts
                                depart = gz.depart
                            if jj is not None:
                                _total_payable += jj._totalPayable - jj._nddxj  # 去除一次性优惠税率
                                _total_tex += 0 - jj._gts + 0 - jj._gstz
                                depart = jj.depart
                            return person, depart, _total_payable, _total_tex
        return None, "", _total_payable, _total_tex

    def validate(self, tex_datas):
        err_mgs = dict()
        for tex_depart, datas in tex_datas.items():

            if datas is not None:
                err_message_map = dict()
                for tex in datas:
                    idno = tex._idno  # 身份证号
                    _tex_total_payable = tex._totalpayable
                    _tex_total_tex = tex._tex
                    person, depart, _total_payable, _total_tex = self.get_person_salary_info_by_idno_two(
                        tex_depart, idno)
                    if person is not None:
                        err_message = []
                        if depart in err_message_map:
                            err_message = err_message_map[depart]
                        if round(_tex_total_payable, 2) != round(_total_payable, 2):  # 当期收入不匹配
                            err_message.append(self.err_mss(
                                "本期收入异常", "税务系统金额{:.2f},宝武EHR金额{:.2f}".format(_tex_total_payable, _total_payable), person))
                        if round(_tex_total_tex, 2) != round(_total_tex, 2):  # 当期所得税不匹配
                            err_message.append(self.err_mss(
                                "所得税异常", "税务系统金额{:.2f},宝武EHR金额{:.2f}".format(_tex_total_tex, _total_tex), person))
                        err_message_map[depart] = err_message
                if len(err_message_map) > 0:
                    err_mgs[tex_depart] = err_message_map
        return len(err_mgs) > 0, err_mgs

    def err_mss(self, err_type, message, person) -> str:
        if person is not None:
            return '错误信息提示:  ->  错误类型 {} - 错误信息 {} - 错误人员 {}'.format(err_type, message, person)
        return '错误信息提示:  ->  错误类型 {} - 错误信息 {}'.format(err_type, message)

    def split_tex_data_by_depart(self, tex_datas):
        res = dict()
        for tex_depart, datas in tex_datas.items():
            if datas is not None:
                dep_res = dict()
                for tex in datas:
                    idno = tex._idno  # 身份证号
                    person, depart, _total_payable, _total_tex = self.get_person_salary_info_by_idno_two(
                        tex_depart, idno)
                    if person is not None:
                        vs = []
                        if depart in dep_res:
                            vs = dep_res[depart]
                        vs.append(tex)
                        dep_res[depart] = vs
                if len(dep_res) > 0:
                    res[tex_depart] = dep_res
        return res


class TexSysStruct(object):
    """
    税务系统信息对象
    """

    def __init__(self):
        self._code = ""  # 工号
        self._name = ""  # 姓名
        self._idtype = "居民身份证"  # 证件类型
        self._idno = ""  # 证件号码
        self._skssqq = ""  # 税款所属期起
        self._skssqz = ""  # 税款所属期止
        self._itemname = "正常工资薪金"  # 所得项目
        self._totalpayable = 0  # 应发合计
        self._bqfy = 0  # 本期费用
        self._bqmssr = 0  # 本期免税收入
        self._tex = 0  # 所得税合计
        self._gjj_gr = 0  # 公积金个人
        self._yl_gr = 0  # 养老保险个人
        self._sy_gr = 0  # 失业保险个人
        self._yil_gr = 0  # 医疗保险个人
        self._nj_gr = 0  # 年金个人
        self._sujkbx = 0  # 本期商业健康保险费
        self._syyl = 0  # 本期税延养老保险费
        self._qtkc = 0  # 本期其他扣除(其他)
        self._ljsr = 0  # 累计收入额
        self._ljms = 0  # 累计免税收入
        self._ljjc = 0  # 累计减除费用
        self._ljzx = 0  # 累计专项扣除
        self._ljznjy = 0  # 累计子女教育支出扣除
        self._ljjxjy = 0  # 累计继续教育支出扣除
        self._ljzfdk = 0  # 累计住房贷款利息支出扣除
        self._ljzfzz = 0  # 累计住房租金支出扣除
        self._ljsylr = 0  # 累计赡养老人支出扣除
        self._ljqtkc = 0  # 累计其他扣除
        self._ljzykc = 0  # 累计准予扣除的捐赠
        self._ljynse = 0  # 累计应纳税所得额
        self._sl = 0  # 税率
        self._sskc = 0  # 速算扣除数
        self._ljynse1 = 0  # 累计应纳税额
        self._ljjm = 0  # 累计减免税额
        self._ljykj = 0  # 累计应扣缴税额
        self._ljynse2 = 0  # 累计已预缴税额

    def getColumnDef(self) -> dict:
        columns = dict()
        columns["_code"] = "工号"
        columns["_name"] = "姓名"
        columns["_idtype"] = "证件类型"
        columns["_idno"] = "证件号码"
        columns["_skssqq"] = "税款所属期起"
        columns["_skssqz"] = "税款所属期止"
        columns["_itemname"] = "所得项目"

        columns["_totalpayable"] = "本期收入"
        columns["_bqfy"] = "本期费用"

        columns["_bqmssr"] = "本期免税收入"
        columns["_yl_gr"] = "本期基本养老保险费"
        columns["_yil_gr"] = "本期基本医疗保险费"
        columns["_sy_gr"] = "本期失业保险费"
        columns["_gjj_gr"] = "本期住房公积金"
        columns["_nj_gr"] = "本期企业(职业)年金"

        columns["_sujkbx"] = "本期商业健康保险费"
        columns["_syyl"] = "本期税延养老保险费"
        columns["_qtkc"] = "本期其他扣除"
        columns["_ljsr"] = "累计收入额"
        columns["_ljms"] = "累计免税收入"

        columns["_ljjc"] = "本累计减除费用"
        columns["_ljzx"] = "累计专项扣除"
        columns["_ljznjy"] = "累计子女教育支出扣除"
        columns["_ljjxjy"] = "累计继续教育支出扣除"
        columns["_ljzfdk"] = "累计住房贷款利息支出扣除"
        columns["_ljzfzz"] = "累计住房租金支出扣除"
        columns["_ljsylr"] = "累计赡养老人支出扣除"

        columns["_ljqtkc"] = "累计其他扣除"
        columns["_ljzykc"] = "累计准予扣除的捐赠"
        columns["_ljynse"] = "累计应纳税所得额"
        columns["_sl"] = "税率"
        columns["_sskc"] = "速算扣除数"
        columns["_ljynse1"] = "累计应纳税额"
        columns["_ljjm"] = "累计减免税额"
        columns["_ljykj"] = "累计应扣缴税额"
        columns["_ljynse2"] = "累计已预缴税额"
        columns["_tex"] = "累计应补(退)税额"

        return columns
