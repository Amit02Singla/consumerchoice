# -*- coding: utf-8 -*-
from multiprocessing import Process, Queue
from product.amazon.helpers import make_request
import scrapy
from scrapy import Request
from scrapy.crawler import  CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from services.siteservices.SiteJabberURLCrawler import SiteJabberURLCrawler
from services.siteservices.HostingFactsURLCrawler import HostingFactsURLCrawler
from services.siteservices.HighyaURLCrawler import HighyaURLCrawler
from services.siteservices.AlterNativeToURLCrawler import AlterNativeToURLCrawler
from services.siteservices.SeniorDatingExpertURLCrawler import SeniorDatingExpertURLCrawler
from services.siteservices.TravelSiteCriticURLCrawler import TravelSiteCriticURLCrawler
from services.siteservices.NetBusinessRatingURLCrawler import NetBusinessRatingURLCrawler
from services.siteservices.ReviewCentreURLCrawler import ReviewCentreURLCrawler
from services.siteservices.ViewpointsURLCrawler import ViewPointsURLCrawler
from services.siteservices.CapterraURLCrawler import CapterraURLCrawler
from services.siteservices.BuyBitcoinWithCreditCardURLCrawler import BuyBitcoinWithCreditCardURLCrawler
from services.siteservices.AnblikURLCrawler import AnblikCrawlerURLCrawler
from services.siteservices.CoinJabberURLCrawler import CoinJabberURLCrawler
from services.siteservices.FreeDatingHelperURLCrawler import FreeDatingHelperURLCrawler
from services.siteservices.bestdatingreviews import BestDatingReviewsCrawlerFactory
from services.siteservices.InfluensterURLCrawler import InfluensterURLCrawler
from services.siteservices.RevexURLCrawler import RevexURLCrawler
from services.siteservices.ReviewOpediaURLCrawler import ReviewOpediaURLCrawler
from services.siteservices.AffgadgetsURLCrawler import AffgadgetsURLCrawler
from services.siteservices.AffpayingURLCrawler import AffPayingURLCrawler
from services.siteservices.BestVPNURLCrawler import BestVPNURLCrawler
from services.siteservices.BestVpnForYouURLCrawler import BestVpnForYouURLCrawler
from services.siteservices.ProductReviewURLCrawler import ProductReviewURLCrawler
from services.siteservices.ResellerRatingsURLCrawler import ResellerRatingsURLCrawler
from services.siteservices.RestorePrivacyURLCrawler import RestorePrivacyURLCrawler
from services.siteservices.TheWebMasterURLCrawler import ThewebmasterURLCrawler
from services.siteservices.WhtopURLCrawler import WhtopURLCrawler
from services.siteservices.YelpURLCrawler import YelpURLCrawler
from services.siteservices.YscamURLCrawler import YscamURLCrawler
from services.siteservices.DatingSitesReviewsURLCrawler import DatingSitesReviewsURLCrawler
from services.siteservices.TopSiteGratisURLCrawler import TopSiteGratisURLCrawler
from services.siteservices.VpnPickURLCrawler import VpnPickURLCrawler
from services.siteservices.PickUpHostURLCrawler import PickuphostURLCrawler
from services.siteservices.BestBitcoinExchnageURLCrawler import BestBitcoinExchangeURLCrawler
from services.siteservices.TrustPilotURLCrawler import TrustPilotURLCrawler
from services.siteservices.VirtualBankingURLCrawler import VirtualBankingURLCrawler
from services.siteservices.Top11HostingUrlCrawler import Top11HostingURLCrawler
from services.siteservices.BestOnlineURLCrawler import BestOnlineURLCrawler
from services.siteservices.ComparitechURLCrawler import ComparitechURLCrawler
from services.siteservices.JoomlaHostingReviewsURLCrawler import JoomlaHostingReviewsURLCrawler
from services.siteservices.WebHostingReviewURLCrawler import WebsHostingReviewsURLCrawler
from services.siteservices.WebHostingHeroURLCrawler import WebHostingHeroURLCrawler
from services.siteservices.MacUpdateURLCrawler import MacUpdateURLCrawler
from services.siteservices.TotallyOnlineDatingURLcrawler import TotallyOnlineDatingURLCrawler
from services.siteservices.ReviewsDatingSitesURLCrawler import ReviewDatingSitesCrawlerURLCrawler
from services.siteservices.TheVpnLabURLCrawler import TheVpnLabCrawlerURLCrawler
from services.siteservices.SecureThoughtsURLCrawler import SecureThoughtsURLCrawler
from services.siteservices.ForexBrokerzURLCrawler import ForexbrokerzCrawlerURLCrawler
from services.siteservices.BestVpnZURLCrawler import BestVpnZURLCrawler
from services.siteservices.WebHostingMediaURLCrawler import WebHostingMediaURLCrawler
from services.siteservices.BestVpnProviderURLCrawler import BestVpnProviderURLCrawler
from services.siteservices.Top20SeniorDatingSitesURLCrawler import Top20SeniorDatingSitesURLCrawler
from services.siteservices.HelloPeterURLCrawler import HellopeterURLCrawler
from services.siteservices.ConsumerAffairsURLCrawler import ConsumerAffairsURLCrawler
from services.siteservices.VPNRanksURLCrawler import VPNRanksURLCrawler
from services.siteservices.PissedConsumerURLCrawler import PissedConsumerURLCrawler

