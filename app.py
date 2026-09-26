import os
import streamlit as st
from utils.session_state import init_session_state
from utils.crisis_resources import locale_options, CRISIS_RESOURCES
from ui import chat_tab, mood_tab, addiction_tab, fear_tab

st.set_page_config(
    page_title="MindMate — Your AI Wellness Companion",
    page_icon="🌿",
    layout="wide",
)

# Bridge Streamlit's secrets manager into environment variables so
# utils/groq_client.py and rag/web_search.py (plain os.environ reads) work
# both locally (secrets.toml) and on Streamlit Community Cloud.
for _key in ("GROQ_API_KEY", "TAVILY_API_KEY"):
    try:
        if _key in st.secrets and _key not in os.environ:
            os.environ[_key] = st.secrets[_key]
    except Exception:
        pass  # secrets.toml not present yet (e.g. first local run before setup)

init_session_state()

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🌿 MindMate")
    st.caption("A warm companion for tough thoughts, habits you're changing, and fears you're facing.")

    st.warning(
        "**MindMate is a supportive companion, not a licensed therapist.** "
        "For diagnosis, medication, or crisis support, please contact a professional.",
        icon="⚠️",
    )

    st.markdown("---")
    st.session_state.user_name = st.text_input("Your first name (optional)", value=st.session_state.user_name)

    locale_labels = {code: info["label"] for code, info in CRISIS_RESOURCES.items()}
    st.session_state.locale = st.selectbox(
        "Your region (for crisis resources)",
        options=locale_options(),
        format_func=lambda c: locale_labels.get(c, c),
        index=locale_options().index(st.session_state.locale) if st.session_state.locale in locale_options() else 0,
    )

    st.session_state.web_search_enabled = st.toggle(
        "Allow live web search", value=st.session_state.web_search_enabled,
        help="Lets agents pull in current info when the source books don't cover something."
    )

    st.markdown("---")
    with st.expander("How MindMate works"):
        st.markdown(
            "- **Mental discomfort** → grounded in *Cognitive Behavior Therapy* (Judith Beck) "
            "and *Get Out of Your Mind and Into Your Life* (Steven Hayes, ACT)\n"
            "- **Addictions** → grounded in *Motivational Interviewing* (Miller & Rollnick), "
            "with CBT relapse-prevention support\n"
            "- **Fears** → grounded in ACT (Hayes): acceptance, defusion, and values-based action\n"
            "- A dedicated **safety layer** checks every message for crisis language *before* "
            "anything else runs, and always shows real crisis resources if needed\n"
            "- Every response passes through a final pass that checks it validates your "
            "feelings before offering any reframe — no toxic positivity"
        )

    with st.expander("🚨 Crisis resources (always available)"):
        region = CRISIS_RESOURCES[st.session_state.locale]
        for line in region["lines"]:
            st.markdown(f"- {line}")

# ---------- Header ----------
st.title("🌿 MindMate")
st.caption("Built by: **Engr. Mubashir Malik**")

tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "🌤️ Mood", "🌱 Habits", "🪜 Fears"])

with tab1:
    chat_tab.render()
with tab2:
    mood_tab.render()
with tab3:
    addiction_tab.render()
with tab4:
    fear_tab.render()

st.markdown("---")
st.caption("MindMate · Built by: Engr. Mubashir Malik · Powered by Groq + RAG + multi-agent reasoning")
