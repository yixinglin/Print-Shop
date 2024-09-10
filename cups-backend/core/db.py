import os
import shutil
from datetime import datetime
from tortoise.contrib.fastapi import register_tortoise
from core.config import cups_client_config as config
from core.log import logger

db_config = config.sqlite

DB_ROOT = db_config.root  # root directory for database files
DB_NAME = db_config.db_name  # database filename
SQLITE_URL = f"sqlite://./{DB_ROOT}/{DB_NAME}"
MAX_BACKUPS = 45   # limit the number of backup files to keep
os.makedirs(DB_ROOT, exist_ok=True)
BACKUP_DIR = os.path.join(DB_ROOT, "backups")  # directory for backup files
os.makedirs(BACKUP_DIR, exist_ok=True)

def init_db_sqlite(app):
    """
    Initialize the database with sqlite
    :param app: FastAPI app instance
    :return:
    """
    register_tortoise(
        app,
        db_url=SQLITE_URL,
        modules={"models": ["models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )




def backup_database():
    # 确保备份目录存在
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    # 生成备份文件名
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"{DB_NAME}_{current_time}.db"
    backup_filepath = os.path.join(BACKUP_DIR, backup_filename)

    # 复制数据库文件进行备份
    DATABASE_PATH = os.path.join(DB_ROOT, DB_NAME)
    shutil.copy2(DATABASE_PATH, backup_filepath)
    logger.info(f"Backup created: {backup_filepath}")

    # 删除旧的备份文件，保留最多 MAX_BACKUPS 个
    backups = sorted(os.listdir(BACKUP_DIR))
    if len(backups) > MAX_BACKUPS:
        for old_backup in backups[:-MAX_BACKUPS]:
            old_backup_path = os.path.join(BACKUP_DIR, old_backup)
            os.remove(old_backup_path)
            logger.info(f"Deleted old backup: {old_backup_path}")

if __name__ == "__main__":
    backup_database()