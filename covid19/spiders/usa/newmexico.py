import scrapy
import logging
from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt
from dateutil.parser import parse

class NewMexicoSpider( scrapy.Spider ) :

    name = "newmexico"
    allowed_domains = ["https://cv.nmhealth.org/"]
    obj = ["NewMexico"]
    case_categories = ["positive", "negative", "Pending"]
    names = ["New Mexico" ]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }


    def start_requests( self ):
        yield scrapy.Request( "https://cv.nmhealth.org/", callback=self.parse )

    def parse( self, response ):
        item = TestingStats()
        positive = response.xpath( "/html/body/div/div[2]/div/article/div/div/div/div/div[2]/div/div[2]/div[2]/div/table/tbody/tr[1]/td[2]/text()" ).get()
        negative = response.xpath( "/html/body/div/div[2]/div/article/div/div/div/div/div[2]/div/div[2]/div[2]/div/table/tbody/tr[2]/td[2]/text()" ).get()
        total = response.xpath( "/html/body/div/div[2]/div/article/div/div/div/div/div[2]/div/div[2]/div[2]/div/table/tbody/tr[3]/td[2]/text()" ).get()
        positive = positive.replace( ",", "" )
        negative = negative.replace(",", "")
        total = total.replace(",", "")
        positive = positive
        negative = negative
        total = total

        date = response.xpath( '/html/body/div/div[2]/div/article/div/div/div/div/div[2]/div/div[2]/div[2]/div/p[3]/em/text()' ).get()
        date = parse( date, fuzzy=True )

        item["date"] = date.strftime( "%Y-%m-%d %H:%M %p" )
        item["name"] = self.names[0]
        item["positive"] = positive
        item["negative"] = negative
        item["pending"] = int( total ) - ( int( positive ) + int( negative ) )

        print( item.toAsciiTable() )
        return item