'''
Author: Jonah Liu
Date: 2022-01-25 19:43:50
LastEditTime: 2022-01-25 19:45:47
LastEditors: Jonah Liu
Description: common vars
'''
import pytz
import os
from datetime import date,time



bibleStart     = date(2022,1,1)
notifyTime     = time(hour=6,tzinfo=pytz.timezone('Asia/Shanghai'))
reminderTime   = time(hour=22,tzinfo=pytz.timezone('Asia/Shanghai'))

introMsg = '''
本服务由隐基底教会同工开发，欢迎加入开发队伍。
项目运行需要一定的成本，目前依托于隐基底教会的厦园雅歌公众号平台 songs.eingedixm.cf 欢迎弟兄姐妹奉献支持。
如需奉献可奉献至隐基底教会或巡司顶母会。
如遇异常请联系隐基底教会同工。'''

database =  os.path.join(os.path.split(os.path.realpath(__file__))[0],'./EingediBibleRead.db')
