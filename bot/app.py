import discord
import commands

from settings import (TOKEN, MAX_STR_SIZE)


client = discord.Client()



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if len(message.content) > MAX_STR_SIZE:
        raise ValueError("String is too big!")

    if message.content.startswith('!'):
        tmp = await client.send_message(message.channel, 'Rolling the stones.')

        message.content = message.content.replace(" ", "%20")
        message.content = message.content.replace("+", "%2B")

        payload = await commands.proxy(message.content.split('!')[1])

        if payload == 'Error! Rolz wont bloody respond!':
            await client.edit_message(tmp, payload)
            return "Going the next step"

        if not isinstance(payload['result'], int):
            response_string = '''
            Please, use valid rolz codes.
            You can find info on roll formats here:
            https://rolz.org/wiki/page?w=help&n=BasicCodes
            '''
            await client.edit_message(tmp, response_string)
            return "Going the next step"

        response_string = '''
        Roll result: {},
        Roll details: {}
        '''.format(payload['result'], payload['details'])

        await client.edit_message(tmp, response_string)

client.run(TOKEN)
