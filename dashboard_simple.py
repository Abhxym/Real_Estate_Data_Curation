import streamlit as st
import pandas as pd
import plotly.express as px
import traceback

st.set_page_config(page_title="Real Estate Dashboard", page_icon="🏠", layout="wide")

st.title("🏠 Real Estate Analytics Dashboard")

# Load data with error handling
@st.cache_data
def load_data():
    try:
        df_dict = pd.read_excel('data/real_estate_curation_project.xlsx', sheet_name=None)
        return df_dict, None
    except Exception as e:
        return None, str(e)

dataframes, error = load_data()

if error:
    st.error(f"❌ Error loading data: {error}")
    st.info("Make sure 'real_estate_curation_project.xlsx' is in the 'data' folder")
    st.stop()

if dataframes is None:
    st.error("❌ No data loaded")
    st.stop()

st.success(f"✅ Data loaded successfully! Found {len(dataframes)} sheets")

# Sidebar
page = st.sidebar.radio("Navigation", ["Overview", "Customers", "Properties", "Brokers", "Deals"])

try:
    if page == "Overview":
        st.header("📊 Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Customers", len(dataframes.get('Customers', [])))
        with col2:
            st.metric("Properties", len(dataframes.get('Properties', [])))
        with col3:
            st.metric("Brokers", len(dataframes.get('Brokers', [])))
        with col4:
            st.metric("Deals", len(dataframes.get('Deals', [])))
        
        st.subheader("Dataset Sizes")
        sizes = pd.DataFrame({
            'Dataset': list(dataframes.keys()),
            'Rows': [len(df) for df in dataframes.values()]
        })
        fig = px.bar(sizes, x='Dataset', y='Rows', title='Records per Dataset')
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Preview Data")
        selected = st.selectbox("Select dataset", list(dataframes.keys()))
        st.dataframe(dataframes[selected].head(10), use_container_width=True)
    
    elif page == "Customers":
        st.header("👥 Customers")
        df = dataframes['Customers']
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'city' in df.columns:
                city_counts = df['city'].value_counts().head(10)
                fig = px.bar(x=city_counts.index, y=city_counts.values,
                           title='Top 10 Cities', labels={'x': 'City', 'y': 'Count'})
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'segment' in df.columns:
                segment_counts = df['segment'].value_counts()
                fig = px.pie(values=segment_counts.values, names=segment_counts.index,
                           title='Customer Segments')
                st.plotly_chart(fig, use_container_width=True)
        
        if 'annual_income' in df.columns and 'segment' in df.columns:
            fig = px.box(df, x='segment', y='annual_income',
                        title='Income by Segment')
            st.plotly_chart(fig, use_container_width=True)
    
    elif page == "Properties":
        st.header("🏘️ Properties")
        df = dataframes['Properties']
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'property_type' in df.columns:
                type_counts = df['property_type'].value_counts()
                fig = px.pie(values=type_counts.values, names=type_counts.index,
                           title='Property Types')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'city' in df.columns:
                city_counts = df['city'].value_counts().head(10)
                fig = px.bar(x=city_counts.index, y=city_counts.values,
                           title='Top 10 Cities', labels={'x': 'City', 'y': 'Count'})
                st.plotly_chart(fig, use_container_width=True)
        
        if 'area_sqft' in df.columns and 'property_type' in df.columns:
            fig = px.box(df, x='property_type', y='area_sqft',
                        title='Area by Property Type')
            st.plotly_chart(fig, use_container_width=True)
    
    elif page == "Brokers":
        st.header("🤝 Brokers")
        df = dataframes['Brokers']
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'agency' in df.columns:
                agency_counts = df['agency'].value_counts().head(10)
                fig = px.bar(x=agency_counts.index, y=agency_counts.values,
                           title='Top 10 Agencies', labels={'x': 'Agency', 'y': 'Count'})
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'rating' in df.columns:
                fig = px.histogram(df, x='rating', title='Broker Ratings')
                st.plotly_chart(fig, use_container_width=True)
        
        if 'experience_years' in df.columns:
            fig = px.histogram(df, x='experience_years',
                             title='Broker Experience (Years)')
            st.plotly_chart(fig, use_container_width=True)
    
    elif page == "Deals":
        st.header("💼 Deals")
        df = dataframes['Deals']
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Deals", len(df))
        with col2:
            if 'status' in df.columns:
                closed = len(df[df['status'] == 'Closed'])
                st.metric("Closed Deals", closed)
        with col3:
            if 'final_price' in df.columns:
                avg_price = df['final_price'].mean()
                st.metric("Avg Price", f"₹{avg_price:,.0f}")
        with col4:
            if 'status' in df.columns:
                rate = (closed / len(df) * 100) if len(df) > 0 else 0
                st.metric("Closure Rate", f"{rate:.1f}%")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'status' in df.columns:
                status_counts = df['status'].value_counts()
                fig = px.pie(values=status_counts.values, names=status_counts.index,
                           title='Deal Status')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'mortgage' in df.columns:
                mortgage_counts = df['mortgage'].value_counts()
                fig = px.pie(values=mortgage_counts.values, names=mortgage_counts.index,
                           title='Mortgage Distribution')
                st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"❌ Error: {e}")
    with st.expander("Show error details"):
        st.code(traceback.format_exc())
