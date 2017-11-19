import discord
import rolz_bot.format_responses as format_responses
import json
import urllib.error

from urllib.parse import quote
from discord.ext import commands
from rolz_bot.roller import Roller


class Choose(Roller):    
    @commands.command(name='choose')
    async def choose(self, *variants : str):
        '''
        Picks between your variants.
        '''
        return_variants = ' '.join(variants)
        return_variants = return_variants.split(',')

        dice_query = '1d' + str(len(return_variants))

        right_choice = await self._roll_dice(dice_query)


        response_string = format_responses.choose_string.format(
                                    return_variants[right_choice['result']-1]
                                    )
        try:
            await self.bot.say(response_string)
        except discord.errors.HTTPException as error:
            response_string = format_responses.message_too_long_string


def setup(bot):
    bot.add_cog(Choose(bot))