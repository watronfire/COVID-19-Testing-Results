import scrapy
import logging
from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt
from dateutil.parser import parse
import re

class CanadaNTSpider( scrapy.Spider ) :

    name = "canadant"
    allowed_domains = ["https://www.hss.gov.nt.ca/en/services/coronavirus-disease-covid-19"]
    case_categories = ["positive", "pending", "negative"]
    names = ["Canada, Northern Territories" ]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://www.hss.gov.nt.ca/en/services/coronavirus-disease-covid-19", callback=self.parse )

    def parse( self, response ):
        item = TestingStats()

        confirmed = response.xpath( '/html/body/div[1]/div/div[5]/main/div/div[2]/div[2]/div/div/ul[1]/li[1]/b/text()' ).get()

        negative = response.xpath( '/html/body/div[1]/div/div[5]/main/div/div[2]/div[2]/div/div/ul[1]/li[3]/strong/text()' ).get()

        pending = response.xpath( '/html/body/div[1]/div/div[5]/main/div/div[2]/div[2]/div/div/ul[1]/li[4]/strong/text()' ).get()

        #deaths_paragraph = response.xpath( '/html/body/form/div[5]/div/span/div[1]/div/div/div[3]/article/div/div/div[2]/div[1]/div/ul/ul/li[2]/text()' ).get()
        #deaths = re.split( ' |\xa0', deaths_paragraph )[0]

        date = response.xpath( '/html/body/div[1]/div/div[5]/main/div/div[2]/div[2]/div/div/h2[1]/text()' ).get()
        date = parse( date, fuzzy=True )
        #date = dt.strptime( date, "\xa0%B %d,\xa0%Y.\xa0" )

        item["date"] = date.strftime( "%Y-%m-%d" )
        item["name"] = self.names[0]
        item["positive"] = confirmed
        item["negative"] = negative
        item["pending"] = pending
        item["deaths"] = 0
        print( item.toAsciiTable() )
        return item