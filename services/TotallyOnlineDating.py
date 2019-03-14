from model.Servicemodel import ServiceRecord
from lxml import etree
# http://www.totallyonlinedating.com/usa-online-dating-services/senior-dating-sites/seniorpeoplemeet.com-review.html
#Todo: redo
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class TotallyOnlineDating(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(TotallyOnlineDating,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        reviews1 = []
        headings = []
        authors = []
        ratings = []
        dates = []
        print("review from totallyonlinedating.com")
        node = response.xpath("//div/table[@class='showcomment']").extract()
        for content in node:
            root = etree.HTML(content)
            if len(root.xpath(".//tr/td[@class='contcomment']"))>0:
                reviews.append(root.xpath(".//tr/td[@class='contcomment']/text()"))
            else:
                reviews.append("")
            if(len(root.xpath(".//td[@class='contcomment']/b/text()"))>0):
                headings.append(root.xpath(".//td[@class='contcomment']/b/text()")[0])
            else:
                headings.append("")
            if (len(root.xpath(".//td[@class='commentid']/i/text()")) > 0):
                authors.append(root.xpath(".//td[@class='commentid']/i/text()")[0])
            else:
                authors.append("")
            if (len(root.xpath(".//td[@class='star']/img/@src")) > 0):
                ratings.append(len(root.xpath(".//td[@class='star']/img/@src")))
            else:
                ratings.append("")

        website_name = response.xpath("//tr/td[@class='centercolomnart']/center[1]/a//@href").extract()

        # http://www.totallyonlinedating.com/usa-online-dating-services/senior-dating-sites/seniorpeoplemeet.com-review.html
        # for node in response.xpath("//tr/td[@class='contcomment']"):
        #     reviews.append(node.xpath('string()').extract());
        # ratings = response.xpath("//div[@class='rating-md']/p/span/span[@itemprop='ratingValue']/@content").extract()
        # headings = response.xpath("//td[@class='contcomment']/b/text()").extract()
        # authors = response.xpath("//td[@class='commentid']/i/text()").extract()
        img_src =  response.xpath("//tr/td[@class='centercolomnart']/center[1]/a/img/@src").extract()

        dates = response.xpath("//div[@class='review-content']/div[@class='rating-md']/p/meta/@content").extract()
        # i=0


        print(" Ratings ", len(ratings), ratings)
        print(" Reviews ", len(reviews), reviews)
        print(" headings ", len(headings), headings)
        print(" authors ", len(authors), authors)
        print(" website_name ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], None, authors[item], self.category,
                          self.servicename, [''.join(reviews[item]).strip()],img_src[0],website_name[0]);
            self.save(servicename1)

        next_page = response.xpath("//div[@class='pagination-container']/ul[@class='pagination']/li[7]/a/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                #print(type(next_page_url))
                #print(next_page_url)
                # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
                yield response.follow(next_page_url, callback=self.parsing)
        self.pushToServer()