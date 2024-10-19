import pandas as pd

# Load both datasets
nutrient_data = pd.read_csv('/mnt/data/nutrients_csvfile.csv')
emoji_data = pd.read_csv('/mnt/data/Emoji Diet Nutritional Data (g) - EmojiFoods (g).csv')

# View column names and first few rows of each dataset
print(nutrient_data.columns)
print(emoji_data.columns)

print(nutrient_data.head())
print(emoji_data.head())

