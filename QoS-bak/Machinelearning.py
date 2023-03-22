
import numpy as np
import pandas as pd
import argparse
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import export_graphviz
import pydotplus



parser = argparse.ArgumentParser()

# Add argument
parser.add_argument('-i', required=True, help='path to dataset')
parser.add_argument('-o', required=True, help='path to outputfile')

args = parser.parse_args()

# extract argument
input = args.i
outputfile = args.o


# output the tree
def get_lineage(tree, feature_names, file):
    sa = []
    sb = []
    sc = []
    sd = []
    left = tree.tree_.children_left
    right = tree.tree_.children_right
    threshold = tree.tree_.threshold
    features = [feature_names[i] for i in tree.tree_.feature]
    value = tree.tree_.value
    le = '<='
    g = '>'
    # get ids of child nodes
    idx = np.argwhere(left == -1)[:, 0]

    # traverse the tree and get the node information
    def recurse(left, right, child, lineage=None):
        if lineage is None:
            lineage = [child]
        if child in left:
            parent = np.where(left == child)[0].item()
            split = 'l'
        else:
            parent = np.where(right == child)[0].item()
            split = 'r'

        lineage.append((parent, split, threshold[parent], features[parent]))
        if parent == 0:
            lineage.reverse()
            return lineage
        else:
            return recurse(left, right, parent, lineage)

    for j, child in enumerate(idx):
        clause = ' when '
        for node in recurse(left, right, child):
                if len(str(node)) < 3:
                    continue
                i = node

                if i[1] == 'l':
                    sign = le
                else:
                    sign = g
                clause = clause + i[3] + sign + str(i[2]) + ' and '

    # wirte the node information into text file
        a = list(value[node][0])
        ind = a.index(max(a))
        clause = clause[:-4] + ' then ' + str(ind)
        file.write(clause)
        file.write(";\n")


# Training set X and Y
Set1 = pd.read_csv(input)
Set = Set1.values.tolist()
X = [i[0:4] for i in Set]
Y =[i[4] for i in Set]

# Test set Xt and Yt
Set2 = pd.read_csv(input)
Sett = Set2.values.tolist()
Xt = [i[0:4] for i in Set]
Yt =[i[4] for i in Set]

class_names=['Streaming','Controllers','Appliances','Sensors','Home Automation']
feature_names=['sa','sb','sc', 'sd']


# prepare training and testing set
X = np.array(X)
Y = np.array(Y)
Xt = np.array(Xt)
Yt = np.array(Yt)

# decision tree fit
dt = DecisionTreeClassifier(max_depth = 12)
dt.fit(X, Y)
Predict_Y = dt.predict(X)
print(accuracy_score(Y, Predict_Y))

Predict_Yt = dt.predict(Xt)
print(accuracy_score(Yt, Predict_Yt))

# output the tree in a text file, write it
threshold = dt.tree_.threshold
features  = [feature_names[i] for i in dt.tree_.feature]
sa = []
sb = []
sc = []
sd = []
for i, fe in enumerate(features):

    if fe == 'sa':
        sa.append(threshold[i])
    elif fe == 'sb':
        if threshold[i] != -2.0:
            sb.append(threshold[i])
    elif fe == 'sc':
        if threshold[i] != -2.0:
            sc.append(threshold[i])
    else:
        sd.append(threshold[i])

sa = [int(i) for i in sa]
sb = [int(i) for i in sb]
sc = [int(i) for i in sc]
sd = [int(i) for i in sd]
sa.sort()
sb.sort()
sc.sort()
sd.sort()
tree = open(outputfile,"w+")
tree.write("sa = ")
tree.write(str(sa))
tree.write(";\n")
tree.write("sb = ")
tree.write(str(sb))
tree.write(";\n")
tree.write("sc = ")
tree.write(str(sc))
tree.write(";\n")
tree.write("sd = ")
tree.write(str(sd))
tree.write(";\n")
get_lineage(dt,feature_names,tree)
tree.close()
