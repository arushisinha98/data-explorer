import pandas as pd
from datetime import datetime

from constants import main_path, minimum_spend, continuous_variables
        
    
def minimum_spend_imputation(input_df):
    '''
    FUNCTION to implement minimum spend logic on dataframe.
    input: input_df
    output: output_df
    '''
    try:
        # if any spend category columns exist in dataframe, implement minimum spend
        if any(col in list(input_df.columns) for col in list(minimum_spend.keys())):
            output_df = input_df.copy()
            for col, val in minimum_spend.items():
                output_df[col].fillna(val, inplace = True)
                output_df.loc[lambda df: df[col] < val, col] = val
            return output_df
        else:
            return input_df
    
    except Exception as e:
        print(f"Failed to perform minimum spend imputation on data.")
        current_dateTime = str(datetime.now())[0:19]
        print(current_dateTime + ': ' + str(e))
        
        
def regression_imputation(input_df, X, Y, coefficients):
    '''
    FUNCTION to implement regression-based imputation on missing or infeasible values of column X using columns Y and the corresponding coefficients.
    input: input_df, X (name of column), Y (tuple with names of columns), coefficients (tuple with coefficients)
    '''
    assert X in input_df.columns, f"The column to be imputed, {X}, does not exist in the input dataframe."
    assert all([y in input_df.columns for y in Y]), f"The dependent columns, {Y}, do not exist in the input dataframe."
    assert len(coefficients) == len(Y), "Require one coefficient to be associated with each dependent column."
    
    try:
        output_df = input_df.copy()
        output_df[X].fillna(-1, inplace = True)
        output_df.loc[lambda df: df[X] < 0, X] = sum([coefficients[ii]*output_df[Y[ii]] for ii in range(len(Y))])
        return output_df
    
    except Exception as e:
        print(f"Failed to perform regression-based imputation on data.")
        current_dateTime = str(datetime.now())[0:19]
        print(current_dateTime + ': ' + str(e))