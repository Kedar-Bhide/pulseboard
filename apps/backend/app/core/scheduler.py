from apscheduler.schedulers.background import BackgroundScheduler
from app.core.prompts import generate_and_log_question, send_missed_checkin_reminders, send_weekly_summaries
import logging

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(
        func=generate_and_log_question,
        trigger="cron",
        hour=9, minute=0  # runs daily at 9:00 AM UTC
    )
    scheduler.add_job(
        func=send_missed_checkin_reminders,
        trigger="cron",
        hour=17,  # 5pm UTC, change as needed
        minute=0
    )

    scheduler.add_job(
        func=send_weekly_summaries,
        trigger="cron",
        day_of_week="sun", hour=17, minute=0  # Sundays at 5PM UTC
    )

    from app.core.prompts import send_email_reminders

    scheduler.add_job(
        func=send_email_reminders,
        trigger="cron",
        hour=10, minute=0  # 10AM UTC
    )
    
    scheduler.start()
    logging.info("Scheduler started with daily question job.")