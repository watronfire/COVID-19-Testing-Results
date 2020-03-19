# -*- coding: utf-8 -*-
import scrapy
from covid19.items import TestingStats
from datetime import datetime as dt
from dateutil.parser import parse
import logging

class IndianaSpider(scrapy.Spider):
    name = 'indiana'
    allowed_domains = ['https://www.in.gov/']
    names = ["Indiana"]
    case_categories = ["positive", "negative", "pending", "pui"]
    custom_settings = {"LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://www.in.gov/coronavirus/", callback=self.parse )

    def parse(self, response):
        item = TestingStats()

        date = response.xpath( '/html/body/div/div/div/div/div/div/margin-container/full-container/div[1]/margin-container/full-container/div/div/nav/span/div/div/h3/strong/text()' ).get()
        date = parse( date, fuzzy=True )
        print( date )

        # Often these changes from b to strong or vice-versa.

        table_values = list()
        for i in response.xpath( '/html/body/div[1]/div[2]/div[1]/main/div/div/div/section/div/div/div/div[1]/div/figure/table/tbody/tr' ):
            _ = i.xpath( 'td[2]/text()' ).get()
            print( _ )
            table_values.append( int( _ ) )

        deaths = 0

        item["date"] = date.strftime("%Y-%m-%d %H:%M %p")
        item["name"] =  self.names[0]
        item["positive"] = table_values[2] + table_values[3]
        item["negative"] = table_values[4]
        item["deaths"] = deaths

        print( item.toAsciiTable() )
        return item

