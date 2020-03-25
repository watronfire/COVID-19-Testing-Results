# -*- coding: utf-8 -*-
import scrapy
from covid19.items import TestingStats
from datetime import datetime as dt
from dateutil.parser import parse
import logging

class BahrainSpider(scrapy.Spider):
    name = 'bahrain'
    allowed_domains = ['https://www.moh.gov.bh']
    names = ["Bahrain"]
    case_categories = ["positive", "negative", "deaths"]
    custom_settings = {"LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( 'https://www.moh.gov.bh/COVID19', callback=self.parse )

    def parse(self, response):
        item = TestingStats()

        #date = response.xpath( '/html/body/div[1]/div/div[2]/div/div[2]/div/div[3]/div[2]/div/div/span/text()' ).get()
        #print( date )
        #date = parse( date, fuzzy=True )
        date = dt.today()

        positive = response.xpath( '/html/body/div[1]/div/div[2]/div/div[2]/div/div[3]/div[2]/div/div/table/thead/tr[2]/td/span/text()' ).get()

        total = response.xpath( '/html/body/div[1]/div/div[2]/div/div[2]/div/div[3]/div[2]/div/div/table/thead/tr[1]/th/span/text()' ).get()
        total = total.replace( " ", "" )

        deaths = response.xpath( '/html/body/div[1]/div/div[2]/div/div[2]/div/div[3]/div[2]/div/div/table/thead/tr[6]/td/span/text()' ).get()

        item["date"] = date.strftime("%Y-%m-%d %H:%M %p")
        item["name"] =  self.names[0]
        item["positive"] = int( positive )
        item["negative"] = int( total ) - int( positive )
        item["deaths"] = int( deaths )

        print( item.toAsciiTable() )
        return item

