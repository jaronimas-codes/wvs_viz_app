import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image
from mappings.country_mapping import country_info
from mappings.variable_mappings_env import variable_mappings  # Ensure this file contains the question mappings

# Custom CSS to style the app with a unified environmental theme
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
            color: #1b5e20; /* Dark green for headers */
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

        /* Buttons and Selection Boxes */
        # .st-dq, .st-dr {
        #     background-color: #66bb6a !important; /* Green buttons */
        #     color: white !important;
        # }

        /* Citations Section */
        .citation-section {
            border-left: 5px solid #388e3c;
            background-color: #f1f8e9; /* Soft green */
            padding: 1rem;
            margin: 1rem 0;
        }

        /* Table Styles */
        .dataframe {
            border: 1px solid #388e3c;
            border-radius: 5px;
            overflow: hidden;
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
    return pd.read_csv('precalculated_data/precomputed_env_data.csv')

@st.cache_data
def load_precomputed_age_data():
    return pd.read_csv('precalculated_data/precomputed_age_data.csv')

@st.cache_data
def load_co2_data():
    return pd.read_csv('precalculated_data/co2-data.csv')

@st.cache_data
def load_tax_data():
    return pd.read_csv('precalculated_data/tax_summary.csv')

# Load the EPI data (replace 'ep.csv' with the correct file path)
@st.cache_data
def load_epi_data():
    return pd.read_csv('precalculated_data/epi.csv', delimiter=';')

# Load data
env_data = load_precomputed_env_data()
age_data = load_precomputed_age_data()
co2_data = load_co2_data()
tax_data = load_tax_data()
epi_data = load_epi_data()

# Country mapping
country_mapping = {info["country_3"]: info["country_name"] for info in country_info}

custom_green_scale = [
    "#99cc99",  # Soft, muted light green
    "#33cc33",  # Bright green
    "#00b359",  # Rich green
    "#009933",  # Medium green
    "#008000",  # Medium-dark green
    "#006600",  # Dark green
    "#004d00",  # Very dark green
    "#003300"   # Very dark green (almost black)
]

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
    "Select countries",
    options=all_countries_names,
    default=default_countries_names,
    key="country_selection"
)

selected_countries_3 = [k for k, v in country_mapping.items() if v in selected_countries_names]

# Wave selection
all_waves = sorted(env_data['Wave'].unique())

selected_waves = st.multiselect(
    "Select survey waves. (2: 1990-1994, 3: 1995-1999, 4: 2000-2004, 5: 2005-2009, 6: 2010-2014, 7: 2017-2022 )",
    options=all_waves,
    default=all_waves,
    key="wave_selection"
)

# Question selection
if question_options:
    selected_question_key = st.selectbox(
        "Select a question to visualize", 
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
            # title=f'% of Agree and Strongly Agree to "{selected_question_label}" ',
            # color_discrete_sequence=custom_green_scale
            color_discrete_sequence=px.colors.sequential.Viridis
        )
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
            color_continuous_scale=custom_green_scale,
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
        labels={'year': 'Year', 
                'co2_per_capita': 'CO₂ Emissions Per Capita (Metric Tons)'
                },
        # title="CO₂ Emissions Per Capita Trends (1981–2023)",
        color_discrete_sequence=custom_green_scale
    )
    # Update the layout to set the legend title
    fig.update_layout(legend_title_text='Country')
    st.plotly_chart(fig, use_container_width=True)



st.markdown("<hr>", unsafe_allow_html=True)


# Step 4: Carbon Pricing Map
st.markdown("""
### Step 4: Carbon Pricing Instruments Map
This map shows the implementation of Carbon Pricing Instruments (Carbon Tax and Emission Trading Systems - ETS) around the world.
""")


# Prepare data for visualization
tax_data['Instrument_Type'] = tax_data.apply(
    lambda row: "Both" if row['Carbon Tax'] > 0 and row['ETS'] > 0 
    else "Carbon Tax" if row['Carbon Tax'] > 0 
    else "ETS" if row['ETS'] > 0 
    else "None", 
    axis=1
)

# Map instruments to colors
instrument_color_map = {
    "None": "#ff0000",  # Strong red for None
    "Carbon Tax": "#66bb6a",  # Light green for Carbon Tax
    "ETS": "#006400",  # Dark green for ETS
    "Both": "#003300",  # Very dark green for Both
}

