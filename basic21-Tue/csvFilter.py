#!/usr/bin/env python3
import pandas as pd
import csv
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

df = pd.read_csv('s1.log', sep='\:', engine='python')
df.to_csv('my_file.csv', index=None)
df = pd.read_csv('my_file.csv', sep='\s+', engine='python')


# Rename the columns
df = df.set_axis(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'M'], axis=1, inplace=False)
df = df[['I','L', 'N']]
df['N']=df['N'].str.replace(',','')
df = df.astype(float)
df = df.mul(0.001)  # convert to milliseconds
df.to_csv('my_file.csv', index=None)

df.plot()
plt.savefig('foo.png')
