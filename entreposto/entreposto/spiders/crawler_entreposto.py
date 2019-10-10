import scrapy
from scrapy.crawler import CrawlerProcess

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
    start_urls = ['https://www.entrepostoauto.pt/viaturas/listagem?carType=novos&orderby=1&currentPage=%s' % page for page in range(1,12)]
    BASE_URL = 'https://www.entrepostoauto.pt'
    custom_settings = {'DEPTH_LIMIT': 1}

    def parse(self, response):
        links = response.xpath("//*[@id='main']/section/div[2]/div[1]/div/section/ul/li/a/@href").extract()

        for link in links:
            full_url = self.BASE_URL + link
            yield scrapy.Request(full_url, callback=self.parse_details)

        while True:
           next = self.driver.find_element_by_xpath('//*[@id="main"]/section/div[2]/div[2]/a[16]/@next')
           try:
               next.click()
           except:
               break

    def parse_details(self, response):

        def merge(list1, list2):
            merged_list = tuple(zip(list1, list2))
            return merged_list

        i = MainItem()

        i['mar'] = response.xpath("//div/section[2]/div[1]/div[2]/h1/span/text()").extract()[0]
        i['mod'] = response.xpath("//div/section[2]/div[1]/div[2]/h1/text()").extract()[0]
        i['ver'] = response.xpath("//div/section[2]/div[1]/div[2]/p[1]/text()").extract()[0]
        i['logo'] = self.BASE_URL + response.xpath("//section[1]/div[2]/article/div[3]/picture/img/@src").extract()[0]
        i['link'] = response.url
        i['burl'] = self.BASE_URL
        i['preco'] = response.xpath("//div/section[2]/div[1]/div[2]/h2/text()[1]").extract()[0]
        i['specs'] = merge(response.xpath("//article/ul/li/text()").extract(),
                           response.xpath("//article/ul/li/strong/text()").extract())
        i['equip'] = response.xpath("//article[1]/div/div/div/p/text()").extract()
        i['foto'] = response.xpath("//div[1]/div/div/article/div/@*").extract()

        yield i