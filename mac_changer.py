import subprocess  # For Running System commands, import subprocess module
import argparse  # For Commandline arguments, import optparse
import re  # For regex expression checking
import netifaces
import logging

logging.basicConfig(filename='mac_changer.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def is_valid_interface(interface):
    interfaces = netifaces.interfaces()
    return interface in interfaces


def change_mac_util(interface, new_mac):
    if not is_valid_interface(interface):
        print("[-] {} is not a valid interface!!".format(interface))
        exit(0)
    curr_mac = get_current_mac(interface)
    if curr_mac == new_mac:
        print("[-] The Current MAC address is same as the new MAC address " +curr_mac)
        exit(0)
    print("Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])


def get_current_mac(interface):
    verify_result = subprocess.check_output(["ifconfig", interface])
    new_mac_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(verify_result))
    if new_mac_search:
        return new_mac_search.group(0)  # We need only the first occurrence of the new MAC
    else:
        print("[-] Could not read a valid MAC address!")


def change_mac():
    interfaces = netifaces.interfaces()
    print(interfaces)
    interface = input("Enter the interface who's MAC address you want to change: ")
    new_mac = input("\nEnter the new MAC address: ")
    # option = get_arguments()
    current_mac = get_current_mac(interface)
    logging.debug("Current MAC address of the interface {}".format(current_mac))
    print("Current MAC address = " + str(current_mac))
    change_mac_util(interface, new_mac)
    current_mac = str(get_current_mac(interface))
    if current_mac == new_mac:
        print("[+] MAC address was changed successfully to " + current_mac)
        logging.debug("New MAC address entered {}".format(new_mac))
    else:
        print("[-] MAC address was not changed!!")

