#!/usr/bin/python
# -*- coding: gbk -*-
#encoding=gbk
#author=daimin


import os
import sys

from os.path import *
import codecs
import time
import re
import datetime
import MySQLdb

from config import *
from activity import *
from act_cls import *
from common import *
from vo_cls import *


class DbUtil:
    """
    #################数据库操作类###############
    """
    
    conn = None                           #数据库连接
    cur = None                            #数据库执行对象
    
    """今天、明天
    """
    curdate = None
    
    tomorrow = None
    
    parseday = None                      # 当前处理哪天的日志
    
    gcount = 0    
 
    gendates = []
    
    basic_userdata = None                 # 基础用户数据值类对象
    """在线用户数据
    """
    online_count = 0                      # 历史在线用户的日志的条数
    total_online_user = 0                 # 历史在线用户总量
    max_time = ['',0]                     # 当日在线用户量最大的时段，元素1是时间段表示，元素2是在线用户量
    min_time = ['',0]                     # 当日在线用户量最小的时段，元素1是时间段表示，元素2是在线用户量
     
    log_users = {}                        # 内建字典用于此次处理过程中的用户
    
    # 机器人统计数据
    # 元素分别是总局数、一副牌局数、两副牌局数、总赢局数、一副牌赢局数、两副牌赢局数、赢金钱、输金钱
    robot_count = [0,0,0,0,0,0]
    
    keepline_data = {}                    # 在线时间记录，记录不同的在线时间长度类别的用户量
    keepline_count = 0                    # 在线用户日志记录的条数
    
    
    #几个数组元素分别是总局数、一副牌局数、一副牌平均番、两副牌局数、两副牌平均番、押宝次数、机器人局数
    product_data_arr = [0,0,0,0,0,0,0]        # 产品数据统计记录
    
    #手机信息统计
    phone_info = {
        "network" : {},                            #联网方式，分别0：WIFI 1：3G 2：2G
        "android_version" : {},                    #版本类别
        "version":{},                              #游戏版本
        "mobile_type" : {},                        #设备型号
        "pixel"  : {},                             #分辨率
        "lang"   : {}                              #客户端语言
    }
    
    #用户等级数组
    '''
    1:门前乞丐
    2:赤贫雀奴
    3:雀街平民
    4:小馆雀友
    5:盈余雀手
    6:麻雀领班
    7:麻雀场主
    8:麻雀富豪
    9:麻雀富翁
    10:白金雀神
    '''
    user_grade_data = [0,0,0,0,0,0,0,0,0,0]
    
    pay_time = 0
    
    """
    麻将场级别设置
    0 # 自由直接对战
    1 # 自由直接对战(两副牌)
    2 # 新手场
    3 # 新手场(两副牌)
    4 # 初级场
    5 # 初级场(两副牌)
    6 # 中级场
    7 # 中级场(两副牌)
    8 # 高级场
    9 # 高级场(两副牌)
    10# 雀神场
    11# 雀神场(两副牌)
    """   
    fan_types = [0,1,2,3,4,5,6,7,8,9,10,11]
    
    #这里11个数组元素对应不同场次,子数组元素1是该场的番数总和，元素2该场的次数
    fan_daily_data = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
    
    fan_data_tile = [0,0,0,0]                # 番数数据，第一个记录两副牌的番数总数，第二个两副牌的记录总数，第三个记录一副牌的
    #                                          番数总数，第四个记录一副牌的记录数
    
   
    iap_users = {}                           # iap用户记录 分别记录 键为用户名加时间，值为金额
    
    iap_time = 0                             # iap付费次数
    
    sys_ecm_data = [0, 0]                    #系统收支情况(机器人),下面为数组，元素一为系统收入，元素二为系统支出

    
    IS_ADD = True                            #是否做累计，针对于可以累加的数据,根据命令行参数来判断，如果有命令行参数就不累加，否则累加


