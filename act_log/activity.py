#!/usr/bin/env python
# -*- coding: gbk -*-
"""activity.py.

活动记录格式

MahJongServer
"""

"""
基本格式:
    当日时间(hhmmss),功能id,功能字段2,功能字段2,...
例子:
    123325,1,192.168.1.2,9893
"""


'''
接口包：
    import activity
    from log import log_activity

接口函数：
    log_activity(fmt, *args)

例子：
    log_activity("%d,%s",activity.ACT_XXX,"value")
'''

#####################################################################################

ACT_REGISTER            = 1     # 注册用户信息:
"""
格式字段:               类型                              说明
ip                      字符串                            注册来源IP地址
port                    整数                              注册来源端口号
UserName                字符串                            注册用户名
NickName                字符串                            注册昵称
Money                   整数                              注册送金币
Sex                     整数                              性别: 
                                                            0.未知 
                                                            1.男 
                                                            2.女
Image_Index             整数                              玩家头像
RegType                 整数                              用户注册类型:
                                                            0.普通注册 
                                                            1.快速注册
                                                            2.QQ注册
                                                            3.微博注册
                                                            9.机器人
Channel                 字符串                            用户渠道包名.
                                                          如果为空表示官方版.
UniqueID                字符串                            客户端硬件唯一ID: 比如Android ID. 
                                                          如果为空表示取不出数据: 未知.

示例:
    234912,1,115.214.168.179,59399,binjune225,iorl,300000,1,4,0,4399专用版,BkSMSQFVimFKRpy0

"""

ACT_LOGIN               = 2     # 登录行为:
'''
格式字段：               类型                          说明
ip                      字符串                         登陆来源IP弟子
port                    整数                           登陆来源端口号
svrName                 字符串                         登陆服务器名
UserName                字符串                         登陆用户用户名
RegType                 整数                           用户注册类型:
                                                         0.普通注册 
                                                         1.快速注册
                                                         2.QQ注册
                                                         3.微博注册
                                                         9.机器人
flag                    整数                           登陆标示：
                                                               1：正常登陆
                                                               2：掉线恢复
VersionNum              字符串                         游戏版本值
VersionString           字符串                         游戏版本串
OSInfo                  字符串                         系统版本信息
SystemLang              字符串                         系统语言
ResInfo                 字符串                         玩家终端分辨率
MachineNo               字符串                         玩家终端机器型号
NetInfo                 字符串                         玩家终端联网方式

示例：
    182339,2,127.0.0.1,3104,localhost2235,_i.robot_77461,1,0,0.0.0,Python 2.6.5,Chinese,1920x1080,BenQ G2222HD,Enternet
'''

ACT_ONLINE              = 3     # 在线玩家,定时触发
'''
格式字段：               类型                          说明
srvName                 字符串                         服务器名
Logining_users          整数                           正在登陆用户数量
robots                  整数                           在线机器人数量
users                   整数                           在线用户玩家数量
PK                      整数                           正在PK的人数量

示例：
    103341,3,localhost2235,0,1,0,0
'''


ACT_KEEPTIME            = 4     # 玩家在线时长
'''
格式字段：               类型                          说明
srvName                 字符串                         服务器名
userName                字符串                         玩家用户名
nickName                字符串                         玩家昵称
DateTimeNow             字符串（年-月-日）,             当前的日期
keepTime                浮点型（时间戳）                最近一次登录到此次登出的时长
mney                    整形                           玩家当前金钱
示例：
    170043,4,localhost2235,ijqns2hl,司空娜迎,2012-07-27,394.938000,100000
'''


ACT_RANK                = 5     # 排行版(暂未添加记录)
'''
格式字段                类型                          说明
SrvName                字符串                         服务器名
userName               字符串                         玩家用户名
nickName               字符串                         玩家昵称
mney                   整数                           玩家金币

示例：
    暂无
'''


ACT_ONE_RESULT          = 6     # 玩家每轮结果记录
'''
格式字段                类型                          说明
UserName               字符串                         玩家用户名
nickName               字符串                         玩家昵称
AIFlag                 整数                           AI标示（表示该用户是否为机器人）：
                                                             1：为机器人
                                                             0：非机器人    
mfan                   整数                           最大番数
dtms                   整数                           总加倍次数
AllCount               整数                           总局数
WinCount               整数                           赢局数
title                  整数                           玩家称号
level                  整数                           所在房间等级
tile_count             整数                           一或两副牌标示(取值为1或2与牌副对应）

示例：
    175550,6,ahnl13cf,栗裕霞,0,13,0,1,1,0,2,1

'''


