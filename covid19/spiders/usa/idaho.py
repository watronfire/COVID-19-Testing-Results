# -*- coding: utf-8 -*-
import scrapy
from covid19.items import TestingStats
from datetime import datetime as dt
import logging

class ArkansasSpider(scrapy.Spider):
    name = 'idaho'
    allowed_domains = ['https://coronavirus.idaho.gov/']
    names = ["Idaho"]
    case_categories = ["positive", "negative", "pending", "pui"]
    custom_settings = {"LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://coronavirus.idaho.gov/", callback=self.parse )

    def parse(self, response):
        item = TestingStats()

        date = response.xpath( '/html/body/div[1]/div[2]/div[1]/main/div/div/div/section/div/div/div/div[1]/div/p[4]/em/text()' ).get()
        date = date.replace( ".", "" )
        date = dt.strptime( date, "* Data as of %I:%M %p MT %m/%d/%Y ")

        # Often these changes from b to strong or vice-versa.

        table_values = list()
        for i in response.xpath( '/html/body/div[1]/div[2]/div[1]/main/div/div/div/section/div/div/div/div[1]/div/figure/table/tbody/tr' ):
            _ = i.xpath( 'td[2]/text()' ).get()
            print( _ )
            table_values.append( int( _ ) )

        deaths = 0

        item["date"] = date.strftime("%Y-%m-%d %H:%M %p")
        item["name"] =  self.names[0]
        total = table_values[2] + table_values[3]
        item["negative"] = total - table_values[4]
        item["positive"] = table_values[4]
        item["deaths"] = deaths

        print( item.toAsciiTable() )
        return item

