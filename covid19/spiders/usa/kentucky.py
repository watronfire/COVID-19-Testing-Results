import scrapy
import logging
from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt
from dateutil.parser import parse

class KentuckySpider( scrapy.Spider ) :

    name = "kentucky"
    allowed_domains = ["https://chfs.ky.gov"]
    obj = ["Kentucky"]
    case_categories = ["positive", "negative"]
    names = ["Kentucky" ]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }


    def start_requests( self ):
        yield scrapy.Request( "https://chfs.ky.gov/agencies/dph/pages/covid19.aspx", callback=self.parse )

    def parse( self, response ):
        item = TestingStats()
        total = response.xpath( "/html/body/div[1]/div[2]/div[2]/p/text()[2]" ).get()
        positive = response.xpath( "/html/body/div[1]/div[2]/div[2]/p/text()[3]" ).get()

        positive = positive.split( ": " )[-1]
        total = total.split( ": " )[-1]

        date = response.xpath( '/html/body/div[1]/div[2]/div[2]/p/b[1]/text()' ).get()
        date = parse( date, fuzzy=True )

        item["date"] = date.strftime( "%Y-%m-%d %H:%M %p" )
        item["name"] = self.names[0]
        item["positive"] = positive
        item["negative"] = int( total ) - int( positive )
        item["deaths"] = 0

        print( item.toAsciiTable() )
        return item