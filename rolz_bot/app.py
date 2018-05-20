from settings import (BOT_TOKEN, STARTUP)
from discord.ext import commands
from rolz_bot.format_responses import help_string

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command(name='halp')
async def halp():
    '''Slightly more detailed help.'''
    await bot.say(help_string)

if __name__ == "__main__":
    for extension in STARTUP:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    bot.run(BOT_TOKEN)
