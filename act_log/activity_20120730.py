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

#####################################################################################

ACT_REGISTER            = 1     # 注册用户信息:
ACT_LOGIN               = 2     # 登录行为
ACT_ONLINE              = 3     # 在线玩家,定时触发
ACT_KEEPTIME            = 4     # 玩家在线时长
ACT_RANK                = 5     # 排行版(暂未添加记录)
ACT_ONE_RESULT          = 6     # 玩家每轮结果记录
ACT_GAMERESULT          = 7     # 结算游戏记录
ACT_MISS_RESULT         = 8     # 荒局
ACT_LEVEL_PLAYING_ROOM  = 9     # 在各等级场子内玩耍玩家个数，定时记录
ACT_ERROR_OPCODE        = 10    # 异常错误opCode (暂定定义，未添加记录)
ACT_IAP                 = 11    # IAP内购记录
ACT_GET_MONEY           = 12    # 领钱记录

'''格式字段
ACT_REGISTER，              ip, port,   UserName(用户名),   NickName(玩家昵称), Sex(性别), meny(注册金币), Image_Index(玩家形象),  qreg(快速注册标示为1，非为0),   IMEI(用户信息)
ACT_LOGIN,                  ip, port,   svrName(服务器名),  UserName,   flag(1,为正常登陆，2为掉线恢复),    IMEI(用户信息)，phoneModel(手机型号)，  PhoneRatio(分辨率)，    GameChannel(游戏渠道)
ACT_ONLINE,                 srvName(服务器名),  Logining_users(正在登陆用户),   robots(在线机器人数)，users(在线用户玩家数)，PK(正在PK数)
ACT_KEEPTIME，              srvName， userName,  nickName，  DateTimeNow（年-月-日）,    keepTime(最近一次登录到此次登出的时长)
ACT_RANK，                  SrvName，   nickName,   mney(金币)
ACT_ONE_RESULT，            UserName,    nickName,   AIFlag(AI标示)，    mfan(最大番)，  dtms(总加倍次数),   AllCount(总局数)，  WinCount(赢局数),  title(称号),  level(所在房间等级)
ACT_GAMERESULT，            round(轮数)，   AIFlag(0:无AI.1:房主AI.2:房客AI，3双方都是AI),  winerNick(赢方昵称)，   winScore(赢方分数)，    loserNick(输方昵称)，   loserScore(输方分数)，  tile_count(一或两副牌标示)，    times(最后局倍率)
ACT_MISS_RESULT，           name(房主名),   AIFlag(0:无AI.1:房主AI.2:房客AI,3双方都是AI),   OwnerNamePoint(房主分数),   ClientName(房客名), ClientNamePotint(房客分数)
ACT_LEVEL_PLAYING_ROOM，    levelRoom(场子等级)，   playingCount(正在玩耍人数)
ACT_IAP，                   UserName， nickName, IAPType(IAP类型)，purchaseState(采购状态)， productId(产品ID), money(产品金钱), userOdlMney(原来的金钱), userNewMney(改变后的金钱)， IAP_ID(IAP数据)
ACT_GET_MONEY，             userName,  nickName, getMoneyType(领钱类型),money(奖励额数)，old_money(增加前玩家金币),new_money(增加后玩家金币)
'''

'''
接口包：
    import activity
    from log import log_activity

接口函数：
    log_activity(fmt, *args)

例子：
    log_activity("%d,%s",activity.ACT_***,"value")
'''
