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
    names = ["Canada, Alberta"]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://www.alberta.ca/covid-19-alberta-data.aspx", callback=self.parse )

    def parse( self, response ) :
        item = TestingStats()

        confirmed = response.xpath( '/html/body/main/div/div/div/table/tbody/tr[2]/td[1]/text()' ).get()
        confirmed = confirmed.replace( ",", "" )

        deaths= response.xpath( '/html/body/main/div/div/div/table/tbody/tr[2]/td[2]/text()' ).get()

        totals = response.xpath( '/html/body/main/div/div/div/table/tbody/tr[2]/td[4]/text()' ).get()
        totals = totals.replace( ",", '' )

        date = response.xpath( '/html/body/main/div/div/div/table/caption/em/text()' ).get()
        date = parse( date, fuzzy=True )

        item["name"] = self.names[0]
        item['date'] = date.strftime( "%Y-%m-%d" )
        item["positive"] = confirmed
        item["negative"] = int( totals ) - int( confirmed )
        item["deaths"] = deaths

        print( item.toAsciiTable() )
        return item