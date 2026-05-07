import pandas as pd
import plotly.express as px
import streamlit as st
from utils import predict_time, recommend_factories, ai_insights, generate_report_dataframe

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Smart Factory Dashboard", layout="wide")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
/* ======== APP BACKGROUND ======== */
.stApp {
    background: linear-gradient(135deg, #eef2f3, #dfe9f3);
    color: #1e293b;
}

/* ======== SIDEBAR STYLING ======== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e3a8a, #3b82f6);
}

/* Sidebar text and general elements */
[data-testid="stSidebar"] * {
    color: #1e293b !important;
    font-weight: 600;
}

/* Sidebar labels */
[data-testid="stSidebar"] label {
    color: #facc15 !important;
    font-weight: bold;
}

/* Dropdown boxes and input fields */
[data-baseweb="select"] > div {
    background-color: #f1f5f9 !important;
    color: #1e293b !important;
    border-radius: 8px;
    font-weight: 600;
}

/* Dropdown options */
[data-baseweb="popover"] div {
    color: #1e293b !important;
}

/* Sliders */
.stSlider > div[data-baseweb="slider"] {
    color: #f8fafc !important;
}

/* Hover glow for dropdowns and sliders */
[data-baseweb="select"] > div:hover,
.stSlider > div[data-baseweb="slider"]:hover {
    box-shadow: 0 0 10px #facc15;
    transition: box-shadow 0.3s ease-in-out;
}

/* Highlight selected dropdown option */
[data-baseweb="popover"] div:hover {
    background-color: #e0f2fe !important;
    color: #1e3a8a !important;
}

/* ======== METRIC CARDS ======== */
div[data-testid="metric-container"] {
    background: white;
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
}

/* ======== BUTTONS ======== */
.stButton>button {
    background: linear-gradient(90deg, #2563eb, #1d4ed8);
    color: white;
    border-radius: 10px;
    font-weight: bold;
}

.stDownloadButton>button {
    background: linear-gradient(90deg, #16a34a, #15803d);
    color: white;
    border-radius: 10px;
}

/* ======== HEADINGS ======== */
h1, h2, h3 {
    color: #1e293b;
}
</style>
""", unsafe_allow_html=True)

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data():
    df = pd.read_csv("clustered_data.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")
    df = df.dropna(subset=["Order Date", "Ship Date"])
    df["Lead Time"] = (df["Ship Date"] - df["Order Date"]).dt.days
    return df

df = load_data()

# ------------------ HEADER ------------------
st.title("📊 Nassau Decision Intelligence Dashboard")

# ------------------ SIDEBAR ------------------
st.sidebar.header("📌 Simulation")

product = st.sidebar.selectbox("Product", df["Product Name"].unique(), index=0)
region = st.sidebar.selectbox("Region", df["Region"].unique(), index=0)
ship_mode = st.sidebar.selectbox("Ship Mode", df["Ship Mode"].unique(), index=0)
sales = st.sidebar.slider("Sales", 100, 10000, 1000)
units = st.sidebar.slider("Units", 1, 50, 10)

# ------------------ MODEL OUTPUT ------------------
predicted_time = predict_time(product, region, ship_mode, sales, units)
results = recommend_factories(product, region, ship_mode, sales, units)

# ------------------ KPI ------------------
col1, col2, col3 = st.columns(3)
col1.metric("⏱ Lead Time", f"{predicted_time:.2f} days")
col2.metric("💰 Sales", f"${sales}")
col3.metric("📦 Units", units)

# ------------------ RECOMMENDATIONS ------------------
st.subheader("🏭 Smart Factory Recommendations")
cols = st.columns(2)
for i, r in enumerate(results):
    with cols[i % 2]:
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 15px;
        box-shadow: 0px 6px 18px rgba(0,0,0,0.08); margin-bottom: 20px;
        border-left: 6px solid {r['color']};">
            <h3>🏭 {r['factory']}</h3>
            <p>⏱ <b>Lead Time:</b> {r['time']} days</p>
            <p>💰 <b>Profit Score:</b> {r['profit']}</p>
            <p>⚠️ <b>Risk:</b> {r['risk']}</p>
            <p>📈 <b>Efficiency:</b> {r['efficiency']}%</p>
        </div>
        """, unsafe_allow_html=True)

# ------------------ AI INSIGHTS ------------------
st.subheader("🤖 AI Insights")
st.info(ai_insights(results))

# ------------------ FILTER DATA ------------------
filtered_df = df[
    (df["Product Name"] == product) &
    (df["Region"] == region) &
    (df["Ship Mode"] == ship_mode)
]

if filtered_df.empty:
    st.warning("⚠️ No data matches your selection. Try a different combination.")
    st.subheader("📊 Overall Dataset Summary")
    fig_overall = px.histogram(df, x="Lead Time", title="Overall Lead Time Distribution")
    st.plotly_chart(fig_overall, use_container_width=True)
else:
    # ------------------ BUSINESS INSIGHTS ------------------
    st.subheader("📈 Business Insights")
    col1, col2 = st.columns(2)
    fig1 = px.histogram(filtered_df, x="Lead Time", title="Lead Time Distribution")
    col1.plotly_chart(fig1, use_container_width=True)
    fig2 = px.scatter(filtered_df, x="Sales", y="Lead Time", color="Region", title="Sales vs Lead Time")
    col2.plotly_chart(fig2, use_container_width=True)

    # ------------------ TRADE-OFF ANALYSIS ------------------
    st.subheader("⚖️ Trade-off Analysis")
    filtered_df["Profit Size"] = filtered_df["Gross Profit"].abs()
    fig3 = px.scatter(filtered_df, x="Lead Time", y="Sales", size="Profit Size", color="Region",
                      hover_data=["Product Name"], title="Profit vs Lead Time")
    st.plotly_chart(fig3, use_container_width=True)

    # ------------------ KPI TREND LINE ------------------
    st.subheader("📊 KPI Trend Line")
    trend_df = filtered_df.groupby("Region")[["Lead Time", "Gross Profit"]].mean().reset_index()
    fig_trend = px.line(trend_df, x="Region", y="Lead Time", markers=True, title="Average Lead Time by Region")
    st.plotly_chart(fig_trend, use_container_width=True)

    # ------------------ SHIPPING PATTERNS ------------------
    st.subheader("🧠 Shipping Patterns")
    fig4 = px.scatter(filtered_df, x="Sales", y="Lead Time", color="Ship Mode", title="Shipping Cluster")
    st.plotly_chart(fig4, use_container_width=True)

# ------------------ EXPORT DATA ------------------
st.subheader("📥 Export Data")
csv = generate_report_dataframe(results).to_csv(index=False).encode("utf-8")
st.download_button("⬇ Download Recommendations Report", csv, "recommendations_report.csv", "text/csv")

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("🚀 Built for Decision Intelligence | Internship Project")
