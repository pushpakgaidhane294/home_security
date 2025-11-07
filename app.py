import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from streamlit_autorefresh import st_autorefresh
import backend  # Import custom backend

# Page Configuration
st.set_page_config(
    page_title="SentinelSphere - IoT Security Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark UI
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    .stMetric { background: rgba(30, 41, 59, 0.7); padding: 20px; border-radius: 10px; border: 1px solid rgba(59, 130, 246, 0.3);}
    .stAlert { border-radius: 10px; border: 1px solid rgba(239, 68, 68, 0.5);}
    h1, h2, h3 { color: #60a5fa !important; font-family: 'Orbitron', sans-serif;}
    .metric-card { background: rgba(30, 41, 59, 0.7); padding: 20px; border-radius: 10px; border: 1px solid rgba(59, 130, 246, 0.3);}
</style>
""", unsafe_allow_html=True)

# Initialize session state (refresh fake devices/alerts on each reload)
count = st_autorefresh(interval=5000, limit=None, key="refresh")
st.session_state.devices = backend.get_devices()
st.session_state.alerts = backend.get_alerts()
st.session_state.activity_log = backend.get_activity_log()

# Sidebar
with st.sidebar:
    st.title("🛡️ SentinelSphere")
    st.markdown("---")
    page = st.radio(
        "Navigation",
        ["Dashboard", "Devices", "Analytics", "Alerts", "Settings"],
        index=0
    )
    st.markdown("---")
    st.subheader("System Status")
    st.metric("Active Devices", len([d for d in st.session_state.devices if d['status'] == 'active']))
    st.metric("Alerts Today", len(st.session_state.alerts))
    st.metric("System Health", "98%", delta="2%")
    st.markdown("---")
    st.caption("Last updated: " + datetime.now().strftime("%H:%M:%S"))

if page == "Dashboard":
    st.title("🏠 Security Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Devices", len(st.session_state.devices), delta="2 new")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        active_devices = len([d for d in st.session_state.devices if d['status'] == 'active'])
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Active Devices", active_devices, delta=f"{(active_devices/len(st.session_state.devices)*100):.0f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Active Alerts", len([a for a in st.session_state.alerts if a['severity'] in ['high', 'medium']]), delta="-1")
        st.markdown('</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("System Uptime", "99.8%", delta="0.2%")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Device Activity (24h)")
        hours = [datetime.now() - timedelta(hours=i) for i in range(24, 0, -1)]
        activity = np.random.randint(5, 50, 24)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hours,
            y=activity,
            mode='lines+markers',
            line=dict(color='#60a5fa', width=3),
            fill='tozeroy',
            fillcolor='rgba(96, 165, 250, 0.2)'
        ))
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(30, 41, 59, 0.5)',
            plot_bgcolor='rgba(30, 41, 59, 0.5)',
            xaxis_title="Time",
            yaxis_title="Events",
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("📈 Alert Distribution")
        alert_types = ['Critical', 'Warning', 'Info']
        alert_counts = [
            len([a for a in st.session_state.alerts if a['severity'] == 'high']),
            len([a for a in st.session_state.alerts if a['severity'] == 'medium']),
            len([a for a in st.session_state.alerts if a['severity'] == 'low'])
        ]
        fig = go.Figure(data=[go.Pie(
            labels=alert_types,
            values=alert_counts,
            hole=.4,
            marker=dict(colors=['#ef4444', '#f59e0b', '#3b82f6'])
        )])
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(30, 41, 59, 0.5)',
            plot_bgcolor='rgba(30, 41, 59, 0.5)',
            height=300,
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    st.subheader("🚨 Recent Alerts")
    for alert in st.session_state.alerts[:5]:
        severity_color = {'high': '🔴', 'medium': '🟡', 'low': '🔵'}
        with st.expander(f"{severity_color[alert['severity']]} {alert['message']}", expanded=False):
            st.write(f"**Timestamp:** {alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
            st.write(f"**Severity:** {alert['severity'].upper()}")
            st.write(f"**Type:** {alert['type']}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Acknowledge", key=f"ack_{alert['id']}"):
                    st.success("Alert acknowledged!")
            with col2:
                if st.button("Dismiss", key=f"dismiss_{alert['id']}"):
                    st.info("Alert dismissed!")

elif page == "Devices":
    st.title("🔧 Device Management")
    device_types = ["All"] + list(set([d['type'] for d in st.session_state.devices]))
    selected_type = st.selectbox("Filter by Type", device_types)
    filtered_devices = st.session_state.devices if selected_type == "All" else [d for d in st.session_state.devices if d['type'] == selected_type]
    cols = st.columns(3)
    for idx, device in enumerate(filtered_devices):
        with cols[idx % 3]:
            status_icon = "🟢" if device['status'] == 'active' else "🔴"
            with st.container():
                st.markdown(f"### {status_icon} {device['name']}")
                st.write(f"**Type:** {device['type'].title()}")
                st.write(f"**Location:** {device['location']}")
                battery_color = "🟢" if device['battery'] > 70 else "🟡" if device['battery'] > 30 else "🔴"
                st.progress(device['battery'] / 100)
                st.write(f"{battery_color} Battery: {device['battery']}%")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Details", key=f"details_{device['id']}"):
                        st.info(f"Showing details for {device['name']}")
                with col2:
                    if st.button("Configure", key=f"config_{device['id']}"):
                        st.info(f"Configuring {device['name']}")
                st.markdown("---")

elif page == "Analytics":
    st.title("📊 Analytics & Insights")
    time_range = st.select_slider(
        "Select Time Range",
        options=["24h", "7d", "30d", "90d", "1y"],
        value="7d"
    )
    st.markdown("---")
    st.subheader("🔥 Activity Heatmap")
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    hours = list(range(24))
    z = np.random.randint(0, 50, (7, 24))
    fig = go.Figure(data=go.Heatmap(z=z, x=hours, y=days, colorscale='Blues'))
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(30, 41, 59, 0.5)',
        plot_bgcolor='rgba(30, 41, 59, 0.5)',
        xaxis_title="Hour of Day",
        yaxis_title="Day of Week",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📱 Device Response Times")
        devices = [d['name'] for d in st.session_state.devices[:5]]
        response_times = np.random.randint(50, 300, 5)
        fig = go.Figure(data=[go.Bar(x=devices, y=response_times, marker_color='#60a5fa')])
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(30, 41, 59, 0.5)',
            plot_bgcolor='rgba(30, 41, 59, 0.5)',
            yaxis_title="Response Time (ms)",
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("🔋 Battery Health")
        devices = [d['name'] for d in st.session_state.devices[:5]]
        battery_levels = [d['battery'] for d in st.session_state.devices[:5]]
        fig = go.Figure(data=[go.Bar(
            x=devices,
            y=battery_levels,
            marker_color=['#22c55e' if b > 70 else '#f59e0b' if b > 30 else '#ef4444' for b in battery_levels]
        )])
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(30, 41, 59, 0.5)',
            plot_bgcolor='rgba(30, 41, 59, 0.5)',
            yaxis_title="Battery Level (%)",
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)

elif page == "Alerts":
    st.title("🚨 Alert Management")
    col1, col2, col3 = st.columns(3)
    with col1:
        severity_filter = st.multiselect(
            "Severity",
            ["high", "medium", "low"],
            default=["high", "medium", "low"]
        )
    with col2:
        type_filter = st.multiselect(
            "Type",
            ["critical", "warning", "info"],
            default=["critical", "warning", "info"]
        )
    with col3:
        time_filter = st.selectbox(
            "Time Range",
            ["Last Hour", "Last 24 Hours", "Last Week", "All Time"]
        )
    st.markdown("---")
    filtered_alerts = [a for a in st.session_state.alerts if a['severity'] in severity_filter and a['type'] in type_filter]
    if filtered_alerts:
        df = pd.DataFrame(filtered_alerts)
        df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        st.dataframe(df, use_container_width=True, height=400)
    else:
        st.info("No alerts match the selected filters.")
    st.markdown("---")
    st.subheader("📈 Alert Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Alerts", len(st.session_state.alerts))
    with col2:
        st.metric("Critical Alerts", len([a for a in st.session_state.alerts if a['severity'] == 'high']))
    with col3:
        st.metric("Resolved Today", 5, delta="3")

elif page == "Settings":
    st.title("⚙️ Settings")
    tabs = st.tabs(["General", "Notifications", "Security", "System"])
    with tabs[0]:
        st.subheader("General Settings")
        auto_refresh = st.toggle("Auto-refresh Dashboard", value=True)
        refresh_interval = st.slider("Refresh Interval (seconds)", 1, 60, 5)
        theme = st.selectbox("Theme", ["Dark", "Light", "Auto"])
        language = st.selectbox("Language", ["English", "Spanish", "French", "German"])
        if st.button("Save General Settings"):
            st.success("Settings saved successfully!")
    with tabs[1]:
        st.subheader("Notification Settings")
        email_notifications = st.toggle("Email Notifications", value=True)
        push_notifications = st.toggle("Push Notifications", value=True)
        st.write("**Alert Preferences**")
        notify_critical = st.checkbox("Critical Alerts", value=True)
        notify_warning = st.checkbox("Warning Alerts", value=True)
        notify_info = st.checkbox("Info Alerts", value=False)
        if st.button("Save Notification Settings"):
            st.success("Notification settings saved!")
    with tabs[2]:
        st.subheader("Security Settings")
        two_factor = st.toggle("Two-Factor Authentication", value=True)
        auto_lock = st.toggle("Auto-lock After Inactivity", value=True)
        lock_timeout = st.number_input("Lock Timeout (minutes)", 1, 60, 15)
        st.write("**Password Requirements**")
        min_length = st.number_input("Minimum Password Length", 8, 32, 12)
        require_special = st.checkbox("Require Special Characters", value=True)
        if st.button("Save Security Settings"):
            st.success("Security settings saved!")
    with tabs[3]:
        st.subheader("System Information")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Version:** 2.5.1")
            st.write("**Last Update:** 2024-01-15")
            st.write("**Database:** Connected")
        with col2:
            st.write("**API Status:** Online")
            st.write("**Backup:** Enabled")
            st.write("**Storage:** 45% used")
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Check for Updates"):
                st.info("System is up to date!")
        with col2:
            if st.button("Export Data"):
                st.info("Data export started...")
        with col3:
            if st.button("Clear Cache"):
                st.success("Cache cleared!")

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #64748b;'>
        <p>SentinelSphere IoT Security Dashboard v2.5.1</p>
        <p>© 2024 SentinelSphere. All rights reserved.</p>
    </div>
    """,
    unsafe_allow_html=True
)
