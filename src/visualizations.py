import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from datetime import datetime
import altair as alt


def PlotHistogram(df, x, group_by = None):
    '''
    FUNCTION to plot 1D histogram chart using Altair, for display on Streamlit.
    Parameters:
    - df: Dataframe
    - x: Name of column to be represented by bars
    - group_by: List of column(s) to group by for visualization
    '''
    assert x in list(df.columns), f"The column '{x}' does not exist in the dataframe."
    assert isinstance(df, pd.DataFrame)
    if group_by:
        assert isinstance(group_by, list) and all(col in list(df.columns) for col in group_by), "Require all column(s) to group by to exist in the dataframe and to be specified in a list."
    
    try:
        df_filtered = df.dropna(subset=[x])
        if group_by: # new 'Group' column for unique combinations
            df_filtered['Group'] = df_filtered[group_by].astype(str).agg(', '.join, axis=1)
            chart = alt.Chart(df_filtered).mark_bar().encode(
                x=alt.X(f'{x}:N', title=x),
                y=alt.Y('count():Q', title='Count'),
                color=alt.Color('Group:N',
                legend=alt.Legend(title=str(group_by)[1:-1].replace("'",""))),
                tooltip=[alt.Tooltip(f'{x}:N'), alt.Tooltip('count():Q'), 'Group:N']
            )
        else:
            chart = alt.Chart(df_filtered).mark_bar().encode(
                x=alt.X(f'{x}:N', title=x),
                y=alt.Y('count():Q', title='Count')
            )
        
        chart = chart.properties(width = 600, height = 400)
        return chart
    
    except Exception as e:
        print("Failed plot histogram.")
        current_dateTime = str(datetime.now())[0:19]
        print(current_dateTime + ': ' + str(e))


def PlotDensity(df, x, group_by = None):
    '''
    FUNCTION to plot 1D density chart using Altair, for display on Streamlit.
    Parameters:
    - df: DataFrame
    - x: Name of column to be represented by density
    - group_by: List of column(s) to group by for visualization
    '''
    assert x in list(df.columns), f"The column '{x}' does not exist in the dataframe."
    assert isinstance(df, pd.DataFrame)
    if group_by:
        assert isinstance(group_by, list) and all(col in list(df.columns) for col in group_by), "Require all column(s) to group by to exist in the dataframe and to be specified in a list."
    
    try:
        df_filtered = df.dropna(subset=[x])
        if group_by: # new 'Group' column for unique combinations
            df_filtered['Group'] = df_filtered[group_by].astype(str).agg(', '.join, axis=1)
            chart = alt.Chart(df_filtered).transform_density(
                density=x,
                groupby=['Group'],
                as_=[x, 'density'],
            ).mark_area(opacity=0.5).encode(
                x=alt.X(f'{x}:Q', title=x),
                y=alt.Y('density:Q', title='Density'),
                color=alt.Color('Group:N', legend=alt.Legend(title=', '.join(group_by))),
                tooltip=[alt.Tooltip(f'{x}:Q'), alt.Tooltip('density:Q'), 'Group:N']
            )
        else:
            chart = alt.Chart(df_filtered).transform_density(
                density=x,
                as_=[x, 'density']
            ).mark_area(opacity=0.5).encode(
                x=alt.X(f'{x}:Q', title=x),
                y=alt.Y('density:Q', title='Density'),
                tooltip=[alt.Tooltip(f'{x}:Q'), alt.Tooltip('density:Q')]
            )
        
        chart = chart.properties(width=600, height=400)
        return chart
    
    except Exception as e:
        print(f"Failed to plot density.")
        current_dateTime = str(datetime.now())[0:19]
        print(current_dateTime + ': ' + str(e))
        

def PlotScatter(df, x, y, group_by = None):
    '''
    FUNCTION to create 2D scatter plot using Altair, for display on Streamlit.
    Parameters:
    - df: DataFrame
    - x: Name of the column for x-axis
    - y: Name of the column for y-axis
    - group_by: List of column(s) to group by for visualization
    '''
    assert x in list(df.columns), f"The column '{x}' does not exist in the dataframe."
    assert y in list(df.columns), f"The column '{y}' does not exist in the dataframe."
    assert isinstance(df, pd.DataFrame)
    if group_by:
        assert isinstance(group_by, list) and all(col in list(df.columns) for col in group_by), "Require all columns to group by to exist in the dataframe and to be specified in a list."
    
    try:
        df_filtered = df.dropna(subset=[x, y])
        
        # TODO: deal with datetime x or y
        if group_by: # new 'Group' column for unique combinations
            df_filtered['Group'] = df_filtered[group_by].astype(str).agg(', '.join, axis=1)
            chart = alt.Chart(df_filtered).mark_circle().encode(
                x=alt.X(f'{x}:Q', title=x),
                y=alt.Y(f'{y}:Q', title=y),
                color=alt.Color('Group:N', legend=alt.Legend(title=', '.join(group_by))),
                tooltip=[alt.Tooltip(f'{x}:Q'), alt.Tooltip(f'{y}:Q'), 'Group:N']
            )
        else:
            chart = alt.Chart(df_filtered).mark_circle().encode(
                x=alt.X(f'{x}:Q', title=x),
                y=alt.Y(f'{y}:Q', title=y),
                tooltip=[alt.Tooltip(f'{x}:Q'), alt.Tooltip(f'{y}:Q')]
            )
        
        chart = chart.properties(width=600, height=400)
        return chart
    
    except Exception as e:
        print(f"Failed to create scatter plot.")
        current_dateTime = str(datetime.now())[0:19]
        print(current_dateTime + ': ' + str(e))


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
        
            
