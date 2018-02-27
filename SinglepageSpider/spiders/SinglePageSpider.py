# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import csv
from scrapy import Selector
from scrapy.selector import HtmlXPathSelector 
#from scrapy.contrib.exporter import CsvItemExporter
#from SinglepageSpider.items import SinglepagespiderItem


class SinglepagespiderSpider(scrapy.Spider):
    
    name = 'SinglePageSpider'
    def __init__(self):
        with open("temp.txt", 'r') as f:
            self.start_urls = f.read().split("\n")
        #print(start_urls);
    
    def parse(self, response):
        self.log('I just visited: ' + response.url)
        #reviews = response.xpath("//div[@class=contains(.,('.*review.*'))]/p[1]/text()").extract()
        selector = HtmlXPathSelector(response)
        reviews = selector.xpath('//div[re:test(@class, ".*review.*|.*comment.*|posting fullpost")]/p[1]/text()').extract()
        with open("output.txt","w") as f:
            for review in reviews: 
                #print review
                f.write(review.encode("utf-8")); 
                f.write("++++++++++++++\n")
        #### Writing to a csv file    
        with open("Reviews.csv", "w") as toWrite:
            writer = csv.writer(toWrite, delimiter=",")
            writer.writerow(["Reviews","Website Link"])
            for review in reviews: 
                writer.writerow([review.encode("utf-8"),response.url.encode("utf-8")]); 

         
        '''page = requests.get(response.url)
        parser = html.fromstring(page.content)
        xpath_reviews= '//div[@class ="user-review-content"]'
        xpath_body    = './/p//text()'
        reviews = parser.xpath(xpath_reviews)
        with open("review.txt",'w') as f:
            for review in reviews:
                body    = review.xpath(xpath_body)
                f.write(str(body))
                f.write("+++++++++++++++++\n")'''
    
    
if __name__ == '__main__':
       process = CrawlerProcess(get_project_settings())
       process.crawl(SinglepagespiderSpider)
       process.start()