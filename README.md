# Ethereum Scraper

## JSON RPC Scraper
 
Run in the terminal (change the ETH_JSON_RPC_URL parameter):

```
> pip install Scrapy
> scrapy runspider ethscraper/spiders/eth_json_rpc_spider.py \
-s ETH_JSON_RPC_URL=https://mainnet.infura.io/<your_api_key> \
-s START_BLOCK=0 \
-s END_BLOCK=1000000 \
-s FEED_FORMAT=csv
```

The output will be in `blocks.csv`, `transactions.csv`, `erc20_transfers.csv` in the current directory.

To scrape from local Ethereum node start `geth` with `--rpc` flag:

```
geth --rpc --rpccorsdomain "*"
```

Then use `ETH_JSON_RPC_URL=http://localhost:8545`

Transactions and ERC20 transfers export can be disabled with

```
-s EXPORT_TRANSACTIONS=False \
-s EXPORT_ERC20_TRANSFERS=False
```

### Feed Formats

- csv
- xml
- json
- jsonlines [http://jsonlines.org/examples/](http://jsonlines.org/examples/)
- pickle [https://docs.python.org/2/library/pickle.html](https://docs.python.org/2/library/pickle.html)
- marshal

### Schema

`blocks.csv`

Column                  | Type               |
------------------------|---------------------
block_number            | bigint             |
block_hash              | hex_string         |
block_parent_hash       | hex_string         |
block_nonce             | hex_string         |
block_sha3_uncles       | hex_string         |
block_logs_bloom        | hex_string         |
block_transactions_root | hex_string         |
block_state_root        | hex_string         |
block_miner             | hex_string         |
block_difficulty        | bigint             |
block_total_difficulty  | bigint             |
block_size              | bigint             |
block_extra_data        | hex_string         |
block_gas_limit         | bigint             |
block_gas_used          | bigint             |
block_timestamp         | bigint             |
block_transaction_count | bigint             |

`transactions.csv`

Column              |    Type     |
--------------------|--------------
tx_hash             | hex_string  |
tx_nonce            | bigint      |
tx_block_hash       | hex_string  |
tx_block_number     | bigint      |
tx_index            | bigint      |
tx_from             | hex_string  |
tx_to               | hex_string  |
tx_value            | bigint      |
tx_gas              | bigint      |
tx_gas_price        | bigint      |
tx_input            | hex_string  |

`erc20_transfers.csv`

Column              |    Type     |
--------------------|--------------
erc20_token         | hex_string  |
erc20_from          | hex_string  |
erc20_to            | hex_string  |
erc20_value         | bigint      |
erc20_tx_hash       | hex_string  |
erc20_block_number  | bigint      |



## Etherscan Scraper

To scrape contract bytecode and Solidity code from Etherscan:

```
> pip install Scrapy
> scrapy runspider ethscraper/spiders/etherscan_contract_spider.py -o data.csv
```

Note that CloudFlare will block your machine after a few thousand requests.