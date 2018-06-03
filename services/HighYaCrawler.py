from model.Servicemodel import ServiceRecord
from lxml import etree


class HighYaCrawler():
    def __init__(self):
        pass

    def parsing(self, response):
        return self.crawl(response, self.category, self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        # print("review from HighYa.com")
        # https://www.highya.com/coinbase-reviews
        # TODO : 2- Auther need to extract: Authors done some other error coming up
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
        # TODO some times auther name structure differ not anchor tag need to check
        authors1 = response.xpath(
            "//div[@id='reviews']/ul[@class='no-list list-review']/li/span/ul[@class='list-line options']/li[1]").extract()
        authors = []
        for content in authors1:
            root = etree.HTML(content)
            if (root.xpath("//a/span")):
                authors.append(root.xpath("//a/span/text()"))
            else:
                authors.append(root.xpath("//span[@itemprop='name']/text()"))
        website_name = response.xpath("//html/head/meta[7]/@content").extract()

        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates[item], authors[item],
                                         category, servicename, reviews[item], None, website_name)
            servicename1.save()

        next_page = response.xpath("//div[@class='pagination']/a[@class='next']/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                yield response.follow(url=next_page_url, callback=self.parsing)
