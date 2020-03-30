import scrapy
import logging
from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt
from dateutil.parser import parse

class AustraliaSpider( scrapy.Spider ) :

    name = "australia"
    allowed_domains = ["https://health.act.gov.au"]
    obj = ["AustraliaCapital"]
    case_categories = ["positive", "pending", "negative"]
    names = ["Australia Capital" ]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }


    def start_requests( self ):
        yield scrapy.Request( "https://www.covid19.act.gov.au/updates/confirmed-case-information", callback=self.parse )

    def parse( self, response ):
        item = TestingStats()
        positive = response.xpath( '/html/body/main/div[2]/div[2]/table[1]/tbody/tr/td[1]/text()' ).get()
        positive = positive.strip()

        negative = response.xpath( '/html/body/main/div[2]/div[2]/table[1]/tbody/tr/td[2]/text()' ).get()
        negative = negative.strip()

        date = response.xpath( '/html/body/div[3]/text()[2]' ).get()
        date = parse( date, fuzzy=True )

        deaths = response.xpath( "/html/body/main/div[2]/div[2]/table[1]/tbody/tr/td[4]/text()" ).get()
        deaths = deaths.strip()

        item["date"] = date.strftime( "%Y-%m-%d" )
        item["name"] = self.names[0]
        item["positive"] = positive
        item["negative"] = negative
        item["deaths"] = deaths
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
