'''
Author: Jonah Liu
Date: 2022-01-25 19:21:23
LastEditTime: 2022-02-09 15:46:40
LastEditors: Jonah Liu
Description: 
'''

from telegram import InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Updater, CallbackContext
import os

# import important variable
from functions import updateDB,getTodayBibleChapters,build_menu,getSystemInformation
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
    
    keyboard = [
        InlineKeyboardButton("查看往期XSD读经心得",callback_data="XSD"),
        InlineKeyboardButton("查看隐基底读经心得",callback_data="EGD")
    ]

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
                                ),
                            reply_markup=InlineKeyboardMarkup(build_menu(keyboard,1))
                            )

def testReminder(context:CallbackContext):
    config.todayCount = (date.today()-config.bibleStart).days + 1

    for adminID in config.adminIDs:
        context.bot.sendMessage(chat_id=adminID,
                        text='\n'.join(getSystemInformation())
                                )
