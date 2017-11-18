import discord
import rolz_bot.format_responses as format_responses
import json
import urllib.error

from discord.ext import commands
from rolz_bot.roller import Roller

class Nwod(Roller):
    async def _exploded(self, number, result):
        final_result = {'result': 0, 'details': ''}
        while True:
            actuall_results = result['details'].split(u"\u2192")[0]
            exploded_dice = 0
            print("Result!", result)
            actuall_results = actuall_results.replace(actuall_results[:4], '')
            print("Result!", actuall_results)
            for s in actuall_results.split(', '):
                print(s)
                if int(s) >= number:
                    exploded_dice += 1
            
            if exploded_dice == 0:
                break

            dice_query = str(exploded_dice) + 'd10e8'

            print(dice_query)
            result = await self._roll_dice(dice_query)
            
            final_result['result'] += result['result']
            final_result['details'] += ' ' + result['details']
        
        return final_result

    async def _nwod(self, ctx, dice):
        dice_query = "".join(dice)

        if dice_query.find('r') != -1:
            dice_query = dice_query.replace('r', '')
            roll_query = dice_query.split('e')[0] + 'd10e8'
            result = await self._roll_dice(roll_query)
            failed_query = int(roll_query.split('d')[0]) - int(result['result'])
            failed_query = str(failed_query) + 'd10e8'
            print("Failde query", failed_query)
            failed_result = await self._roll_dice(failed_query)

            if dice_query.find('e') != -1:
                exploded = await self._exploded(
                                       int(dice_query[dice_query.find('e')+1]),
                                       result)
            else:
                exploded = await self._exploded(10, result)

            result['result'] += failed_result['result'] + exploded['result']
            
            result['details'] += (' ' + failed_result['details'] + 
                                        exploded['details'])

        else:
            roll_query = dice_query.split('e')[0] + 'd10e8'
            result = await self._roll_dice(roll_query)

            if dice_query.find('e') != -1:
                exploded = await self._exploded(
                                       int(dice_query[dice_query.find('e')+1]),
                                       result)
            else:
                print("got to exploded")
                exploded = await self._exploded(10, result)
            print(result)
            result['result'] += exploded['result']
            print(result)
            result['details'] += ' ' + exploded['details']
        

        response_string = format_responses.nwod_response
        response_string = response_string.format(
                                ctx.message.author.display_name,
                                                result['result'],
                                                result['details']
                                                )
        print(response_string)
        
        try:
            await self.bot.say(response_string)
        except discord.errors.HTTPException:
            response_string = format_responses.message_too_long_string
            await self.bot.say(response_string)

    @commands.command(pass_context=True, name='n')
    async def n(self, ctx, *dice : str):
        await self._nwod(ctx, dice)
    
    @commands.command(pass_context=True, name='nwod')
    async def nwod(self, ctx, *dice : str):
        await self._nwod(ctx, dice)
    


def setup(bot):
    bot.add_cog(Nwod(bot))