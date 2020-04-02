# -*- coding: utf-8 -*-
import scrapy
from covid19.items import TestingStats
from datetime import datetime as dt
from dateutil.parser import parse
import logging
import json

class PalestineSpider(scrapy.Spider):
    name = 'palestine'
    allowed_domains = ['http://corona.ps/']
    names = ["Palestine"]
    case_categories = ["positive", "negative"]
    custom_settings = {"LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "http://corona.ps/API/summary", callback=self.parse )

    def parse(self, response):
        item = TestingStats()

        api_call = json.loads( response.body_as_unicode() )

        # Currently the api returns an empty date
        #item["date"] = parse( api_call["data"]["LastUpdated"], fuzzy=True )
        item["date"] = dt.now().strftime( "%Y-%m-%d" )
        item["name"] =  self.names[0]
        item["positive"] = int( api_call["data"]["TotalCases"] )
        item["negative"] = int( api_call["data"]["TotalTestedSamples"] ) - int( api_call["data"]["TotalCases"] )
        item["deaths"] = int( api_call["data"]["TotalDeath"] )

        print( item.toAsciiTable() )
        return item

