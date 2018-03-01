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

The output will be in `blocks.csv` and `transactions.csv` in the current directory.

To scrape from local Ethereum node start `geth` with `--rpc` flag:

```
geth --rpc --rpccorsdomain "*"
```

Then use `ETH_JSON_RPC_URL=http://localhost:8545`

### Schema

`blocks.csv`

Column                 | Type               |
-----------------------|---------------------
block_number           | bigint             |
block_hash             | hex_string         |
block_parentHash       | hex_string         |
block_nonce            | hex_string         |
block_sha3Uncles       | hex_string         |
block_logsBloom        | hex_string         |
block_transactionsRoot | hex_string         |
block_stateRoot        | hex_string         |
block_miner            | hex_string         |
block_difficulty       | bigint             |
block_totalDifficulty  | bigint             |
block_size             | bigint             |
block_extraData        | hex_string         |
block_gasLimit         | bigint             |
block_gasUsed          | bigint             |
block_timestamp        | bigint             |
block_transactionCount | bigint             |

`transactions.csv`

Column              |    Type     |
--------------------|--------------
tx_hash             | hex_string  |
tx_nonce            | bigint      |
tx_blockHash        | hex_string  |
tx_blockNumber      | bigint      |
tx_transactionIndex | bigint      |
tx_from             | hex_string  |
tx_to               | hex_string  |
tx_value            | bigint      |
tx_gas              | bigint      |
tx_gasPrice         | bigint      |
tx_input            | hex_string  |


## Etherscan Scraper

To scrape contract bytecode and Solidity code from Etherscan:

```
> pip install Scrapy
> scrapy runspider ethscraper/spiders/etherscan_contract_spider.py -o data.csv
```

Note that CloudFlare will block your machine after a few thousand requests.