import pandas as pd
from variable_mappings_env import variable_mappings  # Ensure this file contains the question mappings

# Load question mappings for all questions
question_options = {list(item.keys())[0]: list(item.values())[0] for item in variable_mappings}

# Load the data
data = pd.read_csv('data/data.csv')  # Update the path to match your specified file location

# Define variables, countries, and waves
env_vars = list(question_options.keys())  # Variables to analyze
unique_countries = data['COUNTRY_ALPHA'].dropna().unique()  # Dynamically determine countries
unique_waves = data['S002VS'].dropna().unique()  # Dynamically determine waves

# Age group to filter
age_group = 1  # Under 29

# Initialize the results
trend_data_list = []

# Process each variable
for var in env_vars:
    for country in unique_countries:
        for wave in unique_waves:
            # Filter data for the specific variable, country, and wave
            wave_data = data[
                (data['COUNTRY_ALPHA'] == country) &
                (data['S002VS'] == wave) &
                (data[var] > 0) &  # Filter positive responses
                (data['X003R2'] == age_group)  # Only "Under 29"
            ].copy()  # Use .copy() to avoid SettingWithCopyWarning
            
            total_respondents = len(wave_data)
            
            # Skip if there are no respondents
            if total_respondents == 0:
                continue

            # Reverse the scale for the variable if necessary
            wave_data['Transformed_Response'] = wave_data[var].apply(
                lambda x: 5 - x if pd.notna(x) else pd.NA
            )
            
            # Count favorable responses
            favorable_count = (
                (wave_data['Transformed_Response'] == 4).sum() 
                if var == "B008" else 
                (wave_data['Transformed_Response'].isin([3, 4])).sum()
            )

            # Calculate percentage favorable
            percentage_favorable = (favorable_count / total_respondents) * 100
            
            # Add the result to the trend data
            trend_data_list.append({
                "Country": country,
                "Wave": wave,
                "Variable": var,
                "Percentage_Favorable": percentage_favorable
            })

# Convert the results to a DataFrame
trend_data = pd.DataFrame(trend_data_list)

# Pivot the data to have variables as columns, keeping the original column names
pivoted_data = trend_data.pivot(
    index=["Country", "Wave"], 
    columns="Variable", 
    values="Percentage_Favorable"
).reset_index()

# Save the processed data to a CSV file
pivoted_data.to_csv('precomputed_age_data.csv', index=False)

print("Precomputed data saved to 'precomputed_age_data.csv'.")
