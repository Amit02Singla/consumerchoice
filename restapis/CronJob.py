from crontab import CronTab
from datetime import datetime

def cronjob(time, cronTime):
    cron = CronTab(user=True)
    cron.remove_all()
    job = cron.new( command = 'python ApplicationController.py')
    dt = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    job.setall(datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute))
    if cronTime == 'weekly':
        job.every_weekly()
    if cronTime == 'hourly':
        job.hour.every(1)
    if cronTime == 'daily':
        job.every_daily()
    #job.hour.every('3')
    cron.write('output.tab')
    resp = "Scheduling Done"
    return resp

def cronjob1():
    cron = CronTab(user=True)
    cron.remove_all()
    job = cron.new( command = 'python ApplicationController.py')
    # dt = datetime.strptime(datetime.today(), '%Y-%m-%d %H:%M:%S')
    # job.setall(datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute))
    job.run()
    #job.hour.every('3')
    cron.write('output.tab')
    resp = "Scheduling Done"
    return resp

