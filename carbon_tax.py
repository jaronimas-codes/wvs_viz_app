import pandas as pd

# Create the dataset
data = [
    {"ISO3": "ARG", "Country": "Argentina", "Carbon Tax": 2018, "ETS": 0},
    {"ISO3": "AUS", "Country": "Australia", "Carbon Tax": 0, "ETS": 2012},
    {"ISO3": "AUT", "Country": "Austria", "Carbon Tax": 0, "ETS": 2023},
    {"ISO3": "CAN", "Country": "Canada", "Carbon Tax": 2019, "ETS": 2018},
    {"ISO3": "CHE", "Country": "Switzerland", "Carbon Tax": 2008, "ETS": 2008},
    {"ISO3": "CHL", "Country": "Chile", "Carbon Tax": 2017, "ETS": 0},
    {"ISO3": "CHN", "Country": "China", "Carbon Tax": 0, "ETS": 2017},
    {"ISO3": "COL", "Country": "Colombia", "Carbon Tax": 2018, "ETS": 0},
    {"ISO3": "DEU", "Country": "Germany", "Carbon Tax": 0, "ETS": 2021},
    {"ISO3": "DNK", "Country": "Denmark", "Carbon Tax": 1992, "ETS": 0},
    {"ISO3": "ESP", "Country": "Spain", "Carbon Tax": 2014, "ETS": 0},
    {"ISO3": "FIN", "Country": "Finland", "Carbon Tax": 1990, "ETS": 0},
    {"ISO3": "FRA", "Country": "France", "Carbon Tax": 2014, "ETS": 0},
    {"ISO3": "GBR", "Country": "United Kingdom", "Carbon Tax": 0, "ETS": 2021},
    {"ISO3": "IDN", "Country": "Indonesia", "Carbon Tax": 0, "ETS": 2022},
    {"ISO3": "IRL", "Country": "Ireland", "Carbon Tax": 2010, "ETS": 0},
    {"ISO3": "ISL", "Country": "Iceland", "Carbon Tax": 2010, "ETS": 0},
    {"ISO3": "JPN", "Country": "Japan", "Carbon Tax": 2012, "ETS": 0},
    {"ISO3": "KAZ", "Country": "Kazakhstan", "Carbon Tax": 0, "ETS": 2013},
    {"ISO3": "KOR", "Country": "Korea, Rep.", "Carbon Tax": 0, "ETS": 2015},
    {"ISO3": "LUX", "Country": "Luxembourg", "Carbon Tax": 2021, "ETS": 0},
    {"ISO3": "MEX", "Country": "Mexico", "Carbon Tax": 2014, "ETS": 0},
    {"ISO3": "NLD", "Country": "Netherlands", "Carbon Tax": 2021, "ETS": 0},
    {"ISO3": "NOR", "Country": "Norway", "Carbon Tax": 1991, "ETS": 0},
    {"ISO3": "NZL", "Country": "New Zealand", "Carbon Tax": 0, "ETS": 2008},
    {"ISO3": "POL", "Country": "Poland", "Carbon Tax": 1990, "ETS": 0},
    {"ISO3": "PRT", "Country": "Portugal", "Carbon Tax": 2015, "ETS": 0},
    {"ISO3": "SGP", "Country": "Singapore", "Carbon Tax": 2019, "ETS": 0},
    {"ISO3": "SVN", "Country": "Slovenia", "Carbon Tax": 1996, "ETS": 0},
    {"ISO3": "SWE", "Country": "Sweden", "Carbon Tax": 1991, "ETS": 0},
    {"ISO3": "UKR", "Country": "Ukraine", "Carbon Tax": 2011, "ETS": 0},
    {"ISO3": "ZAF", "Country": "South Africa", "Carbon Tax": 2019, "ETS": 0},
]



# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV
file_path = 'carbon_pricing.csv'
df.to_csv(file_path, index=False)
