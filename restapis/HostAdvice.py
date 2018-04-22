from services.ServiceController import crawl_services

webiste = []

webiste.append({"ServiceName": "Bluehost",
                 "Category": "Hosting Service",
                 "url": "https://hostadvice.com/hosting-company/godaddy-reviews/"})
crawl_services(webiste)
