import scrapy
import json

from ethscraper.mapper.block_mapper import EthBlockMapper
from ethscraper.eth.eth_json_rpc_client import EthJsonRpcClient
from ethscraper.mapper.erc20_transfer_mapper import EthErc20TransferMapper
from ethscraper.mapper.transaction_mapper import EthTransactionMapper
from ethscraper.mapper.transaction_receipt_mapper import EthTransactionReceiptMapper
from ethscraper.service.erc20_processor import EthErc20Processor
from ethscraper.utils import str2bool


class JsonRpcSpider(scrapy.Spider):
    name = "JsonRpcSpider"
    custom_settings = {
        'ITEM_PIPELINES': {
            'ethscraper.pipelines.EthereumScraperExportPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            'ethscraper.middlewares.EthereumScraperErrorHandlerMiddleware': 200
        },
        'SPIDER_MIDDLEWARES': {
            'ethscraper.middlewares.EthereumScraperErrorHandlerSpiderMiddleware': 100
        }
    }

    # Dependencies
    block_mapper = EthBlockMapper()
    transaction_mapper = EthTransactionMapper()
    transaction_receipt_mapper = EthTransactionReceiptMapper()
    erc20_transfer_mapper = EthErc20TransferMapper()
    erc20_processor = EthErc20Processor()
    eth_client = None

    # Flags
    export_transactions = True
    export_erc20_transfers = True

    def start_requests(self):
        json_rpc_url = self.settings['ETH_JSON_RPC_URL']
        self.eth_client = EthJsonRpcClient(json_rpc_url)

        self.export_transactions = str2bool(self.settings['EXPORT_TRANSACTIONS'])
        self.export_erc20_transfers = str2bool(self.settings['EXPORT_ERC20_TRANSFERS'])

        start_block = int(self.settings['START_BLOCK'])
        end_block = int(self.settings['END_BLOCK'])

        if start_block > end_block:
            self.logger.warning("START_BLOCK {} is greater than END_BLOCK {}").format(start_block, end_block)
            return

        for block_number in range(start_block, end_block + 1):
            request = self.eth_client.eth_getBlockByNumber(block_number)
            request.meta['block_number'] = block_number
            request.callback = self.parse_block
            yield request

    def parse_block(self, response):
        json_response = json.loads(response.text)
        result = json_response.get('result', None)
        if result is None:
            return
        block = self.block_mapper.json_dict_to_block(result)

        yield self.block_mapper.block_to_dict(block)

        if self.export_transactions or self.export_erc20_transfers:
            for tx in block.transactions:
                if self.export_transactions:
                    yield self.transaction_mapper.transaction_to_dict(tx)
                if self.export_erc20_transfers:
                    tx_receipt_request = self.eth_client.eth_getTransactionReceipt(tx.hash)
                    tx_receipt_request.meta['block_number'] = response.meta.get('block_number', None)
                    tx_receipt_request.meta['tx_hash'] = tx.hash
                    tx_receipt_request.callback = self.parse_transaction_receipt
                    yield tx_receipt_request

    def parse_transaction_receipt(self, response):
        json_response = json.loads(response.text)
        result = json_response.get('result', None)
        if result is None:
            return
        receipt = self.transaction_receipt_mapper.json_dict_to_transaction_receipt(result)

        erc20_transfers = self.erc20_processor.filter_transfers_from_receipt(receipt)

        for erc20_transfer in erc20_transfers:
            yield self.erc20_transfer_mapper.erc20_transfer_to_dict(erc20_transfer)
