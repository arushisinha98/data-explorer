#st.title("Tourism Receipts Data Guide")
#st.caption("A data visualization and experimentation tracking aid for TR2.0 Integration.")

# list categorical variables

# list numeric variables

# show .describe() output


#st.header("Guided Pre-processing")
#selection_type = st.radio("Select data.", ("2016-2018", "2016-2019", "2019"))

# retrieve the specified data set
#input_df = pd.DataFrame(np.random.randint(0,100, size = (100, 4)),
#                        columns = list('ABCD'))

# initialize pipeline
#pipeline = Pipeline(input_df)
#functions = pipeline.listFunctions()
#n = 1

# format dropdown to select transformation step and specify arguments
"""
def UserGuidedPreprocess(n):
    
    # dropdown to select transformation step
    option = st.selectbox(
    "", functions,
    index = None,
    placeholder = "Select Transformation ...",
    label_visibility = 'collapsed')
    
    if option == 'DropColumns':
        column_list = st.multiselect('Select columns to drop.', input_df.columns)
        
        st.write(f"{n}. The following columns will be dropped:\
        {column_list}")
        
    elif option == 'RecodeColumnNames':
        recode_df = pd.DataFrame(columns = ["column", "name"])
        config = {
            "column": st.column_config.SelectboxColumn("Column Name",
                                                       options = input_df.columns),
            "name": st.column_config.TextColumn("Rename")
        }
        recode_dict = recode_df.set_index("column").T.to_dict('records')[0]
        
        st.write(f"{n}. The following dictionary will be used to recode the names of the columns:\
        {recode_dict}")
    
    elif option == 'RecodeColumnTypes':
        recode_df = pd.DataFame(columns = ["column", "dtype"])
        config = {
            "column": st.column_config.SelectboxColumn("Column Name",
                                                       options = input_df.columns),
            "dtype": st.column_config.SelectboxColumn("Column Type,
                                                      options = ['char', 'string', 'int', 'float', 'bool', 'categorical', 'date', 'datetime'])
        }
        recode_dict = recode_df.set_index("column").T.to_dict('records')[0]
        
        st.write(f"{n}. The following dictionary will be used to recode the dtypes of the columns:\
        {recode_dict}")
        
    elif option == 'RecodeColumnValues':
        recode_df = pd.DataFrame(columns = ["column", "map"])
        # visualize column values (categorical)
        config = {
            "column": st.column_config.SelectboxColumn("Column Name",
                                                       optins = input_df.columns),
            "map": st.column_config.TextColumn("Mapping Dictionary")
        }
        recode_dict = recode_df.set_index("column").T.to_dict('records')[0]
        # note: mapping dictionary will be user input string
        
        st.write(f"{n}. The following dictionary will be used to recode the values of the columns:\
        {recode_dict}"

"""

"""
df = pd.DataFrame(columns = ["Transformation"])
config = {
    'Transformation' : st.column_config.SelectboxColumn(
        'Pre-process Step', options = functions, required = True)
}

result = st.data_editor(df, column_config = config, num_rows = 'dynamic')
"""

"""
# option to add additional steps
add = st.button("Add Step")
if add:
    # append a container with transformation choices
    UserGuidedProcess(n)
    n += 1

test = st.button("Test Pipeline")
if test:
    # navigate to comparative visualization page
    
export = st.button("Export Pipeline")
if export:
    # export pipeline artifacts and save as JSON
    
"""

"""
st.header("1. Data Selection")
selection_type = st.radio("a. Type of Selection.",
                          ("**Continuous** to select all data collected during a continuous period.",
                           "**Discrete** to specify select years from the available data."))

if selection_type == "Continuous":
    YEAR_START, YEAR_END = st.slider("Select a continuous time period", 2016, 2023, (2016, 2016))
"""

