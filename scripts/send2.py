#!/usr/bin/env python3
import argparse
import sys
import socket
import random
import struct
import time

from scapy.all import sendp, send, get_if_list, get_if_hwaddr
from scapy.all import Packet
from scapy.all import Ether, IP, UDP, TCP

import numpy as np
import pandas as pd


df = pd.read_csv('pPacket1.csv')

def get_if():
    ifs=get_if_list()
    iface=None # "h1-eth0"
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break;
    if not iface:
        print("Cannot find eth0 interface")
        exit(1)
    return iface

def main():

    if len(sys.argv)<2:
        print('pass 1 arguments: <destination>')
        exit(1)

    addr = socket.gethostbyname(sys.argv[1])
    iface = get_if()

    print(("sending on interface %s to %s" % (iface, str(addr))))

    for i in range(len(df)):
    # for i in range(30000):
      payload=""
      for j in range (0,df['Size'][i]-53):
        payload += "a"
      print("size of the packet : ",df['Size'][i])

      pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
      pkt = pkt /IP(dst=addr) / TCP(dport=df['dPort'][i], sport=df['sPort'][i]) / payload
      pkt.show2()
      sendp(pkt, iface=iface, verbose=False)
      print("we are sending the packets ",i)
      # print(str((i/18896)*100)+"%")
      #time.sleep(0.5)


if __name__ == '__main__':
    main()
