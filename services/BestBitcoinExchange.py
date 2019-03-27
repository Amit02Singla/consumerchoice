from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request
from lxml import etree
from product.amazon.helpers import make_request
from utils.utils import getStarts
# TODO Paging pending because of #
# http://www.bestbitcoinexchange.net/en/bittrex-com/
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class BestBitcoinExchange(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(BestBitcoinExchange,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        reviews1 = []

        root = etree.HTML(response)
        for node in root.xpath(
                ".//div[@class='box']/ol[@class='comment-list']/li/div"):
            reviews1.append(node.xpath('string()'))
        i = 0
        rev = []
        authors = []
        dates = []
        while (i < len(reviews1)):
            revs = (reviews1[i].replace('\t\t\n\t\n\t\n\t', '|'))
            rev = revs.split("|")
            dateAuthor = rev[0].split(",")
            authors.append(dateAuthor[0].strip())
            dates.append(dateAuthor[1])
            reviews.append([rev[1]])
            i = i + 1
        website_name1 = self.link["url"].split("/")
        website_name1 = (website_name1[len(website_name1) - 2]).split("-")
        website_name = 'https://' + website_name1[0] + "."+website_name1[1]
        # img_src = root.xpath("//div[@class='box left']/div[@class='post-image-container']/img[@class='post-image provider-logo']/@src").extract()
        # parsedURL = urlparse(website_name)
        name = "bestbitcoinexchange.net"
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
            servicename1 = ServiceRecord(self.link["url"], None, None, dates[item], authors[item], self.category,
                                         self.servicename, reviews[item], None, website_name, name)
            self.save(servicename1)
        next_page = root.xpath(
            ".//div[@class='box']/nav[@id='comment-nav-below']/div[@class='nav-previous']/a/@href")
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url)
                r = make_request(next_page_url, False, False)
                self.crawl(r.content)
                # yield Request(next_page_url, callback=self.parsing)
                # yield response.follow(next_page_url, callback=self.parsing)
        self.pushToServer()





