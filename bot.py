# -*- coding: utf-8 -*-

import config
import telebot
import logging
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

standup_msg = 'В 16:00 стендап, просьба не расходиться.';
report_msg = 'Просьба всем отчитаться по сегодняшним трудозатратам.';
TEST_MSG = 'Привет, я служба SmartStandupBot. Это тест.'

standup_startdate = '2016-12-08 15:30:00'
report_startdate = '2016-12-08 17:50:00'
test_date = '2016-12-08 12:13:00'

class SmartStandupBot:
    def __init__(self):
        self.bot = telebot.TeleBot(config.token)
        logging.basicConfig(filename='main.log', format='%(asctime)s %(message)s', datefmt='%d.%m.%Y %I:%M:%S %p',
                            level=logging.INFO)
        self.scheduler = BlockingScheduler()

        @self.scheduler.scheduled_job('interval', id='my_job_id1', days=1, start_date=standup_startdate)
        def job_function():
            self.SendMessage(standup_msg)

        @self.scheduler.scheduled_job('interval', id='my_job_id2', days=1, start_date=report_startdate)
        def job_function():
            self.SendMessage(report_msg)

        #test
        # @self.scheduler.scheduled_job('interval', id='testjob', days=1, start_date=test_date)
        # def job_function():
        #     self.SendMessage(TEST_MSG)


    def SendMessage(self, msg):
        if self.todayIsWeekend():
            return
        self.bot.send_message(config.chatId, msg);
        logging.info('Message was sent: {}'.format(msg))

    def run(self):
        try:
            # self.SendMessage(TEST_MSG)
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass

    def stop(self):
        if self.scheduler.running:
            self.scheduler.shutdown()

    @staticmethod
    def todayIsWeekend():
        return datetime.today().weekday() in (5, 6)

