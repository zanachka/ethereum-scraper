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
geth --rpc --rpcapi eth
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


### Internal Transactions

Retrieving internal transactions requires transaction tracing. Since that's potentially a very long running 
operation (hours) and can also result in huge amounts of data, an IPC subscription should be used instead of RPC.

An example is given in this PR [https://github.com/ethereum/go-ethereum/pull/15516](https://github.com/ethereum/go-ethereum/pull/15516)

```
$ nc -U /work/temp/rinkeby/geth.ipc
{"id": 1, "method": "debug_subscribe", "params": ["traceChain", "0x0", "0xffff", {"tracer": "callTracer"}]}
```

The API will stream back one RPC notification per non-empty block. An exception is the very last block, which will 
be reported even if empty so the user knows the stream is done.

```
{"jsonrpc":"2.0","id":1,"result":"0xe1deecc4b399e5fd2b2a8abbbc4624e2"}
{"jsonrpc":"2.0","method":"debug_subscription","params":{"subscription":"0xe1deecc4b399e5fd2b2a8abbbc4624e2","result":{"block":"0x37","hash":"0xdb16f0d4465f2fd79f10ba539b169404a3e026db1be082e7fd6071b4c5f37db7","traces":[{"from":"0x31b98d14007bdee637298086988a0bbd31184523","gas":"0x0","gasUsed":"0x0","input":"0x","output":"0x","time":"1.077µs","to":"0x2ed530faddb7349c1efdbf4410db2de835a004e4","type":"CALL","value":"0xde0b6b3a7640000"}]}}}
{"jsonrpc":"2.0","method":"debug_subscription","params":{"subscription":"0xe1deecc4b399e5fd2b2a8abbbc4624e2","result":{"block":"0xf43","hash":"0xacb74aa08838896ad60319bce6e07c92edb2f5253080eb3883549ed8f57ea679","traces":[{"from":"0x31b98d14007bdee637298086988a0bbd31184523","gas":"0x0","gasUsed":"0x0","input":"0x","output":"0x","time":"1.568µs","to":"0xbedcf417ff2752d996d2ade98b97a6f0bef4beb9","type":"CALL","value":"0xde0b6b3a7640000"}]}}}
{"jsonrpc":"2.0","method":"debug_subscription","params":{"subscription":"0xe1deecc4b399e5fd2b2a8abbbc4624e2","result":{"block":"0xf47","hash":"0xea841221179e37ca9cc23424b64201d8805df327c3296a513e9f1fe6faa5ffb3","traces":[{"from":"0xbedcf417ff2752d996d2ade98b97a6f0bef4beb9","gas":"0x4687a0","gasUsed":"0x12e0d","input":"0x6060604052341561000c57fe5b5b6101828061001c6000396000f30060606040526000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff168063230925601461003b575bfe5b341561004357fe5b61008360048080356000191690602001909190803560ff1690602001909190803560001916906020019091908035600019169060200190919050506100c5565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b6000600185858585604051806000526020016040526000604051602001526040518085600019166000191681526020018460ff1660ff1681526020018360001916600019168152602001826000191660001916815260200194505050505060206040516020810390808403906000866161da5a03f1151561014257fe5b50506020604051035190505b9493505050505600a165627a7a7230582054abc8e7b2d8ea0972823aa9f0df23ecb80ca0b58be9f31b7348d411aaf585be0029","output":"0x60606040526000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff168063230925601461003b575bfe5b341561004357fe5b61008360048080356000191690602001909190803560ff1690602001909190803560001916906020019091908035600019169060200190919050506100c5565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b6000600185858585604051806000526020016040526000604051602001526040518085600019166000191681526020018460ff1660ff1681526020018360001916600019168152602001826000191660001916815260200194505050505060206040516020810390808403906000866161da5a03f1151561014257fe5b50506020604051035190505b9493505050505600a165627a7a7230582054abc8e7b2d8ea0972823aa9f0df23ecb80ca0b58be9f31b7348d411aaf585be0029","time":"658.529µs","to":"0x5481c0fe170641bd2e0ff7f04161871829c1902d","type":"CREATE","value":"0x0"}]}}}
{"jsonrpc":"2.0","method":"debug_subscription","params":{"subscription":"0xe1deecc4b399e5fd2b2a8abbbc4624e2","result":{"block":"0xfff","hash":"0x254ccbc40eeeb183d8da11cf4908529f45d813ef8eefd0fbf8a024317561ac6b"}}}
```

Individual block tracing is concurrent in the transactions (limited to num cores) and also makes chain 
tracing concurrent in the blocks (limited to num cores).


## Etherscan Scraper

To scrape contract bytecode and Solidity code from Etherscan:

```
> pip install Scrapy
> scrapy runspider ethscraper/spiders/etherscan_contract_spider.py -o data.csv
```

Note that CloudFlare will block your machine after a few thousand requests. Be aware that web scraping is considered 
bad practice. This can break without notice, as it is obviously relying on how the frontend is rendered.

