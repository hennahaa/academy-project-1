from crontab import CronTab

cron = CronTab(user=True)
job = cron.new(command='python send_hours.py')

job.day.every(1)

cron.write()

print(job.is_valid())