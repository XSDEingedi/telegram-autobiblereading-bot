'''
Author: Jonah Liu
Date: 2022-01-26 12:01:57
LastEditTime: 2022-01-28 12:32:44
LastEditors: Jonah Liu
Description: 


def callback_dummy(update: Updater, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f"Selected option: {query.data}")
'''


import logging
from telegram.ext import Updater,CallbackContext
import telegram
from functions import updateDB,findFiles
import config 

def callback_button(update: Updater, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    # query.answer()

    reply = query.data
    chatid = update.effective_chat.id
    if reply == 'XSD':
        query.answer("查找往期库文件...")
        years =  updateDB(config.database,"SELECT YEARS FROM SCRIPTS WHERE DAYS==%d"%config.todayCount)[0][0]
        fileID,notes = updateDB(config.database,"SELECT XSD_FILE_ID,XSD_NOTES FROM NOTES WHERE DAYS==%d"%config.todayCount)[0]
        if fileID == None:
            filePrefix = f'Y{years:1d}D{config.todayCount:03d}'
            fileLst= findFiles(filePrefix)
            logging.debug(filePrefix)
            logging.debug(fileLst)
            if len(fileLst)==0:
                query.answer('No found file(s) about today')
                return
            
            file_id = [context.bot.send_document(
                chat_id=chatid,
                document=open(f,'rb')
                ).document.file_id for f in fileLst] 
            logging.debug(f"UPDATE SCRIPTS SET XSD_FILE_ID=\"{file_id}\" WHERE DAYS=={config.todayCount}")
            updateDB(config.database,f"UPDATE NOTES SET XSD_FILE_ID=\"{file_id}\" WHERE DAYS=={config.todayCount}")
        else:
            logging.info("SendFileVia ID")
            idList = fileID.replace('[','').replace(']','').replace('\'','').split(',')
            logging.info(idList)
            [context.bot.send_document(
                    chat_id=chatid,
                    document=fid
                ) for fid in idList]
        logging.info(f"Send MSG..{len(notes)}")
        if not notes==None:
            context.bot.send_message(
                chat_id = chatid,
                text=notes.replace('\n','\n\n'),
                parse_mode=telegram.ParseMode.HTML
                )
    elif reply == 'EGD':
        query.answer("功能还未开放")
    else:
        query.answer()

