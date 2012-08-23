#!/usr/bin/env python
# -*- coding: gbk -*-
"""activity.py.

���¼��ʽ

MahJongServer
"""

ACT_CONNECT			 = 1		 # ������Ϊ
"""
��ʽ:
	ʱ��,1,IP��ַ,�˿�
����:
	20120203123325,1,192.168.1.2,9893
"""

ACT_DISCONNECT		  = 2		 # ���ӶϿ���Ϊ
"""
��ʽ:
	ʱ��,2,IP��ַ,�˿�,����ʱ��(��)
����:
	20120203123325,2,192.168.1.2,9893,382
"""

'''
ACT_REGISTER			= 3		 # ע����Ϊ
ACT_QUICK_REGISTER	  = 4		 # ����ע����Ϊ
ACT_LOGIN			   = 5		 # ��¼��Ϊ
ACT_LOGOUT			  = 6		 # �ǳ���Ϊ
ACT_ENTERLEVEL		  = 7		 # ���볡����Ϊ
ACT_LEAVELEVEL		  = 8		 # �˳�������Ϊ
ACT_STARTGAME		   = 9		 # ��Ϸ��ʼ��Ϊ
ACT_GAMEABORT		   = 10		# ��Ϸ�ж���Ϊ
ACT_GAMEOVER			= 11	# ��Ϸ������Ϊ
ACT_CHALLENGE		   = 12		# ��ս��Ϊ
'''


#####################################################################################

ACT_REGISTER			= 1		# ע���û���Ϣ:
ACT_LOGIN				= 2		# ��¼��Ϊ
ACT_ONLINE				= 3		# �������,��ʱ����
ACT_KEEPTIME			= 4		# �������ʱ��
ACT_RANK				= 5		# ���а�(��δ��Ӽ�¼)
ACT_ONE_RESULT			= 6		# ���ÿ�ֽ����¼
ACT_GAMERESULT			= 7		# ������Ϸ��¼
ACT_MISS_RESULT			= 8		# �ľ�
ACT_LEVEL_PLAYING_ROOM	= 9		# �ڸ��ȼ���������ˣ��Ҹ�������ʱ��¼
ACT_ERROR_OPCODE		= 10	# �쳣����opCode (�ݶ����壬δ��Ӽ�¼)


'''��ʽ�ֶ�
ACT_REGISTER��				ip,	port,	UserName(�û���),	NickName(����ǳ�),	Sex(�Ա�),Mnui(���),	Image_Index(�������),	qreg(����ע���ʾΪ1����Ϊ0),	IMEI(�û���Ϣ)
ACT_LOGIN,					ip,	port,	svrName(��������),	UserName,	flag(1,Ϊ������½��2Ϊ���߻ָ�),	IMEI(�û���Ϣ)��phoneModel(�ֻ��ͺ�)��	PhoneRatio(�ֱ���)��	GameChannel(��Ϸ����)
ACT_ONLINE,					srvName(��������),	Logining_users(���ڵ�½�û�),	robots(���߻�������)��users(�����û������)��PK(����PK��)
ACT_KEEPTIME��				srvName��userName,	nickName��	DateTimeNow����-��-�գ�,	keepTime(���һ�ε�¼���˴εǳ���ʱ��)
ACT_RANK��					SrvName��	nickName,	mney(���)
ACT_ONE_RESULT��				userName,nickName,	AIFlag(AI��ʾ)��	mfan(���)��	dtms(�ܼӱ�����),	AllCount(�ܾ���)��	WinCount(Ӯ����),title(�û��ȼ�),level(���صȼ�)
ACT_GAMERESULT��				round(����)��	AIFlag(0:��AI.1:Ӯ��AI.2:�䷽AI��3˫������AI),	winerNick(Ӯ���ǳ�)��	winScore(Ӯ������)��	loserNick(�䷽�ǳ�)��	loserScore(�䷽����)��	tile_count(һ�������Ʊ�ʾ)��	times(���ֱ���)
ACT_MISS_RESULT��			name(������),	AIFlag(0:��AI.1:����AI.2:����AI,3˫������AI),	OwnerNamePoint(��������),	ClientName(������),	ClientNamePotint(���ͷ���)
ACT_LEVEL_PLAYING_ROOM��		levelRoom(���ӵȼ�)��	playingCount(������ˣ����)

'''

'''
�ӿڰ���
	import activity
	from log import log_activity

�ӿں�����
	log_activity(fmt, *args)

���ӣ�
	log_activity("%d,%s",activity.ACT_***,"value")
'''
