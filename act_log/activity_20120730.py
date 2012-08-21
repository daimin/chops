#!/usr/bin/env python
# -*- coding: gbk -*-
"""activity.py.

���¼��ʽ

MahJongServer
"""

"""
������ʽ:
    ����ʱ��(hhmmss),����id,�����ֶ�2,�����ֶ�2,...
����:
    123325,1,192.168.1.2,9893
"""

#####################################################################################

ACT_REGISTER            = 1     # ע���û���Ϣ:
ACT_LOGIN               = 2     # ��¼��Ϊ
ACT_ONLINE              = 3     # �������,��ʱ����
ACT_KEEPTIME            = 4     # �������ʱ��
ACT_RANK                = 5     # ���а�(��δ��Ӽ�¼)
ACT_ONE_RESULT          = 6     # ���ÿ�ֽ����¼
ACT_GAMERESULT          = 7     # ������Ϸ��¼
ACT_MISS_RESULT         = 8     # �ľ�
ACT_LEVEL_PLAYING_ROOM  = 9     # �ڸ��ȼ���������ˣ��Ҹ�������ʱ��¼
ACT_ERROR_OPCODE        = 10    # �쳣����opCode (�ݶ����壬δ��Ӽ�¼)
ACT_IAP                 = 11    # IAP�ڹ���¼
ACT_GET_MONEY           = 12    # ��Ǯ��¼

'''��ʽ�ֶ�
ACT_REGISTER��              ip, port,   UserName(�û���),   NickName(����ǳ�), Sex(�Ա�), meny(ע����), Image_Index(�������),  qreg(����ע���ʾΪ1����Ϊ0),   IMEI(�û���Ϣ)
ACT_LOGIN,                  ip, port,   svrName(��������),  UserName,   flag(1,Ϊ������½��2Ϊ���߻ָ�),    IMEI(�û���Ϣ)��phoneModel(�ֻ��ͺ�)��  PhoneRatio(�ֱ���)��    GameChannel(��Ϸ����)
ACT_ONLINE,                 srvName(��������),  Logining_users(���ڵ�½�û�),   robots(���߻�������)��users(�����û������)��PK(����PK��)
ACT_KEEPTIME��              srvName�� userName,  nickName��  DateTimeNow����-��-�գ�,    keepTime(���һ�ε�¼���˴εǳ���ʱ��)
ACT_RANK��                  SrvName��   nickName,   mney(���)
ACT_ONE_RESULT��            UserName,    nickName,   AIFlag(AI��ʾ)��    mfan(���)��  dtms(�ܼӱ�����),   AllCount(�ܾ���)��  WinCount(Ӯ����),  title(�ƺ�),  level(���ڷ���ȼ�)
ACT_GAMERESULT��            round(����)��   AIFlag(0:��AI.1:����AI.2:����AI��3˫������AI),  winerNick(Ӯ���ǳ�)��   winScore(Ӯ������)��    loserNick(�䷽�ǳ�)��   loserScore(�䷽����)��  tile_count(һ�������Ʊ�ʾ)��    times(���ֱ���)
ACT_MISS_RESULT��           name(������),   AIFlag(0:��AI.1:����AI.2:����AI,3˫������AI),   OwnerNamePoint(��������),   ClientName(������), ClientNamePotint(���ͷ���)
ACT_LEVEL_PLAYING_ROOM��    levelRoom(���ӵȼ�)��   playingCount(������ˣ����)
ACT_IAP��                   UserName�� nickName, IAPType(IAP����)��purchaseState(�ɹ�״̬)�� productId(��ƷID), money(��Ʒ��Ǯ), userOdlMney(ԭ���Ľ�Ǯ), userNewMney(�ı��Ľ�Ǯ)�� IAP_ID(IAP����)
ACT_GET_MONEY��             userName,  nickName, getMoneyType(��Ǯ����),money(��������)��old_money(����ǰ��ҽ��),new_money(���Ӻ���ҽ��)
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
