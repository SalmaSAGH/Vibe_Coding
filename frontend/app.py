# frontend/app.py
import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List

# Configuration
API_BASE_URL = "http://localhost:8000/api"

# Page configuration
st.set_page_config(
    page_title="Smart Agriculture Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2e7d32;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #4caf50;
    }
    .alert-critical {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .alert-warning {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .recommendation-box {
        background-color: #e8f5e9;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #4caf50;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Helper Functions
def get_sensor_list() -> List[str]:
    """Fetch list of all sensors"""
    try:
        response = requests.get(f"{API_BASE_URL}/sensors/list", timeout=5)
        response.raise_for_status()
        data = response.json()
        return [sensor['sensor_id'] for sensor in data['sensors']]
    except Exception as e:
        st.error(f"Error fetching sensor list: {e}")
        return []

def get_current_data(sensor_id: str) -> Dict:
    """Fetch current sensor data"""
    try:
        response = requests.get(f"{API_BASE_URL}/sensors/current/{sensor_id}", timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching sensor data: {e}")
        return None

def get_recommendations(sensor_id: str) -> Dict:
    """Fetch recommendations"""
    try:
        response = requests.get(f"{API_BASE_URL}/recommendations/{sensor_id}", timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching recommendations: {e}")
        return None

def get_sensor_history(sensor_id: str, limit: int = 50) -> List[Dict]:
    """Fetch historical data"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/sensors/history/{sensor_id}",
            params={"limit": limit},
            timeout=5
        )
        response.raise_for_status()
        return response.json()['readings']
    except Exception as e:
        st.error(f"Error fetching history: {e}")
        return []

def post_sensor_data(sensor_id: str, soil_moisture: float, 
                    temperature: float, humidity: float) -> bool:
    """Post new sensor data"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/sensors/data",
            json={
                "sensor_id": sensor_id,
                "soil_moisture": soil_moisture,
                "temperature": temperature,
                "humidity": humidity
            },
            timeout=5
        )
        response.raise_for_status()
        return True
    except Exception as e:
        st.error(f"Error posting data: {e}")
        return False

# Visualization Functions
def create_gauge_chart(value: float, title: str, max_value: float = 100,
                       optimal_range: tuple = None) -> go.Figure:
    """Create a gauge chart for sensor values"""
    
    # Determine color based on value
    if optimal_range:
        if optimal_range[0] <= value <= optimal_range[1]:
            color = "green"
        elif value < optimal_range[0] * 0.7 or value > optimal_range[1] * 1.2:
            color = "red"
        else:
            color = "orange"
    else:
        color = "blue"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 20}},
        gauge={
            'axis': {'range': [None, max_value], 'tickwidth': 1},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, max_value * 0.3], 'color': '#ffcccc'},
                {'range': [max_value * 0.3, max_value * 0.7], 'color': '#ffffcc'},
                {'range': [max_value * 0.7, max_value], 'color': '#ccffcc'}
            ],
        }
    ))
    
    fig.update_layout(height=250, margin=dict(l=10, r=10, t=50, b=10))
    return fig

def create_history_chart(history: List[Dict]) -> go.Figure:
    """Create time series chart for historical data"""
    if not history:
        return go.Figure()
    
    df = pd.DataFrame(history)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    
    fig = go.Figure()
    
    # Soil Moisture
    fig.add_trace(go.Scatter(
        x=df['timestamp'], y=df['soil_moisture'],
        name='Soil Moisture (%)',
        line=dict(color='#8b4513', width=2),
        mode='lines+markers'
    ))
    
    # Temperature (scaled)
    fig.add_trace(go.Scatter(
        x=df['timestamp'], y=df['temperature'],
        name='Temperature (°C)',
        line=dict(color='#ff6b6b', width=2),
        mode='lines+markers',
        yaxis='y2'
    ))
    
    # Humidity
    fig.add_trace(go.Scatter(
        x=df['timestamp'], y=df['humidity'],
        name='Humidity (%)',
        line=dict(color='#4ecdc4', width=2),
        mode='lines+markers'
    ))
    
    fig.update_layout(
        title='Historical Sensor Data',
        xaxis_title='Time',
        yaxis_title='Moisture & Humidity (%)',
        yaxis2=dict(
            title='Temperature (°C)',
            overlaying='y',
            side='right',
            range=[0, 50]
        ),
        hovermode='x unified',
        height=400,
        showlegend=True,
        legend=dict(x=0.01, y=0.99)
    )
    
    return fig

