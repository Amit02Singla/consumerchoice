from utils import utils

final_json={}
class ServiceRecord(object):
    def __init__(self,url,rating,heading,date,author,category,service_name,reviews,img_src,website_name):
        super(ServiceRecord, self).__init__()
        self.url = url
        self.rating = rating
        self.heading = heading
        self.date = date
        self.author = author
        self.category = category
        self.service_name = service_name
        self.reviews = reviews
        self.img_src = img_src
        self.website_name = website_name

    def save(self):
        response = final_json[self.service_name]["response"]
        response.addRecord(self);

    def str11(self):
        store_data_dict = {}

        # datetime.datetime(2010, 2, 15, 0, 0)
        return {
            "absolute_url": self.url,
            "rating": utils.getStarts(self.rating),
            "review_title": self.heading,
            "reviewed_at": utils.convertDate(self.date),
            "reviewer_name": self.author,
            "category": self.category,
            "service_name": self.service_name,
            "review_text": self.reviews[0],
            "picture_urls": self.img_src,
            "website_name":self.website_name}
        #return json.dumps(store_data_dict["review"]).replace("/", "\\/")
if __name__ == '__main__':
    pass\
