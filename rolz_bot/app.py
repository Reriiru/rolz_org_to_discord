import rolz_bot.format_responses as format_responses
from settings import (BOT_TOKEN, STARTUP)
from discord.ext import commands


bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(name='halp')
async def repeat():
    await bot.say(format_responses.help_string)

if __name__ == "__main__":
    for extension in STARTUP:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    
    bot.run(BOT_TOKEN)


