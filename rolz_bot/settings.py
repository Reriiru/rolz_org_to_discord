import os

ENV = 'prod'

if ENV == 'dev':
    pass
if ENV == 'prod':
    CONSUMER_KEY = os.environ['CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

    IMGUR_CLIENT = os.environ['IMGUR_CLIENT']
    IMGUR_SECRET = os.environ['IMGUR_SECRET']
    BOT_TOKEN = os.environ['BOT_TOKEN']
    MONGO_STRING = os.environ['MONGO_STRING']


STARTUP = ['extensions.rolz', 'extensions.twitter', 'extensions.choose',
           'extensions.nwod', 'extensions.tarot', 'extensions.value']
MAX_STR_SIZE = 255
ROLZ_URL = "https://rolz.org/api/?"
