# -*- coding: utf-8 -*-
import scrapy
from covid19.items import TestingStats
from datetime import datetime as dt
from dateutil.parser import parse
import logging

class NewZealandSpider(scrapy.Spider):
    name = 'newzealand'
    allowed_domains = ['https://www.health.govt.nz/']
    names = ["New Zealand"]
    case_categories = ["positive", "negative" ]
    custom_settings = {"LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus/covid-19-current-situation/covid-19-current-cases", callback=self.parse )

    def parse(self, response):
        item = TestingStats()

        date = response.xpath( '/html/body/div[2]/div/div[1]/section/div[2]/section/div/div/div[2]/div[2]/div/article/div[2]/div/div/p[1]/text()' ).get()
        date = date.replace( "\xa0", " " )
        date = parse( date, fuzzy=True )

        positive = response.xpath( '/html/body/div[2]/div/div[1]/section/div[2]/section/div/div/div[2]/div[2]/div/article/div[2]/div/div/table[1]/tbody/tr[3]/td[2]/strong/text()' ).get()

        total = response.xpath( '//*[@id="node-10813"]/div[2]/div/div/table[5]/tbody/tr[3]/td[2]/text()' ).get()
        total = total.replace( ",", "" )

        deaths = response.xpath( '/html/body/div[2]/div/div[1]/section/div[2]/section/div/div/div[2]/div[2]/div/article/div[2]/div/div/table[1]/tbody/tr[6]/td[2]/text()' ).get()

        item["date"] = date.strftime("%Y-%m-%d")
        item["name"] =  self.names[0]
        item["positive"] = int( positive )
        item["negative"] = int( total ) - int( positive )
        item["deaths"] = int( deaths )

        print( item.toAsciiTable() )
        return item

