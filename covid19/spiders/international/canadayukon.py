import scrapy
import logging
from covid19.items import TestingStats
from dateutil.parser import parse
from datetime import datetime as dt

class CanadaYukonSpider( scrapy.Spider ) :

    name = "canadayukon"
    allowed_domains = ["https://yukon.ca/covid-19"]
    case_categories = ["positive", "pending", "negative"]
    names = ["Canada, Yukon" ]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( 'https://yukon.ca/covid-19', callback=self.parse )

    def parse( self, response ):
        item = TestingStats()

        confirmed = response.xpath( '/html/body/div[3]/div/main/div[1]/section/article/div[1]/div/div/table/tbody/tr[2]/td[2]/text()' ).get()

        negative = response.xpath( '/html/body/div[3]/div/main/div[1]/section/article/div[1]/div/div/table/tbody/tr[4]/td[2]/text()' ).get()

        pending = response.xpath( '/html/body/div[3]/div/main/div[1]/section/article/div[1]/div/div/table/tbody/tr[5]/td[2]/text()' ).get()

        date = response.xpath( '/html/body/div[3]/div/main/div[1]/section/article/div[1]/div/div/h3/text()' ).get()
        date = date.split( ": " )[-1]
        #date = dt.strptime( date, "%B %d, %Y – %I:%M" )
        date = parse( date, fuzzy=True )

        deaths = 0

        item["date"] = date.strftime( "%Y-%m-%d" )
        item["name"] = self.names[0]
        item["positive"] = confirmed
        item["negative"] = negative
        item["pending"] = pending
        item["deaths"] = deaths
        print( item.toAsciiTable() )
        return item