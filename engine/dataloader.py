import pandas as pd
import streamlit as st

@st.cache_data
def load_data(path:str)->pd.DataFrame:
    df = pd.read_csv(path)

    df['ListingCreationDate'] = pd.to_datetime(df['ListingCreationDate'], format="mixed")
    df['ClosedDate'] = pd.to_datetime(df['ClosedDate'], format="mixed")
    df['DateCreditPulled'] = pd.to_datetime(df['DateCreditPulled'], format="mixed")
    df['LoanOriginationDate'] = pd.to_datetime(df['LoanOriginationDate'], format="mixed")

    return df
