import requests
from bs4 import BeautifulSoup
import urlparse

def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass


target_url = ""
def extract_forms():
    global target_url
    url = raw_input("Enter the target url without http\n")
    target_url = url
    response = request(target_url)
    parsed_html = BeautifulSoup(response.content, features="lxml")
    forms_list  = parsed_html.findAll("form")

    for form in forms_list:
        action = form.get("action")
        post_url = urlparse.urljoin(target_url, action)
        # print(action)
        method = form.get("method")
        # print(method)

        inputs_list = form.findAll("input")
        post_data = {}
        for input in inputs_list:
            input_name = input.get("name")
            input_type = input.get("type")
            input_value = input.get("value")
            if input_type == "text":
                input_value = "test"

            post_data[input_name] = input_value

        requests.post(post_url, data=post_data)


extract_forms()