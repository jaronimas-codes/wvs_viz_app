import streamlit as st
import plotly.express as px

def render_youth_responses(age_data):
    st.markdown("### Step 2: Youth Responses")
    selected_wave = st.selectbox("Select a wave", options=sorted(age_data['Wave'].unique()))
    selected_question = st.selectbox("Choose a question", options=age_data.columns[2:])

    filtered_data = age_data[age_data['Wave'] == selected_wave][['Country', selected_question]].rename(
        columns={selected_question: 'Percentage_Favorable'}
    )
    if not filtered_data.empty:
        fig = px.bar(
            filtered_data,
            x='Country',
            y='Percentage_Favorable',
            color='Percentage_Favorable',
            color_continuous_scale='greens',
            title="Youth Responses"
        )
        st.plotly_chart(fig, use_container_width=True)