# Create the map using Plotly
fig_map = px.choropleth(
    tax_data,
    locations="ISO3",  # Country ISO3 codes
    color="Instrument_Type",  # Color by instrument type
    hover_name="Country",  # Display country name on hover
    hover_data={"Carbon Tax": True, "ETS": True, "Instrument_Type": False},
    title=" ",
    color_discrete_map=instrument_color_map,
    projection="natural earth"  # Use a modern map projection
)

# Customize the layout for a clean design
fig_map.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_scale=1.2,  # Adjust map zoom level
        center={"lat": 10, "lon": 0}  # Center the map
    ),
    margin=dict(t=50, b=50, l=50, r=50),
    title=dict(
        font=dict(size=24, color="#2e7d32"),
        x=0.5  # Center the title
    ),
    height=500,
    width=1200
)

# Display the map in Streamlit
st.plotly_chart(fig_map, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Step 5: Environmental Performance Index (EPI)
st.markdown("""
### Step 5: 🌿 Environmental Performance Index (EPI)

The Environmental Performance Index (EPI) ranks countries on their environmental health and ecosystem vitality.
""")

# Filter the data for default countries and only for the year 2024
filtered_epi_data = epi_data[
    (epi_data['region'].isin(default_countries_names)) & 
    (epi_data['date'] == 2024)
]

# Add arrow indicators to the trend column
filtered_epi_data['trend_arrow'] = filtered_epi_data['trend'].apply(
    lambda x: "↑" if x > 0 else "↓" if x < 0 else "→"
)

# Combine trend and arrow into a single column for display
filtered_epi_data['trend_display'] = filtered_epi_data.apply(
    lambda row: f"{row['trend_arrow']} {abs(row['trend']):.1f}", axis=1
)

# Sort the data by value
sorted_epi_data = filtered_epi_data.sort_values(by='value', ascending=True)

# Create the barplot
fig_epi_combined = px.bar(
    sorted_epi_data,
    y='region',
    x='value',
    orientation='h',
    text='value',
    color='value',
    color_continuous_scale=custom_green_scale,
    labels={
        'value': 'Environmental Performance Index (EPI)', 
        'region': 'Country',
        'trend_display': 'Trend'
    },
    # title="Environmental Performance Index (EPI) for Selected Countries (2024)"
)

# Add EPI and trend data to the bar labels
fig_epi_combined.update_traces(
    texttemplate='EPI: %{x:.1f} Trend: %{customdata[0]}',  # Position text next to each other
    customdata=sorted_epi_data[['trend_display']].to_numpy(),  # Pass trend_display column as customdata
    textposition='inside',
    textfont=dict(size=18)  # Make text larger
)

# Customize the chart
fig_epi_combined.update_layout(
    yaxis=dict(title="Country"),
    xaxis=dict(title="EPI Score"),
    margin=dict(t=50, b=50, l=100, r=50),
    coloraxis_showscale=False  # Hide the color scale
)

# Display the chart in Streamlit
st.plotly_chart(fig_epi_combined, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)


# Step 6: Your Action Plan
st.markdown("""
### Step 6: 🌱 Your Action Plan

The path to a sustainable future begins with **awareness** and **action**. Here are some steps you can take:

- 🌍 **Understand the Data**: Compare your country's performance on environmental indicators, such as the Environmental Performance Index (EPI), to identify areas for improvement.
- 📢 **Spread Awareness**: Share the insights from this data with your community, peers, or policymakers. Social platforms and discussions can amplify your voice.
- 🌱 **Take Personal Action**: Reflect on steps you can take to reduce your own carbon footprint, such as:
  - Using energy-efficient appliances and renewable energy sources.
  - Reducing, reusing, and recycling waste.
  - Supporting sustainable businesses and initiatives.

💡 **Remember**: Small, consistent actions can lead to significant change when adopted collectively.

Every action matters. Together, we can make a difference. 🌿
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
        <li><strong>Carbon pricing instruments around the world, 2024:</strong> 
        Data from <a href="https://carbonpricingdashboard.worldbank.org/" target="_blank">World Bank Carbon Pricing Dashboard</a>.</li>
        <li><strong>The Environmental Performance Index (EPI):</strong> 
        Data from <a href="https://global-reports.23degrees.eu/epi/root" target="_blank">23 Degrees Environmental Performance Index Report</a>.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("""
**Author:**  
Jaronimas Snipas  
[GitHub](https://github.com/jaronimas-codes) | 
[LinkedIn](https://www.linkedin.com/in/jaronimas-snipas/)
""")
