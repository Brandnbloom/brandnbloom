from apscheduler.schedulers.background import BackgroundScheduler

def start_scheduler(job_func, minutes: int = 60):
    sched = BackgroundScheduler()
    sched.add_job(job_func, 'interval', minutes=minutes, id='weekly_report_job', replace_existing=True)
    sched.start()
    return sched
