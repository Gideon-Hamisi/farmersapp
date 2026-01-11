import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import os

st.set_page_config(page_title="🌱 Farmer Tracker", layout="wide")
st.title("🌱 Farmer Progress Tracker")
st.markdown("**Live Demo - Nairobi Farmers**")

# Data storage
@st.cache_data
def load_data():
    if os.path.exists("farmers.csv"):
        return pd.read_csv("farmers.csv")
    return pd.DataFrame()

def save_data(df):
    df.to_csv("farmers.csv", index=False)

df = load_data()

# Sidebar
page = st.sidebar.selectbox("Page", ["Dashboard", "Onboard", "Track", "Reminders"])

if page == "Dashboard":
    col1, col2 = st.columns(2)
    col1.metric("Farmers", len(df))
    col2.metric("Growing", len(df[df['status']=='Growing']) if not df.empty else 0)
    
    if not df.empty:
        fig = px.pie(df, names='status', title="Status")
        st.plotly_chart(fig)

elif page == "Onboard":
    with st.form("add_farmer"):
        col1, col2 = st.columns(2)
        name = col1.text_input("Name")
        id = col1.text_input("Farm ID")
        phone = col2.text_input("Phone")
        plant_date = col2.date_input("Plant Date")
        submitted = st.form_submit_button("Add")
        if submitted:
            new = pd.DataFrame({
                'name': [name], 'farm_id': [id], 'phone': [phone],
                'planting_date': [plant_date], 'status': ['Planted'],
                'crop': ['Maize']
            })
            df = pd.concat([df, new])
            save_data(df)
            st.success("Added!")
            st.rerun()

elif page == "Track":
    if df.empty:
        st.info("Add farmers first")
    else:
        fid = st.selectbox("Farm", df['farm_id'])
        row = df[df['farm_id']==fid].iloc[0]
        status = st.selectbox("Status", ['Planted','Growing','Harvested'], 
                             index=['Planted','Growing','Harvested'].index(row['status']))
        if st.button("Update"):
            df.loc[df['farm_id']==fid, 'status'] = status
            save_data(df)
            st.rerun()
        st.dataframe(df)

elif page == "Reminders":
    st.success("✅ All farmers up to date! Check every 3 days.")
