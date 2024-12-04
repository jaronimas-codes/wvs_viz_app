import pandas as pd

# Load the dataset (replace with the actual file path)
file_path = "data/raw_tax_data.csv"  # Replace with your actual file name
data = pd.read_csv(file_path)

# Ensure column names are consistent
data.columns = data.columns.str.strip()

# Reshape data into a long format for easier processing
year_columns = [col for col in data.columns if col.isdigit()]
melted_data = data.melt(
    id_vars=["Economy ISO3", "Economy Name", "Indicator"],
    value_vars=year_columns,
    var_name="Year",
    value_name="Value"
)

# Ensure numeric types for year and value
melted_data["Year"] = pd.to_numeric(melted_data["Year"], errors="coerce")
melted_data["Value"] = pd.to_numeric(melted_data["Value"], errors="coerce").fillna(0)

# Clean up the Indicator column
melted_data["Indicator"] = melted_data["Indicator"].str.strip().str.lower()

# Define mapping for "Carbon Tax" and "ETS"
indicator_map = {
    "ghg emission coverage": "ETS",
    "prices in implemented carbon initiatives: rate 1 (us $/tco2e)": "Carbon Tax",
    "revenue in implemented carbon pricing initiatives (us $, million)": "Carbon Tax",
}

# Map indicators to simpler labels
melted_data["Indicator Type"] = melted_data["Indicator"].map(indicator_map)

# Identify implementation years
def get_implementation_year(group, indicator_type):
    subset = group[group["Indicator Type"] == indicator_type]
    implemented_years = subset[subset["Value"] > 0]["Year"]
    return implemented_years.min() if not implemented_years.empty else 0

# Group by country and calculate the earliest year for Carbon Tax and ETS
summary_data = (
    melted_data.groupby(["Economy ISO3", "Economy Name"])
    .apply(lambda x: pd.Series({
        "Carbon Tax": get_implementation_year(x, "Carbon Tax"),
        "ETS": get_implementation_year(x, "ETS"),
    }))
    .reset_index()
)

# Rename columns for clarity
summary_data.rename(columns={"Economy ISO3": "ISO3", "Economy Name": "Country"}, inplace=True)

# Save the output
output_file = "tax_summary.csv"
summary_data.to_csv(output_file, index=False)
print(f"Summary data saved to {output_file}")
