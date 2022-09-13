from crontab import CronTab

cron = CronTab(user=True)
job = cron.new(command='/home/pydev/workflow/dt_web_scraping/prod/dislicores/web_scraping_dislicores_v2.py')
job.minute.every(1)

cron.write()