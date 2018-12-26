from product.amazon.helpers import make_request
from services.siteservices.SiteServiceListController import crawl_services1
from utils.GoogleSearch import search

if __name__ == '__main__':
    # search("85","BitCoin","[u'https://www.coinjabber.com/site/coinmama.com']","http://52.0.49.246/api/v1/categories/85/scrapping_websites")
    urls = []
    urls.append({"ServiceName": "Expressvpn",
                 "Category": "VPN Service",
                 "url": "https://www.10bestonline.com/top_10_best_online_dating_reviews/SilverSingles_customer_reviews/"})

    crawl_services1(urls)
