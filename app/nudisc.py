#!/usr/bin/env python3
"""
nudisc is a network discovery tool that uses nmap for host scanning.
Copyright (C) 2021  Mike Pfeiffer

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import json
import xmltodict
import subprocess


def find_open_protocols(ip_range, ip_protocols):
    # change this if looking for a different status
    protocol_status = 'open'
    # nmap results as xml file
    output_filename = 'discovery/ipprotosweep'
    # nmap command flags invoked by subprocess
    nmap_proto_scan = [
        'nmap', '-sO', '-p', ip_protocols, ip_range, '--min-hostgroup', '128',
        '--min-rate', '4096', '-oA', output_filename
    ]
    # use host to run nmap process, write output to null
    subprocess.call(nmap_proto_scan, stdout=open(os.devnull, 'wb'))

    with open(output_filename + ".xml") as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
    xml_file.close()

    json_data = json.dumps(data_dict)
    parsed = json.loads(json_data)

    # Keys for retrieving host values
    host_list = parsed['nmaprun']['host']

    # Initialize a targets dictionary for holding results
    targets_dict = {}

    # Checks each host for open protocols
    for host in host_list:
        # Keys for retrieving protocols results
        protocol_list = host['ports']['port']
        # Checks every protocol status for a given host
        for protocol in protocol_list:
            # Keys for retrieving nmap's status for protocol
            protocol_state = protocol['state']['@state']
            protocol_name = protocol['service']['@name']
            # Checks if protocol is in desired state.
            if(protocol_status in protocol_state):
                host_details = host['address']
                if(type(host_details) is dict):
                    ipv4_addr = host_details['@addr']
                elif(type(host_details) is list):
                    # This occurs when a MAC address is present.
                    for addr_type in host_details:
                        if(addr_type['@addrtype'] == 'ipv4'):
                            ipv4_addr = addr_type['@addr']
                            break
                else:
                    ipv4_addr = ''

                # Once host is extracted update the targets dictionary.
                if protocol_name not in targets_dict:
                    targets_dict[protocol_name] = [ipv4_addr]
                else:
                    targets_dict[protocol_name].append(ipv4_addr)

    confirmed_protocols = []

    for key, value in targets_dict.items():
        filename = "targets/" + key + "_targets.txt"
        if key == "tcp" or key == "udp":
            confirmed_protocols.append(filename)
        with open(filename, "w") as target_file:
            for ip in value:
                target_file.write(ip + "\n")
        target_file.close()

    return confirmed_protocols


def find_open_ports(hit_list, tcp_ports, udp_ports):

    for target in hit_list:
        if "tcp" in target:
            nmap_port_scan = [
                'nmap', '-sS', '-n', '-p', tcp_ports, '-iL', target, '-oA',
                'discovery/tcp_scan_results'
            ]
            subprocess.call(nmap_port_scan, stdout=open(os.devnull, 'wb'))
        elif "udp" in target:
            nmap_port_scan = [
                'nmap', '-sU', '-n', '-p', udp_ports, '-iL', target, '-oA',
                'discovery/udp_scan_results'
            ]
            subprocess.call(nmap_port_scan, stdout=open(os.devnull, 'wb'))


if __name__ == '__main__':
    with open("scan.json") as scan_file:
        scan_dict = json.loads(scan_file.read())
        scan_file.close()

    ip_range = scan_dict["ipv4_range"]
    ip_protocols = scan_dict["ip_protocols"]
    tcp_ports = scan_dict["tcp_ports"]
    udp_ports = scan_dict["udp_ports"]

    confirmed_protocols = find_open_protocols(ip_range, ip_protocols)
    find_open_ports(confirmed_protocols, tcp_ports, udp_ports)
