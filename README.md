# data-explorer

The vision is to create a platform for users to explore data wrangling options when cleaning their tabular data sets. A user will be able to apply data wrangling methodologies to each column of their data set and visualize the effect on various plots with the choice of different columns for plot axes.

A platform such as this can explain the impact of different data cleaning and imputation strategies on downstream model performance. Rather than apply various permutations and combinations, run a model, display evaluation metrics, and (often) rinse and repeat to obtain marginally better results, we present this interactive platform that instead allows users to visualize the effect of pre-processing decisions on the data distribution itself.

How to run:
1. pull this repository
2. create a virtual environment to pip install all dependencies in requirements.txt
3. `streamlit run app/Start.py`
