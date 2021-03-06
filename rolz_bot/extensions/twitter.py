import random
import twitter
import twitter.error

from discord.ext import commands
from embeders.twitter import TwitterEmbeder
from rolz_bot.settings import (CONSUMER_KEY,
                               CONSUMER_SECRET,
                               ACCESS_TOKEN,
                               ACCESS_TOKEN_SECRET)


class Twitter(object):
    '''Posts random picture from a specified twitter bot.'''
    def __init__(self, bot):
        self.bot = bot

        self._twitter = twitter.Api(
         consumer_key=CONSUMER_KEY,
         consumer_secret=CONSUMER_SECRET,
         access_token_key=ACCESS_TOKEN,
         access_token_secret=ACCESS_TOKEN_SECRET
         )

        self._shitpost_id = 4462881555
        self._pesel_id = 730505014150582272
        self._hydra_id = 2434906866
        self._neko_id = 2837539873

        self.statuses = []

    async def _post_random_pic(self, type):
        '''The thing that does the business'''
        random_pic = random.choice(self.statuses)

        embed = TwitterEmbeder(random_pic.media[0].media_url_https, type)

        await self.bot.say(embed=embed)

    async def _get_twitter_status_list(self, twitter_id):
        try:
            self.statuses = self._twitter.GetUserTimeline(twitter_id,
                                                          count=200)
        except twitter.error.TwitterError:
            await self.bot.say("Twitter is too busy for shitposting, mate.")
            raise RuntimeError("Twitter doesn't respond properly.")

    @commands.command()
    async def hydra(self):
        """Takes a random picure from a cat bot."""
        await self._get_twitter_status_list(self._hydra_id)
        await self._post_random_pic("hydra")

    @commands.command()
    async def shitpost(self):
        '''Takes from ShitpostBot5000 pool.'''
        await self._get_twitter_status_list(self._shitpost_id)
        await self._post_random_pic("shitpost")

    @commands.command()
    async def pesel(self):
        '''Takes from Shiba Inu bot.'''
        await self._get_twitter_status_list(self._pesel_id)
        await self._post_random_pic("pesel")

    @commands.command()
    async def neko(self):
        '''Takes from a catgirl bot.'''
        await self._get_twitter_status_list(self._neko_id)
        await self._post_random_pic("neko")


def setup(bot):
    bot.add_cog(Twitter(bot))
