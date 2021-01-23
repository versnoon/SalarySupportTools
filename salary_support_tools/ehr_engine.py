#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ehr_engine.py
@Time    :   2021/01/19 13:56:33
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''
from os.path import isfile, exists
from os import makedirs


from collections import OrderedDict
import xlrd
import xlwt


class EhrEngine(object):
    """
    ehr相关操作
    """

    def __init__(self, name='ehr'):
        self._name = name

    def start(self):
        """
        docstring
        """
        # 解析人员基本信息
        personInfo = PersonInfo()
        cov = ExlToClazz(
            PersonInfo, personInfo.getColumnDef(), personInfo.get_exl_tpl_folder_path())
        persons = cov.loadTemp()

        # 解析人员工资信息
        salaryGzInfo = SalaryGzInfo()
        cov = ExlToClazz(
            SalaryGzInfo, salaryGzInfo.getColumnDef(), salaryGzInfo.get_exl_tpl_folder_path())
        salaryGzs = cov.loadTemp()

        # 解析人员将建信息
        salaryJjInfo = SalaryJjInfo()
        cov = ExlToClazz(
            SalaryJjInfo, salaryJjInfo.getColumnDef(), salaryJjInfo.get_exl_tpl_folder_path())
        salaryJjs = cov.loadTemp()

        salaryBankInfo = SalaryBankInfo()
        cov = ExlToClazz(
            SalaryBankInfo, salaryBankInfo.getColumnDef(), salaryBankInfo.get_exl_tpl_folder_path())
        salaryBanks = cov.loadTemp()

        auditOper = AuditerOperator('202101', '01', personInfo.to_map(persons), salaryGzInfo.to_map(
            salaryGzs), salaryJjInfo.to_map(salaryJjs), salaryBankInfo.to_map(salaryBanks))
        return auditOper.export()

    def validate(self, persinfos, salaryGzs, salaryJjs, salaryBanks):
        """
        验证员工的相关信息
        """
        # 验证工资数据
        for gz in salaryGzs:
            code = gz._code
            # 工资奖金实发小于0
            if gz._pay < 0:
                print("{}，工资实发 < 0 {}".format(persinfos[code], gz._pay))
            # 缺少银行卡号
            if salaryBanks[code]['gz'] is None:
                print("{}，缺少工资银行信息".format(persinfos[code]))
        for jj in salaryJjs:
            code = jj._code
            # 工资奖金实发小于0
            if gz._pay < 0:
                if code in persinfos:
                    print("{}，奖金实发 < 0 {}".format(persinfos[code], gz._pay))
            # 缺少银行卡号
            if salaryBanks[code]['jj'] is None:
                print("{}，缺少奖金银行信息".format(persinfos[code]))

            # 所得税核对
            # 社保核对 怎么完成核对逻辑

    def export(self,):
        """
        生成各类所需的拨款单，银行报盘 等
        """


class PersonInfo(object):
    """
    ehr系统中人员信息
    """

    def __init__(self, complay="", depart="", branch="", assignment="", group="", code="", name="", professional="", gender="", nation="", birthday="", age=0, idNo="", personType="", sourceOfPerson="", timeOfWork="", timeOfJoinBaowu="", timeOfJoinComplay="", vJobTitle="", cJobTitle="", postType="", jobStatus=""):
        self._complayLevelOne = complay  # 一级机构(公司)
        self._departLevelTow = depart  # 二级机构（部门）
        self._branchLevelThree = branch  # 三级机构（分厂）
        self._assignmentSectionLevelFour = assignment  # 四级机构（作业区）
        self._groupLevelFive = group  # 五级机构（班组）
        self._code = code  # 职工编码
        self._name = name  # 姓名
        self._professional = professional  # 资格名称
        self._gender = gender  # 性别
        self._nation = nation  # 民族
        self._birthday = birthday  # 出生日期
        self._age = age  # 年龄
        self._certificateType = '居民身份证'  # 证件类型
        self._idNo = idNo  # 身份证号
        self._personType = personType  # 人员类型
        self._sourceOfPerson = sourceOfPerson  # 人员来源
        self._timeOfWork = timeOfWork  # 参加工作时间
        self._timeOfJoinBaowu = timeOfJoinBaowu  # 进入宝武时间
        self._timeOfJoinComplay = timeOfJoinComplay  # 进去公司时间
        self._vJobTile = vJobTitle  # 核定岗位名称
        self._cJobTitle = cJobTitle  # 执行岗位名称
        self._postType = postType  # 岗位类型
        self._jobStatus = jobStatus  # 人员类型

    def getColumnDef(self) -> dict:
        columns = dict()
        columns["_complayLevelOne"] = "一级机构(公司)"
        columns["_departLevelTow"] = "二级机构(部门)"
        columns["_branchLevelThree"] = "三级机构(分厂)"
        columns["_assignmentSectionLevelFour"] = "四级机构(作业区)"
        columns["_groupLevelFive"] = "五级机构(班组)"
        columns["_code"] = "工号"
        columns["_name"] = "姓名全称"
        columns["_professional"] = "资格名称"
        columns["_gender"] = "性别"
        columns["_nation"] = "民族"
        columns["_birthday"] = "出生日期"
        columns["_age"] = "年龄"
        columns["_certificateType"] = "证件类型"
        columns["_idNo"] = "证件号码"
        columns["_personType"] = "人员类型"
        columns["_sourceOfPerson"] = "人员来源"
        columns["_timeOfWork"] = "参加工作时间"
        columns["_timeOfJoinBaowu"] = "来宝钢系统日期"
        columns["_timeOfJoinComplay"] = "来公司日期"
        columns["_vJobTile"] = "核定岗位"
        columns["_cJobTitle"] = "执行岗位"
        columns["_postType"] = "岗位类型"
        columns["_jobStatus"] = "在职状态"
        return columns

    def get_exl_tpl_folder_path(self):
        return r'd:\薪酬审核文件夹\202101\人员信息.xls'

    def to_map(self, datas):
        m = dict()
        for i in range(len(datas)):
            personInfo = datas[i]
            m[personInfo._code] = personInfo
        return m

    def __str__(self):
        return '员工基本信息: 公司 {} - 部门 {} - 分厂 {} - 作业区 {} - 班组 {} - 工号 {} - 姓名 {} - 岗位 {}'.format(self._complayLevelOne, self._departLevelTow, self._branchLevelThree, self._assignmentSectionLevelFour, self._groupLevelFive, self._code, self._name, self._cJobTitle)


