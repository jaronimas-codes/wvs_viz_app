import pandas as pd
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
from country_mapping import country_info
from variable_mappings_env import variable_mappings  # Ensure this file contains the question mappings
import plotly.graph_objects as go

# Custom CSS to change the max-width of the block container
st.markdown(
    """
    <style>
        .stMainBlockContainer.block-container {
            max-width: 65rem;
        }
        .st-bn {
        background-color: rgb(105,105,105);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load the image
image_path = "img/no_planet_b.jpg"  # Update this path to your local image path
image = Image.open(image_path)

# Crop the image to create a cover-photo-like aspect ratio
width, height = image.size
image = image.crop((0, height * 0.25, width, height * 0.9))

# Display the image at the top
st.image(image, caption="No Planet B, Photo by Markus Spiske: https://www.pexels.com/photo/climate-road-landscape-people-2990650/", use_container_width=True)

# Cached function to load the precomputed data
@st.cache_data
def load_precomputed_env_data():
    return pd.read_csv('precomputed_env_data.csv')

@st.cache_data
def load_precomputed_age_data():
    return pd.read_csv('precomputed_age_data.csv')

@st.cache_data
def load_co2_data():
    return pd.read_csv('co2-data.csv')

# Load the precomputed data
env_data = load_precomputed_env_data()
age_data = load_precomputed_age_data()
co2_data = load_co2_data()

# Prepare country mapping
country_mapping = {info["country_3"]: info["country_name"] for info in country_info}

# Filter variable_mappings to include only questions present in env_data columns
question_options = {
    item_code: item_label
    for item in variable_mappings
    for item_code, item_label in item.items()
    if item_code in env_data.columns
}

# Title
st.title("Does Your Country's Politicians Listen to the Youth Voice?")

# Step 1: World Values Survey
st.markdown("""
### Step 1: Explore the World Values Survey (WVS)
The World Values Survey (WVS) is a global research project that explores people's values and beliefs. Choose a country, survey wave, and environmental question to see what people think about environmental issues.
""")

# Country Selection
all_countries_codes = env_data['Country'].unique()
all_countries_names = [country_mapping.get(c3, c3) for c3 in all_countries_codes]  # Map to full names
default_countries_codes = ['AUS', 'CAN', 'CHN', 'RUS', 'DEU', 'CHE', 'USA']
default_countries_names = [country_mapping.get(c3, c3) for c3 in default_countries_codes]

# Allow selection using full country names
selected_countries_names = st.multiselect(
    "Choose countries",
    options=all_countries_names,
    default=default_countries_names,
    key="country_selection"
)

# Map back to 3-letter codes for filtering
selected_countries_3 = [k for k, v in country_mapping.items() if v in selected_countries_names]

# Wave Selection
all_waves = sorted(env_data['Wave'].unique())
selected_waves = st.multiselect(
    "Choose survey waves. ( 2: 1990-1994, 3: 1995-1999, 4: 2000-2004, 5: 2005-2009, 6: 2010-2014, 7: 2017-2022 )",
    options=all_waves,
    default=all_waves,
    key="wave_selection"
)

# Question Selection
if question_options:
    selected_question_key = st.selectbox(
        "Choose a question to visualize", 
        options=list(question_options.keys()), 
        format_func=lambda x: question_options[x],
        index=3,
        key="question_selection"
    )
    selected_question_label = question_options[selected_question_key]

    # Filter data based on selections
    filtered_data = env_data[
        (env_data['Country'].isin(selected_countries_3)) & 
        (env_data['Wave'].isin(selected_waves))
    ][['Country', 'Wave', selected_question_key]].rename(columns={selected_question_key: 'mean_response'})

    # Plot visualization
    if not filtered_data.empty:
        fig = px.line(
            filtered_data,
            x='Wave',
            y='mean_response',
            color='Country',
            markers=True,
            labels={'Wave': 'Survey Wave', 'mean_response': f''},
            title=f'% of Agree and Strongly Agree to "{selected_question_label}" '
        )
        
        # Center the title
        fig.update_layout(
            title={
                'text': f'% of Agree and Strongly Agree to "{selected_question_label}" ',
                'y': 0.9,  # Adjust the vertical position of the title
                'x': 0.5,  # Center horizontally
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write(f"No data available for the selected question '{selected_question_label}' with the chosen countries and waves.")
else:
    st.write("No available questions found in the precomputed data. Please check the 'precomputed_env_data.csv' file.")
    
    

# Add a citation for the data source
st.markdown("""---""")




# Step 2: Youth Responses
st.markdown("""
### Step 2: Youth Responses
This section shows the percentage of youth (under 29 years old) who agreed or strongly agreed with the selected question for a single wave.
""")

selected_countries_names_step_2 = st.multiselect(
    "Choose countries",
    options=all_countries_names,
    default=default_countries_names,
    key="country_selection_step_2"
)

# Allow user to select only one wave
selected_wave_single = st.selectbox(
    "Select a Survey Wave (Only One)", 
    options=sorted(age_data['Wave'].unique()), 
    index=3,  # Default to the first wave
    key="wave_single_selection"
)

# Map full country names to country codes
reverse_country_mapping = {v: k for k, v in country_mapping.items()}  # Reverse the mapping for lookup
selected_countries_3 = [reverse_country_mapping.get(country, country) for country in selected_countries_names_step_2]

# Filter precomputed age data for youth responses, selected countries, and the same selected question
if question_options:
    selected_question_label = question_options[selected_question_key]

    # Filter data
    filtered_age_data = age_data[
        (age_data['Wave'] == selected_wave_single) & 
        (age_data['Country'].isin(selected_countries_3)) &  # Use mapped country codes
        (age_data['Variable'] == selected_question_key) & 
        (age_data['Age_Group'] == 'Under 29')  # Youth filter
    ]

    if filtered_age_data.empty:
        st.write(f"No data available for '{selected_question_label}' with the chosen countries and wave.")
    else:
        # Sort data by Percentage_Favorable in descending order
        filtered_age_data = filtered_age_data.sort_values(by='Percentage_Favorable', ascending=False)

        # Create bar chart
        fig = px.bar(
            filtered_age_data,
            x='Country',
            y='Percentage_Favorable',
            text='Percentage_Favorable',
            labels={
                'Country': 'Country',
                'Percentage_Favorable': 'Percentage Favorable (%)'
            },
            title=f"Youth Favorable Responses to '{selected_question_label}' (Wave {selected_wave_single})",
            color='Percentage_Favorable',
            color_continuous_scale='greens'
        )

        # Customize layout
        fig.update_traces(
            texttemplate='%{text:.1f}%',
            textposition='outside'
        )
        fig.update_layout(
            xaxis_title="Country",
            yaxis_title="Percentage Favorable (%)",
            margin=dict(t=50, b=50, l=25, r=25),
            coloraxis_showscale=False  # Hide color scale bar
        )

        # Display the bar chart
        st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No available questions found in the precomputed data.")

    
    

# Add a citation for the data source
st.markdown("""---""")








# Step 3: CO₂ Emissions Trends
st.markdown("""
### Step 3: CO₂ Emissions Per Capita Trends
Compare the historical CO₂ emissions per capita (1981–2023) for the selected countries to understand their environmental impact.
""")

# Define the year range
year_range = range(1981, 2024)

# Map selected countries to their alpha-3 ISO codes
reverse_country_mapping = {v: k for k, v in country_mapping.items()}  # Reverse mapping for country codes
selected_countries_alpha = [reverse_country_mapping.get(country, country) for country in selected_countries_names]

# Filter CO2 data for selected countries and years
filtered_co2_data = co2_data[
    (co2_data['iso_code'].isin(selected_countries_alpha)) &
    (co2_data['year'].isin(year_range))
].copy()

# Add country name annotations to the last year in the data
if not filtered_co2_data.empty:
    # Find the last year of data for each country
    latest_data = filtered_co2_data.groupby('iso_code').apply(lambda df: df[df['year'] == 2012])

    # Plot CO2 emissions per capita trends
    fig = px.line(
        filtered_co2_data,
        x='year',
        y='co2_per_capita',
        color='iso_code',
        labels={
            'year': 'Year',
            'co2_per_capita': 'CO₂ Emissions Per Capita (Metric Tons)',
            'iso_code': 'Country'
        },
        title="CO₂ Emissions Per Capita Trends (1981–2023)"
    )

    # Add country name annotations for the latest data points
    for _, row in latest_data.iterrows():
        fig.add_annotation(
            x=row['year'],
            y=row['co2_per_capita'],
            text=row['iso_code'],  # Display ISO code or replace with country name if desired
            showarrow=False,
            font=dict(size=10),
            xanchor='left',  # Align annotation to the left of the point
            yanchor='middle'
        )

    # Customize the layout for better visualization
    fig.update_layout(
        title={
            'text': "CO₂ Emissions Per Capita Trends (1981–2023)",
            'x': 0.5,  # Center the title
            'xanchor': 'center'
        },
        legend_title="Country",
        margin=dict(t=50, b=50, l=25, r=25)
    )

    # Display the Plotly chart
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No CO₂ data available for the selected countries and years.")


    
    
    
    
    
    
    
    
    

# Add a citation for the data source
st.markdown("""---""")

st.markdown("""
**Data Sources:**  

**WVS time-series (1981-2022):**  
  Inglehart, R., Haerpfer, C., Moreno, A., Welzel, C., Kizilova, K., Diez-Medrano J., M. Lagos, P. Norris, E. Ponarin & B. Puranen (eds.). 2022. *World Values Survey: All Rounds – Country-Pooled Datafile Version 3.0*. Madrid, Spain & Vienna, Austria: JD Systems Institute & WVSA Secretariat. doi:10.14281/18241.17  
  Visit the [World Values Survey Documentation](https://www.worldvaluessurvey.org/WVSDocumentationWVL.jsp).

**CO₂ and Greenhouse Gas Emissions:**  
  Visit [Our World in Data](https://ourworldindata.org/co2-and-greenhouse-gas-emissions) for more information.
""")

st.markdown("""
**Author:**  
**Jaronimas Snipas**  
[GitHub](https://github.com/jaronimas-codes)  
[LinkedIn](https://www.linkedin.com/in/jaronimas-snipas/)
""")
