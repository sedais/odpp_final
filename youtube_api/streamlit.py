import streamlit as st
import pandas as pd
import numpy as np
import ssl
from api_search import search_by_query
from web_scraper_ifixit import get_the_content


@st.cache
def load_data():
    data = get_the_content()
    return data


def render_info():
    st.title('IFixIt data')
    st.header('Displaying the sentiment analysis scores on youtube search')
    st.markdown('Using streamlit to filter and display data')


def search_by_phone(data):
    data["phone_name"] = data["brand"] + data["model"]
    phone_name = st.sidebar.selectbox('Phone types:', [''] + list(data['phone_name'].drop_duplicates()))
    if phone_name:
        return data[data['phone_name'] == phone_name]
    return data


render_info()
data = load_data()
data = search_by_phone(data)