class SalaryGzInfo(object):
    """
    工资信息
    """

    def __init__(self, code="", name="", departfullinfo="", depart="", branch="", salaryModel="", jobName="", postPrice="", distributionMark="", fzZxkc=0, fdZxkc=0, jxjyZxkc=0, znjyZxkc=0, sylrZxkc=0, zxnf=0, gsgl=0, lxgl=0, bjbl=0, gwxs=0, gwxbz=0, gwgz=0, blgz=0, glgz=0, jbx=0, qtblgz=0, gdgz=0, dtxgz=0, gwx=0, zlx=0, yfjxnx=0, shf=0, jbgzdy=0, rpjgzkk=0, rpjgzjk=0, zybjt=0, jnjt=0, jggzjt=0, gzzjt=0, kjyxjt=0, cznsjt=0, xljt=0, txjt=0, cqjt=0, gwjt=0, mzjt=0, wcjt=0, gsjt=0, gshljt=0, jsjt=0, tsgxjt=0, zwjt=0, gongwjt=0, gxbtjt=0, sdqnwyjt=0, shbtjt=0, shfbcjt=0, totaljt=0, rpjgz=0, qtnssr=0, ygdxz=0, jxgz=0, jdfdyyz=0, khfd=0, shfbt=0, dsznf=0, jkdjf=0, qtdf=0, kdjf=0, gztz=0, qtbf=0, qtkk=0, qtdkk=0, fdjbgz=0, xxrjbgz=0, psjbgz=0, totaljbgz=0, bjkk=0, sjkk=0, kgkk=0, totalkk=0, yl=0, yil=0, sy=0, gjj=0, nj=0, gjjbz=0, yse=0, gts=0, dfxm=0, bfone=0, bftwo=0, totaldk=0, pay=0, ylqybx=0, yilqybx=0, syqybx=0, shyqybx=0, gsqybx=0, gjjqybx=0, njqybx=0, totalPayable=0):
        self._code = code  # 员工通行证
        self._name = name  # 员工姓名
        self._departfullinfo = departfullinfo  # 机构
        self._departLevelTow = depart  # 二级机构
        self._branchLevelThree = branch  # 三级机构
        self._salaryModel = salaryModel  # 薪酬模式
        self._jobName = jobName  # 岗位名称
        self._postPrice = postPrice  # 岗位价值
        self._distributionMark = distributionMark  # 是否代发工资
        self._fzZxkc = fzZxkc  # 累计住房租金支出
        self._fdZxkc = fdZxkc  # 累计住房贷款利息支出
        self._jxjyZxkc = jxjyZxkc  # 累计继续教育支出
        self._znjyZxkc = znjyZxkc  # 累计子女教育支出
        self._sylrZxkc = sylrZxkc  # 累计赡养老人支出
        self._zxnf = zxnf
        self._gsgl = gsgl
        self._lxgl = lxgl
        self._bjbl = bjbl
        self._gwxs = gwxs
        self._gwxbz = gwxbz
        self._gwgz = gwgz
        self._blgz = blgz
        self._glgz = glgz
        self._jbx = jbx
        self._qtblgz = qtblgz
        self._gdgz = gdgz   # 固定工资
        self._dtxgz = dtxgz  # 待退休工资
        self._gwx = gwx  # 岗位薪
        self._zlx = zlx  # 资历薪酬
        self._yfjxnx = yfjxnx
        self._shf = shf
        self._jbgzdy = jbgzdy
        self._rpjgzkk = rpjgzkk
        self._rpjgzjk = rpjgzjk
        # 津贴
        self._zyb_jt = zybjt
        self._jn_jt = jnjt
        self._jggz_jt = jggzjt
        self._gzz_jt = gzzjt
        self._kjyx_jt = kjyxjt
        self._czns_jt = cznsjt
        self._xl_jt = xljt
        self._tx_jt = txjt
        self._cq_jt = cqjt
        self._gw_jt = gwjt
        self._mz_jt = mzjt
        self._wc_jt = wcjt
        self._gs_jt = gsjt
        self._gshl_jt = gshljt
        self._js_jt = jsjt
        self._tsgx_jt = tsgxjt
        self._zw_jt = zwjt   # 驻外津贴
        self._gongw_jt = gongwjt  # 公务津贴
        self._gxbt_jt = gxbtjt  # 各项补贴
        self._sdqnwy_jt = sdqnwyjt  # 水电气暖物业补贴
        self._shbt_jt = shbtjt   # 生活补贴
        self._shfbc_jt = shfbcjt  # 生活费补差
        self._gxbt_jt = gxbtjt  # 岗薪补贴
        self._total_jt = totaljt  # 津贴合计
        # 工资补退
        self._rpjgz = rpjgz    # 日平均工资3(津贴)
        self._qtnssr = qtnssr  # 其他纳税收入
        self._ygdxz = ygdxz  # 月固定工资
        self._jxgz = jxgz  # 绩效工资
        self._jdfdyyz = jdfdyyz  # 季度浮动月预支
        self._khfd = khfd  # 考核浮动
        self._shfbt = shfbt  # 生活费补贴
        self._dsznf = dsznf  # 独生子女费
        self._jkdjf = jkdjf  # 兼课带教费

        self._qtdf = qtdf   # 其他代发
        self._gztz = gztz  # 工资调整
        self._qtbf = qtbf  # 其它补发
        self._qtkk = qtkk  # 其它扣款
        self._qtdkk = qtdkk  # 其他代扣款
        # 加班
        self._fd_jbgz = fdjbgz
        self._xxr_jbgz = xxrjbgz
        self._ps_jbgz = psjbgz
        self._total_jbgz = totaljbgz

        # 扣款
        self._bjkk_kk = bjkk
        self._sjkk_kk = sjkk
        self._kgkk_kk = kgkk
        self._total_kk = totalkk

        # 社保公积金年金
        self._yl_bx = yl  # 养老
        self._yil_bx = yil  # 医疗
        self._sy_bx = sy  # 失业
        self._gjj_bx = gjj  # 公积金
        self._nj_bx = nj  # 年金
        self._gjjbz_bx = gjjbz  # 公积金补助

        self._totalPayable = totalPayable  # 应发
        self._yse = yse  # 应发额
        self._gts = gts  # 个调税
        self._dfxm = dfxm  # 代发项目
        self._bfone = bfone  # 补发1
        self._bftwo = bftwo  # 补发2
        self._total_dk = totaldk  # 代扣合计
        self._pay = pay  # 实发

        # 企业部分
        self._yl_qybx = ylqybx  # 养老
        self._yil_qybx = yilqybx  # 医疗
        self._sy_qybx = syqybx  # 失业
        self._shy_qybx = shyqybx  # 生育
        self._gs_qybx = gsqybx  # 工伤
        self._gjj_qybx = gjjqybx  # 公积金
        self._nj_qybx = njqybx  # 年金

    def __str__(self):
        return '员工工资信息: 机构 {} - 二级机构 {} - 三级机构 {} - 工号 {} - 姓名 {} - 岗位 {} - 应发 {}'.format(self._departfullinfo, self._departLevelTow, self._branchLevelThree, self._code, self._name, self._jobName, self._totalPayable)

    def getColumnDef(self) -> dict:
        columns = dict()
        columns["_code"] = "员工通行证"
        columns["_name"] = "员工姓名"
        columns["_departfullinfo"] = "机构"
        columns["_departLevelTow"] = "二级机构"
        columns["_branchLevelThree"] = "三级机构"
        columns["_salaryModel"] = "薪酬模式"
        columns["_jobName"] = "岗位名称"
        columns["_postPrice"] = "岗位价值"
        columns["_distributionMark"] = "是否代发工资"
        columns["_fzZxkc"] = "累计住房租金支出"
        columns["_fdZxkc"] = "累计住房贷款利息支出"
        columns["_jxjyZxkc"] = "累计继续教育支出"
        columns["_jxjyZxkc"] = "累计子女教育支出"

        columns["_sylrZxkc"] = "累计赡养老人支出"
        columns["_zxnf"] = "执行年份"
        columns["_gsgl"] = "公司工龄"
        columns["_lxgl"] = "连续工龄"
        columns["_bjbl"] = "病假扣款比例"
        columns["_gwxs"] = "岗位系数"
        columns["_gwxbz"] = "岗位薪标准"
        columns["_gwgz"] = "岗位工资"
        columns["_blgz"] = "保留工资"
        columns["_glgz"] = "工龄工资"
        columns["_jbx"] = "基本薪"
        columns["_qtblgz"] = "其他保留工资"
        columns["_gdgz"] = "固定工资"
        columns["_dtxgz"] = "待退休工资"
        columns["_gwx"] = "岗位薪"
        columns["_zlx"] = "资历薪"
        columns["_yfjxnx"] = "预发绩效年薪"
        columns["_shf"] = "生活费"
        columns["_jbgzdy"] = "基本工资单元"
        columns["_rpjgzkk"] = "日平均工资(扣款)"
        columns["_rpjgzjk"] = "日平均工资2(加款)"

        columns["_zyb_jt"] = "中夜班津贴"
        columns["_jn_jt"] = "技能津贴"
        columns["_jggz_jt"] = "兼岗工资"
        columns["_gzz_jt"] = "班组长津贴"
        columns["_kjyx_jt"] = "科技优秀津贴"
        columns["_czns_jt"] = "操作能手津贴"
        columns["_xl_jt"] = "学历津贴"
        columns["_tx_jt"] = "通讯补贴"
        columns["_cq_jt"] = "出勤津贴"
        columns["_gw_jt"] = "高温津贴"
        columns["_mz_jt"] = "民族津贴"
        columns["_wc_jt"] = "误餐补助"
        columns["_gs_jt"] = "工伤津贴"
        columns["_gshl_jt"] = "工伤护理费"
        columns["_js_jt"] = "技术津贴"
        columns["_tsgx_jt"] = "特殊贡献津贴"
        columns["_zw_jt"] = "驻外津贴"

        columns["_gongw_jt"] = "公务车贴"
        columns["_gxbt_jt"] = "各项补贴"
        columns["_sdqnwy_jt"] = "水电气暖物业补贴"
        columns["_shbt_jt"] = "生活补贴"
        columns["_shfbc_jt"] = "生活费补差"
        columns["_gxbt_jt"] = "岗薪补贴"
        columns["_total_jt"] = "津贴合计"
        columns["_rpjgz"] = "日平均工资3(津贴)"
        columns["_qtnssr"] = "其它纳税收入"
        columns["_ygdxz"] = "月固定薪资"
        columns["_jxgz"] = "绩效工资"
        columns["_jdfdyyz"] = "季度浮动月预支"
        columns["_khfd"] = "考核浮动"
        columns["_shfbt"] = "生活费补贴"
        columns["_dsznf"] = "独生子女费"
        columns["_jkdjf"] = "兼课带教费"

        columns["_qtdf"] = "其他代发"
        columns["_gztz"] = "工资调整"
        columns["_qtbf"] = "其它补发"
        columns["_qtkk"] = "其它扣款"
        columns["_qtdkk"] = "其他代扣款"

        columns["_fd_jbgz"] = "法定假日加班工资"
        columns["_xxr_jbgz"] = "休息日加班工资"
        columns["_ps_jbgz"] = "平常加班工资"
        columns["_total_jbgz"] = "加班工资单元"

        columns["_bjkk_kk"] = "病假扣款"
        columns["_sjkk_kk"] = "事假扣款"
        columns["_kgkk_kk"] = "旷工扣款"
        columns["_total_kk"] = "缺勤扣款单元"

        columns["_yl_bx"] = "养老保险个人额度"
        columns["_sy_bx"] = "失业保险个人额度"
        columns["_yil_bx"] = "医疗保险个人额度"
        columns["_gjj_bx"] = "公积金个人额度"
        columns["_nj_bx"] = "企业年金个人额度"

        columns["_gjjbz_bx"] = "公积金补助"
        columns["_totalPayable"] = "应发"
        columns["_yse"] = "应税额"
        columns["_gts"] = "个调税"
        columns["_dfxm"] = "代发项目"
        columns["_bfone"] = "补发一"

        columns["_bftwo"] = "补发二"
        columns["_total_dk"] = "代扣合计"
        columns["_pay"] = "实发"
        columns["_yl_qybx"] = "养老保险企业额度"
        columns["_sy_qybx"] = "失业保险企业额度"
        columns["_yil_qybx"] = "医疗保险企业额度"
        columns["_shy_qybx"] = "生育保险企业额度"
        columns["_gs_qybx"] = "工伤保险企业额度"
        columns["_gjj_qybx"] = "公积金企业额度"
        columns["_nj_qybx"] = "企业年金企业额度"

        return columns

    def get_exl_tpl_folder_path(self):
        return r'd:\薪酬审核文件夹\202101\工资信息-股份.xls'

    def to_map(self, datas):
        m = dict()
        for i in range(len(datas)):
            info = datas[i]
            m[info._code] = info
        return m


