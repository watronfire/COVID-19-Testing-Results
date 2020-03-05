import scrapy
import logging
from covid19.items import CanadaCovid19Stats
import requests
import json
from scrapy.crawler import CrawlerProcess

item = CanadaCovid19Stats()

class CanadaBritishColumbiaSpider( scrapy.Spider ) :

    name = "canadabritishcolumbia"
    allowed_domains = ["http://www.bccdc.ca/", "https://www.publichealthontario.ca"]
    obj = ["BritishColumbia", "Ontario"]
    case_categories = ["positive", "pending", "negative"]
    names = ["British Columbia", "Ontario" ]

    custom_settings = { "LOG_LEVEL" : logging.ERROR }



    def start_requests( self ):
        yield scrapy.Request( "http://www.bccdc.ca/about/news-stories/stories/2020/information-on-novel-coronavirus", callback=self.bcparse )
        yield scrapy.Request( "https://www.publichealthontario.ca/en/diseases-and-conditions/infectious-diseases/respiratory-diseases/novel-coronavirus", callback=self.onparse )

    def bcparse( self, response ):

        confirmed_paragraph = response.xpath( '//*[@id="ctl00_PlaceHolderMain_SubPlaceholder_ctl07__ControlWrapper_RichHtmlField"]/div[1]/div[1]/ul/li[1]/text()' ).get()
        totals_paragraph = response.xpath( '//*[@id="ctl00_PlaceHolderMain_SubPlaceholder_ctl07__ControlWrapper_RichHtmlField"]/div[1]/div[1]/ul/li[2]/p/text()' ).get()
        confirmed = int( confirmed_paragraph.split( "\xa0" )[0] )
        total_tested = int( totals_paragraph.split( " " )[0].replace( ",", "" ) )
        date =  " ".join( totals_paragraph[:-2].split( " " )[8:10] )

        item["date"] = date
        item["BritishColumbia"] = { "name" : "British Columbia",
                    "positive" : confirmed,
                    "negative" : total_tested - confirmed,
                    "pending" : "Unknown" }
        return item

    def onparse( self, response ):
        confirmed = 0
        negative = 0
        pending = 0

        case_table = response.xpath( '//*[@id="pho-main-content-grid"]/div[5]/div/div/table/tbody' )
        for i, row in enumerate( case_table.xpath( 'tr' )[1:-1] ):
            definition = row.xpath( "td[1]/text()" ).get()
            value = row.xpath( "td[2]/text()").get()
            if i == 0: negative = int( value )
            elif i == 1: pending = int( value )
            elif i == 2: confirmed = int( value )

        item["Ontario"] = { "name" : "Ontario",
                                 "positive" : confirmed,
                                 "negative" : negative,
                                 "pending" : pending }
        return item

    #def close( self ):
     #   print( self.item.keys() )
    #    print( self.item.toAsciiTable() )


process = CrawlerProcess()
process.crawl( CanadaBritishColumbiaSpider )
process.start()
process.stop()
print( item.toAsciiTable() )