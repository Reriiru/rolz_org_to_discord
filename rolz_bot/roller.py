import cerberus
import rolz_bot.format_responses as format_responses
import json

import urllib.request
import urllib.error

from rolz_bot.proxy import proxy


class Roller(object):
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

    async def _roll_dice_raw(self, dice):
        revised_dice = []
        for entry in dice:
            if entry.find('#') != -1:
                break
            else:
                revised_dice.append(entry)

        dice_query = "".join(revised_dice)
        return await self._roll_dice(dice_query)

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
