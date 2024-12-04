import streamlit as st
import plotly.express as px

def render_co2_emissions(co2_data):
    st.markdown("### Step 3: 🌍 CO₂ Emissions Trends")
    countries = st.multiselect("Choose countries", options=co2_data['iso_code'].unique(), default=["USA", "CAN"])
    filtered_data = co2_data[co2_data['iso_code'].isin(countries) & (co2_data['year'] >= 1981)]

    if not filtered_data.empty:
        fig = px.line(
            filtered_data,
            x='year',
            y='co2_per_capita',
            color='iso_code',
            title="CO₂ Emissions Trends (1981-2023)"
        )
        st.plotly_chart(fig, use_container_width=True)
