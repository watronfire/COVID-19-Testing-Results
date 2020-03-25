import scrapy
import logging
from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt
#from selenium import webdriver

class CanadaOntarioSpider( scrapy.Spider ):
    name = "canadaontario"
    allowed_domains = ["https://www.ontario.ca/"]
    obj = ["Ontario"]
    case_categories = ["negative", "pending", "positive"]
    names = ["Ontario, CAN"]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://www.ontario.ca/page/2019-novel-coronavirus", callback=self.parse )

    def parse( self, response ):
        item = TestingStats()
        item_dict = { "name" : self.names[0] }
        #print( response.xpath( '/html').get() )

        date = response.xpath( '/html/body/div[3]/div/main/div[4]/div/div[2]/p[4]/text()' ).get()
        #date = date.replace( ".", "" )
        #date = dt.strptime( date, "Last updated: %B %d, %Y at %I:%M %p ET")

        case_table = response.xpath( '/html/body/div[3]/div/main/div[4]/div/div[2]/table[1]/tbody' )
        for i, row in enumerate( case_table.xpath( 'tr' )[:-2] ) :
            value = row.xpath( "td[2]/text()" ).get()
            item_dict[self.case_categories[i]] = int( value )

        print( item_dict )
        item["date"] = "2020-03-23 05:30 pm"
        item["name"] = "Ontario, CAN"
        item["negative"] = 21795
        item["positive"] = 572
        item["deaths"] = 8
        item["pending"] = 10074

        print( item.toAsciiTable() )
        return item