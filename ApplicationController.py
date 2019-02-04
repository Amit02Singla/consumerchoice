from product.amazon.helpers import make_request
from services.siteservices.SiteServiceListController import crawl_services1
from utils.GoogleSearch import search

if __name__ == '__main__':
    # search([[15, "https://www.sadriya.com"], [16, "https://www.sadriya1.com"],
    #         [17, "https://www.sadriya2.com"], [14,
    #                                            "https://www.google.co.in"]],
    #        "http://localhost:3000/admin/categories/scrapping_websites")
    urls = []
    urls.append({"ServiceName": "Expressvpn",
                 "Category": "VPN Service",
                 "url": "https://www.sitejabber.com/search?page=34&q=dresses"})
    serviceName= 'https://sitejabber.com/'
    if ("www" in serviceName):
        serviceName = serviceName.split(".")[1]
    else:
        serviceName = serviceName.split("/")[2]
    crawl_services1(urls, serviceName)
