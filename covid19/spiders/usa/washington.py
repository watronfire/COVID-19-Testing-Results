import scrapy
from scrapy.crawler import CrawlerProcess

from covid19.items import TestingStats
from datetime import datetime as dt
import logging
import requests
import json

class WashingtonSpider( scrapy.Spider ):
    name = "washington"
    allowed_domains = ['http://www.doh.wa.gov/']
    names = ["Washington State"]
    case_categories = ["positive", "negative"]
    custom_settings = {"LOG_LEVEL" : logging.ERROR }

    def start_requests(self):
        yield scrapy.Request( "http://www.doh.wa.gov/Emergencies/Coronavirus", callback=self.parse )

    def parse( self, response ):
        item = TestingStats()

        item_dict = { "name" : self.names[0] }

        date = response.xpath( '/html/body/form/div[3]/div/div/div[3]/section/main/div[4]/div/div/div[7]/div[1]/div/div[1]/div/div[2]/div/div/div/div[6]/p[4]/em/text()' ).get()
        date = date.split( ": " )[1]
        date = date.replace( ".", "" )
        date = date.upper()
        date = dt.strptime( date, "%B %d, %Y at %I:%M %p" )

        case_table = response.xpath( '/html/body/form/div[3]/div/div/div[3]/section/main/div[4]/div/div/div[7]/div[1]/div/div/div/div[2]/div/div/div/div[6]/table[4]/tbody' )
        for i, row in enumerate( case_table.xpath( 'tr' ) ):

            value = row.xpath( 'td[2]/text()' ).get()
            #print( "{},{}".format( row.xpath( 'td[1]/text()' ).get(), value ) )
            item_dict[self.case_categories[i]] = int( value )

        # Snohomish County seperates presumed positive cases from probably cases based on source of the initial positive
        # test. Presumed positive cases have a positive test from a state lab, and probable cases have a positive test
        # from UW. Confirmed are only those which have been confirmed by CDC.

        item["date"] = date.strftime( "%Y-%m-%d %I:%M %p" )
        for i in item_dict.keys():
            item[i] = item_dict[i]

        print( item.toAsciiTable() )
        return item