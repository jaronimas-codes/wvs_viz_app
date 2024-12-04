def apply_custom_styles():
    import streamlit as st
    st.markdown(
        """
        <style>
            .stApp { background-color: #e8f5e9; }
            h1, h2, h3 { color: #2e7d32; }
            hr { border: 1px solid #388e3c; }
        </style>
        """,
        unsafe_allow_html=True
    )
