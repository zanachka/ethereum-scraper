# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter, XmlItemExporter, JsonItemExporter, JsonLinesItemExporter

from ethscraper.utils import without_key

TYPE_FIELD = 'type'


class EthereumScraperExportPipeline(object):

    def open_spider(self, spider):
        self.item_type_to_exporter = {}
        self.export_format = spider.settings.get('EXPORT_FORMAT', 'csv')

    def close_spider(self, spider):
        for exporter in self.item_type_to_exporter.values():
            exporter.finish_exporting()

    def _exporter_for_item(self, item):
        item_type = item.get(TYPE_FIELD, None)
        if item_type is not None and item_type not in self.item_type_to_exporter:
            filename = self.filename_for_item_type(item_type)
            f = open(filename + '.' + self.export_format, 'wb')
            exporter = self.exporter_for_format(self.export_format, f)
            exporter.start_exporting()
            self.item_type_to_exporter[item_type] = exporter
        return self.item_type_to_exporter.get(item_type, None)

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        if exporter is not None:
            exporter.export_item(without_key(dict(item), TYPE_FIELD))
        return item

    @staticmethod
    def filename_for_item_type(item_type):
        if item_type == 'b':
            return 'blocks'
        elif item_type == 't':
            return 'transactions'
        else:
            return 'unknown'

    @staticmethod
    def exporter_for_format(export_format, f):
        if export_format == 'csv':
            return CsvItemExporter(f)
        elif export_format == 'xml':
            return XmlItemExporter(f)
        elif export_format == 'json':
            return JsonItemExporter(f)
        elif export_format == 'jl':
            return JsonLinesItemExporter(f)
        else:
            raise ValueError('format {} is not supported'.format(export_format))
