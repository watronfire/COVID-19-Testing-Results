# -*- coding: utf-8 -*-
import scrapy
from covid19.items import TestingStats
from datetime import datetime as dt
from dateutil.parser import parse
import logging
from io import StringIO
import pandas as pd

class ItalySpider(scrapy.Spider):
    name = 'italy'
    allowed_domains = ['https://raw.githubusercontent.com/']
    names = ["Italy"]
    case_categories = ["positive", "negative"]
    custom_settings = {"LOG_LEVEL" : logging.ERROR }

    def start_requests( self ):
        yield scrapy.Request( "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv", callback=self.parse )

    def parse(self, response):
        item = TestingStats()

        api_call = pd.read_csv( StringIO( response.body_as_unicode() ) )
        api_call["data"] = pd.to_datetime( api_call["data"] )

        last_event = api_call.iloc[-1]

        # Currently the api returns an empty date
        item["date"] = last_event["data"].strftime( "%Y-%m-%d" )
        item["name"] =  self.names[0]
        item["positive"] = last_event["totale_positivi"]
        item["negative"] = last_event["tamponi"] - last_event["totale_positivi"]
        item["deaths"] = last_event["deceduti"]

        print( item.toAsciiTable() )
        return item

