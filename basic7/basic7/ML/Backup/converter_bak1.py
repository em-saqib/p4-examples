

import argparse
import os
import json
import re
import sys
from time import sleep
import grpc
import time
import random

inputfile = './tree.txt'
actionfile = './action.txt'

t1 = []
t2 = []
t3 = []
t4 = []


def find_action(textfile):
    action = []
    f = open(textfile)
    for line in f:
        n = re.findall(r"class", line)
        if n:
            fea = re.findall(r"\d", line)
            action.append(int(fea[1]))
    f.close()
    return action


def find_feature(textfile):
    f = open(textfile)
    line = f.readline()
    proto = re.findall('\d+', line)
    line = f.readline()
    src = re.findall('\d+', line)
    line = f.readline()
    dst = re.findall('\d+', line)
    f.close
    proto = [int(i) for i in proto]
    src = [int(i) for i in src]
    dst = [int(i) for i in dst]
    return proto, src, dst

def find_classification(textfile, proto, src, dst):
    fea = []
    sign = []
    num = []
    f = open(textfile, 'r')
    for line in f:
        n = re.findall(r"when", line)
        if n:
            fea.append(re.findall(r"(proto|src|dst)", line))
            sign.append(re.findall(r"(<=|>)", line))
            num.append(re.findall(r"\d+\.?\d*", line))
    f.close()

    protocol = []
    srouce = []
    dstination = []
    classfication = []

    for i in range(len(fea)):
        feature1 = [k for k in range(len(proto) + 1)]
        feature2 = [k for k in range(len(src) + 1)]
        feature3 = [k for k in range(len(dst) + 1)]
        for j, feature in enumerate(fea[i]):
            if feature == 'proto':
                sig = sign[i][j]
                thres = int(float(num[i][j]))
                id = proto.index(thres)
                if sig == '<=':
                    while id < len(proto):
                        if id + 1 in feature1:
                            feature1.remove(id + 1)
                        id = id + 1
                else:
                    while id >= 0:
                        if id in feature1:
                            feature1.remove(id)
                        id = id - 1
            elif feature == 'src':
                sig = sign[i][j]
                thres = int(float(num[i][j]))
                id = src.index(thres)
                if sig == '<=':
                    while id < len(src):
                        if id + 1 in feature2:
                            feature2.remove(id + 1)
                        id = id + 1
                else:
                    while id >= 0:
                        if id in feature2:
                            feature2.remove(id)
                        id = id - 1
            else:
                sig = sign[i][j]
                thres = int(float(num[i][j]))
                id = dst.index(thres)
                if sig == '<=':
                    while id < len(dst):
                        if id + 1 in feature3:
                            feature3.remove(id + 1)
                        id = id + 1
                else:
                    while id >= 0:
                        if id in feature3:
                            feature3.remove(id)
                        id = id - 1

        protocol.append(feature1)
        srouce.append(feature2)
        dstination.append(feature3)
        a = len(num[i])
        classfication.append(num[i][a - 1])
    return (protocol, srouce, dstination, classfication)

def get_actionpara(action):
    para = {}
    if action == 0:
        para = {}
    elif action == 2:
        para = {"dstAddr": "00:00:00:02:02:00", "port": 2}
    elif action == 3:
        para = {"dstAddr": "00:00:00:03:03:00", "port": 3}
    elif action == 4:
        para = {"dstAddr": "00:00:00:04:04:00", "port": 4}

    return para



proto, src, dst = find_feature(inputfile)
protocol, srouce, dstination, classfication = find_classification(inputfile, proto, src, dst)
action = find_action(actionfile)


def main():

    # Open file to write the outputs
    file_obj = open("output.txt", "w")
    file_obj.truncate()

    for i in range(len(classfication)):

        a = protocol[i]
        #print("a:" , a)
        id = len(a) - 1
        del a[1:id]
        if (len(a) == 1):
            a.append(a[0])
        b = srouce[i]
        id = len(b) - 1
        del b[1:id]
        if (len(b) == 1):
            b.append(b[0])
        c = dstination[i]
        id = len(c) - 1
        del c[1:id]
        if (len(c) == 1):
            c.append(c[0])

        ind = int(classfication[i])
        ac = action[ind]
        a = [i + 1 for i in a]
        b = [i + 1 for i in b]
        c = [i + 1 for i in c]

        t1.append(a)
        t2.append(b)
        t3.append(c)
        t4.append(ac)
        #print(t1)


    print("Entries generation....")

    d = "table_add ipv4_exact ipv4_forward "
    e = "08:00:00:00:02:22 "
    p = 1

    for i in range(len(classfication)):   # should be equal to length of classification entries
        l = t1[i][0]
        h = t1[i][1]
        m = "->"
        x = '%d%s%d' % (l,m,h)

        l = t2[i][0]
        h = t2[i][1]
        m = "->"
        y = '%d%s%d' % (l,m,h)

        l = t3[i][0]
        h = t3[i][1]
        m = "->"
        z = '%d%s%d' % (l,m,h)

        c = t4[i]
        #print(c)  # class id or port

        g = " "
        ge = " => "
        ln = "\n"
        w = '%s%s%s%s%s%s%s%s%d%s%d%s' % (d,x,g,y,g,z,ge,e,c,g,p,ln)
        #print(w)
        file_obj.write(w)


    if len(proto) != 0:
        proto.append(0)
        proto.append(1500)
        proto.sort()
        for i in range(len(proto) - 1):
            #print(proto[i:i + 2], i + 1)

            a = "table_add feature"
            b = 1                             # table id
            c = "_exact set_actionselect"
            d = 1                             # action id
            e = " "
            f = '%s%d%s%d%s' % (a,b,c,d,e)
            x = proto[i:i+2]
            l = x[0]
            h = x[1]
            k = i + 1
            p = " "
            q = 1
            m = "->"
            n = " => "
            ln = "\n"
            w = '%s%d%s%d%s%d%s%d%s' % (f,l,m,h,n,k,p,q,ln)
            #print(w)
            file_obj.write(w)


    if len(src) != 0:
        src.append(0)
        src.append(1500)
        src.sort()
        for i in range(len(src) - 1):
            a = "table_add feature"
            b = 2
            c = "_exact set_actionselect"
            d = 2
            e = " "
            f = '%s%d%s%d%s' % (a,b,c,d,e)
            x = src[i:i+2]
            l = x[0]
            h = x[1]
            k = i + 1
            p = " "
            q = 1
            m = "->"
            n = " => "
            ln = "\n"
            w = '%s%d%s%d%s%d%s%d%s' % (f,l,m,h,n,k,p,q,ln)
            #print(w)
            file_obj.write(w)

    if len(dst) != 0:
        dst.append(0)
        dst.append(1500)
        dst.sort()
        for i in range(len(dst) - 1):
            a = "table_add feature"
            b = 3
            c = "_exact set_actionselect"
            d = 3
            e = " "
            f = '%s%d%s%d%s' % (a,b,c,d,e)
            x = dst[i:i+2]
            l = x[0]
            h = x[1]
            k = i + 1
            p = " "
            q = 1
            m = "->"
            n = " => "
            ln = "\n"
            w = '%s%d%s%d%s%d%s%d%s' % (f,l,m,h,n,k,p,q,ln)
            #print(w)
            file_obj.write(w)


if __name__ == '__main__':

    main()
    print("Successfully generated!")
