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
    #################���ݿ������###############
    """
    
    conn = None                           #���ݿ�����
    cur = None                            #���ݿ�ִ�ж���
    
    """���졢����
    """
    curdate = None
    
    tomorrow = None
    
    parseday = None                      # ��ǰ�����������־
    
    gcount = 0    
 
    gendates = []
    
    basic_userdata = None                 # �����û�����ֵ�����
    """�����û�����
    """
    online_count = 0                      # ��ʷ�����û�����־������
    total_online_user = 0                 # ��ʷ�����û�����
    max_time = ['',0]                     # ���������û�������ʱ�Σ�Ԫ��1��ʱ��α�ʾ��Ԫ��2�������û���
    min_time = ['',0]                     # ���������û�����С��ʱ�Σ�Ԫ��1��ʱ��α�ʾ��Ԫ��2�������û���
     
    log_users = {}                        # �ڽ��ֵ����ڴ˴δ��������е��û�
    
    # ������ͳ������
    # Ԫ�طֱ����ܾ�����һ���ƾ����������ƾ�������Ӯ������һ����Ӯ������������Ӯ������Ӯ��Ǯ�����Ǯ
    robot_count = [0,0,0,0,0,0]
    
    keepline_data = {}                    # ����ʱ���¼����¼��ͬ������ʱ�䳤�������û���
    keepline_count = 0                    # �����û���־��¼������
    
    
    #��������Ԫ�طֱ����ܾ�����һ���ƾ�����һ����ƽ�����������ƾ�����������ƽ������Ѻ�������������˾���
    product_data_arr = [0,0,0,0,0,0,0]        # ��Ʒ����ͳ�Ƽ�¼
    
    #�ֻ���Ϣͳ��
    phone_info = {
        "network" : {},                            #������ʽ���ֱ�0��WIFI 1��3G 2��2G
        "android_version" : {},                    #�汾���
        "version":{},                              #��Ϸ�汾
        "mobile_type" : {},                        #�豸�ͺ�
        "pixel"  : {},                             #�ֱ���
        "lang"   : {}                              #�ͻ�������
    }
    
    #�û��ȼ�����
    '''
    1:��ǰ��ؤ
    2:��ƶȸū
    3:ȸ��ƽ��
    4:С��ȸ��
    5:ӯ��ȸ��
    6:��ȸ���
    7:��ȸ����
    8:��ȸ����
    9:��ȸ����
    10:�׽�ȸ��
    '''
    user_grade_data = [0,0,0,0,0,0,0,0,0,0]
    
    pay_time = 0
    
    """
    �齫����������
    0 # ����ֱ�Ӷ�ս
    1 # ����ֱ�Ӷ�ս(������)
    2 # ���ֳ�
    3 # ���ֳ�(������)
    4 # ������
    5 # ������(������)
    6 # �м���
    7 # �м���(������)
    8 # �߼���
    9 # �߼���(������)
    10# ȸ��
    11# ȸ��(������)
    """   
    fan_types = [0,1,2,3,4,5,6,7,8,9,10,11]
    
    #����11������Ԫ�ض�Ӧ��ͬ����,������Ԫ��1�Ǹó��ķ����ܺͣ�Ԫ��2�ó��Ĵ���
    fan_daily_data = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
    
    fan_data_tile = [0,0,0,0]                # �������ݣ���һ����¼�����Ƶķ����������ڶ��������Ƶļ�¼��������������¼һ���Ƶ�
    #                                          �������������ĸ���¼һ���Ƶļ�¼��
    
   
    iap_users = {}                           # iap�û���¼ �ֱ��¼ ��Ϊ�û�����ʱ�䣬ֵΪ���
    
    iap_time = 0                             # iap���Ѵ���
    
    sys_ecm_data = [0, 0]                    #ϵͳ��֧���(������),����Ϊ���飬Ԫ��һΪϵͳ���룬Ԫ�ض�Ϊϵͳ֧��

    
    IS_ADD = True                            #�Ƿ����ۼƣ�����ڿ����ۼӵ�����,���������в������жϣ�����������в����Ͳ��ۼӣ������ۼ�


################################################## ���� ##############################################################################


    def __init__(self, pday):
        """ ���캯��
            pday �������д�������־������
        """

        self.conn = self.get_conn()
        
        #Ĭ��ÿ�ζ��������������
        now = datetime.datetime.now()
        
        self.curdate = now.strftime("%Y-%m-%d")
        self.gendates.append(now.strftime("%Y-%m-%d"))
        tomorr = now + datetime.timedelta(days = 1 )
        self.gendates.append(tomorr.strftime("%Y-%m-%d"))
        
        # ���״��������������־
        self.parseday = pday.strftime("%Y-%m-%d") 
        # Ϊȷ���������г�ʼ��¼���ɣ�Ҳ���Ը�����������
        self.gendates.append(self.parseday)
        # ���ɻ����û����ݶ���
        self.basic_userdata = BasicUserData()
        #��ʼ������ʱ���¼
        for ot in ONLINE_TIME_TYPES:
            self.keepline_data[ot] = [0,0]
        if len(sys.argv) > 1:
            self.IS_ADD = False
       
    def __del__( self ):
        """ �����������ر����ݿ�����
        """
        if self.conn != None:
            self.conn.close()       


    def get_conn(self) :
        """�������ݿ�
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
        """ �������к�������صı���
            #ͨ��try...except��������쳣���µĳ����˳�
        """  

        # �������з���ͳ�Ƶ�����Ŀ
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
                # ��ѯ���еİ汾Ϊÿ���汾����һ��
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
                
            """����Ҳ������Ҫ������������ֻ���Ϣ
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
        """ ��������
        #ע�⣡���ǵ�log��¼�������������
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
    #################################����ĸ������ݱ�����###########################################
    '''
    def update_userinfo(self, tobj):
        '''
        ��Ҫ����������userinfo
        '''
        if tobj.TAG == ACT_REGISTER:
            #��ѯ��ID�Ƿ����
            iqreg = int(tobj.regType)
            if iqreg == 1:
                self.basic_userdata.guest_num = self.basic_userdata.guest_num + 1
            if self.is_new_user(tobj) == True:
                self.basic_userdata.reg_num = self.basic_userdata.reg_num + 1
            #�����û�����
            self.update_channel(tobj.userName,tobj.channel)
            # ��Ҫandroididÿ�ΰ�װ�����ɲ�ͬ��
            if self.is_new_install(tobj.uniqueID) == True:
                self.basic_userdata.install_num = self.basic_userdata.install_num + 1
            try:
                #userinfo
                if iqreg != 1:  # ֻ��QQע���û�������ʽ�û�������⣬�����Ķ����
                    sql = "insert into userinfo(`androidid`,`username`,`nickname`,`sex`,`gold`,\
                    `total_pay`,`qreg`,`channel`,`reg_date`) values('%s','%s','%s',%d,'%s','0',%d,'%s','%s')"\
                    % (tobj.uniqueID, tobj.userName, tobj.nickName, int(tobj.sex), tobj.money, \
                    iqreg,tobj.channel, self.parseday)
                    self.cur.execute(sql)
                    #ע���û�Ҳ��һ����½�û�
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
                    if int(tobj.regType) <> 1:                             #��½�û���ȥ������ע���û�
                        self.basic_userdata.login_num = self.basic_userdata.login_num + 1
                        if self.log_users.has_key(tobj.userName):
                            lu = self.log_users[tobj.userName]
                        else:
                            lu = LogUser()
                        lu.is_logined = True
                        #����ͻ�����Ϣ
                        
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
            #�������а��е�����¼ʱ��
            self.updatePayBoardLoginTime(tobj.userName, tobj.login_time) 
                
            
    def history_online(self, tobj):
        """ͳ����ʷ��������
        """
        if tobj.TAG == ACT_ONLINE:
            self.split_honline(tobj.time,tobj.users)
              
    def online_time(self, tobj):
        """ͳ���û�����ʱ��  
        """
        if tobj.TAG == ACT_KEEPTIME:
            #print tobj.keepTime
            if self.is_robot(tobj.userName) == False:
                self.get_keepTime(tobj.userName,tobj.dateTimeNow, tobj.keepTime)
    
            
    def product_data(self, tobj):
        """ͳ�Ʋ�Ʒ����
        """
        if tobj.TAG == ACT_GAMERESULT:
            self.get_product_data(tobj.round, tobj.tile_count, tobj.AIFlag, int(tobj.totalfan))
   
    def user_grade(self, tobj):
        """ͳ���û��ȼ�
        """
        if tobj.TAG == ACT_ONE_RESULT:
            title = int(tobj.title)
            #����userinfo����title�ֶ�
            sql = "update userinfo set title=%d where username='%s'" % (title,tobj.userName)
            self.cur.execute(sql)
            #����Ҫ�ռ��û��ȼ���Ϣ
            #if self.log_users.has_key(tobj.userName) == True:
            #    self.log_users[tobj.userName].grade = tobj.title
            #else:
            #    lu = LogUser()
            #    lu.grade = tobj.title
            #    self.log_users[tobj.userName] = lu 
        
    
    def goldboard(self, tobj):
        """ͳ�ƽ�����а�
        """
        if tobj.TAG == ACT_RANK:
            sql = "replace into goldboard(nickname,username,'gold') values('%s','%s','%s')" % (tobj.nickName,tobj.userName, tobj.mney)
            self.cur.execute(sql)
            
    def robot_data(self, tobj):
        """ͳ�ƻ���������
        """
        if tobj.TAG == ACT_GAMERESULT: 
            #������AI��
            AIFlag = int(tobj.AIFlag)
            tileCount = int(tobj.tile_count)
            if AIFlag > 0:
                self.robot_count[0] = self.robot_count[0] + int(tobj.round)
                if tileCount == 1:
                    self.robot_count[1] = self.robot_count[1] + int(tobj.round)
                if tileCount == 2:
                    self.robot_count[2] = self.robot_count[2] + int(tobj.round)
                #Ӯ��AI
                if AIFlag == 1:
                    self.robot_count[3] = self.robot_count[3] + int(tobj.round)
                    if tileCount == 1:
                        self.robot_count[4] = self.robot_count[4] + int(tobj.round)
                    if tileCount == 2:
                        self.robot_count[5] = self.robot_count[5] + int(tobj.round)


    def update_iap_data(self,tobj):
        """����iap��ص�����
        """
        if tobj.TAG == ACT_IAP:
            #�ж�������¼�Ƿ��Ѿ���������
            
            pid = tobj.getPid(tobj)
            
            self.iap_time = self.iap_time + 1
            #�����µ��ֶ����õ���Ǯ
            money = int(tobj.money)
            
            rmbmoney = float(tobj.price)
            #print "username=%s, money=%f" % (tobj.userName, rmbmoney)
            #gold,pay_time,total_pay��userinfo��
            sql = "update userinfo set pay_time=pay_time+1,gold=%d,total_pay=total_pay+%f where username='%s'"\
             % (int(tobj.userNewMney),rmbmoney,tobj.userName)
            self.cur.execute(sql)
            
            if self.IsNewPayUser(tobj.userName,self.parseday) == True:
                sql = "update  new_pay_user set new_num=new_num+1 where `date`='%s'" %(self.parseday)
                self.cur.execute(sql)
            #����pay_detail
            
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
        """ͳ����ҽ�Ǯ��֧��¼���ݸ���
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
        """�ڸ���ǰ�����������ݹ���
        """
        # new_pay_user�����¼����
        self.cur.execute("update new_pay_user set new_num=0,new_reg_num=0 where `date`='%s'" %(self.parseday)) 
    
    def last_update(self):
        """�������
        """
        #���� basic_userdata
        sql = "update basic_userdata set install_num=%d,reg_num=%d,guest_num=%d,lead_reg=%d,login_num=%d,LAUNCH_TIME=%d where date='%s'"\
        % (self.basic_userdata.install_num,self.basic_userdata.reg_num-self.basic_userdata.guest_num,self.basic_userdata.guest_num,self.basic_userdata.lead_reg,\
        self.basic_userdata.login_num,self.basic_userdata.launch_time,self.parseday)
        self.cur.execute(sql)
        
        #��¼������ʷ�������� 
        self.count_honline()
        #��¼��������ʱ��
        self.count_keeptime()
        #��¼���Ĳ�Ʒ����
        self.count_product_data()
        #ֻ������Ұ���ǰ500��
        self.count_goldboard()
        #ͳ���û��ȼ�
        self.count_user_grade()
        #ͳ�ƻ���������
        self.count_robot_data()
        #����ÿ�����Ӫ����
        self.count_iap_data()
        #����ϵͳ��֧��־����
        self.count_economic()
        #�����ֻ���"
        self.count_phoneinfo()
        #ͳ��������
        self.count_retention_rate()

    
    def count_honline(self):
        """ͳ����ʷ����
        """
        ave = round(self.total_online_user / self.online_count)
        self.cur.execute("update history_online set `max_time`='%s',`max_num`=%d,`min_time`='%s',`min_num`=%d,`ave_num`=%d \
                  where `date`='%s'" % (self.max_time[0],self.max_time[1],self.min_time[0],self.min_time[1],ave,self.parseday))
        
         
    def count_keeptime(self):
        """����ͳ��ʹ��ʱ��
        #����ÿ��ʹ��ʱ��
        """
        idx = 1
        for kk in self.keepline_data:
            kd = self.keepline_data[kk][0]
            tl = self.keepline_data[kk][1]
            sql = "update online_time set time_long=%d,time_count=%d where `date`='%s' and `type`=%d " % (tl,kd, self.parseday,idx)
            self.cur.execute(sql)
            idx = idx + 1
        #���㵥��ʹ��ʱ��
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
        """����ͳ�Ʋ�Ʒ����
        """
        # �ܾ�����һ���ƾ�����һ����ƽ�����������ƾ�����������ƽ������Ѻ�������������˾���
        sql = "update product_data set hand_num=%d,one_hand_num=%d,one_hand_fan=%s,two_hand_num=%d,two_hand_fan=%s,bet_baby=%d,robot_hand_num=%d where `date`='%s'" \
        % (self.product_data_arr[0],self.product_data_arr[1],"%.2f" % (round(self.product_data_arr[2]/self.product_data_arr[1])),self.product_data_arr[3],"%.2f" % (round(self.product_data_arr[4]/self.product_data_arr[3])),self.product_data_arr[5],self.product_data_arr[6],self.parseday)
        self.cur.execute(sql)
    
    def count_goldboard(self):
        """���ܴ���������а�
        """
        sql = "select gold from goldboard order by gold desc limit 500,1"
        self.cur.execute(sql)
        row = self.cur.fetchone()
        if row :
            sql = "delete from goldboard where gold < '%s'" % (row[0])
            self.cur.execute(sql)
        
    
    def count_user_grade(self):
        """���ܴ����û��ȼ��ֲ�
        """
        pass
        #����Ҫͳ���û��ȼ���ֱ�Ӵ�userinfo�ж�ȡ����
        #�õ�self.user_grade_data
        #for lk in self.log_users:
        #    lu = self.log_users[lk]
        #    title = int(lu.grade)
        #    if title == 0:
        #        continue
        #    title = title - 1
        #    self.user_grade_data[title] = self.user_grade_data[title] + 1
        #idx = 1
        #�Ƚ�֮ǰ�����
        #self.cur.execute("update user_grade set num=0")
        #for ug in self.user_grade_data:
        #    sql = "update user_grade set num=num+%d where grade=%d" % (ug, idx)
        #    self.cur.execute(sql)
        #    idx = idx + 1
    
    def count_robot_data(self):
        """���ܻ���������
        """
        sql = "update robot_data set total_hand=%d,one_card=%d,two_card=%d,win_time=%d,one_card_win=%d,two_card_win=%d\
         where `date`='%s'" % (self.robot_count[0],self.robot_count[1],self.robot_count[2],\
        self.robot_count[3],self.robot_count[4],self.robot_count[5],self.parseday)
        self.cur.execute(sql)
    
    def count_iap_data(self):
        """����IAP���
        """
        pay_num = len(self.iap_users)
        mny = 0
        #�޸�userinfo�е�gold
        for kn in self.iap_users:
            mny = mny + self.iap_users[kn]
        #rmb = GameMoney2RMB(mny)
        rmb = mny
        sql = "update basic_revenue_data set gain_gold=%d,pay_num=%d,pay_time=%d where `date`='%s'" %(rmb,pay_num,self.iap_time,self.parseday)
        self.cur.execute(sql)
        
        #�õ������û��ĵȼ�
        #����0
        self.cur.execute("update pay_user_grade set num=0")
        sql = "select title from userinfo where pay_time > 0"
        self.cur.execute(sql)
        for title  in self.cur.fetchall():
            title = int(title[0])
            sql = "update pay_user_grade set num=num+1 where grade=%d" %(title + 1)
            self.cur.execute(sql)
        
        #���µõ����յ�ע���û���ֵ
        sql = "select c.reg_date, count(c.reg_date) as rnum from (select a.reg_date,a.username from userinfo a inner join\
            ( select distinct DATE_FORMAT(paytime,'%Y-%m-%d') as paydate,username from pay_detail) b on a.reg_date=b.paydate and \
            a.username=b.username) c group by c.reg_date;"
        self.cur.execute(sql)
        for reg_date,rnum in self.cur.fetchall():
            self.cur.execute("update new_pay_user set new_reg_num=%d where `date`='%s'" %(rnum,reg_date.strftime("%Y-%m-%d")))
                
    def count_phoneinfo(self):
        #�����ֻ���Ϣ����صı���
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
        #�����ֻ���Ϣ��ͳ�Ʊ���
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
                    
        #��ʼ������Ե�����
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
    
    #################################�����෽��###################################################
    
    """

    def is_logined(self, userName):
        """�û��ѵ�¼
        """
        if self.log_users.has_key(userName) == True:
            lu = self.log_users[userName]
            if lu.is_logined == True:
                return True
        return False
        
    
    def is_new_user(self, userName):
        """�ж��Ƿ������û�
        """
        self.cur.execute("select count(id) from userinfo where username='%s'" % (userName))
        row = self.cur.fetchone()
        if row:
            if int(row[0]) <= 0:
                return True
        return False
        
    def is_new_install(self, androidid):
        """�ж��Ƿ����°�װ���û�
        """
        self.cur.execute("select count(id) from userinfo_imei where androidid='%s'" % (androidid))
        row = self.cur.fetchone()
        if row:
            if int(row[0]) <= 0:
                return True
        return False
        
    def split_honline(self,ti,usernum):
        """�����ʷ���߲�������
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
        """��ȡ��Ϸʱ�䳤��
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
        """��þ���ı������ͳ���
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
        """��ȡ��Ʒ����
        """
        #dround = int(dround)
        AIFlag = int(AIFlag)
        tile_count = int(tile_count)
        # �ܾ�����һ���ƾ�����һ����ƽ�����������ƾ�����������ƽ������Ѻ�������������˾���
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
        """�����û����жϸ��û��Ƿ��ǻ�����
        """
        if userName.find(ROBOT_NAME_PREFIX) == -1:
            return False
        return True  
    
    def IsNewPayUser(self,userName,paytime): 
        """�����û����ж��Ƿ����¸����û�
        """
        sql = "select count(username) as pycount from payboard where username='%s' and first_pay_time<'%s'" % (userName, paytime)
        self.cur.execute(sql)           
        pycount = self.cur.fetchone()
        if pycount <> None:
            if int(pycount[0]) <= 0:
                return True
        return False
    
    def updatePayBoardLoginTime(self,userName,logintime):
        """����֧�����а������¼ʱ��
        """
        sql = "update payboard set last_login='%s' where username='%s'" % (logintime,userName)
        self.cur.execute(sql)

    def count_economic(self):
        """����ϵͳ��֧��¼����
        """
        sql = "update robot_data set win_gold='%s',lose_gold='%d' where `date`='%s'"\
         % (self.sys_ecm_data[0], self.sys_ecm_data[1], self.parseday)
        self.cur.execute(sql)
        
    def count_retention_rate(self):
        """����������
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
        """�����û�����
        """
        sql = "update userinfo set channel='%s' where username='%s'" % (channel,username)
        self.cur.execute(sql)
            
        
    
    
    
    

    

   
    