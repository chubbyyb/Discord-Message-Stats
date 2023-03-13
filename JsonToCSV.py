import pandas as pd
import json

# Load the JSON file
with open(r'data\word_counts.json', 'r') as f:
    data = json.load(f)

# Convert the JSON to a DataFrame
df = pd.DataFrame.from_dict(data, orient='index', columns=['count'])

# Write the DataFrame to a CSV file
df.to_csv(r'data\data.csv')
