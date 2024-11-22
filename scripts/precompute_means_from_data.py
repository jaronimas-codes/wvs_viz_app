import pandas as pd

from variable_mappings_env import variable_mappings  # Ensure this file contains the question mappings

# Load question mappings for all questions
question_options = {list(item.keys())[0]: list(item.values())[0] for item in variable_mappings}

# Load the data
data = pd.read_csv('data/data.csv')  # Updated path to match your specified file location

# Define variables, countries, and waves
env_vars = list(question_options.keys())  # Variables to analyze
unique_countries = data['COUNTRY_ALPHA'].dropna().unique()  # Dynamically determine countries
unique_waves = data['S002VS'].dropna().unique()  # Dynamically determine waves

# Initialize trend data
trend_data_list = []

# Process each variable
for var in env_vars:
    for country in unique_countries:
        for wave in unique_waves:
            # Filter data for the specific variable, country, and wave
            wave_data = data[
                (data['COUNTRY_ALPHA'] == country) & 
                (data['S002VS'] == wave) & 
                (data[var] > 0)  # Filter positive responses
            ]
            
            total_respondents = len(wave_data)
            
            # Skip waves with no respondents
            if total_respondents == 0:
                continue

            # Reverse the scale for the variable if necessary
            transformed_responses = wave_data[var].apply(
                lambda x: 5 - x if pd.notna(x) else pd.NA
            )
            
            # Count favorable responses
            if var == "B008":
                # Special case: Only answers of 4
                favorable_count = transformed_responses[transformed_responses == 4].count()
            else:
                # General case: Include 3 and 4
                favorable_count = transformed_responses[transformed_responses.isin([3, 4])].count()
            
            # Skip if there are no favorable responses
            if favorable_count == 0:
                continue
            
            # Calculate percentage of favorable responses
            percentage_favorable = (favorable_count / total_respondents) * 100  # Convert to percentage
            
            # Add the result to the trend data
            trend_data_list.append({
                "Variable": var,
                "Country": country,
                "Wave": wave,
                "Percentage_Favorable": percentage_favorable
            })

# Convert the list of dictionaries to a DataFrame
trend_data = pd.DataFrame(trend_data_list)

# Pivot the data to have variables as columns
pivoted_data = trend_data.pivot(index=["Country", "Wave"], columns="Variable", values="Percentage_Favorable").reset_index()

# Save the pivoted data to a CSV file
pivoted_data.to_csv('precomputed_data_pivoted.csv', index=False)

print("Pivoted precomputed data saved to 'precomputed_data_pivoted.csv'.")
