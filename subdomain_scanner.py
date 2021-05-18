import requests

def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass

def run_subdomain_scan():
    target_url = raw_input("Enter the target url (without http; eg - google.com or ign.com)\n")
    with open("subdomain.txt", "r") as wordlist_file:
        for line in wordlist_file:
            word = line.strip()
            test_url = word + "." + target_url
            response = request(test_url)
            if response:
                print("[+] Discovered Subdomain --> " + test_url)

