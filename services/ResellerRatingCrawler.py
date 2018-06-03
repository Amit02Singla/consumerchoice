from model.Servicemodel import ServiceRecord


class ResellerRatingCrawler():

    def __init__(self):
        pass

    def crawl(self, response, category, servicename):
        reviews = []
        print("Reviews from Resellerrating.com")
        # https://www.resellerratings.com/store/Nordvpn_com
        for node in  response.xpath("//div[@class='comment']/p[@class='review-body']/span"):
            reviews.append(node.xpath('string()').extract());
        headings =  response.xpath("//div[@class='comment']/p[@class='review-title']/span/text()").extract()
        dates =  response.xpath("//div[@class='comment']/div[@class='date fr']/span/text()").extract()
        ratings = response.xpath("//div[@class='rating siteStars fl']/span[@class='ratingLabel']/span[@class='bold']/text()").extract()
        authors =  response.xpath("//div[@class='user-column']/a[@class='rr-purple show-for-large']/text()").extract()
        website_name = response.xpath("//html/head/meta[15]/@content").extract()
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item],headings[item], dates[item], authors[item], category,
                          servicename, reviews[item], website_name);
            servicename1.save()
