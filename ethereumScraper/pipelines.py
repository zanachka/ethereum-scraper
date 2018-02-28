# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter


class EthereumScraperExportPipeline(object):

    def open_spider(self, spider):
        self.item_type_to_exporter = {}

    def close_spider(self, spider):
        for exporter in self.item_type_to_exporter.values():
            exporter.finish_exporting()

    def _exporter_for_item(self, item):
        item_type = item.get('type', None)
        if item_type is not None and item_type not in self.item_type_to_exporter:
            if item_type == 'b':
                f = open('blocks.csv', 'wb')
            elif item_type == 't':
                f = open('transactions.csv', 'wb')
            else:
                f = open('unknown.csv', 'wb')
            exporter = CsvItemExporter(f)
            exporter.start_exporting()
            self.item_type_to_exporter[item_type] = exporter
        return self.item_type_to_exporter.get(item_type, None)

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        if exporter is not None:
            exporter.export_item(item)
        return item
