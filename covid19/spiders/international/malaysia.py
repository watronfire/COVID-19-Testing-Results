# -*- coding: utf-8 -*-
import scrapy
from covid19.items import TestingStats
from datetime import datetime as dt
from dateutil.parser import parse
import logging

class MalaysiaSpider(scrapy.Spider):
    name = 'malaysia'
    allowed_domains = ['http://www.moh.gov.my/']
    names = ["Malaysia"]
    case_categories = ["positive", "negative", "pending"]
    custom_settings = {"LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( 'http://www.moh.gov.my/index.php/pages/view/2019-ncov-wuhan', callback=self.parse )

    def parse(self, response):
        item = TestingStats()
        item["date"] = dt.now().strftime("%Y-%m-%d %H:%M %p")
        item["name"] = self.names[0]

        date = dt.now()

        data_table = response.xpath( '//*[@id="container_content"]/div[1]/center[1]/table/tbody' )

        for j, i in enumerate( data_table.xpath( 'tr' )[:3] ):
            item[self.case_categories[j]] = i.xpath( "td[2]/span/text()" ).get()

        item["deaths"] = response.xpath( '//*[@id="container_content"]/div[1]/center[3]/table/tbody/tr[3]/td[2]/span/text()' ).get()

        print( item.toAsciiTable() )
        return item

