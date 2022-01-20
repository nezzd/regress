import random
import sys
from os.path import dirname, abspath
d = dirname(dirname(abspath(__file__)))
sys.path.append(d)

from tree._tree import DecisionTree

class RandomForest():
    def __init__(self, ntrees = 10):
        self.forest = []
        self.ntrees = ntrees
    
    def grow(self, header, data, target):
        for i in range(0, self.ntrees):
            self.forest.append(getTree(header, data, target))

    def predict(self, header, content):
        res = []
        for item in self.forest:
            data = []
            for obj in content:
                temp = []
                for i in item[2]:
                    temp.append(obj[i])
                data.append(temp)
            res.append(item[0].predict(item[1], data))
        final = []
        for i in range(0, len(content)):
            box = []
            for r in res:
                box.append(r[i])
            final.append(most_frequent(box))
        return final

def most_frequent(data):
    return max(set(data), key = data.count)


def getTree(header, data, target):
        res = DecisionTree()
        altData = []
        altTarget = []
        altHeader = []
        hxs = random.randrange(2, len(header))
        hid = []
        for i in range(0, len(data)):
            rnd = random.randrange(0, len(data))
            altData.append(list(data[rnd]))
            altTarget.append(int(target[rnd]))
        while len(hid) != hxs:
            rnd = random.randrange(0, len(header))
            if rnd not in hid:
                hid.append(rnd)
        for i in sorted(hid):
            altHeader.append(str(header[i]))
        for i in range(0, len(header)):
            if i not in sorted(hid):
                w = i + (len(altData[0]) - len(data[0]))
                check = len(altData[0])
                for r in altData: 
                    if len(r) == check:                 
                        del r[w]
        res.grow(altHeader, altData, altTarget) 
        return res, altHeader, sorted(hid)