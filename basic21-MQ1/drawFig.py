#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('my_file.csv')



ax = sns.lineplot(x=df['L'], y=df['Q'], hue=df['I'], data=df)
plt.show()
