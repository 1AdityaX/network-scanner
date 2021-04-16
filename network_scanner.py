


# with mac_vendor

import scapy.all as scapy
import requests
import time
import optparse
import os


ip_address = "192.168.1.1/24"


def parse_args():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="ip", help="[-] Enter the target, type --help for more info.")
    return parser.parse_args()


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    client_list = []
    for element in answered_list:
        mac_list = [element[1].hwsrc]
        for address in mac_list:

            vendor = requests.get('http://api.macvendors.com/' + address).text
            time.sleep(1)
            client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc, "mac_vendor": vendor}
            client_list.append(client_dict)
    return client_list


def print_result(result_list):
    for client in result_list:
        print(client["ip"] + "\t" + client["mac"] + "\t" + client["mac_vendor"])
if os.geteuid() != 0:
	print("You need root privileges to run this script!")

else:
	try:
		print("______________________________________________________")
		print(" IP\t\t MAC Address\t\t MAC Vendor")
		print("------------------------------------------------------")
		scan_result = scan(ip_address)
		print_result(scan_result)
	except:
	    options = parse_args()
	    scan_results = scan("192.164.1.1/24")
	    print_result(scan_results)
