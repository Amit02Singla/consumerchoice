from model.Servicemodel import ServiceRecord
from lxml import etree
#TODO REDO website : Done
# https://securethoughts.com/cyberghost-review/
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class SecureThoughts(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(SecureThoughts,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []

        print("review from securethoughts.com")
        # nodes = response.xpath("//div[@id='comments']/div[@class='comment list']").extract()
        # for content in nodes:
        #     content = content.replace('<p>',' ').replace('</p>',' ').replace('<br>',' ').strip()
        #     root = etree.HTML(content)
        #     reviews.append(root.xpath("//div/text()"))
        for node in response.xpath("//div[@id='comments']/div[@class='comment list']/div/p"):
            reviews.append(node.xpath('string()').extract());
        # ratings1 = response.xpath("//div[@class='box col-12 review-title']/meta[@itemprop='ratingValue']/@content").extract()
        dates = response.xpath("//div[@id='comments']/div[@class='comment list']/div/div[@class='comment-meta commentmetadata']/a/text()").extract()
        # headings = response.xpath("//div[@class='box col-12 review-title']/h4/text()").extract()
        authors1 = response.xpath("//div[@id='comments']/div[@class='comment list']/div/div[@class='comment-author vcard']").extract()
        website_name = "securethoughts.com"
        img_src = response.xpath("//div[@class='leftSide']/div[@class='ctasWrapper']/a[@class='linkToBrandWrap']/span[@class='rowContainer']/img[@class='logo']/@src").extract()
        authors = []
        for content in authors1:
            root  = etree.HTML(content)
            if(len(root.xpath("//cite[@class='fn']/a[@class='url']"))>0):
                authors.append(root.xpath("//cite[@class='fn']/a[@class='url']/text()")[0])
            else:
                authors.append(root.xpath("//cite[@class='fn']/text()")[0])
        print("reviews ", len(reviews), reviews)
        print("dates ", len(dates), dates)
        print("authors ", len(authors), authors)
        print("")

        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None, None, dates[item], authors[item],
                                         self.category, self.servicename, reviews[item], None, website_name)
            self.save(servicename1)

        #  = response.xpath("//div[@class ='navigator']/a[7]/@href").extract()
        # if  is not None:
        #     _url = "".join()
        #     if _url and _url.strip():
        #         print(type(next_page_url))
        #         print(next_page_url)
        #         # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
        #         yield response.follow(next_page_url, callback=self.parsing)
        self.pushToServer()




