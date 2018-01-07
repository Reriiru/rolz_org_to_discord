import rolz_bot.format_responses as format_responses
import cerberus
import pymongo.errors

from discord.ext import commands
from rolz_bot.roller import Roller
from rolz_bot.database import db


class Value(Roller):
    def __init__(self, bot):
        super().__init__(bot)
        self.values = db.values

        value_schema = {
            'user': {
                'type': 'string',
                'maxlength': 50,
                'minlength': 5,
                'required': True,
            },
            'name': {
                'type': 'string',
                'maxlength': 100,
                'required': True,
            },
            'value': {
                'type': 'string',
                'minlength': 2,
                'maxlength': 1000,
                'required': True,
            }
        }

        self.value_validator = cerberus.Validator(value_schema)

    async def _macro_value_add(self, ctx, name, query):
        '''Creates a new value. Syntax: !value add "NAME" "COMMAND"'''
        to_add = {
            'user': ctx.message.author.name,
            'name': name,
            'value': query
        }

        if self.value_validator.validate(to_add) is False:
            response_string = format_responses.invalid_value_string
            await self.bot.say(response_string)
            raise ValueError("Value is too big")

        unique_check = self.values.find_one({'user': ctx.message.author.name,
                                             'name': name})

        if unique_check is None:
            try:
                self.values.insert_one(to_add)
            except pymongo.errors.PyMongoError as e:
                response_string = format_responses.invalid_value_string
                await self.bot.say(response_string)
                raise pymongo.errors.PyMongoError

            response_string = format_responses.value_added_string
            response_string = response_string.format(name,
                                                     ctx.message.author.name)
            await self.bot.say(response_string)
        else:
            try:
                self.values.update_one(
                    {
                        'user': ctx.message.author.name,
                        'name': name
                    },
                    {
                        "$set": to_add
                    }
                )
            except pymongo.errors.PyMongoError as e:
                response_string = format_responses.invalid_value_string
                await self.bot.say(response_string)
                raise pymongo.errors.PyMongoError

            response_string = format_responses.value_update_string
            response_string = response_string.format(name,
                                                     ctx.message.author.name)
            await self.bot.say(response_string)

    async def _macro_value_show(self, ctx, name):
        '''Shows a value specified by name. Syntax: !value show "NAME"'''
        search_query = {
            'user': ctx.message.author.name,
            'name': name
        }

        try:
            value = self.values.find_one(search_query)
        except pymongo.errors.PyMongoError as e:
            response_string = format_responses.value_search_error_string
            await self.bot.say(response_string)
            raise pymongo.errors.PyMongoError

        if value is None:
            response_string = format_responses.value_nothing_found_string
            await self.bot.say(response_string)

        else:
            response_string = format_responses.value_search_string
            response_string = response_string.format(name,
                                                     ctx.message.author.name)
            await self.bot.say(response_string)
            await self.bot.say(value['value'])

    async def _macro_value_list(self, ctx):
        '''Shows a list of values that user defined.'''
        search_query = {
            'user': ctx.message.author.name
        }

        try:
            value_list = self.values.find(search_query)
        except pymongo.errors.PyMongoError as e:
            response_string = format_responses.value_search_error_string
            await self.bot.say(response_string)
            raise pymongo.errors.PyMongoError

        values_string = ''

        for value in value_list:
            values_string += '`' + value['name'] + '`' + "\n"

        if values_string == '':
            response_string = format_responses.value_list_empty_string
            response_string = response_string.format(ctx.message.author.name)
            await self.bot.say(response_string)
        else:
            response_string = format_responses.value_list_string
            response_string = response_string.format(ctx.message.author.name,
                                                     values_string)
            await self.bot.say(response_string)

    async def _macro_value_delete(self, ctx, name):
        '''Deletes a value specified by its name. Syntax: !value delete "NAME"'''
        search_query = {
            'user': ctx.message.author.name,
            'name': name
        }

        try:
            value = self.values.find_one(search_query)
        except pymongo.errors.PyMongoError as e:
            response_string = format_responses.value_delete_fail_string
            await self.bot.say(response_string)
            raise pymongo.errors.PyMongoError

        if value is None:
            response_string = format_responses.value_delete_none_string
            await self.bot.say(response_string)
        else:
            self.values.delete_one(value)
            response_string = format_responses.value_delete_string
            response_string = response_string.format(name,
                                                     ctx.message.author.name)
            await self.bot.say(response_string)

    @commands.command(pass_context=True, name='value')
    async def macro(self, ctx, *args: str):
        '''Stores a specified value, user unique.'''
        if args[0] == 'add':
            await self._macro_value_add(ctx, args[1], args[2])
        elif args[0] == 'show':
            await self._macro_value_show(ctx, args[1])
        elif args[0] == 'list':
            await self._macro_value_list(ctx)
        elif args[0] == 'delete':
            await self._macro_value_delete(ctx, args[1])


def setup(bot):
    bot.add_cog(Value(bot))
