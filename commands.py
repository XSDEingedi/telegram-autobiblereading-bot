'''
Author: Jonah Liu
Date: 2022-01-25 18:13:02
LastEditTime: 2022-02-10 14:59:07
LastEditors: Jonah Liu
Description: commands for TeleBot
'''

from telegram import InlineKeyboardMarkup, Update,InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext

from functions import *
from config import database,notifyTime,bibleStart,Msg

def hello(update: Updater, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}' + Msg.iAmMsg + Msg.introMsg)


def start(update: Updater, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text=Msg.iAmMsg)



def subscribe(update: Updater, context: CallbackContext) -> None:
    command = "INSERT OR IGNORE INTO USERS (CHAT_ID,START_DAY,ENCRY_NAME) VALUES (%d,date('now'),'%s')"%(update.effective_chat.id,update.effective_chat.first_name)
    updateDB(database,command)
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text=Msg.subscribRplMsg.format(
                                 tzone=notifyTime.tzname(),
                                 hour =notifyTime.hour,
                                 minute=notifyTime.minute
                                 )
                            )



def unsubscribe(update: Updater, context: CallbackContext) -> None:
    command = "DELETE FROM USERS WHERE CHAT_ID==%d"%update.effective_chat.id
    updateDB(database,command)
    update.message.reply_text(Msg.unscubscribeRplMsg)



def today(update: Updater, context: CallbackContext) -> None:
    YBCC = getTodayBibleChapters(database)

    keyboard = [
        InlineKeyboardButton("查看往期XSD读经心得",callback_data="XSD"),
        InlineKeyboardButton("查看隐基底读经心得",callback_data="EGD")
    ]
    replyMsg = config.Msg.bonjourMsg.format(
                                user=update.effective_user.first_name,
                                todayDate=date.today().strftime('%Y年%m月%d日'),
                                YBCC=YBCC,
                                todayCount=config.todayCount
                                )
    update.message.reply_text(text= replyMsg,
                            reply_markup=InlineKeyboardMarkup(build_menu(keyboard,1))
                            )



def checkin(update: Updater, context: CallbackContext) ->None:
    # check ENCRY_NAME

    cmdSelect ="SELECT START_DAY,LAST_DAY,CHECKED_DAY,IS_CHECKED,ENCRY_NAME FROM USERS WHERE CHAT_ID==%d"%update.effective_chat.id
    ret = updateDB(database,cmdSelect)[0]

    if ret:    
        _,lastday,checkedDay,isChecked,EncryName = ret
        if EncryName is None:
            updateDB(database,"UPDATE USERS SET ENCRY_NAME='%s'"%update.effective_user.first_name)
            
        startDay = list(map(int,_.split('-')))
        if isChecked:
            update.message.reply_text(Msg.alreadyChecked.format(user=update.effective_user.first_name))
        else:
            cmdUpdate = "UPDATE USERS SET LAST_DAY=date('now'), CHECKED_DAY=%d, IS_CHECKED=True WHERE CHAT_ID == %d"%(checkedDay+1,update.effective_chat.id)
            updateDB(database,cmdUpdate)
            # checkpercentage = (checkedDay+1)/((date.today()-date(startDay[0],startDay[1],startDay[2])).days + 1)
            update.message.reply_text(Msg.checkinRply.format(
                                        user = update.effective_user.first_name,
                                        checkedDay = checkedDay+1, 
                                        lastDay = lastday, 
                                        percentage = (checkedDay+1)/((date.today()-date(startDay[0],startDay[1],startDay[2])).days + 1))
                                    )
    else:
        update.message.reply_text(Msg.userNotFound.format(
            user = update.effective_user.first_name
            )
        )


def ping(update: Updater, context: CallbackContext) ->None:
    if update.effective_chat.id in config.adminIDs:
        rplyText = '\n'.join(getSystemInformation())
        
        context.bot.send_message(chat_id=update.effective_chat.id, 
                             text=rplyText)