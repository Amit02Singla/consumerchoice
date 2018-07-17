from scrapy import Spider, Request
from lxml import etree
import ast
import json
from services.consumerAffairsCrawler import consumerAffairsCrawler


urlssss = []
class ConsumerAffairsURLCrawler(Spider):
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

        data1 = response.body.split('(',1)
        data1 = data1[1].replace(');','')

        data = json.loads(data1)
        for urls in data["results"]:
            url.append(urls["url"])
            servicelist.append(urls["title"])

        servicelist = map(lambda foo: foo.replace('<b>', ' ').replace('</b>',''), servicelist)
        print("serviceList  ", len(servicelist), servicelist)
        print("URL ", len(url), url)
        i=0
        # while i< len(url):
        #     crawler = consumerAffairsCrawler(self.category, servicelist[i], url[i])
        #     yield Request(url=url[i], callback=crawler.parsing)
        #     # yield response.follow(url=url[i]+'reviews/', callback=crawler.parsing)
        #     # print(url[i][j])
        #     i=i+1
        next_page1 = response.url
        if 'start' not in response.url:

            next_page = response.url + "&start=10"

        else:
            c = next_page1.split('&')
            count = int(c[15].replace('start=', '0')) + 10
            if count < int(data["cursor"]["estimatedResultCount"]):
                next_page = next_page1.replace(c[15], 'start=' + str(count))
            else:
                next_page=""
        if next_page is not None:
            if len(next_page) > 0:
                next_page_url = "".join(next_page)
                if next_page_url and next_page_url.strip():
                    # print(next_page_url)
                    yield Request(url=next_page_url, callback=self.parsing, dont_filter=True)
                # yield response.follow(next_page_url, callback=self.parsing)







