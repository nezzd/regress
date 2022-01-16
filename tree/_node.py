from utils import toColumn, toRow
from tree.metrics import giniIndex, giniIndices, minGini

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
            self.content, toRemove = self.takeOnly(content, header.index(self.field), self.fvalue, True)
            for ind in sorted(toRemove, reverse=True):
                self.target.pop(ind)
            self.left = self.getNode(self.header, self.content, self.target, fvalue, field)
            #Right Node block
            content, indeces = self.subtract(content, header.index(field), fvalue, True)
            for ind in sorted(indeces, reverse=True):
                target.pop(ind)   
            self.right = self.getNode(header, content, target, fvalue, field)
        else:
            pass
    
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
        
    def getNode(self, header, content, target, fvalue, field):
        if len(set(target)) == 1:
            return Node(header, content, target, fvalue, field, res = list(set(target))[0])
        elif len(set(target)) == 0:
            pass
        elif len(set(tuple(row) for row in content)) == 1:
            val = self.mostCommon(target)
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
        nextLeaf = [header[box[0]], sorted(list(set(toColumn(content)[box[0]])))[subgini.index(min(subgini))], min(subgini)]
        return nextLeaf
    ginis = giniIndices(header, content, target)
    gini = minGini(ginis)
    #Retrieves the gini values ​​for the subcategories of the class
    subgini = giniIndex(toColumn(content)[header.index(gini[0])], target)
    nextLeaf = [gini[0], sorted(list(set(toColumn(content)[header.index(gini[0])])))[subgini.index(min(subgini))], min(subgini)]
    return nextLeaf