from services.SiteJabberCrawler import SiteJabberCrawler
from services.HostingFactsCrawler import HostingFactsCrawler
from services.HighYaCrawler import HighYaCrawler
from services.AlterNativeTo import AlterNativeTo
from services.SeniorDatingExpert import SeniorDatingExpert
from services.TravelSiteCritic import TravelSiteCritic
from services.NetBusinessRating import NetBusinessRating
from services.ReviewCentre import ReviewCentre
from services.ViewPoints import ViewPoints
from services.CapterraCrawler import CapterraCrawler
from services.BuyBitcoinsWithCreditCardCrawler import BuyBitcoinsWithCreditCardCrawler
from services.AnblikCrawler import AnblikCrawler
from services.CoinJabber import CoinJabber
from services.hostAdvisor import hostAdvisor
from services.FreeDatingHelperCrawler import FreeDatingHelperCrawler
from services.InfluensterCrawler import InfluensterCrawler
from services.RevexCrawler import RevexCrawler
from services.ReviewOpedia import ReviewOpedia
from services.affgadgetsCrawler import affgadgetsCrawler
from services.affPaying import affPaying
from services.BestVPN import BestVPN
from services.HostAdviceCrawler import HostAdviceCrawler
from services.bestVPNForYou import bestVPNForYou
from services.ProductreviewCrawler import ProductreviewCrawler
from services.ResellerRatingCrawler import ResellerRatingCrawler
from services.restorePrivacy import restorePrivacy
from services.ThewebmasterCrawler import ThewebmasterCrawler
from services.vpnMentor import vpnMentor
from services.webhostinggeeksCrawler import webhostinggeeksCrawler
from services.WhoIsHostingCrawler import WhoIsHostingCrawler
from services.whtop import whtop
from services.yelpCrawler import yelpCrawler
from services.Yscam import Yscam
from services.hostingCharges import hostingCharges
from services.DatingSitesReviewsCrawler import DatingSitesReviewsCrawler
from services.TopSiteGratis import TopSiteGratis
from services.DatingWiseCrawler import DatingWiseCrawler
from services.VPNpickCrawler import VPNpickCrawler
from services.PickuphostCrawler import PickuphostCrawler
from services.BestBitcoinExchange import BestBitcoinExchange
from services.TrustPilot import TrustPilot
from services.VirtualBanking import VirtualBanking
from services.top11Hosting import top11Hosting
from services.BestOnline import BestOnline
from services.CompariTech import CompariTech
from services.JoomlaHostingReviews import JoomlaHostingReviews
from services.Hellopeter import Hellopeter
from services.WebHostingHero import WebHostingHero
from services.MacUpdate import MacUpdate
from services.TotallyOnlineDating import TotallyOnlineDating
from services.ReviewDatingSitesCrawler import ReviewDatingSitesCrawler
from services.TheVPNlabCrawler import TheVPNlabCrawler
from services.SecureThoughts import SecureThoughts
from services.ForexbrokerzCrawler import ForexbrokerzCrawler
from services.BestVPNZCrawler import BestVPNZCrawler
from services.webHostingmedia import webHostingmedia
from services.BestVPNProvidersCrawler import BestVPNProvidersCrawler
from services.SeniorDatingSites import SeniorDatingSites
from services.Hellopeter import Hellopeter
from services.consumerAffairsCrawler import consumerAffairsCrawler
from services.vpnRanks import vpnRanks
from services.BlackPeopleMeet_PissedConsumer import BlackPeopleMeet_PissedConsumer
from services.webshostingFatcow import webshostingFatcow

