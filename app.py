import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import os

st.set_page_config(page_title="🌱 AgriTrack Pro", page_icon="🌱", layout="wide")

st.markdown("""
# 🌱 **AgriTrack Pro** - Precision Farming Dashboard
**Nairobi County Farmers • Real-time Tracking • AI Advisor**
""")

# ========================================
# DATA MANAGEMENT (FIXED - No global errors)
# ========================================
@st.cache_data
def load_sample_data():
    return pd.DataFrame({
        'name': ['John Mwangi', 'Amina Hassan', 'Peter Omondi', 'Fatuma Ali', 'David Kiprop'],
        'farm_id': ['NAI-001', 'NAI-002', 'NAI-003', 'NAI-004', 'NAI-005'],
        'phone': ['+254712345678', '+254798765432', '+254723456789', '+254734567890', '+254745678901'],
        'planting_date': ['2026-01-05', '2026-01-03', '2026-01-07', '2026-01-02', '2026-01-06'],
        'status': ['Growing', 'Germinated', 'Planted', 'Harvested', 'Growing'],
        'crop': ['Maize', 'Tomatoes', 'Beans', 'Maize', 'Potatoes'],
        'farm_size': [2.5, 1.8, 3.2, 2.0, 1.5],
        'last_watered': ['2026-01-10', '2026-01-09', '2026-01-11', '2026-01-08', '2026-01-10'],
        'yield_estimate': [4500, 3200, 2800, 5200, 3800]
    })

def load_data():
    if os.path.exists("farmers.csv"):
        return pd.read_csv("farmers.csv")
    df = load_sample_data()
    save_data(df)
    return df

def save_data(df):
    os.makedirs(".", exist_ok=True)
    df.to_csv("farmers.csv", index=False)

# Load data ONCE
df = load_data()

# Sidebar
st.sidebar.title("📱 Navigation")
page = st.sidebar.selectbox("Select", ["📊 Dashboard", "👤 Onboard", "📈 Track", "🤖 AI", "📚 Training", "🔔 Reminders"])

# ========================================
# DASHBOARD
# ========================================
if page == "📊 Dashboard":
    st.header("📊 Executive Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Farmers", len(df))
    with col2: st.metric("Growing", len(df[df['status']=='Growing']))
    with col3: st.metric("Harvested", len(df[df['status']=='Harvested']))
    with col4: st.metric("Est. Yield", f"{df['yield_estimate'].sum():,.0f}kg")
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(df, names='status', title="Crop Status")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(df, x='name', y='farm_size', color='crop', title="Farm Size")
        st.plotly_chart(fig, use_container_width=True)

# ========================================
# ONBOARD (FIXED - No global statement needed)
# ========================================
elif page == "👤 Onboard":
    st.header("👤 Onboard Farmer")
    with st.form("onboard"):
        col1, col2 = st.columns(2)
        name = col1.text_input("Name")
        farm_id = col1.text_input("Farm ID")
        phone = col2.text_input("Phone")
        plant_date = col2.date_input("Plant Date")
        crop = st.selectbox("Crop", ["Maize", "Tomatoes", "Beans"])
        
        if st.form_submit_button("✅ Add Farmer"):
            new_row = pd.DataFrame([{
                'name': name, 'farm_id': farm_id, 'phone': phone,
                'planting_date': plant_date, 'status': 'Planted',
                'crop': crop, 'farm_size': 2.0, 'last_watered': date.today(),
                'yield_estimate': 4000
            }])
            
            # FIXED: Return new dataframe instead of global
            global_df = pd.concat([df, new_row], ignore_index=True)
            save_data(global_df)
            st.success("✅ Farmer added!")
            st.rerun()

# ========================================
# TRACK PROGRESS
# ========================================
elif page == "📈 Track":
    st.header("📈 Track Progress")
    if not df.empty:
        farm_id = st.selectbox("Farm", df['farm_id'])
        farmer = df[df['farm_id'] == farm_id].iloc[0]
        
        col1, col2 = st.columns(2)
        status = col1.selectbox("Status", ['Planted', 'Germinated', 'Growing', 'Harvested'],
                               index=['Planted', 'Germinated', 'Growing', 'Harvested'].index(farmer['status']))
        
        if st.button("Update"):
            # FIXED: Reload, update, save pattern
            temp_df = load_data()
            mask = temp_df['farm_id'] == farm_id
            temp_df.loc[mask, 'status'] = status
            save_data(temp_df)
            st.success("✅ Updated!")
            st.rerun()
    else:
        st.info("Add farmers first")

# ========================================
# AI ASSISTANT
# ========================================
elif page == "🤖 AI":
    st.header("🤖 AI Farming Advisor")
    ai_tips = {
        "Maize watering?": "Daily 25-30mm first 2 weeks, then every 3 days",
        "Tomato fertilizer?": "NPK 5-10-10 week 2, calcium nitrate week 4", 
        "Pest control?": "Neem oil 5ml/L weekly + companion planting"
    }
    
    question = st.selectbox("Quick Tips:", list(ai_tips.keys()))
    if st.button("💡 Answer"):
        st.info(f"🤖 {ai_tips[question]}")

# ========================================
# TRAINING
# ========================================
elif page == "📚 Training":
    st.header("📚 Training Academy")
    tab1, tab2 = st.tabs(["Watering", "Fertilizer"])
    
    with tab1:
        st.markdown("""
        **💧 Watering Guide:**
        - Maize: Daily first 14 days (25mm)
        - Tomatoes: Every 2 days (20mm)  
        - Check soil 2" deep before watering
        """)
    
    with tab2:
        st.markdown("""
        **🌿 Fertilizer:**
        | Crop | Week 2 | Week 4 |
        |------|--------|--------|
        | Maize | 20-10-10 | Compost |
        | Tomatoes | 5-10-10 | Calcium |
        """)

# ========================================
# REMINDERS
# ========================================
elif page == "🔔 Reminders":
    st.header("🔔 Smart Reminders")
    today = date.today()
    reminders = []
    
    for _, row in df.iterrows():
        days_since = (today - pd.to_datetime(row['planting_date']).date()).days
        if row['status'] == 'Planted' and days_since % 3 == 0:
            reminders.append(f"💧 Water {row['name']}'s {row['crop']}")
    
    if reminders:
        for r in reminders: st.warning(r)
    else:
        st.success("✅ All up to date!")

st.sidebar.success("✅ Live Demo Ready")
