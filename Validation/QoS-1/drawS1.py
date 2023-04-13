#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('s1.csv')

# Packet drop rate
df2 = df.pivot_table(index = ['ClassID'], aggfunc ='size')

ax = sns.lineplot(x=df['Packet'], y=df['Delay (ms)'], hue=df['ClassID'], data=df)
plt.text(.27, .97, 'Packets', ha='right', va='top', transform=ax.transAxes)
plt.text(.27, .91, df2[0], ha='right', va='top', transform=ax.transAxes)
plt.text(.27, .85, df2[1], ha='right', va='top', transform=ax.transAxes)
plt.text(.27, .79, df2[2], ha='right', va='top', transform=ax.transAxes)
plt.text(.27, .74, df2[3], ha='right', va='top', transform=ax.transAxes)
plt.title('Switch-1')
#plt.ylim((0,10000))
plt.show()
