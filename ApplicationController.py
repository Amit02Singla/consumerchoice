from product.amazon.helpers import make_request
from services.siteservices.SiteServiceListController import crawl_services1
if __name__ == '__main__':
    urls=[]
    urls.append({"ServiceName": "Expressvpn",
                 "Category": "VPN Service",
                 "url": "http://www.bestbitcoinexchange.net/?s=review+bitcoin"})

    crawl_services1(urls)

