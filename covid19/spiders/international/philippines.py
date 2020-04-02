# -*- coding: utf-8 -*-
import scrapy
from covid19.items import TestingStats
from datetime import datetime as dt
from dateutil.parser import parse
import logging
import json

class PhilippinesSpider(scrapy.Spider):
    name = 'philippines'
    allowed_domains = ['https://www.doh.gov.ph']
    names = ["Philippines"]
    case_categories = ["positive", "negative"]
    custom_settings = {"LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://www.doh.gov.ph/2019-nCoV/", callback=self.parse )

    def parse(self, response):
        item = TestingStats()

        positive = response.xpath( '//*[@id="block-block-17"]/div/table/tbody/tr[1]/td[2]/p/font/b/text()' ).get()
        positive = positive.replace( ',', '' )

        negative = response.xpath( '//*[@id="block-block-17"]/div/table/tbody/tr[2]/td[2]/p/font/b/text()' ).get()
        negative = negative.replace( ',', '' )

        pending = response.xpath( '//*[@id="block-block-17"]/div/table/tbody/tr[3]/td[2]/p/font/b/text()' ).get()
        pending = pending.replace( ',', '' )

        date = response.xpath( '/html/body/div[3]/div[6]/div/div/div/div/div/div[1]/div[1]/h3/strong/span/text()' ).get()
        date = parse( date, fuzzy=True )

        # Currently the api returns an empty date
        #item["date"] = parse( api_call["data"]["LastUpdated"], fuzzy=True )
        item["date"] = date.strftime( "%Y-%m-%d" )
        item["name"] =  self.names[0]
        item["positive"] = int( positive )
        item["negative"] = int( negative )
        item["pending"] = int( pending )

        print( item.toAsciiTable() )
        return item

