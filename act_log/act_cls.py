#!/usr/bin/env python
# -*- coding:gbk -*-
#encoding=gbk
"""act.py."""
# Python's import is same as Java's import.
from activity import *
import time
import datetime

from common import *
class Act:
    """��־�ı�ֵ��Ĺ�������
    """
    
    
    time = 0
    TAG = 0
    MIN_LEN = 2
    LOG_DAY = ""
    
    def parse(self,linelist):
        pass
    
    def __init__(self, linelist):
        self.time = linelist[0]
        
        
    @staticmethod
    def genParsedObj(line,yesday):
        if line <> None:
            line = line.strip()
            if line <> "":
                linelist = line.split(",")
                if len(linelist) <= Act.MIN_LEN:
                    return None
                Act.LOG_DAY = yesday.strftime("%Y-%m-%d")
                tag = int(linelist[1])

                if tag == ACT_REGISTER:
                    Register.TAG = tag
                    #if len(linelist) < 11:
                    #    return None
                    return Register(linelist)
                elif tag == ACT_LOGIN:
                    Login.TAG = tag
                    return Login(linelist)
                elif tag == ACT_ONLINE:
                    Online.TAG = tag
                    return Online(linelist)
                elif tag == ACT_KEEPTIME:
                    KeepTime.TAG = tag
                    return KeepTime(linelist)
                elif tag == ACT_RANK:
                    Rank.TAG = tag
                    return Rank(linelist)
                elif tag == ACT_ONE_RESULT:
                    OneResult.TAG = tag
                    return OneResult(linelist)
                elif tag == ACT_GAMERESULT:
                    GameResult.TAG = tag
                    return GameResult(linelist)
                elif tag == ACT_MISS_RESULT:
                    MissResult.TAG = tag
                    return MissResult(linelist)
                elif tag == ACT_LEVEL_PLAYING_ROOM:
                    LevelPlayingRoom.TAG = tag
                    return LevelPlayingRoom(linelist)
                elif tag == ACT_IAP:
                    ActIAP.TAG = tag
                    return ActIAP(linelist)
                elif tag == ACT_ECONOMIC_LOG:
                    ActEconomic.TAG = tag
                    return ActEconomic(linelist)
                elif tag == ACT_CLIENT_EXCEPTION:
                    ActClientException.TAG = tag
                    return ActClientException(linelist)
                else:
                    return None
                
                                
                                                        
class Register(Act):
    """ע���û���Ϣ
    """ 
    TAG = ACT_REGISTER
    ip = ""
    port = 0
    userName = ""
    nickName = ""
    money = 0
    sex = 0
    image_Index = 0
    regType = 0
    channel = ""
    uniqueID = ""
    reg_date = ""
    
    def __init__(self, linelist):
        Act.__init__(self,linelist)
        self.parse(linelist)
        pass
    def parse(self, linelist):
   
        self.ip = linelist[2]
        self.port = linelist[3]
        self.userName = linelist[4]
        self.nickName = linelist[5]
        self.money = linelist[6]
        self.sex = linelist[7]
        self.image_Index = linelist[8]
        self.regType = linelist[9]
        self.channel = linelist[10]
        self.uniqueID = linelist[11]
        self.reg_date = Act.LOG_DAY

class Login(Act):
    """��¼��Ϊ
    """ 
    TAG = ACT_LOGIN
    ip = ""
    port = 0
    #����������
    srvName = ""
    userName = ""
    regType = 0
    #(1,Ϊ������½��2Ϊ���߻ָ�)
    flag = 0
    versionNum = ""
    versionString = ""
    oSInfo = ""
    systemLang = ""
    resInfo = ""
    machineNo = ""
    netInfo = ""
    login_time = ""
    
    def __init__(self, linelist):
        Act.__init__(self,linelist)
        self.parse(linelist)
        pass
    
    def parse(self, linelist):
        self.ip = linelist[2]
        self.port = linelist[3]
        self.srvName = linelist[4]
        self.userName = linelist[5]
        self.regType = linelist[6]
        self.flag = linelist[7]
        self.versionNum = linelist[8]
        self.versionString = linelist[9]
        self.oSInfo = linelist[10]
        self.systemLang = linelist[11]
        self.resInfo = linelist[12]
        self.machineNo = linelist[13]
        self.netInfo = linelist[14]

        dt = datetime.datetime.strptime(self.time, "%H%M%S")
        self.login_time = Act.LOG_DAY + " " + dt.strftime("%H:%M:%S")
     
