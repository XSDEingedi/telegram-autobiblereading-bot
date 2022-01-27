'''
Author: Jonah Liu
Date: 2022-01-25 19:21:23
LastEditTime: 2022-01-27 12:23:22
LastEditors: Jonah Liu
Description: 
'''

from telegram.ext import Updater, CallbackContext

# import important variable
from functions import updateDB,getTodayBibleChapters
from datetime import date
import config

def dailyReminder(context:CallbackContext):
    chatIDs= updateDB(config.database,'SELECT CHAT_ID,ENCRY_NAME FROM USERS WHERE IS_CHECKED==0')
    
    for chatID in chatIDs:
        # replyText = "Bonjour %s \n这里是每日提醒！\n\n今天还没有打卡（/checkin）哦! \n\n"%chatID[1] + getTodayBibleChapters(config.database)
        context.bot.sendMessage(chat_id=chatID[0],
                            text=config.Msg.reminderMsg.format(
                                user = chatID[1],
                                todayDate=date.today().strftime('%Y年%m月%d日'),
                                YBCC=getTodayBibleChapters(config.database),
                                todayCount=config.todayCount  
                                )
                            )



def dailyBonjour(context:CallbackContext):
    config.todayCount = (date.today()-config.bibleStart).days + 1
    
    chatIDs= updateDB(config.database,'SELECT CHAT_ID,ENCRY_NAME FROM USERS')
    for chatID in chatIDs:
        cmdDaily = "UPDATE USERS SET IS_CHECKED = 0 WHERE CHAT_ID==%d"%chatID[0]
        updateDB(config.database,cmdDaily)

        context.bot.sendMessage(chat_id=chatID[0],
                            text=config.Msg.bonjourMsg.format(
                                user=chatID[1],
                                todayDate=date.today().strftime('%Y年%m月%d日'),
                                YBCC=getTodayBibleChapters(config.database),
                                todayCount=config.todayCount  
                                )
                            )

def testReminder(context:CallbackContext):
    adminID = 949189546
    config.todayCount = (date.today()-config.bibleStart).days + 1


    context.bot.sendMessage(chat_id=adminID,
                        text="[TEST]\n\n" + config.Msg.bonjourMsg.format(
                                user="WHOM EVER CONCERN",
                                todayDate=date.today().strftime('%Y年%m月%d日'),
                                YBCC=getTodayBibleChapters(config.database),
                                todayCount=config.todayCount  )
                                )
