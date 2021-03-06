# -*- coding: utf-8 -*-
import re

import scrapy
from covid19.items import TestingStats
from datetime import datetime as dt
from dateutil.parser import parse
import logging

class CzechRebublicSpider(scrapy.Spider):
    name = 'czechrebublic'
    allowed_domains = ['https://onemocneni-aktualne.mzcr.cz']
    names = ["Czech Republic"]
    case_categories = ["positive", "negative"]
    custom_settings = {"LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://onemocneni-aktualne.mzcr.cz/covid-19", callback=self.parse )

    def parse(self, response):
        item = TestingStats()

        date = response.xpath( '/html/body/main/div/div[1]/div[1]/div[1]/div/p[3]/text()' ).get()
        date = "".join( re.split( ' |\xa0', date ) )
        date = parse( date, fuzzy=True )
        print( date )

        positive = response.xpath( '/html/body/main/div/div[1]/div[1]/div[2]/div/p[2]/text()' ).get()
        positive = "".join( re.split( ' |\xa0', positive ) )

        total = response.xpath( '/html/body/main/div/div[1]/div[1]/div[1]/div/p[2]/text()' ).get()
        total = total.replace( ' ', '' )

        deaths = response.xpath( '/html/body/main/div/div[1]/div[1]/div[6]/div/p[2]/text()' ).get()

        item["date"] = date.strftime("%Y-%m-%d")
        item["name"] =  self.names[0]
        item["positive"] = positive
        item["negative"] = int( total ) - int( positive )
        item["deaths"] = deaths

        print( item.toAsciiTable() )
        return item

        # have an open dataset at https://onemocneni-aktualne.mzcr.cz/api/v1/covid-19