# Main App Layout
def main():
    # Header
    st.markdown('<div class="main-header">🌱 Smart Agriculture Dashboard</div>', 
                unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/150x150.png?text=Farm+Logo", 
                use_container_width=True)
        st.title("Navigation")
        
        page = st.radio(
            "Select Page:",
            ["📊 Dashboard", "📈 Historical Data", "➕ Add Sensor Data", "ℹ️ About"]
        )
        
        st.divider()
        
        # Sensor Selection
        st.subheader("Select Sensor")
        sensors = get_sensor_list()
        
        if not sensors:
            st.warning("No sensors found. Add sensor data first.")
            selected_sensor = st.text_input("Enter Sensor ID:", "SENSOR_001")
        else:
            selected_sensor = st.selectbox("Sensor ID:", sensors)
        
        st.divider()
        
        # Auto-refresh
        auto_refresh = st.checkbox("Auto-refresh (30s)", value=False)
        if auto_refresh:
            st.rerun()
    
    # Page Routing
    if page == "📊 Dashboard":
        show_dashboard(selected_sensor)
    elif page == "📈 Historical Data":
        show_historical_data(selected_sensor)
    elif page == "➕ Add Sensor Data":
        show_add_data_page()
    else:
        show_about_page()

def show_dashboard(sensor_id: str):
    """Main dashboard view"""
    st.header(f"Dashboard: {sensor_id}")
    
    # Fetch current data
    current_data = get_current_data(sensor_id)
    
    if not current_data:
        st.warning(f"No data available for sensor {sensor_id}")
        return
    
    # Display current readings
    st.subheader("Current Readings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.plotly_chart(
            create_gauge_chart(
                current_data['soil_moisture'],
                "Soil Moisture",
                100,
                (60, 80)
            ),
            use_container_width=True
        )
    
    with col2:
        st.plotly_chart(
            create_gauge_chart(
                current_data['temperature'],
                "Temperature",
                50,
                (15, 30)
            ),
            use_container_width=True
        )
    
    with col3:
        st.plotly_chart(
            create_gauge_chart(
                current_data['humidity'],
                "Humidity",
                100,
                (50, 70)
            ),
            use_container_width=True
        )
    
    # Timestamp
    timestamp = current_data.get('timestamp', 'Unknown')
    st.caption(f"Last updated: {timestamp}")
    
    st.divider()
    
    # Fetch and display recommendations
    st.subheader("🤖 AI Recommendations")
    
    recommendations = get_recommendations(sensor_id)
    
    if not recommendations:
        st.error("Unable to generate recommendations")
        return
    
    # Alerts
    if recommendations.get('alerts'):
        st.subheader("⚠️ Alerts")
        for alert in recommendations['alerts']:
            if "CRITICAL" in alert or "DROUGHT" in alert:
                st.markdown(f'<div class="alert-critical">{alert}</div>', 
                           unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="alert-warning">{alert}</div>', 
                           unsafe_allow_html=True)
    
    # Irrigation Recommendation
    irrigation = recommendations.get('irrigation', {})
    st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
    st.subheader("💧 Irrigation Recommendation")
    
    action = irrigation.get('action', 'Unknown')
    amount = irrigation.get('amount_ml', 0)
    priority = irrigation.get('priority', 'medium')
    explanation = irrigation.get('explanation', 'No explanation available')
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Action", action.replace('_', ' ').title())
    col2.metric("Amount", f"{amount} mL")
    col3.metric("Priority", priority.upper())
    
    st.info(explanation)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Fertilization Recommendation
    fertilization = recommendations.get('fertilization', {})
    st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
    st.subheader("🌿 Fertilization Recommendation")
    
    needed = fertilization.get('needed', False)
    fert_type = fertilization.get('type', 'N/A')
    amount_kg = fertilization.get('amount_kg', 0)
    explanation = fertilization.get('explanation', 'No explanation available')
    
    if needed:
        col1, col2 = st.columns(2)
        col1.metric("Fertilizer Type", fert_type)
        col2.metric("Amount", f"{amount_kg} kg")
        st.success(explanation)
    else:
        st.info(explanation)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_historical_data(sensor_id: str):
    """Historical data view with charts"""
    st.header(f"Historical Data: {sensor_id}")
    
    # Time range selector
    col1, col2 = st.columns(2)
    with col1:
        limit = st.slider("Number of readings:", 10, 200, 50)
    with col2:
        chart_type = st.selectbox("Chart Type:", ["Line Chart", "Area Chart", "Bar Chart"])
    
    # Fetch history
    history = get_sensor_history(sensor_id, limit)
    
    if not history:
        st.warning("No historical data available")
        return
    
    # Display chart
    st.plotly_chart(create_history_chart(history), use_container_width=True)
    
    # Data table
    st.subheader("Raw Data")
    df = pd.DataFrame(history)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp', ascending=False)
    
    st.dataframe(
        df[['timestamp', 'soil_moisture', 'temperature', 'humidity']],
        use_container_width=True,
        hide_index=True
    )
    
    # Statistics
    st.subheader("Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Avg Soil Moisture", f"{df['soil_moisture'].mean():.1f}%")
        st.metric("Min", f"{df['soil_moisture'].min():.1f}%")
        st.metric("Max", f"{df['soil_moisture'].max():.1f}%")
    
    with col2:
        st.metric("Avg Temperature", f"{df['temperature'].mean():.1f}°C")
        st.metric("Min", f"{df['temperature'].min():.1f}°C")
        st.metric("Max", f"{df['temperature'].max():.1f}°C")
    
    with col3:
        st.metric("Avg Humidity", f"{df['humidity'].mean():.1f}%")
        st.metric("Min", f"{df['humidity'].min():.1f}%")
        st.metric("Max", f"{df['humidity'].max():.1f}%")

