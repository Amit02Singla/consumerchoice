from scrapy import Spider, Request
from lxml import etree
import json

from services.Hellopeter import Hellopeter


urlssss = []
class HellopeterURLCrawler(Spider):
    def __init__(self,category):
        self.url_list = []
        self.category = category
    def parsing(self, response):
        return self.crawl(response)
    def crawl(self, response):
        url = []
        urlnext = []
        servicelistnext = []
        servicelist= []
        data = json.loads(response.body)

        for urls in data["data"]:
            url.append("https://api-v3.hellopeter.com/businesses/"+urls["slug"]+"/reviews?include=author&p")
            servicelist.append(urls["name"])
        print("serviceList  ", len(servicelist), servicelist)
        print("URL ", len(url), url)
        i=0


        while i< len(url):
            crawler = Hellopeter(self.category, servicelist[i], url[i])
            yield Request(url=url[i], callback=crawler.parsing)
            # yield response.follow(url=url[i], callback=crawler.parsing)
            # print(url[i][j])
            i=i+1
        # next_page = response.xpath("//a[@class='frtn']/@href").extract()
        # if (len(next_page) > 0):
        #     if 'page' not in response.url:
        #         print next_page
        #     else:
        #         next_page = response.xpath("//a[@class='frtn'][2]/@href").extract()
        # if next_page is not None:
        #     if len(next_page)>0:
        #         next_page_url = "".join(next_page)
        #         if next_page_url and next_page_url.strip():
        #             yield response.follow(url=next_page_url, callback=self.parsing)
        #             # yield Request(url=next_page_url, callback=self.parsing)
