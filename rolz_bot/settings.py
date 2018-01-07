import codecs
import ast

ENV = 'prod'


def parse_option(value, type):
    parsers = {
        bool: lambda x: bool(ast.literal_eval(x))
    }
    parser = parsers.get(type, type)
    return parser(value)


def get_secret(name, *args, **kwargs):
    try:
        with codecs.open('/run/secrets/{}'.format(name), encoding='utf-8') \
                                                                as stream:
            value = stream.read()
            return parse_option(value.strip(), kwargs.get('type', str))
    except IOError:
        if args:
            return args[0]
        raise RuntimeError(u"Not found {} in Docker secrets".format(name))


if ENV == 'dev':
    pass
if ENV == 'prod':
    CONSUMER_KEY = get_secret('twitter_consumer_key')
    CONSUMER_SECRET = get_secret('twitter_consumer_secret')
    ACCESS_TOKEN = get_secret('twitter_access_token')
    ACCESS_TOKEN_SECRET = get_secret('twitter_access_token_secret')

    IMGUR_CLIENT = get_secret('imgur_client')
    IMGUR_SECRET = get_secret('imgur_secret')
    BOT_TOKEN = get_secret('discord_bot_token')
    MONGO_STRING = 'mongodb://mongo:27017/bot-data'


STARTUP = ['extensions.rolz', 'extensions.twitter', 'extensions.choose',
           'extensions.nwod', 'extensions.tarot', 'extensions.value',
           'extensions.wh']
MAX_STR_SIZE = 255
ROLZ_URL = "https://rolz.org/api/?"
