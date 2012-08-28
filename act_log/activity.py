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


'''
�ӿڰ���
    import activity
    from log import log_activity

�ӿں�����
    log_activity(fmt, *args)

���ӣ�
    log_activity("%d,%s",activity.ACT_XXX,"value")
'''

#####################################################################################

ACT_REGISTER            = 1     # ע���û���Ϣ:
"""
��ʽ�ֶ�:               ����                              ˵��
ip                      �ַ���                            ע����ԴIP��ַ
port                    ����                              ע����Դ�˿ں�
UserName                �ַ���                            ע���û���
NickName                �ַ���                            ע���ǳ�
Money                   ����                              ע���ͽ��
Sex                     ����                              �Ա�: 
                                                            0.δ֪ 
                                                            1.�� 
                                                            2.Ů
Image_Index             ����                              ���ͷ��
RegType                 ����                              �û�ע������:
                                                            0.��ͨע�� 
                                                            1.����ע��
                                                            2.QQע��
                                                            3.΢��ע��
                                                            9.������
Channel                 �ַ���                            �û���������.
                                                          ���Ϊ�ձ�ʾ�ٷ���.
UniqueID                �ַ���                            �ͻ���Ӳ��ΨһID: ����Android ID. 
                                                          ���Ϊ�ձ�ʾȡ��������: δ֪.

ʾ��:
    234912,1,115.214.168.179,59399,binjune225,iorl,300000,1,4,0,4399ר�ð�,BkSMSQFVimFKRpy0

"""

ACT_LOGIN               = 2     # ��¼��Ϊ:
'''
��ʽ�ֶΣ�               ����                          ˵��
ip                      �ַ���                         ��½��ԴIP����
port                    ����                           ��½��Դ�˿ں�
svrName                 �ַ���                         ��½��������
UserName                �ַ���                         ��½�û��û���
RegType                 ����                           �û�ע������:
                                                         0.��ͨע�� 
                                                         1.����ע��
                                                         2.QQע��
                                                         3.΢��ע��
                                                         9.������
flag                    ����                           ��½��ʾ��
                                                               1��������½
                                                               2�����߻ָ�
VersionNum              �ַ���                         ��Ϸ�汾ֵ
VersionString           �ַ���                         ��Ϸ�汾��
OSInfo                  �ַ���                         ϵͳ�汾��Ϣ
SystemLang              �ַ���                         ϵͳ����
ResInfo                 �ַ���                         ����ն˷ֱ���
MachineNo               �ַ���                         ����ն˻����ͺ�
NetInfo                 �ַ���                         ����ն�������ʽ

ʾ����
    182339,2,127.0.0.1,3104,localhost2235,_i.robot_77461,1,0,0.0.0,Python 2.6.5,Chinese,1920x1080,BenQ G2222HD,Enternet
'''

ACT_ONLINE              = 3     # �������,��ʱ����
'''
��ʽ�ֶΣ�               ����                          ˵��
srvName                 �ַ���                         ��������
Logining_users          ����                           ���ڵ�½�û�����
robots                  ����                           ���߻���������
users                   ����                           �����û��������
PK                      ����                           ����PK��������

ʾ����
    103341,3,localhost2235,0,1,0,0
'''


ACT_KEEPTIME            = 4     # �������ʱ��
'''
��ʽ�ֶΣ�               ����                          ˵��
srvName                 �ַ���                         ��������
userName                �ַ���                         ����û���
nickName                �ַ���                         ����ǳ�
DateTimeNow             �ַ�������-��-�գ�,             ��ǰ������
keepTime                �����ͣ�ʱ�����                ���һ�ε�¼���˴εǳ���ʱ��
mney                    ����                           ��ҵ�ǰ��Ǯ
ʾ����
    170043,4,localhost2235,ijqns2hl,˾����ӭ,2012-07-27,394.938000,100000
'''


ACT_RANK                = 5     # ���а�(��δ��Ӽ�¼)
'''
��ʽ�ֶ�                ����                          ˵��
SrvName                �ַ���                         ��������
userName               �ַ���                         ����û���
nickName               �ַ���                         ����ǳ�
mney                   ����                           ��ҽ��

ʾ����
    ����
'''


ACT_ONE_RESULT          = 6     # ���ÿ�ֽ����¼
'''
��ʽ�ֶ�                ����                          ˵��
UserName               �ַ���                         ����û���
nickName               �ַ���                         ����ǳ�
AIFlag                 ����                           AI��ʾ����ʾ���û��Ƿ�Ϊ�����ˣ���
                                                             1��Ϊ������
                                                             0���ǻ�����    
mfan                   ����                           �����
dtms                   ����                           �ܼӱ�����
AllCount               ����                           �ܾ���
WinCount               ����                           Ӯ����
title                  ����                           ��ҳƺ�
level                  ����                           ���ڷ���ȼ�
tile_count             ����                           һ�������Ʊ�ʾ(ȡֵΪ1��2���Ƹ���Ӧ��

ʾ����
    175550,6,ahnl13cf,��ԣϼ,0,13,0,1,1,0,2,1

'''