class SalaryJjInfo(object):
    """
    奖金信息
    """

    def __init__(self, code="", name="", departfullinfo="", distributionMark="", ysjse=0, bonusTow=0, gtsyj=0, pay=0, jjhj=0, totalPayable=0, jsjseptsl=0, jbjj=0, gts=0, bonusOne=0, bonusThree=0, yseyhsl=0, yse=0, gstz=0, gcjj=0, jssc=0, nddxj=0, jsjj=0, qt=0, gsxyj=0):
        self._code = code
        self._name = name
        self._departfullinfo = departfullinfo
        self._distributionMark = distributionMark
        self._ysjse = ysjse
        self._bonusTwo = bonusTow
        self._gtsyj = gtsyj
        self._pay = pay
        self._jjhj = jjhj
        self._jsjseptsl = jsjseptsl
        self._jbjj = jbjj
        self._gts = gts
        self._bonusOne = bonusOne
        self._bonusThree = bonusThree
        self._yseyhsl = yseyhsl
        self._yse = yse
        self._totalPayable = totalPayable
        self._gstz = gstz
        self._gcjj = gcjj
        self._jssc = jssc
        self._nddxj = nddxj
        self._jsjj = jsjj
        self._qt = qt
        self._gsxyj = gsxyj

    def __str__(self):
        return '员工奖金信息: 机构 {} - 工号 {} - 姓名 {} - 应发 {} - 实发 {}'.format(self._departfullinfo, self._code, self._name, self._totalPayable, self._pay)

    def getColumnDef(self) -> dict:
        columns = dict()
        columns["_code"] = "员工通行证"
        columns["_name"] = "员工姓名"
        columns["_departfullinfo"] = "机构"
        columns["_distributionMark"] = "是否代发工资"
        columns["_ysjse"] = "应税计算额(优惠税率)"
        columns["_bonusTwo"] = "单项奖2"
        columns["_gtsyj"] = "个调税(应缴)"
        columns["_pay"] = "实发"
        columns["_jjhj"] = "奖金合计"
        columns["_jsjseptsl"] = "应税计算额(普通税率)"
        columns["_jbjj"] = "基本奖金"
        columns["_gts"] = "个调税"
        columns["_bonusOne"] = "单项奖1"
        columns["_bonusThree"] = "单项奖3"
        columns["_yseyhsl"] = "应税额(优惠税率)"
        columns["_bonusThree"] = "单项奖3"
        columns["_yseyhsl"] = "应税额"
        columns["_totalPayable"] = "应发"
        columns["_gstz"] = "个税调整"
        columns["_gcjj"] = "工程津贴"
        columns["_jssc"] = "技术输出"
        columns["_qt"] = "争取国家政策奖"
        columns["_nddx"] = "年底兑现奖"
        columns["_jsjj"] = "计税奖金"
        return columns

    def get_exl_tpl_folder_path(self):
        return r'd:\薪酬审核文件夹\202101\奖金信息-股份.xls'

    def to_map(self, datas):
        m = dict()
        for i in range(len(datas)):
            info = datas[i]
            m[info._code] = info
        return m


