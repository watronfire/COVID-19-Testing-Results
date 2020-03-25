import scrapy
import logging
from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt
from dateutil.parser import parse

class IllinoisSpider( scrapy.Spider ) :

    name = "illinois"
    allowed_domains = ["http://www.dph.illinois.gov/"]
    obj = ["Illinois"]
    case_categories = ["positive", "negative" ]
    names = ["Illinois" ]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }


    def start_requests( self ):
        yield scrapy.Request( "http://www.dph.illinois.gov/topics-services/diseases-and-conditions/diseases-a-z-list/coronavirus", callback=self.parse )

    def parse( self, response ):
        item = TestingStats()

        positive = response.xpath( "/html/body/div[1]/div[3]/div/article/div/div/div/dl/dd[1]/div[1]/div[1]/h3/text()" ).get()
        deaths = response.xpath( '/html/body/div[1]/div[3]/div/article/div/div/div/dl/dd[1]/div[1]/div[3]/h3/text()' ).get()
        total = response.xpath( '/html/body/div[1]/div[3]/div/article/div/div/div/dl/dd[1]/div[1]/div[4]/h3/text()' ).get()

        date = response.xpath( '/html/body/div[1]/div[3]/div/article/div/div/div/dl/dd[1]/p[1]/text()[1]' ).get()
        date = parse( date, fuzzy=True )

        item["date"] = date.strftime( "%Y-%m-%d %H:%M %p" )
        item["positive"] = positive
        item["deaths"] = deaths
        item["negative"] = int( total ) - int( positive )
        item["name"] = self.names[0]

        print( item.toAsciiTable() )
        return item