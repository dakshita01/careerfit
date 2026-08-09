"""
CareerFit — Job Skill Gap Analyzer
"""

import streamlit as st
import plotly.graph_objects as go

from src.skill_extractor import extract_skills
from src.analyzer import analyze_gap


st.set_page_config(
    page_title="CareerFit — Skill Gap Analyzer",
    page_icon=":dart:",
    layout="wide",
)

# Theme

st.markdown("""
<style>

.stApp {
    background:  #24050D;
    color: #FFF8F0;
}

/* Owl in the background */
.stApp::before {
    content: "🦉";
    position: fixed;
    top: 48%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 350px;
    opacity: 0.16;
    z-index: 0;
    pointer-events: none;
}

/* Keep content above the owl */
.stApp > div {
    position: relative;
    z-index: 1;
}

/* CareerFit */
h1 {
    font-size: 80px !important;
    font-weight: 800 !important;
    color: #FFF8F0 !important;
}

/* Other main headings */
h2, h3 {
    background: linear-gradient(
        90deg,
        #F8E7A1 0%,
        #D4AF37 42%,
        #D4AF37 50%,
        #1A0A0D 58%,
        #000000 100%
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700;
}

/* Slightly opaque glass-style text areas */
div[data-testid="stTextArea"] > div {
    background-color: rgba(255, 255, 255, 0.035) !important;
}

div[data-testid="stTextArea"] div[data-baseweb="base-input"] {
    background-color: rgba(255, 255, 255, 0.035) !important;
    border: 1px solid rgba(248, 231, 161, 0.20) !important;
}

div[data-testid="stTextArea"] textarea {
    background-color: transparent !important;
    color: #F5E6C8 !important;
}

</style>
""", unsafe_allow_html=True)


# Header
st.title("CareerFit 🎯")
st.subheader("Job Skill Gap Analyzer")
st.write(
    "For anyone job hunting and curious where they stand, enter your skills "
    "and a job description below, and see your results instantly."
)

st.divider()

# Store results
if "result" not in st.session_state:
    st.session_state.result = None

# Input
st.header("🦉 Your Skills")

user_skills_text = st.text_area(
    "List your skills, comma-separated",
    height=100,
    placeholder="e.g. Python, SQL, Pandas, Power BI, Excel, Git",
)

st.header("🦉 Job Description")

jd_text = st.text_area(
    "Paste the job description",
    height=260,
    placeholder="Paste the full job description here...",
)

analyze_clicked = st.button("Analyze Match", type="primary")

# Analysis
if analyze_clicked:
    if not jd_text.strip():
        st.warning("Please paste a job description first.")
        st.session_state.result = None

    elif not user_skills_text.strip():
        st.warning("Please list at least one skill you have.")
        st.session_state.result = None

    else:
        user_skills = extract_skills(user_skills_text)
        jd_skills = extract_skills(jd_text)

        if not jd_skills:
            st.error(
                "No recognized skills found in this job description. "
                "Try a more detailed posting."
            )
            st.session_state.result = None

        elif not user_skills:
            st.error(
                "We couldn't recognize any skills in what you typed. "
                "Try naming specific tools or languages, e.g. Python, SQL."
            )
            st.session_state.result = None

        else:
            st.session_state.result = analyze_gap(
                jd_skills,
                list(user_skills.keys())
            )

# Results
st.divider()
st.header("Results")

result = st.session_state.result

if result is None:
    st.info(
        "Your skill match results will appear here once you click "
        "**Analyze Match**."
    )

else:
    col1, col2, col3 = st.columns(3)

    col1.metric("Match Score", f"{result['match_percent']}%")
    col2.metric("Skills You Have", len(result["have"]))
    col3.metric("Skills Missing", len(result["missing"]))

    st.caption(
        "This match score reflects keyword overlap only. "
        "It is not a measure of your actual suitability for the job."
    )

    # Skill comparison
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Skills You Have")
        st.success(", ".join(result["have"]) if result["have"] else "None matched.")

    with col_b:
        st.subheader("Missing Skills")
        st.error(", ".join(result["missing"]) if result["missing"] else "None — full match.")

    # Learning order
    if result["priority"]:
        st.subheader("Recommended Learning Order")
        st.success(" → ".join(result["priority"]))

    # Chart
    st.subheader("Skill Match Breakdown")

    have = len(result["have"])
    missing = len(result["missing"])

    fig = go.Figure(
        go.Bar(
            x=["Have", "Missing"],
            y=[have, missing],
            marker_color=["#D4AF37", "#A52A3A"],
            text=[have, missing],
            textposition="outside",
            width=0.45,
        )
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFF8F0", size=14),
        yaxis=dict(
            title="Number of Skills",
            gridcolor="rgba(255,255,255,0.15)",
        ),
        xaxis=dict(showgrid=False),
        showlegend=False,
        height=320,
        margin=dict(t=10, b=10),
    )

    st.plotly_chart(fig, use_container_width=True)

# Footer

st.divider()

st.markdown(
    """
    <div style="
        text-align: center;
        color: #B8860B;
        font-size: 16px;
        font-weight: 500;
        margin-bottom: 4px;
    ">
        CareerFit v1 — Rule-based keyword matching. No AI or paid APIs used.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="
        text-align: center;
        color: #F0D878;
        font-size: 16px;
        font-weight: 500;
    ">
        Built with curiosity by Dakshita Biwal — turning small ideas into real, usable tools.
    </div>
    """,
    unsafe_allow_html=True,
)