import scrapy
import logging

from scrapy.crawler import CrawlerProcess

from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt
import re
from dateutil.parser import parse

class CanadaQuebecSpider( scrapy.Spider ):
    name = "canadaquebec"
    allowed_domains = ["https://www.quebec.ca"]
    obj = ["CanadaQuebec"]
    case_categories = ["negative", "positive", "deaths" ]
    names = ["Canada, Quebec"]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/", callback=self.parse )

    def parse( self, response ) :
        item = TestingStats()

        item_dict = { "name" : self.names[0] }

        date = response.xpath( '/html/body/div[2]/div[3]/div/div/div/div[3]/div/div/div/p/text()' ).get()
        date = date.replace( "avril", "April" )
        date = parse( date, fuzzy=True )

        positive = "".join( i.get() for i in response.xpath( '/html/body/div[2]/div[3]/div/div/div/div[4]/div[1]/div/div/div/p[2]/text()' ) )
        positive = "".join( re.split( ' |\xa0', positive )[:2] )

        negative = response.xpath( '/html/body/div[2]/div[3]/div/div/div/div[4]/div[2]/div/div/div/p[2]/text()' ).get()
        negative = "".join( re.split( ' |\xa0', negative )[:2] )

        deaths = response.xpath( '/html/body/div[2]/div[3]/div/div/div/div[4]/div[4]/div/div/div/p[2]/text()' ).get()
        deaths = re.split( ' |\xa0', deaths )[0]

        item["date"] = date.strftime( "%Y-%m-%d" )
        item["name"] = self.names[0]
        item["positive"] = positive
        item["negative"] = negative
        item["deaths"] = deaths

        print( item.toAsciiTable() )
        return item