import csv

labeledDataset = "csv/labeled5Classes.csv"

labeledFlows = {}


Xx = []
Yy = []
with open(labeledDataset) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader :
        if line_count == 0 :
            line_count += 1
            continue
        # print(row[6],row[7])
        if (row[7],row[8]) not in labeledFlows :
            labeledFlows[(row[7],row[8])] = []
        if len(labeledFlows[(row[7],row[8])]) < 4 :          # indicate input length
            labeledFlows[(row[7],row[8])].append(row[3])     # append packet size
            if len(labeledFlows[(row[7],row[8])]) == 4 :     # indicate input length
                labeledFlows[(row[7],row[8])].append(row[9]) # append class

        line_count += 1


for key in labeledFlows :
    if len(labeledFlows[key]) == 5 :                        # set the input length + 1
        Xx.append(labeledFlows[key][:-1])
        Yy.append(labeledFlows[key][4])                      # append class which is input length + 1



# 4. save the data as CSV and import it into p4virtual machine
import pandas as pd
df = pd.DataFrame(Xx, columns = ["s1", "s2", "s3", "s4"])
Y = pd.DataFrame(Yy)
df['class'] = Y

df.to_csv("csv/sizes4classes5.csv")
