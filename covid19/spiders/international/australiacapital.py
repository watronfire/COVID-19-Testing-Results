import scrapy
import logging
from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt

class AustraliaSpider( scrapy.Spider ) :

    name = "australiacaptital"
    allowed_domains = ["https://health.act.gov.au"]
    obj = ["AustraliaCapital"]
    case_categories = ["positive", "pending", "negative"]
    names = ["Australia Capital" ]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }


    def start_requests( self ):
        yield scrapy.Request( "https://health.act.gov.au/public-health-alert/updated-information-about-covid-19", callback=self.parse )

    def parse( self, response ):
        item = TestingStats()
        positive = response.xpath( '/html/body/div[1]/div/main/div[2]/div/div/div/div[1]/article/div/div[1]/div[1]/ul/li[1]/span/text()' ).get()
        negative = response.xpath( '/html/body/div[1]/div/main/div[2]/div/div/div/div[1]/article/div/div[1]/div[1]/ul/li[2]/span/b/text()' ).get()

        date = response.xpath( '/html/body/div[1]/div/main/div[2]/div/div/div/div[1]/article/div/div[1]/div[1]/p/strong/text()' ).get()
        date = dt.strptime( date, "%d\xa0%B %Y, current as at %I.%M%p AEDT" )


        item["date"] = date.strftime( "%Y-%m-%d %H:%M %p" )
        item["Local"] = { "name" : self.names[0],
                          "positive" : positive,
                          "negative" : negative }
        print( item.toAsciiTable() )
        return item