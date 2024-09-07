from core.config import load_server_config

conf = load_server_config("conf/server.yml")
print(conf)
print(conf.redis)
print(conf.logging.level)