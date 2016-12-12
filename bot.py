# -*- coding: utf-8 -*-

import config
import telebot
import logging
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

standup_msg = 'В 16:00 стендап, просьба не расходиться.';
report_msg = 'Просьба всем отчитаться по сегодняшним трудозатратам.';

standup_startdate = '2016-12-08 15:30:00'
report_startdate = '2016-12-08 17:50:00'

# standup_startdate_test = '2016-12-08 15:30:00'
# report_startdate_test = '2016-12-08 17:50:00'

bot = telebot.TeleBot(config.token)
logging.basicConfig(filename='main.log', format='%(asctime)s %(message)s', datefmt='%d.%m.%Y %I:%M:%S %p', level=logging.INFO)

def todayIsWeekend():
    return datetime.today().weekday() in (5, 6)

def SendMessage(msg):
    if todayIsWeekend():
        return
    bot.send_message(config.chatId, msg);
    logging.info('Message was sent: {}'.format(msg))

scheduler = BlockingScheduler()

@scheduler.scheduled_job('interval', id='my_job_id1', days=1, start_date=standup_startdate)
def job_function():
    SendMessage(standup_msg)

@scheduler.scheduled_job('interval', id='my_job_id2', days=1, start_date=report_startdate)
def job_function():
    SendMessage(report_msg)


# test
# @scheduler.scheduled_job('interval', id='my_job_id1', seconds=5, start_date=standup_startdate_test)
# def job_function():
#     SendMessage(standup_msg)
#
# @scheduler.scheduled_job('interval', id='my_job_id2', seconds=5, start_date=report_startdate_test)
# def job_function():
#     SendMessage(report_msg)

if __name__ == '__main__':
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass