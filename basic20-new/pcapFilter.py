#!/bin/python3

from scapy.utils import rdpcap, wrpcap
from scapy.all import *

pkts = rdpcap('pcap/iot1.pcap')
ports = ['44:65:0d:56:cc:d3', '00:16:6c:ab:6b:88', 'ec:1a:59:83:28:11', '70:ee:50:03:b8:ac' 'e0:76:d0:33:bb:85']   # Only keep these packets : 5 classes
filtered = (pkt for pkt in pkts if
    Ether in pkt and
    (pkt[Ether].src in ports))
wrpcap('pcap/filtered.pcap', filtered)
