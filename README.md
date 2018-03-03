# Ethereum Scraper

## JSON RPC Scraper

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

### Usage
 
Run in the terminal:

```
> pip install Scrapy
> scrapy runspider ethscraper/spiders/eth_json_rpc_spider.py \
-s ETH_JSON_RPC_URL=https://mainnet.infura.io/<your_api_key> \
-s START_BLOCK=0 \
-s END_BLOCK=1000000 \
-s FEED_FORMAT=csv
```

The output will be in 
`blocks.csv`, 
`transactions.csv`, 
`erc20_transfers.csv` 
in the current directory.


### Options

#### `ETH_JSON_RPC_URL`

The Ethereum node JSON RPC url. 
If running a local geth node start it with `--rpc` option:

```
geth --rpc --rpccorsdomain "*"
```

Then use `ETH_JSON_RPC_URL=http://localhost:8545`.

#### `START_BLOCK`, `END_BLOCK`

Integers representing the start and end blocks for scraping, inclusive. 

#### `FEED_FORMAT`

Output format. The output files will have the corresponding extension.

Supported formats are: 
`csv`, 
`xml`, 
`json`,
[`jsonlines`](http://jsonlines.org/examples/), 
[`pickle`](https://docs.python.org/2/library/pickle.html), 
`marshal`.

#### `EXPORT_TRANSACTIONS`

Whether to export `transactions.csv` file.
Possible values: `True`, `False`. 

#### `EXPORT_ERC20_TRANSFERS`

Whether to export `erc20_transfers.csv` file.
Possible values: `True`, `False`.


## Etherscan Scraper

To scrape contract bytecode and Solidity code from Etherscan:

```
> pip install Scrapy
> scrapy runspider ethscraper/spiders/etherscan_contract_spider.py -o data.csv
```

Note that CloudFlare will block your machine after a few thousand requests.