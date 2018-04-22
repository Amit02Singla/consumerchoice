from model.Servicemodel import ServiceRecord

class tbwhsCrawler():
    def __init__(self):
        pass
    #TODO site pending
    def crawl(self, response,category,servicename):
        reviews = []
        # https://tbwhs.com/fatcow-web-hosting-reviews/
        for node in response.xpath(''):
            reviews.append(node.xpath('string()').extract());
        ratings =
        dates =
        headings =
        authors =
        website_name =
        for item in range(1, len(reviews)):
            servicename1 = ServiceRecord(response.url,ratings[item],headings[item],dates[item],authors[item],category,servicename,reviews[item],"",website_name);
            servicename1.save()