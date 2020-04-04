import scrapy
import logging
from covid19.items import TestingStats
from dateutil.parser import parse
from datetime import datetime as dt

class CanadaSaskatchewanSpider( scrapy.Spider ) :

    name = "canadasaskatchewan"
    allowed_domains = ["https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/cases-and-risk-of-covid-19-in-saskatchewan"]
    case_categories = ["positive", "pending", "negative"]
    names = ["Canada, Saskatchewan" ]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/cases-and-risk-of-covid-19-in-saskatchewan", callback=self.parse )

    def parse( self, response ):
        item = TestingStats()

        confirmed = response.xpath( '/html/body/form/div[5]/div[3]/div[1]/section/table[3]/tbody/tr[8]/td[4]/strong/text()' ).get()
        confirmed = confirmed.replace( ',', "" )
        confirmed = confirmed.replace( "*", "" )

        negative = response.xpath( '/html/body/form/div[5]/div[3]/div[1]/section/table[3]/tbody/tr[8]/td[5]/strong/text()' ).get()
        negative = negative.replace( ',', "" )

        date = response.xpath( '/html/body/form/div[5]/div[3]/div[1]/section/p[13]/strong/text()' ).get()
        date = date.split( "(" )[-1]
        print( date )
        date = parse( date, fuzzy=True )

        deaths = response.xpath( '/html/body/form/div[5]/div[3]/div[1]/section/table[1]/tbody/tr[8]/td[7]/strong/text()' ).get()

        item["date"] = date.strftime( "%Y-%m-%d" )
        item["name"] = self.names[0]
        item["positive"] = int( confirmed )
        item["negative"] = negative
        item["deaths"] = deaths
        print( item.toAsciiTable() )
        return item