import scrapy
import json
from ethereumScraper.utils import hex_to_dec
from ethereumScraper.eth_json_rpc_client import EthJsonRpcClient


class JsonRpcSpider(scrapy.Spider):
    name = "JsonRpcSpider"

    def _set_crawler(self, crawler):
        super(JsonRpcSpider, self)._set_crawler(crawler)
        jsonrpc_url = self.settings['ETH_JSON_RPC_URL']
        self.eth_client = EthJsonRpcClient(jsonrpc_url)

    def start_requests(self):
        for i in range(self.settings['START_BLOCK'], self.settings['END_BLOCK']):
            request = self.eth_client.eth_getBlockByNumber(i)
            request.callback = self.parse_block
            yield request

    def parse_block(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        result = jsonresponse['result']
        yield {
            'type': 'b',
            'block_number': hex_to_dec(result.get('number', None)),
            'block_hash': result.get('hash', None),
            'block_parentHash': result.get('parentHash', None),
            'block_nonce': result.get('nonce', None),
            'block_sha3Uncles': result.get('sha3Uncles', None),
            'block_logsBloom': result.get('logsBloom', None),
            'block_transactionsRoot': result.get('transactionsRoot', None),
            'block_stateRoot': result.get('stateRoot', None),
            'block_miner': result.get('miner', None),
            'block_difficulty': hex_to_dec(result.get('difficulty', None)),
            'block_totalDifficulty': hex_to_dec(result.get('totalDifficulty', None)),
            'block_size': hex_to_dec(result.get('size', None)),
            'block_extraData': result.get('extraData', None),
            'block_gasLimit': hex_to_dec(result.get('gasLimit', None)),
            'block_gasUsed': hex_to_dec(result.get('gasUsed', None)),
            'block_timestamp': result.get('timestamp', None),
        }

        transactions = result.get('transactions')
        for item in self.parse_transactions(transactions):
            yield item

    def parse_transactions(self, transactions):
        if transactions is not None:
            for transaction in transactions:
                yield {
                    'type': 't',
                    'tx_hash': transaction.get('hash', None),
                    'tx_nonce': hex_to_dec(transaction.get('nonce', None)),
                    'tx_blockHash': transaction.get('blockHash', None),
                    'tx_blockNumber': hex_to_dec(transaction.get('blockNumber', None)),
                    'tx_transactionIndex': hex_to_dec(transaction.get('transactionIndex', None)),
                    'tx_from': transaction.get('from', None),
                    'tx_to': transaction.get('to', None),
                    'tx_value': hex_to_dec(transaction.get('value', None)),
                    'tx_gas': hex_to_dec(transaction.get('gas', None)),
                    'tx_gasPrice': hex_to_dec(transaction.get('gasPrice', None)),
                    'tx_input': transaction.get('input', None),
                }