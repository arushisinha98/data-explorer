from datetime import datetime
import pandas as pd
import numpy as np
from pandas.api.types import CategoricalDtype
from sklearn.impute import KNNImputer


valid_dtypes = ['char','string','int','float','bool','categorical','datetime']


class Pipeline():
    '''
    The Pipeline object contains member functions that perform transformations on a data set. These functions can be sequentially called to create a pre-processing pipeline. The relevant metadata and artifacts required to reproduce the pipeline are also stored within the Pipeline object.
    '''
    def __init__(self, input_df, description = ""):
        assert isinstance(input_df, pd.DataFrame)
        
        try:
            input_df = input_df.convert_dtypes() # set best dtype for columns
            input_df = input_df.reset_index(drop = True) # set one index = one row
            
            self.data = input_df
            self.metadata = description + "\n"
            self.n_steps = 0
            self.artifacts = dict()
            self.functions = listFunctions(print = False)
            
        except Exception as e:
            print("Failed to create Pipeline object.")
            current_dateTime = str(datetime.now())[0:19]
            print(current_dateTime + ': ' + str(e))
            
            
    def __str__(self):
        return self.metadata
    
    
    def getData(self):
        '''
        Returns data as at latest state in transformation pipeline.
        '''
        return self.data
    
    
    def listFunctions(self, print = False):
        '''
        Lists all the transformation functions available in the class object.
        NOTE: all transformation functions are in PascalCase
        '''
        class_members = dir(self) # list all attributes and methods
        functions = [member for member in class_members if callable(getattr(self, member)) and member[0].isupper()]
        
        if print:
            # print the list of functions
            print("Functions available in the class object:")
            for function in functions:
                print("-", function)
        return functions
            
    
    def DropColumns(self, column_list):
        '''
        FUNCTION to drop columns of a pandas dataframe
        Parameters:
        - column_list: List of column names to be dropped.
        '''
        assert isinstance(column_list, list)
        assert set(column_list) <= set(self.data.columns), "The list of columns to be dropped contains columns that are not present in the original dataframe."

        try:
            self.data = self.data.drop(column_list, axis = 1)
            self.n_steps += 1
            self.metadata += f"{self.n_steps}. The following columns were dropped:\
            {column_list}\n"
            self.artifacts[self.n_steps] = {'DropColumns': column_list}

        except Exception as e:
            print("Failed to drop specified columns.")
            current_dateTime = str(datetime.now())[0:19]
            print(current_dateTime + ': ' + str(e))
    
    
    def DropRows(self, column_list):
        '''
        FUNCTION to drop the rows of a pandas dataframe based on presence of missing values in the specified columns.
        Parameters:
        - column_list: List of columns that must be filled and valid for a row to be retained.
        '''
        assert isinstance(column_list, list)
        assert set(column_list) <= set(self.data.columns), "The list of columns contains columns that are not present in the original dataframe."
        
        try:
            self.data = self.data.dropna(subset = column_list)
            self.n_steps += 1
            self.metadata += f"{self.n_steps}. Rows were dropped based on the presence of missing values in the following columns:\
            {column_list}\n"
            self.artifacts[self.n_steps] = {'DropRows': column_list}
        
        except Exception as e:
            print("Failed to drop rows based on mandatory columns.")
            current_dateTime = str(datetime.now())[0:19]
            print(current_dateTime + ': ' + str(e))


    def RenameColumns(self, recode_dict):
        '''
        FUNCTION to recode the names of columns of a pandas dataframe
        Parameters:
        - recode_dict: Dictionary specifying the columns and their target names.
        '''
        assert isinstance(recode_dict, dict)
        assert set(recode_dict.keys()) <= set(self.data.columns), "The recode dictionary contains columns that are not present in the original dataframe."

        try:
            self.data = self.data.rename(columns = recode_dict)
            self.n_steps += 1
            self.metadata += f"{self.n_steps}. The following dictionary was used to rename the columns:\
            {recode_dict}\n"
            self.artifacts[self.n_steps] = {'RecodeColumnNames': recode_dict}

        except Exception as e:
            print("Failed to recode column names.")
            current_dateTime = str(datetime.now())[0:19]
            print(current_dateTime + ': ' + str(e))
            
            
    def getColumnTypes(self):
        '''
        Outputs a dictionary specifying the data type of each column
        Returns:
        - type_dict: Dictionary specifying columns and their dtypes.
        '''
        return dict(self.data.dtypes)
    
    
    def RecodeColumnTypes(self, recode_dict):
        '''
        FUNCTION to recode the data type of columns of a pandas dataframe
        Parameters:
        - recode_dict: Dictionary specifying the columns and their target dtypes. 
                       The dtypes can be 'char', 'string', 'int', 'float', 'bool',
                       'categorical', 'date', or 'datetime'.
        '''
        assert isinstance(recode_dict, dict)
        assert set(recode_dict.keys()) <= set(self.data.columns), "The recode dictionary contains columns that are not present in the original dataframe."
        assert set(recode_dict.values()) <= set(valid_dtypes),\
        f"You may only recode column into the following types: {valid_dtypes}"
        
        try:
            df = self.data
            for column, dtype in recode_dict.items():
                # keeps NaN intact except in conversion to bool, which replaces missing cells with False if there is no natural distinction between True and False that can be found in original values
                if dtype == 'char':
                    df[column] = np.where(pd.isna(df[column]),
                                          df[column],
                                          df[column].astype(str).str.slice(0, 1))
                elif dtype == 'string':
                    df[column] = np.where(pd.isna(df[column]),
                                          df[column],
                                          df[column].astype('string'))
                elif dtype == 'int':
                    df[column] = np.where(pd.isna(df[column]),
                                          df[column],
                                          pd.to_numeric(df[column], downcast = 'integer', errors = 'coerce'))
                elif dtype == 'float':
                    df[column] = np.where(pd.isna(df[column]),
                                          df[column],
                                          df[column].astype(float))
                elif dtype == 'bool':
                    try:
                        df[column] = df[column].astype('boolean')
                    finally:
                        continue
                elif dtype == 'categorical':
                    df[column] = np.where(pd.isna(df[column]),
                                          df[column],
                                          df[column].astype('category'))
                elif dtype == 'datetime':
                    df[column] = np.where(pd.isna(df[column]),
                                          df[column],
                                          pd.to_datetime(df[column], errors = 'coerce'))
            self.data = df
            self.n_steps += 1
            self.metadata += f"{self.n_steps}. The following dictionary was used to recode the dtypes of the columns:\
            {recode_dict}\n"
            self.artifacts[self.n_steps] = {'RecodeColumnTypes': recode_dict}

        except Exception as e:
            print("Failed to recode column dtypes.")
            current_dateTime = str(datetime.now())[0:19]
            print(current_dateTime + ': ' + str(e))
    
    
    def ReplaceByValue(self, column, bound, direction, group_by = None, fill = 'NA'):
        '''
        FUNCTION to replace cells in a column based on their original value.
        Parameters:
        - column: Name of column to be affected by replacement
        - bound: Values to replace
        - direction: The direction where replacement is to be applied (> bound, < bound, >= bound, <= bound, == bound, != bound)
        - group_by: List of column(s) to group by before applying replacement
        - fill: Value or type of value to fill by
        '''
        if isinstance(fill, str):
            assert fill in ['mean','median','NA'], "For numeric columns, require fill value to be numeric (int or float) or 'mean', 'median', or 'NA'"
        else:
            assert isinstance(fill, int | float), "For numeric columns, require fill value to be numeric (int or float) or 'mean', 'median', or 'NA'"
        if group_by:
            assert isinstance(group_by, list) and all(col in list(self.data.columns) for col in group_by), "Require all column(s) to group by to exist in the dataframe and to be specified in a list."
        assert direction in ['>', '<', '>=', '<=', '==', '!='], "Direction should be one of '>', '<', '>=', '<=', '==', '!='"
        
        try:
            self.RecodeColumnTypes({column: 'float'})
            # group by columns (if any)
            if isinstance(group_by, str):
                group_by = [group_by]
            if group_by:
                grouped = self.data.groupby(group_by)
            else:
                grouped = [(None, self.data)]

            # iterate over groups and determine fill value
            for group_name, group_df in grouped:
                if fill == 'mean':
                    fill_value = group_df[column].mean()
                elif fill == 'median':
                    fill_value = group_df[column].median()
                elif fill == 'NA':
                    fill_value = np.nan

                # apply filter based on direction
                if direction == '>':
                    outliers = group_df[group_df[column] > bound].index
                elif direction == '<':
                    outliers = group_df[group_df[column] < bound].index
                elif direction == '>=':
                    outliers = group_df[group_df[column] >= bound].index
                elif direction == '<=':
                    outliers = group_df[group_df[column] <= bound].index
                elif direction == '==':
                    outliers = group_df[group_df[column] == bound].index
                elif direction == '!=':
                    outliers = group_df[group_df[column] != bound].index

                # fill outliers with specified fill value
                self.data.loc[outliers, column] = fill_value

            self.n_steps += 1
            self.metadata += f"{self.n_steps}. Replaced cells in column '{column}' where original value was {direction} {bound} by {fill}{', grouped by ' + ', '.join(group_by) if group_by else ''}'\n"
            self.artifacts[self.n_steps] = {'ReplaceByValue': {'column': column, 'bound': bound, 'direction': direction, 'group_by': group_by, 'fill': fill}}
        
        except Exception as e:
            print("Failed to replace column values.")
            current_dateTime = str(datetime.now())[0:19]
            print(current_dateTime + ': ' + str(e))
            
    
    def ReplaceByStd(self, column, group_by = None, n_std = 3, direction = '<>', fill = 'NA'):
        '''
        FUNCTION to replace cells in a column if beyond specified standard deviations from mean. By default, does not perform any grouping and replaces all values beyond 3 standard deviations in both directions by 'NA'.
        Parameters:
        - column: Name of column to be affected by replacement
        - group_by: List of column(s) to group by before applying replacement
        - n_std: Number of standard deviations beyond which to replace values
        - direction: The direction where replacement is to be applied (>, < or both)
        - fill: Value or type of value to fill by
        '''
        assert fill in ['mean','median','NA'] or isinstance(fill, int | float), "Require fill value to be numeric (int or float) or 'mean', 'median', or 'NA'"
        if group_by:
            assert isinstance(group_by, list) and all(col in list(self.data.columns) for col in group_by), "Require all column(s) to group by to exist in the dataframe and to be specified in a list."
        assert direction in ['>', '<', '<>'], "Direction should be one of '>', '<', '<>'"
        
        try:
            self.RecodeColumnTypes({column: 'float'})
            # group by columns (if any)
            if isinstance(group_by, str):
                group_by = [group_by]
            if group_by:
                grouped = self.data.groupby(group_by)
            else:
                grouped = [(None, self.data)]

            # iterate over groups and determine fill value
            for group_name, group_df in grouped:
                if fill == 'mean':
                    fill_value = group_df[column].mean()
                elif fill == 'median':
                    fill_value = group_df[column].median()
                else:
                    fill_value = fill

                # calculate mean and standard deviation
                mean_val = group_df[column].mean()
                std_val = group_df[column].std()
                
                # find values beyond n_std standard deviations
                if direction == '<>':
                    outliers = group_df[(group_df[column] > mean_val + n_std * std_val) | (group_df[column] < mean_val - n_std * std_val)].index
                elif direction == '>':
                    outliers = group_df[(group_df[column] > mean_val + n_std * std_val)].index
                elif direction == '<':
                    outliers = group_df[(group_df[column] < mean_val + n_std * std_val)].index
                
                # fill outliers with specified fill value
                self.data.loc[outliers, column] = fill_value

            self.n_steps += 1
            self.metadata += f"{self.n_steps}. Replaced cells in column '{column}' where original value was {direction}{n_std} standard deviations of the {'group ' if group_by else ''}mean by {fill}{', grouped by ' + ', '.join(group_by) if group_by else ''}'\n"
            self.artifacts[self.n_steps] = {'ReplaceByStd': {'column': column, 'group_by': group_by, 'n_std': n_std, 'direction': direction, 'fill': fill}}
            
        except Exception as e:
            print("Failed to filter column values.")
            current_dateTime = str(datetime.now())[0:19]
            print(current_dateTime + ': ' + str(e))
            
            
    #def ExtractYear(self, column)
            
    
    def RecodeColumnValues(self, column, recode_dict):
        '''
        FUNCTION to recode the values of a column in a pandas dataframe
        Parameters:
        - column: Name of column that is to be recoded.
        - recode_dict: Dictionary specifying the values and their targets.
        '''
        assert isinstance(column, str)
        assert isinstance(recode_dict, dict)
        
        try:
            self.RecodeColumnTypes({column: 'categorical'})
            self.data[column] = self.data[column].map(recode_dict).fillna(self.data[column])
            self.n_steps += 1
            self.metadata += f"{self.n_steps}. The following dictionary was used to recode the values of column '{column}':\
            {recode_dict}\n"
            self.artifacts[self.n_steps] = {'RecodeColumnValues': (column, recode_dict)}
            
        except Exception as e:
            print("Failed to recode column values.")
            current_dateTime = str(datetime.now())[0:19]
            print(current_dateTime + ': ' + str(e))
            
            
    def SumColumnValues(self, column_list, target_column):
        '''
        FUNCTION to populate a target column with the sum of the values of a list of columns
        Parameters:
        - column_list: List of columns to be summed
        - target_column: Name of column that is to be populated with the row-wise sums
        '''
        assert isinstance(column_list, list)
        assert set(column_list) <= set(self.data.columns)
        assert isinstance(target_column, str)
        assert target_column not in list(self.data.columns), f"The column {target_column} already exists in the dataframe. Choose another name."
        
        try:
            self.RecodeColumnTypes({item: 'float' for item in column_list})
            self.data[target_column] = self.data[column_list].sum(axis = 1)
            self.n_steps += 1
            self.metadata += f"{self.n_steps}. The column '{target_column}' was created and populated with the row-wise sums of the following columns:\
            {column_list}\n"
            self.artifacts[self.n_steps] = {'SumColumnValues': (column_list, target_column)}
            
        except Exception as e:
            print("Failed to sum column values.")
            current_dateTime = str(datetime.now())[0:19]
            print(current_dateTime + ': ' + str(e))
            
    
    def ImputeWithKNN(self, column, n_neighbors = 5, weights = 'uniform', metric = 'nan_euclidean', add_indicator = True):
        '''
        FUNCTION to perform KNN-based imputation for filling in missing values of a column.
        Parameters:
        - column: Name of column that is to be imputed
        - n_neighbors: Number of neighboring samples to use for imputation.
        - weights: Weight function used in prediction. Possible values:
            - 'uniform' : uniform weights. All points in each neighborhood are weighted equally.
            - 'distance' : weight points by the inverse of their distance.
        - metric: Metric used for the distance computation. Any metric from scikit-learn or scipy.spatial.distance can be used.
        - add_indicator: If True, adds a missing indicator variable for features with missing values.
        '''
        assert isinstance(column, str)
        assert column in list(self.data.columns), f"The column {column} could not be found in the dataframe."
        
        try:
            self.RecodeColumnTypes({column: 'float'})
            imputer = KNNImputer(n_neighbors = n_neighbors,
                                 weights = weights,
                                 metric = metric,
                                 add_indicator = add_indicator)
            imputed_array = imputer.fit_transform(self.data[[column]])
            
            if add_indicator:
                # expand dataframe to include extra column with indicator suffix for missing value
                columns = list(self.data.columns) + [f"{col}_ImputeWithKNN_indicator" for col in self.data.columns if self.data[col].isnull().any()]
            else:
                columns = list(self.data.columns)
            
            self.data[column] = pd.Series(imputed_array[:,0], name = column)
            self.n_steps += 1
            self.metadata += f"{self.n_steps}. KNN-based imputation performed on column '{column}' with {n_neighbors} neighbors, weights = '{weights}', and metric = '{metric}'.\n"
            self.artifacts[self.n_steps] = {'ImputeWithKNN': {'column': column, 'n_neighbors': n_neighbors, 'weights': weights, 'metric': metric, 'add_indicator': add_indicator}}
            
        except Exception as e:
            print("Failed to perform KNN-based imputation.")
            current_dateTime = str(datetime.now())[0:19]
            print(current_dateTime + ': ' + str(e))
            
    
    def ImputeWithEquation(self, column, Xs, coefficients):
        '''
        FUNCTION to impute missing values in a column based on user-specified custom equation using other columns as dependent variables.
        Parameters:
        - column: Name of column that is to be imputed
        - Xs: List of columns (dependent variables) used for regression equation
        - coefficients: List of coefficients used for regression equation
        '''
        assert isinstance(Xs, list) and isinstance(coefficients, list) and len(Xs) == len(coefficients), "Require both Xs and coefficients to be lists of equal length."
        assert all(X in list(self.data.columns) for X in Xs), "Require all independent variable columns to exist in the dataframe."
        # TODO: apply to numeric columns using numeric columns only
        
        try:
            missing_values = self.data[self.data[column].isnull()]
            predicted_values = (missing_values[Xs] * coefficients).sum(axis = 1)
            self.data.loc[missing_values.index, column] = predicted_values

            self.n_steps += 1
            self.metadata += f"{self.n_steps}. Imputed missing values in column '{column}' using regression equation based on columns {Xs}, with coefficients {coefficients}\n"
            self.artifacts[self.n_steps] = {'ImputeWithEquation': {'column': column, 'Xs': Xs, 'coefficients': coefficients}}
        
        except Exception as e:
            print("Failed to perform regression-based imputation.")
            current_dateTime = str(datetime.now())[0:19]
            print(current_dateTime + ': ' + str(e))
        
    
    def ImputeWithValue(self, column, value, group_by = None):
        '''
        FUNCTION to impute missing values in a column using user-specified value.
        Parameters:
        - column: Name of column that is to be imputed
        - value: Value to impute by
        - group_by: List of column(s) to group by before performing imputation
        '''
        if group_by:
            assert isinstance(group_by, list) and all(col in list(self.data.columns) for col in group_by), "Require all column(s) to group by to exist in the dataframe and to be specified in a list."
        
        try:
            if group_by:
                if isinstance(group_by, str):
                    group_by = [group_by]
                self.data[column] = self.data.groupby(group_by)[column].transform(lambda x: x.fillna(value))
            else:
                self.data[column] = self.data[column].fillna(value)

            self.n_steps += 1
            self.metadata += f"{self.n_steps}. Imputed missing values in column '{column}' with '{value}'" + (f", grouped by {group_by}" if group_by else "") + "\n"
            self.artifacts[self.n_steps] = {'ImputeWithValue': {'column': column, 'value': value, 'group_by': group_by}}

        
        except Exception as e:
            print("Failed to perform imputation.")
            current_dateTime = str(datetime.now())[0:19]
            print(current_dateTime + ': ' + str(e))
    
    
    def exportArtifacts(self, filetype = 'json'):
        '''
        Exports the artifacts in the transformation pipeline for reproducibility.
        '''
        return self.artifacts
    
    
    def importArtifacts(self, artifacts):
        '''
        Imports the artifacts of a transformation pipeline and applies to data.
        '''
        assert isinstance(artifacts, dict)
        
        try:
            for n, step in artifacts.items():
                for method, args in step.items():
                    if method == "DropColumns":
                        self.DropColumns(args)
                    elif method == "RenameColumns":
                        self.RenameColumns(args)
                    elif method == "RecodeColumnTypes":
                        self.RecodeColumnTypes(args)
                    elif method == "RecodeColumnValues":
                        self.RecodeColumnValues(args[0], args[1])
                    elif method == "SumColumnValues":
                        self.SumColumnValues(args[0], args[1])
                    elif method == "ImputeWithKNN":
                        self.ImputeWithKNN(args[0], args[1], args[2], args[3], args[4])
                    elif method == "ImputeWithEquation":
                        self.ImputeWithEquation(args[0], args[1], args[2])
                    elif method == "ImputeWithValue":
                        self.ImputeWithValue(args[0], args[1], args[2])
                    elif method == "ReplaceByValue":
                        self.FilterColumnByValue(args[0], args[1], args[2], args[3], args[4])
                    elif method == "ReplaceByStd":
                        self.FilterColumnByStd(args[0], args[1], args[2], args[3])
                    else:
                        raise Exception(f"{n}. {method} could not be executed. Terminate")
        
        except Exception as e:
            print("Failed to import artifacts.")
            current_dateTime = str(datetime.now())[0:19]
            print(current_dateTime + ': ' + str(e))
