import pandas as pd
from datetime import datetime
import os
from os import listdir
from os.path import isfile, join

from constants import main_path
from preprocess import minimum_spend_imputation


class DataObject:
    
    def __init__(self, source, version, model = None):
        assert source in ["OVS", "Synthetic"], "Data source must be one of the following: OVS, Synthetic"
        if source == "Synthetic":
            assert model in ["TVAE", "CTGAN", "TGAN"], "Select one of the following synthetic data generation models: TVAE, CTGAN, TGAN"
        
        try:
            self.source = source
            self.version = version
            self.model = model
            self.imputations = False
            
            self.directory = self.get_directory()
            self.data = self.read_data()
            self.last_updated = self.get_modification_date()
            self.size = (len(self.data.index), len(self.data.columns))
            
            
        except Exception as e:
            print("Failed to create Data class object.")
            current_dateTime = str(datetime.now())[0:19]
            print(current_dateTime + ': ' + str(e))
        
    
    def __str__(self):
        return f"{self.source} Data: {self.version}.\nModel: {self.model}\nSize: {self.size}\nLast Updated: {self.last_updated}"
        
    
    def get_directory(self):
        '''
        FUNCTION to get the directory associated with the Data class object.
        '''
        try:
            if self.source == "OVS":
                return f"{main_path}/Step1/Real Data/OVS{self.version}/"
            else:
                return f"{main_path}/Step3/Synthetic Data/"
            
        except Exception as e:
            print("Failed to get directory associated with Data class object.")
            current_dateTime = str(datetime.now())[0:19]
            print(current_dateTime + ': ' + str(e))
    
    
    def get_filenames(self):
        '''
        FUNCTION to get a list of files associated with the Data class object. If source is OVS, there is usually only one file in the associated directory. If source is Synthetic, there may be more than one file in the list due to repeated generation of synthetic data sets by the same model.
        '''
        try:
            # list all valid CSV files in directory
            files = [f for f in listdir(self.directory) if isfile(join(self.directory, f)) and
                     f.endswith(".csv") and not f.startswith(".")]
            
            if self.source == "OVS":
                return [join(self.directory, f) for f in files if f"{self.source}{self.version}" in f] # match OVS and version
            else:
                return [join(self.directory, f) for f in files if f"{self.model}".lower() in f] # match model name
            
        except Exception as e:
            print("Failed to get filenames associated with Data class object")
            current_dateTime = str(datetime.now())[0:19]
            print(current_dateTime + ': ' + str(e))
    
    
    def read_data(self):
        '''
        FUNCTION to create a pandas dataframe containing all the data associated wth the Data class object.
        '''
        try:
            files = self.get_filenames()
            master_df = pd.DataFrame()
            for file in files:
                master_df = master_df.append(pd.read_csv(file))
            return master_df
        
        except Exception as e:
            print("Failed to read data to populate Data class object")
            current_dateTime = str(datetime.now())[0:19]
            print(current_dateTime + ': ' + str(e))
    
    
    def get_modification_date(self):
        '''
        FUNCTION to get the last imputation date 
        '''
        stats = [os.stat(file) for file in self.get_filenames()]
        dates = [datetime.fromtimestamp(stat.st_mtime) for stat in stats]
        return max(dates)