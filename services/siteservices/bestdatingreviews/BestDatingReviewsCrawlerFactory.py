from services.siteservices.bestdatingreviews.BestDatingReviewsCrawlURL import BestDatingReviewsCrawlURL


def getCrawler(url,category):
    return BestDatingReviewsCrawlURL(category)