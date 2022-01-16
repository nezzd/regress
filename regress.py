"""
This module gathers tree-based methods, including decision, regression and
randomized trees.

"""

# Authors: Nicolo' Giannini

# =============================================================================
# Types and constants
# =============================================================================

def load(filename, hasHeader = True, separator = ','):
    """
    Starting from the file name as a parameter, it returns header 
    and content in the form of lists.

    The header output is optional, it is determined by a parameter 
    that is set True by default.

    Since the processed file must be a .csv the separator is the comma
    but it can be changed by parameter.

    """
    content = []
    header = []
    isFirstLoop = True
    checkFormat(filename)
    #Open the file object
    with open(filename, 'r') as f: 
        for line in f:
            row = []
            fields = line.split(separator)      
            #Checks on possible corner cases
            fields = checkQuotes(fields)  
            if hasHeader and isFirstLoop:
                for field in fields:
                    header.append(field.strip('\n'))
            else:
                for field in fields:
                    row.append(field.strip('\n'))
                content.append(row)
            isFirstLoop = False

    if not hasHeader:
        return content
    else:
        return header, content

def checkFormat(filename):
    if 'csv' != filename[-3:]:
        raise Exception('The file must be .csv')

def checkQuotes(fields):
    """
    Prevents a field containing a comma from being split into two fields,
    only if it is inside the quotes.

    """
    rootIndex = 0
    for field in fields:
        if '"' in field and field.count('"') % 2 != 0:
            suffixIndex = rootIndex + 1
            #Once it has found the start(root) of the string it looks for where else it ends(suffix)
            for suffixIndex in range(suffixIndex, len(fields)):
                if '"' in fields[suffixIndex]:
                    newfield = field + fields[suffixIndex]
                    fields.remove(fields[suffixIndex])
                    break
            fields[fields.index(field)] = newfield
        rootIndex += 1
    return fields

def dataTypes(header, content):
    """
    Returns the types associated with the classes of the first record row.

    """
    result = []
    for i in range(0, len(header)):
        try:
            check = int(content[i])
            dataType = {
                header[i] : type(check)
            }
            result.append(dataType)
        except:
            try:
                check = float(content[i])
                dataType = {
                    header[i] : type(check)
                }
                result.append(dataType)
            except:
                dataType = {
                    header[i] : type(content[i])
                }
                result.append(dataType)
    return result

#Modifier methods

def reverse(data):
    """
    Reverse the data from rows to columns / from columns to rows.

    """
    dataReverse = []
    for headIndex in range (len(data[0])):  
        block = [] 
        for item in data:
            block.append(item[headIndex])
        dataReverse.append(block)
    return dataReverse


def toColumn(content):
    """
    Return an object that will contain all the data present in content 
    but in the form of columns, one for each class.

    """
    dataColumns = reverse(content)
    return dataColumns

def toRow(content):
    """
    Return an object that will contain all the data present in content 
    but in the form of rows, one for each class

    """
    dataRows = reverse(content)
    return dataRows

#Preprocess methods

def preProcessing(content):
    """
    If possible convert each value to the most suitable type.

    """
    rowCounter = 0
    for row in content:
        itemCounter = 0
        for item in row:
            try:
                itemConverted = int(item)
                row[itemCounter] = itemConverted
            except:
                try:
                    itemConverted = float(item)
                    row[itemCounter] = itemConverted
                except:
                    pass
            itemCounter += 1
        rowCounter += 1
    return content

def isCatVar(var):
        """
        Check if all elements in the list are of the same type.

        """
        if all(isinstance(n, int) for n in var):
            return False
        elif all(isinstance(n, float) for n in var):
            return False
        else:
            return True

def processCatVars(header, content):
    """
    Processes categorical variables, the goal is to reproduce the content entirely
    in numerical form.

    """
    dataColumns = toColumn(content)
    boxConverted = []
    for column in dataColumns:
        if isCatVar(column) is not True:
            boxConverted.append(column)
            continue
        columnConverted = []
        for item in column:
            try:
                itemConverted = int(item)
                columnConverted.append(itemConverted)
            except:
                try:
                    itemConverted = float(item)
                    columnConverted.append(itemConverted)
                except:
                    columnConverted = []
                    columnSet = set(column)

                    #Sort the list of variables for being consistent
                    columnsSetOrd = sorted(list(columnSet))
                    for item in column:
                        columnConverted.append(columnsSetOrd.index(item))
                    break
        if len(columnConverted) == len(column):
            boxConverted.append(columnConverted)
    return toRow(boxConverted)

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
        
def giniIndeces(header, content, target):
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

def subtract(data, target, var = None, optionIndex = False):
    """  
    If the var parameter is set, it removes from the data all the records whose target 
    variable corresponds to var.
    Otherwise if var == None deletes from the data, the column that corresponds to the target parameter.

    """
    i = 0
    if var != None:
        toRemove = []
        for row in data:
            if row[target] == var:
                toRemove.append(i)
            i += 1
        for index in sorted(toRemove, reverse=True):
            data.pop(index)
        if optionIndex is False:
            return data
        else:
            #The optionIndex allows you to return a further list containing the indexes of the items processed
            return data, toRemove
    else:
        data = toColumn(data)
        data.pop(target)
        return toRow(data)

