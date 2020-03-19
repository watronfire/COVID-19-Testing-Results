import scrapy
import logging
from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt

class CanadaBritishColumbiaSpider( scrapy.Spider ) :

    name = "canadabritishcolumbia"
    allowed_domains = ["http://www.bccdc.ca/"]
    obj = ["BritishColumbia"]
    case_categories = ["positive", "pending", "negative"]
    names = ["British Columbia, CAN" ]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }

    Small = {
        'zero' : 0,
        'one' : 1,
        'two' : 2,
        'three' : 3,
        'four' : 4,
        'five' : 5,
        'six' : 6,
        'seven' : 7,
        'eight' : 8,
        'nine' : 9,
        'ten' : 10,
        'eleven' : 11,
        'twelve' : 12,
        'thirteen' : 13,
        'fourteen' : 14,
        'fifteen' : 15,
        'sixteen' : 16,
        'seventeen' : 17,
        'eighteen' : 18,
        'nineteen' : 19,
        'twenty' : 20,
        'thirty' : 30,
        'forty' : 40,
        'fifty' : 50,
        'sixty' : 60,
        'seventy' : 70,
        'eighty' : 80,
        'ninety' : 90
    }

    def start_requests( self ):
        yield scrapy.Request( "http://www.bccdc.ca/about/news-stories/stories/2020/information-on-novel-coronavirus", callback=self.parse )

    def parse( self, response ):
        item = TestingStats()
        confirmed_paragraph = response.xpath( '/html/body/form/div[5]/div/span/div[1]/div/div/div[3]/article/div/div/div[2]/div[1]/div/ul/li[1]/span/text()' ).get()
        confirmed = confirmed_paragraph.split( "\xa0" )[0]

        totals_paragraph = response.xpath( '/html/body/form/div[5]/div/span/div[1]/div/div/div[3]/article/div/div/div[2]/div[1]/div/ul/li[2]/p/text()' ).get()
        totals = totals_paragraph.split( "\xa0" )[0]

        deaths_paragraph = response.xpath( '/html/body/form/div[5]/div/span/div[1]/div/div/div[3]/article/div/div/div[2]/div[1]/div/ul/ul/li[2]/text()' ).get()
        deaths = self.Small[deaths_paragraph.split( "\xa0" )[0].lower()]

        date = totals_paragraph.split( " of")[-1]
        date = dt.strptime( date, "\xa0%B %d,\xa0%Y.\xa0" )

        item["date"] = date.strftime( "%Y-%m-%d %H:%M %p" )
        item["name"] = self.names[0]
        item["positive"] = confirmed
        item["negative"] = int( totals.replace( ",", "" ) ) - int( confirmed.replace( ",", "" ) )
        item["deaths"] = deaths
        print( item.toAsciiTable() )
        return item