# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 10:56:00 2022

@author: jonahLiu
"""
from time import strptime
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging

from datetime import date,time
import pytz
import sqlite3
import os

bibleStart = date(2022,1,1)
notifyTime = time(hour=6, tzinfo=pytz.timezone('Asia/Shanghai'))
reminderTime=time(hour=22,tzinfo=pytz.timezone('Asia/Shanghai'))
database =  os.path.join(os.path.split(os.path.realpath(__file__))[0],'./EingediBibleRead.db')
# 日志
logging.basicConfig(format='%(asctime)s-%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def hello(update: Updater, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}, 我是隐基底读经机器人。'+'''
本服务由隐基底教会同工开发，欢迎加入开发队伍。
项目运行需要一定的成本，目前依托于隐基底教会的厦园雅歌公众号平台 songs.eingedixm.cf 欢迎弟兄姐妹奉献支持。
如需奉献可奉献至隐基底教会或巡司顶母会。
如遇异常请联系隐基底教会同工。''')


def today(update: Updater, context: CallbackContext) -> None:
    todaybible = getTodayBibleChapters(database)
    greeting = f'Bonjour {update.effective_user.first_name} ! \n'
    update.message.reply_text(greeting + '\n' + todaybible)


# MessageHandler
from telegram.ext import MessageHandler,Filters
def echo(update: Updater, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def caps(update: Update, context: CallbackContext):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


# 主动发消息
def start(update: Updater, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="我是隐基底的读经机器人，但是读经的时候请不要做机器人~")
    
def subscribe(update: Updater, context: CallbackContext) -> None:
    command = f"INSERT OR IGNORE INTO USERS (CHAT_ID,START_DAY,ENCRY_NAME) VALUES ({update.effective_chat.id},date('now'),'{update.effective_user.first_name}')"
    updateDB(database,command)
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text=f'你好{update.effective_user.first_name}\n'+"订阅成功！\n将在{}时间每天{}点{}分进行提醒！\n"
                             .format(notifyTime.tzname(),notifyTime.hour,notifyTime.minute))
    
def unsubscribe(update: Updater, context: CallbackContext) -> None:
    command = "DELETE FROM USERS WHERE CHAT_ID==%d"%update.effective_chat.id
    updateDB(database,command)
    update.message.reply_text('退订成功。')


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
                                        + "\n今日已打卡！ \n\n 当前打卡总天数：{}\n\n 上次打卡时间：{}。当前打卡率{:.2%}".format(checkedDay+1, lastday, checkpercentage)
                                    )
    else:
        update.message.reply_text(f'Bonjour {update.effective_user.first_name} !，数据库还没有您的信息，请先注册 /subscribe 再打卡哦！')

def updateDB(database,command):
    connDB = sqlite3.connect(database)
    ret =  connDB.cursor().execute(command).fetchall()
    connDB.commit()
    return ret
    
def getTodayBibleChapters(database='./EingediBibleRead.db'):
    today = (date.today()-bibleStart).days + 1
    command = 'SELECT YEARS,BOOKS,CHAPTER_START,CHAPTER_END FROM SCRIPTS WHERE DAYS==%d'%today
    
    YBCC = updateDB(database, command)[0]
    todaybible = '今天是{}，这是读经计划的第{}年，第{}天。\n\n 今天的经文是： {} {}-{}'.format(
        date.today().strftime('%Y年%m月%d日'),
        YBCC[0],
        today,
        YBCC[1],
        YBCC[2],
        YBCC[3])
    
    return todaybible

def dailyBonjour(context:CallbackContext):
    chatIDs= updateDB(os.path.join(os.path.split(os.path.realpath(__file__))[0],'./EingediBibleRead.db'),
             'SELECT CHAT_ID FROM USERS')
    for chatID in chatIDs:
        cmdDaily = "UPDATE USERS SET IS_CHECKED = 0 WHERE CHAT_ID==%d"%chatID[0]
        updateDB(database,cmdDaily)

        replyText = "Bonjour 这里是每日推送！\n\n" + getTodayBibleChapters(database)
        updater.bot.sendMessage(chat_id=chatID[0],
                            text=replyText)
        
def dailyReminder(context:CallbackContext):
    chatIDs= updateDB(os.path.join(os.path.split(os.path.realpath(__file__))[0],'./EingediBibleRead.db'),
             'SELECT CHAT_ID,ENCRY_NAME FROM USERS WHERE IS_CHECKED==0')
    
    for chatID in chatIDs:
        replyText = "Bonjour %s \n这里是每日提醒！\n\n今天还没有打卡（/checkin）哦! \n\n"%chatID[1] + getTodayBibleChapters(database)
        updater.bot.sendMessage(chat_id=chatID[0],
                            text=replyText)
    
    
updater = Updater(os.environ['TELE_KEY'])

updater.job_queue.run_daily(dailyBonjour,notifyTime)
updater.job_queue.run_daily(dailyReminder,reminderTime)
# command注册
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('today', today))
updater.dispatcher.add_handler(CommandHandler('subscribe', subscribe))
updater.dispatcher.add_handler(CommandHandler('unsubscribe', unsubscribe))
updater.dispatcher.add_handler(CommandHandler('checkin', checkin))

# Message Handler注册
updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))




updater.start_polling()
updater.idle()

