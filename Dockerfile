FROM kalilinux/kali-rolling
ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /home/stalker
RUN apt-get -y update && apt-get -y dist-upgrade && apt-get -y autoremove && apt-get clean
RUN apt-get install -y apt-utils
RUN apt-get update && apt-get install -y apt-utils 2>&1 | \grep -v "^debconf: delaying package configuration, since apt-utils.*"
RUN apt-get -y install net-tools

#RUN apt-get install python python3-pip

RUN apt-get -y install pciutils usbutils
COPY stalker_main.py .
COPY requirements.txt .
COPY arp_spoof.py .
COPY mac_changer.py .
COPY network_scanner.py .
COPY packet_sniffer.py .
COPY arp_spoof_detector.py .
COPY subdomain_scanner.py .
COPY subdomain.txt .
COPY url_extractor.py .

#RUN pip install -r requirements.txt

#File will be run from here onwards
ENTRYPOINT ["/bin/zsh"]