class Online(Act):
    """�������,��ʱ����
    """
    TAG = ACT_ONLINE
    #����������
    srvName = ""
    #���ڵ�½�û�
    logining_users = 0
    #���߻�������
    robots = 0
    #�����û������
    users = 0
    #����PK��
    PK = 0
    
    def __init__(self, linelist):
        Act.__init__(self,linelist)
        self.parse(linelist)
        pass    
    def parse(self, linelist):
        self.srvName = linelist[2]
        self.logining_users = linelist[3]
        self.robots = linelist[4]
        self.users = linelist[5]
        self.PK = linelist[6]
        
class KeepTime(Act):
    """�������ʱ��
    """
    TAG = ACT_KEEPTIME
    #����������
    srvName = ""
    userName = ""
    nickName = ""
    #��-��-��
    dateTimeNow = "0000-00-00"
    #���һ�ε�¼���˴εǳ���ʱ��
    keepTime = 0

    def __init__(self, linelist):
        Act.__init__(self,linelist)
        self.parse(linelist)
        pass
        
    def parse(self, linelist):
        self.srvName = linelist[2]
        self.userName = linelist[3]
        self.nickName = linelist[4]
        self.dateTimeNow = linelist[5]
        self.keepTime = linelist[6]
        
 
class Rank(Act):
    """���а�
    """  
    TAG = ACT_RANK
    srvName = ""
    userName = ""
    nickName = ""
    #���
    mney = 0

    def __init__(self, linelist):
        Act.__init__(self,linelist)
        self.parse(linelist)
        pass
        
    def parse(self, linelist):
        self.srvName = linelist[2]
        self.userName = linelist[3]
        self.nickName = linelist[4]
        self.mney = linelist[5]
        
class OneResult(Act):
    """���ÿ�ֽ����¼
    """
    TAG = ACT_ONE_RESULT
    userName = ""
    
    nickName = ""
    # AI��ʾ
    AIFlag = 0
    #���
    mfan = 0
    #�ܼӱ�����
    dtms = 0
    #�ܾ���
    allCount = 0
    #Ӯ����
    winCount = 0
    #�û��ȼ�
    title = 0
    #ȡֵΪ1��2���Ƹ���Ӧ
    tile_count = 0
    
    def __init__(self, linelist):
        Act.__init__(self,linelist)
        self.parse(linelist)
        pass  

    def parse(self, linelist):
        self.userName = linelist[2]
        self.nickName = linelist[3]
        self.AIFlag = linelist[4]
        self.mfan = linelist[5]
        self.dtms = linelist[6]
        self.allCount = linelist[7]
        self.winCount = linelist[8]
        self.title = linelist[9]
        if len(linelist) > 10:
            self.level = linelist[10]
        else:
            self.level = 0
        if len(linelist) > 11:
            self.tile_count = linelist[11]
        else:
            self.tile_count = 0
         
