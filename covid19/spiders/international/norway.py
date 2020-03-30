# -*- coding: utf-8 -*-
import scrapy
from covid19.items import TestingStats
from datetime import datetime as dt
from dateutil.parser import parse
import logging

class NorwaySpider(scrapy.Spider):
    name = 'norway'
    allowed_domains = ['https://www.fhi.no/']
    names = ["Norway"]
    case_categories = ["positive", "negative"]
    custom_settings = {"LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( 'https://www.fhi.no/sv/smittsomme-sykdommer/corona/', callback=self.parse )

    def parse(self, response):
        item = TestingStats()

        date = response.xpath( '/html/body/main/article/div[2]/div/div/div[3]/div[2]/div[2]/a/div/div/div[2]/div[2]/text()' ).get()
        date += " 2020"
        date = date.replace( "mars", "march" )
        date = parse( date, fuzzy=True )

        item["date"] = date.strftime( "%Y-%m-%d" )
        item["name"] = self.names[0]

        total =  response.xpath( "/html/body/main/article/div[2]/div/div/div[3]/div[2]/div[1]/a/div/div/div[2]/div[1]/span/text()" ).get()
        positive = response.xpath( '/html/body/main/article/div[2]/div/div/div[3]/div[2]/div[2]/a/div/div/div[2]/div[1]/span/text()' ).get()

        item["positive"] = positive
        item["negative"] = int( total ) - int( positive )

        print( item.toAsciiTable() )
        return item

