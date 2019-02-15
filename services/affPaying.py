from model.Servicemodel import ServiceRecord
from lxml import etree
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
# http://www.affpaying.com/hotspot-shield-affiliate-program
class affPaying(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(affPaying,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        #
        for node in response.xpath("//dd[@class='s_content_wrap']/div[3]"):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@class='s_rate_mid']/span/meta[@itemprop='ratingValue']/@content").extract()
        dates = response.xpath("//div[@class='s_comment_date']/meta[@itemprop='datePublished']/@content").extract()
        authors = response.xpath("//div/dl[@class='s_comment']/h4/span/text()").extract()
        website_name = response.xpath("//div[@id='s_single_head_left']/div[@id='s_single_head_info']/p/a[@class='s_join_btn']/@href").extract()[0]
        print("Reviews ", len(reviews))
        print("Authors ", len(authors), authors)
        print("ratings ", len(ratings), ratings)

        print("Dates ", len(dates), dates)

        print("websites ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, dates[item], authors[item],
                                         self.category, self.servicename, reviews[item], None, website_name)
            self.save(servicename1)
        next_page = response.xpath("//div[@class='comments-nav'][1]/a[@class='prev page-numbers']/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                yield response.follow(url=next_page_url, callback=self.parsing)
        self.pushToServer()


