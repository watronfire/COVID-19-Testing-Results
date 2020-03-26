import scrapy
import logging

from scrapy.crawler import CrawlerProcess

from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt
from dateutil.parser import parse

class CanadaAlbertaSpider( scrapy.Spider ):
    name = "canadaalberta"
    allowed_domains = ["https://www.alberta.ca/"]
    obj = ["CanadaAlberta"]
    case_categories = ["negative", "positive", "deaths" ]
    names = ["Alberta, CAN"]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://www.alberta.ca/covid-19-alberta-data.aspx", callback=self.parse )

    def parse( self, response ) :
        item = TestingStats()

        #table = response.xpath( '/html/body/main/div/div/div[2]/table/tbody/tr' )

        #print( response.xpath( 'html' ).get() )

        #date = table.xpath( "th/text()" ).get()
        #date = parse( date, fuzzy=True )

        #negative = table.xpath( "td[1]/text()" ).get()
        #negative = negative.replace( ",", "" )

        #positive = table.xpath( 'td[2]/text()' ).get()
        #positive = positive.replace( ",", "" )

        #item["date"] = date.strftime( "%Y-%m-%d %H:%M %p" )

        #deaths = response.xpath( '/html/body/main/div/div/div[1]/table/tbody/tr[2]/td[2]/text()' ).get()

        item["name"] = self.names[0]
        item['date'] = dt.now().strftime( "%Y-%m-%d %H:%M %p" )
        item["positive"] = 419
        item["negative"] = 35089
        item["deaths"] = 2

        print( item.toAsciiTable() )
        return item