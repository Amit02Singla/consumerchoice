from model.Servicemodel import ServiceRecord
from utils.utils import getStarts
from lxml import etree
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
#TODO redo website
#URL https://www.macupdate.com/app/mac/52417/purevpn
class MacUpdate(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(MacUpdate,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        headings = []
        authors = []
        dates = []
        ratings1 = []

        print("review from macupdate.com")
        # nodes = response.xpath("//div[@id='reviews_comments_container']").extract();
        # for content in nodes:
        #     root = etree.HTML(content)
        #     print(content)
        #     if(len(root.xpath("/div/div[@class='yui3-u rcpb-content']/p[@class='rcpb-revcom-content']"))>0):
        #         reviews.append(root.xpath("/div/div[@class='yui3-u rcpb-content']/p[@class='rcpb-revcom-content']")[0])
        # print("reviews ", len(reviews), reviews)

        for node in response.xpath("//div[@id='reviews_comments_container']/div[@id='rc_644247']/div[@class='yui3-u rcpb-content']/p[@class='rcpb-revcom-content']"):
            reviews.append(node.xpath('string()').extract())
        ratings = response.xpath("//div/div[@class='yui3-u rcpb-content']/div/input/@value/@text()").extract()
        dates = response.xpath("//div/div[@class='yui3-u rcpb-content']/span[@class='rcpb-postdate']/text()").extract()
        headings = response.xpath("//div[@class='box col-12 review-title']/h4/text()").extract()
        authors = response.xpath("//div[@class='box col-12 review-info']/strong/span/text()").extract()
        website_name = response.xpath("//div[@class='wpcr3_item_name']/a/text()").extract()
        img_src = response.xpath("//div[@class='avatar']/img/@src").extract()
        print(" raaaaaa")
        #
        # for i in range(len(ratings)):
        #     if i != 0:
        #         del [ratings]
        print("Authors ", len(authors), authors)
        print("Rating ", len(ratings), ratings)
        print("Dates ", len(dates), dates)
        print("reviews ", len(reviews), reviews)
        print("websites ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates[item], authors[item],
                                         self.category, self.servicename, reviews[item], img_src, website_name)
            self.save(servicename1)

        # next_page = response.xpath("//div[@class ='navigator']/a[7]/@href").extract()
        # if next_page is not None:
        #     next_page_url = "".join(next_page)
        #     if next_page_url and next_page_url.strip():
        #         print(type(next_page_url))
        #         print(next_page_url)
        #         # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
        #         yield response.follow(next_page_url, callback=self.parsing)
        self.pushToServer()



