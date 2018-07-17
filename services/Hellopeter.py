from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request


from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
import json
class Hellopeter(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(Hellopeter,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        reviews1 = []
        headings =[]
        ratings = []
        authors = []
        dates = []

        data = json.loads(response.body)
        for content in data["data"]:
            headings.append(content["title"])
            reviews.append(content["content"])
            ratings.append(content["final_rating"])
            dates.append(content["created_at"])
            authors.append(content["author_display_name"])

        website_name = "hellopeter.com"

        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, headings[item], dates[item], authors[item], self.category,
                                         self.servicename, [reviews[item]], None, website_name)
            self.save(servicename1)
        self.pushToServer()





