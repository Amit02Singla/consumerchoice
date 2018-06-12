from restapis import Login
from services.ServiceController import crawl_services
from product.ProductController import crawlAmazon
if __name__ == '__main__':
   #Login.crawling()
    urls=[]
    urls.append({"ServiceName": "Expressvpn",
                 "Category": "VPN Service",
                 "url": "https://www.virtualbanking.com/reviews/localbitcoins-review/"})
    crawl_services(urls)

