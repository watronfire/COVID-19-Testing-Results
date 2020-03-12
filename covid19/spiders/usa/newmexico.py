import scrapy
import logging
from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt

class NewMexicoSpider( scrapy.Spider ) :

    name = "newmexico"
    allowed_domains = ["https://cv.nmhealth.org/"]
    obj = ["NewMexico"]
    case_categories = ["positive", "negative", "Pending"]
    names = ["New Mexico" ]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }


    def start_requests( self ):
        yield scrapy.Request( "https://cv.nmhealth.org/", callback=self.parse )

    def parse( self, response ):
        item = TestingStats()
        presumedPositive = response.xpath( "/html/body/div/div[2]/div/article/div/div/div/div/div[1]/div/div[2]/div[2]/div/table/tbody/tr[1]/td[2]/text()" ).get()
        positive = response.xpath( "/html/body/div/div[2]/div/article/div/div/div/div/div[1]/div/div[2]/div[2]/div/table/tbody/tr[2]/td[2]/text()" ).get()
        negative = response.xpath( "/html/body/div/div[2]/div/article/div/div/div/div/div[1]/div/div[2]/div[2]/div/table/tbody/tr[3]/td[2]/text()" ).get()
        total = response.xpath( "/html/body/div/div[2]/div/article/div/div/div/div/div[1]/div/div[2]/div[2]/div/table/tbody/tr[4]/td[2]/text()" ).get()
        presumedPositive = int( presumedPositive )
        positive = int( positive )
        negative = int( negative )
        total = int( total )

        date = response.xpath( '/html/body/div/div[2]/div/article/div/div/div/div/div[1]/div/div[2]/div[2]/div/p[2]/em/text()' ).get()
        date = date.split( " " )[5:8]
        date = " ".join( date )
        date = dt.strptime( date, "%B %d, %Y" )

        item["date"] = date.strftime( "%Y-%m-%d %H:%M %p" )
        item["Local"] = { "name" : self.names[0],
                          "presumedPositive" : presumedPositive,
                          "positive" : positive,
                          "negative" : negative,
                          "pending" : total - ( positive + negative + presumedPositive )}
        print( item.toAsciiTable() )
        return item