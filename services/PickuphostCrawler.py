from model.Servicemodel import ServiceRecord


class PickuphostCrawler():
    def __init__(self):
        pass

    def crawl(self, response, category, servicename):
        reviews = []
        #http://pickuphost.com/review/bluehost/#customer_review_shap
        for node in response.xpath("//div[@class='one_rew']/div[@class='rewiwer_post']/span"):
            reviews.append(node.xpath('string()').extract());
        ratings =  response.xpath("//div[@class='col-md-12 avg_ratting_bg text-center']/div[@class='avg_ratting text-center']/text()").extract()
        headings = response.xpath("//div[@id='rew_replace_div']/div[@class='one_rew']/h4/b/text()").extract()
        dates = response.xpath("//div[@id='rew_replace_div']/div[@class='one_rew']/span[@class='rewiwer_data']/span[2]/text()").extract()
        authors = response.xpath("//div[@id='rew_replace_div']/div[@class='one_rew']/span[@class='rewiwer_data']/span[1]/text()").extract()
        #TODO Pagination Pending
        name = response.xpath("//div[@class='navbar-header']/a/@href").extract()
        website_name = name[0].split(".")[0].split("/")[-1]
        for item in range(1, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], headings[item], dates[item], authors[item], category,
                          servicename, reviews[item],"",website_name);
            servicename1.save()
        next_page = response.xpath("//div[@class='row']/div[@class='col-lg-8 col-lg-offset-3']/ul[@class='pagecount']/li[8]/a[@class='next page-numbers custom_page_link']/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url)
                # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
                yield response.follow(next_page_url, callback=self.parsing)
