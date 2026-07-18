import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

from auth.session import check_login
from models.predict import predict_mental_health
from utils.history import save_history
from utils.report_generator import generate_pdf


# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Assessment | MindCare AI",
    page_icon="🧠",
    layout="wide"
)

check_login()


# ---------------- CSS ---------------- #

try:
    with open("assets/css/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
except FileNotFoundError:
    pass


# =====================================================
# HERO
# =====================================================

left, right = st.columns([1.8, 1])

with left:

    st.markdown("""
<div class="hero">

<h1>🧠 AI Mental Health Assessment</h1>

<h3 style="color:white;font-weight:500;">
Understand your emotional well-being with Artificial Intelligence
</h3>

<p>

Share your thoughts naturally.

Our Machine Learning model analyzes your text and predicts the most likely mental health condition within seconds.

Receive confidence scores, personalized recommendations, interactive visualizations, and a downloadable professional report.

</p>

</div>
""", unsafe_allow_html=True)

with right:

    st.markdown("""
<div class="glass">

### 🚀 Assessment Includes

✅ AI Prediction

✅ Confidence Score

✅ Probability Analysis

✅ Personalized Suggestions

✅ PDF Report

</div>
""", unsafe_allow_html=True)

st.write("")


# =====================================================
# MODEL OVERVIEW
# =====================================================

st.markdown("## 📊 Model Overview")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
<div class="glass" style="text-align:center; padding:20px;">

<h2>🤖</h2>

<h3>Linear SVM</h3>

<p>Best Performing Model</p>

</div>
""", unsafe_allow_html=True)

with c2:
    st.markdown("""
<div class="glass" style="text-align:center; padding:20px;">

<h2>🎯</h2>

<h3>78.26%</h3>

<p>Prediction Accuracy</p>

</div>
""", unsafe_allow_html=True)

with c3:
    st.markdown("""
<div class="glass" style="text-align:center; padding:20px;">

<h2>⚡</h2>

<h3>Real-Time</h3>

<p>Instant Analysis</p>

</div>
""", unsafe_allow_html=True)

st.write("")


# =====================================================
# INPUT SECTION
# =====================================================

st.markdown("## ✍️ Share Your Thoughts")

st.markdown("""
<div class="glass">

Take a moment to describe how you've been feeling recently.

You can mention your emotions, sleep, stress, relationships, work, studies, or anything else affecting your mental well-being. The more detail you provide, the more meaningful the AI assessment can be.

</div>
""", unsafe_allow_html=True)

statement = st.text_area(
    "Describe your feelings",
    label_visibility="collapsed",
    height=260,
    placeholder="""
Example:

• I feel anxious most of the day.
• I have trouble sleeping at night.
• I don't enjoy activities like I used to.
• I often feel lonely or overwhelmed.

Write naturally in your own words...
"""
)

st.write("")

left, center, right = st.columns([1, 2, 1])

with center:
    analyze = st.button(
        "🚀 Analyze My Mental Health",
        width="stretch"
    )

st.write("")

# ---------------- ANALYSIS ---------------- #

if analyze:

    if statement.strip() == "":
        st.warning("Please enter your feelings before continuing.")
        st.stop()

    with st.spinner("Analyzing..."):

        prediction, confidence, classes, probabilities = predict_mental_health(
            statement
        )

    save_history(
        statement,
        prediction,
        confidence
    )

    st.session_state["statement"] = statement
    st.session_state["prediction"] = prediction
    st.session_state["confidence"] = confidence
    st.session_state["classes"] = classes
    st.session_state["probabilities"] = probabilities

    st.success("Analysis completed successfully.")


# ---------------- RESULTS ---------------- #

if "prediction" in st.session_state:

    prediction = st.session_state["prediction"]
    confidence = st.session_state["confidence"]
    statement = st.session_state["statement"]
    classes = st.session_state["classes"]
    probabilities = st.session_state["probabilities"]

    st.divider()

    st.markdown("# 🧠 Assessment Result")

    result_left, result_right = st.columns([2, 1])

    with result_left:

        st.markdown("""
<div class="glass">

<h2>Prediction</h2>

</div>
""", unsafe_allow_html=True)

        if prediction.lower() == "depression":
            st.error(f"🔴 {prediction}")

        elif prediction.lower() == "anxiety":
            st.warning(f"🟡 {prediction}")

        elif prediction.lower() == "suicidal":
            st.error(f"🚨 {prediction}")

        else:
            st.success(f"🟢 {prediction}")

    with result_right:

        st.markdown("""
<div class="glass">

<h2 style="text-align:center;">Confidence</h2>

</div>
""", unsafe_allow_html=True)

        st.metric(
    "Confidence",
    f"{confidence:.2f}%",
    label_visibility="collapsed"
)

        st.progress(confidence / 100)

    st.write("")

    st.markdown("## 📊 Prediction Probabilities")

    df = pd.DataFrame({
        "Condition": classes,
        "Probability": probabilities
    })

    fig = px.bar(
        df,
        x="Condition",
        y="Probability",
        color="Probability",
        text="Probability",
        title="AI Confidence Across Mental Health Conditions"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Condition",
        yaxis_title="Probability (%)",
        height=500,
        showlegend=False,
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.divider()

    # ---------------- RISK LEVEL ---------------- #

    st.subheader("📈 Risk Level")

    if confidence >= 90:
        st.error("🔴 High Risk")
    elif confidence >= 75:
        st.warning("🟡 Moderate Risk")
    else:
        st.success("🟢 Low Risk")

    st.divider()

    # ---------------- RECOMMENDATIONS ---------------- #

    st.subheader("💡 Personalized Recommendations")

    recommendations = {

        "Anxiety": [
            "🧘 Practice mindfulness or meditation for 10–15 minutes daily.",
            "🚶 Take a short walk every day.",
            "☕ Reduce caffeine intake.",
            "😴 Maintain a consistent sleep schedule."
        ],

        "Depression": [
            "🌞 Spend some time outdoors.",
            "🏃 Exercise regularly.",
            "👨‍👩‍👧 Stay connected with family and friends.",
            "🍎 Eat balanced meals."
        ],

        "Stress": [
            "📝 Plan your daily tasks.",
            "🎵 Listen to relaxing music.",
            "💧 Drink enough water.",
            "😌 Practice deep breathing."
        ],

        "Normal": [
            "😊 Continue maintaining a healthy lifestyle.",
            "🏃 Stay physically active.",
            "😴 Sleep 7–8 hours daily."
        ],

        "Bipolar": [
            "💊 Continue prescribed medications.",
            "👨‍⚕️ Schedule regular psychiatrist visits."
        ],

        "Suicidal": [
            "🚨 Seek immediate professional help.",
            "📞 Contact a trusted family member or friend.",
            "🏥 Visit your nearest hospital or mental health professional."
        ],

        "Personality disorder": [
            "🧠 Consider psychotherapy.",
            "📅 Follow a structured daily routine."
        ]
    }

    for item in recommendations.get(
        prediction,
        ["💚 Please consult a qualified mental health professional."]
    ):
        st.success(item)

    st.divider()

    # ---------------- SUMMARY ---------------- #

    st.subheader("📝 Assessment Summary")

    summary = f"""
Date       : {datetime.now().strftime("%d-%m-%Y %H:%M")}

Prediction : {prediction}

Confidence : {confidence:.2f}%
"""

    st.code(summary)

    st.divider()

    # ---------------- PDF ---------------- #

    st.subheader("📄 Download Report")

    pdf = generate_pdf(
        statement,
        prediction,
        confidence
    )

    st.download_button(
        "⬇️ Download PDF Report",
        data=pdf,
        file_name="MindCare_AI_Report.pdf",
        mime="application/pdf",
        width="stretch"
    )

    st.divider()

    # ---------------- DISCLAIMER ---------------- #

    st.info(
        """
**Disclaimer**

This prediction is generated using a Machine Learning model and is intended
for educational purposes only.

It is **not** a medical diagnosis. If you are experiencing persistent emotional
distress, please consult a licensed mental health professional.
"""
    )