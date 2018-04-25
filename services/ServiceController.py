# -*- coding: utf-8 -*-
from multiprocessing import Process, Queue

import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from services.TotallyOnlineDating import TotallyOnlineDating
from services.BestDatingReviews import BestDatingReviews
from services.SeniorDatingSites import SeniorDatingSites
from services.BlackPeopleMeet_PissedConsumer import BlackPeopleMeet_PissedConsumer
from services.Yscam import Yscam
from services.BestOnline import BestOnline
from services.CompariTech import CompariTech
from services.MacUpdate import MacUpdate
from services.SecureThoughts import SecureThoughts
from services.WebHostingHero import WebHostingHero
from services.VPNpickCrawler import VPNpickCrawler
from services.vpnRanks import vpnRanks
from services.vpnMentor import vpnMentor
from services.restorePrivacy import restorePrivacy
from services.affPaying import affPaying
from services.webHostingmedia import webHostingmedia
from services.hostAdvisor import hostAdvisor
from services.hostingCharges import hostingCharges
from services.top11Hosting import top11Hosting
from services.webhostinggeeksCrawler import webhostinggeeksCrawler
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
from services.WebHostingHeroCrawler import WebHostingHeroCrawler
from services.BestVPNZCrawler import BestVPNZCrawler
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

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url, headers=headers)
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
            restapis.Login.postReview({"business_units":buisness_units})
        with open("reviews.json","w") as f:
            json.dump({"business_units":buisness_units},f)
        reactor.stop()
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
            crawler = SiteJabberCrawler()
        #elif ('bestvpn.com'in response.url):
         #   crawler = BestVPN()
        elif ('resellerratings.com' in response.url):
            crawler = ResellerRatingCrawler()
        elif ('capterra.com' in response.url):
            crawler = CapterraCrawler()
        elif ('forexbrokerz.com' in response.url):
            crawler = ForexbrokerzCrawler()
        #elif('highya.com' in response.url):
         #   crawler = HighYaCrawler()
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
        elif 'whtop.com' in response.url:
            crawler = yelpCrawler()
        elif('webhostinghero.com' in response.url):
            crawler = WebHostingHeroCrawler()
        elif('bestvpnz.com' in response.url):
            crawler =  BestVPNZCrawler()
        elif 'vpnranks.com' in response.url:
            crawler = vpnRanks()
        elif 'webhostinghero.com' in response.url:
            crawler = WebHostingHero()
        elif 'securethoughts.com' in response.url:
            crawler = SecureThoughts()
        elif 'macupdate.com' in response.url:
            crawler = MacUpdate()
        elif 'comparitech.com' in response.url:
             crawler = CompariTech()
        elif '10bestonline.com' in response.url:
            crawler = BestOnline()
        elif 'yscam.com' in response.url:
            crawler = Yscam()
        elif 'blackpeoplemeet.pissedconsumer.com' in response.url:
            crawler = BlackPeopleMeet_PissedConsumer()
        elif 'top20seniordatingsites.com' in response.url:
            crawler = SeniorDatingSites()
        elif 'bestdatingreviews.org' in response.url:
            crawler = BestDatingReviews()
        elif 'totallyonlinedating.com' in response.url:
            crawler = TotallyOnlineDating()
        #elif 'seniordatingexpert.com' in response.url:
         #   crawler = SeniorDatingSites()
        else:
            print("Found Nothing")
        if (crawler != None):
            return crawler.crawl(response, dict_url[response.url]["Category"], dict_url[response.url]["Service Name"])

def f(q, ):
    try:
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        runner = CrawlerRunner()
        deferred = runner.crawl(ServiceController, q[1])
        deferred.addBoth(lambda _: reactor.stop())
        print("method f")
        reactor.run()
        q[0].put(None)
    except Exception as e:
        q[0].put(e)


def crawl_services(urls):
    q = Queue()
    p = Process(target=f, args=([q, urls],))
    print("crawl_services()")
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result

