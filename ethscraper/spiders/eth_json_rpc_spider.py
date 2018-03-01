import scrapy
import json

from ethscraper.mapper.block_mapper import EthBlockMapper
from ethscraper.eth_json_rpc_client import EthJsonRpcClient
from ethscraper.mapper.transaction_mapper import EthTransactionMapper


class JsonRpcSpider(scrapy.Spider):
    name = "JsonRpcSpider"
    block_mapper = EthBlockMapper()
    transaction_mapper = EthTransactionMapper()

    def _set_crawler(self, crawler):
        super(JsonRpcSpider, self)._set_crawler(crawler)
        json_rpc_url = self.settings['ETH_JSON_RPC_URL']
        self.eth_client = EthJsonRpcClient(json_rpc_url)

    def start_requests(self):
        start_block = int(self.settings['START_BLOCK'])
        end_block = int(self.settings['END_BLOCK'])

        if start_block >= end_block:
            self.logger.warning("START_BLOCK {} is less than or equal to END_BLOCK {}").format(start_block, end_block)
            return

        for block_number in range(start_block, end_block + 1):
            request = self.eth_client.eth_getBlockByNumber(block_number)
            yield request

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        result = json_response['result']
        block = self.block_mapper.json_dict_to_block(result)

        yield self.block_mapper.block_to_dict(block)

        for tx in block.transactions:
            yield self.transaction_mapper.transaction_to_dict(tx)

