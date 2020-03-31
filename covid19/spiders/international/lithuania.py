# -*- coding: utf-8 -*-
import re

import scrapy
from covid19.items import TestingStats
from datetime import datetime as dt
from dateutil.parser import parse
import logging

class LithuaniaSpider(scrapy.Spider):
    name = 'lithuania'
    allowed_domains = ['http://sam.lrv.lt/lt/']
    names = ["Lithuania"]
    case_categories = ["positive", "negative"]
    custom_settings = {"LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( 'http://sam.lrv.lt/lt/naujienos/koronavirusas', callback=self.parse )

    def parse(self, response):
        item = TestingStats()

        date = dt.now()

        positive = response.xpath( '//*[@id="module_Structure"]/div[1]/div[2]/div[3]/div[3]/ul/li[1]/b/text()' ).get()

        total = response.xpath( '//*[@id="module_Structure"]/div[1]/div[2]/div[3]/div[3]/ul/li[5]/text()' ).get()
        total = total.split( ":" )[-1]

        deaths = response.xpath( '/html/body/div[1]/div[2]/div[3]/div[3]/ul/li[3]/b/text()' ).get()
        deaths = re.split( " |\xa0", deaths )[1]

        item["date"] = date.strftime("%Y-%m-%d")
        item["name"] =  self.names[0]
        item["positive"] = int( positive )
        item["negative"] = int( total ) - int( positive )
        item["deaths"] = int( deaths )

        print( item.toAsciiTable() )
        return item

