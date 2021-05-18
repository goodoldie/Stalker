import os
import mac_changer, network_scanner, arp_spoof, packet_sniffer, arp_spoof_detector, subdomain_scanner, url_extractor

os.system('cls' if os.name == 'nt' else 'clear')
art = """
     _______.___________.    ___       __       __  ___  _______ .______      
    /       |           |   /   \     |  |     |  |/  / |   ____||   _  \     
   |   (----`---|  |----`  /  ^  \    |  |     |  '  /  |  |__   |  |_)  |    
    \   \       |  |      /  /_\  \   |  |     |    <   |   __|  |      /     
.----)   |      |  |     /  _____  \  |  `----.|  .  \  |  |____ |  |\  \----.
|_______/       |__|    /__/     \__\ |_______||__|\__\ |_______|| _| `._____|


 """
print(art)
while True:
    print("\n\n\n")
    print("1. Change your MAC address")
    print("2. Scan a Network")
    print("3. ARP Spoofing (MITM)")
    print("4. Sniff http Packets")
    print("5. Check if you are under attack (ARP Spoof Detector)")
    print("6. Website Sub-Domain Scanner")
    print("7. Extract All URLs from a target website")
    print("8. Exit Program\n")

    choice = input("Enter your choice: ")
    if choice == '1':
        mac_changer.change_mac()
    elif choice == '2':
        network_scanner.scan_network()
    elif choice == '3':
        arp_spoof.run_spoof()
    elif choice == '4':
        packet_sniffer.run_sniff()
    elif choice == '5':
        arp_spoof_detector.run_spoof_detector()
    elif choice == '6':
        subdomain_scanner.run_subdomain_scan()
    elif choice == '7':
        url_extractor.run_crawler()
    elif choice == '8':
        break
    else:
        print("Please Enter a Valid Input")




