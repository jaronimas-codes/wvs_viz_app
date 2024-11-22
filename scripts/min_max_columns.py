import pandas as pd
from variable_mappings_env import variable_mappings  # Ensure this file contains the question mappings

# Load question mappings for all questions
question_options = {list(item.keys())[0]: list(item.values())[0] for item in variable_mappings}

# Load the data
data = pd.read_csv('data/data.csv')  # Updated path to match your specified file location

# Replace invalid values with NaN for existing questions in the dataset and verify numeric columns
valid_columns = {}
for question_code in question_options.keys():
    if question_code in data.columns:
        # Skip all columns that start with "S", "V", "W", "X", "Y", or "M"
        if question_code.startswith(("S", "V", "W", "X", "Y", "M")):
            print(f"Skipping column with prefix 'S', 'V', 'W', 'X', 'Y', or 'M': {question_code}")
            continue

        # Replace invalid values with NaN
        data[question_code] = data[question_code].apply(lambda x: x if x > 0 else pd.NA)

        # Try converting to numeric; handle any exceptions
        try:
            # Convert to numeric
            data[question_code] = pd.to_numeric(data[question_code])

            # Add mean, min, and max aggregations
            valid_columns[question_code] = ['max']
        except (ValueError, TypeError):
            print(f"Skipping problematic column: {question_code}")

# Group by country and wave, calculate mean, min, and max for valid questions
mean_data = data.groupby(['COUNTRY_ALPHA', 'S002VS']).agg(valid_columns)

# Flatten the column names
mean_data.columns = ['_'.join(col).strip() for col in mean_data.columns.values]
mean_data.reset_index(inplace=True)

# Save the mean, min, and max values into a CSV file
mean_data.to_csv('precomputed_max.csv', index=False)

print("Precomputed means, min, and max saved to 'precomputed_means_with_min_max.csv'.")
