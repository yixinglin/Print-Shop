import os

from tortoise.contrib.fastapi import register_tortoise

DB_ROOT = "database"
SQLITE_URL = f"sqlite://./{DB_ROOT}/cups.db"
os.makedirs(DB_ROOT, exist_ok=True)

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
