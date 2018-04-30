# -*- coding: utf-8 -*-

# Define your middlewares here
#
# Don't forget to add your middleware to the DOWNLOADER_MIDDLEWARES setting
# See: https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
import json
import logging

from scrapy import Request
from scrapy.downloadermiddlewares.retry import RetryMiddleware

logger = logging.getLogger(__name__)


class EthereumScraperErrorHandlerMiddleware(RetryMiddleware):

    def process_response(self, request, response, spider):
        # Call RetryMiddleware first
        response = super(EthereumScraperErrorHandlerMiddleware, self).process_response(request, response, spider)
        failed = response.status >= 300 or not self.has_result(response)
        # If it's a failure and not retried
        if failed and not isinstance(response, Request):
            block_number = request.meta.get('block_number', 'unknown')
            tx_hash = request.meta.get('tx_hash', 'unknown')

            error_message = 'ethscraper error - block_number: {}, tx_hash: {}, body:\n' \
                            '{}\n' \
                            'Response - status: {}, body:\n' \
                            '{}' \
                .format(block_number, tx_hash, request.body, response.status, response.body)

            logger.error(error_message)

        return response

    def process_exception(self, request, exception, spider):
        # Call RetryMiddleware first
        retried = super(EthereumScraperErrorHandlerMiddleware, self).process_exception(request, exception, spider)
        # If not retried
        if retried is None:
            block_number = request.meta.get('block_number', 'unknown')
            tx_hash = request.meta.get('tx_hash', 'unknown')

            error_message = 'ethscraper error - block_number: {}, tx_hash: {}, body:\n' \
                            '{}\n'\
                .format(block_number, tx_hash, request.body)
            logger.error(error_message)

        return retried

    @staticmethod
    def has_result(response):
        try:
            json_response = json.loads(response.body_as_unicode())
            return 'result' in json_response and json_response['result'] is not None
        except Exception as e:
            logger.error('Exception while parsing response ' + repr(e))
            return False
