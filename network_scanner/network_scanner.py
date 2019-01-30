#!/usr/bin/env python
import scapy.all as scapy
import argparse


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list


def print_result(results_list):
    print("IP\t\t\tMAC Address\n")
    print("----------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])


def simple_scan(ip):
    scapy.arping(ip)


def create_argument_parser(argument_name):
    argument_parser = argparse.ArgumentParser(description="Get IP address range")
    argument_parser.add_argument("--" + argument_name)
    return argument_parser


def parse_ip_from_input(parser):
    args = parser.parse_args()
    return args.target


ip_range = parse_ip_from_input(
    create_argument_parser(
        argument_name="target"
    ))
scan_result = scan(ip_range)
print_result(scan_result)
