import sys
sys.path.append("..")

from utils.helper import toColumn, toRow

def giniIndex(data, target):
    """
    Gini impurity is a metric for classification tasks, is a measure of the 
    inequality of a distribution. It stores sum of squared probabilities 
    of each class.

        Gini = 1 - Σ (Pi)² for i=1 to number of classes

    NOTE: The target must be a binary variable.

    """
    if len(set(target)) != 2:
        raise Exception("The target must be a binary variable.")
    subsGini = []
    #Distinct variables from data
    varSet = set(data)
    #In this loop the corresponding indices are saved for each variable into dataIndeces
    dataIndeces = []
    for var in varSet:
        varIndeces = []
        index = 0
        for item in data:
            if var == item:
                varIndeces.append(index)
            index += 1
        dataIndeces.append(varIndeces)

    #For each index block(indcs), the respective values ​​from the target field are saved into targetValues
    for indcs in dataIndeces:
        targetValues = []
        varGini = []
        for ind in indcs:
            targetValues.append(target[ind])
        for x in set(targetValues):
            c = targetValues.count(x)
            varGini.append(c)
        #If there is only one variable, it means that the gini impurity will be zero, for reasons of calculations I add a 0
        if len(varGini) < 2:
            varGini.append(0)
        #Formula for the gini index
        subsGini.append((len(indcs) / len(data)) * (1 - ((varGini[0] / len(indcs)) ** 2) - ((varGini[1] / len(indcs)) ** 2)))
    return subsGini
        
def giniIndices(header, content, target):
    """
    Given n variables it calculates the gini index for each of them.
    The object that the method returns is a dictionary where the key corresponds
    to the analyzed class and the associated value is the gini impurity.

    """
    #ginis stores all the gini impurity for each class
    ginis = {} 
    #Prepares the data for the calculation
    content = toColumn(content)
    c = 0
    for column in content:
        gini = 0
        subsgini = giniIndex(column, target)
        for sub in subsgini:
            gini += sub
        ginis[header[c]] = gini
        c += 1
    return ginis

def minGini(ginis):
    """
    Given a dictionary, it returns a list containing key and value in reference
    to the element with the smallest value.

    """
    listGinis = []
    listKeys = []
    res = []
    for gini in ginis:
        listGinis.append(ginis[gini])
        listKeys.append(gini)
    res.append(listKeys[listGinis.index(min(listGinis))])
    res.append(min(listGinis))
    return res