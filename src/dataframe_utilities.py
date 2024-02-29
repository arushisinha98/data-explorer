import pandas as pd
from datetime import datetime
        
        
def column_sum(input_df, colname, index = None):
    '''
    FUNCTION to compute the global column-wise sum of an input dataframe.
    
    input_df: the input pandas dataframe
    colname: the name of the column of interest in the dataframe
    (optional) index: a list of rows that will be *included* to compute the column sum; by default, all rows will be included
    
    current_sum: the sum of values in the specified column and within the specified list of rows
    '''
    assert isinstance(input_df, pd.DataFrame), "Require input_df to be a pandas dataframe."
    assert colname in list(input_df.columns), f"The column '{colname}' was not found in the input dataframe."
    assert pd.api.types.is_numeric_dtype(input_df[colname]), f"The column '{colname}' is not numeric."
    if index:
        assert isinstance(index, list), "Require the index to be a list."
        assert all([x in list(input_df.index) for x in index]), f"The index includes rows that are not found in the input dataframe."
    else:
        nanvals = np.isnan(input_df[colname]) 
        index = [ix for ii, ix in enumerate(list(input_df.index)) if not nanvals[ii]]
    
    try:
        filter_df = input_df.iloc[index]
        current_sum = sum(filter_df[colname])
        return current_sum

    except Exception as e:
        print(f"Failed to compute column-wise sum. Terminate")
        current_dateTime = str(datetime.now())[0:19]
        print(current_dateTime + ': ' + str(e))


def get_filter_index(input_df, value_filters):
    '''
    FUNCTION to get the index associated with a value filter applied to the columns of the input dataframe.
    
    input_df: the input pandas dataframe
    value_filters: a dictionary containing column names as keys and the value to filter by as values
    
    index: a list of rows that satisfy the value_filters criteria
    '''
    assert isinstance(input_df, pd.DataFrame), "Require input_df to be a pandas dataframe."
    assert isinstance(value_filters,
                      dict), "Require value_filters to be a dictionary with column names as keys and the value to filter by as values."
    assert all(col in list(input_df.columns) for col in list(
        value_filters.keys())), f"The columns {list(value_filters.keys())} do not exist in the input dataframe."

    try:
        output_df = input_df.copy()
        for ix, (key, value) in enumerate(value_filters.items()):
            if isinstance(value, list): # if in list ("OR")
                output_df = output_df.loc[output_df[key].isin(value)]
            else:
                output_df = output_df[output_df[key] == value]
        return list(output_df.index)

    except Exception as e:
        print(f"Failed to filter input data. Terminate")
        current_dateTime = str(datetime.now())[0:19]
        print(current_dateTime + ': ' + str(e))


def subgroup_sum(input_df, colname, value_filters = None):
    '''
    FUNCTION to compute the column-wise sum of a subgroup within the input dataframe, given its definition.
    
    input_df: the input pandas dataframe
    colname: the name of the column of interest in the input dataframe
    value_filters: a dictionary containing the definition of the subgroup (i.e. with column names as keys and value to filter by as values)
    
    sub_sum: the sum of values in the specified column that are within the specified subgroup
    '''
    try:
        if value_filters:
            index = get_filter_index(input_df, value_filters)
        else:
            index = list(input_df.index)
        sub_sum = column_sum(input_df, colname, index)
        return sub_sum
    
    except Exception as e:
        print(f"Failed to compute column-wise sum of subgroup. Terminate")
        current_dateTime = str(datetime.now())[0:19]
        print(current_dateTime + ': ' + str(e))
        
        
def upsample(input_df, nrows, value_filters = None):
    '''
    FUNCTION to randomly sample rows with replacement from an input dataframe. Optionally, takes in value_filters argument to randomly sample a subset of the input dataframe.
    '''
    try:
        if value_filters:
            index = get_filter_index(input_df, value_filters)
        else:
            index = list(input_df.index)
        sample_df = input_df[input_df.index.isin(index)]
        return sample_df.sample(n = nrows, replace = True)
    
    except Exception as e:
        print(f"Failed to upsample dataframe. Terminate")
        current_dateTime = str(datetime.now())[0:19]
        print(current_dateTime + ': ' + str(e))
        