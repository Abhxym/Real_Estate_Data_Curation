import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Real Estate Analytics Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and process data from Excel file"""
    import os
    try:
        excel_file = 'data/real_estate_curation_project.xlsx'
        
        # Debug: Check if file exists
        if not os.path.exists(excel_file):
            st.error(f"❌ Excel file not found at: {excel_file}")
            st.info(f"Current directory: {os.getcwd()}")
            st.info(f"Files in current dir: {os.listdir('.')[:10]}")  # Show first 10 files
            if os.path.exists('data'):
                st.info(f"Files in data/: {os.listdir('data')}")
            return None
        
        dataframes = pd.read_excel(excel_file, sheet_name=None)
        return dataframes
    except Exception as e:
        st.error(f"Error loading data: {e}")
        import traceback
        st.code(traceback.format_exc())
        return None

def clean_city_names(df, city_mapping):
    """Standardize city names"""
    if 'city' in df.columns:
        df['city'] = df['city'].str.strip().str.title()
        df['city'] = df['city'].replace(city_mapping)
    return df

def prepare_data(dataframes):
    """Clean and prepare data"""
    city_mapping = {
        'Surrat': 'Surat', 'Chennnai': 'Chennai', 'Kalkata': 'Kolkata',
        'Calcutta': 'Kolkata', 'Mumbay': 'Mumbai', 'Mumbaai': 'Mumbai',
        'Bengluru': 'Bengaluru', 'Poona': 'Pune', 'Jaypur': 'Jaipur',
        'Ahemdabad': 'Ahmedabad', 'Dehli': 'Delhi', 'New Delhi': 'Delhi',
        'Nodia': 'Noida', 'Hyderbad': 'Hyderabad', 'Gurugram': 'Gurgaon'
    }
    
    for name in ['Customers', 'Brokers', 'Properties']:
        if name in dataframes:
            dataframes[name] = clean_city_names(dataframes[name], city_mapping)
    
    return dataframes

def main():
    st.title("🏠 Real Estate Analytics Dashboard")
    st.markdown("---")
    
    # Load data
    dataframes = load_data()
    
    if dataframes is None:
        st.error("Failed to load data. Please ensure 'real_estate_curation_project.xlsx' is in the data/ directory.")
        st.info("Expected file location: data/real_estate_curation_project.xlsx")
        return
    
    # Prepare data
    dataframes = prepare_data(dataframes)
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Page", 
                           ["Overview", "Customers", "Properties", "Brokers", "Deals", "Analytics", "Predictive Models"])
    
    if page == "Overview":
        show_overview(dataframes)
    elif page == "Customers":
        show_customers(dataframes)
    elif page == "Properties":
        show_properties(dataframes)
    elif page == "Brokers":
        show_brokers(dataframes)
    elif page == "Deals":
        show_deals(dataframes)
    elif page == "Analytics":
        show_analytics(dataframes)
    elif page == "Predictive Models":
        show_predictive_models(dataframes)

def show_overview(dataframes):
    """Display overview page"""
    st.header("📊 Data Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'Customers' in dataframes:
            st.metric("Total Customers", len(dataframes['Customers']))
    
    with col2:
        if 'Properties' in dataframes:
            st.metric("Total Properties", len(dataframes['Properties']))
    
    with col3:
        if 'Brokers' in dataframes:
            st.metric("Total Brokers", len(dataframes['Brokers']))
    
    with col4:
        if 'Deals' in dataframes:
            closed_deals = len(dataframes['Deals'][dataframes['Deals']['status'] == 'Closed'])
            st.metric("Closed Deals", closed_deals)
    
    st.markdown("---")
    
    # Dataset sizes
    st.subheader("Dataset Sizes")
    table_data = []
    for name, df in dataframes.items():
        table_data.append({
            'Dataset': name,
            'Rows': len(df),
            'Columns': len(df.columns)
        })
    
    df_summary = pd.DataFrame(table_data)
    
    fig = px.bar(df_summary, x='Dataset', y='Rows', 
                 title='Number of Records per Dataset',
                 color='Rows',
                 color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)
    
    # Show sample data
    st.subheader("Sample Data Preview")
    selected_table = st.selectbox("Select Dataset", list(dataframes.keys()))
    st.dataframe(dataframes[selected_table].head(10), use_container_width=True)

def show_customers(dataframes):
    """Display customer analytics"""
    st.header("👥 Customer Analytics")
    
    if 'Customers' not in dataframes:
        st.error("Customers data not found")
        return
    
    df = dataframes['Customers']
    
    col1, col2 = st.columns(2)
    
    with col1:
        # City distribution
        if 'city' in df.columns:
            city_counts = df['city'].value_counts().head(10)
            fig = px.bar(x=city_counts.index, y=city_counts.values,
                        title='Top 10 Cities by Customer Count',
                        labels={'x': 'City', 'y': 'Count'},
                        color=city_counts.values,
                        color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Segment distribution
        if 'segment' in df.columns:
            segment_counts = df['segment'].value_counts()
            fig = px.pie(values=segment_counts.values, names=segment_counts.index,
                        title='Customer Segments Distribution',
                        hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
    
    # Income analysis
    if 'annual_income' in df.columns and 'segment' in df.columns:
        st.subheader("Income Analysis by Segment")
        fig = px.box(df, x='segment', y='annual_income',
                    title='Annual Income Distribution by Segment',
                    color='segment')
        st.plotly_chart(fig, use_container_width=True)

def show_properties(dataframes):
    """Display property analytics"""
    st.header("🏘️ Property Analytics")
    
    if 'Properties' not in dataframes:
        st.error("Properties data not found")
        return
    
    df = dataframes['Properties']
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Property type distribution
        if 'property_type' in df.columns:
            type_counts = df['property_type'].value_counts()
            fig = px.pie(values=type_counts.values, names=type_counts.index,
                        title='Property Types Distribution',
                        hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # City distribution
        if 'city' in df.columns:
            city_counts = df['city'].value_counts().head(10)
            fig = px.bar(x=city_counts.index, y=city_counts.values,
                        title='Top 10 Cities by Property Count',
                        labels={'x': 'City', 'y': 'Count'},
                        color=city_counts.values,
                        color_continuous_scale='Reds')
            st.plotly_chart(fig, use_container_width=True)
    
    # Area analysis
    if 'area_sqft' in df.columns and 'property_type' in df.columns:
        st.subheader("Property Area Analysis")
        fig = px.box(df, x='property_type', y='area_sqft',
                    title='Area Distribution by Property Type',
                    color='property_type')
        st.plotly_chart(fig, use_container_width=True)
    
    # Bedrooms vs Bathrooms
    if 'bedrooms' in df.columns and 'bathrooms' in df.columns:
        col1, col2 = st.columns(2)
        with col1:
            bedroom_counts = df['bedrooms'].value_counts().sort_index()
            fig = px.bar(x=bedroom_counts.index, y=bedroom_counts.values,
                        title='Bedroom Distribution',
                        labels={'x': 'Bedrooms', 'y': 'Count'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            bathroom_counts = df['bathrooms'].value_counts().sort_index()
            fig = px.bar(x=bathroom_counts.index, y=bathroom_counts.values,
                        title='Bathroom Distribution',
                        labels={'x': 'Bathrooms', 'y': 'Count'})
            st.plotly_chart(fig, use_container_width=True)

def show_brokers(dataframes):
    """Display broker analytics"""
    st.header("🤝 Broker Analytics")
    
    if 'Brokers' not in dataframes:
        st.error("Brokers data not found")
        return
    
    df = dataframes['Brokers']
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Agency distribution
        if 'agency' in df.columns:
            agency_counts = df['agency'].value_counts().head(10)
            fig = px.bar(x=agency_counts.index, y=agency_counts.values,
                        title='Top 10 Agencies by Broker Count',
                        labels={'x': 'Agency', 'y': 'Count'},
                        color=agency_counts.values,
                        color_continuous_scale='Greens')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Rating distribution
        if 'rating' in df.columns:
            fig = px.histogram(df, x='rating',
                             title='Broker Rating Distribution',
                             nbins=20,
                             color_discrete_sequence=['#2ecc71'])
            st.plotly_chart(fig, use_container_width=True)
    
    # Experience analysis
    if 'experience_years' in df.columns:
        st.subheader("Experience Analysis")
        fig = px.histogram(df, x='experience_years',
                         title='Broker Experience Distribution (Years)',
                         nbins=20,
                         color_discrete_sequence=['#3498db'])
        st.plotly_chart(fig, use_container_width=True)
    
    # City distribution
    if 'city' in df.columns:
        city_counts = df['city'].value_counts().head(10)
        fig = px.bar(x=city_counts.index, y=city_counts.values,
                    title='Top 10 Cities by Broker Count',
                    labels={'x': 'City', 'y': 'Count'},
                    color=city_counts.values,
                    color_continuous_scale='Oranges')
        st.plotly_chart(fig, use_container_width=True)

def show_deals(dataframes):
    """Display deals analytics"""
    st.header("💼 Deals Analytics")
    
    if 'Deals' not in dataframes:
        st.error("Deals data not found")
        return
    
    df = dataframes['Deals']
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_deals = len(df)
        st.metric("Total Deals", total_deals)
    
    with col2:
        closed_deals = len(df[df['status'] == 'Closed'])
        st.metric("Closed Deals", closed_deals)
    
    with col3:
        if 'final_price' in df.columns:
            avg_price = df['final_price'].mean()
            st.metric("Avg Final Price", f"₹{avg_price:,.0f}")
    
    with col4:
        if 'status' in df.columns:
            closure_rate = (closed_deals / total_deals * 100) if total_deals > 0 else 0
            st.metric("Closure Rate", f"{closure_rate:.1f}%")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Status distribution
        if 'status' in df.columns:
            status_counts = df['status'].value_counts()
            fig = px.pie(values=status_counts.values, names=status_counts.index,
                        title='Deal Status Distribution',
                        hole=0.4,
                        color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Mortgage distribution
        if 'mortgage' in df.columns:
            mortgage_counts = df['mortgage'].value_counts()
            fig = px.pie(values=mortgage_counts.values, names=mortgage_counts.index,
                        title='Mortgage Distribution',
                        hole=0.4,
                        color_discrete_sequence=px.colors.sequential.Purp)
            st.plotly_chart(fig, use_container_width=True)
    
    # Price analysis
    if 'offer_price' in df.columns and 'final_price' in df.columns:
        st.subheader("Price Analysis")
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=df['offer_price'], name='Offer Price', opacity=0.7))
        fig.add_trace(go.Histogram(x=df['final_price'], name='Final Price', opacity=0.7))
        fig.update_layout(title='Offer Price vs Final Price Distribution',
                         xaxis_title='Price',
                         yaxis_title='Count',
                         barmode='overlay')
        st.plotly_chart(fig, use_container_width=True)
    
    # Loan rate analysis
    if 'loan_rate' in df.columns:
        st.subheader("Loan Rate Analysis")
        fig = px.histogram(df, x='loan_rate',
                         title='Loan Rate Distribution',
                         nbins=30,
                         color_discrete_sequence=['#e74c3c'])
        st.plotly_chart(fig, use_container_width=True)

def show_analytics(dataframes):
    """Display advanced analytics"""
    st.header("📈 Advanced Analytics")
    
    # Price per square foot
    if 'Properties' in dataframes and 'Deals' in dataframes:
        st.subheader("Price per Square Foot Analysis")
        
        properties = dataframes['Properties']
        deals = dataframes['Deals']
        
        if 'property_id' in properties.columns and 'property_id' in deals.columns:
            merged = deals.merge(properties, on='property_id', how='left')
            
            if 'final_price' in merged.columns and 'area_sqft' in merged.columns:
                merged['price_per_sqft'] = merged['final_price'] / merged['area_sqft']
                merged_clean = merged[merged['price_per_sqft'].notna()]
                
                if 'city_y' in merged_clean.columns:
                    city_avg = merged_clean.groupby('city_y')['price_per_sqft'].mean().sort_values(ascending=False).head(10)
                    fig = px.bar(x=city_avg.index, y=city_avg.values,
                                title='Top 10 Cities by Average Price per Sq Ft',
                                labels={'x': 'City', 'y': 'Price per Sq Ft (₹)'},
                                color=city_avg.values,
                                color_continuous_scale='Plasma')
                    st.plotly_chart(fig, use_container_width=True)
    
    # Broker success rate
    if 'Brokers' in dataframes and 'Deals' in dataframes:
        st.subheader("Broker Success Rate")
        
        brokers = dataframes['Brokers']
        deals = dataframes['Deals']
        
        if 'broker_id' in deals.columns:
            broker_deals = deals.groupby('broker_id').agg({
                'deal_id': 'count',
                'status': lambda x: (x == 'Closed').sum()
            }).reset_index()
            broker_deals.columns = ['broker_id', 'total_deals', 'closed_deals']
            broker_deals['success_rate'] = (broker_deals['closed_deals'] / broker_deals['total_deals'] * 100)
            
            top_brokers = broker_deals.nlargest(10, 'success_rate')
            
            fig = px.bar(top_brokers, x='broker_id', y='success_rate',
                        title='Top 10 Brokers by Success Rate',
                        labels={'broker_id': 'Broker ID', 'success_rate': 'Success Rate (%)'},
                        color='success_rate',
                        color_continuous_scale='Greens')
            st.plotly_chart(fig, use_container_width=True)
    
    # Deal trends over time
    if 'Deals' in dataframes and 'deal_date' in dataframes['Deals'].columns:
        st.subheader("Deal Trends Over Time")
        
        deals = dataframes['Deals'].copy()
        deals['deal_date'] = pd.to_datetime(deals['deal_date'], errors='coerce')
        deals['year_month'] = deals['deal_date'].dt.to_period('M').astype(str)
        
        monthly_deals = deals.groupby('year_month').size().reset_index(name='count')
        
        fig = px.line(monthly_deals, x='year_month', y='count',
                     title='Monthly Deal Trends',
                     labels={'year_month': 'Month', 'count': 'Number of Deals'},
                     markers=True)
        st.plotly_chart(fig, use_container_width=True)

def show_predictive_models(dataframes):
    """Display predictive modeling page"""
    st.header("🤖 Predictive Models")
    
    # Check if we have the necessary data
    if 'Deals' not in dataframes or 'Properties' not in dataframes:
        st.error("Required data not found")
        return
    
    # Prepare transformed data
    with st.spinner("Preparing data and training models..."):
        df_transformed = prepare_transformed_data(dataframes)
        
        if df_transformed is None:
            st.error("Could not prepare data for modeling")
            return
        
        # Import models
        from models import RealEstateModels
        
        # Initialize and train models
        re_models = RealEstateModels(df_transformed)
        
        try:
            results = re_models.train_all_models()
        except Exception as e:
            st.error(f"Error training models: {e}")
            return
    
    st.success("✅ All models trained successfully!")
    
    # Model selection tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "KPI Dashboard",
        "Model Comparison", 
        "Price Prediction", 
        "Feature Importance",
        "Deal Status Prediction",
        "Model Performance"
    ])
    
    with tab1:
        st.subheader("📊 Key Performance Indicators (KPIs)")
        
        # Prepare merged data for KPIs
        deals = dataframes['Deals'].copy()
        properties = dataframes['Properties'].copy()
        customers = dataframes['Customers'].copy()
        brokers = dataframes['Brokers'].copy()
        
        # Merge for comprehensive analysis
        df_kpi = deals.merge(properties, on='property_id', how='left', suffixes=('', '_prop'))
        df_kpi = df_kpi.merge(customers, on='customer_id', how='left', suffixes=('', '_cust'))
        df_kpi = df_kpi.merge(brokers, on='broker_id', how='left', suffixes=('', '_broker'))
        
        # KPI 1: Price per Square Foot
        st.markdown("### 1️⃣ Price per Square Foot")
        col1, col2 = st.columns(2)
        
        with col1:
            if 'final_price' in df_kpi.columns and 'area_sqft' in df_kpi.columns:
                df_kpi['price_per_sqft'] = df_kpi['final_price'] / df_kpi['area_sqft']
                avg_price_sqft = df_kpi['price_per_sqft'].mean()
                median_price_sqft = df_kpi['price_per_sqft'].median()
                
                st.metric("Average Price/Sqft", f"₹{avg_price_sqft:,.2f}")
                st.metric("Median Price/Sqft", f"₹{median_price_sqft:,.2f}")
                
                # Top cities by price/sqft
                if 'city_prop' in df_kpi.columns:
                    city_price = df_kpi.groupby('city_prop')['price_per_sqft'].mean().sort_values(ascending=False).head(10)
                    fig = px.bar(x=city_price.index, y=city_price.values,
                                title='Top 10 Cities by Avg Price/Sqft',
                                labels={'x': 'City', 'y': 'Price per Sqft (₹)'},
                                color=city_price.values,
                                color_continuous_scale='Viridis')
                    st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'price_per_sqft' in df_kpi.columns and 'property_type' in df_kpi.columns:
                type_price = df_kpi.groupby('property_type')['price_per_sqft'].mean().sort_values(ascending=False)
                fig = px.bar(x=type_price.index, y=type_price.values,
                            title='Avg Price/Sqft by Property Type',
                            labels={'x': 'Property Type', 'y': 'Price per Sqft (₹)'},
                            color=type_price.values,
                            color_continuous_scale='Blues')
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # KPI 2: Broker Success Rate
        st.markdown("### 2️⃣ Broker Success Rate")
        col1, col2 = st.columns(2)
        
        with col1:
            if 'status' in df_kpi.columns and 'broker_id' in df_kpi.columns:
                broker_stats = df_kpi.groupby('broker_id').agg({
                    'deal_id': 'count',
                    'status': lambda x: (x == 'Closed').sum()
                }).reset_index()
                broker_stats.columns = ['broker_id', 'total_deals', 'closed_deals']
                broker_stats['success_rate'] = (broker_stats['closed_deals'] / broker_stats['total_deals'] * 100)
                
                avg_success_rate = broker_stats['success_rate'].mean()
                st.metric("Average Broker Success Rate", f"{avg_success_rate:.1f}%")
                
                # Top brokers
                top_brokers = broker_stats.nlargest(10, 'success_rate')
                fig = px.bar(top_brokers, x='broker_id', y='success_rate',
                            title='Top 10 Brokers by Success Rate',
                            labels={'broker_id': 'Broker ID', 'success_rate': 'Success Rate (%)'},
                            color='success_rate',
                            color_continuous_scale='Greens')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'success_rate' in broker_stats.columns:
                fig = px.histogram(broker_stats, x='success_rate',
                                 title='Distribution of Broker Success Rates',
                                 labels={'success_rate': 'Success Rate (%)', 'count': 'Number of Brokers'},
                                 nbins=20,
                                 color_discrete_sequence=['#2ecc71'])
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # KPI 3: Customer Income Segments
        st.markdown("### 3️⃣ Customer Income Segments")
        col1, col2 = st.columns(2)
        
        with col1:
            if 'segment' in df_kpi.columns:
                segment_counts = df_kpi['segment'].value_counts()
                fig = px.pie(values=segment_counts.values, names=segment_counts.index,
                            title='Customer Distribution by Segment',
                            hole=0.4,
                            color_discrete_sequence=px.colors.sequential.RdBu)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'annual_income' in df_kpi.columns and 'segment' in df_kpi.columns:
                fig = px.box(df_kpi, x='segment', y='annual_income',
                            title='Income Distribution by Segment',
                            labels={'segment': 'Customer Segment', 'annual_income': 'Annual Income (₹)'},
                            color='segment')
                st.plotly_chart(fig, use_container_width=True)
        
        # Income statistics by segment
        if 'annual_income' in df_kpi.columns and 'segment' in df_kpi.columns:
            income_stats = df_kpi.groupby('segment')['annual_income'].agg(['mean', 'median', 'count']).reset_index()
            income_stats.columns = ['Segment', 'Avg Income', 'Median Income', 'Count']
            st.dataframe(income_stats.style.format({
                'Avg Income': '₹{:,.0f}',
                'Median Income': '₹{:,.0f}',
                'Count': '{:,}'
            }), use_container_width=True)
        
        st.markdown("---")
        
        # KPI 4: Deal Closure Probability
        st.markdown("### 4️⃣ Deal Closure Probability")
        
        if 'status' in df_kpi.columns:
            total_deals = len(df_kpi)
            closed_deals = len(df_kpi[df_kpi['status'] == 'Closed'])
            pending_deals = len(df_kpi[df_kpi['status'] == 'Pending'])
            cancelled_deals = len(df_kpi[df_kpi['status'] == 'Cancelled'])
            
            closure_rate = (closed_deals / total_deals * 100) if total_deals > 0 else 0
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Deals", f"{total_deals:,}")
            with col2:
                st.metric("Closed Deals", f"{closed_deals:,}", f"{closure_rate:.1f}%")
            with col3:
                st.metric("Pending Deals", f"{pending_deals:,}")
            with col4:
                st.metric("Cancelled Deals", f"{cancelled_deals:,}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Status distribution
                status_counts = df_kpi['status'].value_counts()
                fig = px.pie(values=status_counts.values, names=status_counts.index,
                            title='Deal Status Distribution',
                            hole=0.4,
                            color_discrete_sequence=px.colors.sequential.Teal)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Closure rate by property type
                if 'property_type' in df_kpi.columns:
                    closure_by_type = df_kpi.groupby('property_type').apply(
                        lambda x: (x['status'] == 'Closed').sum() / len(x) * 100
                    ).sort_values(ascending=False)
                    
                    fig = px.bar(x=closure_by_type.index, y=closure_by_type.values,
                                title='Closure Rate by Property Type',
                                labels={'x': 'Property Type', 'y': 'Closure Rate (%)'},
                                color=closure_by_type.values,
                                color_continuous_scale='Blues')
                    st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # KPI 5: Amenity Co-occurrence Patterns
        st.markdown("### 5️⃣ Amenity Co-occurrence Patterns")
        
        if 'PropertyDetails' in dataframes:
            prop_details = dataframes['PropertyDetails'].copy()
            
            # Check for amenity columns
            amenity_cols = [col for col in prop_details.columns if 'amenity' in col.lower() or 
                          col in ['parking', 'gym', 'pool', 'garden', 'security', 'elevator']]
            
            if amenity_cols:
                st.info(f"Found {len(amenity_cols)} amenity features")
                
                # Amenity frequency
                amenity_counts = {}
                for col in amenity_cols:
                    if prop_details[col].dtype == 'bool' or prop_details[col].dtype == 'object':
                        amenity_counts[col] = prop_details[col].sum() if prop_details[col].dtype == 'bool' else len(prop_details[prop_details[col] == 'Yes'])
                
                if amenity_counts:
                    amenity_df = pd.DataFrame(list(amenity_counts.items()), columns=['Amenity', 'Count'])
                    amenity_df = amenity_df.sort_values('Count', ascending=False)
                    
                    fig = px.bar(amenity_df, x='Amenity', y='Count',
                                title='Amenity Frequency',
                                labels={'Amenity': 'Amenity Type', 'Count': 'Number of Properties'},
                                color='Count',
                                color_continuous_scale='Purples')
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Amenity data not available in standard format. Showing property features instead.")
                
                # Show property condition and other features
                if 'condition' in prop_details.columns:
                    condition_counts = prop_details['condition'].value_counts()
                    fig = px.pie(values=condition_counts.values, names=condition_counts.index,
                                title='Property Condition Distribution',
                                hole=0.4)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Show correlation with price if available
                if 'property_id' in prop_details.columns and 'final_price' in df_kpi.columns:
                    df_amenity = df_kpi.merge(prop_details, on='property_id', how='left')
                    
                    if 'school_score' in df_amenity.columns and 'walk_score' in df_amenity.columns:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            fig = px.scatter(df_amenity, x='school_score', y='final_price',
                                           title='School Score vs Property Price',
                                           labels={'school_score': 'School Score', 'final_price': 'Final Price (₹)'},
                                           opacity=0.5)
                            st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            fig = px.scatter(df_amenity, x='walk_score', y='final_price',
                                           title='Walk Score vs Property Price',
                                           labels={'walk_score': 'Walk Score', 'final_price': 'Final Price (₹)'},
                                           opacity=0.5)
                            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("📊 Regression Model Comparison")
        comparison_df = re_models.get_model_comparison()
        
        # Display comparison table
        st.dataframe(comparison_df.style.format({
            'R² Score': '{:.4f}',
            'RMSE': '₹{:,.2f}',
            'MAPE': '{:.2%}',
            'Accuracy %': '{:.2f}%'
        }), use_container_width=True)
        
        # Visualize comparison
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(comparison_df, x='Model', y='R² Score',
                        title='R² Score Comparison',
                        color='R² Score',
                        color_continuous_scale='Blues')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(comparison_df, x='Model', y='MAPE',
                        title='MAPE Comparison (Lower is Better)',
                        color='MAPE',
                        color_continuous_scale='Reds_r')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("💰 Price Prediction Tool")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            area_sqft = st.number_input("Area (sqft)", min_value=500, max_value=10000, value=1500)
            bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10, value=3)
            bathrooms = st.number_input("Bathrooms", min_value=1, max_value=10, value=2)
        
        with col2:
            property_age = st.number_input("Property Age (years)", min_value=0, max_value=100, value=5)
            hoa_fee = st.number_input("HOA Fee", min_value=0, max_value=100000, value=5000)
            school_score = st.slider("School Score", 0, 100, 75)
        
        with col3:
            walk_score = st.slider("Walk Score", 0, 100, 70)
            experience_years = st.number_input("Broker Experience (years)", min_value=0, max_value=50, value=10)
            rating = st.slider("Broker Rating", 0.0, 5.0, 4.0, 0.1)
        
        offer_price = st.number_input("Offer Price", min_value=100000, max_value=50000000, value=5000000)
        loan_rate = st.slider("Loan Rate (%)", 5.0, 15.0, 9.5, 0.1)
        
        model_choice = st.selectbox("Select Model", 
                                   ["Simple Regression", "Multiple Regression", "Random Forest"])
        
        if st.button("Predict Price", type="primary"):
            features = {
                'area_sqft': area_sqft,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'property_age_at_deal': property_age,
                'experience_years': experience_years,
                'rating': rating,
                'hoa_fee': hoa_fee,
                'school_score': school_score,
                'walk_score': walk_score,
                'offer_price': offer_price,
                'loan_rate': loan_rate
            }
            
            model_map = {
                "Simple Regression": "simple_regression",
                "Multiple Regression": "multiple_regression",
                "Random Forest": "random_forest_regression"
            }
            
            try:
                predicted_price = re_models.predict_price(model_map[model_choice], features)
                
                st.success(f"### Predicted Price: ₹{predicted_price:,.2f}")
                
                # Show price per sqft
                price_per_sqft = predicted_price / area_sqft
                st.info(f"Price per sqft: ₹{price_per_sqft:,.2f}")
                
            except Exception as e:
                st.error(f"Prediction error: {e}")
    
    with tab4:
        st.subheader("📈 Feature Importance Analysis")
        
        model_select = st.selectbox("Select Model for Feature Importance",
                                   ["Multiple Regression", "Random Forest Regression"])
        
        if model_select == "Multiple Regression" and 'multiple_regression' in results:
            importance_df = results['multiple_regression']['feature_importance']
            
            fig = px.bar(importance_df.head(10), 
                        x='coefficient', 
                        y='feature',
                        orientation='h',
                        title='Top 10 Feature Coefficients (Multiple Regression)',
                        labels={'coefficient': 'Coefficient Value', 'feature': 'Feature'},
                        color='coefficient',
                        color_continuous_scale='RdBu')
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(importance_df, use_container_width=True)
        
        elif model_select == "Random Forest Regression" and 'random_forest_regression' in results:
            importance_df = results['random_forest_regression']['feature_importance']
            
            fig = px.bar(importance_df.head(10), 
                        x='importance', 
                        y='feature',
                        orientation='h',
                        title='Top 10 Feature Importances (Random Forest)',
                        labels={'importance': 'Importance Score', 'feature': 'Feature'},
                        color='importance',
                        color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(importance_df, use_container_width=True)
    
    with tab5:
        st.subheader("🎯 Deal Status Prediction")
        
        if 'status_classifier' in results:
            # Show classifier metrics
            clf_results = results['status_classifier']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Overall Accuracy", f"{clf_results['accuracy']:.2%}")
            with col2:
                st.metric("Number of Classes", len(clf_results['classes']))
            with col3:
                st.metric("Test Samples", len(clf_results['y_test']))
            
            # Confusion Matrix
            st.subheader("Confusion Matrix")
            cm = clf_results['confusion_matrix']
            
            fig = px.imshow(cm,
                           labels=dict(x="Predicted", y="Actual", color="Count"),
                           x=clf_results['classes'],
                           y=clf_results['classes'],
                           title="Confusion Matrix",
                           color_continuous_scale='Blues',
                           text_auto=True)
            st.plotly_chart(fig, use_container_width=True)
            
            # Classification Report
            st.subheader("Classification Report")
            report_df = pd.DataFrame(clf_results['classification_report']).transpose()
            st.dataframe(report_df.style.format("{:.2f}"), use_container_width=True)
            
            # Feature Importance for Classifier
            st.subheader("Feature Importance for Status Prediction")
            importance_df = clf_results['feature_importance']
            
            fig = px.bar(importance_df.head(10), 
                        x='importance', 
                        y='feature',
                        orientation='h',
                        title='Top 10 Features for Deal Status Prediction',
                        color='importance',
                        color_continuous_scale='Greens')
            st.plotly_chart(fig, use_container_width=True)
            
            # Interactive Prediction Tool
            st.subheader("Predict Deal Status")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                area_sqft_s = st.number_input("Area (sqft) ", min_value=500, max_value=10000, value=1500, key='status_area')
                bedrooms_s = st.number_input("Bedrooms ", min_value=1, max_value=10, value=3, key='status_bed')
                bathrooms_s = st.number_input("Bathrooms ", min_value=1, max_value=10, value=2, key='status_bath')
            
            with col2:
                property_age_s = st.number_input("Property Age ", min_value=0, max_value=100, value=5, key='status_age')
                hoa_fee_s = st.number_input("HOA Fee ", min_value=0, max_value=100000, value=5000, key='status_hoa')
                school_score_s = st.slider("School Score ", 0, 100, 75, key='status_school')
            
            with col3:
                walk_score_s = st.slider("Walk Score ", 0, 100, 70, key='status_walk')
                experience_years_s = st.number_input("Broker Experience ", min_value=0, max_value=50, value=10, key='status_exp')
                rating_s = st.slider("Broker Rating ", 0.0, 5.0, 4.0, 0.1, key='status_rating')
            
            offer_price_s = st.number_input("Offer Price ", min_value=100000, max_value=50000000, value=5000000, key='status_offer')
            loan_rate_s = st.slider("Loan Rate (%) ", 5.0, 15.0, 9.5, 0.1, key='status_loan')
            
            if st.button("Predict Deal Status", type="primary"):
                features_s = {
                    'area_sqft': area_sqft_s,
                    'bedrooms': bedrooms_s,
                    'bathrooms': bathrooms_s,
                    'property_age_at_deal': property_age_s,
                    'experience_years': experience_years_s,
                    'rating': rating_s,
                    'hoa_fee': hoa_fee_s,
                    'school_score': school_score_s,
                    'walk_score': walk_score_s,
                    'offer_price': offer_price_s,
                    'loan_rate': loan_rate_s
                }
                
                try:
                    prediction = re_models.predict_status(features_s)
                    
                    st.success(f"### Predicted Status: {prediction['predicted_status']}")
                    
                    # Show probabilities
                    st.subheader("Prediction Probabilities")
                    prob_df = pd.DataFrame(list(prediction['probabilities'].items()), 
                                          columns=['Status', 'Probability'])
                    prob_df['Probability'] = prob_df['Probability'] * 100
                    
                    fig = px.bar(prob_df, x='Status', y='Probability',
                                title='Prediction Confidence',
                                color='Probability',
                                color_continuous_scale='Blues')
                    st.plotly_chart(fig, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"Prediction error: {e}")
    
    with tab6:
        st.subheader("📉 Model Performance Visualization")
        
        model_perf = st.selectbox("Select Model", 
                                 ["Simple Regression", "Multiple Regression", "Random Forest Regression"])
        
        model_key_map = {
            "Simple Regression": "simple_regression",
            "Multiple Regression": "multiple_regression",
            "Random Forest Regression": "random_forest_regression"
        }
        
        model_key = model_key_map[model_perf]
        
        if model_key in results:
            result = results[model_key]
            
            # Actual vs Predicted
            st.subheader("Actual vs Predicted Prices")
            
            comparison_df = pd.DataFrame({
                'Actual': result['y_test'].values[:100],
                'Predicted': result['y_pred'][:100]
            })
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=comparison_df['Actual'], 
                                    mode='lines+markers',
                                    name='Actual Price',
                                    line=dict(color='blue')))
            fig.add_trace(go.Scatter(y=comparison_df['Predicted'], 
                                    mode='lines+markers',
                                    name='Predicted Price',
                                    line=dict(color='red')))
            fig.update_layout(title='Actual vs Predicted Prices (First 100 Samples)',
                            xaxis_title='Sample Index',
                            yaxis_title='Price (₹)')
            st.plotly_chart(fig, use_container_width=True)
            
            # Scatter Plot
            st.subheader("Prediction Scatter Plot")
            scatter_df = pd.DataFrame({
                'Actual': result['y_test'].values,
                'Predicted': result['y_pred']
            })
            
            fig = px.scatter(scatter_df, x='Actual', y='Predicted',
                           title='Actual vs Predicted Scatter Plot',
                           labels={'Actual': 'Actual Price (₹)', 'Predicted': 'Predicted Price (₹)'},
                           trendline='ols')
            
            # Add perfect prediction line
            min_val = min(scatter_df['Actual'].min(), scatter_df['Predicted'].min())
            max_val = max(scatter_df['Actual'].max(), scatter_df['Predicted'].max())
            fig.add_trace(go.Scatter(x=[min_val, max_val], y=[min_val, max_val],
                                    mode='lines',
                                    name='Perfect Prediction',
                                    line=dict(color='green', dash='dash')))
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Residual Plot
            st.subheader("Residual Analysis")
            residuals = result['y_test'].values - result['y_pred']
            
            fig = px.scatter(x=result['y_pred'], y=residuals,
                           title='Residual Plot',
                           labels={'x': 'Predicted Price (₹)', 'y': 'Residual (Actual - Predicted)'},
                           color=residuals,
                           color_continuous_scale='RdBu')
            fig.add_hline(y=0, line_dash="dash", line_color="red")
            st.plotly_chart(fig, use_container_width=True)
            
            # Distribution of Residuals
            fig = px.histogram(x=residuals, nbins=50,
                             title='Distribution of Residuals',
                             labels={'x': 'Residual Value'},
                             color_discrete_sequence=['#3498db'])
            st.plotly_chart(fig, use_container_width=True)

def prepare_transformed_data(dataframes):
    """Prepare and transform data for modeling"""
    try:
        # Merge all dataframes
        deals = dataframes['Deals'].copy()
        customers = dataframes['Customers'].copy()
        brokers = dataframes['Brokers'].copy()
        properties = dataframes['Properties'].copy()
        prop_details = dataframes['PropertyDetails'].copy()
        
        # Merge datasets
        df = deals.merge(customers, on='customer_id', how='left', suffixes=('', '_cust'))
        df = df.merge(brokers, on='broker_id', how='left', suffixes=('', '_broker'))
        df = df.merge(properties, on='property_id', how='left', suffixes=('', '_prop'))
        df = df.merge(prop_details, on='property_id', how='left', suffixes=('', '_detail'))
        
        # Calculate property age
        if 'deal_date' in df.columns and 'year_built' in df.columns:
            df['deal_date'] = pd.to_datetime(df['deal_date'], errors='coerce')
            df['property_age_at_deal'] = df['deal_date'].dt.year - df['year_built']
        
        # Select only numeric columns needed for modeling
        numeric_cols = ['area_sqft', 'bedrooms', 'bathrooms', 'property_age_at_deal',
                       'experience_years', 'rating', 'hoa_fee', 'school_score', 
                       'walk_score', 'offer_price', 'loan_rate', 'final_price', 'status']
        
        # Keep only available columns
        available_cols = [col for col in numeric_cols if col in df.columns]
        df_transformed = df[available_cols].copy()
        
        return df_transformed
        
    except Exception as e:
        st.error(f"Error preparing data: {e}")
        return None

if __name__ == "__main__":
    main()
