from restapis import Login
from services.ServiceController import crawl_services
if __name__ == '__main__':
    urls = []
    urls.append({"ServiceName": "Expressvpn",
                 "Category": "VPN Service",
                 "url": "https://www.reviewcentre.com/Dating-Sites/Elite-Singles-www-elitesingles-co-uk-www-hospiconsultant-com-reviews_3802989#Reviews"})
    crawl_services(urls)