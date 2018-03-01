import scrapy
import json


class EthJsonRpcClient(object):

    def __init__(self, url):
        self.url = url

    def eth_getBlockByNumber(self, block=0, tx_objects=True):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getblockbynumber
        """
        block = self.validate_block(block)
        return self._call('eth_getBlockByNumber', [block, tx_objects])

    def _call(self, method, params=None, _id=1):
        data = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params,
            'id': _id,
        }
        return scrapy.Request(self.url,
                              method='POST',
                              body=json.dumps(data),
                              headers={'Content-Type': 'application/json'})

    def validate_block(self, block):
        if isinstance(block, int):
            block = hex(block)
        return block
