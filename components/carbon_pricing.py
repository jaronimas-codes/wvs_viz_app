import streamlit as st
import plotly.express as px
import pandas as pd
import pycountry





def classify_instrument(row):
    if row["Carbon Tax"] > 0 and row["ETS"] > 0:
        return "Both"
    elif row["Carbon Tax"] > 0:
        return "Carbon Tax"
    elif row["ETS"] > 0:
        return "ETS"
    else:
        return "None"


def render_carbon_pricing_map(tax_data):
    st.markdown("### Step 4: Carbon Pricing Map")

    # Prepare map data
    iso3_codes = pd.DataFrame([country.alpha_3 for country in pycountry.countries], columns=["ISO3"])
    iso3_codes["Instrument"] = "None"
    tax_data["Instrument"] = tax_data.apply(lambda row: classify_instrument(row), axis=1)
    merged_data = pd.merge(iso3_codes, tax_data, on="ISO3", how="left")
    merged_data["Instrument"] = merged_data["Instrument"].fillna("None")

    # Render map
    fig = px.choropleth(
        merged_data,
        locations="ISO3",
        color="Instrument",
        title="Carbon Pricing Instruments",
        color_discrete_map={"None": "lightgray", "Carbon Tax": "#66bb6a", "ETS": "#42a5f5", "Both": "#8e24aa"}
    )
    st.plotly_chart(fig, use_container_width=True)