ACT_GAMERESULT          = 7     # 结算游戏记录（含双方玩家，每胡牌结算记录一次）
'''
格式字段               类型                           说明
level                  整数                           所在房间等级
tile_count             整数                           一或两副牌标示（取值为1或2与牌副对应）
round                  整数                           当前回合数（房间内同玩家之间打了多少回合） 
AIFlag                 整数                           机器人标识：
                                                        0:无机器人.
                                                        1:赢家是机器人
                                                        2:输家机器人
                                                        3:赢家输家都是机器人
winner                 字符串                         赢方用户名
loser                  字符串                         输方用户名
base                   整数                           每番基数
times                  整数                           当前倍率
fan                    整数                           牌番数
double                 整数                           加倍次数
taskfan                整数                           任务倍率
totalfan               整数                           总番数 = 牌番数 * (2 ^ 加倍番数) * 任务倍率
totalmoney             整数                           总钱数 = 每番基数 * 当前倍率 * 总番数
loserMoneyOld          整数                           输家扣钱之前的金数
loserMoneyNew          整数                           输家扣钱之后的金数
loserMoneyCost         整数                           输家实际扣钱
commission             整数                           系统抽水钱数
winnerMoneyAdd         整数                           赢家实际加钱
winnerMoneyOld         整数                           赢家加钱之前的钱数
winnerMoneyNew         整数                           赢家加钱之后的钱数
示例
    175550,7,3,2,5,2,binggo0,_i.robot_22344,2000,1,16,2,2,128,256000,255000,0,25500,500000,729500
'''


ACT_MISS_RESULT         = 8     # 荒局
'''
格式字段                类型                          说明
OwnerName              字符串                        房主昵称名
AIFlag                 整数                          机器人标识：
                                                        0:无机器人
                                                        1:房主是机器人
                                                        2:房客机器人
                                                        3：双方都是机器人
OwnerNamePoint          整形                         房主分数
ClientName             字符串                        房客昵称名
ClientNamePotint       整形                          房客分数
 
示例：
    暂无
    
'''


ACT_LEVEL_PLAYING_ROOM  = 9     # 在各等级场子内玩耍玩家个数，定时记录
'''
格式字段                类型                          说明
levelRoom              整数                           场子等级
playingCount           整数                           正在玩耍人数

示例：
    175508,9,0,0
    175508,9,1,0
    175508,9,2,2
    175508,9,3,0
    175508,9,4,0
    175508,9,5,0
    175508,9,6,0
    175508,9,7,0
    175508,9,8,0
    175508,9,9,0
    175508,9,10,0
    175508,9,11,0
'''


ACT_ERROR_OPCODE        = 10    # 异常错误opCode (暂定定义，未添加记录)
'''
格式字段                类型                          说明
    暂无

示例：
    暂无
'''



ACT_IAP                 = 11    # IAP内购记录
'''
格式字段                类型                          说明
UserName               字符串                         玩家用户名
nickName               字符串                         玩家昵称
IAPType                整数                           IAP类型：
                                                        1.谷歌内购
                                                        2.AppStore
                                                        3.支付宝
                                                        4.卡类
                                                        5.短信
purchaseState          整数                           采购状态：
                                                           0：purchased(购买)
                                                           1：canceled(撤消)
                                                           2：refunded(退款)
                                                           3：expired, for subscription purchases only(过期,只订阅购买)
productId              字符串                         产品ID
money                  整数                           产品金钱
userOdlMney            整数                           购买前玩家的金钱
userNewMney            整数                           购买后玩家的金钱
IAP_ID                 字符串                         IAP数据
diamond                整数                           产品钻石数量
price                  浮点数                         价格(RMB)

示例：
    015717,11,zhuchunya526,tanya,3,0,游戏充值_200万金,2000000,68000,2068000,AliPay:20120730015758564_mj_zhuchunya526,0,2.00
    121609,11,zhuchunya526,tanya,3,0,游戏充值_500万金,5000000,0,5000000,AliPay:20120730121639260_mj_zhuchunya526,0,2.00

'''



