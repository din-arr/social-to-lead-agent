import streamlit as st
from agent.graph import process_message

st.set_page_config(
    page_title="AutoStream AI Agent",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>

    .stApp {
        background: #fffdf7;
        color: #2c2c2c;
    }

    header[data-testid="stHeader"] {
        background: #ffffff !important;
        border-bottom: 1px solid #f1f1f1;
    }

    section[data-testid="stSidebar"] {
        background: #fff8ec;
        border-right: 1px solid #f3e6d2;
    }

    .hero-card {
        background: white;
        border: 1px solid #f3e6d2;
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 20px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.04);
    }

    .hero-title {
        font-size: 2.6rem;
        font-weight: 700;
        color: #2c2c2c;
        margin-bottom: 6px;
    }

    .hero-subtitle {
        color: #7a7a7a;
        font-size: 1rem;
    }

    .section-label {
        font-weight: 600;
        color: #444;
        margin-bottom: 8px;
    }

    .info-card {
        background: white;
        border: 1px solid #f0e4cf;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
        color: #444;
    }

    .bot-card {
        background: #fff8ec;
        border: 1px solid #f0e4cf;
        border-radius: 14px;
        padding: 14px;
        margin: 10px 0;
    }

    .user-card {
        background: #ff8c2a;
        border-radius: 14px;
        padding: 14px;
        margin: 10px 0;
        color: white;
    }

    .msg-row {
        display: flex;
        gap: 10px;
        align-items: flex-start;
    }

    .msg-icon {
        font-size: 1.2rem;
    }

    .msg-text {
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .stButton > button {
        background: white;
        border: 1px solid #f0e4cf;
        color: #444;
        border-radius: 10px;
        width: 100%;
    }

    .stButton > button:hover {
        background: #ff8c2a;
        color: white;
        border-color: #ff8c2a;
    }

    div[data-testid="stChatInput"] textarea {
        background: white !important;
        color: black !important;
        border-radius: 10px !important;
        border: 1px solid #f0e4cf !important;
    }

    div[data-testid="stChatInput"] button {
        background: #ff8c2a !important;
        color: white !important;
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

    st.markdown(f'<div class="info-card"><b>Intent:</b><br>{st.session_state.agent_state.get("intent","-")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-card"><b>Name:</b><br>{st.session_state.agent_state.get("name","-")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-card"><b>Email:</b><br>{st.session_state.agent_state.get("email","-")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-card"><b>Platform:</b><br>{st.session_state.agent_state.get("platform","-")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-card"><b>Lead:</b><br>{"Captured ✅" if st.session_state.agent_state.get("lead_captured") else "Not yet"}</div>', unsafe_allow_html=True)

    if st.button("Reset Chat"):
        reset_chat()
        st.rerun()

left, center, right = st.columns([1, 3.8, 1])

with center:
    st.markdown("""
        <div class="hero-card">
            <div class="hero-title">AutoStream AI Agent</div>
            <div class="hero-subtitle">
                Conversational AI for product queries and lead capture
            </div>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    if c1.button("Pricing"):
        st.session_state.quick_prompt = "pricing"

    if c2.button("Features"):
        st.session_state.quick_prompt = "features"

    if c3.button("Refund"):
        st.session_state.quick_prompt = "refund"

    if c4.button("Start"):
        st.session_state.quick_prompt = "start"

    for msg in st.session_state.chat_history:
        render_message(msg["role"], msg["content"])

    user_input = st.chat_input("Type your message...")

    if st.session_state.quick_prompt:
        user_input = st.session_state.quick_prompt
        st.session_state.quick_prompt = ""

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        render_message("user", user_input)

        response = process_message(st.session_state.agent_state, user_input)

        st.session_state.chat_history.append({"role": "assistant", "content": response})
        render_message("assistant", response)

        if st.session_state.agent_state.get("lead_captured"):
            st.success("Lead captured successfully")