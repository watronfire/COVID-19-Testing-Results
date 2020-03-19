# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from datetime import datetime as dt

class TestingStats( scrapy.Item ):
    date = scrapy.Field()
    positive = scrapy.Field( serializer = int )
    pending = scrapy.Field( serializer = int )
    negative = scrapy.Field( serializer = int )
    deaths = scrapy.Field( serializer = int )
    name = scrapy.Field( serializer = str )


    def getTotal(self, key = "positive"):
        categories = sorted( [i for i in self.keys() if i not in  ["date", "name"]] )
        return sum( [int( self[i] ) for i in categories] )

    def toAsciiTable(self):
        # Get case categories for which data exists
        case_categories = sorted([i for i in self.keys() if i not in ["date", "name"]])
        row_format = "|{:^30}|{:^30}|\n"
        rows = list()
        rows.append( [""] )
        rows[0].extend( [self["name"]] )
        rows.extend( [[i.capitalize()] + [self[i]] for i in case_categories] )
        rows.append( ["Total"] + [self.getTotal()] )
        row_str = "Last updated: {}".format( dt.strftime( dt.strptime( self["date"], "%Y-%m-%d %H:%M %p"), "%Y-%m-%d" ) )
        row_str += "\n```\n"
        for i in rows:
            row_str += row_format.format( *i )
        row_str += "```\n"
        return row_str