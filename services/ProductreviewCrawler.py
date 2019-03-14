from model.Servicemodel import ServiceRecord

from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class ProductreviewCrawler(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(ProductreviewCrawler,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        print("review from productreview.com")
        # https://www.productreview.com.au/p/smart-fares.html
        for node in response.xpath("//div/div[@class=' col-md-9_35n']/div[@class='mb-4_1be']/span[@class=' break-word_qgH']/p[@class='mb-0_31F']/span"):
            reviews.append(node.xpath('string()').extract());
        rating =  response.xpath("//div/div[@class=' col-md-9_35n']/div[@class='mb-4_1be align-items-center_nNY flex-wrap_1Wl d-flex_b9D']/div[@class='mr-1_1hU flex-shrink-0_37K stars-container_2-J stars-container--medium_1hQ stars-container--dark_2gk']/@title").extract()
        headings = response.xpath("//div/div[@class=' col-md-9_35n']/h3[@class='mb-2_23n']/text()").extract()
        dates =  response.xpath("//div/div[@class=' col-md-9_35n']/div[@class='mb-4_1be align-items-center_nNY flex-wrap_1Wl d-flex_b9D']/span[@class=' text-muted_rsX font-size-sm_3PE']/span/time/@datetime").extract()
        authors = response.xpath("//span[@class='flex-shrink-0_37K text-link_1W2 textDecorationHover--underline_1Dc']/span[@class='align-items-center_nNY flex-wrap_1Wl d-inline-flex_2a2']/a/span[@class='cursor--pointer_1MN text-link_1W2 textDecorationHover--underline_1Dc']/text()").extract()
        img_src =  response.xpath("//div[@class='p-1_2ec align-items-center_nNY flex-column_36B justify-content-center_1IB relative_2e- d-flex_b9D card-body_10p']/img[@class=' img-fluid_a42']/@src").extract()
        website_name =  response.xpath("//div[@class='mb-3_2I3 overflow-x-hidden_15c card_134 card-full_3wf card-full-md_2gh']/div[@class='p-4_LM_ card-body_10p']/a/@href").extract()
        i=0
        ratings =[]
        while(i< len(rating)):
            ratings.append((rating[i].split(" ")[0]))
            i = i+1
        print("dates ", len(dates), dates)
        print(" Reviews ", len(reviews), reviews)
        print(" headings ", len(headings), headings)
        print(" authors ", len(authors), authors)
        print(" website_name ", len(website_name), website_name)
        print("image ", img_src)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates[item], authors[item], self.category,
                          self.servicename, reviews[item],img_src[0],website_name);
            self.save(servicename1)

        next_page = response.xpath("//div[@class='pagination-container']/ul[@class='pagination']/li[7]/a/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url)
                # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
                yield response.follow(next_page_url, callback=self.parsing)
        self.pushToServer()