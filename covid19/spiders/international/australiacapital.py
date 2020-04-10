import scrapy
import logging
from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt
from dateutil.parser import parse

class AustraliaSpider( scrapy.Spider ) :

    name = "australia"
    allowed_domains = ["https://www.covid19.act.gov.au/"]
    obj = ["AustraliaCapital"]
    case_categories = ["positive", "pending", "negative"]
    names = ["Australia Capital" ]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }


    def start_requests( self ):
        yield scrapy.Request( "https://www.covid19.act.gov.au/home", callback=self.parse )

    def parse( self, response ):
        item = TestingStats()
        positive = response.xpath( '/html/body/main/div[2]/div/div/div[1]/div/div[3]/div/div[1]/table/tr/td[2]/text()' ).get()
        positive = positive.strip()

        negative = response.xpath( '/html/body/main/div[2]/div/div/div[1]/div/div[3]/div/div[2]/table/tr/td[2]/text()' ).get()
        negative = negative.strip()
        negative = negative.replace( ",", "" )

        date = response.xpath( '/html/body/main/div[2]/div/div/div[1]/div/div[2]/p/text()' ).get()
        date = parse( date, fuzzy=True )

        #deaths = response.xpath( "/html/body/main/div[2]/div[2]/table[1]/tbody/tr/td[4]/text()" ).get()
        #exitdeaths = deaths.strip()

        item["date"] = date.strftime( "%Y-%m-%d" )
        item["name"] = self.names[0]
        item["positive"] = positive
        item["negative"] = negative
        print( item.toAsciiTable() )
        return item

#['aupyth',
# 'australiansw',
# 'canadaalberta',
# 'canadabritishcolumbia',
# 'canadanational',
# 'canadaontario',
# 'unitedkingdomnational',
# 'florida',
# 'illinois',
# 'newmexico',
# 'newyork',
# 'oregon',
# 'sandiego',
# 'snohomish',
# 'washington']
