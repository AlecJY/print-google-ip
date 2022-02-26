#!/usr/bin/env python3
import argparse
import json
import requests
from ipaddress import ip_network

GOOGLE_IP_URL = 'https://www.gstatic.com/ipranges/goog.json'
GOOGLE_DNS = ['8.8.8.8', '8.8.4.4', '2001:4860:4860::8888', '2001:4860:4860::8844']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--exclude-dns", help="exclude the IPs of Google Public DNS", action="store_true")
    args = parser.parse_args()

    exclude_ips = []
    for ip in GOOGLE_DNS:
        exclude_ips.append(ip_network(ip))

    ips = []
    r = requests.get(GOOGLE_IP_URL)
    ip_list = json.loads(r.text)
    for prefix in ip_list["prefixes"]:
        for ip in prefix.values():
            if args.exclude_dns:
                addresses = [ip_network(ip)]
                for exclude_ip in exclude_ips:
                    for index, address in enumerate(addresses):
                        if address.overlaps(exclude_ip):
                            addresses.pop(index)
                            addresses.extend(list(address.address_exclude(exclude_ip)))
                ips.extend(addresses)
            else:
              ips.append(ip)
    print(ips[0], end='')
    for ip in ips[1:]:
        print(',', ip, end='')
    print()

if __name__ == '__main__':
    main()
