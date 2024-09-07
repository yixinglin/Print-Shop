import os
from dataclasses import dataclass, field
from typing import Optional
import yaml

# ========= Server Config =========
@dataclass
class History:
    path: str

@dataclass
class Logging:
    level: str
    format: str
    datefmt: str
    path: str
    max_size: int
    backup_count: int

@dataclass
class Redis:
    host: str
    port: int
    db: int
    password: Optional[str] = None

@dataclass
class MongoDB:
    host: str
    port: int
    db: str
    username: Optional[str] = None
    password: Optional[str] = None

@dataclass
class SQLite:
    file: str


@dataclass
class ServerConfig:
    debug: bool
    env: str
    project_name: str
    version: str
    summary: str
    email: str
    author: str
    url: str
    history: History
    logging: Logging
    redis: Redis
    mongodb: MongoDB
    sqlite: SQLite


def load_server_config(path: str) -> ServerConfig:
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    conf = ServerConfig(
        debug=config['debug'],
        env=config['env'],
        project_name=config['project_name'],
        version=config['version'],
        summary=config['summary'],
        email=config['email'],
        author=config['author'],
        url=config['url'],
        history=History(**config['history']),
        logging=Logging(**config['logging']),
        redis=Redis(**config['redis']),
        mongodb=MongoDB(**config['mongodb']),
        sqlite=SQLite(**config['sqlite'])
    )
    log_ = conf.logging
    os.makedirs(os.path.dirname(log_.path), exist_ok=True)
    hist_ = conf.history
    os.makedirs(hist_.path, exist_ok=True)
    sqlite_ = conf.sqlite
    os.makedirs(os.path.dirname(sqlite_.file), exist_ok=True)
    return conf


# ============================== Client Config =========

@dataclass
class Server:
    host: str
    port: int
    username: str
    password: str

@dataclass
class Jobs:
    path: str
    interval: int

@dataclass
class ClientConfig:
    debug: bool
    env: str
    server: Server
    logging: Logging
    jobs: Jobs


def load_client_config(path: str) -> ClientConfig:
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    conf = ClientConfig(
        debug=config['debug'],
        env=config['env'],
        server=Server(**config['server']),
        logging=Logging(**config['logging']),
        jobs=Jobs(**config['jobs'])
    )

    log_ = conf.logging
    os.makedirs(os.path.dirname(log_.path), exist_ok=True)
    jobs_ = conf.jobs
    os.makedirs(jobs_.path, exist_ok=True)

    return conf



server_config = load_server_config('conf/server.yml')
client_config = load_client_config('conf/client.yml')
