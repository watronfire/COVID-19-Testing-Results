import scrapy
import logging
from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt
from dateutil.parser import parse
import re

class CanadaManitobaSpider( scrapy.Spider ) :

    name = "canadamanitoba"
    allowed_domains = ["https://www.gov.mb.ca/covid19/"]
    case_categories = ["positive", "pending", "negative"]
    names = ["Canada, Manitoba" ]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://www.gov.mb.ca/covid19/updates/index.html", callback=self.parse )

    def parse( self, response ):
        item = TestingStats()

        confirmed = response.xpath( '/html/body/div[4]/div/div/div[3]/div[1]/div/table/tbody/tr[7]/td[2]/p/strong/text()' ).get()
        #confirmed = re.split( ' |\xa0', confirmed_paragraph )[0]

        totals_paragraph = response.xpath( '/html/body/div[4]/div/div/div[3]/div[1]/div/p[11]/text()' ).get()
        totals = totals_paragraph.split( "," )[-1]

        totals = "".join( totals.split( " " )[1:3] )
        print( totals )

        deaths = response.xpath( '/html/body/div[4]/div/div/div[3]/div[1]/div/table/tbody/tr[7]/td[5]/p/strong/text()' ).get()
        #deaths = re.split( ' |\xa0', deaths_paragraph )[0]

        date = response.xpath( '/html/body/div[4]/div/div/div[3]/div[1]/div/p[10]/em/text()' ).get()
        date = parse( date, fuzzy=True )

        item["date"] = date.strftime( "%Y-%m-%d" )
        item["name"] = self.names[0]
        item["positive"] = confirmed
        item["negative"] = int( totals.replace( ",", "" ) ) - int( confirmed.replace( ",", "" ) )
        item["deaths"] = deaths
        print( item.toAsciiTable() )
        return item