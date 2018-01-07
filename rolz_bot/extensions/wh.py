import rolz_bot.format_responses as format_responses

from discord.ext import commands
from rolz_bot.roller import Roller


class Wh(Roller):
    ROLL_QUERY = '1d100'

    @commands.command(pass_context=True, name='wh')
    async def tarot(self, ctx, stat: int):
        roll_result = await self._roll_dice(self.ROLL_QUERY)
        if int(roll_result['result']) < stat:
            response_string = format_responses.wh_string_success
            degree = (abs((roll_result['result'] - stat)) // 10) + 1
            response_string = response_string.format(
                ctx.message.author.display_name,
                roll_result['result'],
                degree
            )
        else:
            response_string = format_responses.wh_string_fail
            degree = ((roll_result['result'] - stat) // 10) + 1
            response_string = response_string.format(
                ctx.message.author.display_name,
                roll_result['result'],
                degree
            )
        await self.bot.say(response_string)


def setup(bot):
    bot.add_cog(Wh(bot))
