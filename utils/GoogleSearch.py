import requests
from bs4 import BeautifulSoup
import time
from restapis.RestClient import RestClient;
from urlparse import urlparse

#USER_AGENT = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
from restapis.Login import google_search_post

USER_AGENT = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
superset = [];
def fetch_results(search_term, number_results, language_code):

    print("Searching ", search_term)
    search_term = str(search_term)
    assert isinstance(search_term, str), 'Search term must be a string'
    assert isinstance(number_results, int), 'Number of results must be an integer'
    escaped_search_term = search_term.replace(' ', '+')

    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results, language_code)
    print("google_url ", google_url)
    response = requests.get(google_url, headers=USER_AGENT,verify= False)
    response.raise_for_status()

    return search_term, response.text


def parse_results(html, keyword):
    soup = BeautifulSoup(html, 'html.parser')

    found_results = []
    rank = 1
    result_block = soup.find_all('div', attrs={'class': 'g'})
    for result in result_block:

        link = result.find('a', href=True)
        title = result.find('h3', attrs={'class': 'r'})
        if(title == None):
            title = result.find('h3', attrs={'class': 'LC20lb'})
        description = result.find('span', attrs={'class': 'st'})
        if link and title:
            link = link['href']
            if(title != None):
                title = title.get_text()
                if link != '#':
                    found_results.append({"url":link, "name": title})
                    rank += 1
    return found_results
def scrape_google(search_term, number_results, language_code):
    try:
        keyword, html = fetch_results(search_term, number_results, language_code)
        results = parse_results(html, keyword)
        return results
    except AssertionError:
        raise Exception("Incorrect arguments parsed to function")
    except requests.HTTPError:
        raise Exception("You appear to have been blocked by Google")
    except requests.RequestException:
        raise Exception("Appears to be an issue with your connection")

def search(websiteUrls, callbackurl):
        data = []
        for websiteUrl in websiteUrls:
            id = websiteUrl[0]
            parsedURL = urlparse(websiteUrl[1])
            hostname = parsedURL.hostname.split(".")[1]
            try:
                results = scrape_google(hostname, 10, "en")
                for result in results:
                    resultParseURL = urlparse(result['url'])
                    resultParseURLHostName = resultParseURL.hostname
                    if(resultParseURLHostName in superset):
                        resultset = {"id":id,
                                     "name":result['name'],
                                     "url":result['url']}
                        data.append(resultset)
                time.sleep(10)
            except Exception as e:
                print(e)
            finally:
                time.sleep(10)
        google_search_post(callbackurl, {"scrapping_websites":data})

def dataforSEO(id,categoryName,keywords,callbackurl):
    my = RestClient()
    print(" in search method")
    data = []
    i=0;
    post_data = dict()
    for keyword in keywords:
        i = i + 1;
        post_data[i] = dict(
            priority=1,
            se_name="google.com",
            se_language="English",
            loc_name_canonical="India",
            key=keyword
        )
    print ("before send request")
    response = my.post("/v2/srp_tasks_post", dict(data=post_data))
    if response["status"] == "error":
        print("error. Code: %d Message: %s" % (response["error"]["code"], response["error"]["message"]))
    else:
        print("request succesfully  ",response["results"])
    time.sleep(90)
    print("after wait")
    completed_tasks_response = my.get("/v2/srp_tasks_get")
    if completed_tasks_response["status"] == "error":
        print("error. Code: %d Message: %s" % (
        completed_tasks_response["error"]["code"], completed_tasks_response["error"]["message"]))
    else:
        results = completed_tasks_response["results"]
        print("resultssssss     ", results)
        for result in results:
            srp_response = my.get("/v2/srp_tasks_get/%d" % (result["task_id"]))
            print("after getting response")
            if srp_response["status"] == "error":
                print("error. Code: %d Message: %s" % (
                    srp_response["error"]["code"], srp_response["error"]["message"]))
            else:
                dictionary = srp_response["results"]
                for urlList in dictionary["organic"]:
                    a = {"url": urlList["result_url"],
                         "name": categoryName}
                    data.append(a);
    time.sleep(10)
    print("urls list count is ", len(data))
    search_data ={
        "scrapping_websites" : data
    }
    print(search_data)
    google_search_post(callbackurl,search_data)

