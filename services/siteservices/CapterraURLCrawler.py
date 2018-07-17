from scrapy import Spider, Request
from lxml import etree
import json
from services.CapterraCrawler import CapterraCrawler


urlssss = []
class CapterraURLCrawler(Spider):
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
        for urls in data["webPages"]["value"]:
            url.append(urls["url"])
            servicelist.append(urls["name"])

        servicelist = map(lambda foo: foo.replace('<b>', ' ').replace('</b>',''), servicelist)
        print("serviceList  ", len(servicelist), servicelist)
        print("URL ", len(url), url)
        i=0


        # while i< len(url):
        #     crawler = CapterraCrawler(self.category, servicelist[i], url[i])
        #     yield Request(url=url[i], callback=crawler.parsing)
        #     # yield response.follow(url=url[i]+'reviews/', callback=crawler.parsing)
        #     # print(url[i][j])
        #     i=i+1
        next_page1 = response.url
        if 'offset=' in response.url:
            c= next_page1.split('&')
            count = int(c[3].replace('offset=','0'))+10
            if count < int(data["webPages"]["totalEstimatedMatches"]):
                next_page = next_page1.replace(c[3],'offset='+str(count))
                if next_page is not None:
                    next_page_url = "".join(next_page)
                    if next_page_url and next_page_url.strip():
                        print(type(next_page_url))
                        print(next_page_url)
                        yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
                        # yield response.follow(next_page_url, callback=self.parsing)






