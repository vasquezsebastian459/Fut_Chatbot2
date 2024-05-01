import pandas as pd

# Load the CSV file
file_path = 'dataset/all_players_stats.csv'
df = pd.read_csv(file_path)

# Function to replace non-breaking spaces
def replace_nbsp(value):
    if isinstance(value, str):
        return value.replace(u'\u00A0', ' ')
    return value

# Apply the function to clean each column that is of string type
for col in df.columns:
    if df[col].dtype == object:
        df[col] = df[col].apply(replace_nbsp)

# Save the cleaned data back to a CSV
df.to_csv('dataset/all_players_stats2.csv', index=False)
