# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CasesCategory(scrapy.Item):
    positive = scrapy.Field(serialier = int)
    negative = scrapy.Field(serialzer = int)
    pending = scrapy.Field(serializer = int)
    name = scrapy.Field()

class SanDiegoCovid19Stats(scrapy.Item):
    date = scrapy.Field()
    SanDiegoCounty = scrapy.Field(serializer = CasesCategory)
    FederalQuarantine = scrapy.Field(serializer = CasesCategory)
    NonSanDiegoCounty = scrapy.Field(serializer = CasesCategory)

    def getTotal(self, key):
        return int(self[key]["positive"]) +int(self[key]["pending"]) + int(self[key]["negative"])

    def toAsciiTable(self):
        row_format = "|{:^30}" * 4 + "|\n"
        rows = []
        rows.append(["", self["SanDiegoCounty"]["name"], self["FederalQuarantine"]["name"], self["NonSanDiegoCounty"]["name"]])
        rows.extend([[i.capitalize(), self["SanDiegoCounty"][i], self["FederalQuarantine"][i], self["NonSanDiegoCounty"][i]] for i in ["positive", "pending", "negative"]])
        rows.append(["Total", self.getTotal("SanDiegoCounty"), self.getTotal("FederalQuarantine"), self.getTotal("NonSanDiegoCounty")])
        row_str = "Last updated: {}".format(self["date"])
        row_str += "\n```\n"
        for i in rows:
            row_str += row_format.format(*i)
        row_str += "```\n"
        row_str += "Total cases: {}".format(sum([self.getTotal("SanDiegoCounty"), self.getTotal("FederalQuarantine"), self.getTotal("NonSanDiegoCounty")]))
        return row_str
