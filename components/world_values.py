import streamlit as st
import plotly.express as px
from utils.data_loader import get_country_mapping, get_question_options

def render_world_values(env_data):
    st.markdown("### Step 1: 🌎 Explore World Trends")

    # Country selection
    country_mapping = get_country_mapping()
    all_countries_codes = env_data['Country'].unique()
    all_countries_names = [country_mapping.get(c3, c3) for c3 in all_countries_codes]
    selected_countries = st.multiselect(
        "Choose countries", options=all_countries_names, default=["Australia", "Canada", "China"]
    )
    selected_countries_3 = [k for k, v in country_mapping.items() if v in selected_countries]

    # Survey wave selection
    waves = sorted(env_data['Wave'].unique())
    selected_waves = st.multiselect("Choose survey waves", options=waves, default=waves)

    # Question selection
    question_options = get_question_options(env_data)
    if question_options:
        selected_question = st.selectbox(
            "Choose a question", options=list(question_options.keys()), format_func=lambda x: question_options[x]
        )
        filtered_data = env_data[
            (env_data['Country'].isin(selected_countries_3)) & (env_data['Wave'].isin(selected_waves))
        ][['Country', 'Wave', selected_question]].rename(columns={selected_question: 'mean_response'})

        if not filtered_data.empty:
            fig = px.line(
                filtered_data,
                x='Wave',
                y='mean_response',
                color='Country',
                markers=True,
                title=f"Responses to '{question_options[selected_question]}'",
                color_discrete_sequence=px.colors.sequential.Blues
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No data available for the selected filters.")
