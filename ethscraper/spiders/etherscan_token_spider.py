"""Module for scraping Etherscan for tokens."""

import sys
# -*- coding: utf-8 -*-
from time import sleep

import scrapy

import re


class EtherscanTokenSpider(scrapy.Spider):
    """Class for scraping Etherscan for tokens."""

    name = "EtherscanTokenSpider"
    start_urls = ['https://etherscan.io/tokens']
    allowed_domains = ["etherscan.io"]
    page = 1
    download_delay = 1
    seconds_to_sleep = 20
    max_throttles_before_giving_up = 5
    throttle_counter = 0

    def parse(self, response):
        root_url = 'https://etherscan.io'
        tokens = response.css('h3')
        for token_row in tokens:
            url = root_url + token_row.css('a::attr(href)').extract_first()
            name_with_symbol = token_row.css('a::text').extract_first()

            details_request = scrapy.Request(url, callback=self.parse_detail)
            details_request.meta['name_with_symbol'] = name_with_symbol
            yield details_request
            break

        if tokens:
            self.page = self.page + 1
            next_page = root_url + ('/tokens?p=%d' % self.page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_detail(self, response):
        """Parse detail page."""

        def e(path):
            return response.css(path).extract_first()

        name_with_symbol = response.meta.get('name_with_symbol', None)
        price = parse_price(e('#ContentPlaceHolder1_tr_valuepertoken > td:nth-child(2)::text'))
        decimals = parse_decimals(e('#ContentPlaceHolder1_trDecimals > td:nth-child(2)::text'))
        item = {
            'name': parse_name_and_symbol(name_with_symbol)[0],
            'symbol': parse_name_and_symbol(name_with_symbol)[1],
            'eth_address': e('#ContentPlaceHolder1_trContract > td.tditem > a::text'),
            'price': price,
            'decimals': decimals,
        }

        if response.css('#address::text').extract_first() == '{Request Throttled}':
            self.throttle_counter = self.throttle_counter + 1
            if self.throttle_counter > self.max_throttles_before_giving_up:
                print('Request throttled %d times - exiting ...' % self.max_throttles_before_giving_up)
                sys.exit()
            print('Request throttled #%d - sleeping %d seconds ...' %
                  (self.throttle_counter, self.seconds_to_sleep))
            sleep(self.seconds_to_sleep)
            return
        else:
            self.throttle_counter = 0

        return {k: v for k, v in item.items() if v is not None}


def parse_decimals(str):
    if str is None:
        return None
    try:
        return int(str) if int(str) < 256 else None
    except ValueError:
        return None

def parse_name_and_symbol(name_with_symbol):
    if name_with_symbol is None or len(name_with_symbol) == 0:
        return '', ''

    m = re.search('(.+) \((.*)\)', name_with_symbol)
    if m:
        groups = m.groups()
        if len(groups) > 1:
            return groups
        elif len(groups) == 1:
            return groups[0], ''
    else:
        return '', ''


def parse_price(price_text):
    if price_text is None or len(price_text) == 0:
        return None

    m = re.search('\$([\d.]+).*', price_text)
    if m:
        groups = m.groups()
        if len(groups) == 1:
            return groups[0]

    return None
