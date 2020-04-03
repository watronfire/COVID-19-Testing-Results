# -*- coding: utf-8 -*-
import scrapy
from covid19.items import TestingStats
from datetime import datetime as dt
from dateutil.parser import parse
import logging

class AustriaSpider(scrapy.Spider):
    name = 'austria'
    allowed_domains = ['https://www.sozialministerium.at/']
    names = ["Austria"]
    case_categories = ["positive", "negative"]
    custom_settings = {"LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html", callback=self.parse )

    def parse(self, response):
        item = TestingStats()

        #date = response.xpath( '/html/body/div[3]/div/div/div/div[2]/main/p/strong[1]/text()' ).get()
        #date = dt.strptime( date, 'Stand in Österreich, %d.%m.%Y, %H:%M Uhr' )
        date = dt.now()

        positive = response.xpath( '/html/body/div[3]/div/div/div/div[2]/main/p[3]/text()' ).get()
        positive = positive.split( " F" )[0]
        positive = positive.replace( ".", "" )
        positive = positive.replace( "\xa0", "" )
        positive = positive.replace( ":", "" )

        total = response.xpath( '/html/body/div[3]/div/div/div/div[2]/main/p[2]/text()' ).get()
        total = total.replace( ".", "" )
        total = total.split( " (" )[0]

        deaths = response.xpath( '/html/body/div[3]/div/div/div/div[2]/main/p[4]/text()[2]' ).get()
        deaths = deaths.split( "," )[0]

        item["date"] = date.strftime("%Y-%m-%d")
        item["name"] =  self.names[0]
        item["positive"] = int( positive )
        item["negative"] = int( total ) - int( positive )
        item["deaths"] = int( deaths )

        print( item.toAsciiTable() )
        return item

