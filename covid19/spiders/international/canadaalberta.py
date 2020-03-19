import scrapy
import logging

from scrapy.crawler import CrawlerProcess

from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt

class CanadaNationalSpider( scrapy.Spider ):
    name = "canadaalberta"
    allowed_domains = ["https://www.alberta.ca/"]
    obj = ["CanadaAlberta"]
    case_categories = ["negative", "positive", "deaths" ]
    names = ["Alberta, CAN"]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://www.alberta.ca/coronavirus-info-for-albertans.aspx", callback=self.parse )

    def parse( self, response ) :
        item = TestingStats()

        item_dict = { "name" : self.names[0] }

        data_table = response.xpath( '/html/body/main/div[1]/div[1]/div[4]/table/tbody/tr' )

        date = data_table.xpath( "th/text()" ).get()
        print( date )
        date += " 2020"
        date = dt.strptime( date, 'Completed tests (as of %B %d) %Y')

        for i, row in enumerate( data_table.xpath( 'td' ) ):
            _ = row.xpath( "text()" ).get()
            item_dict[self.case_categories[i]] = int( _.replace( ",", "" ) )

        item["date"] = date.strftime( "%Y-%m-%d %H:%M %p" )

        deaths = response.xpath( "/html/body/main/div[1]/div[1]/div[3]/table/tbody/tr[2]/td[2]/text()" ).get()
        item_dict["deaths"] = deaths

        for i in item_dict.keys():
            item[i] = item_dict[i]

        print( item.toAsciiTable() )
        return item