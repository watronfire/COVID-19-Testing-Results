import scrapy
import logging

from scrapy.crawler import CrawlerProcess

from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt
from dateutil.parser import parse

class CanadaNewBrunswickSpider( scrapy.Spider ):
    name = "canadanb"
    allowed_domains = ["https://www2.gnb.ca/"]
    obj = ["CanadaNewBrunswick"]
    case_categories = ["negative", "positive", "deaths" ]
    names = ["New Brunswick, Canada"]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://www2.gnb.ca/content/gnb/en/departments/ocmoh/cdc/content/respiratory_diseases/coronavirus.html#", callback=self.parse )

    def parse( self, response ) :
        item = TestingStats()

        item_dict = { "name" : self.names[0] }

        date = response.xpath( '/html/body/div[1]/div[4]/div[5]/div[1]/div/div/div[2]/div[5]/div[1]/div[2]/span/a/text()' ).get()
        date = parse( date, fuzzy=True )

        positive = response.xpath( '/html/body/div[1]/div[4]/div[5]/div[1]/div/div/div[2]/div[8]/div/div[2]/div/div[2]/div/div[2]/div/div/div/p/b/text()' ).get()
        #presumed = response.xpath( '/html/body/div[1]/div[4]/div[5]/div[1]/div/div/div[2]/div[8]/div/div[2]/div/div[2]/div/div[2]/div/div/div/p/b/text()' ).get()

        #positive = int( positive ) + int( presumed )

        negative = response.xpath( '/html/body/div[1]/div[4]/div[5]/div[1]/div/div/div[2]/div[8]/div/div[2]/div/div[1]/div/div[2]/div/div/div/p/b/text()' ).get()
        negative = negative.replace( ",", "" )

        #deaths = response.xpath( '/html/body/main/div[2]/div/section/div/div[1]/div[4]/ul/li[3]/text()' ).get()
        deaths = 0

        item["date"] = date.strftime( "%Y-%m-%d" )
        item["name"] = self.names[0]
        item["positive"] = positive
        item["negative"] = negative
        item["deaths"] = deaths

        print( item.toAsciiTable() )
        print( "REMEMBER TO UPDATES DEATHS" )
        return item