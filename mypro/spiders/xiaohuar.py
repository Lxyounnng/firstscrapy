# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector,HtmlXPathSelector
from scrapy.http import Request
import requests

class XiaohuarSpider(scrapy.Spider):
    name = 'xiaohuar'
    allowed_domains = ['xiaohuar.com']
    start_urls = ['http://www.xiaohuar.com/hua/']

    def parse(self, response):
        hxs = Selector(response=response)
        user_list = hxs.xpath('//div[@class="item masonry_brick"]')

        for item in user_list:
            price = item.xpath('.//span[@class="price"]/text()').extract_first()
            url = item.xpath('div[@class="item_t"]/div[@class="title"]//a/@href').extract_first()

            src = item.xpath('div[@class="item_t"]/div[@class="img"]//img/@src').extract_first()
            photo_url = "http://www.xiaohuar.com%s" %(src)
            photo = requests.get(photo_url)
            filename = "F:\photo/%s.jpg" %(price)
            with open(filename,'wb') as f:
                f.write(photo.content)

            print(price,url,src)

        result = hxs.xpath('//a[re:test(@href,"http://www.xiaohuar.com/list-1-\d+.html")]/@href').extract()
        for url in result:
            yield Request(url=url, callback=self.parse)
