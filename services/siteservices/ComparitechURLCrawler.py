from scrapy import Spider, Request
from lxml import etree
from product.amazon.helpers import make_request
from services.CompariTech import CompariTech


urlssss = []
class ComparitechURLCrawler():
    def __init__(self,category):
        self.url_list = []
        self.category = category
    def parsing(self, response):
        return self.crawl(response)
    def crawl(self, response):
        servicelist= []
        root = etree.HTML(response)
        url = root.xpath(".//div[@class='col span_1_of_2 grid-item']/a/@href")
        for content in url:
            c= content.split('/')
            servicelist.append(c[len(c)-2])


        print("serviceList  ", len(servicelist), servicelist)
        print("URL ", len(url), url)
        i=0


        while i< len(url):
            crawler = CompariTech(self.category, servicelist[i], url[i])
            # yield Request(url=url[i], callback=crawler.parsing)
            r=  make_request(url[i], False,False)
            crawler.crawl(r.content)
            # print(url[i][j])
            i=i+1
        next_page = root.xpath(".//div[@class='pagination-container clearfix']/div[@class='pages']/a[@class='next page-numbers']/@href")
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                r = make_request(next_page_url, False, False)
                self.crawl(r.content)
