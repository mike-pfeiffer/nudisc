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


def find_open_protocols():
    # change this if looking for a different status
    protocol_status = 'open'
    # icmp, udp, tcp
    ip_protocols = '1,6,17'
    ip_range = '192.168.0.0/16'
    # nmap results as xml file
    output_filename = 'discovery/ipprotosweep.xml'
    # nmap command flags invoked by subprocess
    nmap_proto_scan = [
        'nmap', '-sO', '-p', ip_protocols, ip_range, '--min-hostgroup', '128',
        '--min-rate', '4096', '-oX', output_filename
    ]
    # use host to run nmap process, write output to null
    subprocess.call(nmap_proto_scan, stdout=open(os.devnull, 'wb'))

    # TODO make sure this handles file exceptions properly
    with open(output_filename) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
        xml_file.close()

    # TODO should I add logic to exit if data dict is empty?
    if(data_dict):
        print("yo")

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
            protocol_name = ''
            # Checks if protocol is in desired state.
            if(protocol_state == protocol_status):
                protocol_name = protocol['service']['@name']
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
                if not protocol_name:
                    continue
                elif protocol_name not in targets_dict:
                    targets_dict[protocol_name] = [ipv4_addr]
                else:
                    targets_dict[protocol_name].append(ipv4_addr)

    for key, value in targets_dict.items():
        with open("./targets/" + key + "_targets.txt", "w") as target_file:
            for ip in value:
                target_file.write(ip + "\n")
            target_file.close()


if __name__ == '__main__':
    find_open_protocols()
