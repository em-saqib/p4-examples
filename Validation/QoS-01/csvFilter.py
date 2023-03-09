#!/usr/bin/env python3
import pandas as pd
import csv
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

df1 = pd.read_csv('s1.log', sep='\:', engine='python')
df1.to_csv('s1.csv', index=None)
df1 = pd.read_csv('s1.csv', sep='\s+', engine='python')

df2 = pd.read_csv('s2.log', sep='\:', engine='python')
df2.to_csv('s2.csv', index=None)
df2 = pd.read_csv('s2.csv', sep='\s+', engine='python')

df3 = pd.read_csv('s3.log', sep='\:', engine='python')
df3.to_csv('s3.csv', index=None)
df3 = pd.read_csv('s3.csv', sep='\s+', engine='python')


# Rename the columns
df1 = df1.set_axis(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'ClassID', 'J', 'K', 'Packet', 'M', 'N', 'O', 'P', 'Delay (ms)', 'R'], axis=1, inplace=False)
df1 = df1[['ClassID', 'Packet', 'Delay (ms)']]
df1['Delay (ms)']=df1['Delay (ms)'].str.replace(',','')
df1['Delay (ms)'] = df1['Delay (ms)'].astype(float)
df1['Delay (ms)'] = df1['Delay (ms)'].mul(0.001)  # convert to milliseconds

# Rename the columns
df2 = df2.set_axis(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'ClassID', 'J', 'K', 'Packet', 'M', 'N', 'O', 'P', 'Delay (ms)', 'R'], axis=1, inplace=False)
df2 = df2[['ClassID', 'Packet', 'Delay (ms)']]
df2['Delay (ms)']=df2['Delay (ms)'].str.replace(',','')
df2['Delay (ms)'] = df2['Delay (ms)'].astype(float)
df2['Delay (ms)'] = df2['Delay (ms)'].mul(0.001)  # convert to milliseconds

# Rename the columns
df3 = df3.set_axis(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'ClassID', 'J', 'K', 'Packet', 'M', 'N', 'O', 'P', 'Delay (ms)', 'R'], axis=1, inplace=False)
df3 = df3[['ClassID', 'Packet', 'Delay (ms)']]
df3['Delay (ms)']=df3['Delay (ms)'].str.replace(',','')
df3['Delay (ms)'] = df3['Delay (ms)'].astype(float)
df3['Delay (ms)'] = df3['Delay (ms)'].mul(0.001)  # convert to milliseconds

df1.to_csv('s1.csv', index=None)
df2.to_csv('s2.csv', index=None)
df3.to_csv('s3.csv', index=None)

# df1.plot()
#plt.savefig('foo.png')
