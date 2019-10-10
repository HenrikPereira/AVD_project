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

class MySpider(scrapy.Spider):
    name = 'entrepostoauto'
    allowed_domains = ['entrepostoauto.pt']
    start_urls = ['https://www.entrepostoauto.pt/viaturas/listagem?carType=novos&orderby=1&currentPage=1']
    BASE_URL = 'https://www.entrepostoauto.pt'
    custom_settings = {'DEPTH_LIMIT': 1}

    def parse(self, response):
        links = response.xpath("//*[@id='main']/section/div[2]/div[1]/div/section/ul/li/a/@href").extract()
        #foto = FotoItem()
        #foto['foto'] = self.BASE_URL + \
        #               response.xpath("//section/div[2]/div[1]/div/section/div/aside/figure/img/@src").extract()
        for link in links:
            full_url = self.BASE_URL + link
            yield scrapy.Request(full_url, callback=self.parse_details)

    def parse_details(self, response):
        lista_final = []
        i = MainItem()
        i['mar'] = response.xpath("//div/section[2]/div[1]/div[2]/h1/span/text()").extract()
        i['mod'] = response.xpath("//div/section[2]/div[1]/div[2]/h1/text()").extract()
        # i['cars']['mar']['mod']['ver'] = response.xpath("//div/section[2]/div[1]/div[2]/p[1]/text()").extract()
        # i['cars']['mar']['mod']['logo'] = self.BASE_URL + response.xpath("//section[1]/div[2]/article/div[3]/picture/img/@src").extract()
        # i['cars']['mar']['mod']['ver']['link'] = response.url
        # i['cars']['mar']['mod']['ver']['preco'] = response.xpath("//div/section[2]/div[1]/div[2]/h2/text()[1]").extract()
        # i['cars']['mar']['mod']['ver']['specs'] = response.xpath("//article/ul/li//text()").extract()
        # i['cars']['mar']['mod']['ver']['equip'] = response.xpath("//article[1]/div/div/div/p/text()").extract()

        lista_final.append(i)
        lista_act = []

        for it in lista_final:
            for n in range(len(it['mar'])):
                sub = {}
                sub['cars'] = {}
                sub['cars']['mar'] = [it['mar'][n]]
                sub['cars']['mod'] = [it['mod'][n]]

                lista_act.append(sub)

        return lista_act

        # response.xpath("//section/div[2]/div[1]/div/section/div/aside/figure/img/@src").extract() --> img do carro
        # response.xpath("//article/ul/li//text()").extract() --> especificações
        # response.xpath("//article[1]/div/div/div/p/text()").extract() --> equipamento de série
        # response.xpath("//section[1]/div[2]/article/div[3]/picture/img/@src").extract() --> logo marca
        # response.xpath("//div/section[2]/div[1]/div[2]/h1//text()").extract() --> marca modelo
        # response.xpath("//div/section[2]/div[1]/div[2]/p[1]/text()").extract() --> versão
        # response.xpath("//div/section[2]/div[1]/div[2]/h2/text()[1]").extract() --> preço

        # for line in response.xpath('//*[@id="main"]/section/div[2]/div[1]/div/section/div[1]/div[2]/p'):
        #     yield {
        #         'model': line.xpath('//*[@id="main"]/section/div[2]/div[1]/div/section/div[1]/div[2]/p/text()').extract_first(),
        #         'link': line.xpath("//*[@id='main']/section/div[2]/div[1]/div/section/ul/li/a/@href").extract()
        #     }

        # uls = response.xpath('//*[@id="main"]/section/div[2]/div[1]/div/section/ul')
        # item = {'model': ''}
        # for ul in uls:
        #     # for each ul, add a key value pair
        #     item['model'][ul.xpath("//*[@id='main']/section/div[2]/div[1]/div/section/ul/li/p/text()").extract_first()] \
        #         = {"link{}".format(i):
        #                node for i, node in enumerate(ul.xpath("//*[@id='main']/section/div[2]/div[1]/div/section/ul/li/a/@href")
        #                                              .getall())}
        # # yield outside the loop


        #yield item
        #while True:
        #    next = self.driver.find_element_by_xpath('//*[@id="main"]/section/div[2]/div[2]/a[16]')
        #    try:
        #        next.click()
        #    except:
        #        break