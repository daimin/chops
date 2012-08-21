#!/usr/bin/env python
# -*- coding: gbk -*-
"""用来得到场子的详细数据，从这里拿到数据到在加入到具体的库中
"""

import codecs

MAHJONG_LEVELS = [
{1:"对战场(经典)"},
{2:"对战场(豪快)"},
{3:"新手场(经典)"},
{4:"新手场(豪快)"},
{5:"初级场(经典)"},
{6:"初级场(豪快)"},
{7:"中级场(经典)"},
{8:"中级场(豪快)"},
{9:"高级场(经典)"},
{10:"高级场(豪快)"},
{11:"雀神场(经典)"},
{12:"雀神场(豪快)"},
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
        return "场子ID\t"\
               "场子\t"\
               "总回合数\t"\
               "玩家回合数\t"\
               "机器回合数\t"\
               "机器人参与率%\t"\
               "机器人赢回合数\t"\
               "机器人赢率%\t"\
               "机器人赢钱\t"\
               "机器人输钱\t"\
               "机器人赢输钱比%\t"\
               "抽水\t"\
               "系统盈亏\t"\
               "系统赢输钱比%\t"\
               "机器人清空用户回合\t"\
               "机器人清空用户率%\t"\
               "用户清空机器人回合\t"\
               "用户清空机器人率%\t"\
               "用户间清空回合\t"\
               "用户间清空率%"

def parse_file(filename):
    lines = open(filename, "r").readlines()
    summary_levels = {}
    for level in MAHJONG_LEVELS:
        summary_levels[level] = summary(level)

    def parse_line(line):
        # 场子	赢家	输家	总值	输家钱数	抽水	赢家钱数
        # 高级场	xiaoyun8902(我能日天)	_i.robot_33761(青胡子zy)	4320000	489545500	864000	252471897
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
        # 机器人赢
        if '_i.robot_' in winner:
            s.robot_round += 1
            s.robot_win_round += 1
            s.robot_win_money += loser_cost_money
            if loser_cost_money >= losermoney:
                s.robot_clear_user_round += 1
        # 机器人输
        elif '_i.robot_' in loser:
            s.robot_round += 1
            s.robot_lose_money += loser_cost_money
            s.commission += commission
            if loser_cost_money >= losermoney:
                s.user_clear_robot_round += 1
        # 玩家之间
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
    all_summary = summary("汇总")
    for k, v in sorted(summary_levels.items(), key=lambda (k,v): v.level_id):
        #for v in summary_levels.values():
        output_file.write(u"%s\n" % str(v).decode('gbk'))
        all_summary += v
    output_file.write(u"%s\n" % str(all_summary).decode('gbk'))
    
if __name__ == "__main__":
    parse_file("D:/www/pyscripts/log/activity.gamesvc.localhost2235.log.20120820")
    

