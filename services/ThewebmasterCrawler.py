from model.Servicemodel import ServiceRecord

from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
from lxml import etree

class ThewebmasterCrawler(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(ThewebmasterCrawler,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        # https://www.thewebmaster.com/web-hosting/shared/justhost-reviews/
        for node in response.xpath("//div[@class='user-review-description-row']/div[@class='user-review-description-col']"):
            reviews.append(node.xpath('string()').extract())
        ratings =   response.xpath("//div[@class='user-review-summary-col'][2]/div[@class='reviewbar-wrapper']/div[@class='reviewbar skills']/div/p/strong/text()").extract()
        dates1 = response.xpath("//div[@class='user-review-summary-col'][1]/div[@class='user-review-date']/text()").extract()
        authors1 = response.xpath("//div[@class='user-review-summary-col'][1]/div[@class='user-review-name']/span/text()").extract()
        dates = []
        i=0
        while i< len(dates1):
            dates.append((dates1[i].split('Date:')[1]))
            i= i+1
        # authors = []
        # for content in authors1:
        #     root = etree.HTML(content)
        #     if len(root.xpath("//h4[@class='usrv-Header_Title']/text()"))>0:
        #         authors.append(root.xpath("//h4[@class='usrv-Header_Title']/text()")[0])
        #     else:
        #         authors.append("")
        website =  response.xpath("//div[@class='table-of-contents-wrapper']/div[@class='mt-4']/a[@class='dashboard-button']/@href").extract()
        website_name = "https://www.thewebmaster.com"+website[0]
        print(" reviews ", len(reviews))
        print(" ratings ", len(ratings))
        print(" authors ", len(authors1), authors1)
        print(" dates ", len(dates))
        print(" website ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None,dates[item], authors1[item], self.category,
                          self.servicename, reviews[item],None,website_name)
            self.save(servicename1)
        next_page = response.xpath(
               "//div[ @class ='pgn-Inner'] / a[@ class ='pgn-Next pgn-Prev-disabled']/@href").extract()
        if next_page is not None and "#" not in next_page:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                #print(type(next_page_url))
                #print(next_page_url, "    url")
                yield response.follow(url=next_page_url, callback=self.parsing)
        self.pushToServer()

