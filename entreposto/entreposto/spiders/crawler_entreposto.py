import scrapy
from scrapy.crawler import CrawlerProcess

class MySpider(scrapy.Spider):
    name = 'entrepostoauto'
    allowed_domains = ['entrepostoauto.pt']
    start_urls = ['https://www.entrepostoauto.pt/viaturas/listagem?carType=novos&orderby=1&currentPage=1']

    custom_settings = {'DEPTH_LIMIT': 1}

    def parse(self, response):
        for line in response.xpath('//*[@id="main"]/section/div[2]/div[1]/div/section/div[1]/div[2]/p'):
            yield {
                'model': line.xpath('//*[@id="main"]/section/div[2]/div[1]/div/section/div[1]/div[2]/p/text()').extract_first(),
                'link': line.xpath("//*[@id='main']/section/div[2]/div[1]/div/section/ul/li/a/@href").extract()
            }

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