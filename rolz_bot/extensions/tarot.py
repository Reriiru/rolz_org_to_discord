import discord
import rolz_bot.format_responses as format_responses
import rolz_bot.settings

from discord.ext import commands
from rolz_bot.roller import Roller
from imgurpython import ImgurClient


class Tarot(Roller):
    def __init__(self, bot):
        super().__init__(bot)
        self.imgur_client = ImgurClient(rolz_bot.settings.IMGUR_CLIENT,
                                        rolz_bot.settings.IMGUR_SECRET)
        self.tarot_album = self.imgur_client.get_album_images('5TzBe')

    @commands.command(pass_context=True, name='tarot')
    async def tarot(self, ctx):
        '''Posts a randomized tarot card.'''
        dice_query = '1d156'
        number = await self._roll_dice(dice_query)
        number = number['result']

        response_string = format_responses.tarot_string
        response_string = response_string.format(
                                    ctx.message.author.display_name,
                                    self.tarot_album[number-1].link)

        try:
            await self.bot.say(response_string)
        except discord.errors.HTTPException:
            response_string = format_responses.message_too_long_string
            await self.bot.say(response_string)


def setup(bot):
    bot.add_cog(Tarot(bot))
