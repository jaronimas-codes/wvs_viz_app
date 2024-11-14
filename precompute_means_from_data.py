import pandas as pd
from variable_mappings import variable_mappings  # Ensure this file contains the question mappings

# Load question mappings for the first 10 questions
question_options = {list(item.keys())[0]: list(item.values())[0] for item in variable_mappings}

# Load the data
data = pd.read_csv('data/data.csv')  # Updated path to match your specified file location

# Replace invalid values with NaN for existing questions in the dataset and verify numeric columns
valid_columns = {}
for question_code in question_options.keys():
    if question_code in data.columns:
        # Skip all columns that start with "S", "V", "W", "X", or "Y"
        if question_code.startswith(("S", "V", "W", "X", "Y")):
            print(f"Skipping column with prefix 'S', 'V', 'W', 'X', or 'Y': {question_code}")
            continue

        # Replace invalid values with NaN
        data[question_code] = data[question_code].apply(lambda x: x if x not in [-5, -4, -2, -1] else pd.NA)
        
        # Try converting to numeric; if fails, skip the column
        try:
            data[question_code] = pd.to_numeric(data[question_code])
            valid_columns[question_code] = 'mean'  # Include only numeric columns
        except ValueError:
            print(f"Skipping non-numeric column: {question_code}")

# Group by country and wave, calculate mean for valid questions
mean_data = data.groupby(['COUNTRY_ALPHA', 'S002VS']).agg(valid_columns).reset_index()

# Save the mean values into a CSV file
mean_data.to_csv('precomputed_means.csv', index=False)
