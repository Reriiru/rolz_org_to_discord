import os

ENV = 'dev'

if ENV == 'dev':
    pass

if ENV == 'prod':
    CONSUMER_KEY = os.environ['CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

    BOT_TOKEN = os.environ['BOT_TOKEN']


MAX_STR_SIZE = 255
ROLZ_URL = "https://rolz.org/api/?"