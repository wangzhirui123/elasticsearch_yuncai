# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YuncaiwangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    publish_time = scrapy.Field()
    con = scrapy.Field()
    province = scrapy.Field()
    province_id = scrapy.Field()
    city = scrapy.Field()
    city_id = scrapy.Field()
    company_name = scrapy.Field()
    phone = scrapy.Field()
    contact_nam = scrapy.Field()
