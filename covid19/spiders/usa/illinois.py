import scrapy
import logging
from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt

class IllinoisSpider( scrapy.Spider ) :

    name = "illinois"
    allowed_domains = ["http://www.dph.illinois.gov/"]
    obj = ["Illinois"]
    case_categories = ["positive", "presumedPositive", "negative", "pending", "pui" ]
    names = ["Illinois" ]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }


    def start_requests( self ):
        yield scrapy.Request( "http://www.dph.illinois.gov/topics-services/diseases-and-conditions/diseases-a-z-list/coronavirus", callback=self.parse )

    def parse( self, response ):
        item = TestingStats()
        item_dict = { "name" : self.names[0] }

        results = response.xpath( '/html/body/div[1]/div[3]/div/article/div/div/div/dl/dd[1]/table/tbody' )

        for i, row in enumerate( results.xpath( "tr" ) ):
            value = row.xpath( "td/text()" ).get()
            print( "{},{}".format( value, self.case_categories[i] ) )
            item_dict[self.case_categories[i]] = int( value )

        date = response.xpath( '/html/body/div[1]/div[3]/div/article/div/div/div/dl/dd[1]/p[1]/text()[1]' ).get()
        date = date.split( " " )[-3:]
        date = " ".join( date )
        date = dt.strptime( date, "%B %d, %Y." )

        item["date"] = date.strftime( "%Y-%m-%d %H:%M %p" )
        item["Local"] = item_dict

        print( item.toAsciiTable() )
        return item