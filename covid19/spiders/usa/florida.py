# -*- coding: utf-8 -*-
import scrapy
from covid19.items import TestingStats
from datetime import datetime as dt
import logging

# Deprecated: No longer reporting negative tests.
class FloridaSpider(scrapy.Spider):
    name = 'florida'
    allowed_domains = ['http://www.floridahealth.gov/']
    names = ["Florida State"]
    case_categories = ["positive", "negative", "pending", "pui"]
    custom_settings = {"LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "http://www.floridahealth.gov/diseases-and-conditions/COVID-19/", callback=self.parse )

    def parse(self, response):
        item = TestingStats()

        #date = response.xpath( '/html/body/div[1]/div[3]/div/div[2]/div[3]/div/div[1]/block/p[1]/sup/text()' ).get()
        date = response.xpath( '/html/body/div[2]/div/div/div[3]/div[1]/p/text()' ).get()
        date = date.replace( ".", "" ).split( "of " )[-1]
        date = dt.strptime( date, "%I:%M %p ET %m/%d/%Y")

        positive = response.xpath( '/html/body/div[2]/div/div/div[3]/div[2]/div[1]/div/div[1]/h2/text()' ).get()
        positive = positive.split( " " )[0]

        negative = response.xpath( '/html/body/div[1]/div[3]/div/div[2]/div[3]/div/div[1]/block/div[5]/text()' ).get()

        pending = response.xpath( '/html/body/div[1]/div[3]/div/div[2]/div[3]/div/div[1]/block/div[6]/text()' ).get()

        deaths = response.xpath( '/html/body/div[2]/div/div/div[3]/div[4]/div/table/tbody/tr[2]/td[2]/text()' ).get()

        item["date"] = date.strftime("%Y-%m-%d %H:%M %p")
        item["name"] =  "Florida",
        item["positive"] = positive
        item["pending"] = pending
        item["negative"] = negative

        print( item.toAsciiTable() )
        return item

