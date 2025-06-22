import pandas as pd

# Load the CSV files
df_obesity = pd.read_csv("obesity_data.csv")
df_malnutrition = pd.read_csv("malnutrition_data.csv")

# Define relevant columns
keep_columns = ['IndicatorCode', 'SpatialDim', 'ParentLocation', 'TimeDim', 'Dim1', 'NumericValue', 'age_group']

# Clean obesity dataset
df_obesity_clean = df_obesity[keep_columns].copy()
df_obesity_clean.rename(columns={
    'IndicatorCode': 'indicator',
    'SpatialDim': 'country',
    'ParentLocation': 'region',
    'TimeDim': 'year',
    'Dim1': 'sex',
    'NumericValue': 'value'
}, inplace=True)

# Clean malnutrition dataset
df_malnutrition_clean = df_malnutrition[keep_columns].copy()
df_malnutrition_clean.rename(columns={
    'IndicatorCode': 'indicator',
    'SpatialDim': 'country',
    'ParentLocation': 'region',
    'TimeDim': 'year',
    'Dim1': 'sex',
    'NumericValue': 'value'
}, inplace=True)

# Preview cleaned obesity data
print(df_obesity_clean.head())
