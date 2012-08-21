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
    """日志文本值类的公共父类
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
                else:
                    return None
                
                                
                                                        
class Register(Act):
    """注册用户信息
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
    """登录行为
    """ 
    TAG = ACT_LOGIN
    ip = ""
    port = 0
    #服务器名称
    srvName = ""
    userName = ""
    regType = 0
    #(1,为正常登陆，2为掉线恢复)
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
    """在线玩家,定时触发
    """
    TAG = ACT_ONLINE
    #服务器名称
    srvName = ""
    #正在登陆用户
    logining_users = 0
    #在线机器人数
    robots = 0
    #在线用户玩家数
    users = 0
    #正在PK数
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
    """玩家在线时长
    """
    TAG = ACT_KEEPTIME
    #服务器名称
    srvName = ""
    userName = ""
    nickName = ""
    #年-月-日
    dateTimeNow = "0000-00-00"
    #最近一次登录到此次登出的时长
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
    """排行版
    """  
    TAG = ACT_RANK
    srvName = ""
    userName = ""
    nickName = ""
    #金币
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
    """玩家每轮结果记录
    """
    TAG = ACT_ONE_RESULT
    userName = ""
    
    nickName = ""
    # AI标示
    AIFlag = 0
    #最大番
    mfan = 0
    #总加倍次数
    dtms = 0
    #总局数
    allCount = 0
    #赢局数
    winCount = 0
    #用户等级
    title = 0
    #取值为1或2与牌副对应
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
    """结算游戏记录
    """
    TAG = ACT_GAMERESULT
    level = 0                          #所在房间的等级
    tile_count = 0                     #一或两副牌标示（取值为1或2与牌副对应）

    round = 0                          #当前回合数（房间内同玩家之间打了多少回合） 
    
    AIFlag = 0                         #0:无机器人.1:赢家是机器人 2:输家机器人 3:赢家输家都是机器人
    winner = ""                        #赢方用户名
    loser = ""                         #输方用户名
    base = 0                           #每番基数
    times = 0                          #当前倍率
    fan = 0                            #牌番数
    double = 0                         #加倍次数
    taskfan = 0                        #任务倍率
    totalfan = 0                       #总番数 = 牌番数 * (2 ^ 加倍番数) * 任务倍率
    totalmoney = 0                     #总钱数 = 每番基数 * 当前倍率 * 总番数
    loserMoneyOld = 0                  #输家扣钱之前的金数
    loserMoneyNew = 0                  #输家扣钱之后的金数
    loserMoneyCost = 0                 #输家实际扣钱
    commission = 0                     #系统抽水钱数
    winnerMoneyAdd = 0                 #赢家实际加钱
    winnerMoneyOld = 0                 #赢家加钱之前的钱数
    winnerMoneyNew = 0                 #赢家加钱之后的钱数
   
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
    """荒局
    """
    TAG = ACT_MISS_RESULT
    #房主名
    ownerName = ""
    #(0:无AI.1:房主AI.2:房客AI,3双方都是AI)
    AIFlag = 0
    #房主分数
    ownerPoint = 0
    #房客名
    clientName = ""
    #房客分数
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
    """在各等级场子内玩耍玩家个数，定时记录
    """
    TAG = ACT_LEVEL_PLAYING_ROOM
    #场子等级
    levelRoom = 0
    #正在玩耍的人数
    playingCount = 0
    def __init__(self, linelist):
        Act.__init__(self,linelist)
        self.parse(linelist)
        pass
   
    def parse(self, linelist):
        self.levelRoom = linelist[2]
        self.playingCount = linelist[3]
        
class ActIAP(Act):
    """IAP内购记录
    """
    TAG = ACT_IAP
    #字符串                         玩家用户名
    userName = ''
    #字符串                         玩家昵称
    nickName = ''
    '''
                    整数                           IAP类型：
       1：谷歌Play内购类型
       3：AliPay支付宝类型
    '''
    IAPType = 0
    '''
              整数                           采购状态：
     0：purchased(购买)
     1：canceled(撤消)
     2：refunded(退款)
     3：expired, for subscription purchases only(过期,只订阅购买)
    '''
    purchaseState = -1
    productId = 0                     #整数                           产品ID
    money = 0                         #整数                           产品金钱
    userOdlMney = 0                   #整数                           购买前玩家的金钱
    userNewMney = 0                   #整数                           购买后玩家的金钱
    IAP_ID = ""                       #字符串                         IAP数据
    
    vip = 0                           #产品带的vip等级:0.此产品非vip产品 1.vip等级1 2.vip等级2  3.vip等级3
    price = 0.0                       #浮点数                         价格(RMB)
    iap_time = ""                     #内购发生的时间
    
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
        """使用PID来唯一化当前记录，不然可能会出现一天重复记录一个人的采购记录
        """
        dt = datetime.datetime.strptime(tobj.iap_time,"%Y-%m-%d %H:%M:%S")
        return tobj.userName+dt.strftime('%Y%m%d%H%M%S')

class ActEconomic(Act):
    """系统和玩家金钱收支记录
    """
    type = 0                                   #整数                           类型
    sub_type = 0                               #整数                           子类型
    amount = 0                                 #整数                           钱数
    user = ""                                  #字符串                         影响玩家
    nick = ""                                  #字符串                         昵称
    money = ""                                 #整数                           玩家更新后的金钱
    economic_time = ""                         #收支记录时间
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
        
