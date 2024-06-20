import streamlit as st
import streamlit_mermaid as mermaid
import pandas as pd

import sys
sys.path.append('src/')
from PipelineClass import Pipeline


class_diagram = """
    classDiagram
        class START{
            DropColumns
            DropRows
            RenameColumns
            RecodeColumnTypes
        }
        class Outliers{
        <<numerical>>
            ReplaceByValue
            ReplaceByStd
        }
        class Scale{
        <<numerical>>
            LogTransform
            Standardize
            MinMaxScale
            RankTransform
            RobustScale
            MedianAbsoluteDeviation
            TrimmedMean
            Windsorize
        }
        class Impute{
        <<categorical or numerical>>
        
            both : ImputeWithValue
            both : ImputeWithKNN
            both : ImputeWithCART
            both : ImputeWithRandomForest
            
            numerical : ImputeWithEquation
            numerical : ImputeWithGBM
            numerical : ImputeWithSVM
            
            categorical : ImputeWithLightGBM
            categorical : ImputeWithCatBoost
            categorical : ImputeWithRandom
            
            addIndicator()
        }
        class Encode{
        <<categorical>>
            OneHotEncode
            LabelEncode
            BinaryEncode
        }
        class Bin{
        <<numerical>>
            BinByPercentile
            BinByInterval
            BinByCount
        }
        class Date{
        <<datetime>>
            ExtractYear
            ExtractFinancialYear
            ExtractQuarter
            ExtractMonth
            ExtractWeek
            CheckIfWeekend
            ComputeTimeDelta
        }
        class Text{
        <<string>>
            CleanText
            TokenizeText
            VectorizeText
        }
        direction TD
        START --> Date
        START --> Encode
        START --> Outliers
        START --> Text
        Outliers --> Scale : <b><u>Scale</b> <i>before</i> <b>Imputing</u></b><br>if imputation method<br>is sensitive to scale of<br>features and/or outliers
        Outliers --> Impute : <b><u>Impute</b> <i>before</i> <b>Scaling</u></b><br>if scaling needs to be<br>applied to all values,<br>including imputed ones
        Encode --> Impute
        Scale --> Bin
        Impute --> Bin
    """

mermaid.st_mermaid(class_diagram, height = "900px")

st.write(Pipeline)
