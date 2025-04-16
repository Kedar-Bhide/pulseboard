from apscheduler.schedulers.background import BackgroundScheduler
from app.core.prompts import generate_and_log_question  # you’ll build this next
import logging

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(
        func=generate_and_log_question,
        trigger="cron",
        hour=9, minute=0  # ⏰ runs daily at 9:00 AM UTC
    )
    scheduler.start()
    logging.info("Scheduler started with daily question job.")