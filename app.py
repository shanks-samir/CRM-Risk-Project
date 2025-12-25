import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="CRM Risk Engine",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS for that "Corporate" look
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stMetric { background-color: white; padding: 15px; border-radius: 5px; border: 1px solid #ddd; }
    h1, h2, h3 { color: #2c3e50; font-family: 'Helvetica', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA FUNCTIONS ---
def load_market_data():
    """Fetches the latest market snapshot for all assets."""
    conn = sqlite3.connect('data/crm_risk.db')
    query = """
    SELECT ticker, price, high, low, asset_class, consensus_mech 
    FROM market_data 
    GROUP BY ticker 
    ORDER BY timestamp DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def load_audit_log():
    """Fetches the trade audit trail."""
    conn = sqlite3.connect('data/crm_risk.db')
    df = pd.read_sql("SELECT * FROM trade_audit ORDER BY execution_time DESC", conn)
    conn.close()
    return df

# --- 3. DASHBOARD LAYOUT ---

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🛡️ Institutional Risk Dashboard")
with col2:
    # Placeholder Logo
    st.image("https://cdn-icons-png.flaticon.com/512/2702/2702069.png", width=50) 

st.divider()

# KPI Section
st.subheader("1. Portfolio Risk Overview")
market_df = load_market_data()

if not market_df.empty:
    cols = st.columns(len(market_df))
    for index, (i, row) in enumerate(market_df.iterrows()):
        with cols[index]:
            st.metric(
                label=f"{row['ticker']} ({row['asset_class']})",
                value=f"${row['price']:,.2f}",
                delta=f"Range: ${row['low']} - ${row['high']}"
            )
else:
    st.warning("No market data found. Run 'python -m modules.pipeline' first.")

# Tabbed View for Details
tab1, tab2 = st.tabs(["📊 Market Conformity Audit", "🌱 ESG & Tech Risk"])

with tab1:
    st.header("Trade Conformity Log")
    st.markdown("Real-time monitoring of trade execution against Fair Market Value (FMV).")
    
    audit_df = load_audit_log()
    if not audit_df.empty:
        # Styling the dataframe: Highlight "FAIL" in red
        def highlight_status(val):
            color = '#ffcdd2' if val == 'FAIL' else '#c8e6c9'
            return f'background-color: {color}'

        st.dataframe(
            audit_df.style.map(highlight_status, subset=['conformity_status']),
            use_container_width=True
        )
    else:
        st.info("No trades logged yet. Run the pipeline to generate mock trades.")

with tab2:
    st.header("ESG Impact Analysis (Radial View)")
    st.markdown("Visualizing energy intensity per asset consensus mechanism.")
    
    if not market_df.empty:
        # 1. Prepare Data
        esg_data = market_df[['ticker', 'consensus_mech']].copy()
        
        # Mapping: Higher score = Higher Energy Intensity
        esg_map = {'PoW': 80, 'PoS': 10, 'N/A': 5} 
        esg_data['Energy_Score'] = esg_data['consensus_mech'].map(esg_map)
        
        # 2. Setup Matplotlib Radial (Polar) Chart
        N = len(esg_data)
        theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
        radii = esg_data['Energy_Score']
        width = 2 * np.pi / N
        colors = plt.cm.viridis(radii / 100)

        # CHANGE 1: Reduced figsize from (6, 6) to (2.5, 2.5)
        fig, ax = plt.subplots(figsize=(2.5, 2.5), subplot_kw={'projection': 'polar'})
        
        # Plot bars
        bars = ax.bar(theta, radii, width=width, bottom=0.0, color=colors, alpha=0.7)

        # 3. Customizing for the smaller size
        ax.set_xticks(theta)
        
        # CHANGE 2: Smaller font sizes so they fit the small chart
        ax.set_xticklabels(esg_data['ticker'], fontweight='bold', fontsize=7)
        ax.set_yticks([20, 50, 80])
        ax.set_yticklabels(["Low", "Med", "High"], color="gray", fontsize=5)
        
        # Remove the outer frame
        ax.spines['polar'].set_visible(False) 
        
        # Adjust layout to prevent clipping labels
        plt.tight_layout()

        # Display in Streamlit (use_container_width=False keeps it true to size)
        st.pyplot(fig, use_container_width=False)
        
        st.caption("Figure 1: Radial representation of consensus energy cost.")