# -*- coding: UTF-8 -*-
from ..items import MyItem

import scrapy


class MeizituSpider(scrapy.Spider):
    name = "meizitu"
    host = "http://www.meizitu.com/"
    start_urls = [
        "http://www.meizitu.com/a/fuli.html"
        # "http://www.meizitu.com/a/pure.html"
    ]

    def parse(self, response):
        nextPage = response.xpath(u'//div[@id="wp_page_numbers"]//a[text()="下一页"]/@href').extract_first()
        nextPage = self.host + nextPage

        for p in response.xpath("//li[@class='wp-item']//a//@href").extract():
            yield scrapy.Request(p, callback=self.parse_item)

        yield scrapy.Request(nextPage, classback=self.parse)

    def parse_item(self, response):
        item = MyItem()
        item['image_urls'] = response.xpath("//div[@id='picture']//img/@src").extract()
        item['name'] = response.xpath("//div[@id='picture']//img/@alt").extract()[0].split(u'，')[0]
        return item
