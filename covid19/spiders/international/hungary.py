# -*- coding: utf-8 -*-
import scrapy
from covid19.items import TestingStats
from datetime import datetime as dt
from dateutil.parser import parse
import logging

class HungarySpider(scrapy.Spider):
    name = 'hungary'
    allowed_domains = ['https://koronavirus.gov.hu/']
    names = ["Hungary"]
    case_categories = ["positive", "negative"]
    custom_settings = {"LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( 'https://koronavirus.gov.hu/', callback=self.parse )

    def parse(self, response):
        item = TestingStats()

        date = response.xpath( '/html/body/div[1]/div/section/div/section[2]/div/div[1]/div[2]/div[1]/div[1]/section/div/p/text()' ).get()
        date = parse( date, fuzzy=True )

        positive = response.xpath( '/html/body/div[1]/div/section/div/section[2]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div/span/div/span[1]/text()' ).get()

        total = response.xpath( '/html/body/div[1]/div/section/div/section[2]/div/div[1]/div[2]/div[1]/div[2]/div[5]/div/span/div/span[1]/text()' ).get()
        total = total.replace( " ", "" )

        deaths = response.xpath( '/html/body/div[1]/div/section/div/section[2]/div/div[1]/div[2]/div[1]/div[2]/div[3]/div/span/div/span[1]/text()' ).get()

        item["date"] = date.strftime("%Y-%m-%d")
        item["name"] =  self.names[0]
        item["positive"] = int( positive )
        item["negative"] = int( total ) - int( positive )
        #item["deaths"] = int( deaths )
        item["deaths"] = 16

        print( item.toAsciiTable() )
        return item

