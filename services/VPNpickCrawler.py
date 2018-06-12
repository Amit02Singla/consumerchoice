from model.Servicemodel import ServiceRecord
from lxml import etree


class VPNpickCrawler():
    def __init__(self):
        pass

 #TODO author and review count mismatch-- Done some error
    def crawl(self, response, category, servicename):
        reviews = []
        # https://vpnpick.com/reviews/expressvpn/
        authors = []
        dates = []
        ratings = []
        reviews = []
        data = response.xpath( "//div[@id='comments']/ol[@class='commentlist']/li").extract()
        # print("data",  data)
        for content in data:
            content = content.replace('<br>', '$')
            root = etree.HTML(content)
            reviews.append(root.xpath("//div/div[@class='commentmetadata']/div[@class='commenttext']/p/text()"))
            authors.append(str(root.xpath("//div/div[@class='comment-author vcard']/span[@class='fn']/span/text()")))
            if(len(root.xpath("//div/div[@class='comment-author vcard']/span[@class='ago']/text()"))>0):
                dates.append(str(root.xpath("//div/div[@class='comment-author vcard']/span[@class='ago']/text()")[0]))
            else:
                dates.append("")
        '''for node in response.xpath("//div[@id='comments']/ol[@class='commentlist']/li/div/div[@class='commentmetadata']/div[@class='commenttext']"):
            reviews.append(node.xpath('string()').extract());
        dates = response.xpath("//div[@class='comment-author vcard']/span[@class='ago']/text()").extract()
        authors =  response.xpath("//div[@id='comments']/ol[@class='commentlist']/li/div/div[@class='comment-author vcard']/span[@class='fn']/span")
        img_src =  response.xpath("//div[@class='thecontent']/p[1]/img[@class='alignright wp-image-3155']/@src").extract()'''
        website_name =  response.xpath("/html/head/meta[6]/@content").extract()
        # print("Reviews ", len(reviews), reviews)
        # print("Authors ", len(authors), authors)
        # print("Rating ", len(ratings), ratings)
        # print("Dates ", len(dates), dates)
        # print("img_src ", len(img_src), img_src)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, None, dates[item], authors[item], category,
                          servicename, reviews[item],None,website_name);
            servicename1.save()