from model.Servicemodel import ServiceRecord
from lxml import etree
class FreeDatingHelperCrawler():
    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        # http://www.freedatinghelper.com/reviews/fortyplus-singles/
        #TODO Need to check pick only first review: Refer Sandy
        authors = []
        reviews=[]
        ratings =[]
        data = response.xpath("//section[@id='comment-wrap']/ol[@class='commentlist clearfix']").extract()
        for content in data:
            # content = content.replace('<br>', '$')
            root = etree.HTML(content)
            if(len(root.xpath("//li/article[@class='comment-body clearfix']/div[@class='comment_postinfo']/div/span[@class='fn']/span/text()"))>0):
                authors.append(root.xpath("//li/article[@class='comment-body clearfix']/div[@class='comment_postinfo']/div/span[@class='fn']/span/text()")[0])
            else:
                authors.append("")
            if(len(root.xpath("//li/article[@class='comment-body clearfix']/div[@class='comment_postinfo']/div/div[@class='comment_area']/div[@class='comment-content clearfix']/div/span/p/text()"))>0):
                reviews.append(root.xpath("//li/article[@class='comment-body clearfix']/div[@class='comment_postinfo']/div/div[@class='comment_area']/div[@class='comment-content clearfix']/div/span/p/text()"))
            else:
                reviews.append("")
            if(len(root.xpath("//li/article[@class='comment-body clearfix']/div[@class='comment_postinfo']/div/table[@class='ratings']/tbody/tr/td[@class='rating_value']/div/text()"))>0):
                ratings = root.xpath("//li/article[@class='comment-body clearfix']/div[@class='comment_postinfo']/div/table[@class='ratings']/tbody/tr/td[@class='rating_value']/div/text()")
            else:
                ratings.append("")

        website_name= response.xpath("//html/head/meta[8]/@content").extract()[0]
        # print("Reviews ", len(reviews), reviews)
        # # print("Headings ", len(headings), headings)
        # print("Authors ", len(authors), authors)
        # print("Rating ", len(ratings), ratings)
        # # print("Dates ", len(dates), dates)
        # # print("Img_src ", len(img_src), img_src)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, None, authors[item],
                                         category, servicename, reviews[item], None, website_name)
            servicename1.save()