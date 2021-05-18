import scapy.all as scapy
import os
import sys


def become_root():
    euid = os.geteuid()
    if euid != 0:
        print("Script not started as root. Running sudo..")
        args = ['sudo', sys.executable] + sys.argv + [os.environ]
        os.execlpe('sudo', *args)

    print('Running. Your euid is', + euid)
    print("---------------------------------------------------------")


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast_frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_ether_broadcast = broadcast_frame / arp_request
    answered_list = scapy.srp(arp_ether_broadcast, timeout=1, verbose=False)[0]  # we need only answered list
    client_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        client_list.append(client_dict)
    return client_list


def print_result(result_list):
    print("IP\t\t\tMAC Address\n---------------------------------------------------------")
    for client in result_list:
        print(client["ip"] + "\t\t" + client["mac"])


def scan_network():
    become_root()
    target_ip_range = input("Enter the target IP range you want to scan (eg - 10.0.2.1/24) :")
    scan_result = scan(target_ip_range)
    print_result(scan_result)

