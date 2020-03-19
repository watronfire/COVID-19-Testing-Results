# -*- coding: utf-8 -*-
import scrapy
from covid19.items import TestingStats
from datetime import datetime as dt
import logging

class ArkansasSpider(scrapy.Spider):
    name = 'arkansas'
    allowed_domains = ['https://www.healthy.arkansas.gov/']
    names = ["Arkansaa"]
    case_categories = ["positive", "negative", "pending", "pui"]
    custom_settings = {"LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://www.healthy.arkansas.gov/programs-services/topics/novel-coronavirus", callback=self.parse )

    def parse(self, response):
        item = TestingStats()

        date = response.xpath( '/html/body/div[7]/div[1]/table[4]/thead/tr/th/text()' ).get()
        date = dt.strptime( date, "Status Update as of %B %d, %Y")

        # Often these changes from b to strong or vice-versa.
        positive = response.xpath( '/html/body/div[7]/div[1]/table[4]/tbody/tr[1]/td[2]/b/text()' ).get()
        negative = response.xpath( '/html/body/div[7]/div[1]/table[6]/tbody/tr[1]/td[2]/strong/text()' ).get()

        deaths = 0

        item["date"] = date.strftime("%Y-%m-%d %H:%M %p")
        item["name"] =  self.names[0]
        item["positive"] = positive
        item["negative"] = negative
        item["deaths"] = deaths

        print( item.toAsciiTable() )
        return item

