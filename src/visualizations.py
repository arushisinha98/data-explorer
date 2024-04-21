import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
import altair as alt


def PlotBar(df, x, group_by = None, width = 600, height = 400):
    '''
    FUNCTION to plot 1D bar chart using Altair, for display on Streamlit.
    Parameters:
    - df: Dataframe
    - x: Name of column to be represented by bars
    - group_by: List of column(s) to group by for visualization
    - width: width of chart
    - height: height of chart
    '''
    assert isinstance(df, pd.DataFrame)
    assert x in list(df.columns), f"The column '{x}' does not exist in the dataframe."
    if group_by:
        assert isinstance(group_by, list) and all(col in list(df.columns) for col in group_by), "Require all column(s) to group by to exist in the dataframe and to be specified in a list."
    
    try:
        df_filtered = df.copy()
        df_filtered = df_filtered.dropna(subset=[x])
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
                y=alt.Y('count():Q', title='Count'),
                tooltip=[alt.Tooltip(f'{x}:N'), alt.Tooltip('count():Q')]
            )
        
        chart = chart.properties(width=width, height=height)
        return chart
    
    except Exception as e:
        print("Failed to create bar chart.")
        current_dateTime = str(datetime.now())[0:19]
        print(current_dateTime + ': ' + str(e))


def PlotDensity(df, x, group_by = None, width = 600, height = 400):
    '''
    FUNCTION to plot 1D density chart using Altair, for display on Streamlit.
    Parameters:
    - df: DataFrame
    - x: Name of column to be represented by density
    - group_by: List of column(s) to group by for visualization
    - width: width of chart
    - height: height of chart
    '''
    assert isinstance(df, pd.DataFrame)
    assert x in list(df.columns), f"The column '{x}' does not exist in the dataframe."
    if group_by:
        assert isinstance(group_by, list) and all(col in list(df.columns) for col in group_by), "Require all column(s) to group by to exist in the dataframe and to be specified in a list."
    
    try:
        df_filtered = df.copy()
        df_filtered = df_filtered.dropna(subset=[x])
        type = ['T' if dict(df.dtypes)[x] == "datetime64[ns]" else 'Q']
        
        if group_by: # new 'Group' column for unique combinations
            df_filtered['Group'] = df_filtered[group_by].astype(str).agg(', '.join, axis=1)
            chart = alt.Chart(df_filtered).transform_density(
                density=x,
                groupby=['Group'],
                as_=[x, 'density'],
            ).mark_area(opacity=0.5).encode(
                x=alt.X(f'{x}:{type[0]}', title=x),
                y=alt.Y('density:Q', title='Density'),
                color=alt.Color('Group:N', legend=alt.Legend(title=', '.join(group_by))),
                tooltip=[alt.Tooltip(f'{x}:{type[0]}'), alt.Tooltip('density:Q'), 'Group:N']
            )
        else:
            chart = alt.Chart(df_filtered).transform_density(
                density=x,
                as_=[x, 'density']
            ).mark_area(opacity=0.5).encode(
                x=alt.X(f'{x}:{type[0]}', title=x),
                y=alt.Y('density:Q', title='Density'),
                tooltip=[alt.Tooltip(f'{x}:{type[0]}'), alt.Tooltip('density:Q')]
            )
        
        chart = chart.properties(width=width, height=height)
        return chart
    
    except Exception as e:
        print("Failed to create density plot.")
        current_dateTime = str(datetime.now())[0:19]
        print(current_dateTime + ': ' + str(e))
        

