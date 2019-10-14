import scrapy
import pandas as pd


class MainItem(scrapy.Item):
    mar = scrapy.Field()
    mod = scrapy.Field()
    ver = scrapy.Field()
    preco = scrapy.Field()
    link = scrapy.Field()
    specs = scrapy.Field()
    equip = scrapy.Field()
    logo = scrapy.Field()
    cars = scrapy.Field()
    foto = scrapy.Field()
    burl = scrapy.Field()


class MySpider(scrapy.Spider):
    name = 'entrepostoauto'
    allowed_domains = ['entrepostoauto.pt']
    start_urls = [link
                  for sub in pd.read_csv(r'C:\Users\henri\OneDrive\Documentos\EDSA\AVD\project\Data\dados_entreposto.csv')
                      .values.tolist()
                  for link in sub]
    BASE_URL = 'https://www.entrepostoauto.pt'

    def parse(self, response):

        def merge(list1, list2):
            merged_list = tuple(zip(list1, list2))
            return merged_list

        atrib = MainItem()

        atrib['mar'] = response.xpath("//div/section[2]/div[1]/div[2]/h1/span/text()").extract()[0]
        atrib['mod'] = response.xpath("//div/section[2]/div[1]/div[2]/h1/text()").extract()[0]
        atrib['ver'] = response.xpath("//div/section[2]/div[1]/div[2]/p[1]/text()").extract()[0]
        atrib['logo'] = self.BASE_URL + response.xpath("//section[1]/div[2]/article/div[3]/picture/img/@src").extract()[0]
        atrib['link'] = response.url
        atrib['burl'] = self.BASE_URL
        atrib['preco'] = response.xpath("//div/section[2]/div[1]/div[2]/h2/text()[1]").extract()[0]
        atrib['specs'] = merge(response.xpath("//article/ul/li/text()").extract(),
                           response.xpath("//article/ul/li/strong/text()").extract())
        atrib['equip'] = response.xpath("//article[1]/div/div/div/p/text()").extract()
        atrib['foto'] = response.xpath("//div[1]/div/div/article/div/@*").extract()[0:4]

        yield atrib
