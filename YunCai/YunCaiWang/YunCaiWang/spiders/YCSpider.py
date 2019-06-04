# -*- coding: utf-8 -*-
import sys
import scrapy
import urlparse
import re

from YunCaiWang.settings import COOKIE
reload(sys)
sys.setdefaultencoding('utf8')
def getcookie(cookie):
    item_dict = {}
    for item in cookie.split(';'):
        item_dict[item.split('=')[0].strip()] = item.split('=')[1].strip()
    return item_dict


class YcspiderSpider(scrapy.Spider):
    name = 'YCSpider'
    allowed_domains = ['http://www.zgsgycw.com']
    start_urls = ['http://www.zgsgycw.com/Portal/Search?t=%E6%9D%90%E6%96%99&c=%E9%87%87%E8%B4%AD%E5%85%AC%E5%91%8A&Page={}'.format(i) for i in range(800,2783)]

    def parse(self, response):
        cookie = COOKIE
        for i in response.xpath('//table[@class="table table-hover"]/tbody/tr'):
            yield scrapy.Request(urlparse.urljoin('http://www.zgsgycw.com',i.xpath('td[4]/a/@href').extract_first().replace('\r','').replace('\n','').strip()),cookies=cookie,callback=self.detail,dont_filter=True,meta={'title':i.xpath('td[4]/a/text()')[-1].extract().replace('\r','').replace('\n','').strip(),'publish_time':i.xpath('td[3]/a/text()').extract_first().replace('\r','').replace('\n','').strip()})

    def detail(self,response):
        from YunCaiWang.items import YuncaiwangItem
        items = YuncaiwangItem()
        from bs4 import BeautifulSoup
        con = BeautifulSoup(response.body).find_all('div',class_="col-md-9 left")[0]


        try:
            div = con.find_all('div',class_="form-group form-group-btn text-center")[0]
            div.clear()
        except:
            pass
        try:
            blockquote = con.find_all('blockquote')[0]
            blockquote.clear()
        except:
            pass
        items['title'] = response.meta['title']
        items['publish_time'] = response.meta['publish_time']
        items['con'] =str(con).replace('"','\'')
        items['province'] = response.xpath('/html/body/div/div/div[2]/div[1]/div[2]/div[3]/div/text()').extract_first().replace('\r','').replace('\n','').strip().split(' ')[0]
        # province_id = scrapy.Field()
        items['city'] = response.xpath('/html/body/div/div/div[2]/div[1]/div[2]/div[3]/div/text()').extract_first().replace('\r','').replace('\n','').strip().split(' ')[1]
        # city_id = scrapy.Field()
        items['company_name'] = response.xpath('/html/body/div/div/div[2]/div[1]/div[2]/div[1]/div/a/text()').extract_first()+response.xpath('/html/body/div/div/div[2]/div[1]/div[2]/div[2]/div/text()').extract_first().replace('\r','').replace('\n','').strip()
        #
        items['phone'] = response.xpath('/html/body/div/div/div[2]/div[1]/div[2]/div[5]/div/text()').extract_first().replace('\r','').replace('\n','').strip()

        items['contact_nam'] = response.xpath('/html/body/div/div/div[2]/div[1]/div[2]/div[4]/div/text()').extract_first().replace('\r','').replace('\n','').strip()
        # print items['city']
        yield items






