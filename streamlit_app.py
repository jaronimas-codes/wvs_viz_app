import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image
from country_mapping import country_info
from variable_mappings_env import variable_mappings  # Ensure this file contains the question mappings
import pycountry

# Custom CSS to style the app with an environmental theme
st.markdown(
    """
    <style>
        /* General App Styles */
        .stApp {
            background-color: #e8f5e9; /* Light green background */
        }
        .block-container {
            max-width: 65rem; /* Adjust width */
            padding: 2rem 2rem; /* Add padding */
        }

        /* Headers and Titles */
        h1, h2, h3, h4, h5, h6 {
            color: #2e7d32; /* Dark green for headers */
            font-family: 'Arial', sans-serif;
        }

        /* Section Dividers */
        hr {
            border: 1px solid #388e3c; /* Green divider lines */
        }

        /* Buttons and Selection Boxes */
        .st-bn {
            background-color: #66bb6a !important; /* Green buttons */
            color: white !important;
        }

        /* Citations Section */
        .citation-section {
            border-left: 5px solid #388e3c;
            background-color: #f1f8e9; /* Soft green */
            padding: 1rem;
            margin: 1rem 0;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Add a custom header image
image_path = "img/no_planet_b.jpg"  # Replace with a relevant environmental image
image = Image.open(image_path)

st.image(image, 
        caption="No Planet B, Photo by [Markus Spiske](https://www.pexels.com/photo/climate-road-landscape-people-2990650/)",
        use_container_width=True)

# Title
st.title("🌱 Youth, Environment, and Action: Insights from Global Data")

# Divider
st.markdown("<hr>", unsafe_allow_html=True)

# Load the precomputed data with caching
@st.cache_data
def load_precomputed_env_data():
    return pd.read_csv('precomputed_env_data.csv')

@st.cache_data
def load_precomputed_age_data():
    return pd.read_csv('precomputed_age_data.csv')

@st.cache_data
def load_co2_data():
    return pd.read_csv('co2-data.csv')

@st.cache_data
def load_tax_data():
    return pd.read_csv('tax_summary.csv')

# Load data
env_data = load_precomputed_env_data()
age_data = load_precomputed_age_data()
co2_data = load_co2_data()
tax_data = load_tax_data()

# Country mapping
country_mapping = {info["country_3"]: info["country_name"] for info in country_info}

# Filter variable_mappings to include only questions present in env_data columns
question_options = {
    item_code: item_label
    for item in variable_mappings
    for item_code, item_label in item.items()
    if item_code in env_data.columns
}

# Step 1: World Values Survey
st.markdown("""
### Step 1: 🌎 Explore World Trends
Dive into the World Values Survey to understand global perspectives on environmental issues.
""")

# Country selection
all_countries_codes = env_data['Country'].unique()

all_countries_names = [country_mapping.get(c3, c3) for c3 in all_countries_codes]
default_countries_codes = ['AUS', 'CAN', 'CHN', 'RUS', 'DEU', 'CHE', 'USA']
default_countries_names = [country_mapping.get(c3, c3) for c3 in default_countries_codes]

selected_countries_names = st.multiselect(
    "Choose countries",
    options=all_countries_names,
    default=default_countries_names,
    key="country_selection"
)

selected_countries_3 = [k for k, v in country_mapping.items() if v in selected_countries_names]

# Wave selection
all_waves = sorted(env_data['Wave'].unique())

selected_waves = st.multiselect(
    "Choose survey waves. (2: 1990-1994, 3: 1995-1999, 4: 2000-2004, 5: 2005-2009, 6: 2010-2014, 7: 2017-2022 )",
    options=all_waves,
    default=all_waves,
    key="wave_selection"
)

# Question selection
if question_options:
    selected_question_key = st.selectbox(
        "Choose a question to visualize", 
        options=list(question_options.keys()), 
        format_func=lambda x: question_options[x],
        index=3,
        key="question_selection"
    )
    selected_question_label = question_options[selected_question_key]

    filtered_data = env_data[
        (env_data['Country'].isin(selected_countries_3)) & 
        (env_data['Wave'].isin(selected_waves))
    ][['Country', 'Wave', selected_question_key]].rename(columns={selected_question_key: 'mean_response'})

    if not filtered_data.empty:
        fig = px.line(
            filtered_data,
            x='Wave',
            y='mean_response',
            color='Country',
            markers=True,
            labels={'Wave': 'Survey Wave', 'mean_response': f''},
            title=f'% of Agree and Strongly Agree to "{selected_question_label}" ',
            color_discrete_sequence=px.colors.sequential.Blues
        )
        # fig.update_layout(
        #     title={'text': f'% of Agree and Strongly Agree to "{selected_question_label}" ', 'x': 0.5}
        # )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write(f"No data available for the selected question '{selected_question_label}' with the chosen countries and waves.")
else:
    st.write("No available questions found in the precomputed data.")

st.markdown("<hr>", unsafe_allow_html=True)

# Step 2: Youth Responses
st.markdown("""
### Step 2: Youth Responses
This section shows the percentage of youth (under 29 years old) who agreed or strongly agreed with the selected question for a single wave.
""")
selected_wave_single = st.selectbox(
    "Select a Survey Wave (Only One)", 
    options=sorted(age_data['Wave'].unique()), 
    index=3,
    key="wave_single_selection"
)

reverse_country_mapping = {v: k for k, v in country_mapping.items()}
selected_countries_3 = [reverse_country_mapping.get(country, country) for country in selected_countries_names]

if selected_question_key in age_data.columns:
    filtered_age_data = age_data[
        (age_data['Wave'] == selected_wave_single) & (age_data['Country'].isin(selected_countries_3))
    ][['Country', selected_question_key]].rename(columns={selected_question_key: 'Percentage_Favorable'})

    if not filtered_age_data.empty:
        filtered_age_data = filtered_age_data.sort_values(by='Percentage_Favorable', ascending=False)
        fig = px.bar(
            filtered_age_data,
            x='Country',
            y='Percentage_Favorable',
            text='Percentage_Favorable',
            color='Percentage_Favorable',
            color_continuous_scale='greens',
            labels={'Percentage_Favorable': 'Percentage Favorable (%)'}
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write(f"No data available for '{selected_question_label}' with the chosen countries and wave.")

st.markdown("<hr>", unsafe_allow_html=True)

# Step 3: CO₂ Emissions Trends
st.markdown("""
### Step 3: 🌍 CO₂ Emissions Per Capita Trends
Compare the historical CO₂ emissions per capita (1981–2023) for the selected countries to understand their environmental impact.
""")

selected_countries_alpha = [reverse_country_mapping.get(country, country) for country in selected_countries_names]
filtered_co2_data = co2_data[
    (co2_data['iso_code'].isin(selected_countries_alpha)) & 
    (co2_data['year'].between(1981, 2023))
]

if not filtered_co2_data.empty:
    fig = px.line(
        filtered_co2_data,
        x='year',
        y='co2_per_capita',
        color='iso_code',
        labels={'year': 'Year', 'co2_per_capita': 'CO₂ Emissions Per Capita (Metric Tons)'},
        title="CO₂ Emissions Per Capita Trends (1981–2023)",
        color_discrete_sequence=px.colors.sequential.PuBu
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Step 4: Carbon Pricing Map
st.markdown("""
### Step 4: Carbon Pricing Instruments Map
This map shows the implementation of Carbon Pricing Instruments (Carbon Tax and Emission Trading Systems - ETS) around the world.
""")

iso3_codes = [country.alpha_3 for country in pycountry.countries]
all_countries = pd.DataFrame(iso3_codes, columns=["ISO3"])
all_countries["Instrument"] = "None"

def classify_instrument(row):
    if row["Carbon Tax"] > 0 and row["ETS"] > 0:
        return "Both"
    elif row["Carbon Tax"] > 0:
        return "Carbon Tax"
    elif row["ETS"] > 0:
        return "ETS"
    else:
        return "None"
    
# Classify instruments in the tax_data
tax_data["Instrument"] = tax_data.apply(classify_instrument, axis=1)

# Merge tax data with all countries
merged_data = pd.merge(all_countries, tax_data, on="ISO3", how="left")

# Fill missing values for classification and country names
merged_data["Instrument"] = merged_data["Instrument_y"].combine_first(merged_data["Instrument_x"])
merged_data["Country"] = merged_data["Country"].fillna("Unknown")
merged_data["Carbon Tax"] = merged_data["Carbon Tax"].fillna(0).astype(int)
merged_data["ETS"] = merged_data["ETS"].fillna(0).astype(int)

# Create a choropleth map
fig = px.choropleth(
    merged_data,
    locations="ISO3",
    color="Instrument",
    hover_name="Country",
    hover_data={
        "Carbon Tax": True,
        "ETS": True,
        "Instrument": False,
    },
    title="🌍 Carbon Pricing Instruments Around the World, 2024",
    color_discrete_map={
        "None": "#e0e0e0",  # Light gray
        "Carbon Tax": "#66bb6a",  # Green
        "ETS": "#42a5f5",  # Blue
        "Both": "#8e24aa",  # Purple
    }
)

# Customize the map layout
fig.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type="equirectangular",
        projection_scale=1.4,
        center={"lat": 20, "lon": 0},
    ),
    height=800,
    width=1200,
    title_x=0.5,
)

# Display the map
st.plotly_chart(fig, use_container_width=False)

# Step 5: Your Action Plan
st.markdown("""
### Step 5: 🌱 Your Action Plan

The journey to a sustainable planet doesn't stop here. It's time to act!

- Compare your country's carbon pricing initiatives to others.
- Share insights with peers, policymakers, and on social platforms.
- Reflect on steps you can take to reduce your carbon footprint.

Every action counts. 🌍 Be the change you wish to see in the world!
""")

# Add a section for data sources and author information
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div class="citation-section">
    <strong>Data Sources:</strong><br>
    <ul>
        <li><strong>WVS Time-Series (1981–2022):</strong> Inglehart, R., et al. (2022). 
        <i>World Values Survey: All Rounds – Country-Pooled Datafile Version 3.0</i>. 
        Madrid, Spain & Vienna, Austria: JD Systems Institute & WVSA Secretariat. 
        <a href="https://www.worldvaluessurvey.org/WVSDocumentationWVL.jsp" target="_blank">Documentation</a></li>
        <li><strong>CO₂ and Greenhouse Gas Emissions:</strong> 
        Data from <a href="https://ourworldindata.org/co2-and-greenhouse-gas-emissions" target="_blank">Our World in Data</a>.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("""
**Author:**  
Jaronimas Snipas  
[GitHub](https://github.com/jaronimas-codes) | 
[LinkedIn](https://www.linkedin.com/in/jaronimas-snipas/)
""")
