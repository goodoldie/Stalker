import requests
import logging

logging.basicConfig(filename='subdomains.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass


def run_subdomain_scan():
    target_url = input("Enter the target url (without http; eg - google.com or ign.com)\n")
    with open("subdomain.txt", "r") as wordlist_file:
        for line in wordlist_file:
            word = line.strip()
            test_url = word + "." + target_url
            response = request(test_url)
            if response:
                print("[+] Discovered Subdomain --> " + test_url)
                logging.debug("Discovered Subdomain --> {}".format(test_url))

