#!/bin/python3

import os

f = open("s1.log", 'r')
lines = f.readlines()
c0 = 0;
c1 = 0;
c2 = 0;
c3 = 0;
c4 = 0;
c5 = 0;
c6 = 0;
c7 = 0;
c8 = 0;
c9 = 0;

for l in lines:

    t = int(l[62:63])

    if t == 0:
        c0 = int(l[74:])

    elif t == 1:
        c1 = int(l[74:])

    elif t == 2:
        c2 = int(l[74:])

    elif t == 3:
        c3 = int(l[74:])

    elif t == 4:
        c4 = int(l[74:])

    elif t == 5:
        c5 = int(l[74:])

    elif t == 6:
        c6 = int(l[74:])

    elif t == 7:
        c7 = int(l[74:])

    elif t == 8:
        c8 = int(l[74:])


    elif t == 9:
        c9 = int(l[74:])


    else:
        pass

print("Class 0:", c0)
print("Class 1:", c1)
print("Class 2:", c2)
print("Class 3:", c3)
print("Class 4:", c4)
print("Class 5:", c5)
print("Class 6:", c6)
print("Class 7:", c7)
print("Class 8:", c8)
print("Class 9:", c9)
