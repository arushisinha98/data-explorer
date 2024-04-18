import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from datetime import datetime


def KDEPlot(input_dfs, columns, labels, figname = "", save = False):
    '''
    FUNCTION to plot and compare KDE of different data sets.
    '''
    assert all([col in df.columns for col in columns for df in input_dfs]), "Require all columns to exist in all input dataframes."
    assert len(input_dfs) == len(labels), "Require one label per input dataframe."
    if save:
        assert len(figname) > 0, "Require non-empty string as figname to save the plot."
    
    try:
        ncols = len(columns)
        fig, axs = plt.subplots(ncols//2+1, 2, figsize = (15, 5*(ncols//2+1)))

        for ii, col in enumerate(columns):
            irow, icol = ii//2, ii-2*(ii//2)
            axs[irow, icol].set_title(col)
            for jj, df in enumerate(input_dfs):
                if len(df[col].unique()) > 5:
                    sns.kdeplot(df[col], fill = True, ax = axs[irow, icol], label = labels[jj])
            axs[irow, icol].legend();
        
        if save:
            plt.savefig(f'/home/dsml01/Ultron/Step4/figures/{figname}.png')
            plt.close()
        else:
            plt.show()
        
    except Exception as e:
        print(f"Failed to plot KDE visualizations of the data.")
        current_dateTime = str(datetime.now())[0:19]
        print(current_dateTime + ': ' + str(e))
        
        
def get_n_bins(data):
    x = np.concatenate(data, axis = None)
    q25, q75 = np.percentile(x, [25, 75])
    bin_width = 2*(q75 - q25)*len(x)**(-1/3)
    bins = round((x.max() - x.min())/bin_width)
    return bins


def HistPlot(input_dfs, columns, labels, figname = "", save = False):
    '''
    FUNCTION to plot histograms of different data sets
    '''
    assert all([col in df.columns for col in columns for df in input_dfs]), "Require all columns to exist in all input dataframes."
    assert len(input_dfs) == len(labels), "Require one label per input dataframe."
    if save:
        assert len(figname) > 0, "Require non-empty string as figname to save the plot."
        
    try:
        ncols = len(columns)
        fig, axs = plt.subplots(ncols//2+1, 2, figsize = (15, 5*(ncols//2+1)))
        
        for ii, col in enumerate(columns):
            irow, icol = ii//2, ii-2*(ii//2)
            axs[irow, icol].set_title(col)
            nbins = max([get_n_bins(np.asarray(df[col])) for df in input_dfs])
            data_array = [np.asarray(df[col]) for df in input_dfs]
            axs[irow, icol].hist(data_array, nbins, histtype = 'bar', label = labels[jj])
            axs[irow, icol].legend();
            
        if save:
            plt.savefig(f'/home/dsml01/Ultron/Step4/figures/{figname}.png')
            plt.close()
        else:
            plt.show()
        
    except Exception as e:
        print(f"Failed to plot histogram visualizations of the data.")
        current_dateTime = str(datetime.now())[0:19]
        print(current_dateTime + ': ' + str(e))
        
            