ACT_ECONOMIC_LOG        = 13    # 系统和玩家金钱收支记录
# QREG : 快速注册用户
# USER : 普通用户
# ROBOT : 机器人
# 类型
ECONOMIC_INCOME         = 1                     # 系统收入
ECONOMIC_EXPEND         = 2                     # 系统支出
ECONOMIC_EXCHANGE       = 3                     # USER之间收支
# 子类型: 收入类(1000 - 1999):
INCOME_ROBOT_WIN_USER   = 1000                  # USER输ROBOT(抽水前)
INCOME_COMMISSION_USER_WIN_USER = 1001          # 场子抽水: USER赢USER
#INCOME_COMMISSION_USER_WIN_QREG = 1002         # 场子抽水: USER赢QREG
#INCOME_COMMISSION_USER_WIN_ROBOT = 1003        # 场子抽水: USER赢ROBOT
INCOME_GM_RECOVER_USER  = 1004                  # GM扣USER钱
INCOME_QREG_WIN_USER    = 1005                  # USER输QREG(抽水前)
# 子类型: 支出类(2000 - 2999):
EXPEND_USER_REG_GIFT    = 2000                  # USER注册时赠送
EXPEND_USER_WIN_ROBOT   = 2001                  # USER赢ROBOT(抽水后)
EXPEND_USER_WIN_QREG    = 2002                  # USER赢QREG(抽水后)
EXPEND_USER_DAILY_BONUS = 2003                  # USER领粮饷
EXPEND_USER_REVISIT_BONUS= 2004                 # USER领回访奖励
EXPEND_USER_CHARGE      = 2005                  # USER充值加钱
EXPEND_GM_SEND_USER     = 2006                  # GM给予USER钱
EXPEND_USER_TASK_DONE   = 2007                  # USER完成任务
EXPEND_USER_ACHI_DONE   = 2008                  # USER完成成就
EXPAND_DIAMOND_2_MONEY  = 2009                  # 钻石兑换金币
EXPAND_ETERNAL_TIPS     = 2010                  # 免死符补贴玩家
# 子类型: USER之间收支类(3000 - 3999):
EXCHANGE_USER_LOSE_USER = 3000                  # USER输USER(抽水前)
EXCHANGE_USER_WIN_USER  = 3001                  # USER净赢USER(抽水后)
'''
格式字段               类型                           说明
type                   整数                           类型
sub_type               整数                           子类型
amount                 整数                           钱数
user                   字符串                         影响玩家
nick                   字符串                         昵称
money                  整数                           玩家更新后的金钱

示例
    123456,13,1,1000,52000,binggo0,阿滨古0,243300 # (机器人)赢玩家binggo0钱52000,剩余243300
    123456,13,1,1001,3500,binggo1,阿滨古0,233000  # 场子抽水3500,玩家binggo0剩余233000
'''

ACT_CLIENT_EXCEPTION    = 14    # 客户端异常报告
"""
格式字段:               类型                              说明
ip                      字符串                            来源IP地址
port                    整数                              来源端口号
VersionNum              字符串                            游戏版本值
VersionString           字符串                            游戏版本串
OSInfo                  字符串                            系统版本信息
SystemLang              字符串                            系统语言
ResInfo                 字符串                            玩家终端分辨率
MachineNo               字符串                            玩家终端机器型号
NetInfo                 字符串                            玩家终端联网方式

示例:
    234912,14,115.214.168.179,59399,0,0.0.0,Python 2.6.5,Chinese,1920x1080,BenQ G2222HD,Enternet
"""

ACT_CLICK_LOG           = 15    # 点击记录
"""
格式字段:               类型                              说明
UserName                字符串                            用户名
ClickName               字符串                            点击对象名
ClickAddTime            整数                              新增点击次数

示例:
    234912,15,binggo0,大厅快速充值,2
"""

ACT_ITEM_LOG            = 16    # 道具记录(包括钻石)
# 类型
ITEM_GOT                = 1                     # 玩家获得道具
ITEM_COST               = 2                     # 玩家消耗道具
# 子类型: 获得
GOT_CHARGE              = "充值获得"
GOT_SHOP                = "商店购买"
GOT_GM_SEND             = "GM给予"
# 子类型: 消耗
COST_SHOP               = "商店消耗"
COST_USE                = "主动使用"
COST_GM_RECOVER         = "GM收回"
COST_PASSIVE            = "被动使用"
"""
格式字段:               类型                              说明
UserName                字符串                            用户名
ItemLogType             整数                              类型
ItemLogSubType          字符串                            子类型
ItemName                字符串                            道具名
ItemCount               整数                              道具数量

示例:
    234912,16,binggo0,1,充值获得,钻石,100
    234912,16,binggo0,2,商店消耗,钻石,20
    234912,16,binggo0,1,商店购买,PK令,1
    234913,16,binggo0,2,使用消耗,PK令,1
"""


##########################################################################################

'''
接口包：
    import activity
    from log import log_activity

接口函数：
    log_activity(fmt, *args)tt

例子：
    log_activity("%d,%s",activity.ACT_***,"value")
'''

