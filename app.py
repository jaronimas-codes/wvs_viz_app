import pandas as pd
import plotly.express as px
import streamlit as st
import random
from variable_mappings_env import variable_mappings

# Custom CSS to enlarge text and maximize graph area
st.markdown(
    """
    <style>
        .title { font-size: 2em; font-weight: bold; }
        .question-label { font-size: 1.5em; font-weight: bold; margin-top: 1rem; }
        .stPlotlyChart { max-width: 100%; padding: 0; margin-top: 1rem; }
        .main { padding: 1rem 3rem; }
    </style>
    """,
    unsafe_allow_html=True
)

# Cached function to load the precomputed data
@st.cache_data
def load_precomputed_data():
    return pd.read_csv('precomputed_means.csv')

mean_data = load_precomputed_data()

# Filter variable_mappings to include only questions present in mean_data columns
question_options = {
    item_code: item_label
    for item in variable_mappings
    for item_code, item_label in item.items()
    if item_code in mean_data.columns
}

# Title
st.markdown("<div class='title'>World Values Survey Data Visualization</div>", unsafe_allow_html=True)

# Sidebar for filters and citation
st.sidebar.header("Filters")
default_countries = ['AUS', 'CAN', 'CHN', 'RUS', 'DEU', 'LTU', 'CHE']
selected_countries = st.sidebar.multiselect("Select Countries", mean_data['COUNTRY_ALPHA'].unique(), default=default_countries)
selected_wave = st.sidebar.multiselect("Select Survey Wave", mean_data['S002VS'].unique(), default=mean_data['S002VS'].unique())

# Citation in the sidebar
st.sidebar.markdown("""
**Data Source:**  
**WVS time-series (1981-2022):**  
Inglehart, R., Haerpfer, C., Moreno, A., Welzel, C., Kizilova, K., Diez-Medrano J., M. Lagos, P. Norris, E. Ponarin & B. Puranen (eds.). 2022. *World Values Survey: All Rounds – Country-Pooled Datafile Version 3.0*. Madrid, Spain & Vienna, Austria: JD Systems Institute & WVSA Secretariat. doi:10.14281/18241.17  

For more information, visit the [World Values Survey Documentation](https://www.worldvaluessurvey.org/WVSDocumentationWVL.jsp).
""")

# Citation in the sidebar
st.sidebar.markdown("""
**Author:**  
**Jaronimas Snipas**  
[GitHub](https://github.com/jaronimas-codes)  
[LinkedIn](https://www.linkedin.com/in/jaronimas-snipas/)
""")

def get_random_index(options):
    return random.randint(0, len(options) - 1)

# Check if questions are available; if not, display a message
if question_options:
    for i, question_key in enumerate(['first_question', 'second_question', 'third_question'], start=1):
        st.markdown(f"<div class='question-label'>Select Question {i}</div>", unsafe_allow_html=True)
        selected_question_key = st.selectbox(
            f"Question {i} for visualization", 
            options=list(question_options.keys()), 
            format_func=lambda x: question_options[x], 
            index=i,
            key=question_key, 
            label_visibility="collapsed"
        )
        selected_question_label = question_options[selected_question_key]

        filtered_data = mean_data[
            (mean_data['COUNTRY_ALPHA'].isin(selected_countries)) & (mean_data['S002VS'].isin(selected_wave))
        ][['COUNTRY_ALPHA', 'S002VS', selected_question_key]].rename(columns={selected_question_key: 'mean_response'})

        try:
            fig = px.line(
                filtered_data,
                x='S002VS',
                y='mean_response',
                color='COUNTRY_ALPHA',
                markers=True,
                labels={'S002VS': 'Survey Wave', 'mean_response': f'Mean {selected_question_label}'},
                title=f'Mean "{selected_question_label}" by Country and Survey Wave'
            )
            st.plotly_chart(fig, key=f'fig_{i}', use_container_width=True)
        except ValueError:
            st.write(f"No data available for the selected question '{selected_question_label}' with the chosen countries and waves.")

else:
    st.write("No available questions found in the precomputed data. Please check the 'precomputed_means.csv' file.")