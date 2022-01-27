'''
Author: Jonah Liu
Date: 2022-01-03 19:19:36
LastEditTime: 2022-01-27 20:38:41
LastEditors: Jonah Liu
Description: 
'''
# -*- coding: utf-8 -*-

from pdb import Restart
from telegram.ext import Updater,Filters
import logging
from threading import Thread
import sys

from commands import *
from jobs import *
from callback_Function import *
from config import *

config.todayCount = (date.today()-config.bibleStart).days + 1

# 日志

logging.basicConfig(format='%(asctime)s-%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


# command注册
cmds = {
    'hello':hello, 
    'start':start,
    'today':today,
    'subscribe':subscribe,
    'unsubscribe':unsubscribe,
    'checkin':checkin,
    }

# jobs注册
jobs = (
    {'name':dailyBonjour, 'time':notifyTime},
    {'name':dailyReminder,'time':reminderTime},
    {'name':testReminder, 'time':testTime}

)


# callback Functions注册
callbackFuncs = [
    callback_button
]

def stop_and_restart():
        """Gracefully stop the Updater and replace the current process with a new one"""
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)


def restart(update, context):
        update.message.reply_text('Bot is restarting...')
        Thread(target=stop_and_restart).start()


if __name__ == "__main__":
    updater = Updater(os.environ['TELE_KEY'])

    registCommands(updater, cmds)
    registCallback(updater,callbackFuncs)
    # updater.dispatcher.add_handler(CallbackQueryHandler(callback_button))
    registJobs(updater,jobs)
    
    updater.dispatcher.add_handler(CommandHandler('r', restart, filters=Filters.user(username='@ShuayLiu')))

    updater.start_polling()
    updater.idle()

    


