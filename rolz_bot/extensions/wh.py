import rolz_bot.format_responses as format_responses

from discord.ext import commands
from rolz_bot.roller import Roller


class Wh(Roller):
    ROLL_QUERY = '1d100'

    def _get_response(self, result, stat):
        if result <= stat:
            return format_responses.wh_string_success
        else:
            return format_responses.wh_string_fail

    def _calculate_degree(self, result, type, stat):
        if type == 'old':
            return (abs((result - stat)) // 10)
        if type == 'new':
            return (abs((result - stat)) // 10) + 1

    async def _calculate_result(self, ctx, stat, type):
        roll_result = await self._roll_dice(self.ROLL_QUERY)
        response_string = self._get_response(int(roll_result['result']), stat)
        degree = self._calculate_degree(int(roll_result['result']), type, stat)
        response_string = response_string.format(
            ctx.message.author.display_name,
            roll_result['result'],
            degree
        )
        return response_string

    @commands.command(pass_context=True, name='wh')
    async def wh(self, ctx, stat: int):
        response_string = await self._calculate_result(ctx, stat, 'new')
        await self.bot.say(response_string)

    @commands.command(pass_context=True, name='wh_old')
    async def wh_old(self, ctx, stat: int):
        response_string = await self._calculate_result(ctx, stat, 'old')
        await self.bot.say(response_string)


def setup(bot):
    bot.add_cog(Wh(bot))
