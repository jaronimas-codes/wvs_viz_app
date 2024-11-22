import pandas as pd

# Load the Excel file
file_path = 'data/vars.xlsx'
excel_data = pd.ExcelFile(file_path)

# Load the first sheet of the Excel file
data = pd.read_excel(file_path, sheet_name='Hoja1')

# Create a raw dictionary for variable mappings
variable_mappings = [
    {row['Variable']: row['Title']} for _, row in data.iterrows()
]

# Example usage of the variable mappings
for mapping in variable_mappings:
    print(f'{mapping},')  # Print the first 5 mappings for illustration