# -*- coding: utf-8 -*-
import scrapy
from covid19.items import TestingStats
from datetime import datetime as dt
from dateutil.parser import parse
import logging

class VietnamSpider(scrapy.Spider):
    name = 'vietnam'
    allowed_domains = ['https://ncov.moh.gov.vn/']
    names = ["Vietnam"]
    case_categories = ["positive", "negative", "pending", "pui"]
    custom_settings = {"LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://ncov.moh.gov.vn/", callback=self.parse )

    def parse(self, response):
        item = TestingStats()

        date = response.xpath( '/html/body/div[1]/div/div/div/div/div[1]/div/div/section/div[2]/div[1]/div[1]/div[2]/p/small/strong/text()' ).get()
        date = parse( date )

        positive = response.xpath( '//*[@id="p_p_id_56_"]/div/div/div/div[3]/div[6]/strong/span[2]/span/text()' ).get()

        negative = response.xpath( '//*[@id="p_p_id_56_"]/div/div/div/div[3]/div[7]/strong/span[2]/span/text()' ).get()
        negative = negative.replace( ".", "" )

        deaths = response.xpath( '//*[@id="p_p_id_56_"]/div/div/div/div[1]/div/h4/strong/span/span/text()' ).get()

        item["date"] = date.strftime("%Y-%m-%d %H:%M %p")
        item["name"] =  self.names[0]
        item["positive"] = int( positive )
        item["negative"] = int( negative )
        item["deaths"] = int( deaths )

        print( item.toAsciiTable() )
        return item

