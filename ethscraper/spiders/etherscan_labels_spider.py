"""Module for scraping Etherscan for tokens."""

import sys
# -*- coding: utf-8 -*-
from time import sleep

import scrapy

import re


class EtherscanLabelsSpider(scrapy.Spider):
    """Class for scraping Etherscan for labels."""

    name = "EtherscanLabelsSpider"
    start_urls = ['https://etherscan.io/labelcloud']
    allowed_domains = ["etherscan.io"]
    page = 1
    download_delay = 1
    seconds_to_sleep = 20
    max_throttles_before_giving_up = 5
    throttle_counter = 0

    def parse(self, response):
        root_url = 'https://etherscan.io'
        rot_label_elems = response.css('.mb-3 .col-md-4 .dropdown')
        counter = 0
        for root_label_elem in rot_label_elems:
            if counter >= 10:
                break
            counter = counter + 1

            root_label = strip(root_label_elem.css('button span::text').extract_first())
            root_label_urls = root_label_elem.css('a::attr(href)')

            for root_label_url in root_label_urls:
                label_list_request = scrapy.Request(root_url + root_label_url.extract(), callback=self.parse_label_list)
                label_list_request.meta['root_label'] = root_label
                yield label_list_request

    def parse_label_list(self, response):
        def e(path):
            return response.css(path).extract_first()

        root_label = response.meta.get('root_label', None)

        table_row_elems = response.css('.card-body tbody tr')

        items = []
        for table_row_elem in table_row_elems:
            address = table_row_elem.css('td:nth-child(1) a::text').extract_first()

            label = strip(table_row_elem.css('td:nth-child(2)::text').extract_first())
            items.append({
                'address': address,
                'label': label
            })
            items.append({
                'address': address,
                'label': root_label
            })

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

        return items


def strip(str):
    if str is None:
        return None
    return str.strip()
