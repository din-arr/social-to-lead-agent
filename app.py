import streamlit as st
from agent.graph import process_message

st.set_page_config(
    page_title="AutoStream AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background: #fffdf7;
        color: #2c2c2c;
    }

    header[data-testid="stHeader"] {
        background: #ffffff !important;
        border-bottom: 1px solid #ece7dc !important;
    }

    section[data-testid="stSidebar"] {
        background: #fff8ec !important;
        border-right: 1px solid #f3e6d2 !important;
    }

    section[data-testid="stSidebar"] * {
        color: #2c2c2c !important;
    }

    .hero-card {
        background: #ffffff;
        border: 1px solid #f0e4cf;
        border-radius: 18px;
        padding: 28px;
        margin-bottom: 20px;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.04);
    }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #2c2c2c;
        margin-bottom: 8px;
        line-height: 1.1;
    }

    .hero-subtitle {
        color: #727272;
        font-size: 1.02rem;
    }

    .section-label {
        font-weight: 700;
        color: #3c3c3c;
        margin: 8px 0 10px 0;
    }

    .info-card {
        background: #ffffff;
        border: 1px solid #f0e4cf;
        border-radius: 12px;
        padding: 12px 14px;
        margin-bottom: 10px;
        color: #3f3f3f;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
    }

    .bot-card {
        background: #fff8ec;
        border: 1px solid #f0e4cf;
        border-radius: 16px;
        padding: 14px 16px;
        margin: 12px 0;
        color: #2f2f2f;
    }

    .user-card {
        background: #ff922b;
        border: 1px solid #ff922b;
        border-radius: 16px;
        padding: 14px 16px;
        margin: 12px 0;
        color: #ffffff;
    }

    .msg-row {
        display: flex;
        gap: 10px;
        align-items: flex-start;
    }

    .msg-icon {
        font-size: 1.2rem;
        line-height: 1.5;
    }

    .msg-text {
        font-size: 1rem;
        line-height: 1.65;
        word-break: break-word;
    }

    .quick-note {
        color: #777777;
        font-size: 0.95rem;
        margin-bottom: 12px;
    }

    .stButton > button {
        width: 100%;
        background: #ffffff !important;
        color: #333333 !important;
        border: 1px solid #f0e4cf !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
    }

    .stButton > button:hover {
        background: #ff922b !important;
        color: white !important;
        border-color: #ff922b !important;
    }

    div[data-testid="stChatInput"] {
        margin-top: 18px;
    }

    div[data-testid="stChatInput"] > div {
        background: #1f2230 !important;
        border-radius: 16px !important;
        padding: 14px !important;
        border: none !important;
    }

    div[data-testid="stChatInput"] textarea {
        background: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #e6d7bf !important;
        border-radius: 12px !important;
        opacity: 1 !important;
    }

    div[data-testid="stChatInput"] textarea::placeholder {
        color: #8c8c8c !important;
        opacity: 1 !important;
    }

    div[data-testid="stChatInput"] button {
        background: #ff922b !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        border: none !important;
    }

    div[data-testid="stChatInput"] button:hover {
        background: #e97e13 !important;
        color: #ffffff !important;
    }

    .stSuccess {
        background: #eefbf0 !important;
        color: #216b2f !important;
        border: 1px solid #cce8d2 !important;
        border-radius: 12px !important;
    }

    .stAlert {
        border-radius: 12px !important;
    }

    span, label, p, h1, h2, h3, h4, h5, h6, div {
        color: inherit;
    }

    svg {
        color: currentColor !important;
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
                    "Hi! I’m the AutoStream AI Agent. "
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
                "Hi! I’m the AutoStream AI Agent. "
                "I can help you with pricing, features, refunds, and sign-up."
            )
        }
    ]

    st.session_state.quick_prompt = ""


def render_message(role: str, content: str):
    card_class = "bot-card" if role == "assistant" else "user-card"
    icon = "🤖" if role == "assistant" else "👤"
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
    st.markdown("## Session Info")

    st.markdown(
        f'<div class="info-card"><b>Intent:</b><br>{st.session_state.agent_state.get("intent", "") or "Not detected yet"}</div>',
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
        f'<div class="info-card"><b>Lead:</b><br>{"Captured ✅" if st.session_state.agent_state.get("lead_captured", False) else "Not yet"}</div>',
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
            <div class="hero-title">AutoStream AI Agent</div>
            <div class="hero-subtitle">
                Conversational AI for product queries and lead capture
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="section-label">Quick Actions</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    if c1.button("Pricing"):
        st.session_state.quick_prompt = "pricing"

    if c2.button("Features"):
        st.session_state.quick_prompt = "features"

    if c3.button("Refund"):
        st.session_state.quick_prompt = "refund"

    if c4.button("Start"):
        st.session_state.quick_prompt = "start"

    st.markdown(
        '<div class="quick-note">Try pricing, features, refund policy, or start the signup flow.</div>',
        unsafe_allow_html=True
    )

    for msg in st.session_state.chat_history:
        render_message(msg["role"], msg["content"])

    user_input = st.chat_input("Type your message...")

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
                st.success("Lead captured successfully.")

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            st.session_state.chat_history.append({"role": "assistant", "content": error_message})
            st.error(error_message)