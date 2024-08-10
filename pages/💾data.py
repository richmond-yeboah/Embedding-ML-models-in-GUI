import streamlit as st
import pandas as pd
import numpy as np


st.title("This is the data page")

@st.cache_data(show_spinner='Loading data')
def load_data():
    df = pd.read_csv('https://github.com/richmond-yeboah/Customer-Churn-Prediction/raw/main/Data/Telco.csv')
    return df

st.dataframe(load_data())