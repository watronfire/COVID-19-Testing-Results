import scrapy
import logging
from covid19.items import TestingStats
from dateutil.parser import parse
from datetime import datetime as dt

class CanadaNovaScotiaSpider( scrapy.Spider ) :

    name = "canadanovascotia"
    allowed_domains = ["https://novascotia.ca/"]
    obj = ["NovaScotia"]
    case_categories = ["positive", "pending", "negative"]
    names = ["Nova Scotia, CAN" ]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://novascotia.ca/coronavirus/", callback=self.parse )

    def parse( self, response ):
        item = TestingStats()
        confirmed = response.xpath( '/html/body/main/div/div[4]/div[1]/section[2]/table/tr[1]/td/text()' ).get()
        presumed_confirmed = response.xpath( '/html/body/main/div/div[4]/div[1]/section[2]/table/tr[2]/td/text()' ).get()

        negative = response.xpath( '/html/body/main/div/div[4]/div[1]/section[2]/table/tr[3]/td/text()' ).get()

        date = response.xpath( '/html/body/main/div/div[4]/div[1]/section[2]/p[1]/text()' ).get()

        date = parse( date, fuzzy=True )

        deaths = 0

        item["date"] = date.strftime( "%Y-%m-%d %H:%M %p" )
        item["name"] = self.names[0]
        item["positive"] = int( confirmed ) + int( presumed_confirmed )
        item["negative"] = negative
        item["deaths"] = deaths
        print( item.toAsciiTable() )
        return item