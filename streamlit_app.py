import pandas as pd
import plotly.express as px
import streamlit as st
from variable_mappings_env import variable_mappings

# Custom CSS to reduce padding and maximize content area
st.markdown(
    """
    <style>
        .appview-container .main .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Cached function to load the precomputed data
@st.cache_data
def load_precomputed_data():
    return pd.read_csv('precomputed_env_data.csv')

mean_data = load_precomputed_data()

# Filter variable_mappings to include only questions present in mean_data columns
question_options = {
    item_code: item_label
    for item in variable_mappings
    for item_code, item_label in item.items()
    if item_code in mean_data.columns
}

# Title
st.title("Does Your Country's Politicians Listen to the Youth Voice?")

# Country Selection
st.markdown("<div class='subtitle'>Select Countries</div>", unsafe_allow_html=True)
all_countries = sorted(mean_data['Country'].unique())
default_countries = ['AUS', 'CAN', 'CHN', 'RUS', 'DEU', 'CHE', 'USA']
selected_countries = st.multiselect(
    "Choose countries",
    options=all_countries,
    default=default_countries,
    key="country_selection"
)

# Wave Selection
st.markdown("<div class='subtitle'>Select Survey Waves</div>", unsafe_allow_html=True)
all_waves = sorted(mean_data['Wave'].unique())
selected_waves = st.multiselect(
    "Choose survey waves", 
    options=all_waves, 
    default=all_waves, 
    key="wave_selection"
)

# Question Selection
st.markdown("<div class='subtitle'>Select a Question</div>", unsafe_allow_html=True)
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
    filtered_data = mean_data[
        (mean_data['Country'].isin(selected_countries)) & 
        (mean_data['Wave'].isin(selected_waves))
    ][['Country', 'Wave', selected_question_key]].rename(columns={selected_question_key: 'mean_response'})

    # Plot visualization
    if not filtered_data.empty:
        fig = px.line(
            filtered_data,
            x='Wave',
            y='mean_response',
            color='Country',
            markers=True,
            labels={'Wave': 'Survey Wave', 'mean_response': f'Mean {selected_question_label}'},
            title=f'Mean "{selected_question_label}" by Country and Survey Wave'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write(f"No data available for the selected question '{selected_question_label}' with the chosen countries and waves.")
else:
    st.write("No available questions found in the precomputed data. Please check the 'precomputed_env_data.csv' file.")

# Citation at the bottom of the main page
st.markdown("""---""")  # Separator line

st.markdown("""
**Data Source:**  
**WVS time-series (1981-2022):**  
Inglehart, R., Haerpfer, C., Moreno, A., Welzel, C., Kizilova, K., Diez-Medrano J., M. Lagos, P. Norris, E. Ponarin & B. Puranen (eds.). 2022. *World Values Survey: All Rounds – Country-Pooled Datafile Version 3.0*. Madrid, Spain & Vienna, Austria: JD Systems Institute & WVSA Secretariat. doi:10.14281/18241.17  

For more information, visit the [World Values Survey Documentation](https://www.worldvaluessurvey.org/WVSDocumentationWVL.jsp).
""")

st.markdown("""
**Author:**  
**Jaronimas Snipas**  
[GitHub](https://github.com/jaronimas-codes)  
[LinkedIn](https://www.linkedin.com/in/jaronimas-snipas/)
""")
