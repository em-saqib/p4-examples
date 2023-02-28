import pandas as import pd
import csv

df = pd.read_csv('csv/labeledDataset.csv')

df1 = df[df['device name'] == 'Amazon Echo']
df2 = df[df['device name'] == 'Samsung SmartCam']
df3 = df[df['device name'] == 'Belkin wemo motion sensor']
df4 = df[df['device name'] == 'PIX-STAR Photo-frame']
df5 = df[df['device name'] == 'Netatmo weather station']

df6 = pd.concat([df1, df2, df3, df4, df5])

df6['device name'].value_counts()

df6 = df6.drop(['eth.src'],axis=1)
df6 = df6.drop(['eth.dst'],axis=1)
df6.to_csv('csv/labeled5Classes.csv')
