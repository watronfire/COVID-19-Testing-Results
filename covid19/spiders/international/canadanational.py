import scrapy
import logging

from scrapy.crawler import CrawlerProcess

from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt
from dateutil.parser import parse

class CanadaNationalSpider( scrapy.Spider ):
    name = "canadanational"
    allowed_domains = ["https://www.canada.ca"]
    obj = ["CanadaNational"]
    case_categories = ["total", "positive", "negative"]
    names = ["Canada National"]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request(
            "https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection.html",
            callback=self.parse )

    def parse( self, response ) :
        item = TestingStats()
        item_dict = { "name" : self.names[0] }

        date = response.xpath( '/html/body/main/div[7]/table/caption/text()' ).get()
        date = date.split( " of ")[-1]
        date = parse( date, fuzzy=True )

        case_table = response.xpath( '/html/body/main/div[7]/table/tbody/tr' )
        for i, row in enumerate( case_table.xpath( 'td/text()' )[:3] ):
            if i == 0:
                total = int( row.get().replace( ",", "" ) )
            else:
                item_dict[self.case_categories[i]] = int( row.get().replace( ",", "" ) )

        #deaths = response.xpath( '/html/body/div/table/tbody/tr[1]/td[4]/text()' ).get()
        deaths = 109
        item_dict["deaths"] = deaths

        item["date"] = date.strftime( "%Y-%m-%d" )

        # Commenting this out because its not clear if pending cases are listed or not.
        item_dict["pending"] = total - ( item_dict["positive"] + item_dict["negative"] )

        for i in item_dict.keys():
            item[i] = item_dict[i]

        print( item.toAsciiTable() )
        return item