import scrapy
import logging
from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt

class OregonSpider( scrapy.Spider ) :

    name = "oregon"
    allowed_domains = ["https://www.oregon.gov/"]
    obj = ["Oregon"]
    case_categories = ["positive", "negative", "pending" ]
    names = ["Oregon" ]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }


    def start_requests( self ):
        yield scrapy.Request( "https://www.oregon.gov/oha/PH/DISEASESCONDITIONS/DISEASESAZ/Pages/emerging-respiratory-infections.aspx", callback=self.parse )

    def parse( self, response ):
        item = TestingStats()
        item_dict = { "name" : self.names[0] }

        results = response.xpath( '/html/body/form/main/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div/table[1]/tbody' )

        for i, row in enumerate( results.xpath( "tr" )[1:4] ):
            value = row.xpath( "td[2]/text()" ).get()
            item_dict[self.case_categories[i]] = int( value )

        deaths = response.xpath( '/html/body/form/main/div/div[2]/div/div/div[2]/div/div/div[1]/div/div/div/div/table[2]/tbody/tr[15]/td[3]/strong/text()' ).get()
        item_dict["deaths"] = deaths

        date = results.xpath( "tr[1]/td/em/text()").get()
        date = date[:-1]
        date = dt.strptime( date, "As of %m/%d/\u200b%Y, %I:%M %p" )
        item["date"] = date.strftime( "%Y-%m-%d %H:%M %p" )

        for i in item_dict.keys():
            item[i] = item_dict[i]

        print( item.toAsciiTable() )
        return item