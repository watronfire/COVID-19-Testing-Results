# -*- coding: utf-8 -*-
import scrapy
from covid19.items import TestingStats
import requests
import json
import covid19.config
from covid19.config import slack_sandiego_post_url
from datetime import datetime as dt

class FloridaSpider(scrapy.Spider):
    name = 'florida'
    allowed_domains = ['www.floridahealth.gov']
    start_urls = ["http://www.floridahealth.gov/diseases-and-conditions/COVID-19/_documents/covid19-daily-numbers.txt"]
    # Ajax request from http://www.floridahealth.gov/diseases-and-conditions/COVID-19/index.html

    def parse(self, response):
        text = response.text
        item = TestingStats()
        split_text = text.split("*")
        date = split_text[0]
        date = dt.strptime(date.replace("p.m.", "PM"), "%H:%M %p ET %d/%m/%Y")
        item["date"] = date.strftime("%Y-%m-%d %H:%M %p")
        item["Local"] = {
            "name": "Florida",
            "positive": split_text[1],
            "presumedPositive": split_text[2],
            "pending": split_text[3],
            "negative": split_text[4],
            "pui": split_text[5]
        }
        item["NonLocal"] = {
            "name": "Non Florida",
            "positive": split_text[-4],
            "presumedPositive": split_text[-3]
        }
        print(item.toAsciiTable())
        return item

