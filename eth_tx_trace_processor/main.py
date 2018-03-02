import json

import requests

headers = {'Content-Type': 'application/json'}

data = {
            'jsonrpc': '2.0',
            'method':  'debug_traceTransaction',
            'params':  ['0x663254ac1888a6f04e3330c4c6b86127f618b486be6ce85cfda6f500fa1c2849', {}],
            'id':      1,
        }

response = requests.Session().post('https://mainnet.infura.io/eQq8vdX3vS511ulZw8fs',
                        headers = headers,
                        data=json.dumps(data))

print response.body_as_unicode()