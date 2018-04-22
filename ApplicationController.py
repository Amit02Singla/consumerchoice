from restapis import Login
from services.ServiceController import crawl_services
if __name__ == '__main__':
    #Login.getUrl()
    urls = [];
    urls.append({"ServiceName": "NordVPN",
                 "Category": "Hosting Service",
                 "url": "https://www.resellerratings.com/store/Nordvpn_com"})
    '''urls.append({"ServiceName": "NordVPN",
                 "Category": "VPN Service",
                "Category":"Hosting Service",
                "url": "https://www.whoishostingthis.com/hosting-reviews/bluehost/"})
    urls.append({"ServiceName":"zoosk.compy",
                "Category":"Dating site",
                "url": "https://www.sitejabber.com/reviews/zoosk.com"})
    urls.append({"ServiceName": "Hostgator",
                 "Category": "Hosting Service",
                 "url": "https://hostingfacts.com/hosting-reviews/hostgator-wordpress-managed/"})
    urls.append({"ServiceName": "GoDaddy.com",
                 "Category": "Hosting Service",
                 "url": "https://hostadvice.com/hosting-company/godaddy-reviews/"})
    urls.append({"ServiceName": "Expressvpn",
                 "Category": "VPN Service",
                 "url": "https://www.bestvpn.com/expressvpn-review/"})
    urls.append({"ServiceName": "NordVPN",
                 "Category": "VPN Service",
                 "url": "https://www.resellerratings.com/store/Nordvpn_com"})
    urls.append({"ServiceName": "Nordvpn",
                 "Category": "VPN Service",
                 "url": "https://www.capterra.com/p/166743/NordVPN/"})
    urls.append({"ServiceName": "Nordvpn",
                 "Category": "VPN Service",
                 "url": "https://bestcompany.com/vpn/company/nordvpn"})
    urls.append({"ServiceName": "Binance",
                 "Category": "Cryptocurrency Excahnges",
                 "url": "https://www.forexbrokerz.com/brokers/binance-review"})

    urls.append({"ServiceName": "Expressvpn",
                 "Category": "VPN Service",
                 "url": "https://www.sitejabber.com/reviews/expressvpn.com"})
    urls.append({"ServiceName": "Expressvpn",
                 "Category": "VPN Service",
                 "url": "https://www.highya.com/coinbase-reviews"})
    urls.append({"ServiceName": "Expressvpn",
                 "Category": "VPN Service",
                 "url": "https://www.consumeraffairs.com/internet/godaddy.html"})
    urls.append({"ServiceName": "Expressvpn",
                 "Category": "VPN Service",
                 "url": "https://www.yelp.com/biz/fatcow-burlington"})
    
    urls.append({"ServiceName": "Expressvpn",
                 "Category": "VPN Service",
                 "url": "https://www.productreview.com.au/p/smart-fares.html"})
    urls.append({"ServiceName": "Expressvpn",
                 "Category": "VPN Service",
                 "url": "http://reviewsdatingsites.com/site/elitesingles"})
    urls.append({"ServiceName": "Expressvpn",
                 "Category": "VPN Service",
                 "url": "https://www.thewebmaster.com/web-hosting/shared/justhost-reviews/"})'''

    crawl_services(urls)