# Ethereum Scraper
 
Update the settings in `ethereumScraper/settings.py`:

```
ETH_JSON_RPC_URL = 'https://mainnet.infura.io/XXXXXXXXXXXXXXXXXXX'
START_BLOCK = 0
END_BLOCK = 1000000
```
 
Run in command line:

```
> pip install Scrapy
> scrapy runspider ethereumScraper/spiders/eth_json_rpc_spider.py >> data.log 2>> data.err
```

The output will be in blocks.csv and transactions.csv in the current directory.

To scrape from local Ethereum node start geth with --rpc flag:

```
geth --rpc --rpccorsdomain "*"
```

---

To scrape contract bytecode and Solidity code from Etherscan:

```
> pip install Scrapy
> scrapy runspider ethereumScraper/spiders/etherscan_contract_spider.py -o data.csv  >> data.log 2>> data.err
```