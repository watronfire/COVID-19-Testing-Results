# -*- coding: utf-8 -*-
import scrapy
from covid19.items import TestingStats
from datetime import datetime as dt
import logging
from dateutil.parser import parse

class AlaskaSpider(scrapy.Spider):
    name = 'alaska'
    allowed_domains = ['http://dhss.alaska.gov/']
    names = ["Alaska"]
    case_categories = ["positive", "negative", "pending", "pui"]
    custom_settings = {"LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "http://dhss.alaska.gov/dph/Epi/id/Pages/COVID-19/monitoring.aspx", callback=self.parse )

    def parse(self, response):
        item = TestingStats()

        date = response.xpath( '/html/body/form/div[3]/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/div/p/em/text()' ).get()
        date = parse( date, fuzzy=True )

        positive = response.xpath( '/html/body/form/div[3]/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/div[1]/ul[1]/li[2]/text()' ).get()
        positive = positive.split( ": " )[-1]

        negative = response.xpath( '/html/body/form/div[3]/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/div[1]/ul[2]/li[3]/text()' ).get()
        negative = negative.split( ": " )[-1]

        deaths = 0

        item["date"] = date.strftime("%Y-%m-%d %H:%M %p")
        item["name"] =  self.names[0]
        item["positive"] = positive
        item["negative"] = negative
        item["deaths"] = deaths

        print( item.toAsciiTable() )
        return item

