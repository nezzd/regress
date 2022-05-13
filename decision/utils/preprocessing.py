from decision.utils.helper import to_column, to_row

def pre_processing(content):
    """
    If possible convert each value to the most suitable type.

    """
    row_counter = 0
    for row in content:
        item_counter = 0
        for item in row:
            try:
                item_converted = int(item)
                row[item_counter] = item_converted
            except:
                try:
                    item_converted = float(item)
                    row[item_counter] = item_converted
                except:
                    pass
            item_counter += 1
        row_counter += 1
    return content

def is_cat_var(var):
        """
        Check if all elements in the list are of the same type.

        """
        if all(isinstance(n, int) for n in var):
            return False
        elif all(isinstance(n, float) for n in var):
            return False
        else:
            return True

def process_cat_vars(header, content):
    """
    Processes categorical variables, the goal is to reproduce the content entirely
    in numerical form.

    """
    data_columns = to_column(content)
    box_converted = []
    for column in data_columns:
        if is_cat_var(column) is not True:
            box_converted.append(column)
            continue
        column_converted = []
        for item in column:
            try:
                item_converted = int(item)
                column_converted.append(item_converted)
            except:
                try:
                    item_converted = float(item)
                    column_converted.append(item_converted)
                except:
                    column_converted = []
                    columnSet = set(column)

                    #Sort the list of variables for being consistent
                    columns_set_ord = sorted(list(columnSet))
                    for item in column:
                        column_converted.append(columns_set_ord.index(item))
                    break
        if len(column_converted) == len(column):
            box_converted.append(column_converted)
    return to_row(box_converted)