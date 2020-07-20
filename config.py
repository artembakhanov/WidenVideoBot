import os

TEMP = os.getenv('temp')
TOKEN = os.getenv('token')
REDIS = {
    "host": os.getenv('redis_host'),
    "port": os.getenv('redis_port'),
}

TIMOUT = 15
