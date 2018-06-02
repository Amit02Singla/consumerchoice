from model.Servicemodel import ServiceRecord
from utils.utils import getStarts

class BestDatingReviews():
    def __init__(self):
        pass
    def parsing(self, response):
        return self.crawl(response,self.category,self.servicename)

    def crawl(self, response, category, servicename):
        reviews = []
        self.category = category
        self.servicename = servicename
        print("review from blackpeoplemeet.pissedconsumer.com")
        for node in response.xpath("//div[@class='mid_left']/div[@class='mid_left_site']/div[@class='latest_reviews_a']/div[@class='latest_reviews_content']/div"):
            reviews.append(node.xpath('string()').extract());
        ratings1 = response.xpath("//div[@class='mid_left']/div[@class='mid_left_site']/div[@class='latest_reviews_a']/div[@class='latest_reviews_content']/font/img/@src").extract()
        dates1 = response.xpath("//div[@class='mid_left']/div[@class='mid_left_site']/div[@class='latest_reviews_a']/div[@class='latest_reviews_content']/font/span[1]/text()").extract()
        headings = response.xpath("//div[@class='mid_left']/div[@class='mid_left_site']/div[@class='latest_reviews_a']/div[@class='latest_reviews_content']/font/a/text()").extract()
        # authors = response.xpath("//div[@class='cust_review']/table/tbody/tr[3]/td[@class='customer']").extract()
        website_name = response.xpath("//div[@class='wpcr3_item_name']/a/text()").extract()
        # img_src = response.xpath("//div[@id='comments']/ul[@class='comment-list']/li/article/footer[@class='comment-meta']/div[@class='comment-author vcard']/img[@class='avatar avatar-74 photo']/@src").extract()
        sum = 0
        c = 0
        ratings = []
        dates1 = map(lambda foo: foo.replace(u'\xa0', u''), dates1)
        dates1 = map(lambda foo: foo.replace('By', ''), dates1)
        dates = []
        dates2 = []
        authors = []
        authorsCount = 0
        # authors = map(lambda foo: foo.replace('By', ''), authors)
        while authorsCount < len(dates1):
            authorDetails = dates1[authorsCount].split('|')
            authors.append(authorDetails[0])
            dates.append(authorDetails[1])
            authorsCount = authorsCount + 1
        authorsCount = 0
        while authorsCount < len(dates):
            authorDetails = dates1[authorsCount].split('      ')
            dates2.append(authorDetails[1])
            authorsCount = authorsCount + 1

        i = 0
        while i < len(ratings1):
            star = getStarts(ratings1[i])
            if(star == '01.'):
                ratings.append(5)
            else :
                ratings.append(0)
            i = i + 1

        ratings2 = []
        for i in range(len(ratings)):
            if i % 5 != 0 and i != 0:
                sum = sum + int(ratings[i])
            else :
                if i!=0:
                    c= sum/5.0
                    ratings2.append(str(round(c,2)))
                sum = 0
                sum = sum + int(ratings[i])
        c = sum / 5.0
        ratings2.append(str(round(c,2)))
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings2[item], headings[item], dates2[item], authors[item],
                                         category, servicename, reviews[item], None, website_name)
            servicename1.save()

        next_page = response.xpath("//div[@class='mid_left']/div[@class='mid_left_site']/div[@class='viciao']/div[@class='page_cut']/a[@class='cur_pageva']/@href").extract()
        if next_page is not None:
            next_page_url = "".join(next_page)
            if next_page_url and next_page_url.strip():
                print(type(next_page_url))
                print(next_page_url)
                # yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
                yield response.follow(next_page_url, callback=self.parsing)





