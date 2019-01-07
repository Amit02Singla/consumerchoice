from model.Servicemodel import ServiceRecord
from lxml import etree
#URL https://www.forexbrokerz.com/brokers/binance-review
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class ForexbrokerzCrawler(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(ForexbrokerzCrawler,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        headings = []
        dates = []
        ratings = []
        authors = []
        data = response.xpath("//div[@id='tab_friends']/div[@class='review']").extract()
        for content in data:
            root = etree.HTML(content)
            reviews.append(''.join(root.xpath('//div[@class="review_top"]/p/text()')).strip())
            if(len(root.xpath("//div[@class='review']/div[@class='review_top']/span/h3/a/text()"))>0):
                headings.append(root.xpath("//div[@class='review']/div[@class='review_top']/span/h3/a/text()")[0])
            else:
                headings.append("")
            if (len(root.xpath("//div[@class='review_details']/span/text()")) > 0):
                dates.append(root.xpath("//div[@class='review_details']/span/text()")[0])
            else:
                dates.append("")
            if (len(root.xpath("//div[@class='review_details']/div/div/a/text()")) > 0):
                ratings.append(root.xpath("//div[@class='review_details']/div/div/a/text()")[0])
            else:
                ratings.append("")
            if (len(root.xpath("//div[@class='review_details']/span/strong/text()")) > 0):
                authors.append(root.xpath("//div[@class='review_details']/span/strong/text()")[0])
            else:
                authors.append("")


        img_src = response.xpath("//div[@class='center_box borker_box  wbord']/div[@class='broker_img_container']/img/@src").extract()[0]
        img_src = 'https://www.forexbrokerz.com'+img_src
        website_name = response.xpath("").extract()[0]
        website_name = "forexbrokerz.com"
        print("reviews ", len(reviews), reviews)
        print("ratings ", len(ratings), ratings)
        print("headings ", len(headings), headings)
        print("dates ", len(dates), dates)
        print("authors ", len(authors), authors)
        # print("img_src ", len(img_src), img_src)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates[item], authors[item], self.category,
                          self.servicename, reviews[item], "",website_name);
            self.save(servicename1)
        self.pushToServer()
