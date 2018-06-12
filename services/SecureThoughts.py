from model.Servicemodel import ServiceRecord
from lxml import etree
#TODO REDO website : Done
# https://securethoughts.com/cyberghost-review/
class SecureThoughts():
    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename

        print("review from securethoughts.com")
        for node in response.xpath("//div[@id='comments']/div[@class='comment list']/div/p"):
            reviews.append(node.xpath('string()').extract());
        # ratings1 = response.xpath("//div[@class='box col-12 review-title']/meta[@itemprop='ratingValue']/@content").extract()
        dates = response.xpath("//div[@id='comments']/div[@class='comment list']/div/div[@class='comment-meta commentmetadata']/a/text()").extract()
        # headings = response.xpath("//div[@class='box col-12 review-title']/h4/text()").extract()
        authors1 = response.xpath("//div[@id='comments']/div[@class='comment list']/div/div[@class='comment-author vcard']").extract()
        website_name = response.xpath("//div[@class='wpcr3_item_name']/a/text()").extract()
        img_src = response.xpath("//div[@class='leftSide']/div[@class='ctasWrapper']/a[@class='linkToBrandWrap']/span[@class='rowContainer']/img[@class='logo']/@src").extract()
        authors = []
        for content in authors1:
            root  = etree.HTML(content)
            if(len(root.xpath("//cite[@class='fn']/a[@class='url']"))>0):
                authors.append(root.xpath("//cite[@class='fn']/a[@class='url']/text()")[0])
            else:
                authors.append(root.xpath("//cite[@class='fn']/text()")[0])


        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, None, dates[item], authors[item],
                                         category, servicename, reviews[item], None, website_name)
            servicename1.save()

        #  = response.xpath("//div[@class ='navigator']/a[7]/@href").extract()
        # if  is not None:
        #     _url = "".join()
        #     if _url and _url.strip():
        #         print(type(next_page_url))
        #         print(next_page_url)
        #         # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
        #         yield response.follow(next_page_url, callback=self.parsing)




