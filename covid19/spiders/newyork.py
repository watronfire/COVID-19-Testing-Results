# -*- coding: utf-8 -*-
import scrapy
from covid19.items import TestingStats
from datetime import datetime as dt

class NewyorkSpider(scrapy.Spider):
    name = 'newyork'
    allowed_domains = ['health.ny.gov']
    start_urls = ['https://health.ny.gov/diseases/communicable/coronavirus/']

    objs = ["Local", "NonLocal"]
    case_categories = ["positive", "negative", "pending"]
    names = ["Outside of New York City", "New York City"]
    
    def parse(self, response):
        caption = response.xpath("//table/caption//text()").extract_first()
        item = TestingStats()
        date = response.xpath("//table/caption//text()").extract_first()
        date = dt.strptime(date[18:], "%H:%M%p %B %d, %Y")
        item["date"] = date.strftime("%Y-%m-%d %H:%M %p")
        cases_table = response.xpath("//table")[0]
        rows = cases_table.xpath("tr")
        for rind, row in enumerate(rows[1:]):
            for cind, cell in enumerate(row.xpath("td//text()").extract()[1:3]):
                if self.objs[cind - 1] not in item.keys():
                    item[self.objs[cind - 1]] = {
                        "name": self.names[cind - 1]
                    }
                item[self.objs[cind - 1]][self.case_categories[rind]] = cell
        # PUI as a separate category since ful new york state
        pui = rows[1].xpath("td//text()").extract()[-1]
        item["Combined"] = {
            "name": "New York State (Total)",
            "pui": pui
        }
        return item