class GameResult(Act):
    """������Ϸ��¼
    """
    TAG = ACT_GAMERESULT
    level = 0                          #���ڷ���ĵȼ�
    tile_count = 0                     #һ�������Ʊ�ʾ��ȡֵΪ1��2���Ƹ���Ӧ��

    round = 0                          #��ǰ�غ�����������ͬ���֮����˶��ٻغϣ� 
    
    AIFlag = 0                         #0:�޻�����.1:Ӯ���ǻ����� 2:��һ����� 3:Ӯ����Ҷ��ǻ�����
    winner = ""                        #Ӯ���û���
    loser = ""                         #�䷽�û���
    base = 0                           #ÿ������
    times = 0                          #��ǰ����
    fan = 0                            #�Ʒ���
    double = 0                         #�ӱ�����
    taskfan = 0                        #������
    totalfan = 0                       #�ܷ��� = �Ʒ��� * (2 ^ �ӱ�����) * ������
    totalmoney = 0                     #��Ǯ�� = ÿ������ * ��ǰ���� * �ܷ���
    loserMoneyOld = 0                  #��ҿ�Ǯ֮ǰ�Ľ���
    loserMoneyNew = 0                  #��ҿ�Ǯ֮��Ľ���
    loserMoneyCost = 0                 #���ʵ�ʿ�Ǯ
    commission = 0                     #ϵͳ��ˮǮ��
    winnerMoneyAdd = 0                 #Ӯ��ʵ�ʼ�Ǯ
    winnerMoneyOld = 0                 #Ӯ�Ҽ�Ǯ֮ǰ��Ǯ��
    winnerMoneyNew = 0                 #Ӯ�Ҽ�Ǯ֮���Ǯ��
   
    def __init__(self, linelist):
        Act.__init__(self,linelist)
        self.parse(linelist)
        pass

    def parse(self, linelist):
        self.level = linelist[2]
        self.tile_count = linelist[3]
        self.round = linelist[4]
        self.AIFlag = linelist[5]
        self.winner = linelist[6]
        self.loser = linelist[7]
        self.base = linelist[8]
        self.times = linelist[9]
        self.fan = linelist[10]
        self.double = linelist[11]
        self.taskfan = linelist[12]
        self.totalfan = linelist[13]
        self.totalmoney = linelist[14]
        self.loserMoneyOld = linelist[15]
        self.loserMoneyNew = linelist[16]
        self.loserMoneyCost = linelist[17]
        self.commission = linelist[18]
        self.winnerMoneyAdd = linelist[19]
        self.winnerMoneyOld = linelist[20]
        self.winnerMoneyNew = linelist[21]
        
    
class MissResult(Act):
    """�ľ�
    """
    TAG = ACT_MISS_RESULT
    #������
    ownerName = ""
    #(0:��AI.1:����AI.2:����AI,3˫������AI)
    AIFlag = 0
    #��������
    ownerPoint = 0
    #������
    clientName = ""
    #���ͷ���
    clientPoint = 0
    def __init__(self, linelist):
        Act.__init__(self,linelist)
        self.parse(linelist)
        pass

    def parse(self, linelist):
        self.ownerName = linelist[2]
        self.AIFlag = linelist[3]
        self.ownerPoint = linelist[4]
        self.clientName = linelist[5]
        self.clientPoint = linelist[6]

        
class LevelPlayingRoom(Act):
    """�ڸ��ȼ���������ˣ��Ҹ�������ʱ��¼
    """
    TAG = ACT_LEVEL_PLAYING_ROOM
    #���ӵȼ�
    levelRoom = 0
    #������ˣ������
    playingCount = 0
    def __init__(self, linelist):
        Act.__init__(self,linelist)
        self.parse(linelist)
        pass
   
    def parse(self, linelist):
        self.levelRoom = linelist[2]
        self.playingCount = linelist[3]
        
