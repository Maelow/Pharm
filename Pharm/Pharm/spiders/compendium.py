# -*- coding: utf-8 -*-

from scrapy.contrib.spiders.crawl import CrawlSpider
from scrapy.http import Request

from Pharm.items import PharmItem

class CompendiumSpider(CrawlSpider):
    name = "compendium"
    allowed_domains = ["compendium.com.ua"]
    start_urls = (                          # Scrapy will automatically
        'http://compendium.com.ua/makers',  # retrieve this page for you and
    )                                       # pass it to you parse() method

    def parse_start_url(self, response):
        # Let's retrieve links to all sub-pages using XPath query:
        pages = response.xpath('//*[@id="src_top"]/div/div/a/@href').extract()

        # Iterate over all pages and emit new request for each:
        for lnk in pages:
            yield Request('http://{}{}'.format(self.allowed_domains[0], lnk),
                          callback=self.retrieve_companies)  # Let Scrapy pass
                                                             # response to
                                                             # retrieve_companies()
                                                             # method

    def retrieve_companies(self, response):
        comps = response.css('.makers_list')

        for lnk in comps:
            clnk = lnk.xpath('@href').extract()
            if len(clnk) < 1:
                continue

            req = Request('http://{}{}'.format(self.allowed_domains[0],
                                               clnk[0]),
                          callback=self.retrieve_preparats)

            # this will be available in callback via response.meta:
            req.meta['company_name'] = lnk.xpath('text()').extract()[0]

            yield req

    def retrieve_preparats(self, response):
        cname = response.meta['company_name']

        comps = response.css('.preparat_list')

        for lnk in comps:
            iname = lnk.xpath('text()').extract()
            if len(iname) < 1:  # empty prod name
                continue
            ilnk = lnk.xpath('@href').extract()[0]
            item = PharmItem(name=iname[0], link=ilnk, company_name=cname)
            yield item
