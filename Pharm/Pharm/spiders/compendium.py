# -*- coding: utf-8 -*-
import scrapy

from scrapy.selector import Selector
from scrapy.http import Request

from Pharm.items import PharmItem

class CompendiumSpider(scrapy.Spider):
    name = "compendium"
    allowed_domains = ["compendium.com.ua"]
    start_urls = (                          # Scrapy will automatically
        'http://compendium.com.ua/makers',  # retrieve this page for you and
    )                                       # pass it to you parse() method

    def parse(self, response):
        # Let's retrieve links to all sub-pages using XPath query:
        pages = Selector(response=response)\
                    .xpath('//*[@id="src_top"]/div/div/a/@href')\
                    .extract()

        # Iterate over all pages and emit new request for each:
        for lnk in pages:
            yield Request('http://{}{}'.format(self.allowed_domains[0], lnk),
                          callback=self.retrieve_companies)  # Let Scrapy pass
                                                             # response to
                                                             # retrieve_companies()
                                                             # method

    def retrieve_companies(self, response):
        comps = Selector(response=response)\
                    .xpath('//*/a[@class="makers_list"]/@href')\
                    .extract()
                    
        for lnk in comps:
            yield Request('http://{}{}'.format(self.allowed_domains[0], lnk),
                          callback=self.retrieve_preparats)
                          
                          
            
    def retrieve_preparats(self, response):
        comps = Selector(response=response)\
                    .xpath('//*/a[@class="preparat_list"]')

        for lnk in comps:
            item = PharmItem(name=lnk.extract(),
                             link=lnk.xpath('@href').extract())        
            yield item