ACT_GAMERESULT          = 7     # ������Ϸ��¼����˫����ң�ÿ���ƽ����¼һ�Σ�
'''
��ʽ�ֶ�               ����                           ˵��
level                  ����                           ���ڷ���ȼ�
tile_count             ����                           һ�������Ʊ�ʾ��ȡֵΪ1��2���Ƹ���Ӧ��
round                  ����                           ��ǰ�غ�����������ͬ���֮����˶��ٻغϣ� 
AIFlag                 ����                           �����˱�ʶ��
                                                        0:�޻�����.
                                                        1:Ӯ���ǻ�����
                                                        2:��һ�����
                                                        3:Ӯ����Ҷ��ǻ�����
winner                 �ַ���                         Ӯ���û���
loser                  �ַ���                         �䷽�û���
base                   ����                           ÿ������
times                  ����                           ��ǰ����
fan                    ����                           �Ʒ���
double                 ����                           �ӱ�����
taskfan                ����                           ������
totalfan               ����                           �ܷ��� = �Ʒ��� * (2 ^ �ӱ�����) * ������
totalmoney             ����                           ��Ǯ�� = ÿ������ * ��ǰ���� * �ܷ���
loserMoneyOld          ����                           ��ҿ�Ǯ֮ǰ�Ľ���
loserMoneyNew          ����                           ��ҿ�Ǯ֮��Ľ���
loserMoneyCost         ����                           ���ʵ�ʿ�Ǯ
commission             ����                           ϵͳ��ˮǮ��
winnerMoneyAdd         ����                           Ӯ��ʵ�ʼ�Ǯ
winnerMoneyOld         ����                           Ӯ�Ҽ�Ǯ֮ǰ��Ǯ��
winnerMoneyNew         ����                           Ӯ�Ҽ�Ǯ֮���Ǯ��
ʾ��
    175550,7,3,2,5,2,binggo0,_i.robot_22344,2000,1,16,2,2,128,256000,255000,0,25500,500000,729500
'''


ACT_MISS_RESULT         = 8     # �ľ�
'''
��ʽ�ֶ�                ����                          ˵��
OwnerName              �ַ���                        �����ǳ���
AIFlag                 ����                          �����˱�ʶ��
                                                        0:�޻�����
                                                        1:�����ǻ�����
                                                        2:���ͻ�����
                                                        3��˫�����ǻ�����
OwnerNamePoint          ����                         ��������
ClientName             �ַ���                        �����ǳ���
ClientNamePotint       ����                          ���ͷ���
 
ʾ����
    ����
    
'''


ACT_LEVEL_PLAYING_ROOM  = 9     # �ڸ��ȼ���������ˣ��Ҹ�������ʱ��¼
'''
��ʽ�ֶ�                ����                          ˵��
levelRoom              ����                           ���ӵȼ�
playingCount           ����                           ������ˣ����

ʾ����
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


ACT_ERROR_OPCODE        = 10    # �쳣����opCode (�ݶ����壬δ��Ӽ�¼)
'''
��ʽ�ֶ�                ����                          ˵��
    ����

ʾ����
    ����
'''



ACT_IAP                 = 11    # IAP�ڹ���¼
'''
��ʽ�ֶ�                ����                          ˵��
UserName               �ַ���                         ����û���
nickName               �ַ���                         ����ǳ�
IAPType                ����                           IAP���ͣ�
                                                        1.�ȸ��ڹ�
                                                        2.AppStore
                                                        3.֧����
                                                        4.����
                                                        5.����
purchaseState          ����                           �ɹ�״̬��
                                                           0��purchased(����)
                                                           1��canceled(����)
                                                           2��refunded(�˿�)
                                                           3��expired, for subscription purchases only(����,ֻ���Ĺ���)
productId              �ַ���                         ��ƷID
money                  ����                           ��Ʒ��Ǯ
userOdlMney            ����                           ����ǰ��ҵĽ�Ǯ
userNewMney            ����                           �������ҵĽ�Ǯ
IAP_ID                 �ַ���                         IAP����
diamond                ����                           ��Ʒ��ʯ����
price                  ������                         �۸�(RMB)

ʾ����
    015717,11,zhuchunya526,tanya,3,0,��Ϸ��ֵ_200���,2000000,68000,2068000,AliPay:20120730015758564_mj_zhuchunya526,0,2.00
    121609,11,zhuchunya526,tanya,3,0,��Ϸ��ֵ_500���,5000000,0,5000000,AliPay:20120730121639260_mj_zhuchunya526,0,2.00

