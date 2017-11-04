import urllib.request
import urllib.error
import json

from settings import ROLZ_URL


async def proxy(content):
    connection = urllib.request.Request(ROLZ_URL + content + '.json',
                                        headers={
                                            'User-Agent': 'Discord roller bot.'
                                        }                                
                                        )

    try:
        response = urllib.request.urlopen(connection)
    except urllib.error.HTTPError as error:
        return 'Error! Rolz wont bloody respond!'

    payload = json.load(response)
    return payload
