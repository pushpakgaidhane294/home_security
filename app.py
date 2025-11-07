import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# =========================================
# SENTINELSPHERE — STREAMLIT DASHBOARD
# =========================================

st.set_page_config(page_title="SentinelSphere Dashboard", layout="wide")
st.title("🧠 SentinelSphere — AI-Powered Home Security Dashboard")

# ---------- Sidebar: Controls & AI Insights ----------
st.sidebar.title("🧠 AI Insights & Controls")

security_score = random.randint(60, 95)
st.sidebar.metric("Daily Security Score", f"{security_score}/100")
st.sidebar.progress(security_score)

st.sidebar.markdown("**Routine Patterns Learned:**")
st.sidebar.text("🕒 Sleep: 11PM – 7AM")
st.sidebar.text("📱 Phone away: 8AM – 6PM")
st.sidebar.text("🏠 Empty home: 9AM – 5PM")

predictions = {
    "Door Access Anomaly": "30%",
    "Cyber Intrusion Risk": "15%",
}
st.sidebar.markdown("**Predicted Threats (Next 24h):**")
for k, v in predictions.items():
    st.sidebar.text(f"• {k}: {v}")

st.sidebar.markdown("**Automation Shortcuts:**")
st.sidebar.checkbox("🔔 Auto-notify neighbor")
st.sidebar.checkbox("🤫 Enable silent mode")
st.sidebar.checkbox("🎥 Auto-record if threat > 80")

# ---------- Simulated Live Data ----------
def generate_alert():
    titles = [
        "Unusual Wi-Fi signal near window",
        "Door opened unexpectedly",
        "Motion detected in living room",
        "New device joined the network",
        "High noise level detected"
    ]
    locations = ["Living Room", "Bedroom", "Kitchen", "Front Door", "Backyard"]
    threat = random.choice(["Low", "Medium", "High"])
    title = random.choice(titles)
    return {
        "Time": datetime.now().strftime("%I:%M:%S %p"),
        "Title": title,
        "Location": random.choice(locations),
        "Threat": threat,
        "Description": f"{title} in {locations[random.randint(0,4)]}. Threat level: {threat}."
    }

# ---------- Layout ----------
col1, col2 = st.columns([2, 1])

