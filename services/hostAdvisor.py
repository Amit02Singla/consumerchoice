from model.Servicemodel import ServiceRecord
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler

class hostAdvisor(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(hostAdvisor,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        # https://www.hostadvisor.com/reviews/shared-web-hosting/bluehost
        for node in response.xpath("//div[@class='textHolder']/div[2]/p"):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@class='textHolder']/div/span/meta[@itemprop='ratingValue']/@content").extract()
        # dates = response.xpath("//div[@class='review-mid']/p/text()").extract()
        headings = response.xpath("//div[@class='textHolder']/h5/text()").extract()
        #img_src = response.xpath("//div[@class='user-img ']/img/@src").extract()
        authors = response.xpath("//div[@class='hidden-xs']/p[1]/text()").extract()
        website_name = response.xpath("//html/head/title/text()").extract()[0].split("-")[1]
        authors = map(lambda s: s.strip(), authors)
        authors = list(filter(None, authors))
        # print("Reviews ", len(reviews))
        # print("Authors ", len(authors), authors)
        # print("ratings ", len(ratings), ratings)
        #
        # print("heading ", len(headings), headings)
        #
        # print("websites ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], None, authors[item],
                                         "", self.servicename, reviews[item], None, website_name)
            self.save(servicename1)

        next_page = response.xpath("//div[@class='reviewBlock']/nav[@class='text-center']/ul[@class='pagination']/li[21]/a/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                yield response.follow(url=next_page_url, callback=self.parsing)
        self.pushToServer()


