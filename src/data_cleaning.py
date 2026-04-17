import pandas as pd
import numpy as np

def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Removes exact duplicates and drops rows with missing values."""
    df = df.drop_duplicates()
    df = df.dropna()
    return df

def remove_outliers_iqr(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Removes outliers from a specific column based on the Interquartile Range (IQR) method."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Keep only rows within the IQR bounds
    filtered_df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    return filtered_df.copy()