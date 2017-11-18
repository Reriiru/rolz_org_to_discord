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

    response = urllib.request.urlopen(connection)
    payload = json.load(response)

    return payload
