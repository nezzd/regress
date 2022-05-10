from decisionkit.utils.helper import load, to_column, to_row, subtract, accuracy
from decisionkit.utils.preprocessing import pre_processing, process_cat_vars
from decisionkit.tree._tree import DecisionTree
from sklearn import tree

import sys
from os.path import dirname, abspath
d = dirname(abspath(__file__))
sys.path.append(d)

header, content = load(d + '\\train.csv')

content = subtract(content, 0) #Remove the Id Column
header.remove('PassengerId') #Remove the Head PassengerId
content = subtract(content, 2) 
header.remove('Name') 
content = subtract(content, 6) 
header.remove('Ticket') 
content = subtract(content, 6) 
header.remove('Fare') 
content = subtract(content, 6) 
header.remove('Cabin') 

contentConverted = pre_processing(content)

i = 0
for item in contentConverted:
    if item[3] == "":
        contentConverted[i][3] = 'None'
    elif item[3] > 60:
        contentConverted[i][3] = 'High'
    elif item[3] > 30:
        contentConverted[i][3] = 'Mid'
    elif item[3] > 13:
        contentConverted[i][3] = 'Low'
    else:
        contentConverted[i][3] = 'NA'
    i += 1

convertedcat = process_cat_vars(header, contentConverted)

target = to_column(convertedcat)[0]

convertedcat = to_column(convertedcat)
convertedcat.pop(0)
header.pop(0)
convertedcat = to_row(convertedcat)

xtrain = convertedcat[slice(0, 700)].copy()
ytrain = target[slice(0, 700)].copy()

xtest = convertedcat[slice(700, 893)].copy()
ytest = target[slice(700, 893)].copy()

scikit_learn_tree = tree.DecisionTreeClassifier()
my_decision_tree = DecisionTree()

scikit_learn_tree.fit(xtrain, ytrain)
my_decision_tree.build(header, xtrain, ytrain)

scikit_learn_accuracy = accuracy(scikit_learn_tree.predict(xtest), ytest)
my_prediction_accuracy = accuracy(my_decision_tree.predict(header, xtest), ytest)

print(f'Scikit-learn accuracy: {scikit_learn_accuracy}')
print(f'My prection accuracy: {my_prediction_accuracy}')