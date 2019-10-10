# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class FotoItem(scrapy.Item):
    foto = scrapy.Field()

class MainItem(scrapy.Item):
    mar_mod = scrapy.Field()
    ver = scrapy.Field()
    preco = scrapy.Field()
    link = scrapy.Field()
    specs = scrapy.Field()
    equip = scrapy.Field()
    logo = scrapy.Field()
