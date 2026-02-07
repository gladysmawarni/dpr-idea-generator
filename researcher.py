import streamlit as st
from helper.function import research_function, formatter


st.set_page_config(layout="centered")

## SESSION STATE
if "results" not in st.session_state:
    st.session_state["results"] = None

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Dosis:wght@200..800&family=Spectral:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,800;1,200;1,300;1,400;1,500;1,600;1,700;1,800&display=swap');

        .custom-font {
            font-family: 'Dosis', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)


## FORM
company_name = st.text_input("Company Name")
topics = st.text_input("Topics")

if st.button("Research"):
    if not company_name and not topics:
        st.error("Please enter at least a Company Name or Topics before researching.")
    else:
        st.session_state["results"] = research_function(company_name, topics)

        if st.session_state["results"] is not None:
            formatter(st.session_state["results"], True)