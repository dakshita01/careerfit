"""
CareerFit - Job Skill Gap Analyzer
Streamlit front-end.
"""

import streamlit as st
import plotly.graph_objects as go

from src.skill_extractor import extract_skills
from src.analyzer import analyze_gap

st.set_page_config(
    page_title="CareerFit - Skill Gap Analyzer", 
    page_icon="🎯", 
    layout="centered"
)

st.title("🎯 CareerFit — Job Skill Gap Analyzer")
st.caption("Type your skills, paste a job description, and see how you stack up.")

# user type their own skills
st.subheader("1️⃣ Your Skills")
user_skills_text = st.text_area(
    "List your skills (comma-separated works well)",
    height=100,
    placeholder="e.g. Python, SQL, Pandas, Power BI, Excel, Git"
)

# job description
st.subheader("2️⃣ Job Description")
jd_text = st.text_area(
    "Paste job description here",
    height=200,
    placeholder="e.g. Looking for a Data Analyst skilled in Python, SQL, Pandas, Power BI, Excel, Statistics and Tableau."
)

analyze_clicked = st.button("Analyze", type="primary")

if analyze_clicked:
    if not jd_text.strip():
        st.warning("Please paste a job description first.")
    elif not user_skills_text.strip():
        st.warning("Please type at least one skill you have.")
    else:
        # Same extraction function used for both inputs
        user_skills_found = extract_skills(user_skills_text)
        jd_skills_found = extract_skills(jd_text)

        if not jd_skills_found:
            st.error("No recognized skills found in this job description. Try a more detailed posting.")
        elif not user_skills_found:
            st.error("We couldn't recognize any skills in what you typed. Try naming specific tools/languages (e.g. Python, SQL).")
        else:
            result = analyze_gap(jd_skills_found, list(user_skills_found.keys()))

            col1, col2, col3 = st.columns(3)
            col1.metric("Match Score", f"{result['match_percent']}%")
            col2.metric("Skills You Have", len(result["have"]))
            col3.metric("Skills Missing", len(result["missing"]))

            st.info(
                "ℹ️ This match score reflects **keyword overlap only** — "
                "it is NOT a measure of your actual suitability for the job."
            )

            c1, c2 = st.columns(2)
            with c1:
                st.subheader("✅ Skills You Have")
                if result["have"]:
                    for s in result["have"]:
                        st.write(f"- {s}")
                else:
                    st.write("None matched.")

            with c2:
                st.subheader("❌ Missing Skills")
                if result["missing"]:
                    for s in result["missing"]:
                        st.write(f"- {s}")
                else:
                    st.write("You match every required skill! 🎉")

            if result["priority"]:
                st.subheader("📌 Priority: What to Learn First")
                st.success(" → ".join(result["priority"]))

            st.subheader("📊 Skill Match Breakdown")
            fig = go.Figure(data=[
                go.Bar(
                    x=["Have", "Missing"],
                    y=[len(result["have"]), len(result["missing"])],
                    marker_color=["#2ecc71", "#e74c3c"],
                    text=[len(result["have"]), len(result["missing"])],
                    textposition="auto",
                )
            ])
            fig.update_layout(yaxis_title="Number of Skills", showlegend=False, height=350)
            st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("CareerFit v1 · Rule-based keyword matching · No AI/ML APIs used")