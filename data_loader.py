import pandas as pd
import streamlit as st


@st.cache_data
def load_data():

    df = pd.read_csv("data/Atlantic_South_Korea.csv")

    df["date"] = pd.to_datetime(df["date"])

    return df