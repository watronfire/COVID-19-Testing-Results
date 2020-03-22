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

        date = response.xpath( '/html/body/div[3]/div/div/div/div[2]/main/p/strong[1]/text()' ).get()
        date = dt.strptime( date, 'Stand, %d.%m.%Y, %H:%M Uhr' )

        positive = response.xpath( '/html/body/div[3]/div/div/div/div[2]/main/p/strong[4]/text()' ).get()
        positive = positive.replace( ".", "" )

        total = response.xpath( '/html/body/div[3]/div/div/div/div[2]/main/p/strong[2]/text()' ).get()
        total = total.replace( ".", "" )

        deaths = response.xpath( '/html/body/div[3]/div/div/div/div[2]/main/p/strong[5]/text()[2]' ).get()
        deaths = deaths.split( ": " )[-1]

        item["date"] = date.strftime("%Y-%m-%d %H:%M %p")
        item["name"] =  self.names[0]
        item["positive"] = int( positive )
        item["negative"] = int( total ) - int( positive )
        item["deaths"] = int( deaths )

        print( item.toAsciiTable() )
        return item