# ---------- Digital Twin / Home View ----------
with col1:
    st.subheader("🏠 Home Digital Twin — 3D View")

    # 3D coordinates for rooms
    rooms_3d = [
        {"Room": "Living Room", "x": 0, "y": 0, "z": 0},
        {"Room": "Kitchen", "x": 4, "y": 0, "z": 0},
        {"Room": "Bedroom", "x": 0, "y": 4, "z": 0},
        {"Room": "Front Door", "x": 4, "y": 4, "z": 0},
        {"Room": "Backyard", "x": 2, "y": 2, "z": -1},
    ]
    df_3d = pd.DataFrame(rooms_3d)
    df_3d["Activity"] = np.random.randint(40, 100, len(df_3d))

    fig_3d = go.Figure(data=[
        go.Scatter3d(
            x=df_3d["x"],
            y=df_3d["y"],
            z=df_3d["z"],
            mode='markers+text',
            text=df_3d["Room"],
            textposition="top center",
            marker=dict(
                size=14,
                color=df_3d["Activity"],
                colorscale="Turbo",
                opacity=0.9,
                colorbar=dict(title="Activity Level")
            )
        )
    ])

    fig_3d.update_layout(
        title="3D Digital Twin — Interactive Home Layout",
        scene=dict(
            xaxis_title='Width',
            yaxis_title='Depth',
            zaxis_title='Height',
            bgcolor='black'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=500
    )

    st.plotly_chart(fig_3d, use_container_width=True)

    # 2D Activity Heatmap (kept for comparison)
    st.subheader("📊 Activity Heatmap (2D View)")
    rooms = ["Living Room", "Bedroom", "Kitchen", "Front Door", "Backyard"]
    heat_values = np.random.randint(20, 100, len(rooms))
    df_heat = pd.DataFrame({"Room": rooms, "Activity Score": heat_values})
    fig_heat = px.bar(df_heat, x="Room", y="Activity Score", color="Activity Score",
                      color_continuous_scale=["#00f5ff", "#ff004c"])
    st.plotly_chart(fig_heat, use_container_width=True)

    # Timeline Replay (Bottom Panel)
    st.subheader("📈 Timeline & Replay")
    hours = pd.date_range(datetime.now() - timedelta(hours=24), periods=24, freq='H')
    events = np.random.randint(0, 10, 24)
    fig_timeline = go.Figure()
    fig_timeline.add_trace(go.Scatter(x=hours, y=events, mode='lines+markers', name='Events'))
    fig_timeline.update_layout(title="Security Event Timeline (Last 24 Hours)",
                               xaxis_title="Time", yaxis_title="Events Count")
    st.plotly_chart(fig_timeline, use_container_width=True)

    st.info("🗣️ **AI Narration:** Between 10PM–11:30PM, an unusual Wi-Fi signal and motion were detected near the entrance.")

# ---------- Real-Time Alerts Feed ----------
with col2:
    st.subheader("🚨 Real-Time Alerts")
    placeholder = st.empty()

    for _ in range(3):
        alerts = [generate_alert() for _ in range(random.randint(1, 3))]
        with placeholder.container():
            for a in alerts:
                color = "#ff4d4d" if a["Threat"] == "High" else "#ffaa00" if a["Threat"] == "Medium" else "#00ffcc"
                st.markdown(
                    f"""
                    <div style="background-color:#111;padding:10px;border-radius:10px;margin-bottom:10px;">
                        <b style="color:{color}">[{a['Threat']}]</b> {a['Title']}  
                        <br><small>🕒 {a['Time']} | 📍 {a['Location']}</small>
                        <br>{a['Description']}
                        <div style="margin-top:8px;">
                            <button style="background:#2563eb;color:white;border:none;padding:4px 8px;border-radius:5px;margin-right:4px;">Verify</button>
                            <button style="background:#374151;color:white;border:none;padding:4px 8px;border-radius:5px;">Ignore</button>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        time.sleep(1)

# ---------- Analytics Section ----------
st.markdown("---")
st.header("📊 Security Analytics & Reports")

colA, colB, colC = st.columns(3)

with colA:
    trend_data = pd.DataFrame({
        "Day": [f"Day {i}" for i in range(1, 8)],
        "Threat Score": np.random.randint(50, 100, 7)
    })
    fig_trend = px.line(trend_data, x="Day", y="Threat Score", title="Weekly Security Trend")
    st.plotly_chart(fig_trend, use_container_width=True)

with colB:
    freq_data = pd.DataFrame({
        "Room": rooms,
        "Events": np.random.randint(1, 10, len(rooms))
    })
    fig_bar = px.bar(freq_data, x="Room", y="Events", title="Event Frequency by Room")
    st.plotly_chart(fig_bar, use_container_width=True)

with colC:
    pie_data = pd.DataFrame({
        "Response": ["Confirmed", "False Alarm", "Ignored"],
        "Count": [random.randint(5, 15) for _ in range(3)]
    })
    fig_pie = px.pie(pie_data, values="Count", names="Response", title="User Response Metrics")
    st.plotly_chart(fig_pie, use_container_width=True)

# ---------- Community Watch ----------
st.markdown("---")
st.header("🌐 Community Watch (Anonymous)")

map_data = pd.DataFrame({
    "lat": [19.07 + random.uniform(-0.01, 0.01) for _ in range(10)],
    "lon": [72.87 + random.uniform(-0.01, 0.01) for _ in range(10)],
    "ThreatLevel": np.random.randint(20, 100, 10)
})
fig_map = px.density_mapbox(map_data, lat='lat', lon='lon', z='ThreatLevel', radius=20,
                            center=dict(lat=19.07, lon=72.87), zoom=12,
                            mapbox_style="stamen-toner",
                            title="Neighborhood Threat Heatmap")
st.plotly_chart(fig_map, use_container_width=True)

st.success("✅ SentinelSphere AI Dashboard Simulation Running Successfully!")
