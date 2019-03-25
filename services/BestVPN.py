from model.Servicemodel import ServiceRecord
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
# https://www.bestvpn.com/expressvpn-review/
class BestVPN(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(BestVPN,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        # https://www.bestvpn.com/expressvpn-review/
        print("https://www.bestvpn.com/     ", self.link["url"])
        for node in response.xpath("//ol[@class='post-comments']/li[@class='comment']/p"):
            reviews.append(node.xpath('string()').extract());
        # ratings = "8.2"
        dates = response.xpath("//ol[@class='post-comments']/li[@class='comment']/header/div[@class='mr-auto']/div[@class='comment-author']/div/span/em/text()").extract()
        authors = response.xpath("//ol[@class='post-comments']/li[@class='comment']/header/div[@class='mr-auto']/div[@class='comment-author']/div/h5/text()").extract()
        if(len(response.xpath("//a[@class='logo-link']/img[@class='provider-logo']/@src"))>0):
            img_src = response.xpath("//a[@class='logo-link']/img[@class='provider-logo']/@src").extract()[0]
        else:
            img_src = ""
        website_name= ""
        if ("expressvpn" in self.link["url"]):
            website_name = "https://www.expressvpn.com"
        elif ("nordvpn" in self.link["url"]):
            website_name ="https://nordvpn.com"
        elif ("cyberghost" in self.link["url"]):
            website_name = "https://www.cyberghostvpn.com"
        elif ("ipvanish" in self.link["url"]):
            website_name = "https://www.ipvanish.com"
        elif ("privatevpn" in self.link["url"]):
            website_name = "https://privatevpn.com"
        elif ("vyprvpn" in self.link["url"]):
            website_name = "https://www.vyprvpn.com"
        elif ("protonvpn" in self.link["url"]):
            website_name = "https://protonvpn.com"
        elif ("privateinternetaccess" in self.link["url"]):
            website_name = "https://www.privateinternetaccess.com"
        elif ("hotspotshield" in self.link["url"]):
            website_name = "https://www.hotspotshield.com"
        elif ("vpnunlimited" in self.link["url"]):
            website_name = "https://www.vpnunlimitedapp.com"
        name = "bestvpn.com"
        print("Reviews ", len(reviews))
        print("Authors ", len(authors), authors)
        print("img_src ", len(img_src), img_src)

        print("Dates ", len(dates), dates)

        print("websites ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, None,None, dates[item], authors[item], self.category,
                          self.servicename, reviews[item], img_src,website_name, name);
            self.save(servicename1)

        custom_url =""
        if("expressvpn" in self.link["url"]):
            custom_url = "https://www.bestvpn.com/api/get_comments/review/6/?start=4&count=10000&lang=en"
        elif ("nordvpn" in self.link["url"]):
            custom_url = "https://www.bestvpn.com/api/get_comments/review/5/?start=4&count=10000&lang=en"
        elif ("cyberghost" in self.link["url"]):
            custom_url = "https://www.bestvpn.com/api/get_comments/review/9/?start=4&count=10000&lang=en"
        elif ("ipvanish" in self.link["url"]):
            custom_url = "https://www.bestvpn.com/api/get_comments/review/107/?start=4&count=10000&lang=en"
        elif ("privatevpn" in self.link["url"]):
            custom_url = "https://www.bestvpn.com/api/get_comments/review/10/?start=4&count=10000&lang=en"
        elif ("vyprvpn" in self.link["url"]):
            custom_url = "https://www.bestvpn.com/api/get_comments/review/61/?start=4&count=10000&lang=en"
        elif ("protonvpn" in self.link["url"]):
            custom_url = "https://www.bestvpn.com/api/get_comments/review/17/?start=4&count=10000&lang=en"
        elif ("privateinternetaccess" in self.link["url"]):
            custom_url = "https://www.bestvpn.com/api/get_comments/review/30/?start=4&count=10000&lang=en"
        elif ("hotspotshield" in self.link["url"]):
            custom_url = "https://www.bestvpn.com/api/get_comments/review/16/?start=4&count=10000&lang=en"
        elif ("vpnunlimited" in self.link["url"]):
            custom_url = "https://www.bestvpn.com/api/get_comments/review/135/?start=4&count=10000&lang=en"
        # next_page = response.xpath("//div[@class='comments-nav'][1]/a[@class='prev page-numbers']/@href").extract()
        if custom_url is not "":
            next_page_url = custom_url
            if next_page_url and next_page_url.strip():
                yield response.follow(url=next_page_url, callback=self.parsing)
        self.pushToServer()
