from model.Servicemodel import ServiceRecord
from lxml import etree
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class FreeDatingHelperCrawler(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(FreeDatingHelperCrawler,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        # http://www.freedatinghelper.com/reviews/fortyplus-singles/

        authors = []
        reviews=[]
        ratings =[]
        data = response.xpath("//li/article[@class='comment-body clearfix']/div[@class='comment_postinfo']").extract()

        for content in data:
            content = content.replace('<br>', '')
            content = content.replace('<p>','').replace('</p>','')

            root = etree.HTML(content)
            if(len(root.xpath("//div/span[@class='fn']/span/text()"))>0):
                authors.append(root.xpath("//div/span[@class='fn']/span/text()"))
            else:
                authors.append("")
            if(len(root.xpath("//div/div[@class='comment_area']/div[@class='comment-content clearfix']/div/span/text()"))>0):
                reviews.append(root.xpath("//div/div[@class='comment_area']/div[@class='comment-content clearfix']/div/span/text()"))
            else:
                reviews.append("")
            # if(len(root.xpath("//li/article[@class='comment-body clearfix']/div[@class='comment_postinfo']/div[2]/table[@class='ratings']/tbody/tr/td[@class='rating_value']/div/text()"))>0):
            #     ratings.append(root.xpath("//li/article[@class='comment-body clearfix']/div[@class='comment_postinfo']/div/table[@class='ratings']/tbody/tr/td[@class='rating_value']/div/text()"))
            # el
            if(len(root.xpath("//div[2]/table[@class='ratings']/tr/td[@class='rating_value']/div/span/text()"))>0):
                ratings.append(root.xpath("//div[2]/table[@class='ratings']/tr/td[@class='rating_value']/div/span/text()"))
            else:
                ratings.append("")
            website_name = root.xpath(
                "//div[2]/div[@class='comment_area']/center/a[@class='small-button smallorange']/@href").extract()

        # if(len(authors)>0):
        #     authors = authors[0]
        # if len(reviews)>0:
        #     reviews = reviews[0]
        print("Reviews ", len(reviews[0]), reviews)
        # print("Headings ", len(headings), headings)
        print("Authors ", len(authors[0]), authors)
        print("Rating ", len(ratings[0]), ratings)
        # print("Dates ", len(dates), dates)
        print("website ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, None, authors[item],
                                         "", self.servicename, reviews[item], None, website_name)
            self.save(servicename1)
        self.pushToServer()