class SalaryBankInfo(object):
    """
    奖金信息
    """

    def __init__(self, code="", name="", departfullinfo="", financialInstitution="", bankNo="", payment="", purpose="", associalBankNo="", cardType=""):
        self._code = code
        self._name = name
        self._departfullinfo = departfullinfo
        self._financialInstitution = financialInstitution
        self._bankNo = bankNo
        self._payment = payment
        self._purpose = purpose
        self._associalBankNo = associalBankNo
        self._cardType = cardType

    def __str__(self):
        return '员工银行卡信息: 机构 {} - 工号 {} - 姓名 {} - 金融机构 {} - 卡号 {}'.format(self._departfullinfo, self._code, self._name, self._financialInstitution, self._bankNo)

    def getColumnDef(self) -> dict:
        columns = dict()
        columns["_code"] = "员工通行证"
        columns["_name"] = "员工姓名"
        columns["_departfullinfo"] = "部门"
        columns["_financialInstitution"] = "金融机构"
        columns["_bankNo"] = "卡号"
        columns["_payment"] = "支付方式"
        columns["_purpose"] = "卡用途"
        columns["_associalBankNo"] = "联行号/网点代码"
        columns["_cardType"] = "卡折类型"

        return columns

    def get_exl_tpl_folder_path(self):
        return r'd:\薪酬审核文件夹\202101\银行卡信息-股份.xls'

    def to_map(self, datas):
        m = dict()
        for i in range(len(datas)):
            info = datas[i]
            v = dict()
            if info._code in m:
                v = m[info._code]
            if self.is_gz_bankno(info._purpose):
                v['gz'] = info
            if self.is_jj_bankno(info._purpose):
                v['jj'] = info
            m[info._code] = v
        return m

    def is_gz_bankno(self, purpose=""):
        return self.val_bank_purpost(purpose, "工资卡")

    def is_jj_bankno(self, purpose=""):
        return self.val_bank_purpost(purpose, "奖金卡")

    def val_bank_purpost(self, purpose="", banktype=""):
        if len(purpose) == 0:
            return False
        if len(banktype) == 0:
            return False
        if banktype in purpose:
            return True
        else:
            return False


