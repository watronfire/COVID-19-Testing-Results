# -*- coding: utf-8 -*-
import scrapy
from covid19.items import TestingStats
from datetime import datetime as dt
from dateutil.parser import parse
import logging

class IcelandSpider(scrapy.Spider):
    name = 'iceland'
    allowed_domains = ['https://www.covid.is/data']
    names = ["Iceland"]
    case_categories = ["positive", "negative"]
    custom_settings = {"LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( 'https://www.covid.is/data', callback=self.parse )

    def parse(self, response):
        item = TestingStats()
        item["date"] = dt.now().strftime( "%Y-%m-%d" )
        item["name"] = self.names[0]

        total =  response.xpath( "/html/body/div[2]/div/div[1]/div[1]/div[1]/div/div/div/div[1]/div/div[28]/div/div/div/div/div[2]/div[1]/span/text()" ).get()
        positive = response.xpath( '/html/body/div[2]/div/div[1]/div[1]/div[1]/div/div/div/div[1]/div/div[10]/div/div/div/div/div[2]/div[1]/text()' ).get()

        item["deaths"] = 2

        item["positive"] = positive
        item["negative"] = int( total ) - int( positive )

        print( item.toAsciiTable() )
        return item

