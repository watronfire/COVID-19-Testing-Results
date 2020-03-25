# -*- coding: utf-8 -*-
import scrapy
from covid19.items import TestingStats
from datetime import datetime as dt
import logging
from dateutil.parser import parse

class DistrictColumbiaSpider( scrapy.Spider ):
    name = 'dc'
    allowed_domains = ['https://coronavirus.dc.gov/']
    names = ["District of Columbia"]
    case_categories = ["positive", "negative", "pending"]
    custom_settings = {"LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://coronavirus.dc.gov/page/coronavirus-data", callback=self.parse )

    def parse(self, response):
        item = TestingStats()

        date = response.xpath( '//*[@id="node-page-1464296"]/div[1]/div/div/div/p[1]/strong/text()[1]' ).get()
        date = parse( date, fuzzy=True )

        values = list()
        for i in response.xpath( '//*[@id="node-page-1464296"]/div[1]/div/div/div/ul[1]/li' ):
            _ = i.xpath( 'text()' ).get()
            _ = _.split( ":" )[-1]
            values.append( int( _ ) )

        deaths = 0
        #print( values )

        item["date"] = date.strftime("%Y-%m-%d %H:%M %p")
        item["name"] =  self.names[0]
        item["positive"] = values[1] + values[2]
        item["negative"] = values[3] + values[4]
        item["pending"] = values[5]
        item["deaths"] = deaths

        print( item.toAsciiTable() )
        return item