def PlotScatter(df, x, y, group_by = None, width = 600, height = 400):
    '''
    FUNCTION to create 2D scatter plot using Altair, for display on Streamlit.
    Parameters:
    - df: DataFrame
    - x: Name of the column for x-axis
    - y: Name of the column for y-axis
    - group_by: List of column(s) to group by for visualization
    - width: width of chart
    - height: height of chart
    '''
    assert isinstance(df, pd.DataFrame)
    assert x in list(df.columns), f"The column '{x}' does not exist in the dataframe."
    assert y in list(df.columns), f"The column '{y}' does not exist in the dataframe."
    if group_by:
        assert isinstance(group_by, list) and all(col in list(df.columns) for col in group_by), "Require all columns to group by to exist in the dataframe and to be specified in a list."
    
    try:
        df_filtered = df.copy()
        df_filtered = df_filtered.dropna(subset=[x,y])
        type, axis = 'Q', alt.Axis()
        if dict(df.dtypes)[x] == "datetime64[ns]":
            type = 'T'
            axis = alt.Axis(format = '%b %Y')
        
        if group_by: # new 'Group' column for unique combinations
            df_filtered['Group'] = df_filtered[group_by].astype(str).agg(', '.join, axis=1)
            
            chart = alt.Chart(df_filtered).mark_circle().encode(
                x=alt.X(f'{x}:{type}', title=x, axis=axis),
                y=alt.Y(f'{y}:Q', title=y),
                color=alt.Color('Group:N', legend=alt.Legend(title=', '.join(group_by))),
                tooltip=[alt.Tooltip(f'{x}:{type}'), alt.Tooltip(f'{y}:Q'), 'Group:N']
            )
        else:
            chart = alt.Chart(df_filtered).mark_circle().encode(
                x=alt.X(f'{x}:{type}', title=x, axis=axis),
                y=alt.Y(f'{y}:Q', title=y),
                tooltip=[alt.Tooltip(f'{x}:{type}'), alt.Tooltip(f'{y}:Q')]
            )
        
        chart = chart.properties(width=width, height=height)
        return chart
    
    except Exception as e:
        print("Failed to create scatter plot.")
        current_dateTime = str(datetime.now())[0:19]
        print(current_dateTime + ': ' + str(e))
        
        
def PlotBubble(df, x, y, width = 600, height = 400):
    '''
    FUNCTION to create a 2D bubble plot using Altair, for display on Streamlit.
    Parameters:
    - df: DataFrame
    - x: Name of the column for the x-axis
    - y: Name of the column for the y-axis
    - width: width of chart
    - height: height of chart
    '''
    assert isinstance(df, pd.DataFrame)
    assert x in list(df.columns), f"The column '{x}' does not exist in the dataframe."
    assert y in list(df.columns), f"The column '{y}' does not exist in the dataframe."
    
    try:
        df_filtered = df.copy()
        df_filtered = df_filtered.dropna(subset=[x,y])
        
        chart = alt.Chart(df_filtered).mark_circle().encode(
            x=alt.X(f'{x}:O', title=x),
            y=alt.Y(f'{y}:O', title=y),
            size='sum(count):Q',
            #tooltip=[alt.Tooltip(f'{x}:O'), alt.Tooltip(f'{y}:O'), 'Group:N']
        )
        
        chart = chart.properties(width=width, height=height)
        return chart
        
    except Exception as e:
        print("Failed to create bubble plot.")
        current_dateTime = str(datetime.now())[0:19]
        print(current_dateTime + ': ' + str(e))
        

def PlotBox(df, x, width = 600, height = 60):
    '''
    FUNCTION to create a horizontal boxplot using Altair, for display on Streamlit.
    Parameters:
    - df: Dataframe
    - x: Name of the column for the x-axis
    - width: width of chart
    - height: height of chart
    '''
    assert isinstance(df, pd.DataFrame)
    assert x in list(df.columns), f"The column '{x}' does not exist in the dataframe."
    
    try:
        df_filtered = df.copy()
        df_filtered = df_filtered.dropna(subset=[x])
        df_filtered.loc[:,"Y"] = 0
        
        chart = alt.Chart(df_filtered).mark_boxplot().encode(
            x=alt.X(f'{x}:Q', title="").scale(zero=False)
        )
        
        chart = chart.properties(width=width, height=height)
        return chart
        
    except Exception as e:
        print("Failed to create boxplot.")
        current_dateTime = str(datetime.now())[0:19]
        print(current_dateTime + ': ' + str(e))


def PlotStrip(df, x, width = 600, height = 60):
    '''
    FUNCTION to create strip plot using Altair, for display on Streamlit.
    Parameters:
    - df: Dataframe
    - x: Name of the column for x-axis
    - width: width of chart
    - height: height of chart
    '''
    assert isinstance(df, pd.DataFrame)
    assert x in list(df.columns), f"The column '{x}' does not exist in the dataframe."
    
    try:
        df_filtered = df.copy()
        df_filtered = df_filtered.dropna(subset=[x])
        df_filtered.loc[:,"Y"] = 0
        
        chart = alt.Chart(df_filtered).mark_tick().encode(
                x=alt.X(f'{x}:Q', title=""),
                y=alt.Y('Y:Q', title="", axis=None),
                tooltip=[alt.Tooltip(f'{x}:Q')]
                )
        
        chart = chart.properties(width=width, height=height)
        return chart
        
    except Exception as e:
        print("Failed to create strip plot.")
        current_dateTime = str(datetime.now())[0:19]
        print(current_dateTime + ': ' + str(e))
