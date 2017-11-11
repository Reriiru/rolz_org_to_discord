import discord
import handler

from settings import (BOT_TOKEN)


client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith('!'):
        try:
            message_handler = handler.MessageHandler(message, client)
        except ValueError:
            raise ValueError('Could not initialise the Handler')

        await message_handler.fill_payload()
        await message_handler.post_message()


client.run(BOT_TOKEN)
