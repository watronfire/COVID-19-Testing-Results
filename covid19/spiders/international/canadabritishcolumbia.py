import scrapy
import logging
from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt
from dateutil.parser import parse
import re

class CanadaBritishColumbiaSpider( scrapy.Spider ) :

    name = "canadabritishcolumbia"
    allowed_domains = ["http://www.bccdc.ca/"]
    obj = ["BritishColumbia"]
    case_categories = ["positive", "pending", "negative"]
    names = ["Canada, British Columbia" ]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "http://www.bccdc.ca/about/news-stories/stories/2020/information-on-novel-coronavirus", callback=self.parse )

    def parse( self, response ):
        item = TestingStats()

        confirmed_paragraph = response.xpath( '/html/body/form/div[5]/div/span/div[1]/div/div/div[3]/article/div/div/div[2]/div[1]/div/ul/li[1]/strong/text()' ).get()
        confirmed = re.split( ' |\xa0', confirmed_paragraph )[0]
        confirmed = confirmed.replace( ",", '' )

        totals_paragraph = response.xpath( '/html/body/form/div[5]/div/span/div[1]/div/div/div[3]/article/div/div/div[2]/div[1]/div/ul/li[2]/text()' ).get()
        totals = re.split( ' |\xa0', totals_paragraph )[0]
        totals = totals.replace( ",", "" )

        deaths_paragraph = response.xpath( '/html/body/form/div[5]/div/span/div[1]/div/div/div[3]/article/div/div/div[2]/div[1]/div/ul/ul/li[2]/text()' ).get()
        deaths = re.split( ' |\xa0', deaths_paragraph )[0]

        date = parse( confirmed_paragraph.split( "of " )[-1], fuzzy=True )
        #date = dt.strptime( date, "\xa0%B %d,\xa0%Y.\xa0" )

        print( "Confirmed: {}".format( confirmed ) )
        print( "totals: {}".format( totals ) )
        print( "deaths: {}".format( deaths ) )


        item["date"] = date.strftime( "%Y-%m-%d" )
        item["name"] = self.names[0]
        item["positive"] = confirmed
        item["negative"] = int( totals.replace( ",", "" ) ) - int( confirmed.replace( ",", "" ) )
        item["deaths"] = deaths
        print( item.toAsciiTable() )
        return item