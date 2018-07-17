from model.Servicemodel import ServiceRecord
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class yelpCrawler(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(yelpCrawler,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        # https://www.yelp.com/biz/fatcow-burlington
        for node in response.xpath('//div[@class="review-wrapper"]/div[@class="review-content"]/p'):
            reviews.append(node.xpath('string()').extract())

        ratings =  response.xpath("//div[@class='biz-rating biz-rating-large clearfix']/div/div/@title").extract()
        dates =  response.xpath("//div[@class='biz-rating biz-rating-large clearfix']/span[@class='rating-qualifier']/text()").extract()
        authors =  response.xpath("//div[@class='media-story']/ul[@class='user-passport-info']/li[@class='user-name']/a[@id='dropdown_user-name']/text()").extract()
        website_name =  response.xpath("//html/head/meta[6]/@content").extract()[0]
        dates = map(lambda foo: foo.replace('\n        ', ''), dates)
        dates = map(lambda foo: foo.replace('\n    ', ''), dates)
        print(" Ratings ", len(ratings))
        print("dates ", len(dates))
        print(" Reviews ", len(reviews))
        # print(" headings ", len(headings), headings)
        print(" authors ", len(authors))
        print(" website_name ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url,ratings[item],None,dates[item],authors[item],"",self.servicename,reviews[item],"",website_name);
            self.save(servicename1)

        next_page = response.xpath("//div[@class='arrange_unit']/a[@class='u-decoration-none next pagination-links_anchor']/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url, "    url")
                yield response.follow(url=next_page_url, callback=self.parsing)
        self.pushToServer()
