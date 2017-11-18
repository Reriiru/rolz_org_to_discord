import discord
import rolz_bot.format_responses as format_responses
import cerberus
import json
import urllib.error

from urllib.parse import quote
from discord.ext import commands
from rolz_bot.proxy import proxy


class Rolz(object):
    '''Frontend for the rolz proxy.'''
    def __init__(self, bot):
        self.bot = bot
        self.result_validation_schema = {
            'result': {
                'type': 'number'
            }
        }

        self.result_validator = cerberus.Validator(
                                        self.result_validation_schema,
                                        allow_unknown=True
                                        )
      
    async def _unserializable_data_response(self):
        response_string = format_responses.invalid_roll_string
        await self.bot.say(response_string)
        raise json.decoder.JSONDecodeError('Rolz returned empty JSON')
    
    async def _rolz_connection_error(self):
        response_string = format_responses.response_error_string
        await self.bot.say(response_string)
        raise urllib.error.HTTPError('Rolz is unavailable')
    
    async def _weird_characters_response(self):
        response_string = format_responses.weird_characters_string

        await self.bot.say(response_string)
        raise UnicodeEncodeError('Cyrillic characters occured.')
    
    async def _validation_fail(self):
        response_string = format_responses.invalid_roll_string
        await self.bot.say(response_string)
        raise ValueError('Result have not passed validation.')
    
    async def _roll_dice(self, dice_query):
        try:
            result = await proxy(dice_query)
        except UnicodeEncodeError:
            await self._weird_characters_response()
        except json.decoder.JSONDecodeError:
            await self._unserializable_data_response()
        except urllib.error.HTTPError:
            await self._rolz_connection_error()
        
        if self.result_validator.validate(result) is False:
            await self._validation_fail()
        
        return result

    @commands.command(pass_context=True, name='roll')
    async def roll(self, ctx, *dice : str):
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
        
    @commands.command(pass_context=True, name='repeat')
    async def repeat(self, ctx, repeats : int, *dice : str):           
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
    
    @commands.command(name='choose')
    async def choose(self, *variants : str):
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
    bot.add_cog(Rolz(bot))