def takeOnly(data, target, var = None, optionIndex = False):
    """
    Returns only the data that contains the indicated variable in the target field.

    """
    dataReduced = []
    toRemove = []
    i = 0
    for item in data:
        if item[target] == var:
            dataReduced.append(item)
        else:
            toRemove.append(i)
        i += 1
    if optionIndex == False:
        return dataReduced
    else:
        #The optionIndex allows you to return a further list containing the indexes of the items processed
        return dataReduced, toRemove

def nextLeaf(header, content, target):
    """
    Based on the gini index it decides how to compose the next leaf.

    """
    box = []
    i = 0
    for col in toColumn(content):
        if len(set(col)) > 1:
            box.append(i)
        i += 1
    if len(box) == 1:
        subgini = giniIndex(toColumn(content)[box[0]], target)
        nextLeaf = [ header[box[0]], sorted(list(set(toColumn(content)[box[0]])))[subgini.index(min(subgini))], min(subgini) ]
        return nextLeaf
    ginis = giniIndeces(header, content, target)
    gini = minGini(ginis)
    #Retrieves the gini values ​​for the subcategories of the class
    subgini = giniIndex(toColumn(content)[header.index(gini[0])], target)
    nextLeaf = [ gini[0], sorted(list(set(toColumn(content)[header.index(gini[0])])))[subgini.index(min(subgini))], min(subgini) ]
    return nextLeaf

def getNode(header, content, target, fvalue, field):
    if len(set(target)) == 1:
        return Node(header, content, target, fvalue, field, res = list(set(target))[0])
    elif len(set(target)) == 0:
        pass
    elif len(set(tuple(row) for row in content)) == 1:
        val = mostCommon(target)
        return Node(header, content, target, fvalue, field, res = val)
    else:
        nextNode = nextLeaf(header, content, target)
        return Node(header, content, target, nextNode[1], nextNode[0])

def mostCommon(target):
    """
    Return the most common option in a binary collection.

    """
    both = []
    for x in sorted(set(target)):
        both.append(target.count(x))
    val = sorted(set(target))[both.index(max(both))]
    return val

def accuracy(predicted, target):
    """
    Accuracy is the ratio of correct predictions to total predictions.

    """
    i = 0
    tot = []
    for predict in predicted:
        if predict == target[i]:
            tot.append(predict)
        i += 1
    acc = len(tot) / len(target)
    return round(acc, 3)

class DecisionTree:
    """
    DecisionTree uses the gini index to create decision points for classification tasks.
    The goal is to create a model capable of predicting a target variable, building the decision
    rules by learning from the data.

    """
    def __init__(self):
        #Indicates whether the tree is fully built or not
        self.finished = False
        #The root is the node from which the branches will start
        self.root = None
    def grow(self, header, content, target):
        """
        Develops the decision tree based on the data.

        """
        #For now it branches out as much as possible
        #TODO add a parameter that allows you to specify the maximum depth of the tree
        while self.finished == False:
            if self.root:
                self.finished = True
            else:
                nextNode = nextLeaf(header, content, target)
                self.root = Node(header, content, target, nextNode[1], nextNode[0])
    
    def predict(self, header, content):
        """
        Processes the predicted target variable based on the tree

        """
        prediction = []
        for item in content:
            predict = self.checkNode(header, self.root, item)
            prediction.append(predict)
        return prediction
    
    def checkNode(self, header, node, item):
        """
        Iterative logic to check the condition of each node, until the path is exhausted
        and the variable is predicted

        """
        if node.res == None:
            if node.fvalue == item[header.index(node.field)]:
                res = self.checkNode(header, node.left, item)
                return res
            else:
                res = self.checkNode(header, node.right, item)
                return res
        else:
            return node.res

class Node:
    """
    Core element in the composition of the tree, each node will contain the 
    information to proceed to the next ones.
    Each node on the left will be the path if the condition of the parent node
    is respected, the nodes on the right are instead the negation of the parent condition.

    """
    def __init__(self, header, content, target, fvalue = None, field = None, res = None):
        """
        Each node, once initialized, will continue to branch until its own branch is exhausted.

        """
        #print(sys.getrecursionlimit())
        self.left = None
        self.right = None
        #At the moment I make a copy of the data for each node, it is not optimal and to be replaced with another logic
        self.header = header.copy()
        self.content = content.copy()
        self.target = target.copy()
        self.field = field   
        self.fvalue = fvalue
        self.res = res
        if res is None:
            #Left Node block
            self.content, toRemove = takeOnly(content, header.index(self.field), self.fvalue, True)
            for ind in sorted(toRemove, reverse=True):
                self.target.pop(ind)
            self.left = getNode(self.header, self.content, self.target, fvalue, field)
            #Right Node block
            content, indeces = subtract(content, header.index(field), fvalue, True)
            for ind in sorted(indeces, reverse=True):
                target.pop(ind)   
            self.right = getNode(header, content, target, fvalue, field)
        else:
            pass