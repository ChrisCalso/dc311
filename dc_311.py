import pandas as pd
import streamlit as st
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans

st.title("What the 311??")
st.subheader("DC 311 Data from 2019")

@st.cache
def fetch_data():
    data = pd.read_csv('https://opendata.arcgis.com/datasets/98b7406def094fa59838f14beb1b8c81_10.csv')
    # change dates to datetime data types
    date_cols = ['ADDDATE', 'RESOLUTIONDATE', 'SERVICEDUEDATE', 'SERVICEORDERDATE', 'INSPECTIONDATE']
    data[date_cols] = data[date_cols].apply(pd.to_datetime)
    data = data.dropna(subset=['WARD', 'SERVICECODEDESCRIPTION'])
    # rename for ST map function requirement
    return data

data = fetch_data().copy()
st.write(data.head())


# get list of types of 311 calls to add to a sidebar menu
@st.cache
def get_code_names(data):
    return data.SERVICECODEDESCRIPTION.value_counts().index.values
code_names = get_code_names(data)
code_value = st.sidebar.selectbox(
    'Which call type would you like to see?',
     code_names)

@st.cache
def get_ward_names(data):
    names = data.WARD.unique()
    names.sort()
    return names
ward_names = list(get_ward_names(data))
ward_values = st.sidebar.multiselect(
    'Which ward(s) would you like to see?',
     ward_names,
     default=ward_names[:-1]  # get rid of NaNs for now
     )
@st.cache
def get_data_code_ward(data, code, wards):
    return_df = data[(data.WARD.isin(wards)) & (data.SERVICECODEDESCRIPTION == code)]
    return return_df

st.write(f'## Map of {code_value} Reports')
map_df = get_data_code_ward(data, code_value, ward_values).copy()
map_df = map_df.rename(columns={'LATITUDE': 'lat',
                                'LONGITUDE': 'lon'})
st.map(map_df)
  

