import sys

def load(file, has_header = True, separator = ','):
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
    is_first_loop = True
    check_format(file)

    #Open the file object
    with open(file, 'r') as f: 
        for line in f:
            row = []
            fields = line.split(separator)      
            #Checks on possible corner cases
            fields = check_quotes(fields)  
            if has_header and is_first_loop:
                for field in fields:
                    header.append(field.strip('\n'))
            else:
                for field in fields:
                    row.append(field.strip('\n'))
                content.append(row)
            is_first_loop = False

    if not has_header:
        return content
    else:
        return header, content

def check_format(filename):
    if 'csv' != filename[-3:]:
        raise Exception('The file must be .csv')

def check_quotes(fields):
    """
    Prevents a field containing a comma from being split into two fields,
    only if it is inside the quotes.

    """
    root_index = 0
    for field in fields:
        if '"' in field and field.count('"') % 2 != 0:
            suffix_index = root_index + 1
            #Once it has found the start(root) of the string it looks for where else it ends(suffix)
            for suffix_index in range(suffix_index, len(fields)):
                if '"' in fields[suffix_index]:
                    new_field = field + fields[suffix_index]
                    fields.remove(fields[suffix_index])
                    break
            fields[fields.index(field)] = new_field
        root_index += 1
    return fields

def data_types(header, content):
    """
    Returns the types associated with the classes of the first record row.

    """
    result = []
    for i in range(0, len(header)):
        try:
            check = int(content[i])
            data_type = {
                header[i] : type(check)
            }
            result.append(data_type)
        except:
            try:
                check = float(content[i])
                data_type = {
                    header[i] : type(check)
                }
                result.append(data_type)
            except:
                data_type = {
                    header[i] : type(content[i])
                }
                result.append(data_type)
    return result

def reverse(data):
    """
    Reverse the data from rows to columns / from columns to rows.

    """
    data_reverse = []
    for head_index in range (len(data[0])):
        block = []
        for item in data:
            block.append(item[head_index])
        data_reverse.append(block)
    return data_reverse


def to_column(content):
    """
    Return an object that will contain all the data present in content 
    but in the form of columns, one for each class.

    """
    data_columns = reverse(content)
    return data_columns

def to_row(content):
    """
    Return an object that will contain all the data present in content 
    but in the form of rows, one for each class

    """
    data_rows = reverse(content)
    return data_rows

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

def take_only(data, target, var = None, option_index = False):
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