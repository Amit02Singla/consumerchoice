# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from services.VPNpickCrawler import VPNpickCrawler
from services.vpnRanks import vpnRanks
from services.vpnMentor import vpnMentor
from services.restorePrivacy import restorePrivacy
from services.affPaying import affPaying
from services.webHostingmedia import webHostingmedia
from services.hostAdvisor import hostAdvisor
from services.hostingCharges import hostingCharges
from services.top11Hosting import top11Hosting
from services.ThewebmasterCrawler import ThewebmasterCrawler
from services.webhostinggeeksCrawler import webhostinggeeksCrawler
from services.yelpCrawler import yelpCrawler
from services.consumerAffairsCrawler import consumerAffairsCrawler
from services.HighYaCrawler import HighYaCrawler
from services.whtop import whtop
from services.bestVPNForYou import bestVPNForYou
from services.webshostingFatcow import webshostingFatcow
from services.BestVPN import BestVPN
from services.CapterraCrawler import CapterraCrawler
from services.ForexbrokerzCrawler import ForexbrokerzCrawler
# from scrapy.selector import HtmlXPathSelector
from services.HighYaCrawler import HighYaCrawler
from services.HostAdviceCrawler import HostAdviceCrawler
from services.HostingFactsCrawler import HostingFactsCrawler
from services.ResellerRatingCrawler import ResellerRatingCrawler
from model.Response import Response
from services.SiteJabberCrawler import SiteJabberCrawler
from services.WhoIsHostingCrawler import WhoIsHostingCrawler
from services.consumerAffairsCrawler import consumerAffairsCrawler
from services.yelpCrawler import yelpCrawler
from services.affgadgetsCrawler import AffgadgetsCrawler
from services.ProductreviewCrawler import ProductreviewCrawler
from services.ReviewDatingSitesCrawler import ReviewDatingSitesCrawler
from services.ThewebmasterCrawler import ThewebmasterCrawler
from services.TheVPNlabCrawler import TheVPNlanCrawler
from model.Servicemodel import final_json
import restapis.Login
import json

final_dict_reviews= {}
dict_url = {}
class ServiceController(scrapy.Spider):
    start_urls = []

    def __init__(self, url):
        for link in url:
            self.start_urls.append(link["url"])
            category = link["Category"];
            service_name = link["ServiceName"]
            dict_url[link["url"]] = {"Category": category,
                                     "Service Name": service_name}
            response = Response("Service");
            response.Service_Name = service_name
            response.Category = category
            response.URL = link["url"]
            final_json[service_name] = {"response": response}

    def closed(self, reason):
        # with open("reviews.json","w") as f:
        #    json.dump(final_json,f)
        str1 = ""
        dictionary = {}
        buisness_units = []
        for k, v in final_json.items():
            responselist = []
            responselist.append(v["response"].dump())
            dictionary[k] = {"scrapping_website_name": k, "scrapping_website_url": v["response"].URL,
                             "response": responselist}
            buisness_units.append(dictionary[k])
            #Todo need to uncomment
          #  restapis.Login.postReview({"business_units":buisness_units})
        with open("reviews.json","w") as f:
            json.dump({"business_units":buisness_units},f)
    def parse(self, response):
        self.log('I just visited: ' + response.url)
        dict_reviews = {}
        reviews= []

        if ('hostingfacts.com' in response.url):
            crawler = HostingFactsCrawler()
        elif ('hostadvice.com' in response.url):
            crawler = HostAdviceCrawler()
        elif ('whoishostingthis.com' in response.url):
            crawler = WhoIsHostingCrawler()
        elif ('sitejabber.com' in response.url):
            # sitejabber
            crawler = SiteJabberCrawler()
        elif (response.xpath('//div[@class="comment-content"]')):
            crawler = BestVPN()
        elif ('resellerratings.com' in response.url):
            crawler = ResellerRatingCrawler()
        elif ('capterra.com' in response.url):
            crawler = CapterraCrawler()
        elif ('forexbrokerz.com' in response.url):
            crawler = ForexbrokerzCrawler()
        elif('highya.com' in response.url):
            crawler = HighYaCrawler()
        elif(response.xpath("//div[@class='campaign-reviews__regular-container js-campaign-reviews__regular-container']/div/div[@class='rvw-bd ca-txt-bd-2']/p")):
            crawler = consumerAffairsCrawler()
        elif('yelp.com' in response.url):
            crawler = yelpCrawler()
        elif('affgadgets.com' in response.url):
            crawler = AffgadgetsCrawler()
        elif('productreview.com' in response.url):
            crawler = ProductreviewCrawler()
        elif('reviewsdatingsites.com' in response.url):
            crawler = ReviewDatingSitesCrawler()
        elif('thewebmaster.com' in response.url):
            crawler = ThewebmasterCrawler()
        elif('thevpnlab.com' in response.url):
            crawler = TheVPNlanCrawler()
        elif ('affpaying.com' in response.url):
            crawler = affPaying()
        elif ('bestvpnforyou.com' in response.url):
            crawler = bestVPNForYou()
        elif ('hostadvisor.com' in response.url):
            crawler = hostAdvisor()
        elif ('hostingcharges.in' in response.url):
            crawler = hostingCharges()
        elif ('restoreprivacy.com' in response.url):
            crawler = restorePrivacy()
        elif ('top11hosting.com' in response.url):
            crawler = top11Hosting()
        elif ('vpnmentor.com' in response.url):
            crawler = vpnMentor()
        elif ('vpnpick.com' in response.url):
            crawler = VPNpickCrawler()
        elif ('webhostingmedia.net' in response.url):
            crawler = webHostingmedia()
        elif ('webhostinggeeks.com' in response.url):
            crawler = webhostinggeeksCrawler()
        elif ('webshosting.review' in response.url):
            crawler = webshostingFatcow()
        elif ('whtop.com' in response.url):
            crawler = whtop()
        elif ('whtop.com' in response.url):
            crawler = yelpCrawler()
        else:
            print("kuch nhi mila")
        if(crawler!=None):
            return crawler.crawl(response, dict_url[response.url]["Category"], dict_url[response.url]["Service Name"])


def crawl_services(urls):
    process = CrawlerProcess(get_project_settings())
    process.crawl(ServiceController, urls)
    process.start()
    # print final_dict_reviews

    # with open("reviews.json","w") as f:
    #          json.dump(final_dict_reviews,f)
    # print("Writing json file")