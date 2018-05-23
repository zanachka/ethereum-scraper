# -*- coding: utf-8 -*-

# Define your middlewares here
#
# Don't forget to add your middleware to the DOWNLOADER_MIDDLEWARES setting
# See: https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
import json
import logging

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.exceptions import IgnoreRequest
from scrapy.http import Response, TextResponse

logger = logging.getLogger(__name__)


class EthereumScraperErrorHandlerMiddleware(RetryMiddleware):

    def process_response(self, request, response, spider):
        # Call RetryMiddleware first
        response = super(EthereumScraperErrorHandlerMiddleware, self).process_response(request, response, spider)
        # RetryMiddleware returns Request for retries.
        if isinstance(response, Response):
            error = None

            if not isinstance(response, TextResponse):
                error = 'not TextResponse'
            elif response.status >= 300:
                error = 'non-2xx status'

            if error is not None:
                block_number = request.meta.get('block_number', 'unknown')
                tx_hash = request.meta.get('tx_hash', 'unknown')
                error_message = 'ethscraper error - reason: {}, block_number: {}, tx_hash: {}, body:\n' \
                                '{}\n' \
                                'Response - status: {}, body:\n' \
                                '{}' \
                    .format(error, block_number, tx_hash, request.body, response.status, response.body)
                logger.error(error_message)
                raise IgnoreRequest('The response is ignored because of an error {}'.format(error))

        return response

    def process_exception(self, request, exception, spider):
        # Call RetryMiddleware first
        retried_request = super(EthereumScraperErrorHandlerMiddleware, self).process_exception(request, exception, spider)
        # If not retried
        if retried_request is None:
            block_number = request.meta.get('block_number', 'unknown')
            tx_hash = request.meta.get('tx_hash', 'unknown')

            error_message = 'ethscraper error - reason: exception, block_number: {}, tx_hash: {}, body:\n' \
                            '{}\n' \
                            'Exception:\n' \
                            '{}\n'\
                .format(block_number, tx_hash, request.text, repr(exception))
            logger.error(error_message)

        return retried_request

    @staticmethod
    def has_result(response):
        try:
            json_response = json.loads(response.text)
            return 'result' in json_response and json_response['result'] is not None
        except Exception as e:
            logger.error('Exception while parsing response ' + repr(e))
            return False


# Will not be invoked until this bug is fixed https://github.com/scrapy/scrapy/issues/1015
class EthereumScraperErrorHandlerSpiderMiddleware(object):

    def process_spider_exception(self, response, exception, spider):
        request = response.request
        block_number = request.meta.get('block_number', 'unknown')
        tx_hash = request.meta.get('tx_hash', 'unknown')

        error_message = 'ethscraper error - reason: spider exception, block_number: {}, tx_hash: {}, body:\n' \
                        '{}\n' \
                        'Exception:\n' \
                        '{}\n' \
            .format(block_number, tx_hash, request.text, repr(exception))
        logger.error(error_message)

