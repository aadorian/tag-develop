import streamlit as st
import pandas as pd
import sqlite3
import tempfile

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
st.code(""" http://localhost:8501/ """)
input = st.text_input('URL', 'https://docs.google.com/document/d/1VYT6uk7Q3DVAPudb1c7qIbojfoN3d5qgmH3ggREHmOo/edit?usp=sharing')
st.code(""" https://docs.google.com/document/d/1EFGk8gaQwCqsPY-i5YaMTo41EVRgrhLs/edit?usp=sharing&ouid=100322575540100494079&rtpof=true&sd=true """)