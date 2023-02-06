

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
t5 = []


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
    s1 = re.findall('\d+', line)
    line = f.readline()
    s2 = re.findall('\d+', line)
    line = f.readline()
    s3 = re.findall('\d+', line)
    line = f.readline()
    s4 = re.findall('\d+', line)
    f.close
    s1 = [int(i) for i in s1]
    s2 = [int(i) for i in s2]
    s3 = [int(i) for i in s3]
    s4 = [int(i) for i in s4]
    return s1, s2, s3, s4

def find_classification(textfile, s1, s2, s3, s4):
    fea = []
    sign = []
    num = []
    f = open(textfile, 'r')
    for line in f:
        n = re.findall(r"when", line)
        if n:
            fea.append(re.findall(r"(s1|s2|s3|s4)", line))
            sign.append(re.findall(r"(<=|>)", line))
            num.append(re.findall(r"\d+\.?\d*", line))
    f.close()

    size1 = []
    size2 = []
    size3 = []
    size4 = []
    classfication = []

    for i in range(len(fea)):
        feature1 = [k for k in range(len(s1) + 1)]
        feature2 = [k for k in range(len(s2) + 1)]
        feature3 = [k for k in range(len(s3) + 1)]
        feature4 = [k for k in range(len(s4) + 1)]
        #print(feature2)
        for j, feature in enumerate(fea[i]):
            if feature == 's1':
                sig = sign[i][j]
                thres = int(float(num[i][j]))
                id = s1.index(thres)
                if sig == '<=':
                    while id < len(s1):
                        if id + 1 in feature1:
                            feature1.remove(id + 1)
                        id = id + 1
                else:
                    while id >= 0:
                        if id in feature1:
                            feature1.remove(id)
                        id = id - 1
            elif feature == 's2':
                sig = sign[i][j]
                thres = int(float(num[i][j]))
                #print(num[i][j])
                id = s2.index(thres)
                if sig == '<=':
                    while id < len(s2):
                        if id + 1 in feature2:
                            feature2.remove(id + 1)
                        id = id + 1
                else:
                    while id >= 0:
                        if id in feature2:
                            feature2.remove(id)
                        id = id - 1

            elif feature == 's3':
                sig = sign[i][j]
                thres = int(float(num[i][j]))
                id = s3.index(thres)
                if sig == '<=':
                    while id < len(s3):
                        if id + 1 in feature3:
                            feature3.remove(id + 1)
                        id = id + 1
                else:
                    while id >= 0:
                        if id in feature3:
                            feature3.remove(id)
                        id = id - 1
            else:
                sig = sign[i][j]
                thres = int(float(num[i][j]))
                id = s4.index(thres)
                if sig == '<=':
                    while id < len(s4):
                        if id + 1 in feature4:
                            feature4.remove(id + 1)
                        id = id + 1
                else:
                    while id >= 0:
                        if id in feature4:
                            feature4.remove(id)
                        id = id - 1

        size1.append(feature1)
        size2.append(feature2)
        size3.append(feature3)
        size4.append(feature4)
        a = len(num[i])
        classfication.append(num[i][a - 1])
    return (size1, size2, size3, size4, classfication)

def get_actionpara(action):
    para = {}
    if action == 0:
        para = {}
    elif action == 2:
        para = {"s3Addr": "00:00:00:02:02:00", "port": 2}
    elif action == 3:
        para = {"s3Addr": "00:00:00:03:03:00", "port": 3}
    elif action == 4:
        para = {"s3Addr": "00:00:00:04:04:00", "port": 4}

    return para



s1, s2, s3, s4 = find_feature(inputfile)
size1, size2, size3, size4, classfication = find_classification(inputfile, s1, s2, s3, s4)
action = find_action(actionfile)


def main():

    # Open file to write the outputs
    file_obj = open("output.txt", "w")
    file_obj.truncate()

    for i in range(len(classfication)):

        aa = size1[i]
        #print("a:" , a)
        id = len(aa) - 1
        del aa[1:id]
        if (len(aa) == 1):
            aa.append(aa[0])
        bb = size2[i]
        id = len(bb) - 1
        del bb[1:id]
        if (len(bb) == 1):
            bb.append(bb[0])
        cc = size3[i]
        id = len(cc) - 1
        del cc[1:id]
        if (len(cc) == 1):
            cc.append(cc[0])
        dd = size4[i]
        id = len(dd) - 1
        del dd[1:id]
        if (len(dd) == 1):
            dd.append(dd[0])

        ind = int(classfication[i])
        ac = action[ind]
        aa = [i + 1 for i in aa]
        bb = [i + 1 for i in bb]
        cc = [i + 1 for i in cc]
        dd = [i + 1 for i in dd]

        t1.append(aa)
        t2.append(bb)
        t3.append(cc)
        t4.append(dd)
        t5.append(ac)  # actions


    print("Tables....")
    print("Table 1:", t1)
    print("Table 2:", t2)
    print("Table 3:", t3)
    print("Table 3:", t4)
    print("Table 4:", t5)


    d = "table_add ipv4_exact ipv4_forward "
    e = "08:00:00:00:02:22 "
    p = 1

    for i in range(7):
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

        l = t4[i][0]
        h = t4[i][1]
        m = "->"
        z = '%d%s%d' % (l,m,h)

        c = t5[i]   # class id or port

        g = " "
        ge = " => "
        ln = "\n"
        w = '%s%s%s%s%s%s%s%s%d%s%d%s' % (d,x,g,y,g,z,ge,e,c,g,p,ln)
        #print(w)
        file_obj.write(w)


    if len(s1) != 0:
        s1.append(0)
        s1.append(1500)
        s1.sort()
        for i in range(len(s1) - 1):
            #print(s1[i:i + 2], i + 1)

            a = "table_add feature"
            b = 1                             # table id
            c = "_exact set_actionselect"
            d = 1                             # action id
            e = " "
            f = '%s%d%s%d%s' % (a,b,c,d,e)    # table and action identifier
            x = s1[i:i+2]
            l = x[0]    # lower range of match
            h = x[1]    # higher range of match
            k = i + 1   # index for iteration
            p = " "      # space
            q = 1        # priority of entry
            m = "->"
            n = " => "
            ln = "\n"
            w = '%s%d%s%d%s%d%s%d%s' % (f,l,m,h,n,k,p,q,ln)
            #print(w)
            file_obj.write(w)


    if len(s2) != 0:
        s2.append(0)
        s2.append(1500)
        s2.sort()
        for i in range(len(s2) - 1):
            a = "table_add feature"
            b = 2   # table id
            c = "_exact set_actionselect"
            d = 2   # action id
            e = " "
            f = '%s%d%s%d%s' % (a,b,c,d,e)
            x = s2[i:i+2]
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

    if len(s3) != 0:
        s3.append(0)
        s3.append(1500)
        s3.sort()
        for i in range(len(s3) - 1):
            a = "table_add feature"
            b = 3
            c = "_exact set_actionselect"
            d = 3
            e = " "
            f = '%s%d%s%d%s' % (a,b,c,d,e)
            x = s3[i:i+2]
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

    if len(s4) != 0:
        s4.append(0)
        s4.append(1500)
        s4.sort()
        for i in range(len(s4) - 1):
            a = "table_add feature"
            b = 4
            c = "_exact set_actionselect"
            d = 4
            e = " "
            f = '%s%d%s%d%s' % (a,b,c,d,e)
            x = s4[i:i+2]
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
