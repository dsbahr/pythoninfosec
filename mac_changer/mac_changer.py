#!/usr/bin/env python

import subprocess
import argparse
import re


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + str(new_mac))

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", str(new_mac)])
    subprocess.call(["ifconfig", interface, "up"])


def get_arguments():
    argument_parser = argparse.ArgumentParser(description="Change MAC address")
    argument_parser.add_argument("-i", "--interface", help="The target interface", dest="interface")
    argument_parser.add_argument("-m", "--mac",  help="The new mac address", dest="new_mac")
    options = argument_parser.parse_args()
    if not options.interface:
        argument_parser.error("[-] No interface found")
    elif not options.new_mac:
        argument_parser.error("[-] No valid MAC address was defined")
    return options


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search("\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address")


options = get_arguments()

current_mac = get_current_mac(options.interface)
print("[+] Current MAC = " + str(current_mac))

change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed.")

