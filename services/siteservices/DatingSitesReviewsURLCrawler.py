from scrapy import Spider, Request
from lxml import etree

from services.DatingSitesReviewsCrawler import DatingSitesReviewsCrawler


urlssss = []
class DatingSitesReviewsURLCrawler(Spider):
    def __init__(self,category):
        self.url_list = []
        self.category = category
    def parsing(self, response):
        return self.crawl(response)
    def crawl(self, response):
        url = []
        urlnext = []
        servicelistnext = []
        serviceList= []

        url = response.xpath("//div[@class='block-center-content']/div/a/@href").extract()
        servicelist = response.xpath("//div[@class='block-center-content']/div/a").extract()
        for content in servicelist:
            content = content.replace('<span class="b">',"")
            content = content.replace('</span>', "")
            root = etree.HTML(content)
            serviceList.append(root.xpath("//a/text()")[0])



        print("serviceList  ", len(serviceList), serviceList)
        print("URL ", len(url), url)
        i=0


        while i< len(url):
            crawler = DatingSitesReviewsCrawler(self.category, servicelist[i], url[i])
            yield Request(url=url[i], callback=crawler.parsing)
            # yield response.follow(url=url[i], callback=crawler.parsing)
            # print(url[i][j])
            i=i+1
        next_page = response.xpath("//div[@class='uk-width-1-1']/ul[@class='uk-pagination']/li[10]/a/@href").extract()
        if next_page is not None:
            if len(next_page)>0:
                next_page_url = "".join(next_page)
                if next_page_url and next_page_url.strip():
                    yield Request(url=next_page_url, callback=self.parsing)
