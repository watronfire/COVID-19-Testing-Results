# -*- coding: utf-8 -*-
import scrapy
from covid19.items import TestingStats
from datetime import datetime as dt
from dateutil.parser import parse
import logging

class EstoniaSpider(scrapy.Spider):
    name = 'estonia'
    allowed_domains = ['https://www.kriis.ee/en']
    names = ["Estonia"]
    case_categories = ["positive", "negative"]
    custom_settings = {"LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( 'https://www.kriis.ee/en', callback=self.parse )

    def parse(self, response):
        item = TestingStats()
        item["date"] = dt.now().strftime( "%Y-%m-%d" )
        item["name"] = self.names[0]

        total =  response.xpath( '//*[@id="block-block-12"]/div/div/div/div[1]/div[2]/h2/text()' ).get()
        positive = response.xpath( '//*[@id="block-block-12"]/div/div/div/div[2]/div[2]/h2/text()' ).get()

        item["deaths"] = response.xpath( '//*[@id="block-block-12"]/div/div/div/div[3]/div[2]/h2/text()' ).get()

        item["positive"] = positive
        item["negative"] = int( total ) - int( positive )

        print( item.toAsciiTable() )
        return item

