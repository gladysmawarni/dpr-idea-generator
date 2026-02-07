import streamlit as st
from streamlit_gsheets import GSheetsConnection

from helper.function import formatter


st.set_page_config(layout="wide")

st.title('Saved Ideas :bulb:')

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()

# reverse the df
df = df.iloc[::-1].reset_index(drop=True)


st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Dosis:wght@200..800&family=Spectral:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,800;1,200;1,300;1,400;1,500;1,600;1,700;1,800&display=swap');

        .custom-font {
            font-family: 'Dosis', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)


formatter(df)