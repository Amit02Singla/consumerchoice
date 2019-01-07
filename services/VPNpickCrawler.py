from model.Servicemodel import ServiceRecord
from lxml import etree

from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class VPNpickCrawler(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(VPNpickCrawler,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        # https://vpnpick.com/reviews/expressvpn/
        authors = []
        dates = []
        reviews1 = []
        reviews = []
        data = response.xpath( "//div[@id='comments']/ol[@class='commentlist']/li").extract()
        # print("data",  data)
        for content in data:
            content = content.replace('<br>', '')
            content = content.replace('<p>','')
            content = content.replace('</p>','')
            root = etree.HTML(content)
            reviews.append(root.xpath("//div/div[@class='commentmetadata']/div[@class='commenttext']/text()")[0])
            reviews = map(lambda foo: foo.replace('\r\n\t\t\t\t    ', ''), reviews)
            reviews = map(lambda foo: foo.replace('\n                ', ''), reviews)
            authors.append(str(root.xpath("//div/div[@class='comment-author vcard']/span[@class='fn']/span/text()")[0]))
            if(len(root.xpath("//div/div[@class='comment-author vcard']/span[@class='ago']/text()"))>0):
                dates.append(str(root.xpath("//div/div[@class='comment-author vcard']/span[@class='ago']/text()")[0]))
            else:
                dates.append("")
            # i=0
            # while i < len(reviews1):
            #     reviews.append(reviews1[i])
            #     i=  i+1
        '''for node in response.xpath("//div[@id='comments']/ol[@class='commentlist']/li/div/div[@class='commentmetadata']/div[@class='commenttext']"):
            reviews.append(node.xpath('string()').extract());
        dates = response.xpath("//div[@class='comment-author vcard']/span[@class='ago']/text()").extract()
        authors =  response.xpath("//div[@id='comments']/ol[@class='commentlist']/li/div/div[@class='comment-author vcard']/span[@class='fn']/span")
        img_src =  response.xpath("//div[@class='thecontent']/p[1]/img[@class='alignright wp-image-3155']/@src").extract()'''
        img_src = response.xpath("//div[@class='post-single-content box mark-links entry-content']/div[@class='thecontent']/p[1]/img[@class='alignright wp-image-3155']/@src").extract()[0]
        website_name =  response.xpath("//div[@class='post-single-content box mark-links entry-content']/div[@class='thecontent']/p[2]/a/@href").extract()[0]
        print("Reviews ", len(reviews), reviews)
        print("Authors ", len(authors), authors)
        print("img src ", img_src)
        print("Dates ", len(dates), dates)
        print("website ", website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, None, dates[item], authors[item], "",
                          self.servicename, [reviews[item]],img_src,website_name);
            self.save(servicename1)
        self.pushToServer()