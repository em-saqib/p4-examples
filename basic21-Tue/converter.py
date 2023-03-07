

import argparse
import os
import json
import re
import sys
from time import sleep
import grpc
import time
import random
import numpy as np

inputfile = './tree.txt'
actionfile = './action.txt'

t1 = []   # Feature 1
t2 = []   # Feature 2
t3 = []   # Feature 3
t4 = []   # Feature 4
t5 = []   # Class IDs


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
    sa = re.findall('\d+', line)
    line = f.readline()
    sb = re.findall('\d+', line)
    line = f.readline()
    sc = re.findall('\d+', line)
    line = f.readline()
    sd = re.findall('\d+', line)
    f.close
    sa = [int(i) for i in sa]
    sb = [int(i) for i in sb]
    sc = [int(i) for i in sc]
    sd = [int(i) for i in sd]

    return sa, sb, sc, sd

def find_classification(textfile, sa, sb, sc, sd):
    fea = []
    sign = []
    num = []
    f = open(textfile, 'r')
    for line in f:
        n = re.findall(r"when", line)
        if n:
            fea.append(re.findall(r"(sa|sb|sc|sd)", line))
            sign.append(re.findall(r"(<=|>)", line))
            num.append(re.findall(r"\d+\.?\d*", line))
    f.close()

    size1 = []
    size2 = []
    size3 = []
    size4 = []
    classfication = []

    for i in range(len(fea)):
        feature1 = [k for k in range(len(sa) + 1)]
        feature2 = [k for k in range(len(sb) + 1)]
        feature3 = [k for k in range(len(sc) + 1)]
        feature4 = [k for k in range(len(sd) + 1)]
        #print(feature2)
        for j, feature in enumerate(fea[i]):
            if feature == 'sa':
                sig = sign[i][j]
                thres = int(float(num[i][j]))
                id = sa.index(thres)
                if sig == '<=':
                    while id < len(sa):
                        if id + 1 in feature1:
                            feature1.remove(id + 1)
                        id = id + 1
                else:
                    while id >= 0:
                        if id in feature1:
                            feature1.remove(id)
                        id = id - 1
            elif feature == 'sb':
                sig = sign[i][j]
                thres = int(float(num[i][j]))
                #print(num[i][j])
                id = sb.index(thres)
                if sig == '<=':
                    while id < len(sb):
                        if id + 1 in feature2:
                            feature2.remove(id + 1)
                        id = id + 1
                else:
                    while id >= 0:
                        if id in feature2:
                            feature2.remove(id)
                        id = id - 1

            elif feature == 'sc':
                sig = sign[i][j]
                thres = int(float(num[i][j]))
                id = sc.index(thres)
                if sig == '<=':
                    while id < len(sc):
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
                id = sd.index(thres)
                if sig == '<=':
                    while id < len(sd):
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
        para = {"scAddr": "00:00:00:02:02:00", "port": 2}
    elif action == 3:
        para = {"scAddr": "00:00:00:03:03:00", "port": 3}
    elif action == 4:
        para = {"scAddr": "00:00:00:04:04:00", "port": 4}

    return para



sa, sb, sc, sd = find_feature(inputfile)
size1, size2, size3, size4, classfication = find_classification(inputfile, sa, sb, sc, sd)
action = find_action(actionfile)

def unique(t5):  # for identifying unique classes
    x = np.array(t5)

def main():

    # Open file to write the outputs
    file_obj = open("rules.cmd", "w")
    file_obj.truncate()

    for i in range(len(classfication)):   # to run for all classes

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


    # Generate entries for table 1
    if len(sa) != 0:
        sa.append(0)
        sa.append(1500)
        sa.sort()
        for i in range(len(sa) - 1):
            #print(sa[i:i + 2], i + 1)

            a = "table_add feature"
            b = 1                             # table id
            c = "_exact set_actionselect"
            d = 1                             # action id
            e = " "
            f = '%s%d%s%d%s' % (a,b,c,d,e)    # table and action identifier
            x = sa[i:i+2]
            l = x[0]    # lower range of match
            h = x[1]    # higher range of match
            k = i + 1   # entry index in table
            p = " "      # space
            q = 1        # priority of entry
            m = "->"
            n = " => "
            ln = "\n"
            w = '%s%d%s%d%s%d%s%d%s' % (f,l,m,h,n,k,p,q,ln)
            #print(w)
            file_obj.write(w)


    # Generate entries for table 2
    if len(sb) != 0:
        sb.append(0)
        sb.append(1500)
        sb.sort()
        for i in range(len(sb) - 1):
            a = "table_add feature"
            b = 2   # table id
            c = "_exact set_actionselect"
            d = 2   # action id
            e = " "
            f = '%s%d%s%d%s' % (a,b,c,d,e)
            x = sb[i:i+2]
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

    # Generate entries for table 3
    if len(sc) != 0:
        sc.append(0)
        sc.append(1500)
        sc.sort()
        for i in range(len(sc) - 1):
            a = "table_add feature"
            b = 3
            c = "_exact set_actionselect"
            d = 3
            e = " "
            f = '%s%d%s%d%s' % (a,b,c,d,e)
            x = sc[i:i+2]
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

    # Generate entries for table 4
    if len(sd) != 0:
        sd.append(0)
        sd.append(1500)
        sd.sort()
        for i in range(len(sd) - 1):
            a = "table_add feature"
            b = 4
            c = "_exact set_actionselect"
            d = 4
            e = " "
            f = '%s%d%s%d%s' % (a,b,c,d,e)
            x = sd[i:i+2]
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

    d = "table_add set_class_t set_class_a "
    #e = "08:00:00:00:02:22 "
    p = 1

    # Generate entries for forwarding table
    for i in range(len(classfication)):
        l = t1[i][0]
        h = t1[i][1]
        m = "->"
        w = '%d%s%d' % (l,m,h)  # first match entry
        #print(t1)

        l = t2[i][0]
        h = t2[i][1]
        m = "->"
        x = '%d%s%d' % (l,m,h) # second match entry

        l = t3[i][0]
        h = t3[i][1]
        m = "->"
        y = '%d%s%d' % (l,m,h)   # third match entry

        l = t4[i][0]
        h = t4[i][1]
        m = "->"
        z = '%d%s%d' % (l,m,h)  # fourth match entry

        c = t5[i]   # class id or port

        if c == 0:
            e = "08:00:00:00:00:00 "
        elif c == 1:
            e = "08:00:00:00:01:11 "
        elif c == 2:
            e = "08:00:00:00:02:22 "
        elif c == 3:
            e = "08:00:00:00:03:33 "
        elif c == 4:
            e = "08:00:00:00:04:44 "
        else:
            pass

        g = " "
        ge = " => "
        ln = "\n"
        ww = '%s%s%s%s%s%s%s%s%s%d%s%d%s' % (d,w,g,x,g,y,g,z,ge,c,g,p,ln) # to combine all for line
        #print(w)
        file_obj.write(ww)




if __name__ == '__main__':

    print("Start generating entries")
    main()
    print("Entries are successfully genereated!")
