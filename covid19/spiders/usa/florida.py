# -*- coding: utf-8 -*-
import scrapy
from covid19.items import TestingStats
from datetime import datetime as dt
import logging

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

        date = response.xpath( '/html/body/div[1]/div[3]/div/div[2]/div[3]/div/div[1]/block/p[1]/sup/text()' ).get()
        date = date.replace( ".", "" )
        date = dt.strptime( date, "as of %I:%M %p ET %m/%d/%Y")

        positive = response.xpath( '/html/body/div[1]/div[3]/div/div[2]/div[3]/div/div[1]/block/div[1]/text()' ).get()
        positive = int( positive.split( " " )[0] )

        nonlocal_positive = response.xpath( '/html/body/div[1]/div[3]/div/div[2]/div[3]/div/div[1]/block/div[3]/text()' ).get()
        nonlocal_positive = int( nonlocal_positive.split( " " )[0] )

        negative = response.xpath( '/html/body/div[1]/div[3]/div/div[2]/div[3]/div/div[1]/block/div[5]/text()' )
        negative = int( negative.get() )

        pending = response.xpath( '/html/body/div[1]/div[3]/div/div[2]/div[3]/div/div[1]/block/div[6]/text()' )
        pending = int( pending.get() )

        pui = response.xpath( '/html/body/div[1]/div[3]/div/div[2]/div[3]/div/div[1]/block/div[7]/text()' ).get()
        pui = int( pui.split( " " )[0] )

        item["date"] = date.strftime("%Y-%m-%d %H:%M %p")
        item["Local"] = {
            "name": "Florida",
            "positive": positive,
            "pending": pending,
            "negative": negative,
            "pui": pui
        }
        item["NonLocal"] = {
            "name": "Non Florida",
            "positive": nonlocal_positive
        }
        print( item.toAsciiTable() )
        return item

