import commands

from settings import MAX_STR_SIZE


class MessageHandler(object):
    def __init__(self, message, client, tmp):
        self.message = message
        self.client = client
        self.payload = None
        self.tmp_message = tmp

        self._check_length()

        self.message.content = self._strip_special_chars()

        self._type = self._check_type()

    def _check_length(self):
        if len(self.message.content) > MAX_STR_SIZE:
            raise ValueError("String is too big!")

    def _strip_special_chars(self):
        tmp_message_content = self.message.content.replace(" ", "%20")
        tmp_message_content = tmp_message_content.replace("+", "%2B")

        return tmp_message_content

    def _check_type(self):
        tmp_type = self.message.content.split('!')[1]
        tmp_type = tmp_type.split('%20')[0]

        return tmp_type

    async def _check_rolz_connection(self):
        if self.payload == 'Error! Rolz wont bloody respond!':
            await self.client.edit_message(self.tmp_message, self.payload)
            raise ValueError('Rolz is unavailable')

    async def _check_roll_validity(self):
        print(self.payload)
        if not isinstance(self.payload['result'], int):
            response_string = '''
            Please, use valid rolz codes.
            You can find info on roll formats here:
            https://rolz.org/wiki/page?w=help&n=BasicCodes
            '''
            await self.client.edit_message(self.tmp_message, response_string)
            raise ValueError('Roll is invalid')

    async def _check_rolls_validity(self):
        for roll in self.payload:
            if not isinstance(roll['result'], int):
                response_string = '''
                Please, use valid rolz codes.
                You can find info on roll formats here:
                https://rolz.org/wiki/page?w=help&n=BasicCodes
                '''
                await self.client.edit_message(self.tmp_message,
                                               response_string)
                raise ValueError('Roll is invalid')

    async def _weird_characters_response(self):
        response_string = '''
        Enough with the weird characters, you ponce!
        '''

        await self.client.edit_message(self.tmp_message, response_string)
        raise ValueError('Weird characters encountered.')

    async def fill_payload(self):
        if self._type == 'roll':
            try:
                self.payload = await commands.proxy(
                                self.message.content.split('!')[1])
            except UnicodeEncodeError:
                await self._weird_characters_response()

            await self._check_rolz_connection()
            await self._check_roll_validity()

        elif self._type == 'repeat' or self._type == 'sum':
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
            response_string = '''
            Roll Result: {}
            Roll Details: {}
            '''.format(self.payload['result'], self.payload['details'])

            await self.client.edit_message(self.tmp_message, response_string)

        elif self._type == 'repeat':
            response_string = '''
            Repeat rolls are now in.
            '''
            results = 'Results are: | '
            details = 'Here are some details: '
            for roll in self.payload:
                results += str(roll['result']) + ' | '
                details += ('Roll Number: ' + str(self.payload.index(roll)+1)
                            + roll['details'])

            await self.client.edit_message(self.tmp_message, response_string)
            await self.client.send_message(self.message.channel, results)
            await self.client.send_message(self.message.channel, details)

        elif self._type == 'sum':
            response_string = '''
            Sum rolls are now in.
            '''
            summ = 'Sum result is: '
            details = 'Here are some details: '
            sum_number = 0

            for roll in self.payload:
                sum_number += roll['result']
                details += ('Roll Number: ' + str(self.payload.index(roll)+1)
                            + roll['details'])

            summ += str(sum_number)

            await self.client.edit_message(self.tmp_message, response_string)
            await self.client.send_message(self.message.channel, summ)
            await self.client.send_message(self.message.channel, details)

        elif self._type == 'choose':
            response_string = '''
            I choose {}!
            '''.format(self.payload['result'])

            await self.client.edit_message(self.tmp_message, response_string)

        elif self._type == 'help':
            response_string = '''
            This bot proxies your rolls to rolz.org.
            Syntax info can be found here:
            https://rolz.org/wiki/page?w=help&n=BasicCodes
            To roll you use !roll. Example:
            !roll 6d6
            It can use multiple rolls with !sum and !repeat. Example:
            !sum 5 1d6
            !repeat 5 1d6
            It can also use choose. Example:
            !choose Love, Marry, Kill
            '''

            await self.client.edit_message(self.tmp_message, response_string)

        elif self._type == 'vibe':
            response_string = '''
            Vibe away, boyos!
            https://www.youtube.com/watch?v=QXuIwJfwVf8
            '''

            await self.client.edit_message(self.tmp_message, response_string)