class ExlToClazz(object):
    """
    模板
    """

    def __init__(self, clazz, columnsDef, filePath, titleindex=0):
        self.clazz = clazz
        self.columnsDef = columnsDef
        self.filePath = filePath
        self.titleindex = titleindex

    def loadTemp(self) -> []:
        if not isfile(self.filePath):
            raise FileNotFoundError("文件路径 {0} 不存在".format(self.filePath))
        # 读取模板文件
        book = xlrd.open_workbook(self.filePath)
        # 读取第一个sheet 工作簿
        sheet = book.sheet_by_index(0)
        # 获取列头
        titles = sheet.row_slice(self.titleindex)
        # 反射生成
        res = []
        for r in range(sheet.nrows):
            if r > self.titleindex:
                row = sheet.row_slice(r)
                ins = self.clazz()
                for i in range(len(titles)):
                    propertyName = self.getPropertyName(titles[i].value)
                    if "" != propertyName:
                        setattr(ins, propertyName, row[i].value)
                res.append(ins)

        return res

    def getPropertyName(self, columnName) -> str:
        """
        docstring
        """
        columns = self.columnsDef
        for key in columns.keys():
            if columns[key] == columnName:
                return key
        return ""


class AuditerOperator(object):
    """
    审核表相关业务
    """

    def __init__(self, period, salaryScope, personinfos, salaryGzs, salaryJjs, salaryBanks):
        self.period = period
        self.salaryScope = salaryScope
        self._persons = personinfos
        self._gzs = salaryGzs
        self._jjs = salaryJjs
        self._banks = salaryBanks

    def to_auditors(self):
        datas = []
        # 工资奖金数据
        for key in self._gzs.keys():
            a = Auditor(self.period, self.salaryScope)
            jj = None
            if key in self._jjs:
                jj = self._jjs[key]
            bank = None
            if key in self._banks:
                bank = self._banks[key]
            a.to_auditor(self._persons[key],
                         self._gzs[key], jj, bank)
            datas.append(a)
        # 其他不在系统内人员
        for key in self._jjs.keys():
            if key not in self._gzs:
                a = Auditor(self.period, self.salaryScope)
                bank = None
                if key in self._banks:
                    bank = self._banks[key]
                a.to_auditor(None, None, self._jjs[key], bank)
        return datas

    def export(self):
        # 导出excel
        self.createExcel(self.to_auditors(), self.columnsDef())

    def columnsDef(self):
        columns = OrderedDict()
        columns["period"] = "发薪期间"
        columns["salaryScope"] = "工资范围"
        columns["_code"] = "员工编号"
        columns["_name"] = "员工姓名"
        columns["_gwgz"] = "岗位工资"
        columns["_blgz"] = "保留工资"
        columns["_nggz"] = "年功工资"
        columns["_fzgz"] = "辅助工资"
        columns["_shbt"] = "生活补贴"
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
        columns["_yzdnjt"] = "一专多能、计生、纪检、信访津贴"
        columns["_ksjt"] = "矿山津贴"
        columns["_xjjt"] = "下井津贴"
        columns["_zwjt"] = "驻外津贴"
        columns["_wyjt"] = "外语津贴"
        columns["_bzzjt"] = "班组长津贴"
        columns["_kjjt"] = "科技津贴"
        columns["_nsjt"] = "能手津贴"
        columns["_totaljj"] = "奖金合计"
        columns["_totaljbf"] = "加班费合计"
        columns["_totalqq"] = "缺勤扣款合计"
        columns["_gjj"] = "公积金"
        columns["_yl"] = "养老保险"
        columns["_sy"] = "失业保险"
        columns["_yil"] = "医疗保险"
        columns["_nj"] = "年金"
        columns["_totalsdj"] = "工资税收"
        columns["_sljj"] = "水利基金"
        columns["_df"] = "电费"
        columns["_fz"] = "房租"
        columns["_dsf"] = "电视费"
        columns["_qjf"] = "清洁费"
        columns["_ccf"] = "乘车费"
        columns["_cwbt"] = "财务补退"
        columns["_wybt"] = "物业补贴"
        columns["_bjf"] = "保健费"
        columns["_db"] = "独补"
        columns["_txf"] = "通讯费"
        columns["_gwf"] = "高温津贴"
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

        columns["_totalpayalbe"] = "应发合计"
        columns["_totalpay"] = "实发合计"
        columns["_jyjf"] = "教育经费"
        columns["_gcjj"] = "工程津贴"
        columns["_jssc"] = "技术输出"
        columns["_qt"] = "其他"
        columns["_gsxyj"] = "公司效益奖"
        columns["_gsxyjpay"] = "公司效益奖上卡"
        columns["_gsxyjtex"] = "公司效益奖所得税"
        columns["_nddxj"] = "年底兑现奖"
        columns["_nddxjpay"] = "年底兑现奖实发"
        columns["_nddxjtex"] = "年底兑现奖所得税"
        columns["_jsjj"] = "计税奖金"
        columns["_yznx"] = "预支年薪"
        columns["_zygz"] = "执业工资"
        columns["_bankno1"] = "银行卡1"
        columns["_bankinfo1"] = "银行1"
        columns["_bankno2"] = "银行卡2"
        columns["_bankinfo2"] = "银行2"
        columns["_gzpay"] = "上卡工资"
        columns["_nddxjpay"] = "上卡年终奖"
        columns["_jjpay"] = "上卡基本奖"
        columns["_sfhd"] = "实发核对"
        columns["_ygz"] = "员工组"
        columns["_ygzz"] = "员工子组"

        return columns

    def createExcel(self, datas, columndefs):
        """
        创建excel
        """
        b = xlwt.Workbook(encoding='uft-8')
        s = b.add_sheet('系统数据')

        # 写入标题
        for i, v in enumerate(columndefs.values()):
            s.write(0, i, v)
        for i, v in enumerate(datas):
            for j, propertyName in enumerate(columndefs.keys()):
                try:
                    s.write(
                        i+1, j, getattr(datas[i], propertyName, ''))
                except TypeError:
                    print(propertyName)

        path = r'd:\薪酬审核文件夹\202101\导出文件'
        if not exists(path):
            makedirs(path)
        b.save(r'd:\薪酬审核文件夹\202101\导出文件\系统数据.xls')
        pass


