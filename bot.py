'''
Author: Jonah Liu
Date: 2022-01-03 19:19:36
LastEditTime: 2022-01-25 19:56:43
LastEditors: Jonah Liu
Description: 
'''
# -*- coding: utf-8 -*-

from telegram.ext import Updater
import logging

from commands import *
from jobs import *
from config import *


# 日志

logging.basicConfig(format='%(asctime)s-%(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


# command注册
cmds = {
    'hello':hello, 
    'start':start,
    'today':today,
    'subscribe':subscribe,
    'unsubscribe':unsubscribe,
    'checkin':checkin
    }

# jobs注册
jobs = (
    {'name':dailyBonjour,'time':notifyTime},
    {'name':dailyReminder,'time':reminderTime}
)

if __name__ == "__main__":
    updater = Updater(os.environ['TELE_KEY'])

    registCommands(updater, cmds)
    registJobs(updater,jobs)

    updater.start_polling()
    updater.idle()
