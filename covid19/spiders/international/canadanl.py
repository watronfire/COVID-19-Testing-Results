import scrapy
import logging
from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt
from dateutil.parser import parse
import re

class CanadaNLSpider( scrapy.Spider ) :

    name = "canadanl"
    allowed_domains = ["https://www.gov.nl.ca/covid-19/pandemic-update/"]
    case_categories = ["positive", "pending", "negative"]
    names = ["Canada, NL" ]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://www.gov.nl.ca/covid-19/pandemic-update/", callback=self.parse )

    def parse( self, response ):
        item = TestingStats()

        confirmed_paragraph = response.xpath( '/html/body/div/div/div/main/article/div/p[2]/text()' ).get()
        confirmed_paragraph = [i for i in confirmed_paragraph.split( " " ) if i.isnumeric()]
        confirmed =confirmed_paragraph[0]

        totals_paragraph = response.xpath( '/html/body/div/div/div/main/article/div/p[3]/text()' ).get()
        totals_paragraph = totals_paragraph.replace( ",", "" )
        totals_paragraph = [i for i in totals_paragraph.split( " " ) if i.isnumeric()]
        total = totals_paragraph[0]

        negatives = totals_paragraph[1]

        date = response.xpath( '/html/body/div/div/div/main/article/div/p[1]/text()' ).get()
        date = parse( date, fuzzy=True )
        #date = dt.strptime( date, "\xa0%B %d,\xa0%Y.\xa0" )

        item["date"] = date.strftime( "%Y-%m-%d" )
        item["name"] = self.names[0]
        item["positive"] = confirmed
        item["negative"] = negatives
        item["pending"] = int( total ) - ( int( confirmed) + int( negatives ) )
        item["deaths"] = 1
        print( item.toAsciiTable() )
        return item