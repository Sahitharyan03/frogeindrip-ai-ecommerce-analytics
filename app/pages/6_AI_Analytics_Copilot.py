"""Page 6: AI Analytics Copilot Chat Interface."""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(ROOT_DIR / "src") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "src"))

import streamlit as st

from app.components.ui import inject_custom_css, render_page_header, render_sidebar
from frogeindrip.ai.copilot import FrogeindripCopilot
from frogeindrip.config import OPENAI_API_KEY

st.set_page_config(page_title="AI Analytics Copilot | Frogeindrip", page_icon="🐸", layout="wide")
inject_custom_css()
render_sidebar()

render_page_header(
    title="Frogeindrip AI Analytics Copilot",
    subtitle="Natural-language business intelligence agent with tool-grounded execution and privacy guardrails.",
    badge_type="hybrid",
)

# Engine Status & Mode
api_key_configured = bool(OPENAI_API_KEY)
if api_key_configured:
    st.success("🟢 **Copilot Engine:** OpenAI Tool-Calling Mode Enabled (Grounded Synthesis)")
else:
    st.info("🔵 **Copilot Engine:** Deterministic Offline Mode Enabled (Instant, Free, 100% Grounded in DuckDB Marts)")

# Initialize Chat History
if "copilot_messages" not in st.session_state:
    st.session_state.copilot_messages = [
        {
            "role": "assistant",
            "content": (
                "👋 Hello! I am the **Frogeindrip AI Analytics Copilot**.\n\n"
                "I can analyze verified Square evidence, customer RFM segments, cohort retention, repeat buyer GMV, and product margins. "
                "Ask any analytical question below or select one of the suggested prompts!"
            ),
        }
    ]

# Suggested Quick Questions
st.markdown("##### 💡 Suggested Executive Inquiries:")
col_q1, col_q2, col_q3, col_q4 = st.columns(4)

suggested_q = None
with col_q1:
    if st.button("📊 Average Order Value", use_container_width=True):
        suggested_q = "What was our Average Order Value and overall revenue?"
with col_q2:
    if st.button("🔁 Repeat Buyer GMV %", use_container_width=True):
        suggested_q = "What percentage of GMV came from repeat customers under lifetime vs point-in-time?"
with col_q3:
    if st.button("🏷️ Verified Square Evidence", use_container_width=True):
        suggested_q = "What are the verified sales totals and peak months from the Square screenshots?"
with col_q4:
    if st.button("👕 High-Margin Products", use_container_width=True):
        suggested_q = "Which apparel products generated the highest realized gross profit margins?"

# Render Chat History
for msg in st.session_state.copilot_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle User Input
user_query = st.chat_input("Ask an analytics question (e.g., 'What were the highest-revenue months?')...")
active_query = suggested_q or user_query

if active_query:
    # Append user question
    st.session_state.copilot_messages.append({"role": "user", "content": active_query})
    with st.chat_message("user"):
        st.markdown(active_query)

    # Execute Copilot
    copilot = FrogeindripCopilot()
    with st.spinner("Executing analytical query..."):
        answer = copilot.ask(active_query)

    # Format Assistant Response
    with st.chat_message("assistant"):
        st.markdown(answer.summary_markdown)

    st.session_state.copilot_messages.append({"role": "assistant", "content": answer.summary_markdown})

st.markdown("<br>", unsafe_allow_html=True)

# Safety & Privacy Architecture
with st.expander("🛡️ Copilot Safety & Privacy Architecture"):
    st.markdown(
        """
        - **No Arbitrary SQL:** The Copilot does not allow the model to craft free-form SQL against the database. It exclusively maps intents to approved, read-only Python functions.
        - **Data Masking:** Customer names, emails, and transaction IDs are never passed into generative prompts.
        - **Provenance Tagging:** Every response explicitly discloses the exact data source (Verified Square POS capture vs. Synthetic DuckDB Mart) to avoid misrepresenting simulation as client truth.
        """
    )
