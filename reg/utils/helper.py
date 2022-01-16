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