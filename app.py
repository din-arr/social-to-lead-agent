import streamlit as st
from agent.graph import process_message

st.set_page_config(
    page_title="AutoStream AI Agent",
    page_icon="🎀",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #fff0f7 0%, #ffe4f1 45%, #ffd6eb 100%);
        color: #4a2140;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffdeee 0%, #ffd0e6 100%);
        border-right: 1px solid rgba(255, 105, 180, 0.18);
    }

    .hero-card {
        background: linear-gradient(135deg, #fff7fb 0%, #ffe8f3 100%);
        border: 1px solid rgba(255, 105, 180, 0.18);
        border-radius: 28px;
        padding: 30px 34px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(255, 105, 180, 0.10);
    }

    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        color: #a12662;
        line-height: 1.05;
        margin-bottom: 0.45rem;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        color: #8a4f73;
        margin-bottom: 0;
    }

    .section-label {
        font-size: 1rem;
        font-weight: 700;
        color: #a12662;
        margin-top: 0.5rem;
        margin-bottom: 0.8rem;
    }

    .info-card {
        background: rgba(255, 255, 255, 0.55);
        border: 1px solid rgba(255, 105, 180, 0.16);
        border-radius: 18px;
        padding: 14px 16px;
        margin-bottom: 12px;
        color: #5b2547;
        box-shadow: 0 6px 18px rgba(255, 105, 180, 0.07);
    }

    .bot-card {
        background: linear-gradient(135deg, #fff7fb 0%, #ffe4f1 100%);
        border: 1px solid rgba(255, 105, 180, 0.18);
        border-radius: 20px;
        padding: 16px 18px;
        margin: 10px 0 14px 0;
        color: #4f2442;
        box-shadow: 0 8px 22px rgba(255, 105, 180, 0.07);
    }

    .user-card {
        background: linear-gradient(135deg, #ffd9eb 0%, #ffc7e2 100%);
        border: 1px solid rgba(214, 51, 132, 0.16);
        border-radius: 20px;
        padding: 16px 18px;
        margin: 10px 0 14px 0;
        color: #5a1e45;
        box-shadow: 0 8px 22px rgba(214, 51, 132, 0.08);
    }

    .msg-row {
        display: flex;
        gap: 12px;
        align-items: flex-start;
    }

    .msg-icon {
        font-size: 1.45rem;
        line-height: 1;
        margin-top: 2px;
    }

    .msg-text {
        font-size: 1.05rem;
        line-height: 1.7;
        word-break: break-word;
    }

    .quick-tip {
        color: #8b5978;
        font-size: 0.96rem;
        margin-top: 0.25rem;
        margin-bottom: 1rem;
    }

    .stButton > button {
        width: 100%;
        border-radius: 16px;
        border: 1px solid rgba(255, 105, 180, 0.16);
        background: linear-gradient(135deg, #fff7fb 0%, #ffe8f3 100%);
        color: #a12662;
        font-weight: 700;
        padding: 0.72rem 1rem;
        box-shadow: 0 6px 16px rgba(255, 105, 180, 0.07);
    }

    .stButton > button:hover {
        border-color: #d63384;
        color: #7c184a;
        background: linear-gradient(135deg, #ffe8f3 0%, #ffd8eb 100%);
    }

    div[data-testid="stChatInput"] {
        margin-top: 18px;
    }

    div[data-testid="stChatInput"] textarea {
        background: rgba(255,255,255,0.8) !important;
        color: #5b2547 !important;
        border-radius: 16px !important;
    }

    div[data-testid="stChatInput"] button {
        background: #ff5fa2 !important;
        color: white !important;
        border-radius: 14px !important;
    }

    .stSuccess {
        background: rgba(255, 105, 180, 0.10) !important;
        color: #7c184a !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 105, 180, 0.18) !important;
    }

    h1, h2, h3, p, label, div {
        color: inherit;
    }
</style>
""", unsafe_allow_html=True)


def initialize_state():
    if "agent_state" not in st.session_state:
        st.session_state.agent_state = {
            "messages": [],
            "intent": "",
            "name": "",
            "email": "",
            "platform": "",
            "lead_captured": False,
            "lead_stage": ""
        }

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": (
                    "Hii! I’m the AutoStream AI Agent 🎀 "
                    "I can help you with pricing, features, refunds, and sign-up."
                )
            }
        ]

    if "quick_prompt" not in st.session_state:
        st.session_state.quick_prompt = ""


def reset_chat():
    st.session_state.agent_state = {
        "messages": [],
        "intent": "",
        "name": "",
        "email": "",
        "platform": "",
        "lead_captured": False,
        "lead_stage": ""
    }
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": (
                "Hii! I’m the AutoStream AI Agent 🎀 "
                "I can help you with pricing, features, refunds, and sign-up."
            )
        }
    ]
    st.session_state.quick_prompt = ""


def render_message(role: str, content: str):
    card_class = "bot-card" if role == "assistant" else "user-card"
    icon = "🎀" if role == "assistant" else "💗"
    safe_content = content.replace("\n", "<br>")
    st.markdown(
        f"""
        <div class="{card_class}">
            <div class="msg-row">
                <div class="msg-icon">{icon}</div>
                <div class="msg-text">{safe_content}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


initialize_state()

with st.sidebar:
    st.markdown("## 💖 Session Info")

    st.markdown(
        f'<div class="info-card"><b>Current Intent:</b><br>{st.session_state.agent_state.get("intent", "") or "Not detected yet"}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="info-card"><b>Name:</b><br>{st.session_state.agent_state.get("name", "") or "Not provided"}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="info-card"><b>Email:</b><br>{st.session_state.agent_state.get("email", "") or "Not provided"}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="info-card"><b>Platform:</b><br>{st.session_state.agent_state.get("platform", "") or "Not provided"}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="info-card"><b>Lead Stage:</b><br>{st.session_state.agent_state.get("lead_stage", "") or "Not started"}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="info-card"><b>Lead Captured:</b><br>{"Yes ✅" if st.session_state.agent_state.get("lead_captured", False) else "No ❌"}</div>',
        unsafe_allow_html=True
    )

    st.divider()

    if st.button("Reset Chat"):
        reset_chat()
        st.rerun()

left, center, right = st.columns([1, 3.8, 1])

with center:
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">🎀 AutoStream AI Agent</div>
            <div class="hero-subtitle">
                Conversational AI for product queries, lead qualification, and lead capture.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="section-label">✨ Quick Actions</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)

    if c1.button("Pricing"):
        st.session_state.quick_prompt = "Tell me about pricing"

    if c2.button("Features"):
        st.session_state.quick_prompt = "What features are included?"

    if c3.button("Refund Policy"):
        st.session_state.quick_prompt = "What is your refund policy?"

    if c4.button("Start Signup"):
        st.session_state.quick_prompt = "start"

    st.markdown(
        '<div class="quick-tip">Try asking about pricing, features, refunds, or click <b>Start Signup</b> to begin the lead flow.</div>',
        unsafe_allow_html=True
    )

    for message in st.session_state.chat_history:
        render_message(message["role"], message["content"])

    user_input = st.chat_input("Type your message here...")

    if st.session_state.quick_prompt:
        user_input = st.session_state.quick_prompt
        st.session_state.quick_prompt = ""

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        render_message("user", user_input)

        try:
            response = process_message(st.session_state.agent_state, user_input)

            st.session_state.chat_history.append({"role": "assistant", "content": response})
            render_message("assistant", response)

            if st.session_state.agent_state.get("lead_captured", False):
                st.success("Lead captured successfully 💖")

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            st.session_state.chat_history.append({"role": "assistant", "content": error_message})
            st.error(error_message)