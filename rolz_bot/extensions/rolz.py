import discord
import rolz_bot.format_responses as format_responses
import json
import urllib.error

from urllib.parse import quote
from discord.ext import commands
from rolz_bot.roller import Roller


class Rolz(Roller):
    '''Frontend for the rolz proxy.'''    

    async def _roll(self, ctx, dice):
        dice_query = "".join(dice)
        dice_query = quote(dice_query, safe='')

        result = await self._roll_dice(dice_query)

        pre_format_string = format_responses.roll_string
        response_string = pre_format_string.format(
                            ctx.message.author.display_name,
                            result['result'],
                            result['details']
                            )

        try:
            await self.bot.say(response_string)
        except discord.errors.HTTPException:
            response_string = format_responses.message_too_long_string
            await self.bot.say(response_string)

    @commands.command(pass_context=True, name='roll')
    async def _roll(self, ctx, *dice : str):
        '''Gives you a roll, according to Rolz.org syntax'''
        await self._roll(ctx, dice)
   
    
    @commands.command(pass_context=True, name='r')
    async def _roll(self, ctx, *dice : str):
        '''Same as roll, but shorter'''
        await self._roll(ctx, dice)
    
    @commands.command(pass_context=True, name='repeat')
    async def repeat(self, ctx, repeats : int, *dice : str):
        '''Syntax is !repeat X `roll_query`, rolls multiple time.'''           
        full_result = []

        dice_query = "".join(dice)
        dice_query = quote(dice_query, safe='')

        for index in range(repeats):
            single_result = await self._roll_dice(dice_query)
            full_result.append(single_result)
        
        
        name_string = format_responses.repeat_string.format(
                                        ctx.message.author.display_name
                                        )

        result_string = format_responses.repeat_results_string
        details_string = format_responses.repeat_details_string

        for roll in full_result:
            result_string += str(roll['result']) + ' | '
            details_string += ('Roll Number: ' + ' `' +
                        str(full_result.index(roll)+1) + ' |' +
                        roll['details'] + '`')
        
        result_string += '**'

        try:
            await self.bot.say(name_string)
            await self.bot.say(result_string)
            await self.bot.say(details_string)
        except discord.errors.HTTPException as error:
            response_string = format_responses.message_too_long_string
            await self.bot.say(response_string)
        
    @commands.command(pass_context=True, name='sum')
    async def sum(self, ctx, repeats : int, *dice : str):
        '''
        Syntax is !sum X `roll_query`, rolls multiple time.
        Summs up the results.
        '''   
        full_result = []

        dice_query = "".join(dice)
        dice_query = quote(dice_query, safe='')

        for index in range(repeats):
            single_result = await self._roll_dice(dice_query)
            full_result.append(single_result)

        name_string = format_responses.sum_string.format(
                                        ctx.message.author.display_name
                                        )

        result_string = format_responses.sum_results_string
        details_string = format_responses.sum_details_string

        sum_result = 0

        for roll in full_result:
            sum_result += roll['result']
            details_string += ('Roll Number: ' + ' `' +
                        str(full_result.index(roll)+1) + ' |' +
                        roll['details'] + '`')
        
        result_string = result_string.format(str(sum_result))

        try:
            await self.bot.say(name_string)
            await self.bot.say(result_string)
            await self.bot.say(details_string)
        except discord.errors.HTTPException as error:
            response_string = format_responses.message_too_long_string
            await self.bot.say(response_string)


def setup(bot):
    bot.add_cog(Rolz(bot))