import scrapy
import logging
from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt
from dateutil.parser import parse

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

        results = response.xpath( '/html/body/div[1]/div[6]/div/div[1]/div[2]/div/table' )

        for i, row in enumerate( results.xpath( "tbody/tr" )[0:3] ):
            if i == 0:
                value = row.xpath( 'td[2]/b/text()' ).get()
            else:
                value = row.xpath( "td[2]/text()" ).get()
            print( value )
            value = value.replace( ',', '' )
            item_dict[self.case_categories[i]] = int( value )

        deaths = response.xpath( '/html/body/div/div[6]/div/div[2]/div[2]/div/table[1]/tbody/tr[15]/td[3]/b/text()' ).get()
        item_dict["deaths"] = deaths

        date = results.xpath( 'thead/tr/th/text()' ).get()
        date = parse( date, fuzzy=True )
        item["date"] = date.strftime( "%Y-%m-%d %H:%M %p" )

        print( item_dict )

        for i in item_dict.keys():
            item[i] = item_dict[i]

        print( item.toAsciiTable() )
        return item