# -*- coding: utf-8 -*-

import config
import telebot

from apscheduler.schedulers.blocking import BlockingScheduler

standup_msg = 'В 16:00 стендап, просьба не расходиться.';
report_msg = 'Просьба всем отчитаться по сегодняшним трудозатратам.';

standup_startdate = '2016-12-09 15:30:00'
report_startdate = '2016-12-09 17:50:00'

bot = telebot.TeleBot(config.token)

def SendMessage(msg):
    bot.send_message(config.chatId, msg);


scheduler = BlockingScheduler()

@scheduler.scheduled_job('interval', id='my_job_id1', day=1, start_date=standup_startdate)
def job_function():
    SendMessage(standup_msg)

@scheduler.scheduled_job('interval', id='my_job_id2', day=1, start_date=report_startdate)
def job_function():
    SendMessage(report_msg)

if __name__ == '__main__':
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass