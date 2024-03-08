from datetime import datetime
import pandas as pd
from pandas.api.types import CategoricalDtype


class Pipeline():

    def __init__(self, input_df, description = ""):
        assert isinstance(input_df, pd.DataFrame)
        
        try:
            # set best dtype for columns
            input_df = input_df.convert_dtypes()
            # set one index = one row
            input_df = input_df.reset_index(drop = True)
            
            self.data = input_df
            self.metadata = description + "\n"
            self.n_steps = 0
            
        except Exception as e:
            print("Failed to create Pipeline object.")
            current_dateTime = str(datetime.now())[0:19]
            print(current_dateTime + ': ' + str(e))
            
            
    def __str__(self):
        return self.metadata
    
    
    def getData(self):
        return self.data
    
    
    def listFunctions(self):
        '''
        Lists all the transformation functions available in the class object.
        '''
        class_members = dir(self) # list of all attributes and methods of the class
        functions = [member for member in class_members if callable(getattr(self, member)) and member[0].isupper()]
        
        # Print the list of functions
        print("Functions available in the class object:")
        for function in functions:
            print("-", function)
            
    
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

        except Exception as e:
            print("Failed to drop specified columns.")
            current_dateTime = str(datetime.now())[0:19]
            print(current_dateTime + ': ' + str(e))


    def RecodeColumnNames(self, recode_dict):
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
        assert isinstance(recode_dict, dict)
        
        try:
            self.RecodeColumnTypes({column: 'categorical'})
            self.data[column] = self.data[column].map(recode_dict).fillna(self.data[column])
            self.n_steps += 1
            self.metadata += f"{self.n_steps}. The following dictionary was used to recode the values of column '{column}':\
            {recode_dict}\n"
            
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
        assert set(column_list) <= set(self.data.columns)
        assert target_column not in list(self.data.columns), f"The column {target_column} already exists in the dataframe. Choose another name."
        
        try:
            self.RecodeColumnTypes({item: 'float' for item in column_list})
            self.data[target_column] = self.data[column_list].sum(axis = 1)
            self.n_steps += 1
            self.metadata += f"{self.n_steps}. The column '{target_column}' was created and populated with the row-wise sums of the following columns:\
            {column_list}\n"
            
        except Exception as e:
            print("Failed to sum column values.")
            current_dateTime = str(datetime.now())[0:19]
            print(current_dateTime + ': ' + str(e))