'''
Author: Jonah Liu
Date: 2022-01-25 18:30:21
LastEditTime: 2022-01-25 19:33:04
LastEditors: Jonah Liu
Description:  Functions for pyTelegrambot
'''
import sqlite3
from datetime import date,time
from telegram import Update
from telegram.ext import Updater, CommandHandler

def registCommands(updater:Updater,cmdDict:dict):
    for funcStrName,funcName in cmdDict.items():
        updater.dispatcher.add_handler(CommandHandler(funcStrName, funcName))

def registJobs(updater:Updater, jobs):
    for job in jobs:
        updater.job_queue.run_daily(job['name'],job['time'])

def updateDB(database,command):
    connDB = sqlite3.connect(database)
    ret =  connDB.cursor().execute(command).fetchall()
    return ret


def getTodayBibleChapters(bibleStart,database):
    today = (date.today()-bibleStart).days + 1
    command = 'SELECT YEARS,BOOKS,CHAPTER_START,CHAPTER_END FROM SCRIPTS WHERE DAYS==%d'%today
    
    return updateDB(database, command)
