import streamlit as st
import streamlit_mermaid as mermaid


class_diagram = """
    classDiagram
        class _{
            DropColumns
            DropRows
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
        class Recode{
        <<categorical>>
            OneHotEncode
            LabelEncode
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
        }
        direction TD
        _ --> Date
        _ --> Recode
        _ --> Outliers
        Outliers --> Scale : 1
        Outliers --> Impute : 2
        Recode --> Impute
        Scale --> Bin
        Impute --> Bin
    """

mermaid.st_mermaid(class_diagram, height = "1000px")

st.write("(1) **Scale** before **Impute**\n\
            if imputation method is sensitive to scale of features and/or outliers")
st.write("(2) **Impute** before **Scale**\n\
            if scaling needs to be applied to all values, including imputed ones")
