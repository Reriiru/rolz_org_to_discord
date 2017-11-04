import commands
import twitter
import twitter.error
import random
import format_responses

from settings import MAX_STR_SIZE


class MessageHandler(object):
    def __init__(self, message, client, tmp=None):
        self.message = message
        self.client = client
        self.payload = None
        self.statuses = None

        self.tmp_message = None

        self._check_length()

        self.message.content = self._strip_special_chars()

        self._type = self._check_type()
        self._twitter = twitter.Api(
         consumer_key='yQaj8jUbjBAOlCjaMUfhX2A4n',
         consumer_secret='88uYcFAUlWYfepF7268w5aR9pRsuX9RAfQOHKCsEdUTX710Rce',
         access_token_key='489158548-3PM1kj018S5LkJUh9FKEvaCZrqmQI6g55ABJbI4C',
         access_token_secret='p3Sy6wJPTAG3ooNFPxBID3XCoHloSLxw7KGLS6itHd1oV'
         )
        self._shitpost_id = 4462881555
        self._pesel_id = 3254628247
        self._hydra_id = 2434906866

    def _check_length(self):
        if len(self.message.content) > MAX_STR_SIZE:
            raise ValueError("String is too big!")

    def _strip_special_chars(self):
        tmp_message_content = self.message.content.replace(" ", "%20")
        tmp_message_content = tmp_message_content.replace("+", "%2B")

        return tmp_message_content

    async def _post_random_pic(self, response_string):
        random_pic = random.choice(self.statuses)

        response_string = response_string.format(
                                random_pic.media[0].media_url_https
                                )

        await self.client.send_message(self.message.channel,
                                       response_string)

    async def _post_tmp(self):
        self.tmp_message = await self.client.send_message(
                                 self.message.channel,
                                 'Rolling the stones.'
                                 )

    def _check_type(self):
        tmp_type = self.message.content.split('!')[1]
        tmp_type = tmp_type.split('%20')[0]

        return tmp_type

    async def _get_twitter_status_list(self, twitter_id):
        try:
            self.statuses = self._twitter.GetUserTimeline(twitter_id,
                                                          count=200)
        except twitter.error.TwitterError:
            await self.client.send_message(
                                self.message.channel,
                                "Twitter is too busy for shitposting, mate."
                                )
            raise RuntimeError("Twitter doesn't respond properly.")


    async def _check_rolz_connection(self):
        if self.payload == 'Error! Rolz wont bloody respond!':
            await self.client.edit_message(self.tmp_message, self.payload)
            raise ValueError('Rolz is unavailable')

    async def _check_roll_validity(self):
        if not isinstance(self.payload['result'], int):
            response_string = format_responses.invalid_roll_string
            await self.client.edit_message(self.tmp_message, response_string)
            raise ValueError('Roll is invalid')

    async def _check_rolls_validity(self):
        for roll in self.payload:
            if not isinstance(roll['result'], int):
                response_string = format_responses.invalid_roll_string
                await self.client.edit_message(self.tmp_message,
                                               response_string)
                raise ValueError('Roll is invalid')

    async def _weird_characters_response(self):
        response_string = format_responses.weird_characters_string

        await self.client.edit_message(self.tmp_message, response_string)
        raise ValueError('Weird characters encountered.')

    async def fill_payload(self):
        if self._type == 'roll':
            await self._post_tmp()
            try:
                self.payload = await commands.proxy(
                                self.message.content.split('!')[1])
            except UnicodeEncodeError:
                await self._weird_characters_response()

            await self._check_rolz_connection()
            await self._check_roll_validity()

        elif self._type == 'repeat' or self._type == 'sum':
            await self._post_tmp()
            repeats = self.message.content.split('%20')[1]
            roll_string = ''

            for part in self.message.content.split('%20')[2:]:
                roll_string += part

            self.payload = []
            for index in range(int(repeats)):
                try:
                    roll_result = await commands.proxy(roll_string)
                    self.payload.append(roll_result)
                except UnicodeEncodeError:
                    await self._weird_characters_response()

            await self._check_rolz_connection()
            await self._check_rolls_validity()

        elif self._type == 'choose':
            await self._post_tmp()
            variants = self.message.content.split(',%20')
            variants[0] = variants[0].split('%20')[1]

            roll_string = '1d' + str(len(variants))

            roll_result = await commands.proxy(roll_string)

            self.payload = {
                'result': variants[roll_result['result']-1],
                'details': None
            }

            await self._check_rolz_connection()

    async def post_message(self):
        if self._type == 'roll':
            dice_amount = self.message.content[8]
            if dice_amount.isdigit() and int(dice_amount) == 1:
                pre_format_string = format_responses.roll_one_string
                response_string = pre_format_string.format(
                                        self.payload['result']
                                        )
            else:
                pre_format_string = format_responses.roll_many_string
                print(self.payload['result'])
                response_string = pre_format_string.format(
                                        self.payload['result'],
                                        self.payload['details']
                                        )

            await self.client.edit_message(self.tmp_message, response_string)

        elif self._type == 'repeat':
            response_string = '''
            Repeat rolls are now in.
            '''
            results = 'Results are: ** | '
            details = 'Here are some details: '
            for roll in self.payload:
                results += str(roll['result']) + ' | '
                details += ('Roll Number: ' + str(self.payload.index(roll)+1)
                            + roll['details'])
            results += '**'
            await self.client.edit_message(self.tmp_message, response_string)
            await self.client.send_message(self.message.channel, results)
            await self.client.send_message(self.message.channel, details)

        elif self._type == 'sum':
            response_string = '''
            Sum rolls are now in.
            '''
            summ = 'Sum result is: ```'
            details = 'Here are some details: '
            sum_number = 0

            for roll in self.payload:
                sum_number += roll['result']
                details += ('Roll Number: ' + str(self.payload.index(roll)+1)
                            + roll['details'])

            summ += str(sum_number) + '```'

            await self.client.edit_message(self.tmp_message, response_string)
            await self.client.send_message(self.message.channel, summ)
            await self.client.send_message(self.message.channel, details)

        elif self._type == 'choose':
            pre_format_string = format_responses.choose_string
            response_string = pre_format_string.format(self.payload['result'])
            await self.client.send_message(self.message.channel, 
                                           response_string)

        elif self._type == 'help':
            response_string = format_responses.help_string
            await self.client.send_message(self.message.channel, 
                                           response_string)

        elif self._type == 'vibe':
            response_string = format_responses.vibe_string
            await self.client.send_message(self.message.channel, 
                                           response_string)

        elif self._type == 'shitpost':
            response_string = format_responses.shitpost_string

            await self._get_twitter_status_list(self._shitpost_id)
            await self._post_random_pic(response_string)

        elif self._type == 'pesel':
            response_string = format_responses.pesel_string

            await self._get_twitter_status_list(self._pesel_id)
            await self._post_random_pic(response_string)

        elif self._type == 'hydra':
            response_string = format_responses.hydra_string

            await self._get_twitter_status_list(self._hydra_id)
            await self._post_random_pic(response_string)