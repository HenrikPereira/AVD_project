import scrapy
import pandas as pd
from time import sleep
from selenium import webdriver
from scrapy.selector import Selector
from selenium.common.exceptions import NoSuchElementException


class Postos(scrapy.Item):
    urlLoc = scrapy.Field()
    urlPos = scrapy.Field()
    sc95 = scrapy.Field()
    sc95p = scrapy.Field()
    sc98 = scrapy.Field()
    sc98p = scrapy.Field()
    diesel = scrapy.Field()
    dplus = scrapy.Field()
    gpl = scrapy.Field()


class MySpider(scrapy.Spider):
    name = 'combustiveis'
    allowed_domains = ['maisgasolina.com']

    start_urls = []
    for linha in pd.read_csv(r'C:\Users\henri\OneDrive\Documentos\EDSA\AVD\project\Data\links_concelhos_postos.csv')\
            .values:
        for links in linha.tolist():
            for link in links.split(','):
                start_urls.append(link)

    BASE_URL = 'https://www.maisgasolina.com'

    def parse(self, response):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
        self.driver = webdriver.Chrome(r'C:\Users\henri\OneDrive\Documentos\EDSA\AVD\project\Resources\chromedriver.exe')
        self.driver.get(response.url)
        sleep(0.8)
        comb_selector = Selector(text=self.driver.page_source)

        concelhos = Postos()

        concelhos['urlLoc'] = response.url
        concelhos['urlPos'] = response.xpath('//*[@id="stationList"]/a/@href').extract()
        try:
            concelhos['sc95'] = comb_selector.xpath('//*[@id="stationList"]/a/div[4]/div[1]/div[2]/text()').extract()
        except NoSuchElementException:
            concelhos['sc95'] = ''

        try:
            concelhos['sc95p'] = comb_selector.xpath('//*[@id="stationList"]/a/div[4]/div[2]/div[2]/text()').extract()
        except NoSuchElementException:
            concelhos['sc95p'] = ''

        try:
            concelhos['sc98'] = comb_selector.xpath('//*[@id="stationList"]/a/div[4]/div[3]/div[2]/text()').extract()
        except NoSuchElementException:
            concelhos['sc98'] = ''

        try:
            concelhos['sc98p'] = comb_selector.xpath('//*[@id="stationList"]/a/div[4]/div[4]/div[2]/text()').extract()
        except NoSuchElementException:
            concelhos['sc98p'] = ''

        try:
            concelhos['diesel'] = comb_selector.xpath('//*[@id="stationList"]/a/div[4]/div[5]/div[2]/text()').extract()
        except NoSuchElementException:
            concelhos['diesel'] = ''

        try:
            concelhos['dplus'] = comb_selector.xpath('//*[@id="stationList"]/a/div[4]/div[6]/div[2]/text()').extract()
        except NoSuchElementException:
            concelhos['dplus'] = ''

        try:
            concelhos['gpl'] = comb_selector.xpath('//*[@id="stationList"]/a/div[4]/div[7]/div[2]/text()').extract()
        except NoSuchElementException:
            concelhos['gpl'] = ''

        yield concelhos