################################################## 函数 ##############################################################################


    def __init__(self, pday):
        """ 构造函数
            pday 参数进行处理的日志的日期
        """

        self.conn = self.get_conn()
        
        #默认每次都生成两天的数据
        now = datetime.datetime.now()
        
        self.curdate = now.strftime("%Y-%m-%d")
        self.gendates.append(now.strftime("%Y-%m-%d"))
        tomorr = now + datetime.timedelta(days = 1 )
        self.gendates.append(tomorr.strftime("%Y-%m-%d"))
        
        # 到底处理的是哪天的日志
        self.parseday = pday.strftime("%Y-%m-%d") 
        # 为确保处理日有初始记录生成，也尝试给处理日生成
        self.gendates.append(self.parseday)
        # 生成基础用户数据对象
        self.basic_userdata = BasicUserData()
        #初始化在线时间记录
        for ot in ONLINE_TIME_TYPES:
            self.keepline_data[ot] = [0,0]
        if len(sys.argv) > 1:
            self.IS_ADD = False
       
    def __del__( self ):
        """ 析构函数，关闭数据库连接
        """
        if self.conn != None:
            self.conn.close()       


    def get_conn(self) :
        """连接数据库
        """
        if self.conn == None:
            try: 
                self.conn = MySQLdb.connect(db = database, host = mysqlhost, user = username, passwd = password, charset="gbk", unix_socket="/var/lib/mysql/mysql.sock")
            except MySQLdb.Error,e:
                pk_log("Cannot connect to server")
                pk_log("Error code:", e.args[0])
                pk_log("Error message:", e.args[1])
                return 0
            
            return self.conn

    def update_date_tab(self):
        """ 更新所有和日期相关的表格
            #通过try...except语句抑制异常导致的程序退出
        """  

        # 生成所有分日统计的日条目
        for dd in self.gendates:
            # basic_userdata
            try:
                sql = "insert into basic_userdata(`date`,`install_num`,`reg_num`,`guest_num`,\
                `lead_reg`,`login_num`,`launch_time`) values('%s',0,0,0,0,0,0)" % (dd)
                self.cur.execute(sql)
            except:
                pk_log()
            # history_online
            try:    
                self.cur.execute("insert into history_online(`date`,`max_time`,`max_num`,\
                `min_time`,`min_num`,`ave_num`) values('%s',0,0,0,0,0)" % (dd))
            except:
                pk_log()
            
            # version_detail
            try: 
                # 查询所有的版本为每个版本都加一条
                self.cur.execute("select version from versions")
                for version in self.cur.fetchall():
                    self.cur.execute("insert into version_detail(`date`,`version`,`login_num`,\
                    `new_num`,`upgrade_num`,`imei_login_num`,`imei_new_num`,`imei_upgrade_num`)\
                    values('%s','%s',0,0,0,0,0,0)" % (dd, version[0]))
            except:
                pk_log()
            
            # online_time
            try: 
                for t in ONLINE_TIME_TYPES:
                    self.cur.execute("insert into online_time(`date`,`type`,`time_long`,`max_time`,`avg_time`) values('%s',%d,0,0,0)" % (dd,t))
            except:
                pk_log()
            #online_time_onetime
            try: 
                for t in ONLINE_TIME_TYPES:
                    self.cur.execute("insert into online_time_onetime(`date`,`type`,`time_long`) values('%s',%d,0)" % (dd,t))
            except:
                pk_log()
            # area_data
            try:
                self.cur.execute("select area from areas")
                for area in self.cur.fetchall():
                    self.cur.execute("insert into area_data(`date`,`area`,`user_num`)\
                    values('%s','%s',0)" % (dd, area[0]))
            except:
                pk_log()
            # product_data
            try:
                self.cur.execute("insert into product_data(`date`,`hand_num`,`one_hand_num`,`two_hand_num`,`bet_baby`,`robot_hand_num`)\
                values('%s',0,0,0,0,0)" % (dd))
            except:
                pk_log()
            # exception_data
            try:
                self.cur.execute("insert into exception_data(`date`,`offline_num`,`exception_time`,`offline_rate`)\
                values('%s',0,0,0.00)" % (dd))
            except:
                pk_log()
            # robot_data
            try:
                self.cur.execute("insert into robot_data(`date`,`total_hand`,`one_card`,`two_card`,`win_time`,`one_card_win`,`two_card_win`,\
                `win_gold`,`lose_gold`)values('%s',0,0,0,0,0,0,0,0)" % (dd))
            except:
                pk_log()
                
            """我们也许不需要在这里插入日手机信息
            # operators_data
            try:
                for opers in OPERATORS_TYPES:
                    self.cur.execute("insert into operators_data(`date`,`type`,`account_num`,`imei_num`)values('%s',%d,0,0)" % (dd, opers))
            except:
                pk_log()
            """
            """
            # network_data
            try:
                for nt in NETWORK_TYPES:
                    self.cur.execute("insert into network_data(`date`,`type`,`account_num`,`imei_num`)values('%s',%d,0,0)" % (dd, nt))
            except:
                pk_log()
            """
            """
            # android_data
            try:
                self.cur.execute("select os from os")
                for os in self.cur.fetchall():
                    self.cur.execute("insert into android_data(`date`,`os`,`account_num`,`imei_num`)values('%s','%s',0,0)" % (dd, os[0]))
            except:
                pk_log()
            """
            """
            # mobile_data
            try:
                self.cur.execute("select mobile from mobiles")
                for mb in self.cur.fetchall():
                    self.cur.execute("insert into android_data(`date`,`mobile`,`account_num`,`imei_num`)values('%s','%s',0,0)" % (dd, mb[0]))
            except:
                pk_log()
            """
            """
            # pixel_data
            try:
                self.cur.execute("select pixel from pixels")
                for px in self.cur.fetchall():
                    self.cur.execute("insert into pixel_data(`date`,`pixel`,`account_num`,`imei_num`)values('%s','%s',0,0)" % (dd, px[0]))
            except:
                pk_log()
            """
            # uid_data
            try:
                self.cur.execute("select uid from uids")
                for uid in self.cur.fetchall():
                    self.cur.execute("insert into uid_data(`date`,`uid`,`new_user`,`launch_time`,`total_user`,`login_user`,`imei_new_user`,\
                    `imei_launch_time`,`imei_login_user`,`imei_total_user`)values('%s','%s',0,0,0,0,0,0,0,0)" % (dd, uid[0]))
            except:
                pk_log()
            # basic_revenue_data
            try:
                self.cur.execute("insert into basic_revenue_data(`date`,`gain_gold`,`pay_num`,`pay_time`)values('%s',0,0,0)" % (dd))
            except:
                pk_log()
            # new_pay_user
            try:
                self.cur.execute("insert into new_pay_user(`date`,`new_num`)values('%s',0)" % (dd))
            except:
                pk_log()
            # retention_rate
            try:
                self.cur.execute("insert into retention_rate(`regdate`,`1_num`,`2_num`,`3_num`,`4_num`,`5_num`,\
                `6_num`,`7_num`,`8_num`\
                ) values('%s',0,0,0,0,0,0,0,0)" % (dd))
            except:
                pk_log()
            # fan_data
            try:
                for ft in  self.fan_types:
                    self.cur.execute("insert into fan_data(`date`,`type`,`total_fan`,`round_nums`) values('%s',%d,0,0)" % (dd,ft))
            except:
                pk_log()
            #total_fan_data
            try:
                self.cur.execute("insert into total_fan_data(`date`,`two_fan`,`two_count`,`one_fan`,`one_count`) values('%s',0,0,0,0)" % (dd,ft))
            except:
                pk_log()
        
           

    def update(self, objs):
        """ 更新数据
        #注意！我们的log记录的是昨天的数据
        """
        if self.conn <> None:
            self.cur = self.conn.cursor()
            self.update_date_tab()

            self.first_update()
            for ao in objs:
                if ao == None:
                    continue
                self.update_userinfo(ao)
                self.history_online(ao)
                self.online_time(ao)
                self.product_data(ao)
                self.user_grade(ao)
                self.goldboard(ao)
                self.robot_data(ao)
                self.update_iap_data(ao)
                self.update_economic(ao)
                
            self.last_update()
            self.cur.close()
    '''
    #################################具体的更新数据表代码###########################################
    '''
    def update_userinfo(self, tobj):
        '''
        需要处理两个表userinfo
        '''
        if tobj.TAG == ACT_REGISTER:
            #查询改ID是否存在
            iqreg = int(tobj.regType)
            if iqreg == 1:
                self.basic_userdata.guest_num = self.basic_userdata.guest_num + 1
            if self.is_new_user(tobj) == True:
                self.basic_userdata.reg_num = self.basic_userdata.reg_num + 1
            #更新用户渠道
            self.update_channel(tobj.userName,tobj.channel)
            # 需要androidid每次安装后都生成不同的
            if self.is_new_install(tobj.uniqueID) == True:
                self.basic_userdata.install_num = self.basic_userdata.install_num + 1
            try:
                #userinfo
                if iqreg != 1:  # 只有QQ注册用户不算正式用户，不入库，其它的都入库
                    sql = "insert into userinfo(`androidid`,`username`,`nickname`,`sex`,`gold`,\
                    `total_pay`,`qreg`,`channel`,`reg_date`) values('%s','%s','%s',%d,'%s','0',%d,'%s','%s')"\
                    % (tobj.uniqueID, tobj.userName, tobj.nickName, int(tobj.sex), tobj.money, \
                    iqreg,tobj.channel, self.parseday)
                    self.cur.execute(sql)
                    #注册用户也算一个登陆用户
                    if self.is_logined(tobj.userName) == False:
                        self.basic_userdata.login_num = self.basic_userdata.login_num + 1
                        if self.log_users.has_key(tobj.userName):
                            lu = self.log_users[tobj.userName]
                        else:
                            lu = LogUser()
                        lu.is_logined = True

                    #userinfo_imei
                    sql = "insert into userinfo_imei(`androidid`,`username`,`nickname`,`sex`,`gold`,\
                    `total_pay`,`qreg`,`reg_date`) values('%s','%s','%s',%d,'%s','0',%d,'%s')"\
                    % (tobj.uniqueID, tobj.userName, tobj.nickName, int(tobj.sex), tobj.money, \
                    iqreg, self.parseday)
                    self.cur.execute(sql)

            except:
                pk_log()
        if tobj.TAG == ACT_LOGIN:
            if self.is_robot(tobj.userName) == False:
                self.basic_userdata.launch_time = self.basic_userdata.launch_time + 1
                if self.is_logined(tobj.userName) == False:
                    if int(tobj.regType) <> 1:                             #登陆用户中去掉快速注册用户
                        self.basic_userdata.login_num = self.basic_userdata.login_num + 1
                        if self.log_users.has_key(tobj.userName):
                            lu = self.log_users[tobj.userName]
                        else:
                            lu = LogUser()
                        lu.is_logined = True
                        #保存客户端信息
                        
                        if self.phone_info['network'].has_key(tobj.netInfo):
                            self.phone_info['network'][tobj.netInfo] = self.phone_info['network'][tobj.netInfo] + 1
                        else:
                            self.phone_info['network'][tobj.netInfo] = 1
                        
                        if self.phone_info['android_version'].has_key(tobj.oSInfo):
                            self.phone_info['android_version'][tobj.oSInfo] = self.phone_info['android_version'][tobj.oSInfo] + 1
                        else:
                            self.phone_info['android_version'][tobj.oSInfo] = 1
                            
                        if self.phone_info['pixel'].has_key(tobj.resInfo):
                            self.phone_info['pixel'][tobj.resInfo] = self.phone_info['pixel'][tobj.resInfo] + 1
                        else:
                            self.phone_info['pixel'][tobj.resInfo] = 1
                            
                        if self.phone_info['version'].has_key(tobj.versionString):
                            self.phone_info['version'][tobj.versionString] = self.phone_info['version'][tobj.versionString] + 1
                        else:
                            self.phone_info['version'][tobj.versionString] = 1
                            
                        if self.phone_info['mobile_type'].has_key(tobj.machineNo):
                            self.phone_info['mobile_type'][tobj.machineNo] = self.phone_info['mobile_type'][tobj.machineNo] + 1
                        else:
                            self.phone_info['mobile_type'][tobj.machineNo] = 1
                            
                        if self.phone_info['lang'].has_key(tobj.systemLang):
                            self.phone_info['lang'][tobj.systemLang] = self.phone_info['lang'][tobj.systemLang] + 1
                        else:
                            self.phone_info['lang'][tobj.systemLang] = 1
                            
                        """
                        lu.network = tobj.netInfo
                        lu.android_version = tobj.oSInfo
                        lu.pixel = tobj.resInfo
                        lu.mobile_type = tobj.machineNo
                        lu.lang = tobj.systemLang
                        lu.version = tobj.versionString
                        """
                        
                        self.log_users[tobj.userName] = lu
            #更新排行榜中的最后登录时间
            self.updatePayBoardLoginTime(tobj.userName, tobj.login_time) 
                
            
    def history_online(self, tobj):
        """统计历史在线人数
        """
        if tobj.TAG == ACT_ONLINE:
            self.split_honline(tobj.time,tobj.users)
              
    def online_time(self, tobj):
        """统计用户在线时长  
        """
        if tobj.TAG == ACT_KEEPTIME:
            #print tobj.keepTime
            if self.is_robot(tobj.userName) == False:
                self.get_keepTime(tobj.userName,tobj.dateTimeNow, tobj.keepTime)
    
            
    def product_data(self, tobj):
        """统计产品数据
        """
        if tobj.TAG == ACT_GAMERESULT:
            self.get_product_data(tobj.round, tobj.tile_count, tobj.AIFlag, int(tobj.totalfan))
   
    def user_grade(self, tobj):
        """统计用户等级
        """
        if tobj.TAG == ACT_ONE_RESULT:
            title = int(tobj.title)
            #更新userinfo表的title字段
            sql = "update userinfo set title=%d where username='%s'" % (title,tobj.userName)
            self.cur.execute(sql)
            #不需要收集用户等级信息
            #if self.log_users.has_key(tobj.userName) == True:
            #    self.log_users[tobj.userName].grade = tobj.title
            #else:
            #    lu = LogUser()
            #    lu.grade = tobj.title
            #    self.log_users[tobj.userName] = lu 
        
    
    def goldboard(self, tobj):
        """统计金币排行榜
        """
        if tobj.TAG == ACT_RANK:
            sql = "replace into goldboard(nickname,username,'gold') values('%s','%s','%s')" % (tobj.nickName,tobj.userName, tobj.mney)
            self.cur.execute(sql)
            
    def robot_data(self, tobj):
        """统计机器人数据
        """
        if tobj.TAG == ACT_GAMERESULT: 
            #必须是AI局
            AIFlag = int(tobj.AIFlag)
            tileCount = int(tobj.tile_count)
            if AIFlag > 0:
                self.robot_count[0] = self.robot_count[0] + int(tobj.round)
                if tileCount == 1:
                    self.robot_count[1] = self.robot_count[1] + int(tobj.round)
                if tileCount == 2:
                    self.robot_count[2] = self.robot_count[2] + int(tobj.round)
                #赢方AI
                if AIFlag == 1:
                    self.robot_count[3] = self.robot_count[3] + int(tobj.round)
                    if tileCount == 1:
                        self.robot_count[4] = self.robot_count[4] + int(tobj.round)
                    if tileCount == 2:
                        self.robot_count[5] = self.robot_count[5] + int(tobj.round)


    def update_iap_data(self,tobj):
        """更新iap相关的数据
        """
        if tobj.TAG == ACT_IAP:
            #判断这条记录是否已经处理过了
            
            pid = tobj.getPid(tobj)
            
            self.iap_time = self.iap_time + 1
            #采用新的字段来得到金钱
            money = int(tobj.money)
            
            rmbmoney = float(tobj.price)
            #print "username=%s, money=%f" % (tobj.userName, rmbmoney)
            #gold,pay_time,total_pay在userinfo中
            sql = "update userinfo set pay_time=pay_time+1,gold=%d,total_pay=total_pay+%f where username='%s'"\
             % (int(tobj.userNewMney),rmbmoney,tobj.userName)
            self.cur.execute(sql)
            
            if self.IsNewPayUser(tobj.userName,self.parseday) == True:
                sql = "update  new_pay_user set new_num=new_num+1 where `date`='%s'" %(self.parseday)
                self.cur.execute(sql)
            #插入pay_detail
            
            sql = "replace into pay_detail(pid,username,nickname,paytime,mney) values('%s','%s','%s','%s',%f)" % (pid,tobj.userName,tobj.nickName,tobj.iap_time,rmbmoney)
            self.cur.execute(sql)
            if self.IS_ADD == True:
                sql = "select count(username) as pcount from payboard where pid='%s'" %(pid)
                self.cur.execute(sql)
                pcount = self.cur.fetchone()
                if pcount <> None:
                    if int(pcount[0]) <= 0:
                        sql = "select count(username) as ucount from payboard where username='%s'" % (tobj.userName)
                        self.cur.execute(sql)
                        ucount = self.cur.fetchone()
                        if ucount <> None:
                            if int(ucount[0]) <= 0:
                                sql = "insert into payboard(`pid`,`username`,`nickname`,`mney`,`first_pay_time`) values('%s','%s','%s',%f,'%s')" %(pid,tobj.userName,tobj.nickName,rmbmoney,self.parseday)
                            else:
                                sql = "update payboard set mney=mney+%f where username='%s'" %(rmbmoney, tobj.userName)
                        self.cur.execute(sql)
            
            if self.iap_users.has_key(tobj.userName) == False:
                self.iap_users[tobj.userName] = rmbmoney
            else:
                self.iap_users[tobj.userName] = self.iap_users[tobj.userName] + rmbmoney
            
    
    def update_economic(self, tobj):
        """统和玩家金钱收支记录数据更新
        """
        if tobj.TAG == ACT_ECONOMIC_LOG:
            itype = int(tobj.type)
            if itype == ECONOMIC_INCOME:
                self.sys_ecm_data[0] = self.sys_ecm_data[0] + int(tobj.amount)
            elif itype == ECONOMIC_EXPEND:
                self.sys_ecm_data[1] = self.sys_ecm_data[1] + int(tobj.amount)
    
            
    """
    
    ###########################################################################################################
    
    """
   
    def first_update(self):
        """在更新前做的重置数据工作
        """
        # new_pay_user当天记录清零
        self.cur.execute("update new_pay_user set new_num=0,new_reg_num=0 where `date`='%s'" %(self.parseday)) 
    
    def last_update(self):
        """结果汇总
        """
        #更新 basic_userdata
        sql = "update basic_userdata set install_num=%d,reg_num=%d,guest_num=%d,lead_reg=%d,login_num=%d,LAUNCH_TIME=%d where date='%s'"\
        % (self.basic_userdata.install_num,self.basic_userdata.reg_num-self.basic_userdata.guest_num,self.basic_userdata.guest_num,self.basic_userdata.lead_reg,\
        self.basic_userdata.login_num,self.basic_userdata.launch_time,self.parseday)
        self.cur.execute(sql)
        
        #记录最后的历史在线人数 
        self.count_honline()
        #记录最后的在线时间
        self.count_keeptime()
        #记录最后的产品数据
        self.count_product_data()
        #只保留金币榜中前500名
        self.count_goldboard()
        #统计用户等级
        self.count_user_grade()
        #统计机器人数据
        self.count_robot_data()
        #更新每天的运营数据
        self.count_iap_data()
        #更新系统收支日志数据
        self.count_economic()
        #更新手机信"
        self.count_phoneinfo()
        #统计留存率
        self.count_retention_rate()

    
    def count_honline(self):
        """统计历史在线
        """
        ave = round(self.total_online_user / self.online_count)
        self.cur.execute("update history_online set `max_time`='%s',`max_num`=%d,`min_time`='%s',`min_num`=%d,`ave_num`=%d \
                  where `date`='%s'" % (self.max_time[0],self.max_time[1],self.min_time[0],self.min_time[1],ave,self.parseday))
        
         
    def count_keeptime(self):
        """汇总统计使用时间
        #计算每日使用时间
        """
        idx = 1
        for kk in self.keepline_data:
            kd = self.keepline_data[kk][0]
            tl = self.keepline_data[kk][1]
            sql = "update online_time set time_long=%d,time_count=%d where `date`='%s' and `type`=%d " % (tl,kd, self.parseday,idx)
            self.cur.execute(sql)
            idx = idx + 1
        #计算单次使用时间
        sum_time = 0 
        max_time = 0
        user_count = 0
       
        for lk in self.log_users:
            if self.is_robot(lk) == True:
                continue
            lu = self.log_users[lk]
            
            avetime = 0
            user_count = user_count + 1
            if lu.use_time > 0:
                avetime = lu.time_long / lu.use_time
            if lu.time_long > max_time:
                max_time = lu.time_long
            sum_time = sum_time + lu.time_long
            ttype = self.get_keeptime_type(avetime)
            
            sql = "update online_time_onetime set time_count=time_count+1,time_long=time_long+%d where `date`='%s' and `type`=%d" % (avetime,self.parseday,ttype)
            self.cur.execute(sql)
        avg_time = round(sum_time / self.keepline_count)
        sql = "update online_time set max_time=%d,avg_time=%d where `date`='%s'" % (max_time,avg_time,self.parseday)
        self.cur.execute(sql)
        
    
    def count_product_data(self):
        """汇总统计产品数据
        """
        # 总局数、一副牌局数、一副牌平均番、两副牌局数、两副牌平均番、押宝次数、机器人局数
        sql = "update product_data set hand_num=%d,one_hand_num=%d,one_hand_fan=%s,two_hand_num=%d,two_hand_fan=%s,bet_baby=%d,robot_hand_num=%d where `date`='%s'" \
        % (self.product_data_arr[0],self.product_data_arr[1],"%.2f" % (round(self.product_data_arr[2]/self.product_data_arr[1])),self.product_data_arr[3],"%.2f" % (round(self.product_data_arr[4]/self.product_data_arr[3])),self.product_data_arr[5],self.product_data_arr[6],self.parseday)
        self.cur.execute(sql)
    
    def count_goldboard(self):
        """汇总处理金币排行榜
        """
        sql = "select gold from goldboard order by gold desc limit 500,1"
        self.cur.execute(sql)
        row = self.cur.fetchone()
        if row :
            sql = "delete from goldboard where gold < '%s'" % (row[0])
            self.cur.execute(sql)
        
    
    def count_user_grade(self):
        """汇总处理用户等级分布
        """
        pass
        #不需要统计用户等级，直接从userinfo中读取即可
        #得到self.user_grade_data
        #for lk in self.log_users:
        #    lu = self.log_users[lk]
        #    title = int(lu.grade)
        #    if title == 0:
        #        continue
        #    title = title - 1
        #    self.user_grade_data[title] = self.user_grade_data[title] + 1
        #idx = 1
        #先将之前的清空
        #self.cur.execute("update user_grade set num=0")
        #for ug in self.user_grade_data:
        #    sql = "update user_grade set num=num+%d where grade=%d" % (ug, idx)
        #    self.cur.execute(sql)
        #    idx = idx + 1
    
    def count_robot_data(self):
        """汇总机器人数据
        """
        sql = "update robot_data set total_hand=%d,one_card=%d,two_card=%d,win_time=%d,one_card_win=%d,two_card_win=%d\
         where `date`='%s'" % (self.robot_count[0],self.robot_count[1],self.robot_count[2],\
        self.robot_count[3],self.robot_count[4],self.robot_count[5],self.parseday)
        self.cur.execute(sql)
    
    def count_iap_data(self):
        """汇总IAP结果
        """
        pay_num = len(self.iap_users)
        mny = 0
        #修改userinfo中的gold
        for kn in self.iap_users:
            mny = mny + self.iap_users[kn]
        #rmb = GameMoney2RMB(mny)
        rmb = mny
        sql = "update basic_revenue_data set gain_gold=%d,pay_num=%d,pay_time=%d where `date`='%s'" %(rmb,pay_num,self.iap_time,self.parseday)
        self.cur.execute(sql)
        
        #得到付费用户的等级
        #先置0
        self.cur.execute("update pay_user_grade set num=0")
        sql = "select title from userinfo where pay_time > 0"
        self.cur.execute(sql)
        for title  in self.cur.fetchall():
            title = int(title[0])
            sql = "update pay_user_grade set num=num+1 where grade=%d" %(title + 1)
            self.cur.execute(sql)
        
        #更新得到首日的注册用户的值
        sql = "select c.reg_date, count(c.reg_date) as rnum from (select a.reg_date,a.username from userinfo a inner join\
            ( select distinct DATE_FORMAT(paytime,'%Y-%m-%d') as paydate,username from pay_detail) b on a.reg_date=b.paydate and \
            a.username=b.username) c group by c.reg_date;"
        self.cur.execute(sql)
        for reg_date,rnum in self.cur.fetchall():
            self.cur.execute("update new_pay_user set new_reg_num=%d where `date`='%s'" %(rnum,reg_date.strftime("%Y-%m-%d")))
                
    def count_phoneinfo(self):
        #更新手机信息的相关的表格
        try: 
            for nw in self.phone_info['network']:
                self.cur.execute("replace into networks(`network`) values('%s')" % (nw))
            
            for os in self.phone_info['android_version']:
                self.cur.execute("replace into os(`os`) values('%s')" % (os))

            for ver in self.phone_info['version']:
                self.cur.execute("replace into versions(`version`) values('%s')" % (ver))
            
            for mt in self.phone_info['mobile_type']:
                self.cur.execute("replace into mobiles(`mobile`) values('%s')" % (mt))        

            for px in self.phone_info['pixel']:
                self.cur.execute("replace into pixels(`pixel`) values('%s')" % (px))        

            for l in self.phone_info['lang']:
                self.cur.execute("replace into langs(`lang`) values('%s')" % (l))        
        except:
            pk_log()
        #更新手机信息日统计表格
        for dd in self.gendates:
                
                try:
                    self.cur.execute("select network from networks")
                    for nw in self.cur.fetchall():
                        self.cur.execute("insert into network_data(`date`,`type`,`account_num`,`imei_num`)values('%s','%s',0,0)" % (dd, nw[0]))
                except:
                    pk_log()
                    
                try:
                    self.cur.execute("select os from os")
                    for os in self.cur.fetchall():
                        self.cur.execute("insert into android_data(`date`,`os`,`account_num`,`imei_num`)values('%s','%s',0,0)" % (dd, os[0]))
                except:
                    pk_log()
                try:
                    self.cur.execute("select mobile from mobiles")
                    for mb in self.cur.fetchall():
                        self.cur.execute("insert into mobile_data(`date`,`mobile`,`account_num`,`imei_num`)values('%s','%s',0,0)" % (dd, mb[0]))
                except:
                    pk_log()
           
                try:
                    self.cur.execute("select pixel from pixels")
                    for px in self.cur.fetchall():
                        self.cur.execute("insert into pixel_data(`date`,`pixel`,`account_num`,`imei_num`)values('%s','%s',0,0)" % (dd, px[0]))
                except:
                    pk_log()
                    
                try:
                    self.cur.execute("select lang from langs")
                    for px in self.cur.fetchall():
                        self.cur.execute("insert into lang_data(`date`,`lang`,`account_num`,`imei_num`)values('%s','%s',0,0)" % (dd, px[0]))
                except:
                    pk_log()
                    
        #开始插入各自的数据
        for nw in self.phone_info['network']:
            num = self.phone_info['network'][nw]
            try:
                self.cur.execute("update network_data set account_num=%d where `date`='%s' and `type`='%s'" % (num, self.parseday,nw) )
            except:
                pk_log()
            
        for av in self.phone_info['android_version']:
            num = self.phone_info['android_version'][av]
            try:
                self.cur.execute("update android_data set account_num=%d where `date`='%s' and `os`='%s'" % (num, self.parseday,av) )
            except:
                pk_log()
            
        for mt in self.phone_info['mobile_type']:
            num = self.phone_info['mobile_type'][mt]
            try:
                self.cur.execute("update mobile_data set account_num=%d where `date`='%s' and `mobile`='%s'" % (num, self.parseday,mt) )
            except:
                pk_log()
        for px in self.phone_info['pixel']:
            num = self.phone_info['pixel'][px]
            self.cur.execute("update pixel_data set account_num=%d where `date`='%s' and `pixel`='%s'" % (num, self.parseday,px) )
            
        for lang in self.phone_info['lang']:
            num = self.phone_info['lang'][lang]
            self.cur.execute("update lang_data set account_num=%d where `date`='%s' and `lang`='%s'" % (num, self.parseday,lang) )

                
           
                
    """
    
    #################################工具类方法###################################################
    
    """

    def is_logined(self, userName):
        """用户已登录
        """
        if self.log_users.has_key(userName) == True:
            lu = self.log_users[userName]
            if lu.is_logined == True:
                return True
        return False
        
    
    def is_new_user(self, userName):
        """判断是否是新用户
        """
        self.cur.execute("select count(id) from userinfo where username='%s'" % (userName))
        row = self.cur.fetchone()
        if row:
            if int(row[0]) <= 0:
                return True
        return False
        
    def is_new_install(self, androidid):
        """判断是否是新安装的用户
        """
        self.cur.execute("select count(id) from userinfo_imei where androidid='%s'" % (androidid))
        row = self.cur.fetchone()
        if row:
            if int(row[0]) <= 0:
                return True
        return False
        
    def split_honline(self,ti,usernum):
        """拆分历史在线并作处理
        """
        usernum = int(usernum)
        self.total_online_user = self.total_online_user + usernum
        self.online_count = self.online_count + 1
        if self.max_time[1] < usernum:
            self.max_time[0] = ti
            self.max_time[1] = usernum
        if self.min_time[1] == 0:
            self.min_time[1] = usernum
            self.min_time[0] = ti
        else:
            if self.min_time[1] > usernum :
                self.min_time[1] = usernum
                self.min_time[0] = ti
                           
    def get_keepTime(self,userName, dateTimeNow, keepTime):
        """获取游戏时间长度
        """
        keepTime = round(float(keepTime))
        self.keepline_count = self.keepline_count + 1
        if keepTime < 60:
            self.keepline_data[1][0] = self.keepline_data[1][0] + 1
            self.keepline_data[1][1] = self.keepline_data[1][1] + keepTime
        elif keepTime >= 60 and keepTime < 5 * 60:
            self.keepline_data[2][0] = self.keepline_data[2][0] + 1
            self.keepline_data[2][1] = self.keepline_data[2][1] + keepTime
        elif keepTime >= 5 * 60 and keepTime < 10 * 60:
            self.keepline_data[3][0] = self.keepline_data[3][0] + 1
            self.keepline_data[3][1] = self.keepline_data[3][1] + keepTime
        elif keepTime >= 10 * 60 and keepTime < 30 * 60:
            self.keepline_data[4][0] = self.keepline_data[4][0] + 1
            self.keepline_data[4][1] = self.keepline_data[4][1] + keepTime
        elif keepTime >= 30 * 60 and keepTime < 60 * 60:
            self.keepline_data[5][0] = self.keepline_data[5][0] + 1
            self.keepline_data[5][1] = self.keepline_data[5][1] + keepTime
        elif keepTime >= 60 * 60 and keepTime < 2 * 60 * 60:
            self.keepline_data[6][0] = self.keepline_data[6][0] + 1
            self.keepline_data[6][1] = self.keepline_data[6][1] + keepTime
        elif keepTime >= 2 * 60 * 60 and keepTime < 4 * 60 * 60:
            self.keepline_data[7][0] = self.keepline_data[7][0] + 1
            self.keepline_data[7][1] = self.keepline_data[7][1] + keepTime
        elif keepTime >= 4 * 60 * 60 and keepTime < 6 * 60 * 60:
            self.keepline_data[8][0] = self.keepline_data[8][0] + 1
            self.keepline_data[8][1] = self.keepline_data[8][1] + keepTime
        elif keepTime >= 6 * 60 * 60:
            self.keepline_data[9][0] = self.keepline_data[9][0] + 1
            self.keepline_data[9][1] = self.keepline_data[9][1] + keepTime
        
        if self.log_users.has_key(userName) == False:
            self.log_users[userName] = LogUser()
        self.log_users[userName].use_time = self.log_users[userName].use_time + 1
        self.log_users[userName].time_long = self.log_users[userName].time_long + keepTime
    
   
       
    def get_keeptime_type(self, time_long):
        """获得具体的保存类型长度
        """
        ttype = 0
        if time_long < 60:
            ttype = 1
        elif time_long >= 60 and time_long < 5 * 60:
            ttype = 2
        elif time_long >= 5 * 60 and time_long < 10 * 60:
            ttype = 3
        elif time_long >= 10 * 60 and time_long < 30 * 60:
            ttype = 4
        elif time_long >= 30 * 60 and time_long < 60 * 60:
            ttype = 5
        elif time_long >= 60 * 60 and time_long < 2 * 60 * 60:
            ttype = 6
        elif time_long >= 2 * 60 * 60 and time_long < 4 * 60 * 60:
            ttype = 7
        elif time_long >= 4 * 60 * 60 and time_long < 6 * 60 * 60:
            ttype = 8
        elif time_long >= 6 * 60 * 60:
            ttype = 9
        return ttype
    
    def get_product_data(self,dround, tile_count, AIFlag,total_fan):
        """获取产品数据
        """
        #dround = int(dround)
        AIFlag = int(AIFlag)
        tile_count = int(tile_count)
        # 总局数、一副牌局数、一副牌平均番、两副牌局数、两副牌平均番、押宝次数、机器人局数
        self.product_data_arr[0] = self.product_data_arr[0] + 1
        if AIFlag <> 0:
            self.product_data_arr[6] = self.product_data_arr[6] + 1
        if tile_count == 1:
            self.product_data_arr[1] = self.product_data_arr[1] + 1
            self.product_data_arr[2] = self.product_data_arr[2] + total_fan
        if tile_count == 2:
            self.product_data_arr[3] = self.product_data_arr[3] + 1
            self.product_data_arr[4] = self.product_data_arr[4] + total_fan
       
        
    def is_robot(self,userName):
        """根据用户名判断该用户是否是机器人
        """
        if userName.find(ROBOT_NAME_PREFIX) == -1:
            return False
        return True  
    
    def IsNewPayUser(self,userName,paytime): 
        """根据用户名判断是否是新付费用户
        """
        sql = "select count(username) as pycount from payboard where username='%s' and first_pay_time<'%s'" % (userName, paytime)
        self.cur.execute(sql)           
        pycount = self.cur.fetchone()
        if pycount <> None:
            if int(pycount[0]) <= 0:
                return True
        return False
    
    def updatePayBoardLoginTime(self,userName,logintime):
        """更新支付排行榜的最后登录时间
        """
        sql = "update payboard set last_login='%s' where username='%s'" % (logintime,userName)
        self.cur.execute(sql)

    def count_economic(self):
        """更新系统收支记录数据
        """
        sql = "update robot_data set win_gold='%s',lose_gold='%d' where `date`='%s'"\
         % (self.sys_ecm_data[0], self.sys_ecm_data[1], self.parseday)
        self.cur.execute(sql)
        
    def count_retention_rate(self):
        """计算留存率
        """
        if self.IS_ADD == False:
            return
        pdate = datetime.datetime.strptime(self.parseday, "%Y-%m-%d")
        for st in range(1,9):
            cdate = pdate - datetime.timedelta(days = st )
            csdate =  cdate.strftime("%Y-%m-%d")
            query = "select username from userinfo where reg_date='%s'" % (csdate)
            self.cur.execute(query)
            for username  in self.cur.fetchall():
                if self.log_users.has_key(username[0]):
                    wrage = "%d_num" % (st)
                    sql = "update retention_rate set %s=%s+1 where regdate='%s'" % (wrage,wrage, csdate)
                    self.cur.execute(sql)            
    
    def update_channel(self,username,channel):
        """更新用户渠道
        """
        sql = "update userinfo set channel='%s' where username='%s'" % (channel,username)
        self.cur.execute(sql)
            
        
    
    
    
    

    

   
    
