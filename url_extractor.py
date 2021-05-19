import requests
import re
from urllib.parse import urljoin
import logging

logging.basicConfig(filename='urls.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')
target_url = ""
target_links = []


def extract_links_from(url):
    response = requests.get(url)
    return re.findall('(?:href=")(.*?)"', str(response.content))


def crawl(url):
    href_links = extract_links_from(url)
    for link in href_links:
        link = urljoin(url, link)

        if '#' in link:
            link = link.split('#')[0]

        if target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            logging.debug("URL Extracted --> {}".format(link))
            crawl(link)


def run_crawler():
    global target_url
    url = input("Enter the target URL\n")
    target_url = url
    crawl(target_url)

