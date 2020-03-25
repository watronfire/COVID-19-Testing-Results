# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter


class Covid19Pipeline(object):

    def __init__(self):
        self.file = open( "/Users/natem/Dropbox (Scripps Research)/Personal/Code/Python/crawl-covid19-cases/data/cleaned_international.csv", "ab" )
        self.exporter = CsvItemExporter( self.file, include_headers_line=False )
        self.exporter.start_exporting()

    def close_spider( self, spider ):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item( item )
        return item
