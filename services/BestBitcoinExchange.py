from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from utils.utils import getStarts

# http://www.bestbitcoinexchange.net/en/bittrex-com/
class BestBitcoinExchange(Spider):
# TODO Paging pending because of #
    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        reviews1 = []
        self.category = category
        self.servicename = servicename

        for node in response.xpath(
                "//div[@class='box']/ol[@class='comment-list']/li/div"):
            reviews1.append(node.xpath('string()').extract());
        i = 0
        rev = []
        authors = []
        dates = []
        while (i < len(reviews1)):
            revs = (reviews1[i][0].replace("\t\t\n\t\n\t\n\t", "|"))
            rev = revs.split("|")
            dateAuthor = rev[0].split(",")
            authors.append(dateAuthor[0])
            dates.append(dateAuthor[1])
            reviews.append(rev[1])
            i = i + 1

        website_name = response.xpath("////head/meta[8]/@content").extract()
        # website_name2 = website_name1[0].("|")
        # website_name = []
        # website_name.append(website_name2[1])
        print("Reviews ", len(reviews), reviews)
        print("Authors ", len(authors), authors)
        # print("Rating ", len(ratings), ratings)
        print("Dates ", len(dates), dates)
        # # print("img_src ", len(img_src), img_src)
        print("websites ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, None, dates[item], authors[item], category,
                                         servicename, reviews[item], None, website_name)
            servicename1.save()
        next_page = response.xpath(
            "//div[@class='box']/nav[@id='comment-nav-below']/div[@class='nav-previous']/a/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url)
                yield Request(next_page_url, callback=self.parsing)
                # yield response.follow(next_page_url, callback=self.parsing)





