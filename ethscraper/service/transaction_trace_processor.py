from ethscraper.domain.erc20_transfer import EthErc20Transfer
from ethscraper.domain.transaction_receipt import EthTransactionReceipt


class EthTransactionTraceProcessor(object):

    def filter_transfers_from_receipt(self, tx_receipt):
        # type: (EthTransactionReceipt) -> [EthErc20Transfer]

        return None

