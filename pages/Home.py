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

# -------------------------
# HERO
# -------------------------

st.markdown("""
<div class="hero">

<h1>🧠 MindCare AI</h1>

<p>

AI-powered Mental Health Assessment Platform

Using Machine Learning + NLP to provide
fast mental health screening,
professional reports,
analytics,
and personalized recommendations.

</p>

</div>

""", unsafe_allow_html=True)

st.write("")

# -------------------------
# STATS
# -------------------------

c1,c2,c3,c4 = st.columns(4)

with c1:

    st.metric(
        "🎯 Accuracy",
        "78.26%"
    )

with c2:

    st.metric(
        "🤖 AI Model",
        "Linear SVM"
    )

with c3:

    st.metric(
        "🧠 Conditions",
        "7"
    )

with c4:

    st.metric(
        "📄 Reports",
        "Unlimited"
    )

st.divider()

# -------------------------
# FEATURES
# -------------------------

st.header("✨ Features")

col1,col2,col3 = st.columns(3)

with col1:

    st.markdown("""
<div class="glass">

## 🧠 AI Assessment

Write how you feel.

Our AI predicts possible
mental health conditions
within seconds.

</div>
""",unsafe_allow_html=True)

with col2:

    st.markdown("""
<div class="glass">

## 📊 Analytics

Interactive dashboard

Charts

Prediction history

Confidence analysis

</div>
""",unsafe_allow_html=True)

with col3:

    st.markdown("""
<div class="glass">

## 📄 Reports

Generate beautiful

PDF Reports

Download anytime

</div>
""",unsafe_allow_html=True)

st.write("")
st.write("")

# -------------------------
# HOW IT WORKS
# -------------------------

st.header("⚙️ How It Works")

steps = st.columns(7)

titles = [
    "Write",
    "Analyze",
    "Predict",
    "Confidence",
    "Recommendation",
    "Report",
    "History"
]

icons = [
    "✍️",
    "🧠",
    "🎯",
    "📈",
    "💡",
    "📄",
    "📊"
]

for i,col in enumerate(steps):

    with col:

        st.markdown(f"""
<div class="feature">

# {icons[i]}

### {titles[i]}

</div>

""",unsafe_allow_html=True)

st.divider()

# -------------------------
# MODEL
# -------------------------

st.header("🤖 AI Model")

st.info("""

**Best Performing Model**

Linear Support Vector Machine (Linear SVM)

Accuracy : **78.26%**

Dataset :

Mental Health Combined Dataset

TF-IDF Vectorization

Natural Language Processing

""")

st.divider()

# -------------------------
# DISCLAIMER
# -------------------------

st.warning("""

### ⚠️ Disclaimer

MindCare AI is an educational project.

It is **NOT**

a medical diagnosis tool.

Always consult a qualified
mental health professional.

""")

st.write("")

st.caption(
    "Made by Divyansh Raj | Scikit-Learn | Plotly"
)