class ActIAP(Act):
    """IAP�ڹ���¼
    """
    TAG = ACT_IAP
    #�ַ���                         ����û���
    userName = ''
    #�ַ���                         ����ǳ�
    nickName = ''
    '''
                    ����                           IAP���ͣ�
       1���ȸ�Play�ڹ�����
       3��AliPay֧��������
    '''
    IAPType = 0
    '''
              ����                           �ɹ�״̬��
     0��purchased(����)
     1��canceled(����)
     2��refunded(�˿�)
     3��expired, for subscription purchases only(����,ֻ���Ĺ���)
    '''
    purchaseState = -1
    productId = 0                     #����                           ��ƷID
    money = 0                         #����                           ��Ʒ��Ǯ
    userOdlMney = 0                   #����                           ����ǰ��ҵĽ�Ǯ
    userNewMney = 0                   #����                           �������ҵĽ�Ǯ
    IAP_ID = ""                       #�ַ���                         IAP����
    
    vip = 0                           #��Ʒ����vip�ȼ�:0.�˲�Ʒ��vip��Ʒ 1.vip�ȼ�1 2.vip�ȼ�2  3.vip�ȼ�3
    price = 0.0                       #������                         �۸�(RMB)
    iap_time = ""                     #�ڹ�������ʱ��
    
    def __init__(self, linelist):
        Act.__init__(self,linelist)
        self.parse(linelist)
        pass
    
    def parse(self, linelist):
        self.userName = linelist[2]
        self.nickName = linelist[3]
        self.IAPType = linelist[4]
        self.purchaseState = linelist[5]
        self.productId = linelist[6]
        self.money = linelist[7]
        self.userOdlMney = linelist[8]
        self.userNewMney = linelist[9]
        self.IAP_ID = linelist[10]
        self.vip = linelist[11]
        self.price = linelist[12]
        dt = datetime.datetime.strptime(self.time, "%H%M%S")
        self.iap_time = Act.LOG_DAY + " " + dt.strftime("%H:%M:%S")
        
    def getPid(self,tobj):
        """ʹ��PID��Ψһ����ǰ��¼����Ȼ���ܻ����һ���ظ���¼һ���˵Ĳɹ���¼
        """
        dt = datetime.datetime.strptime(tobj.iap_time,"%Y-%m-%d %H:%M:%S")
        return tobj.userName+dt.strftime('%Y%m%d%H%M%S')

class ActEconomic(Act):
    """ϵͳ����ҽ�Ǯ��֧��¼
    """
    type = 0                                   #����                           ����
    sub_type = 0                               #����                           ������
    amount = 0                                 #����                           Ǯ��
    user = ""                                  #�ַ���                         Ӱ�����
    nick = ""                                  #�ַ���                         �ǳ�
    money = ""                                 #����                           ��Ҹ��º�Ľ�Ǯ
    economic_time = ""                         #��֧��¼ʱ��
    def __init__(self, linelist):
        Act.__init__(self,linelist)
        self.parse(linelist)
        pass
    
    def parse(self, linelist):
        self.type = linelist[2]
        self.sub_type = linelist[3]
        self.amount = linelist[4]
        self.user = linelist[5]
        self.nick = linelist[6]
        self.money = linelist[7]

        dt = datetime.datetime.strptime(self.time, "%H%M%S")
        self.economic_time = Act.LOG_DAY + " " + dt.strftime("%H:%M:%S")

class ActClientException(Act):
    """�ͻ����쳣����
    """
    ip = ""                      #�ַ���                            ��ԴIP��ַ
    port = 0                     #����                              ��Դ�˿ں�
    versionNum = ""              #�ַ���                            ��Ϸ�汾ֵ
    versionString = ""           #�ַ���                            ��Ϸ�汾��
    oSInfo = ""                  #�ַ���                            ϵͳ�汾��Ϣ
    systemLang = ""              #�ַ���                            ϵͳ����
    resInfo = ""                 #�ַ���                            ����ն˷ֱ���
    machineNo = ""               #�ַ���                            ����ն˻����ͺ�
    netInfo = ""                 #�ַ���                            ����ն�������ʽ
    happen_time = ""             #
    
    def __init__(self, linelist):
        Act.__init__(self,linelist)
        self.parse(linelist)
        pass
    
    def parse(self, linelist):
        self.ip = linelist[2]
        self.port = int(linelist[3])
        self.versionNum = linelist[4]
        self.versionString = linelist[5]
        self.oSInfo = linelist[6]
        self.systemLang = linelist[7]
        self.resInfo = linelist[8]
        self.machineNo = linelist[9]
        self.netInfo = linelist[10]

        dt = datetime.datetime.strptime(self.time, "%H%M%S")
        self.happen_time = Act.LOG_DAY + " " + dt.strftime("%H:%M:%S")        