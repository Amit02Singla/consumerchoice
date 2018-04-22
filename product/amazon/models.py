#conn = psycopg2.connect(database=settings.database, host=settings.host, user=settings.user)
#cur = conn.cursor()


class ProductRecord(object):
    """docstring for ProductRecord"""
    def __init__(self, title, product_url, listing_url, price, primary_img, crawl_time):
        super(ProductRecord, self).__init__()
        self.title = title
        self.product_url = product_url
        self.listing_url = listing_url
        self.price = price
        self.primary_img = primary_img
        self.crawl_time = crawl_time

    def save(self):
        with open("output.text","a") as f:    
            f.write("@@@@@@@@@@@@@@@@@@@@@@@")
            f.write(self.product_url)
            f.write("\n")
            f.write(self.primary_img)
            f.write("\n")
            f.write(str(self.price))
            f.write("\n")
            f.write(self.reviews)
            f.write("\n")
            f.write(self.ratings)
            f.write("\n")
            f.write(self.title)
            f.write("\n")
            f.write("\n")
            f.write("\n")
            f.write("\n")
            f.write("\n")


if __name__ == '__main__':
    pass