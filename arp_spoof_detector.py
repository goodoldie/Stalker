import scapy.all as scapy
import os
import sys
import netifaces


def become_root():
    euid = os.geteuid()
    if euid != 0:
        print("Script not started as root. Running sudo..")
        args = ['sudo', sys.executable] + sys.argv + [os.environ]
        os.execlpe('sudo', *args)

    print('Running. Your euid is', + euid)
    print("---------------------------------------------------------")


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast_frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_ether_broadcast = broadcast_frame / arp_request
    answered_list = scapy.srp(arp_ether_broadcast, timeout=1, verbose=False)[0]  # we need only answered list
    return answered_list[0][1].hwsrc


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=processed_sniffed_packet)


def processed_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc

            if real_mac != response_mac:
                print("[+] !!!!!!!You are under attack!!!!!")

        except IndexError:
            # unable to find the real mac
            pass


def run_spoof_detector():
    become_root()
    interfaces = netifaces.interfaces()
    print("Availabe Interfaces :")
    print(interfaces)
    interface = input("Enter the interface ")
    if interface not in interfaces:
        print("Pleas Enter a valid Interface!!")
    else:
        print("ARP Spoof Detector ON!!!")
        sniff(interface)

