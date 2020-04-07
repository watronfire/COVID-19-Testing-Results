import scrapy
import logging
from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt
from dateutil.parser import parse

class UKSpider( scrapy.Spider ):
    name = "unitedkingdomnational"
    allowed_domains = ["https://www.gov.uk/"]
    obj = ["UnitedKingdom"]
    case_categories = ["total", "positive"]
    names = ["United Kingdom"]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://www.gov.uk/guidance/coronavirus-covid-19-information-for-the-public", callback=self.parse )

    def parse( self, response ):
        item = TestingStats()
        item_dict = { "name" : self.names[0] }

        date_paragraph = response.xpath( '//*[@id="contents"]/div[2]/div/p[2]/text()' ).get()
        date = date_paragraph.split( "," )[0]
        date += " 2020"
        date = parse( date, fuzzy=True )

        case_paragraph = response.xpath( '/html/body/div[6]/main/div[3]/div[1]/div/div[2]/div/p[3]/text()' ).get()
        case_paragraph = case_paragraph.replace( ",", "" )

        values = [i for i in case_paragraph.split( " " ) if i.isnumeric()]
        for i, value in enumerate( values ):
            item_dict[self.case_categories[i]] = value

        deaths = response.xpath( '/html/body/div[6]/main/div[3]/div[1]/div/div[2]/div/p[4]/text()' ).get()
        deaths = deaths.split( "," )[-1]
        deaths = deaths.split( ' ' )[0]

        item_dict["negative"] = int( item_dict["total"] ) - int( item_dict["positive"] )
        item_dict["deaths"] = deaths
        del item_dict["total"]

        item["date"] = date.strftime( "%Y-%m-%d" )
        for i in item_dict.keys():
            item[i] = item_dict[i]

        print( item.toAsciiTable() )
        return item