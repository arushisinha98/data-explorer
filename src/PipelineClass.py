from datetime import datetime
import pandas as pd
from pandas.api.types import CategoricalDtype
from sklearn.impute import KNNImputer


class Pipeline():

    def __init__(self, input_df, description = ""):
        assert isinstance(input_df, pd.DataFrame)
        
        try:
            input_df = input_df.convert_dtypes() # set best dtype for columns
            input_df = input_df.reset_index(drop = True) # set one index = one row
            
            self.data = input_df
            self.metadata = description + "\n"
            self.n_steps = 0
            self.artifacts = dict()
            
        except Exception as e:
            print("Failed to create Pipeline object.")
            current_dateTime = str(datetime.now())[0:19]
            print(current_dateTime + ': ' + str(e))
            
            
    def __str__(self):
        return self.metadata
    
    
    def getData(self):
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
            self.metadata += f"{self.n_steps}. The following dictionary was used to recode the names of the columns:\
            {recode_dict}\n"
            self.artifacts[self.n_steps] = {'RecodeColumnNames': recode_dict}

        except Exception as e:
            print("Failed to recode column names.")
            current_dateTime = str(datetime.now())[0:19]
            print(current_dateTime + ': ' + str(e))
            
            
    def getColumnTypes(self):
        '''
        FUNCTION to get the data type of each column
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
        valid_dtypes = {'char', 'string', 'int', 'float', 'bool', 'categorical', 'date', 'datetime'}
        assert set(recode_dict.values()) <= valid_dtypes,\
        f"You may only recode column into the following types: {valid_dtypes}"
        
        try:
            df = self.data
            for column, dtype in recode_dict.items():
                if dtype == 'char':
                    df[column] = df[column].astype(str).str.slice(0, 1)
                elif dtype == 'string':
                    df[column] = df[column].astype('string')
                elif dtype == 'int':
                    df[column] = pd.to_numeric(df[column], downcast = 'integer', errors = 'coerce')
                elif dtype == 'float':
                    df[column] = df[column].astype(float)
                elif dtype == 'bool':
                    df[column] = df[column].astype(bool)
                elif dtype == 'categorical':
                    df[column] = df[column].astype('category')
                elif dtype == 'date' or dtype == 'datetime':
                    df[column] = pd.to_datetime(df[column], errors = 'coerce')
            
            self.data = df
            self.n_steps += 1
            self.metadata += f"{self.n_steps}. The following dictionary was used to recode the dtypes of the columns:\
            {recode_dict}\n"
            self.artifacts[self.n_steps] = {'RecodeColumnTypes': recode_dict}

        except Exception as e:
            print("Failed to recode column dtypes.")
            current_dateTime = str(datetime.now())[0:19]
            print(current_dateTime + ': ' + str(e))
    
    
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
            
    
    # def ImputeWithRegression(self, column, Xs, coefficients):
    # def ImputeWithValue(self, column, value, group_by = None):
    
    
    # def FilterColumnByValue(self, column, value, direction, group_by = None, fill = 'null'):
    # def FilterColumnByStd(self, column, n_std = 3, group_by = None, fill = 'null'):
    
    """
    def FilterColumnByStd(self, column, group_by = None, n_std = 3, fill = 'null'):
        '''
        FUNCTION to filter out values by standard deviation. By default, does not perform any grouping and replaces all values beyond 3 standard deviations by null.
        Parameters:
        - column: Name of column to be filtered
        - group_by: Name of column or list of columns to group by before applying filter
        - n_std: Number of standard deviations beyond which to filter
        - fill: Value or type of value to fill by
        '''
        assert fill in ['mean','null'] or isinstance(fill, int | float), "Require fill value to be numeric (int or float) or 'mean' or 'null'"
        assert isinstance(group_by, string | list) and all(group_by in list(self.data.columns)), "Require all column(s) to group by to exist in the dataframe and to be specified in a list."
        
        try:
            self.
            
        except Exception as e:
            print("Failed to filter column values.")
            current_dateTime = str(datetime.now())[0:19]
            print(current_dateTime + ': ' + str(e))
    """
    
    
    def exportArtifacts(self, filetype = 'json'):
        '''
        FUNCTION to export the artifacts in the transformation pipeline for reproducibility
        '''
        return self.artifacts
    
    
    def importArtifacts(self, artifacts):
        '''
        FUNCTION to import and apply a transformation pipeline from the 
        '''
        assert isinstance(artifacts, dict)
        
        try:
            for n, step in artifacts.items():
                for method, args in step.items():
                    if method == "DropColumns":
                        self.DropColumns(args)
                    elif method == "RecodeColumnNames":
                        self.RecodeColumnNames(args)
                    elif method == "RecodeColumnTypes":
                        self.RecodeColumnTypes(args)
                    elif method == "RecodeColumnValues":
                        self.RecodeColumnValues(args[0], args[1])
                    elif method == "SumColumnValues":
                        self.SumColumnValues(args[0], args[1])
                    else:
                        raise Exception(f"{n}. {method} could not be executed. Terminate")
        
        except Exception as e:
            print("Failed to import artifacts.")
            current_dateTime = str(datetime.now())[0:19]
            print(current_dateTime + ': ' + str(e))