class Auditor(object):
    """
    审核表业务模型
    """

    def __init__(self, period, salaryScope, code="", name="", gwgz=0, blgz=0, nggz=0, fzgz=0, shbz=0, khgz=0, gzbt=0, qtgz=0, ntjbgz=0, ntzz=0, ntglgz=0, djsj=0, ybjt=0, jsjt=0, yzdnjt=0, ksjt=0, xjjt=0, zwjt=0, wyjt=0, bzzjt=0, kjjt=0, nsjt=0, totaljbf=0, totalqq=0, gjj=0, yl=0, sy=0, yil=0, nj=0, totalsdj=0, sljj=0, cwkk=0, cwbt=0, wybt=0, bjf=0, db=0, txf=0, gwf=0, hm=0, wcf=0, scjt=0, zwbt=0, kyxm=0, jsgg=0, fgzjtbf=0, yznx=0, totalpayalbe=0, totalpay=0, jyjf=0, gcjt=0, jssc=0, qt=0, jbjj=0, gsxyj=0, nddxj=0, nddxjpay=0, nddxjtex=0, jsjj=0, totaljj=0, gzpay=0, jjpay=0, bankno1="", bankinfo1="", bankno2="", bankinfo2="", ygz=""):
        self.period = period  # 期间
        self.salaryScope = salaryScope  # 工资范围
        self._code = code  # 职工编码
        self._name = name  # 姓名
        # 工资信息
        self._gwgz = gwgz  # 岗位工资
        self._blgz = blgz  # 保留工资
        self._nggz = nggz  # 年功工资
        self._fzgz = fzgz  # 辅助工资
        self._shbz = shbz  # 生活补助
        self._khgz = khgz  # 考核工资
        self._gzbt = gzbt  # 工资补退
        self._qtgz = qtgz  # 其他工资
        self._ntjbgz = ntjbgz  # 内退基本工资
        self._ntzz = ntzz  # 内退增资
        self._ntglgz = ntglgz  # 内退工龄工资
        self._djsj = djsj  # 代缴三金
        self._wjbt = 0  # 物价补贴
        self._ybjt = ybjt  # 夜班津贴
        self._jsjt = jsjt  # 技师津贴
        self._yzdnjt = yzdnjt  # 一转多能津贴(纪检 计生 信访)
        self._ksjt = ksjt  # 矿山津贴
        self._xjjt = xjjt  # 下井津贴
        self._zwjt = zwjt  # 驻外津贴 （原教护龄津贴）
        self._wyjt = wyjt  # 外语津贴
        self._bzzjt = bzzjt  # 班组长津贴
        self._kjjt = kjjt  # 科技津贴
        self._nsjt = nsjt  # 能手津贴
        self._totaljj = totaljj  # 奖金合计
        self._totaljbf = totaljbf  # 加班费合计
        self._totalqq = totalqq  # 缺勤扣款合计
        self._yznx = yznx  # 预支年薪
        self._zygz = 0  # 执业工资

        self._gjj = gjj  # 公积金个人
        self._yl = yl  # 养老保险个人
        self._sy = sy  # 失业保险个人
        self.yil = yil  # 医疗保险个人
        self._nj = nj  # 年金保险个人

        # 其他扣缴
        self._sljj = sljj  # 水利基金
        self._cwkk = cwkk  # 财务扣款

        self._df = 0  # 电费
        self._fz = 0  # 房租
        self._dsf = 0  # 电视费
        self._qjf = 0  # 清洁费
        self._ccf = 0  # 乘车费
        self._cwbt = cwbt  # 财务补退

        # 非工资信息
        self._wybt = wybt  # 物业补贴
        self._bjf = bjf  # 保健费
        self._db = db  # 独补
        self._txf = txf  # 通讯费
        self._gwf = gwf  # 高温津贴
        self._hm = hm  # 回民
        self._jj = 0  # 纪检津贴
        self._js = 0  # 计生津贴
        self._wcf = wcf  # 误餐费
        self._ksryj = 0  # 矿山荣誉金
        self._xf = 0  # 信访津贴
        self._scjt = scjt  # 伤残津贴
        self._zwbt = zwbt  # 职务补贴
        self._kyxm = kyxm  # 科研项目津贴
        self._jsgg = jsgg  # 技术攻关津贴
        self._fgzjtbf = fgzjtbf  # 非工资津贴补发

        # 奖金信息
        self._jbjj = jbjj  # 基本奖金
        self._gsxyj = gsxyj  # 公司效益奖
        self._gsxyjpay = 0  # 公司效益奖上卡
        self._gsxyjtex = 0  # 公司效益奖所得税
        self._nddxj = nddxj  # 年底兑现奖
        self._nddxjpay = 0  # 年底兑现将实发
        self._nddxjtex = 0  # 年底兑现将所得税
        self._jsjj = jsjj  # 计税奖金
        self._gcjt = gcjt  # 工程津贴
        self._jssc = jssc  # 技术输出
        self._qt = qt  # 争取国家政策等
        # 账号信息
        self._bankno1 = bankno1  # 银行账号1
        self._bankinfo1 = bankinfo1  # 银行1
        self._bankno2 = bankno2  # 银行账号1
        self._bankinfo2 = bankinfo2  # 银行1

        # 汇总

        self._totalsdj = totalsdj  # 所得税
        self._totalpayalbe = totalpayalbe  # 应发
        self._totalpay = totalpay  # 实发
        self._gzpay = gzpay  # 工资上卡
        self._jjpay = jjpay  # 奖金上卡
        self._nddxjpay = 0  # 年终奖上卡
        self._sfhd = 0  # 实发核对

        # 代发项目

        self._jyjf = jyjf  # 教育经费
        self._gcjt = gcjt  # 工程津贴
        self._jssc = jssc  # 技术输出
        self._qt = qt  # 其他

        self._ygz = ygz
        self._ygzz = ""

    def to_auditor(self, personinfo: PersonInfo, gzinfo: SalaryGzInfo, jjinfo: SalaryJjInfo, bankinfo: SalaryBankInfo):
        if personinfo is not None:
            self._code = personinfo._code
            self._name = personinfo._name
            self._ygz = personinfo._personType
            self._ygzz = personinfo._jobStatus
        else:
            if jjinfo is not None:
                self._code = jjinfo._code
                self._name = jjinfo._name
            else:
                raise ValueError("数据异常，存在不合法的发放人员数据")
        if gzinfo is not None:
            self._gwgz = gzinfo._gwgz
            self._blgz = gzinfo._blgz
            self._nggz = gzinfo._glgz
            self._fzgz = gzinfo._qtblgz
            self._shbz = gzinfo._shbt_jt
            self._khgz = gzinfo._khfd
            self._gzbt = gzinfo._gztz
            self._qtgz = gzinfo._shf
            self._ntjbgz = gzinfo._gdgz
            self._ntzz = gzinfo._dtxgz
            self._ntglgz = gzinfo._glgz
            self._djsj = gzinfo._shfbc_jt
            self._wjbt = 0
            self._ybjt = gzinfo._zyb_jt
            self._jsjt = gzinfo._jn_jt
            self._yzdnjt = gzinfo._jggz_jt
            self._ksjt = 0
            self._xjjt = 0
            self._zwjt = gzinfo._zw_jt
            self._wyjt = gzinfo._xl_jt
            self._bzzjt = 0
            self._kjjt = gzinfo._kjyx_jt
            self._nsjt = gzinfo._czns_jt
            self._totaljbf = gzinfo._total_jbgz
            self._totalqq = gzinfo._total_kk

            self._gjj = 0 - gzinfo._gjj_bx
            self._yl = 0 - gzinfo._yl_bx
            self._sy = 0 - gzinfo._sy_bx
            self._yil = 0 - gzinfo._yil_bx
            self._nj = 0 - gzinfo._nj_bx

            if gzinfo._gts != "":
                self._totalsdj = 0 - gzinfo._gts  # 工资所得税

            if gzinfo._qtdkk != "":
                self._sljj = 0 - gzinfo._qtdkk  # 水利基金
            if gzinfo._qtkk != "":
                self._cwkk = 0 - gzinfo._qtkk  # 其他扣款

            self._wyjt = gzinfo._sdqnwy_jt  # 物业补贴
            self._bjf = gzinfo._cq_jt
            self._db = gzinfo._dsznf
            self._txf = gzinfo._tx_jt
            self._gwf = gzinfo._gw_jt
            self._hm = gzinfo._mz_jt
            self._wcf = gzinfo._wc_jt
            self._scjt = gzinfo._gs_jt
            self._zwbt = gzinfo._gongw_jt
            self._kyxm = gzinfo._tsgx_jt
            self._jsgg = gzinfo._js_jt
            self._fgzjtbf = gzinfo._gxbt_jt
            self._yznx = gzinfo._ygdxz + gzinfo._jxgz

            self._totalpayalbe = gzinfo._totalPayable   # 工资应发
            self._totalpay = gzinfo._pay  # 工资实发
            self._gzpay = gzinfo._pay  # 工资实发

            self._jyjf = gzinfo._jkdjf

        if jjinfo is not None:
            self._jbjj = jjinfo._jbjj

            self._gcjt = jjinfo._gcjj
            self._jssc = jjinfo._jssc
            self._qt = jjinfo._qt
            self._gsxyj = jjinfo._gsxyj
            self._nddxj = jjinfo._nddxj
            self._jsjj = jjinfo._jsjj

            self._totaljj = jjinfo._totalPayable

            self._totalsdj = self._totalsdj + 0 - jjinfo._gts  # 合并入奖金所得税

            self._totalpayalbe = self._totalpayalbe + jjinfo._totalPayable  # 合并奖金应发
            self._totalpay = self._totalpay + jjinfo._totalPayable  # 合并奖金实发
            self._jjpay = jjinfo._pay  # 奖金实发

        if bankinfo is not None:
            self._bankno1 = bankinfo['gz']._bankNo
            self._bankinfo1 = bankinfo['gz']._financialInstitution
            if 'jj' in bankinfo:
                self._bankno2 = bankinfo['jj']._bankNo
                self._bankinfo2 = bankinfo['jj']._financialInstitution

    def __str__(self):
        return '审批表信息: 发薪日期 {} - 工资范围 {} - 职工编码 {} - 姓名 {} - 人员类型 {} - 在职状态 {} - 应发合计 {} - 奖金合计 {} - 公积金 {} - 养老保险 {} - 失业保险 {} - 医疗保险 {} - 年金 {} - 所得税 {} - 实发合计 {} - 工资卡号 {} - 工资卡金融机构 {} - 奖金卡号 {} - 奖金卡金融机构 {}'.format(
            self.period, self.salaryScope, self._code, self._name, self._ygz, self._ygzz, self._totalpayalbe, self._totaljj, self._gjj, self._yl, self._sy, self._yil, self._nj, self._totalsdj, self._totalpay, self._bankno1, self._bankinfo1, self._bankno2, self._bankinfo2)


class TexOperator(object):
    """
    税单相关表
    """

    def __init__(self, datas,):
        self._datas = datas


class TexInfo(object):
    """
    所得税相关信息定义
    """

    def __init__(self, code, name, certificateType, idno, totalpayable):
        self._code = code
        self._name = name
        self._certificateType = certificateType
        self._idno = idno
        self._totalpayable = totalpayable
