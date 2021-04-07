import subprocess  # For Running System commands, import subprocess module
import argparse  # For Commandline arguments, import optparse
import re  # For regex expression checking
import netifaces


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Interface Name whose MAC address is to be changed")
    parser.add_argument("-m", "--mac", dest="new_mac", help="New MAC address of the Interface")
    options = parser.parse_args()
    if not options.interface:
        parser.error("Please specify an interface, use --help or -h for more info.")
    elif not options.new_mac:
        parser.error("Please specify a new MAC address, use --help or -h for more info.")
    return options


def is_valid_interface(interface):
    interfaces = netifaces.interfaces()
    print(interfaces)
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
    subprocess.run(["sudo", "ifconfig", interface, "down"])
    subprocess.run(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.run(["sudo", "ifconfig", interface, "up"])


def get_current_mac(interface):
    verify_result = subprocess.check_output(["ifconfig", interface])
    new_mac_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(verify_result))
    if new_mac_search:
        return new_mac_search.group(0)  # We need only the first occurrence of the new MAC
    else:
        print("[-] Could not read a valid MAC address!")


def change_mac():
    option = get_arguments()
    current_mac = get_current_mac(option.interface)
    print("Current MAC address = " + str(current_mac))
    change_mac_util(option.interface, option.new_mac)
    current_mac = str(get_current_mac(option.interface))
    if current_mac == option.new_mac:
        print("[+] MAC address was changed successfully to " + current_mac)
    else:
        print("[-] MAC address was not changed!!")


change_mac()
