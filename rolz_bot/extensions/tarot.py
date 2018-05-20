import discord
import rolz_bot.format_responses as format_responses

from discord.ext import commands
from rolz_bot.embeders.tarot import TarotEmbeder, TarotShortEmbeder
from rolz_bot.database import db


class Tarot(object):
    def __init__(self, bot):
        self.collection = db.tarot
        self.bot = bot

    def _get_tarot_card(self):
        tarot = self.collection.aggregate(
            [{"$sample": {"size": 1}}]
        )
        tarot = list(tarot).pop()
        return tarot
    
    async def _post_tarot_card(self, embed, name, tarot):
        try:
            await self.bot.say(embed=embed)
        except discord.errors.HTTPException as e:
            response_string = format_responses.message_too_long_string
            await self.bot.say(response_string)

    @commands.command(pass_context=True, name='tarot')
    async def tarot(self, ctx):
        '''Posts a randomized tarot card.'''

        tarot = self._get_tarot_card()
        name = ctx.message.author.display_name
        embed = TarotEmbeder(tarot, name)

        await self._post_tarot_card(embed, name, tarot)

    @commands.command(pass_context=True, name='tarot_short')
    async def tarot_short(self, ctx):
        '''Posts a shortened format tarot.'''

        tarot = self._get_tarot_card()
        name = ctx.message.author.display_name
        embed = TarotShortEmbeder(tarot, name)

        await self._post_tarot_card(embed, name, tarot)


def setup(bot):
    bot.add_cog(Tarot(bot))
