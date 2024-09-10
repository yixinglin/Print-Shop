import os
from dataclasses import dataclass, field

import yaml


@dataclass
class History:
    path: str

@dataclass
class SQLite:
    root: str
    db_name: str

@dataclass
class Logging:
    path: str


@dataclass
class Config:
    debug: bool
    env: str
    version: str
    summary: str
    email: str
    author: str
    url: str
    history: History
    sqlite: SQLite
    logging: Logging

def load_cups_client_config(path):
    print(f"Loading configuration from {path}...")
    with open(path, 'r', encoding='utf-8') as f:
        conf = yaml.safe_load(f)
    c = Config(
        debug=conf['debug'],
        env=conf['env'],
        version=conf['version'],
        summary=conf['summary'],
        email=conf['email'],
        author=conf['author'],
        url=conf['url'],
        history=History(**conf['history']),
        sqlite=SQLite(**conf['sqlite']),
        logging=Logging(**conf['logging'])
        )
    print("Configuration loaded successfully.")
    print(c)
    log_ = c.logging
    os.makedirs(log_.path, exist_ok=True)
    hist_ = c.history
    os.makedirs(hist_.path, exist_ok=True)
    sqlite_ = c.sqlite
    os.makedirs(sqlite_.root, exist_ok=True)
    return c


from dotenv import load_dotenv
# 读取环境变量
load_dotenv()
cups_conf_file_path = os.getenv('CUPS_CONFIG_FILE')

cups_client_config = load_cups_client_config(cups_conf_file_path)

