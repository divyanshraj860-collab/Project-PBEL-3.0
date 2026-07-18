import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

# =====================================================
# DASHBOARD HERO
# =====================================================

hero_left, hero_right = st.columns([2, 1])

with hero_left:

    st.markdown("""
<div class="hero">

<h1>📊 Mental Health Dashboard</h1>

<h3 style="color:white;font-weight:500;">
Track your assessment journey with AI-powered insights
</h3>

<p>

Analyze previous assessments, monitor confidence trends,
explore prediction distributions, and gain a deeper
understanding of your mental wellness over time.

</p>

</div>
""", unsafe_allow_html=True)

with hero_right:

    st.markdown("""
<div class="glass">

### 📌 Dashboard Overview

✅ Assessment History

✅ AI Analytics

✅ Confidence Trends

✅ Prediction Insights

✅ CSV Export

</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------- LOAD HISTORY ---------------- #

history = load_history()

if history.empty:
    st.info("No assessments available.")
    st.stop()

history["Confidence"] = history["Confidence"].astype(float)
# =====================================================
# AI INSIGHTS
# =====================================================

total_assessments = len(history)
avg_conf = history["Confidence"].mean()
max_conf = history["Confidence"].max()
min_conf = history["Confidence"].min()
latest_prediction = history.iloc[-1]["Prediction"]
common_prediction = history["Prediction"].mode()[0]
unique_conditions = history["Prediction"].nunique()

if total_assessments > 1:
    trend = history.iloc[-1]["Confidence"] - history.iloc[0]["Confidence"]
else:
    trend = 0

trend_text = (
    "📈 Improving"
    if trend > 0
    else "📉 Declining"
    if trend < 0
    else "➡ Stable"
)

st.markdown("# 🧠 AI Insights")

i1, i2, i3, i4 = st.columns(4)

with i1:
    st.markdown(f"""
<div class="glass" style="text-align:center;padding:20px;">
<h2>📝</h2>
<h2>{total_assessments}</h2>
Total Assessments
</div>
""", unsafe_allow_html=True)

with i2:
    st.markdown(f"""
<div class="glass" style="text-align:center;padding:20px;">
<h2>🧠</h2>
<h2>{common_prediction}</h2>
Most Common
</div>
""", unsafe_allow_html=True)

with i3:
    st.markdown(f"""
<div class="glass" style="text-align:center;padding:20px;">
<h2>📊</h2>
<h2>{avg_conf:.1f}%</h2>
Average Confidence
</div>
""", unsafe_allow_html=True)

with i4:
    st.markdown(f"""
<div class="glass" style="text-align:center;padding:20px;">
<h2>{trend_text}</h2>
Confidence Trend
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="glass">

### 🤖 AI Summary

Based on **{total_assessments}** assessments, the most frequently detected condition is **{common_prediction}**.

The average confidence is **{avg_conf:.2f}%**, with a highest recorded confidence of **{max_conf:.2f}%**.

Across your history, **{unique_conditions}** different mental health conditions have been identified.

Your latest assessment was **{latest_prediction}**, and your overall confidence trend is **{trend_text}**.

</div>
""", unsafe_allow_html=True)

st.write("")
# =====================================================
# WELLNESS SCORE
# =====================================================

wellness_score = round(avg_conf)

gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=wellness_score,
        title={"text": "Mental Wellness Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#2563EB"},
            "steps": [
                {"range": [0, 40], "color": "#FECACA"},
                {"range": [40, 70], "color": "#FDE68A"},
                {"range": [70, 100], "color": "#BBF7D0"},
            ],
        },
    )
)

gauge.update_layout(
    height=320,
    margin=dict(l=20, r=20, t=40, b=20),
)

left, right = st.columns([1,2])

with left:

    st.plotly_chart(
        gauge,
        width="stretch"
    )

with right:

    st.markdown("""
<div class="glass">

# 🧠 Mental Wellness Score

This score is calculated using your
overall assessment confidence.

Higher values indicate that your
assessment history has remained more
consistent and confident.

It is intended as a dashboard indicator
only and should not be interpreted as a
medical measurement.

</div>
""", unsafe_allow_html=True)
# =====================================================
# DASHBOARD METRICS
# =====================================================

st.markdown("## 📈 Dashboard Overview")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
<div class="glass" style="text-align:center;">

<h2>📝</h2>

<h2>{len(history)}</h2>

Assessments

</div>
""", unsafe_allow_html=True)

