# -*- coding: utf-8 -*-
import scrapy
from covid19.items import TestingStats
from datetime import datetime as dt
from dateutil.parser import parse
import logging

class EcuadorSpider(scrapy.Spider):
    name = 'ecuador'
    allowed_domains = ['https://www.salud.gob.ec/']
    names = ["Ecuador"]
    case_categories = ["positive", "negative"]
    custom_settings = {"LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://www.salud.gob.ec/actualizacion-de-casos-de-coronavirus-en-ecuador/", callback=self.parse )

    def parse(self, response):
        item = TestingStats()

        #date = response.xpath( '/html/body/div[3]/div/div/div/div[2]/main/p/strong[1]/text()' ).get()
        #date = dt.strptime( date, 'Stand in Österreich, %d.%m.%Y, %H:%M Uhr' )
        date = dt.now()

        total = response.xpath( '/html/body/div[2]/div/div/div[2]/section/table/tbody/tr[1]/td[2]/strong[1]/text()' ).get()

        positive = response.xpath( '/html/body/div[2]/div/div/div[2]/section/table/tbody/tr[2]/td[2]/strong/text()' ).get()

        deaths = response.xpath( '/html/body/div[2]/div/div/div[2]/section/table/tbody/tr[2]/td[2]/ul/li[5]/strong/text()' ).get()

        pending = response.xpath( '/html/body/div[2]/div/div/div[2]/section/table/tbody/tr[3]/td[2]/strong/text()' ).get()
        pending = pending.split( " " )[0]

        negative = response.xpath( '/html/body/div[2]/div/div/div[2]/section/table/tbody/tr[3]/td[2]/p[1]/strong/text()' ).get()
        negative = negative.split( " " )[0]

        item["date"] = date.strftime("%Y-%m-%d")
        item["name"] =  self.names[0]
        item["positive"] = int( positive )
        item["pending"] = pending
        item["negative"] = negative
        item["deaths"] = int( deaths )

        print( item.toAsciiTable() )
        return item

