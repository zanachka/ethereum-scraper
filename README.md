# Ethereum Scraper
 
Run in command line (change the ETH_JSON_RPC_URL parameter):

```
> pip install Scrapy
> scrapy runspider ethereumScraper/spiders/eth_json_rpc_spider.py -s ETH_JSON_RPC_URL=https://mainnet.infura.io/XXXXXXXXXXXXXXXXXXX -s START_BLOCK=0 -s END_BLOCK=1000000
```

The output will be in blocks.csv and transactions.csv in the current directory.

To scrape from local Ethereum node start geth with `--rpc` flag:

```
geth --rpc --rpccorsdomain "*"
```

Use `ETH_JSON_RPC_URL=http://localhost:8545`

---

To scrape contract bytecode and Solidity code from Etherscan:

```
> pip install Scrapy
> scrapy runspider ethereumScraper/spiders/etherscan_contract_spider.py -o data.csv  >> data.log 2>> data.err
```

Note that CloudFlare will block your machine after a few thousand requests.