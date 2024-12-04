import streamlit as st
from utils.data_loader import load_all_data
from utils.styles import apply_custom_styles
from components.world_values import render_world_values
from components.youth_responses import render_youth_responses
from components.co2_emissions import render_co2_emissions
from components.carbon_pricing import render_carbon_pricing_map

# Apply styles
apply_custom_styles()

# Header Image
st.image(
    "img/no_planet_b.jpg",
    caption="No Planet B, Photo by [Markus Spiske](https://www.pexels.com/photo/climate-road-landscape-people-2990650/)",
    use_container_width=True
)

# Title
st.title("🌱 Youth, Environment, and Action: Insights from Global Data")

# Load data
env_data, age_data, co2_data, tax_data = load_all_data()

# Render sections
st.markdown("<hr>", unsafe_allow_html=True)
render_world_values(env_data)

st.markdown("<hr>", unsafe_allow_html=True)
render_youth_responses(age_data)

st.markdown("<hr>", unsafe_allow_html=True)
render_co2_emissions(co2_data)

st.markdown("<hr>", unsafe_allow_html=True)
render_carbon_pricing_map(tax_data)

# Action Plan
st.markdown("""
### Step 5: 🌱 Your Action Plan
- Compare your country's initiatives with others.
- Share insights and take action to reduce your carbon footprint.

**Data Sources:**  
- [World Values Survey](https://www.worldvaluessurvey.org/WVSDocumentationWVL.jsp)  
- [Our World in Data](https://ourworldindata.org/co2-and-greenhouse-gas-emissions)

**Author:**  
Jaronimas Snipas | [GitHub](https://github.com/jaronimas-codes) | [LinkedIn](https://www.linkedin.com/in/jaronimas-snipas/)
""")
