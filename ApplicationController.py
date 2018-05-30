from restapis import Login
from services.ServiceController import crawl_services
if __name__ == '__main__':
    urls = []
    urls.append({"ServiceName": "Expressvpn",
                 "Category": "VPN Service",
                 "url": "http://pickuphost.com/review/bluehost/"})
    crawl_services(urls)