'''



ACT_ECONOMIC_LOG        = 13    # ϵͳ����ҽ�Ǯ��֧��¼
# QREG : ����ע���û�
# USER : ��ͨ�û�
# ROBOT : ������
# ����
ECONOMIC_INCOME         = 1                     # ϵͳ����
ECONOMIC_EXPEND         = 2                     # ϵͳ֧��
ECONOMIC_EXCHANGE       = 3                     # USER֮����֧
# ������: ������(1000 - 1999):
INCOME_ROBOT_WIN_USER   = 1000                  # USER��ROBOT(��ˮǰ)
INCOME_COMMISSION_USER_WIN_USER = 1001          # ���ӳ�ˮ: USERӮUSER
#INCOME_COMMISSION_USER_WIN_QREG = 1002         # ���ӳ�ˮ: USERӮQREG
#INCOME_COMMISSION_USER_WIN_ROBOT = 1003        # ���ӳ�ˮ: USERӮROBOT
INCOME_GM_RECOVER_USER  = 1004                  # GM��USERǮ
INCOME_QREG_WIN_USER    = 1005                  # USER��QREG(��ˮǰ)
# ������: ֧����(2000 - 2999):
EXPEND_USER_REG_GIFT    = 2000                  # USERע��ʱ����
EXPEND_USER_WIN_ROBOT   = 2001                  # USERӮROBOT(��ˮ��)
EXPEND_USER_WIN_QREG    = 2002                  # USERӮQREG(��ˮ��)
EXPEND_USER_DAILY_BONUS = 2003                  # USER������
EXPEND_USER_REVISIT_BONUS= 2004                 # USER��طý���
EXPEND_USER_CHARGE      = 2005                  # USER��ֵ��Ǯ
EXPEND_GM_SEND_USER     = 2006                  # GM����USERǮ
EXPEND_USER_TASK_DONE   = 2007                  # USER�������
EXPEND_USER_ACHI_DONE   = 2008                  # USER��ɳɾ�
EXPAND_DIAMOND_2_MONEY  = 2009                  # ��ʯ�һ����
EXPAND_ETERNAL_TIPS     = 2010                  # �������������
# ������: USER֮����֧��(3000 - 3999):
EXCHANGE_USER_LOSE_USER = 3000                  # USER��USER(��ˮǰ)
EXCHANGE_USER_WIN_USER  = 3001                  # USER��ӮUSER(��ˮ��)
'''
��ʽ�ֶ�               ����                           ˵��
type                   ����                           ����
sub_type               ����                           ������
amount                 ����                           Ǯ��
user                   �ַ���                         Ӱ�����
nick                   �ַ���                         �ǳ�
money                  ����                           ��Ҹ��º�Ľ�Ǯ

ʾ��
    123456,13,1,1000,52000,binggo0,������0,243300 # (������)Ӯ���binggo0Ǯ52000,ʣ��243300
    123456,13,1,1001,3500,binggo1,������0,233000  # ���ӳ�ˮ3500,���binggo0ʣ��233000
'''

ACT_CLIENT_EXCEPTION    = 14    # �ͻ����쳣����
"""
��ʽ�ֶ�:               ����                              ˵��
ip                      �ַ���                            ��ԴIP��ַ
port                    ����                              ��Դ�˿ں�
VersionNum              �ַ���                            ��Ϸ�汾ֵ
VersionString           �ַ���                            ��Ϸ�汾��
OSInfo                  �ַ���                            ϵͳ�汾��Ϣ
SystemLang              �ַ���                            ϵͳ����
ResInfo                 �ַ���                            ����ն˷ֱ���
MachineNo               �ַ���                            ����ն˻����ͺ�
NetInfo                 �ַ���                            ����ն�������ʽ

ʾ��:
    234912,14,115.214.168.179,59399,0,0.0.0,Python 2.6.5,Chinese,1920x1080,BenQ G2222HD,Enternet
"""

ACT_CLICK_LOG           = 15    # �����¼
"""
��ʽ�ֶ�:               ����                              ˵��
UserName                �ַ���                            �û���
ClickName               �ַ���                            ���������
ClickAddTime            ����                              �����������

ʾ��:
    234912,15,binggo0,�������ٳ�ֵ,2
"""

ACT_ITEM_LOG            = 16    # ���߼�¼(������ʯ)
# ����
ITEM_GOT                = 1                     # ��һ�õ���
ITEM_COST               = 2                     # ������ĵ���
# ������: ���
GOT_CHARGE              = "��ֵ���"
GOT_SHOP                = "�̵깺��"
GOT_GM_SEND             = "GM����"
# ������: ����
COST_SHOP               = "�̵�����"
COST_USE                = "����ʹ��"
COST_GM_RECOVER         = "GM�ջ�"
COST_PASSIVE            = "����ʹ��"
"""
��ʽ�ֶ�:               ����                              ˵��
UserName                �ַ���                            �û���
ItemLogType             ����                              ����
ItemLogSubType          �ַ���                            ������
ItemName                �ַ���                            ������
ItemCount               ����                              ��������

ʾ��:
    234912,16,binggo0,1,��ֵ���,��ʯ,100
    234912,16,binggo0,2,�̵�����,��ʯ,20
    234912,16,binggo0,1,�̵깺��,PK��,1
    234913,16,binggo0,2,ʹ������,PK��,1
"""


##########################################################################################

'''
�ӿڰ���
    import activity
    from log import log_activity

�ӿں�����
    log_activity(fmt, *args)tt

���ӣ�
    log_activity("%d,%s",activity.ACT_***,"value")
'''

