# -*- coding: utf-8 -*-
import scrapy

from scrapy.selector import Selector
from scrapy.http import Request

from Pharm.items import PharmItem

class CompendiumSpider(scrapy.Spider):
    name = "compendium"
    allowed_domains = ["compendium.com.ua"]
    start_urls = (
        'http://compendium.com.ua/makers',
    )

    def parse(self, response):
        return self.parse_start_url(response)

    def parse_start_url(self, response):
        # '//*[@id="src_top"]/div/div/a'
        pages = Selector(response=response).xpath('//*[@id="src_top"]/div/div/a/@href').extract()

        for lnk in pages:
            yield Request('{}{}'.format(self.start_urls[0], lnk), callback=self.retrieve_companies)

    def retrieve_companies(self, response):
        #import ipdb; ipdb.set_trace()
        #print(response)
        comps = Selector(response=response).xpath('//*[@id="green_wrap"]/table/tbody/tr/td/div/a').extract()
        #print(comps)

        for lnk in comps:
            item = PharmItem(name=lnk.extract(), link=lnk.xpath('@href').extract())
            #print(item)
            yield item