final_dict_urls= {}
dict_url = {}
class SiteServiceListController(scrapy.Spider):
    start_urls = []

    def __init__(self, link):
        if (len(self.start_urls) > 0):
            self.start_urls.pop(0)
        self.start_urls.append(link["url"])
        category = link["Category"];
        dict_url[link["url"]] = {"Category": category}
        if(len(link["url1"])>0):
            url1 = link["url1"]
            dict_url["url1"] = {"url1": url1}

    def closed(self, reason):
        pass

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
        for url in self.start_urls:
            yield Request(url, headers=headers,meta={'dont_merge_cookies': True})

    def parse(self, response):
        self.log('I just visited: ' + response.url)
        if ('sitejabber.com' in response.url):
            if('reviews' in response.url):
                service  = response.url.split("/");
                serviceName = service[len(service)-1];
                print(" Servicesssss   ", serviceName)
                crawler = SiteJabberCrawler( dict_url[response.url]["Category"],serviceName,response.url)
            else:
                crawler = SiteJabberURLCrawler(dict_url[response.url]["Category"])
        elif('hostingfacts.com' in response.url):
            if ('reviews' in response.url):
                service = response.url.split("/");
                serviceName = service[len(service) - 1];
                print(" Servicesssss   ", serviceName)
                crawler = HostingFactsCrawler(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = HostingFactsURLCrawler(dict_url[response.url]["Category"])
        elif ('highya.com' in response.url):
            if ('reviews' in response.url):
                service = response.url.split("/");
                serviceName = service[len(service) - 1];
                print(" Servicesssss   ", serviceName)
                crawler = HighYaCrawler(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = HighyaURLCrawler(dict_url[response.url]["Category"])
        elif ('alternativeto.net' in response.url):
            if ('browse' in response.url):
                crawler = AlterNativeToURLCrawler(dict_url[response.url]["Category"])
            else:
                service = response.url.split("/");
                serviceName = service[len(service) - 2];
                print(" Servicesssss   ", serviceName)
                crawler = AlterNativeTo(dict_url[response.url]["Category"], serviceName, response.url)
        elif ('seniordatingexpert.com' in response.url):
            if len(response.url.split('/')) > 5:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = SeniorDatingExpert(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = SeniorDatingExpertURLCrawler(dict_url[response.url]["Category"])
        elif ('travelsitecritic.com' in response.url):
            if len(response.url.split('/')) > 5:
                service = response.url.split("/")
                serviceName = service[len(service) - 2]
                serviceName = serviceName.replace("-reviews","")
                print(" Servicesssss   ", serviceName)
                crawler = TravelSiteCritic(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = TravelSiteCriticURLCrawler(dict_url[response.url]["Category"])
        elif ('netbusinessrating.com' in response.url):
            if ('ranking' in response.url):
                crawler = NetBusinessRatingURLCrawler(dict_url[response.url]["Category"])
            else:
                service = response.url.split("/");
                serviceName = service[len(service) - 1];
                print(" Servicesssss   ", serviceName)
                crawler = NetBusinessRating(dict_url[response.url]["Category"], serviceName, response.url)
        elif ('reviewcentre.com' in response.url):
            if('searchstring' not in response.url):
                service  = response.url.split("/");
                serviceName = service[len(service)-1];
                print(" Servicesssss   ", serviceName)
                crawler = ReviewCentre( dict_url[response.url]["Category"],serviceName,response.url)
            else:
                crawler = ReviewCentreURLCrawler(dict_url[response.url]["Category"])
        elif ('viewpoints.com' in response.url):
            if 'search' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                serviceName = serviceName.replace("-reviews","")
                print(" Servicesssss   ", serviceName)
                crawler = ViewPoints(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = ViewPointsURLCrawler(dict_url[response.url]["Category"])
        elif ('capterra.com' in dict_url["url1"]["url1"]):
            if 'search' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 2]
                print(" Servicesssss   ", serviceName)
                crawler = CapterraCrawler(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = CapterraURLCrawler(dict_url[response.url]["Category"])
        elif ('buybitcoinswithcreditcard.net' in response.url):
            if '?s=' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 2]
                print(" Servicesssss   ", serviceName)
                crawler = BuyBitcoinsWithCreditCardCrawler(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = BuyBitcoinWithCreditCardURLCrawler(dict_url[response.url]["Category"])
        elif ('anblik.com' in response.url):
            if '?s=' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 2]
                print(" Servicesssss   ", serviceName)
                cat = dict_url["url1"]
                crawler = AnblikCrawler(dict_url[cat["url1"]]["Category"], serviceName, response.url)
            else:
                crawler = AnblikCrawlerURLCrawler(dict_url[response.url]["Category"])
        elif ('coinjabber.com' in response.url):
            if 'search' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = CoinJabber( "",serviceName, response.url)
            else:
                crawler = CoinJabberURLCrawler(dict_url[response.url]["Category"])
        elif ('hostadvisor.com' in response.url):
            if 'search' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = hostAdvisor(dict_url[response.url]["Category"], serviceName, response.url)
        elif ('freedatinghelper.com' in response.url):
            if '?s=' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 2]
                print(" Servicesssss   ", serviceName)
                crawler = FreeDatingHelperCrawler(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = FreeDatingHelperURLCrawler(dict_url[response.url]["Category"])
        elif ('bestdatingreviews.org' in response.url):
            crawler = BestDatingReviewsCrawlerFactory.getCrawler(response.url,dict_url[response.url]["Category"])
        elif ('influenster.com' in response.url):
            if 'search' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = InfluensterCrawler(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = InfluensterURLCrawler(dict_url[response.url]["Category"])
        elif ('revex.co' in response.url):
            if '/?s=' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = RevexCrawler(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = RevexURLCrawler(dict_url[response.url]["Category"])
        elif ('reviewopedia.com' in response.url):
            if 'search' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = ReviewOpedia(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = ReviewOpediaURLCrawler(dict_url[response.url]["Category"])
        elif ('affgadgets.com' in response.url):
            if '/?s=' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = affgadgetsCrawler(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = AffgadgetsURLCrawler(dict_url[response.url]["Category"])
        elif ('affpaying.com' in response.url):
            if '/?s=' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = affPaying(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = AffPayingURLCrawler(dict_url[response.url]["Category"])
        elif ('bestvpn.com' in response.url):
            if len(response.url.split('/')) > 5:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = BestVPN("", serviceName, response.url)
            else:
                crawler = BestVPNURLCrawler(dict_url[response.url]["Category"])
        elif ('forexbrokerz.com' in response.url):
            if len(response.url.split('/')) > 4:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = ForexbrokerzCrawler(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = ForexbrokerzCrawlerURLCrawler(dict_url[response.url]["Category"])
        elif ('hostadvice.com' in response.url):
            if 'search' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = HostAdviceCrawler(dict_url[response.url]["Category"], serviceName, response.url)
        elif ('bestvpnforyou.com' in response.url):
            if '/?s=' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = bestVPNForYou(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = BestVpnForYouURLCrawler(dict_url[response.url]["Category"])
        elif ('productreview.com.au' in dict_url["url1"]["url1"]):
            if 'search' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = ProductreviewCrawler(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = ProductReviewURLCrawler(dict_url[response.url]["Category"])
        elif ('resellerratings.com' in response.url):
            if 'search' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = ResellerRatingCrawler(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = ResellerRatingsURLCrawler(dict_url[response.url]["Category"])
        elif ('restoreprivacy.com' in response.url):
            if '/?s=' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = restorePrivacy(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = RestorePrivacyURLCrawler(dict_url[response.url]["Category"])
        elif ('bestvpnz.com' in response.url):
            if '/?s=' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 2]
                print(" Servicesssss   ", serviceName)
                cat = dict_url["url1"]
                crawler = BestVPNZCrawler(dict_url[cat["url1"]], serviceName, response.url)
            else:
                crawler = BestVpnZURLCrawler(dict_url[response.url]["Category"])
        elif ('webhostingmedia.net' in response.url):
            if '/?s=' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 2]
                print(" Servicesssss   ", serviceName)
                crawler = webHostingmedia(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = WebHostingMediaURLCrawler(dict_url[response.url]["Category"])
        elif ('thewebmaster.com' in response.url):
            if 'search' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 2]
                print(" Servicesssss   ", serviceName)
                crawler = ThewebmasterCrawler(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = ThewebmasterURLCrawler(dict_url[response.url]["Category"])
        elif ('vpnmentor.com' in response.url):
            if 'search' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 2]
                print(" Servicesssss   ", serviceName)
                crawler = vpnMentor(dict_url[response.url]["Category"], serviceName, response.url)
        elif ('webhostinggeeks.com' in response.url):
            if 'search' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = webhostinggeeksCrawler(dict_url[response.url]["Category"], serviceName, response.url)
        elif ('whoishostingthis.com' in response.url):
            if 'search' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = WhoIsHostingCrawler(dict_url[response.url]["Category"], serviceName, response.url)
        elif ('whtop.com' in response.url):
            if 'search' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = whtop("", serviceName, response.url)
            else:
                crawler = WhtopURLCrawler(dict_url[response.url]["Category"])
        elif ('yelp.com' in response.url):
            if 'search' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = yelpCrawler(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = YelpURLCrawler(dict_url[response.url]["Category"])
        elif ('yscam.com' in response.url):
            if 'search' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = Yscam(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = YscamURLCrawler(dict_url[response.url]["Category"])
        elif ('hostingcharges.in' in response.url):
            if 'search' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = hostingCharges( "",serviceName, response.url)
        elif ('datingsitesreviews.com' in response.url):
            if 'search' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = DatingSitesReviewsCrawler(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = DatingSitesReviewsURLCrawler(dict_url[response.url]["Category"])
        elif ('vpnranks.com' in dict_url["url1"]["url1"]):
            if 'search' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = vpnRanks(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = VPNRanksURLCrawler(dict_url[response.url]["Category"])
        elif ('topsitegratis.com.br' in response.url):
            if '/?q=' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = TopSiteGratis(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = TopSiteGratisURLCrawler(dict_url[response.url]["Category"])
        elif ('datingwise.com' in response.url):
            if 'search' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 2]
                print(" Servicesssss   ", serviceName)
                crawler = DatingWiseCrawler(dict_url[response.url]["Category"], serviceName, response.url)
        elif ('vpnpick.com' in response.url):
            if '/?s=' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 2]
                print(" Servicesssss   ", serviceName)
                crawler = VPNpickCrawler(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = VpnPickURLCrawler(dict_url[response.url]["Category"])
        elif ('bestbitcoinexchange.net' in response.url):
            if '/?s=' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 2]
                print(" Servicesssss   ", serviceName)
                crawler = BestBitcoinExchange(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = BestBitcoinExchangeURLCrawler(dict_url[response.url]["Category"])
        elif ('trustpilot.com' in response.url):
            if 'search' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = TrustPilot(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawtler = TrustPilotURLCrawler(dict_url[response.url]["Category"])
        elif ('virtualbanking.com' in response.url):
            if '/?s=' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 2]
                serviceName.replace("-review","")
                print(" Servicesssss   ", serviceName)
                crawler = VirtualBanking(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = VirtualBankingURLCrawler(dict_url[response.url]["Category"])
        elif ('top11hosting.com' in response.url):
            if len(response.url.split('/')) > 4:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = top11Hosting(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = Top11HostingURLCrawler(dict_url[response.url]["Category"])
        elif ('10bestonline.com' in response.url):
            if len(response.url.split('/')) > 5:
                service = response.url.split("/")
                serviceName = service[len(service) - 2]
                print(" Servicesssss   ", serviceName)
                crawler = BestOnline(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = BestOnlineURLCrawler(dict_url[response.url]["Category"])
        elif ('comparitech.com' in response.url):
            if '/?s=' not in response.url:
                url = response.url
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                r = make_request(response.url, False, False)
                crawler = CompariTech(dict_url[response.url]["Category"], serviceName, url)
                response = r.content
                crawler.crawl(response)
                crawler = None
            else:
                r = make_request(response.url, False, False)
                crawler = ComparitechURLCrawler(dict_url[response.url]["Category"])
                response = r.content
        elif ('joomlahostingreviews.com' in response.url):
            if 'search' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                serviceName = serviceName.replace("-review.html","")
                print(" Servicesssss   ", serviceName)
                crawler = JoomlaHostingReviews(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = JoomlaHostingReviewsURLCrawler(dict_url[response.url]["Category"])
        elif ('macupdate.com' in response.url):
            if 'find' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = MacUpdate(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = MacUpdateURLCrawler(dict_url[response.url]["Category"])
        elif ('totallyonlinedating.com' in response.url):
            if len(response.url.split('/')) > 5:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = TotallyOnlineDating(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = TotallyOnlineDatingURLCrawler(dict_url[response.url]["Category"])
        elif ('reviewsdatingsites.com' in response.url):
            if 'search' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = ReviewDatingSitesCrawler(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = ReviewDatingSitesCrawlerURLCrawler(dict_url[response.url]["Category"])
        elif ('thevpnlab.com' in response.url):
            if '/?s=' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 2]
                print(" Servicesssss   ", serviceName)
                crawler = TheVPNlabCrawler(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = TheVpnLabCrawlerURLCrawler(dict_url[response.url]["Category"])
        elif ('pickuphost.com' in response.url):
            if len(response.url.split('/')) > 5:
                service = response.url.split("/")
                serviceName = service[len(service) - 2]
                print(" Servicesssss   ", serviceName)
                crawler = PickuphostCrawler("", serviceName, response.url)
            else:
                crawler = PickuphostURLCrawler(dict_url[response.url]["Category"])
        elif ('top20seniordatingsites.com' in response.url):
            if len(response.url.split('/')) > 4:
                service = response.url.split("/")
                serviceName = service[len(service) - 2]
                print(" Servicesssss   ", serviceName)
                crawler = SeniorDatingSites(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = Top20SeniorDatingSitesURLCrawler(dict_url[response.url]["Category"])
        elif ('hellopeter.com' in response.url):
            if 'search' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = Hellopeter(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = HellopeterURLCrawler(dict_url[response.url]["Category"])
        elif ('consumeraffairs.com' in response.url):
            if 'search' not in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 1]
                print(" Servicesssss   ", serviceName)
                crawler = consumerAffairsCrawler(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = ConsumerAffairsURLCrawler(dict_url[response.url]["Category"])
        elif ('pissedconsumer.com' in response.url):
            if ('review'  in response.url):
                service = response.url.split("/");
                serviceName = service[2].split('.')[0];
                print(" Servicesssss   ", serviceName)
                crawler = BlackPeopleMeet_PissedConsumer(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = PissedConsumerURLCrawler(dict_url[response.url]["Category"])
        elif ('securethoughts.com' in response.url):
            # if len(response.url.split('/')) > 5:
            #     service = response.url.split("/")
            #     serviceName = service[len(service) - 2]
            #     print(" Servicesssss   ", serviceName)
            #     crawler = SecureThoughts(dict_url[response.url]["Category"], serviceName, response.url)
            # else:
            crawler = SecureThoughtsURLCrawler(dict_url[response.url]["Category"])
        elif ('webshosting.review' in response.url):
            # if 'search' not in response.url:
            service = response.url.split("/")
            serviceName = service[len(service) - 1]
            serviceName = serviceName.replace("-reviews","")
            print(" Servicesssss   ", serviceName)
            #     crawler = Hellopeter(dict_url[response.url]["Category"], serviceName, response.url)
            # else:

            crawler = webshostingFatcow(dict_url[response.url]["Category"], serviceName, response.url)
        elif ('webhostinghero.com' in response.url):
            if 'reviews' in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 2]
                print(" Servicesssss   ", serviceName)
                crawler = WebHostingHero(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = WebHostingHeroURLCrawler(dict_url[response.url]["Category"])
        elif ('bestvpnprovider.co' in response.url):
            if 'review' in response.url:
                service = response.url.split("/")
                serviceName = service[len(service) - 2]
                print(" Servicesssss   ", serviceName)
                crawler = BestVPNProvidersCrawler(dict_url[response.url]["Category"], serviceName, response.url)
            else:
                crawler = BestVpnProviderURLCrawler(dict_url[response.url]["Category"])
        else:
            print("Found Nothing")
        if (crawler != None):
            return crawler.crawl(response)

def f(q, ):
    try:
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        runner = CrawlerRunner()
        deferred = runner.crawl(SiteServiceListController, q[1])
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        q[0].put(None)
    except Exception as e:
        q[0].put(e)

def run_spider(urls):
    q = Queue()
    p = Process(target=f, args=([q, urls],))
    p.start()
    result = q.get()
    p.join()
    if result is not None:
        raise result
def crawl_services1(urls):
    url = getAjax(urls)

    for i in url:
        if callingBeautifulSoap(i) is False:
            run_spider(i)

def getAjax(urls):
    urllist = []
    for url in urls:
        if 'hellopeter.com' in  url["url"]:
            a = url["url"].split('/')[-1]
            url["url1"] = url["url"]
            url["url"] = "https://api-v3.hellopeter.com/search/businesses?q="+a
            urllist.append(url)
            url = url.copy()
            url["url"] = "https://api-v3.hellopeter.com/search/industries?q="+a
            urllist.append(url)
        # elif 'capterra.com' in  url["url"]:
        #     a = url["url"].split('search=')[-1]
        #     url["url1"] = url["url"]
        #     url["url"] = "https://ui.customsearch.ai/api/search?q="+a+"&customConfig=3916836352&count=10&offset=0&mkt=en-US&safeSearch=Moderate&textFormat=HTML&textDecorations=true"
        #     urllist.append(url)
        elif 'consumeraffairs.com' in  url["url"]:
            a = url["url"].split('?q=')[-1]
            url["url1"] = url["url"]
            url["url"] = "https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=10&hl=en&prettyPrint=false&source=gcsc&gss=.com&sig=4aa0772189af4c17ea7ec181af2bca15&cx=partner-pub-0200629403145096:6869548600&q="+a+"&cse_tok=AF14hliZogyX-UIGsRzeh53SxuUcuVAYLw:1531574501440&googlehost=www.google.com&callback=google.search.Search.apiary18179&nocache=1531574555569"
            urllist.append(url)
        elif 'vpnranks.com' in  url["url"]:
            a = url["url"].split('?q=')[-1]
            url["url1"] = url["url"]
            url["url"] = "https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=10&hl=en&prettyPrint=false&source=gcsc&gss=.com&sig=4aa0772189af4c17ea7ec181af2bca15&cx=017240969328192326971:ou9j9m_tmba&q="+a+"&cse_tok=AF14hlhuQXH7yfX1J17hCZYy8EH5ZtOl8A:1531575399065&googlehost=www.google.com&callback=google.search.Search.apiary5263&nocache=1531575454153"
            urllist.append(url)
        elif 'productreview.com.au' in url["url"]:
            a = url["url"].split('search=')[-1]
            a  = a[1].split('&')[0]
            url["url1"] = url["url"]
            url["url"] = "https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=10&hl=en&prettyPrint=false&source=gcsc&gss=.au&sig=4aa0772189af4c17ea7ec181af2bca15&cx=003361650787787341744:smnuvutjqce&q="+a+"&cse_tok=AF14hljfNW8Na3fY5No5Ifhaq7LepkJN-A:1531575202440&googlehost=www.google.com&callback=google.search.Search.apiary11993&nocache=1531575257715"
            urllist.append(url)
        else:
            url["url1"] = url["url"]
            urllist.append(url)
    return urllist

def callingBeautifulSoap(dictURL):
    url = dictURL["url"]
    if('comparitech.com' in url):
        print("urllllllllllllll   "+ url);
        if '/?s=' not in url:
            service = url.split("/")
            serviceName = service[len(service) - 2]
            print(" Servicesssss   ", serviceName)
            r = make_request(url, False, False)
            crawler = CompariTech(dictURL["Category"], serviceName, url)
            response = r.content
            crawler.crawl(response)
        else:
            r = make_request(url, False, False)
            crawler = ComparitechURLCrawler(dictURL["Category"])
            response = r.content
            crawler.crawl(response)
    elif ('bestbitcoinexchange.net' in url):
        if '/?s=' not in url:
            service = url.split("/")
            serviceName = service[len(service) - 2]
            print(" Servicesssss   ", serviceName)
            r = make_request(url, False, False)
            crawler = BestBitcoinExchange(dictURL["Category"], serviceName, url)
            response = r.content
            crawler.crawl(response)
        else:
            r = make_request(url, False, False)
            crawler = BestBitcoinExchangeURLCrawler(dictURL["Category"])
            response = r.content
            crawler.crawl(response)
        return True
    return False
