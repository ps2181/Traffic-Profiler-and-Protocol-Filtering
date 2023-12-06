import argparse
import json

from scapy import plist
from scapy.all import *


app_filters = {'ftp': 'tcp port 21', 'http': 'tcp port 80', 'telnet': 'tcp port 23','HTTP':'tcp port 80','DNS':'tcp port 53','ICMP':'tcp port 8'}


def profile_sessions(pcap_reader):
    packets = []
    print('Getting details from packets.')
    first_timestamp = None
    last_timestamp = None
    for packet in pcap_reader:
        if IP not in packet:
            continue
        if TCP not in packet:
            continue
        if not first_timestamp:
            first_timestamp = packet.time
        if not last_timestamp:
            last_timestamp = packet.time
        if packet.time < first_timestamp:
            first_timestamp = packet.time
        elif packet.time > last_timestamp:
            last_timestamp = packet.time
        packets.append(packet)
    packets = plist.PacketList(packets)
    print('Analyzing sessions.')
    sessions = packets.sessions()
    profile = {'start_timestamp': float(first_timestamp), 'end_timestamp': float(last_timestamp),
               'duration_secs': float(last_timestamp - first_timestamp), 'total_packets': len(packets),
               'total_sessions': len(sessions)}
    profile['avg_pps'] = profile['duration_secs'] / profile['total_packets']
    profile['packets_to_sessions_ratio'] = profile['total_packets'] / profile['total_sessions']
    return profile

def filter_http(packets,methods):
    filtered_packets=[]
    for packet in packets:
        if TCP not in packet:
            continue
        if HTTP not in packet:
            continue
        if packet[HTTP].Method.decode() in methods():
            filtered_packets.append(packet)
    return filtered_packets


def filter_dns(packets, query_types):

  filtered_packets = []
  for packet in packets:
    if UDP not in packet:
      continue
    if DNS not in packet:
      continue
    if packet[DNS].qr == 0 and packet[DNS].qd[0].qtype in query_types:
      filtered_packets.append(packet)
  return filtered_packets

def filter_icmp(packets, message_types):

  filtered_packets = []
  for packet in packets:
    if IP not in packet:
      continue
    if ICMP not in packet:
      continue
    if packet[ICMP].type in message_types:
      filtered_packets.append(packet)
  return filtered_packets



def main():
    parser = argparse.ArgumentParser(
        description='This application calculates a network traffic profile for a specific host from a provided PCAP file.')
    parser.add_argument('-a', '--application', help='Application to filter packets for',
                        choices=list(app_filters.keys()))
    parser.add_argument('-i', '--ip', help='IP address to filter packets for (source or destination)', required=True)
    parser.add_argument('-o', '--output', help='Output file to write to')
    parser.add_argument('pcap_file', help='PCAP file to read packets from')
    args = parser.parse_args()

    application = args.application
    if application:
        packet_filter = app_filters[application]
        packet_filter = '{} and host {}'.format(packet_filter, args.ip)
    else:
        packet_filter = 'host {}'.format(args.ip)
    pcap_file = args.pcap_file
    output = args.output

    # read and analyze packets
    print('Starting to read packets from file with filter "{}".'.format(packet_filter))
    with PcapReader(tcpdump(pcap_file, args=["-w", "-", packet_filter], getfd=True)) as pcap_reader:
        profile = profile_sessions(pcap_reader)

    if output:
        with open(output, 'w') as of:
            json.dump(profile, of, indent=2)
    else:
        print(json.dumps(profile, indent=2))


if __name__ == '__main__':
    main()