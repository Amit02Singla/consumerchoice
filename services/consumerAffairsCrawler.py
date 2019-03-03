from model.Servicemodel import ServiceRecord
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class consumerAffairsCrawler(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(consumerAffairsCrawler,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        print("review from Consumeraffairs.com")
        # https://www.consumeraffairs.com/internet/godaddy.html
        for node in response.xpath("//div[@class='js-paginator-data']/div/div[@class='rvw-bd ca-txt-bd-2']/p[2]"):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div/div[@class='rvw__hdr']/div[@class='rvw__hdr-stat']/img/@data-rating").extract()
        # i=0
        # while(i < len(ratings)):
        #     ratings.pop(0)
        #     i=i+1
        #     if (i == 5):
        #         break;

        temp_dates = response.xpath("//div/div[@class='rvw-bd ca-txt-bd-2']/span[@class='ca-txt-cpt ca-txt--clr-gray']/text()").extract()
        dates = []
        for date in temp_dates:
            dates.append(date.split(":")[1])
        authors =  response.xpath("//div/div[@class='rvw-aut']/div[@class='rvw-aut__inf']/strong[@class='rvw-aut__inf-nm']/text()").extract()
        website_name = "consumeraffairs.com"
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings, None, dates[item], authors[item], self.category, self.servicename,
                                         reviews[item], None, website_name)
            self.save(servicename1)
        next_page = response.xpath("//div[@class='prf-lst']/nav[@class='prf-pgr js-profile-pager']/a[@class='ca-a-md "
                                   "ca-a-uprcs ca-a-blk prf-pgr__nxt js-profile-pager__next']/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url, "    url")
                yield response.follow(url=next_page_url, callback=self.parsing)
        self.pushToServer()
