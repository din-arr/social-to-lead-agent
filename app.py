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
        background: linear-gradient(180deg, #07111f 0%, #0a1020 100%);
        color: white;
    }

    section[data-testid="stSidebar"] {
        background: #232633;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    .main-title {
        font-size: 4rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.25rem;
        line-height: 1.1;
    }

    .sub-title {
        font-size: 1.15rem;
        color: #b8bfd3;
        margin-bottom: 2rem;
    }

    .info-card {
        background: rgba(255,255,255,0.04);
        padding: 14px 16px;
        border-radius: 14px;
        margin-bottom: 12px;
        border: 1px solid rgba(255,255,255,0.06);
        color: white;
    }

    .quick-title {
        font-size: 1rem;
        font-weight: 700;
        color: #d8deee;
        margin-top: 0.5rem;
        margin-bottom: 0.8rem;
    }

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08);
        background: #1a2030;
        color: white;
        font-weight: 600;
        padding: 0.65rem 1rem;
    }

    .stButton > button:hover {
        border-color: #ff9d00;
        color: #ffcc70;
    }

    .stChatMessage {
        background: transparent !important;
    }

    [data-testid="stChatInput"] {
        border-top: 1px solid rgba(255,255,255,0.08);
        padding-top: 0.75rem;
    }

    .helper-text {
        color: #aeb7cb;
        font-size: 0.95rem;
        margin-top: 0.5rem;
        margin-bottom: 1rem;
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


initialize_state()

with st.sidebar:
    st.markdown("## Session Info")

    st.markdown(
        f'<div class="info-card"><b>Current Intent:</b> {st.session_state.agent_state.get("intent", "") or "Not detected yet"}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="info-card"><b>Name:</b> {st.session_state.agent_state.get("name", "") or "Not provided"}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="info-card"><b>Email:</b> {st.session_state.agent_state.get("email", "") or "Not provided"}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="info-card"><b>Platform:</b> {st.session_state.agent_state.get("platform", "") or "Not provided"}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="info-card"><b>Lead Stage:</b> {st.session_state.agent_state.get("lead_stage", "") or "Not started"}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="info-card"><b>Lead Captured:</b> {"Yes ✅" if st.session_state.agent_state.get("lead_captured", False) else "No ❌"}</div>',
        unsafe_allow_html=True
    )

    st.divider()

    if st.button("Reset Chat"):
        reset_chat()
        st.rerun()

st.markdown('<div class="main-title">🤖 AutoStream AI Agent</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Conversational AI for product queries, lead qualification, and lead capture.</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="quick-title">Quick Actions</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

if col1.button("Pricing"):
    st.session_state.quick_prompt = "Tell me about pricing"

if col2.button("Features"):
    st.session_state.quick_prompt = "What features are included?"

if col3.button("Refund Policy"):
    st.session_state.quick_prompt = "What is your refund policy?"

if col4.button("Start Signup"):
    st.session_state.quick_prompt = "start"

st.markdown(
    '<div class="helper-text">Try asking about pricing, features, refunds, or click <b>Start Signup</b> to begin lead capture.</div>',
    unsafe_allow_html=True
)

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your message here...")

if st.session_state.quick_prompt:
    user_input = st.session_state.quick_prompt
    st.session_state.quick_prompt = ""

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        response = process_message(st.session_state.agent_state, user_input)

        st.session_state.chat_history.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

        if st.session_state.agent_state.get("lead_captured", False):
            st.success("Lead captured successfully.")

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        st.session_state.chat_history.append({"role": "assistant", "content": error_message})

        with st.chat_message("assistant"):
            st.error(error_message)