with m2:
    st.markdown(f"""
<div class="glass" style="text-align:center;">

<h2>🎯</h2>

<h2>{history['Confidence'].mean():.1f}%</h2>

Average Confidence

</div>
""", unsafe_allow_html=True)

with m3:
    st.markdown(f"""
<div class="glass" style="text-align:center;">

<h2>🚀</h2>

<h2>{history['Confidence'].max():.1f}%</h2>

Highest Confidence

</div>
""", unsafe_allow_html=True)

with m4:
    st.markdown(f"""
<div class="glass" style="text-align:center;">

<h2>🧠</h2>

<h2>{history['Prediction'].mode()[0]}</h2>

Most Common

</div>
""", unsafe_allow_html=True)

st.write("")

# =====================================================
# AI ANALYTICS
# =====================================================

st.markdown("## 📊 AI Analytics")

left_chart, right_chart = st.columns(2)

with left_chart:

    pie = px.pie(
        history,
        names="Prediction",
        hole=0.65,
        title="Prediction Distribution",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    pie.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    pie.update_layout(
        height=430,
        legend_title="Conditions",
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(pie, width="stretch")

with right_chart:

    line = px.line(
        history,
        x="Date",
        y="Confidence",
        markers=True,
        title="Confidence Over Time"
    )

    line.update_traces(
        line=dict(width=3),
        marker=dict(size=9)
    )

    line.update_layout(
        height=430,
        yaxis_title="Confidence (%)",
        xaxis_title="Assessment Date",
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(line, width="stretch")

st.write("")

bar = px.histogram(
    history,
    x="Prediction",
    color="Prediction",
    title="Assessment Frequency",
    text_auto=True,
    color_discrete_sequence=px.colors.qualitative.Pastel
)

bar.update_layout(
    height=430,
    xaxis_title="Mental Health Condition",
    yaxis_title="Number of Assessments",
    margin=dict(l=20, r=20, t=60, b=20),
    showlegend=False
)

st.plotly_chart(bar, width="stretch")

st.divider()
# =====================================================
# SEARCH HISTORY
# =====================================================

st.markdown("## 🔍 Search Assessment History")

search = st.text_input(
    "Search Assessment History",
    label_visibility="collapsed",
    placeholder="Search by prediction..."
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
# =====================================================
# LATEST ASSESSMENT
# =====================================================

st.markdown("## 📝 Latest Assessment")

latest = history.iloc[-1]

left, right = st.columns([2,1])

with left:

    st.markdown(f"""
<div class="glass">

<h3>🧠 Prediction</h3>

<h2>{latest['Prediction']}</h2>

<b>Confidence:</b> {latest['Confidence']:.2f}%

<br><br>

<b>Date:</b><br>

{latest['Date']}

</div>
""", unsafe_allow_html=True)

with right:

    st.markdown("""
<div class="glass">

<h3>📌 Status</h3>

Latest AI Assessment

</div>
""", unsafe_allow_html=True)

st.markdown("### 💬 Statement")

st.info(latest["Statement"])

st.divider()

# =====================================================
# EXPORT
# =====================================================

st.markdown("## 📥 Export Assessment History")

st.markdown("""
<div class="glass">

Download all previous assessments as a CSV file for future reference or analysis.

</div>
""", unsafe_allow_html=True)

csv = history.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Download Complete History",
    csv,
    "assessment_history.csv",
    "text/csv",
    width="stretch"
)

st.divider()

# =====================================================
# RECENT RECORDS
# =====================================================

st.markdown("## 📋 Recent Assessments")

history_sorted = history.sort_values(
    by="Date",
    ascending=False
)

st.dataframe(
    history_sorted,
    width="stretch",
    hide_index=True
)

st.divider()

st.markdown(
"""
<div style="text-align:center;padding:25px;opacity:0.75;">

<b> MindCare AI Dashboard </b>
<b>AI Powered Analytics</b>


Made by 
<b>Divyansh Raj • All Rights Reserved • 2026 • email: divyanshraj860@gmail.com</b>
</div>
""",
unsafe_allow_html=True
)