import scrapy
import logging

from scrapy.crawler import CrawlerProcess

from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt
from dateutil.parser import parse

class CanadaQuebecSpider( scrapy.Spider ):
    name = "canadaquebec"
    allowed_domains = ["https://www.msss.gouv.qc.ca/professionnels/maladies-infectieuses/coronavirus-2019-ncov/"]
    obj = ["CanadaQuebec"]
    case_categories = ["negative", "positive", "deaths" ]
    names = ["Quebec, Canada"]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://www.msss.gouv.qc.ca/professionnels/maladies-infectieuses/coronavirus-2019-ncov/", callback=self.parse )

    def parse( self, response ) :
        item = TestingStats()

        item_dict = { "name" : self.names[0] }

        date = response.xpath( '/html/body/main/div[2]/div/section/div/div[1]/div[4]/p[1]/text()' ).get()
        date = date.replace( "mars", "March" )
        date = parse( date, fuzzy=True )

        positive = response.xpath( '/html/body/main/div[2]/div/section/div/div[1]/div[4]/ul/li[1]/text()' ).get()
        positive = "".join( positive.split( "\xa0" )[:2] )

        negative = response.xpath( '/html/body/main/div[2]/div/section/div/div[1]/div[4]/ul/li[5]/text()' ).get()
        negative = "".join( negative.split( "\xa0" )[:2] )

        deaths = response.xpath( '/html/body/main/div[2]/div/section/div/div[1]/div[4]/ul/li[2]/text()' ).get()
        deaths = deaths.split( "\xa0" )[0]

        item["date"] = date.strftime( "%Y-%m-%d %H:%M %p" )
        item["name"] = self.names[0]
        item["positive"] = positive
        item["negative"] = negative
        item["deaths"] = deaths

        print( item.toAsciiTable() )
        return item