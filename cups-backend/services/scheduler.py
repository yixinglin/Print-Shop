from apscheduler.schedulers.background import BackgroundScheduler

from core.db import backup_database
from core.log import logger

scheduler = BackgroundScheduler()

@scheduler.scheduled_job('interval', hours=24)
def daily_job():
    # print("Daily job running...")
    logger.info("Daily job running...")
    backup_database()  # Call the backup_database function to backup the database
    # print("Daily job done.")
    logger.info("Daily job done.")
