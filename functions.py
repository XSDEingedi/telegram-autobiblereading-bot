'''
Author: Jonah Liu
Date: 2022-01-25 18:30:21
LastEditTime: 2022-01-27 14:40:10
LastEditors: Jonah Liu
Description:  Functions for pyTelegrambot
'''
import sqlite3
from datetime import date,time
from telegram import Update
from telegram.ext import Updater, CommandHandler,CallbackQueryHandler
import config
import os 

def registCommands(updater:Updater,cmdDict:dict):
    for funcStrName,funcName in cmdDict.items():
        updater.dispatcher.add_handler(CommandHandler(funcStrName, funcName))

def registJobs(updater:Updater, jobs):
    for job in jobs:
        updater.job_queue.run_daily(job['name'],job['time'])

def registCallback(updater:Updater,CallbackFuncs):
    for func in CallbackFuncs:
        updater.dispatcher.add_handler(CallbackQueryHandler(func))

def updateDB(database,command):
    connDB = sqlite3.connect(database)
    ret =  connDB.cursor().execute(command).fetchall()
    connDB.commit()
    return ret

def getTodayBibleChapters(database):
    if config.todayCount == -1:
        config.todayCount = (date.today()-config.bibleStart).days + 1
    command = 'SELECT YEARS,BOOKS,CHAPTER_START,CHAPTER_END FROM SCRIPTS WHERE DAYS==%d'%config.todayCount
    
    return updateDB(database, command)[0]

from typing import Union, List
from telegram import InlineKeyboardButton

def build_menu(
    buttons: List[InlineKeyboardButton],
    n_cols: int,
    header_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]]=None,
    footer_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]]=None
) -> List[List[InlineKeyboardButton]]:
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons if isinstance(header_buttons, list) else [header_buttons])
    if footer_buttons:
        menu.append(footer_buttons if isinstance(footer_buttons, list) else [footer_buttons])
    return menu

def findFiles(filePrefix:str,notesDir = config.notesDir ):
    # if len(config.notesLst) == 0:
    config.notesLst = os.listdir(config.notesDir)
    sendLst = [os.path.join(config.notesDir,note) for note in config.notesLst if filePrefix == note[:6]]

    return sendLst




