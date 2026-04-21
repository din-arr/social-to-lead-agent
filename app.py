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
        background: #0b1220;
        color: #e5e7eb;
    }

    header[data-testid="stHeader"] {
        background: #0b1220 !important;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }

    section[data-testid="stSidebar"] {
        background: #0f172a;
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    .hero-card {
        background: #111827;
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 18px;
        padding: 28px;
        margin-bottom: 20px;
    }

    .hero-title {
        font-size: 2.6rem;
        font-weight: 700;
        color: #f9fafb;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        color: #9ca3af;
        font-size: 1rem;
    }

    .section-label {
        font-weight: 600;
        color: #cbd5e1;
        margin-bottom: 8px;
    }

    .info-card {
        background: #111827;
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 10px;
        color: #cbd5e1;
    }

    .bot-card {
        background: #1e293b;
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 14px;
        margin: 10px 0;
        color: #e5e7eb;
    }

    .user-card {
        background: #1e40af;
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
        line-height: 1.4;
    }

    .msg-text {
        font-size: 0.95rem;
        line-height: 1.6;
        word-break: break-word;
    }

    .stButton > button {
        background: #1f2937;
        border: 1px solid rgba(255,255,255,0.06);
        color: #e5e7eb;
        border-radius: 10px;
        width: 100%;
        font-weight: 600;
    }

    .stButton > button:hover {
        background: #2563eb;
        color: white;
    }

    div[data-testid="stChatInput"] textarea {
        background: #111827 !important;
        color: white !important;
        border-radius: 10px !important;
    }

    div[data-testid="stChatInput"] button {
        background: #2563eb !important;
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
            <div class="hero-title">🤖 AutoStream AI Agent</div>
            <div class="hero-subtitle">
                Conversational AI for product queries, lead qualification, and lead capture.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="section-label">Quick Actions</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)

    if c1.button("Pricing"):
        st.session_state.quick_prompt = "Tell me about pricing"

    if c2.button("Features"):
        st.session_state.quick_prompt = "What features are included?"

    if c3.button("Refund Policy"):
        st.session_state.quick_prompt = "What is your refund policy?"

    if c4.button("Start Signup"):
        st.session_state.quick_prompt = "start"

    st.caption("Try pricing, features, refunds, or start the signup flow.")

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
                st.success("Lead captured successfully.")

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            st.session_state.chat_history.append({"role": "assistant", "content": error_message})
            st.error(error_message)