import requests

def request(url):
    try:
        return reqyests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass

target_url = ""

with open("wordlist file path here", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        test_url = target_url + "/" + word
        response = request(test_url)
        if response:
            print("[+] Discovered URL -->" + test_url)