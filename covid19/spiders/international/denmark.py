# -*- coding: utf-8 -*-
import scrapy
from covid19.items import TestingStats
from datetime import datetime as dt
from dateutil.parser import parse
import logging

class DenmarkSpider(scrapy.Spider):
    name = 'denmark'
    allowed_domains = ['https://www.ssi.dk/']
    names = ["Denmark"]
    case_categories = ["positive", "negative"]
    custom_settings = {"LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://www.ssi.dk/aktuelt/sygdomsudbrud/coronavirus", callback=self.parse )

    def parse(self, response):
        item = TestingStats()

        #date = response.xpath( '/html/body/div[3]/div/div/div/div[2]/main/p/strong[1]/text()' ).get()
        #date = dt.strptime( date, 'Stand in Österreich, %d.%m.%Y, %H:%M Uhr' )
        date = dt.now()

        positive = response.xpath( '/html/body/div[1]/div[2]/section[5]/div[1]/table/tbody/tr[1]/td[3]/text()' ).get()
        positive = positive.replace( ".", "" )

        total = response.xpath( '/html/body/div[1]/div[2]/section[5]/div[1]/table/tbody/tr[1]/td[2]/text()' ).get()
        total = total.replace( ".", "" )

        deaths = response.xpath( '/html/body/div[1]/div[2]/section[5]/div[1]/table/tbody/tr[1]/td[5]/text()' ).get()

        item["date"] = date.strftime("%Y-%m-%d")
        item["name"] =  self.names[0]
        item["positive"] = int( positive )
        item["negative"] = int( total ) - int( positive )
        item["deaths"] = int( deaths )

        print( item.toAsciiTable() )
        return item

