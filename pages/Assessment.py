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


# ---------------- HEADER ---------------- #

st.title("🧠 AI Mental Health Assessment")

st.write(
    "Describe how you are feeling today. "
    "Our Machine Learning model will analyze your text and estimate the most likely mental health condition."
)

st.divider()


# ---------------- MODEL INFO ---------------- #

c1, c2, c3 = st.columns(3)

c1.metric("Model", "Linear SVM")
c2.metric("Accuracy", "78.26%")
c3.metric("Prediction Type", "Text Classification")

st.divider()


# ---------------- INPUT ---------------- #

statement = st.text_area(
    "Describe your feelings",
    height=220,
    placeholder="""
Example:

I feel anxious all the time.
I don't enjoy anything anymore.
I can't sleep.
I feel lonely and hopeless.
"""
)

analyze = st.button(
    "🚀 Analyze",
    width="stretch"
)


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

    st.header("Prediction Result")

    if prediction.lower() == "depression":
        st.error(f"Prediction: {prediction}")
    elif prediction.lower() == "anxiety":
        st.warning(f"Prediction: {prediction}")
    else:
        st.success(f"Prediction: {prediction}")

    st.metric(
        "Confidence",
        f"{confidence:.2f}%"
    )

    st.progress(confidence / 100)

    st.subheader("Prediction Probabilities")

    df = pd.DataFrame({
        "Condition": classes,
        "Probability": probabilities
    })

    fig = px.bar(
        df,
        x="Condition",
        y="Probability",
        color="Probability",
        text="Probability"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}"
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