def show_add_data_page():
    """Form to manually add sensor data"""
    st.header("➕ Add Sensor Data")
    
    with st.form("sensor_data_form"):
        sensor_id = st.text_input("Sensor ID:", "SENSOR_001")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            soil_moisture = st.number_input(
                "Soil Moisture (%):", 
                min_value=0.0, 
                max_value=100.0, 
                value=50.0,
                step=0.1
            )
        
        with col2:
            temperature = st.number_input(
                "Temperature (°C):", 
                min_value=-50.0, 
                max_value=60.0, 
                value=25.0,
                step=0.1
            )
        
        with col3:
            humidity = st.number_input(
                "Humidity (%):", 
                min_value=0.0, 
                max_value=100.0, 
                value=60.0,
                step=0.1
            )
        
        submitted = st.form_submit_button("Submit Data")
        
        if submitted:
            success = post_sensor_data(sensor_id, soil_moisture, temperature, humidity)
            if success:
                st.success("✅ Data submitted successfully!")
                st.balloons()
            else:
                st.error("❌ Failed to submit data")

def show_about_page():
    """About page with system information"""
    st.header("ℹ️ About Smart Agriculture System")
    
    st.markdown("""
    ### 🌾 System Overview
    
    The Smart Agriculture Decision Support System helps farmers make informed decisions 
    about irrigation and fertilization based on real-time sensor data and AI-powered recommendations.
    
    ### 📊 Features
    
    - **Real-time Monitoring**: Track soil moisture, temperature, and humidity
    - **AI Recommendations**: Get actionable advice for irrigation and fertilization
    - **Historical Analysis**: Review trends and patterns over time
    - **Alert System**: Receive warnings about critical conditions
    
    ### 🔬 Technology Stack
    
    - **Backend**: Python + FastAPI
    - **Frontend**: Streamlit
    - **Database**: SQLite
    - **Charts**: Plotly
    
    ### 📖 How to Use
    
    1. Select a sensor from the sidebar
    2. View current readings and recommendations on the Dashboard
    3. Analyze historical data to identify trends
    4. Manually add sensor data if needed
    
    ### ⚙️ Configuration
    
    - **Optimal Soil Moisture**: 60-80%
    - **Optimal Temperature**: 15-30°C
    - **Target Crop**: Tomatoes (configurable)
    
    ### 📞 Support
    
    For support, contact: support@smartagri.example.com
    
    ---
    
    *Version 1.0.0 - Built with ❤️ for farmers*
    """)

if __name__ == "__main__":
    main()