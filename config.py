'''
Author: Jonah Liu
Date: 2022-01-25 19:43:50
LastEditTime: 2022-01-27 13:42:26
LastEditors: Jonah Liu
Description: common vars
'''
import pytz
import os
from datetime import date,time

class stru:
    pass


database =  os.path.join(os.path.split(os.path.realpath(__file__))[0],'./EingediBibleRead.db')
notesDir = os.path.join(os.path.split(os.path.realpath(__file__))[0],'./ReadNotes/')
notesLst = []

bibleStart     = date(2022,1,1)
notifyTime     = time(hour=6,tzinfo=pytz.timezone('Asia/Shanghai'))
reminderTime   = time(hour=22,tzinfo=pytz.timezone('Asia/Shanghai'))

testTime     = time(hour=12,minute=47,tzinfo=pytz.timezone('Asia/Shanghai'))

todayCount = -1




Msg = stru()

Msg.iAmMsg = "我是隐基底的读经机器人，但是读经的时候请不要做机器人~"
Msg.introMsg = '''
本服务由隐基底教会同工开发，欢迎加入开发队伍。
项目运行需要一定的成本，目前依托于隐基底教会的厦园雅歌公众号平台 songs.eingedixm.cf 欢迎弟兄姐妹奉献支持。
如需奉献可奉献至隐基底教会或巡司顶母会。
如遇异常请联系隐基底教会同工。'''

Msg.scriptMsg = "今天是{todayDate}，这是读经计划的第{YBCC[0]}年，第{todayCount}天。\n\n 今天的经文是： {YBCC[1]} {YBCC[2]}-{YBCC[3]}"
Msg.bonjourMsg = "Bonjour {user} 这里是每日推送 ! \n\n " + Msg.scriptMsg
Msg.reminderMsg = "Bonjour {user} \n这里是每日提醒！\n\n今天还没有打卡（/checkin）哦! \n\n "+ Msg.scriptMsg

Msg.subscribRplMsg = "订阅成功！\n将在{tzone}时间每天{hour}点{minute}分进行提醒！\n"
Msg.unscubscribeRplMsg = "退订成功！ byebye~"

Msg.userNotFound = "Bonjour {user}!，数据库还没有您的信息，请先注册 /subscribe 再打卡哦！"
Msg.alreadyChecked = "Bonjour {user} !，今天已经打过卡啦！"
Msg.checkinRpl = "Bonjour {user}! \n今日已打卡！ \n\n 当前打卡总天数：{checkedDay}\n\n 上次打卡时间：{lastDay}。当前打卡率{percentage:.2%}"