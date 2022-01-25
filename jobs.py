'''
Author: Jonah Liu
Date: 2022-01-25 19:21:23
LastEditTime: 2022-01-25 19:52:23
LastEditors: Jonah Liu
Description: 
'''

from telegram.ext import Updater, CallbackContext

# import important variable
from functions import updateDB,getTodayBibleChapters
from config import database


def dailyReminder(context:CallbackContext):
    chatIDs= updateDB(database,'SELECT CHAT_ID,ENCRY_NAME FROM USERS WHERE IS_CHECKED==0')
    
    for chatID in chatIDs:
        replyText = "Bonjour %s \n这里是每日提醒！\n\n今天还没有打卡（/checkin）哦! \n\n"%chatID[1] + getTodayBibleChapters(database)
        updater.bot.sendMessage(chat_id=chatID[0],
                            text=replyText)



def dailyBonjour(context:CallbackContext):
    chatIDs= updateDB(database,'SELECT CHAT_ID FROM USERS')
    for chatID in chatIDs:
        cmdDaily = "UPDATE USERS SET IS_CHECKED = 0 WHERE CHAT_ID==%d"%chatID[0]
        updateDB(database,cmdDaily)

        replyText = "Bonjour 这里是每日推送！\n\n" + getTodayBibleChapters(database)
        updater.bot.sendMessage(chat_id=chatID[0],
                            text=replyText)
    