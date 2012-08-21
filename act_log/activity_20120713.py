#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#encoding=utf-8
"""activity.py.

活动记录格式

MahJongServer
"""

ACT_CONNECT			 = 1		 # 连接行为
"""
格式:
	时间,1,IP地址,端口
例子:
	20120203123325,1,192.168.1.2,9893
"""

ACT_DISCONNECT		  = 2		 # 连接断开行为
"""
格式:
	时间,2,IP地址,端口,连接时长(秒)
例子:
	20120203123325,2,192.168.1.2,9893,382
"""

'''
ACT_REGISTER			= 3		 # 注册行为
ACT_QUICK_REGISTER	  = 4		 # 快速注册行为
ACT_LOGIN			   = 5		 # 登录行为
ACT_LOGOUT			  = 6		 # 登出行为
ACT_ENTERLEVEL		  = 7		 # 进入场子行为
ACT_LEAVELEVEL		  = 8		 # 退出场子行为
ACT_STARTGAME		   = 9		 # 游戏开始行为
ACT_GAMEABORT		   = 10		# 游戏中断行为
ACT_GAMEOVER			= 11	# 游戏结束行为
ACT_CHALLENGE		   = 12		# 挑战行为
'''


ACT_REGISTER			= 1		# 注册用户信息:
ACT_LOGIN				= 2		# 登录行为
ACT_ONLINE				= 3		# 在线玩家,定时触发
ACT_KEEPTIME			= 4		# 玩家在线时长
ACT_RANK				= 5		# 排行版
ACT_ONE_RESULT			= 6		# 玩家每轮结果记录
ACT_GAMERESULT			= 7		# 结算游戏记录
ACT_MISS_RESULT			= 8		# 荒局
ACT_LEVEL_PLAYING_ROOM	= 9		# 在各等级场子内玩耍玩家个数，定时记录
ACT_LEVEL_WAITING_ROOM	= 10	# 在场子里等待玩耍的单玩家个数，定时记录



'''格式字段
ACT_REGISTER，				ip,	port,	UserName(用户名),	NickName(玩家昵称),	Sex(性别),	Image_Index(玩家形象),	qreg(快速注册标示为1，非为0),	IMEI(用户信息)
ACT_LOGIN,					ip,	port,	svrName(服务器名),	UserName,	flag(1,为正常登陆，2为掉线恢复),	IMEI(用户信息)，phoneModel(手机型号)，	PhoneRatio(分辨率)，	GameChannel(游戏渠道)
ACT_ONLINE,					srvName(服务器名),	Logining_users(正在登陆用户),	robots(在线机器人数)，users(在线用户玩家数)，PK(正在PK数)
ACT_KEEPTIME，				srvName，	nickName，	DateTimeNow（年-月-日）,	keepTime(最近一次登录到此次登出的时长)
ACT_RANK，					SrvName，	nickName,	mney(金币)
ACT_ONE_RESULT，				nickName,	AIFlag(AI标示)，	mfan(最大番)，	dtms(总加倍次数),	AllCount(总局数)，	WinCount(赢局数)
ACT_GAMERESULT，				round(轮数)，	AIFlag(0:无AI.1:房主AI.2:房客AI，3双方都是AI),	winerNick(赢方昵称)，	winScore(赢方分数)，	loserNick(输方昵称)，	loserScore(输方分数)，	一两副牌标示，	最后局倍率
ACT_MISS_RESULT，			name(房主名),	AIFlag(0:无AI.1:房主AI.2:房客AI,3双方都是AI),	OwnerNamePoint(房主分数),	ClientName(房客名),	ClientNamePotint(房客分数)
ACT_LEVEL_PLAYING_ROOM，		levelRoom(场子等级)，	playingCount(正在玩耍人数)

'''
