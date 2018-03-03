import json

import requests
import sys

from ethscraper.mapper.trace.transaction_trace_mapper import EthTransactionTraceMapper

headers = {'Content-Type': 'application/json'}

data = {
    'jsonrpc': '2.0',
    'method': 'debug_traceTransaction',
    'params': ['0xfc753235989d274b7053dcfaec9383c24d10321649e2de0d60d8ace18b1abc98', {}],
    'id': 1,
}

response = requests.Session().post('http://127.0.0.1:8545/', headers=headers, data=json.dumps(data))
json_response = json.loads(response.text)

if 'error' in json_response:
    print 'Error: ' + json_response['error']
    sys.exit(1)

result = json_response.get('result', None)

if result is None:
    print 'result is empty in response'
    sys.exit(1)

trace_mapper = EthTransactionTraceMapper()
trace = trace_mapper.json_dict_to_transaction_trace(result)

print str(trace)