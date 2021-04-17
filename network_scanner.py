import scapy.all as scapy
import requests
import time
import os




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


def result(result_list):
    for client in result_list:
        print(client["ip"] + "\t" + client["mac"] + "\t" + client["mac_vendor"])


if os.geteuid() != 0:
	print("You need root privileges to run this script!")

else:
    ip_address = input("Enter the ip address and range that you want to scan(ex: 192.168.1.1/24): ")
    print("______________________________________________________")
    print(" IP\t\t MAC Address\t\t MAC Vendor")
    print("------------------------------------------------------")
    scan_result = scan(ip_address)
    result(scan_result)
	
