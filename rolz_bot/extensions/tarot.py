import discord
import rolz_bot.format_responses as format_responses

from discord.ext import commands
from rolz_bot.embeders.tarot import TarotEmbeder
from rolz_bot.database import db


class Tarot(object):
    def __init__(self, bot):
        self.collection = db.tarot
        self.bot = bot

    @commands.command(pass_context=True, name='tarot')
    async def tarot(self, ctx):
        '''Posts a randomized tarot card.'''

        tarot = self.collection.aggregate(
            [{"$sample": {"size": 1}}]
        )
        tarot = list(tarot).pop()
        name = ctx.message.author.display_name
        embed = TarotEmbeder(tarot, name)
        try:
            await self.bot.say(embed=embed)
        except discord.errors.HTTPException as e:
            response_string = format_responses.message_too_long_string
            await self.bot.say(response_string)


def setup(bot):
    bot.add_cog(Tarot(bot))
