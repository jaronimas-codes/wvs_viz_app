import pandas as pd
from variable_mappings import variable_mappings  # Ensure this file contains the question mappings

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
        data[question_code] = data[question_code].apply(lambda x: x if x not in [-5, -4, -2, -1] else pd.NA)

        try:
            # Convert to numeric
            data[question_code] = pd.to_numeric(data[question_code], errors='coerce')

            # Determine transformation based on max value in the column
            max_value = data[question_code].max()
            if max_value == 4:
                # Reverse the scale for columns with a max value of 4
                data[question_code] = data[question_code].apply(lambda x: 5 - x if pd.notna(x) else pd.NA)

            # Add column to the valid columns dictionary for aggregation
            valid_columns[question_code] = 'mean'

        except (ValueError, TypeError):
            print(f"Skipping problematic column: {question_code}")

# Group by country and wave, calculate mean for valid questions
mean_data = data.groupby(['COUNTRY_ALPHA', 'S002VS']).agg(valid_columns).reset_index()

# Save the mean values into a CSV file
mean_data.to_csv('precomputed_means.csv', index=False)

print("Precomputed means saved to 'precomputed_means.csv'.")
