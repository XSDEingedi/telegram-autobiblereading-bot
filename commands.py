'''
Author: Jonah Liu
Date: 2022-01-25 18:13:02
LastEditTime: 2022-01-25 20:04:28
LastEditors: Jonah Liu
Description: commands for TeleBot
'''

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from functions import *
from config import introMsg,database,notifyTime,bibleStart


def hello(update: Updater, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}, 我是隐基底读经机器人。'+ introMsg)



def start(update: Updater, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="我是隐基底的读经机器人，但是读经的时候请不要做机器人~")



def subscribe(update: Updater, context: CallbackContext) -> None:
    command = "INSERT OR IGNORE INTO USERS (CHAT_ID,START_DAY) VALUES (%d,date('now'))"%update.effective_chat.id
    updateDB(database,command)
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="订阅成功！\n将在{}时间每天{}点{}分进行提醒！\n"
                             .format(notifyTime.tzname(),notifyTime.hour,notifyTime.minute))



def unsubscribe(update: Updater, context: CallbackContext) -> None:
    command = "DELETE FROM USERS WHERE CHAT_ID==%d"%update.effective_chat.id
    updateDB(database,command)
    update.message.reply_text('退订成功。')



def today(update: Updater, context: CallbackContext) -> None:
    YBCC = getTodayBibleChapters(bibleStart,database)[0]
    print(YBCC)
    update.message.reply_text( f'Bonjour {update.effective_user.first_name} ! \n' 
                            + '\n' 
                            + f"今天是{date.today().strftime('%Y年%m月%d日')}，这是读经计划的第{YBCC[0]}年，第{(date.today()-bibleStart).days + 1}天。\n"
                            + f"\n 今天的经文是： {YBCC[1]} {YBCC[2]}-{YBCC[3]}")



def checkin(update: Updater, context: CallbackContext) ->None:
    cmdSelect ="SELECT START_DAY,LAST_DAY,CHECKED_DAY,IS_CHECKED FROM USERS WHERE CHAT_ID==%d"%update.effective_chat.id
    ret = updateDB(database,cmdSelect)[0]

    if ret:    
        _,lastday,checkedDay,isChecked = ret
        startDay = list(map(int,_.split('-')))
        if isChecked:
            update.message.reply_text(f'Bonjour {update.effective_user.first_name} !，今天已经打过卡啦！')
        else:
            cmdUpdate = "UPDATE USERS SET LAST_DAY=date('now'), CHECKED_DAY=%d, IS_CHECKED=True WHERE CHAT_ID == %d"%(checkedDay+1,update.effective_chat.id)
            updateDB(database,cmdUpdate)
            checkpercentage = (checkedDay+1)/((date.today()-date(startDay[0],startDay[1],startDay[2])).days + 1)
            update.message.reply_text(f"Bonjour {update.effective_user.first_name}! " 
                                        + "\n今日已打卡！ \n\n 当前打卡总天数：{}\n\n 上次打卡时间：{}。当前打卡率{:.2%}"
                                        .format(checkedDay+1, lastday, checkpercentage)
                                    )
    else:
        update.message.reply_text(f'Bonjour {update.effective_user.first_name} !，数据库还没有您的信息，请先注册 /subscribe 再打卡哦！')

