import streamlit as st
from auth.session import check_login

# -------------------------
# Page Config
# -------------------------

st.set_page_config(
    page_title="MindCare AI",
    page_icon="🧠",
    layout="wide"
)

check_login()

# -------------------------
# CSS
# -------------------------

def load_css():
    with open("assets/css/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# =====================================================
# HERO SECTION
# =====================================================

hero_left, hero_right = st.columns([1.9,1])

with hero_left:

    st.markdown("""
<div class="hero">

<h1>
🧠 MindCare AI
</h1>

<h3 style="color:white;font-weight:500;margin-top:-8px;">
Your Personal AI Mental Wellness Assistant
</h3>

<p>

Leverage the power of
<b>Artificial Intelligence</b>,
<b>Machine Learning</b>
and
<b>Natural Language Processing</b>
to understand your emotional well-being.

Receive instant assessments,
download professional reports,
track previous assessments,
and visualize your mental health journey.

</p>

</div>

""", unsafe_allow_html=True)

    btn1,btn2=st.columns(2)

    with btn1:

        if st.button(
            "🚀 Start Assessment",
            width="stretch"
        ):
            st.switch_page("pages/Assessment.py")

    with btn2:

        if st.button(
            "📊 Dashboard",
            width="stretch"
        ):
            st.switch_page("pages/Dashboard.py")

with hero_right:

    st.markdown("""

<div class="glass">

<h2 style="text-align:center;">
✨ Highlights
</h2>

<br>

### 🤖 AI Powered Analysis

Advanced NLP & Machine Learning

---

### 📈 Smart Analytics

Interactive Dashboard

---

### 📄 PDF Reports

Professional Downloads

---

### 🔒 Secure History

Previous Assessments

---

### ⚡ Instant Results

Within Seconds

</div>

""", unsafe_allow_html=True)

st.write("")
st.write("")
st.divider()
# =====================================================
# PLATFORM STATS
# =====================================================

st.markdown("## 📊 Platform Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
<div class="glass" style="text-align:center;">

<h1>🎯</h1>

<h2>78.26%</h2>

Accuracy

</div>
""", unsafe_allow_html=True)

with c2:
    st.markdown("""
<div class="glass" style="text-align:center;">

<h1>🤖</h1>

<h2>Linear SVM</h2>

Best ML Model

</div>
""", unsafe_allow_html=True)

with c3:
    st.markdown("""
<div class="glass" style="text-align:center;">

<h1>🧠</h1>

<h2>7</h2>

Mental Conditions

</div>
""", unsafe_allow_html=True)

with c4:
    st.markdown("""
<div class="glass" style="text-align:center;">

<h1>📄</h1>

<h2>Unlimited</h2>

PDF Reports

</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")
# =====================================================
# FEATURES
# =====================================================

st.markdown("# ✨ Why MindCare AI?")

st.caption(
    "Designed to provide a fast, intelligent and user-friendly mental wellness assessment experience."
)

st.write("")

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("""
<div class="glass">

<h2>🧠 AI Assessment</h2>

<hr>

✔ Advanced NLP

✔ Machine Learning

✔ Instant Prediction

✔ Confidence Analysis

✔ Seven Mental Health Categories

</div>
""", unsafe_allow_html=True)

with col2:

    st.markdown("""
<div class="glass">

<h2>📈 Smart Dashboard</h2>

<hr>

✔ Assessment History

✔ Interactive Analytics

✔ Confidence Tracking

✔ Visualization

✔ Easy Navigation

</div>
""", unsafe_allow_html=True)

with col3:

    st.markdown("""
<div class="glass">

<h2>📄 Professional Reports</h2>

<hr>

✔ PDF Generation

✔ Download Anytime

✔ Clean Layout

✔ Printable

✔ Secure Storage

</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# =====================================================
# HOW IT WORKS
# =====================================================

st.markdown("# ⚙️ How MindCare AI Works")

st.caption(
    "From your thoughts to AI-powered insights in four simple steps."
)

st.write("")

step1, step2, step3, step4 = st.columns(4)

with step1:
    st.markdown("""
<div class="glass" style="text-align:center;height:250px;">

<h1>✍️</h1>

<h3>Describe</h3>

Tell us how you are feeling.

Be as natural as possible.

</div>
""", unsafe_allow_html=True)

with step2:
    st.markdown("""
<div class="glass" style="text-align:center;height:250px;">

<h1>🤖</h1>

<h3>Analyze</h3>

Natural Language Processing

extracts important patterns.

</div>
""", unsafe_allow_html=True)

with step3:
    st.markdown("""
<div class="glass" style="text-align:center;height:250px;">

<h1>🧠</h1>

<h3>Predict</h3>

Our Machine Learning model predicts the
most likely condition.

</div>
""", unsafe_allow_html=True)

with step4:
    st.markdown("""
<div class="glass" style="text-align:center;height:250px;">

<h1>📄</h1>

<h3>Report</h3>

Download your professional report and
view your assessment history.

</div>
""", unsafe_allow_html=True)

st.write("")
st.divider()

# =====================================================
# TECHNOLOGY
# =====================================================

st.markdown("# 🚀 Technology Stack")

t1, t2 = st.columns([1.2,1])

with t1:

    st.markdown("""
<div class="glass">

## 🧠 Artificial Intelligence

This project combines

• Machine Learning

• Natural Language Processing

• TF-IDF Vectorization

• Linear Support Vector Machine

to deliver fast and reliable
mental health screening.

</div>
""", unsafe_allow_html=True)

with t2:

    st.markdown("""
<div class="glass">

## 📊 Performance

🎯 Accuracy : 78.26%

🤖 Best Model : Linear SVM

📄 Reports : Unlimited

⚡ Prediction : Real Time

🔒 Privacy Focused

</div>
""", unsafe_allow_html=True)

st.write("")
st.divider()

# =====================================================
# DISCLAIMER
# =====================================================

st.markdown("# ⚠️ Important Notice")

st.warning("""

MindCare AI is intended for **educational purposes only**.

It does **not** replace professional psychological
or medical diagnosis.

If you are experiencing emotional distress,
please consult a qualified mental health professional.

""")

st.write("")

st.markdown("---")

st.markdown(
"""
<div style="text-align:center;padding:25px;">

<h3>MindCare AI</h3>

AI Powered Mental Health Assessment Platform

Made by

<b>Divyansh Raj • All Rights Reserved • 2026 • email: divyanshraj860@gmail.com</b>

</div>
""",
unsafe_allow_html=True
)