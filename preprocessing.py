from utils import toColumn, toRow

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