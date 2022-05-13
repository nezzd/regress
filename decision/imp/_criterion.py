from decision.utils.helper import to_column

def gini_index(data, target):
    """
    Gini impurity is a metric for classification tasks, is a measure of the 
    inequality of a distribution. It stores sum of squared probabilities 
    of each class.

        Gini = 1 - Σ (Pi)² for i=1 to number of classes

    NOTE: The target must be a binary variable.

    """
    if len(set(target)) != 2:
        raise Exception("The target must be a binary variable.")
    subs_gini = []
    #distinct variables from data
    s_data = set(data)
    #in this loop the corresponding indices are saved for each variable into dataIndeces
    data_indices = []
    for var in s_data:
        var_indices = []
        index = 0
        for item in data:
            if var == item:
                var_indices.append(index)
            index += 1
        data_indices.append(var_indices)

    #for each index block(indcs), the respective values ​​from the target field are saved into targetValues
    for indcs in data_indices:
        target_values = []
        var_gini = []
        for ind in indcs:
            target_values.append(target[ind])
        for x in set(target_values):
            c = target_values.count(x)
            var_gini.append(c)
        #if there is only one variable, it means that the gini impurity will be zero, for reasons of calculations I add a 0
        if len(var_gini) < 2:
            var_gini.append(0)
        #formula for the gini index
        subs_gini.append((len(indcs) / len(data)) * (1 - ((var_gini[0] / len(indcs)) ** 2) - ((var_gini[1] / len(indcs)) ** 2)))
    return subs_gini
        
def gini_indices(header, content, target):
    """
    Given n variables it calculates the gini index for each of them.
    The object that the method returns is a dictionary where the key corresponds
    to the analyzed class and the associated value is the gini impurity.

    """
    #ginis stores all the gini impurity for each class
    ginis = {} 
    #prepares the data for the calculation
    content = to_column(content)
    c = 0
    for column in content:
        gini = 0
        subs_gini = gini_index(column, target)
        for sub in subs_gini:
            gini += sub
        ginis[header[c]] = gini
        c += 1
    return ginis

def min_gini(ginis):
    """
    Given a dictionary, it returns a list containing key and value in reference
    to the element with the smallest value.

    """
    list_ginis = []
    list_keys = []
    res = []
    for gini in ginis:
        list_ginis.append(ginis[gini])
        list_keys.append(gini)
    res.append(list_keys[list_ginis.index(min(list_ginis))])
    res.append(min(list_ginis))
    return res
