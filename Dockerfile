FROM python:3.8.10-buster
WORKDIR /app
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
RUN pip install -r requirements.txt

#File will be run from here onwards
ENTRYPOINT python stalker_main.py