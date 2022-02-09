'''
Author: Jonah Liu
Date: 2022-01-26 12:01:57
LastEditTime: 2022-02-09 16:02:42
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


from datetime import date
import logging
from telegram.ext import Updater,CallbackContext
import telegram
from functions import updateDB,findFiles,getTodayBibleChapters,publishToTypecho
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
                context.bot.send_message(chat_id=chatid,text='No found file(s) about today')
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
        query.answer()
        context.bot.send_message(
            chat_id = chatid,
            text=f'<a href="{config.Site.url}">{config.Site.url}</a>',
            parse_mode=telegram.ParseMode.HTML
            )
    else:
        query.answer()


def channel_callback(update: Updater, context: CallbackContext) -> None:
    logging.debug("-----------------Channel CALLBACK-----------------")
    logging.debug(update.channel_post.chat.id)
    if update.channel_post.chat.id in config.channelIDs:
        YBCC = getTodayBibleChapters(config.database)
        title =  date.today().strftime('%Y年%m月%d日') + f' {YBCC[1]}:{YBCC[2]}-{YBCC[3]}'
       
        channelContent = update.channel_post.text
        publishToTypecho(url=config.Site.rpcUrl,
                        content=channelContent.replace('\n','\n\n'),
                        title=title,
                        username=config.Site.username,
                        passwd=config.Site.password)
