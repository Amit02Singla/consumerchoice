from model.Servicemodel import ServiceRecord
from lxml import etree
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler

# TODO: need to check last url
class HighYaCrawler(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(HighYaCrawler,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []

        print("review from HighYa.com  ", self.link["url"])
        # https://www.highya.com/coinbase-reviews
        for node in response.xpath(
                "//div[@class='left-col col-lg-8 col-lg']/div[@id='reviews']/ul[@class='no-list list-review']/li/span/div[@class='description']"):
            reviews.append(node.xpath('string()').extract());

        ratings = response.xpath(
            "//div[@id='reviews']/ul[@class='no-list list-review']/li/span/span[@class='review']/meta[@itemprop='ratingValue']/@content").extract()

        date = response.xpath(
                "//div[@id='reviews']/ul[@class='no-list list-review']/li/span/ul[@class='list-line options']").extract()
        dates = []
        for content in date:
            root = etree.HTML(content)
            isVerified = root.xpath("//li[last()]/@class")
            if(len(isVerified)==0):
                dates.append(root.xpath("//li[last()]/text()")[0])
            else:
                dates.append(root.xpath("//li[last()-1]/text()")[0])
        headings = response.xpath(
            "//div[@id='reviews']/ul[@class='no-list list-review']/li/span/h3[@class='title']/text()").extract()
        authors1 = response.xpath(
            "//div[@id='reviews']/ul[@class='no-list list-review']/li/span/ul[@class='list-line options']/li[1]").extract()
        authors = []
        for content in authors1:
            root = etree.HTML(content)
            if (root.xpath("//a/span")):
                authors.append(root.xpath("//a/span/text()")[0])
            else:
                authors.append(root.xpath("//span[@itemprop='name']/text()")[0])
        website_name1 = self.link["url"].split("/")
        website_name1 = (website_name1[len(website_name1) - 1]).split("-")
        website_name = 'https://' + website_name1[0] + ".com"
        name="highya.com"
        print("reviews  ", len(reviews))
        print ("website ", website_name);
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates[item], authors[item],
                                         self.category, self.servicename, reviews[item], None, website_name, name)
            self.save(servicename1)

        next_page = response.xpath("//div[@class='pagination']/a[@class='next']/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                yield response.follow(url=next_page_url, callback=self.parsing)
        self.pushToServer()
