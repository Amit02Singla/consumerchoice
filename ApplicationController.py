from restapis import Login
from services.ServiceController import crawl_services
if __name__ == '__main__':
    urls = []
    urls.append({"ServiceName": "Expressvpn",
                 "Category": "VPN Service",
                 "url": "https://vpnpick.com/reviews/expressvpn/"})
    crawl_services(urls)