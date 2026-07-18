import streamlit as st
import pandas as pd
import plotly.express as px
from auth.session import check_login
from utils.history import load_history

# ---------------- PAGE ---------------- #

st.set_page_config(
    page_title="Dashboard | MindCare AI",
    page_icon="📊",
    layout="wide"
)

check_login()

# ---------------- CSS ---------------- #

with open("assets/css/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- TITLE ---------------- #

st.markdown("""
<div class="hero">
<h1>📊 Dashboard</h1>
<p>
View your previous assessments and analytics.
</p>
</div>
""", unsafe_allow_html=True)

# ---------------- LOAD HISTORY ---------------- #

history = load_history()

if history.empty:
    st.info("No assessments available.")
    st.stop()

history["Confidence"] = history["Confidence"].astype(float)

# ---------------- METRICS ---------------- #

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Assessments",
        len(history)
    )

with c2:
    st.metric(
        "Average Confidence",
        f"{history['Confidence'].mean():.2f}%"
    )

with c3:
    st.metric(
        "Highest Confidence",
        f"{history['Confidence'].max():.2f}%"
    )

with c4:
    st.metric(
        "Most Common",
        history["Prediction"].mode()[0]
    )

st.divider()

# ---------------- PIE CHART ---------------- #

st.subheader("Prediction Distribution")

pie = px.pie(
    history,
    names="Prediction",
    hole=0.45,
    title="Mental Health Prediction Distribution"
)

st.plotly_chart(
    pie,
    width="stretch"
)

st.divider()

# ---------------- CONFIDENCE ---------------- #

st.subheader("Confidence Trend")

line = px.line(
    history,
    y="Confidence",
    markers=True,
    title="Confidence Over Time"
)

st.plotly_chart(
    line,
    width="stretch"
)

st.divider()

# ---------------- BAR ---------------- #

st.subheader("Prediction Frequency")

bar = px.histogram(
    history,
    x="Prediction",
    color="Prediction",
    title="Frequency of Predictions"
)

st.plotly_chart(
    bar,
    width="stretch"
)

st.divider()
# ---------------- SEARCH ---------------- #

st.subheader("🔍 Search Assessment History")

search = st.text_input(
    "Search by Prediction or Statement"
)

filtered = history.copy()

if search.strip():

    filtered = filtered[
        filtered["Prediction"].str.contains(search, case=False, na=False)
        |
        filtered["Statement"].str.contains(search, case=False, na=False)
    ]

st.dataframe(
    filtered,
    width="stretch",
    hide_index=True
)

st.divider()

# ---------------- LATEST ---------------- #

st.subheader("📝 Latest Assessment")

latest = history.iloc[-1]

left, right = st.columns(2)

with left:

    st.info(f"""
### Prediction

**{latest['Prediction']}**

Confidence:

**{latest['Confidence']:.2f}%**
""")

with right:

    st.success(f"""
### Date

{latest['Date']}
""")

st.write("### Statement")

st.write(latest["Statement"])

st.divider()

# ---------------- DOWNLOAD ---------------- #

st.subheader("📥 Export History")

csv = history.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Download History CSV",
    csv,
    "assessment_history.csv",
    "text/csv",
    width="stretch"
)

st.divider()

# ---------------- RECENT RECORDS ---------------- #

st.subheader("📋 Recent Assessments")

st.dataframe(
    history.sort_values(
        by="Date",
        ascending=False
    ),
    width="stretch",
    hide_index=True
)

st.divider()

# ---------------- FOOTER ---------------- #

st.caption(
    "MindCare AI • Dashboard Analytics • Streamlit • Plotly"
)