import json
import redis
import pymongo
from pymongo.errors import ServerSelectionTimeoutError
from core.config import server_config as config
from core.log import server_logger as logger

redis_pool = None

DATETIME_PATTERN = '%Y-%m-%dT%H:%M:%SZ'

class RedisDataManager:
    def __init__(self, *args, **kwargs):
        self.redis_host = config.redis.host
        self.redis_port = config.redis.port
        # self.redis_client = settings.REDIS_USERNAME
        # self.redis_password = settings.REDIS_PASSWORD
        self.redis_db = config.redis.db
        self.encoding = 'utf-8'

        if not redis_pool:
            redis.ConnectionPool(max_connections=100)
        self.client = redis.Redis(host=self.redis_host,
                                  port=self.redis_port,
                                  db=self.redis_db,
                                  decode_responses=True,
                                  connection_pool=redis_pool, **kwargs)

    def get_keys_with_prefix(self, prefix):
        cursor = 0
        keys = []
        while True:
            # SCAN 命令通过 cursor 遍历所有 key，支持模式匹配
            cursor, new_keys = self.client.scan(cursor=cursor, match=f'{prefix}*')
            keys.extend(new_keys)
            if cursor == 0:
                break
        return keys

    def set(self, key: str, value: str, time_to_live_sec: int = None):
        self.client.set(key, value)
        if time_to_live_sec:
            self.client.expire(key, time_to_live_sec)

    def get(self, key: str) -> str:
        return self.client.get(key)

    def delete(self, key: str):
        self.client.delete(key)

    def set_json(self, key: str, value: dict, time_to_live_sec: int = None):
        self.client.set(key, json.dumps(value))
        if time_to_live_sec:
            self.client.expire(key, time_to_live_sec)

    def get_json(self, key: str) -> dict:
        data = self.client.get(key)
        if data:
            return json.loads(data)
        else:
            return None


class MongoDBDataManager:

    def __init__(self):
        self.db_host = config.mongodb.host
        self.db_port = config.mongodb.port
        self.db_client = None

    def connect(self):
        # Connect to MongoDB
        try:
            self.db_client = pymongo.MongoClient(self.db_host, self.db_port, serverSelectionTimeoutMS=10000)  # Connect
            names = self.db_client.list_database_names()
        except ServerSelectionTimeoutError as e:
            logger.error(f"Error connecting to MongoDB: {e}")
            raise RuntimeError("Error connecting to MongoDB")
        return self

    def get_client(self):
        return self.db_client

    def set_client(self, client):
        self.db_client = client
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        del self

    def close(self):
        if self.db_client:
            self.db_client.close()