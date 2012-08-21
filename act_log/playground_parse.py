#!/usr/bin/env python
# -*- coding: gbk -*-
"""�����õ����ӵ���ϸ���ݣ��������õ����ݵ��ڼ��뵽����Ŀ���
"""

import codecs

MAHJONG_LEVELS = [
{1:"��ս��(����)"},
{2:"��ս��(����)"},
{3:"���ֳ�(����)"},
{4:"���ֳ�(����)"},
{5:"������(����)"},
{6:"������(����)"},
{7:"�м���(����)"},
{8:"�м���(����)"},
{9:"�߼���(����)"},
{10:"�߼���(����)"},
{11:"ȸ��(����)"},
{12:"ȸ��(����)"},
                  ]

def vs(little, large):
    return 0 if not large else little * 100 / large

class summary(object):
    def __init__(self, level):
        self.level = level
        self.level_id = 999 if level not in MAHJONG_LEVELS else MAHJONG_LEVELS.index(level)
        self.total_round = 0
        self.user_round  = 0
        self.robot_round = 0
        self.robot_win_round = 0
        self.robot_win_money = 0
        self.robot_lose_money = 0
        self.commission = 0
        self.robot_clear_user_round = 0
        self.user_clear_robot_round = 0
        self.user_clear_user_round = 0


    def __add__(self, other):
        self.total_round += other.total_round
        self.user_round += other.user_round
        self.robot_round += other.robot_round
        self.robot_win_round += other.robot_win_round
        self.robot_win_money += other.robot_win_money
        self.robot_lose_money += other.robot_lose_money
        self.commission += other.commission
        self.robot_clear_user_round += other.robot_clear_user_round
        self.user_clear_robot_round += other.user_clear_robot_round
        self.user_clear_user_round += other.user_clear_user_round
        return self

    def __str__(self):
        fmt = "%d\t%s"+"\t%d"*18
        return fmt % \
               (self.level_id,
                self.level,
                self.total_round,
                self.user_round,
                self.robot_round,
                vs(self.robot_round, self.total_round),
                self.robot_win_round,
                vs(self.robot_win_round, self.robot_round),
                self.robot_win_money,
                self.robot_lose_money,
                vs(self.robot_win_money, self.robot_lose_money),
                self.commission,
                self.robot_win_money + self.commission - self.robot_lose_money,
                vs(self.robot_win_money + self.commission, self.robot_lose_money),
                self.robot_clear_user_round,
                vs(self.robot_clear_user_round, self.robot_round),
                self.user_clear_robot_round,
                vs(self.user_clear_robot_round, self.robot_round),
                self.user_clear_user_round,
                vs(self.user_clear_user_round, self.user_round))

    @staticmethod
    def header():
        return "����ID\t"\
               "����\t"\
               "�ܻغ���\t"\
               "��һغ���\t"\
               "�����غ���\t"\
               "�����˲�����%\t"\
               "������Ӯ�غ���\t"\
               "������Ӯ��%\t"\
               "������ӮǮ\t"\
               "��������Ǯ\t"\
               "������Ӯ��Ǯ��%\t"\
               "��ˮ\t"\
               "ϵͳӯ��\t"\
               "ϵͳӮ��Ǯ��%\t"\
               "����������û��غ�\t"\
               "����������û���%\t"\
               "�û���ջ����˻غ�\t"\
               "�û���ջ�������%\t"\
               "�û�����ջغ�\t"\
               "�û��������%"

def parse_file(filename):
    lines = open(filename, "r").readlines()
    summary_levels = {}
    for level in MAHJONG_LEVELS:
        summary_levels[level] = summary(level)

    def parse_line(line):
        # ����	Ӯ��	���	��ֵ	���Ǯ��	��ˮ	Ӯ��Ǯ��
        # �߼���	xiaoyun8902(��������)	_i.robot_33761(�����zy)	4320000	489545500	864000	252471897
        l = line.strip().split(',')
        if l[1] != '7':
            return
        #print l
        level,winner,loser,totalmoney,losermoney,commission,winnermoney = l[2],\
                                                                          l[6],\
                                                                          l[7],\
                                                                          int(l[14]),\
                                                                          int(l[15]),\
                                                                          int(l[18]),\
                                                                          int(l[20])
        # print level,winner,loser,totalmoney,losermoney,commission,winnermoney
        levelname = MAHJONG_LEVELS[int(level)]
        s = summary_levels[levelname]

        s.total_round += 1
        loser_cost_money = min(losermoney, totalmoney)
        winner_add_money = loser_cost_money - commission
        # ������Ӯ
        if '_i.robot_' in winner:
            s.robot_round += 1
            s.robot_win_round += 1
            s.robot_win_money += loser_cost_money
            if loser_cost_money >= losermoney:
                s.robot_clear_user_round += 1
        # ��������
        elif '_i.robot_' in loser:
            s.robot_round += 1
            s.robot_lose_money += loser_cost_money
            s.commission += commission
            if loser_cost_money >= losermoney:
                s.user_clear_robot_round += 1
        # ���֮��
        else:
            s.user_round += 1
            s.commission += commission
            if loser_cost_money >= losermoney:
                s.user_clear_user_round += 1


    for i in xrange(len(lines)):
        parse_line(lines[i])

    header = summary.header()

    output_file = codecs.open(filename+".result.csv", "w", "utf-16")
    output_file.write(u"%s\n" % header.decode('gbk'))
    all_summary = summary("����")
    for k, v in sorted(summary_levels.items(), key=lambda (k,v): v.level_id):
        #for v in summary_levels.values():
        output_file.write(u"%s\n" % str(v).decode('gbk'))
        all_summary += v
    output_file.write(u"%s\n" % str(all_summary).decode('gbk'))
    
if __name__ == "__main__":
    parse_file("D:/www/pyscripts/log/activity.gamesvc.localhost2235.log.20120820")
    

