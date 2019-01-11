import requests
from bs4 import BeautifulSoup
import time

#USER_AGENT = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
from restapis.Login import google_search_post

USER_AGENT = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}

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
def search(id,categoryName,keywords,callbackurl):
    data = []
    for keyword in keywords:
        try:
            results = scrape_google(keyword, 10, "en")
            for result in results:
                data.append(result)
            time.sleep(10)
        except Exception as e:
            print(e)
        finally:
            time.sleep(10)
    search_data ={
        "scrapping_websites" : data
    }
    print(search_data)
    google_search_post(callbackurl,search_data)
