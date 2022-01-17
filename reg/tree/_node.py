import sys
from os.path import dirname, abspath
d = dirname(dirname(abspath(__file__)))
sys.path.append(d)

from utils.helper import to_row, to_column
from tree._metrics import gini_index, gini_indices, min_gini

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
            self.content, to_remove = self.take_only(content, header.index(self.field), self.fvalue, True)
            for ind in sorted(to_remove, reverse=True):
                self.target.pop(ind)
            self.left = self.getNode(self.header, self.content, self.target, fvalue, field)
            #Right Node block
            content, indeces = self.subtract(content, header.index(field), fvalue, True)
            for ind in sorted(indeces, reverse=True):
                target.pop(ind)   
            self.right = self.getNode(header, content, target, fvalue, field)
        else:
            pass
    
    def subtract(data, target, var = None, option_index = False):
        """  
        If the var parameter is set, it removes from the data all the records whose target 
        variable corresponds to var.
        Otherwise if var == None deletes from the data, the column that corresponds to the target parameter.

        """
        i = 0
        if var != None:
            to_remove = []
            for row in data:
                if row[target] == var:
                    to_remove.append(i)
                i += 1
            for index in sorted(to_remove, reverse=True):
                data.pop(index)
            if option_index is False:
                return data
            else:
                #The optionIndex allows you to return a further list containing the indexes of the items processed
                return data, to_remove
        else:
            data = to_column(data)
            data.pop(target)
            return to_row(data)

    def takeOnly(data, target, var = None, option_index = False):
        """
        Returns only the data that contains the indicated variable in the target field.

        """
        data_reduced = []
        to_remove = []
        i = 0
        for item in data:
            if item[target] == var:
                data_reduced.append(item)
            else:
                to_remove.append(i)
            i += 1
        if option_index == False:
            return data_reduced
        else:
            #The optionIndex allows you to return a further list containing the indexes of the items processed
            return data_reduced, to_remove
        
    def get_node(self, header, content, target, fvalue, field):
        if len(set(target)) == 1:
            return Node(header, content, target, fvalue, field, res = list(set(target))[0])
        elif len(set(target)) == 0:
            pass
        elif len(set(tuple(row) for row in content)) == 1:
            val = self.mostCommon(target)
            return Node(header, content, target, fvalue, field, res = val)
        else:
            next_node = next_leaf(header, content, target)
            return Node(header, content, target, next_node[1], next_node[0])

    def most_common(target):
        """
        Return the most common option in a binary collection.

        """
        both = []
        for x in sorted(set(target)):
            both.append(target.count(x))
        val = sorted(set(target))[both.index(max(both))]
        return val

def next_leaf(header, content, target):
    """
    Based on the gini index it decides how to compose the next leaf.

    """
    box = []
    i = 0
    for col in to_column(content):
        if len(set(col)) > 1:
            box.append(i)
        i += 1
    if len(box) == 1:
        subgini = gini_index(to_column(content)[box[0]], target)
        nextLeaf = [header[box[0]], sorted(list(set(to_column(content)[box[0]])))[subgini.index(min(subgini))], min(subgini)]
        return nextLeaf
    ginis = gini_indices(header, content, target)
    gini = min_gini(ginis)
    #Retrieves the gini values ​​for the subcategories of the class
    subgini = gini_index(to_column(content)[header.index(gini[0])], target)
    leaf = [gini[0], sorted(list(set(to_column(content)[header.index(gini[0])])))[subgini.index(min(subgini))], min(subgini)]
    return leaf