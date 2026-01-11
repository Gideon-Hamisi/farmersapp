import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import os

# Config for presentation
st.set_page_config(
    page_title="🌱 AgriTrack Pro - Nairobi Farmers",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
# 🌱 **AgriTrack Pro** - Precision Farming Dashboard
**Real-time farmer management for Nairobi County**  
*Onboarding • Progress Tracking • AI Assistant • Training Academy*
""")

# ========================================
# SAMPLE DATA (Auto-loads for presentation)
# ========================================
@st.cache_data
def load_sample_data():
    sample_data = {
        'name': ['John Mwangi', 'Amina Hassan', 'Peter Omondi', 'Fatuma Ali', 'David Kiprop'],
        'farm_id': ['NAI-001', 'NAI-002', 'NAI-003', 'NAI-004', 'NAI-005'],
        'phone': ['+254712345678', '+254798765432', '+254723456789', '+254734567890', '+254745678901'],
        'planting_date': ['2026-01-05', '2026-01-03', '2026-01-07', '2026-01-02', '2026-01-06'],
        'status': ['Growing', 'Germinated', 'Planted', 'Harvested', 'Growing'],
        'crop': ['Maize', 'Tomatoes', 'Beans', 'Maize', 'Potatoes'],
        'farm_size': [2.5, 1.8, 3.2, 2.0, 1.5],
        'last_watered': ['2026-01-10', '2026-01-09', '2026-01-11', '2026-01-08', '2026-01-10'],
        'yield_estimate': [4500, 3200, 2800, 5200, 3800]
    }
    return pd.DataFrame(sample_data)

def save_data(df):
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/farmers.csv", index=False)

# Load data
if os.path.exists("data/farmers.csv"):
    df = pd.read_csv("data/farmers.csv")
else:
    df = load_sample_data()
    save_data(df)

# Sidebar
with st.sidebar:
    st.markdown("## 📱 Navigation")
    page = st.selectbox("Go To", [
        "📊 Dashboard", "👤 Onboard", "📈 Track Progress", 
        "🤖 AI Assistant", "📚 Training", "🔔 Reminders", "📋 Farmers"
    ], index=0)
    
    st.markdown("---")
    st.metric("Live Farmers", len(df))
    st.success("✅ **Production Ready**")

# ========================================
# 1. DASHBOARD (Presentation Hero)
# ========================================
if page == "📊 Dashboard":
    st.header("📊 **Executive Dashboard**")
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total = len(df)
        st.metric("Total Farmers", total, delta=f"+{total//2}")
    with col2:
        growing = len(df[df['status']=='Growing'])
        st.metric("Growing Crops", growing, delta="+2")
    with col3:
        harvested = len(df[df['status']=='Harvested'])
        st.metric("Harvested", harvested, delta="+1")
    with col4:
        total_yield = df['yield_estimate'].sum()
        st.metric("Est. Yield (kg)", f"{total_yield:,.0f}", delta="+15%")
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    with col1:
        status_pie = px.pie(df, names='status', 
                           title="Crop Status Distribution",
                           color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
        st.plotly_chart(status_pie, use_container_width=True)
    
    with col2:
        crop_bar = px.bar(df, x='name', y='farm_size', color='crop',
                         title="Farm Size by Crop Type")
        st.plotly_chart(crop_bar, use_container_width=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    with col1:
        days_since = (date.today() - pd.to_datetime(df['planting_date']).dt.date).dt.days
        fig_hist = px.histogram(x=days_since, color=df['status'],
                               title="Days Since Planting")
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        yield_scatter = px.scatter(df, x='farm_size', y='yield_estimate', 
                                  size='farm_size', color='status',
                                  hover_name='name', title="Yield vs Farm Size")
        st.plotly_chart(yield_scatter, use_container_width=True)

# ========================================
# 2. ONBOARD FARMER
# ========================================
elif page == "👤 Onboard":
    st.header("👤 **Onboard New Farmer**")
    with st.form("onboard_form"):
        col1, col2 = st.columns(2)
        name = col1.text_input("👨‍🌾 Full Name *")
        farm_id = col1.text_input("🏡 Farm ID *", help="e.g., NAI-006")
        phone = col2.text_input("📱 Phone *")
        planting_date = col2.date_input("🌱 Planting Date *")
        
        col3, col4 = st.columns(2)
        crop = col3.selectbox("🌾 Crop Type", ["Maize", "Tomatoes", "Beans", "Potatoes", "Wheat"])
        farm_size = col4.number_input("📏 Farm Size (Acres)*", min_value=0.1, value=1.0)
        
        notes = st.text_area("📝 Notes")
        
        col1, col2 = st.columns(2)
        submitted = col1.form_submit_button("✅ Onboard Farmer", use_container_width=True)
        
        if submitted and name and farm_id and phone:
            new_farmer = pd.DataFrame([{
                'name': name, 'farm_id': farm_id, 'phone': phone,
                'planting_date': planting_date, 'status': 'Planted',
                'crop': crop, 'farm_size': farm_size, 'notes': notes,
                'last_watered': date.today(), 'yield_estimate': farm_size * 2000
            }])
            global df
            df = pd.concat([df, new_farmer], ignore_index=True)
            save_data(df)
            st.success("🎉 **New farmer onboarded successfully!**")
            st.balloons()
            st.rerun()

# ========================================
# 3. AI ASSISTANT (Presentation Wow!)
# ========================================
elif page == "🤖 AI Assistant":
    st.header("🤖 **AI Farming Advisor**")
    
    # AI Responses
    ai_questions = {
        "What watering schedule for maize?": """
        **🌽 Maize Watering Schedule:**
        - **Days 1-14**: Daily, 25-30mm
        - **Days 15-30**: Every 2 days, 30mm  
        - **Vegetative**: Every 3 days, 40mm
        - **Flowering**: Every 2 days, 50mm
        - **Tip**: Water early morning 5-8AM
        """,
        "Best fertilizer for tomatoes?": """
        **🍅 Tomato Fertilizer Program:**
        1. **Week 2**: NPK 5-10-10 (200g/plant)
        2. **Week 4**: Calcium nitrate (150g/plant)  
        3. **Week 6+**: Potassium sulfate (100g/plant)
        4. **Organic**: Compost monthly (2kg/plant)
        """,
        "Pest control methods?": """
        **🐛 Integrated Pest Management:**
        - **Aphids**: Neem oil (5ml/L) weekly spray
        - **Cutworms**: Ash collar around stems
        - **Fall Armyworm**: Pheremone traps + Bt toxin
        - **Prevention**: Companion planting (marigolds)
        """
    }
    
    question = st.selectbox("Ask AI:", list(ai_questions.keys()))
    if st.button("💡 Get Advice", use_container_width=True):
        st.markdown(ai_questions[question])
    
    # Free chat
    st.subheader("💬 Free Chat")
    user_input = st.text_input("Ask anything about farming...")
    if st.button("Send") and user_input:
        st.info(f"🤖 **AI**: For '{user_input}', check our comprehensive training manual or ask a specific question!")

# ========================================
# 4. TRAINING ACADEMY
# ========================================
elif page == "📚 Training":
    st.header("📚 **Farmer Training Academy**")
    
    tab1, tab2, tab3, tab4 = st.tabs(["💧 Watering", "🌿 Nutrition", "🐛 Pests", "📈 Harvest"])
    
    with tab1:
        st.markdown("""
        ### 💧 **Precision Watering Guide**
        | Crop | Days 1-14 | Days 15-30 | Mature |
        |------|-----------|------------|--------|
        | Maize | Daily 25mm | 2-3 days | 5-7 days |
        | Tomatoes | Daily 20mm | Every 2d | Every 3d |
        | Beans | Every 2d | Every 3d | Weekly |
        
        **Pro Tip**: Finger test - dry 2" deep = water time
        """)
    
    with tab2:
        st.markdown("""
        ### 🌿 **Fertilizer Calculator**
        - **NPK Ratios**: Maize(20-10-10), Tomatoes(5-10-10)
        - **Application**: 200g/plant every 2 weeks
        - **Organic**: 2kg compost monthly per acre
        """)
    
    with tab3:
        st.markdown("""
        ### 🐛 **Pest Control Protocol**
        1. **Scout weekly** - Check 10 plants/acre
        2. **Neem oil** - 5ml/L water, spray weekly
        3. **Trap crops** - Plant marigolds around field
        4. **Bt toxin** - Organic bacterial control
        """)
    
    with tab4:
        st.markdown("""
        ### 📈 **Harvest Readiness**
        | Crop | Days to Harvest | Indicators |
        |------|----------------|------------|
        | Maize | 90-120 | Dry husk, hard kernels |
        | Tomatoes | 60-75 | Full color, slight softness |
        | Beans | 45-60 | Dry pods, rattle sound |
        """)
    
    st.download_button("📥 Full Manual PDF", "Training content...", "training.pdf")

# ========================================
# 5. REMINDERS & TRACK
# ========================================
elif page == "🔔 Reminders":
    st.header("🔔 **Smart Reminders**")
    today = date.today()
    
    reminders = []
    for _, row in df.iterrows():
        days_since = (today - pd.to_datetime(row['planting_date']).date()).days
        if row['status'] in ['Planted', 'Germinated'] and days_since % 3 == 0:
            reminders.append(f"💧 **{row['name']}** - Water {row['crop']} today!")
    
    if reminders:
        for r in reminders:
            st.warning(r)
    else:
        st.success("✅ All farmers up to date!")

elif page == "📈 Track Progress":
    st.header("📈 **Track Individual Progress**")
    fid = st.selectbox("Select Farmer", df['farm_id'])
    farmer = df[df['farm_id']==fid].iloc[0]
    
    col1, col2, col3 = st.columns(3)
    status = col1.selectbox("Status", ['Planted','Germinated','Growing','Harvested'],
                           index=['Planted','Germinated','Growing','Harvested'].index(farmer['status']))
    watered = col2.date_input("Last Watered", pd.to_datetime(farmer['last_watered']).date())
    yield_est = col3.number_input("Yield Est (kg)", value=float(farmer['yield_estimate']))
    
    if st.button("💾 Update", use_container_width=True):
        mask = df['farm_id']==fid
        df.loc[mask, 'status'] = status
        df.loc[mask, 'last_watered'] = watered
        df.loc[mask, 'yield_estimate'] = yield_est
        save_data(df)
        st.success("✅ Updated!")
        st.rerun()
    
    st.dataframe(df[df['farm_id']==fid])

elif page == "📋 Farmers":
    st.header("📋 **Complete Farmer Database**")
    st.dataframe(df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
**🌍 AgriTrack Pro** | Optimized for Nairobi Farmers | Built with ❤️ for Kenyan Agriculture
""")
