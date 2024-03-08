from datetime import datetime
import pandas as pd
import numpy as np


def RecodeColumns(input_df, recode_dict):
    '''
    FUNCTION to recode the columns of a pandas dataframe
    inputs:
    - input_df, the input dataframe
    - recode_dict, a dictionary with original column names as keys and the recode names as values
    outputs:
    - output_df, the output dataframe
    '''
    assert isinstance(input_df, pd.DataFrame)
    assert isinstance(recode_dict, dict)
    assert set(recode_dict.keys()) <= set(input_df.columns), "The recode dictionary contains columns that are not present in the original dataframe."
    
    try:
        output_df = df.rename(columns = recode_dict)
        return output_df
        
    except Exception as e:
        print(e)