import streamlit as st
from agent.graph import process_message

st.set_page_config(
    page_title="AutoStream AI Agent",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 20% 20%, rgba(255, 181, 72, 0.10) 0, rgba(255, 181, 72, 0.10) 2px, transparent 2px, transparent 100px),
            radial-gradient(circle at 80% 30%, rgba(255, 140, 42, 0.08) 0, rgba(255, 140, 42, 0.08) 2px, transparent 2px, transparent 120px),
            radial-gradient(circle at 40% 70%, rgba(255, 208, 120, 0.08) 0, rgba(255, 208, 120, 0.08) 2px, transparent 2px, transparent 110px),
            linear-gradient(180deg, #fffdf8 0%, #fff9ef 100%);
        color: #2c2c2c;
    }

    header[data-testid="stHeader"] {
        background: rgba(255, 255, 255, 0.86) !important;
        backdrop-filter: blur(8px);
        border-bottom: 1px solid #ece4d3 !important;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fff8ec 0%, #fff4e3 100%) !important;
        border-right: 1px solid #f0e1c7 !important;
    }

    section[data-testid="stSidebar"] * {
        color: #2c2c2c !important;
    }

    .sidebar-title {
        font-size: 1.6rem;
        font-weight: 800;
        color: #1f2937;
        margin-bottom: 14px;
        letter-spacing: -0.02em;
    }

    .hero-card {
        background: rgba(255, 255, 255, 0.82);
        backdrop-filter: blur(10px);
        border: 1px solid #f0e4cf;
        border-radius: 24px;
        padding: 30px;
        margin-bottom: 22px;
        box-shadow: 0 10px 30px rgba(31, 41, 55, 0.06);
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        color: #222222;
        margin-bottom: 8px;
        line-height: 1.05;
        letter-spacing: -0.03em;
    }

    .hero-subtitle {
        color: #6f6f6f;
        font-size: 1.04rem;
    }

    .section-label {
        font-weight: 700;
        color: #3c3c3c;
        margin: 8px 0 10px 0;
        font-size: 1.05rem;
    }

    .info-card {
        background: rgba(255, 255, 255, 0.75);
        border: 1px solid #f0e4cf;
        border-radius: 16px;
        padding: 14px 16px;
        margin-bottom: 12px;
        color: #3f3f3f;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.03);
        font-size: 0.98rem;
    }

    .info-card b {
        font-size: 1.06rem;
        font-weight: 700;
        color: #111827;
    }

    .quick-note {
        color: #777777;
        font-size: 0.95rem;
        margin-bottom: 12px;
    }

    .stButton > button {
        width: 100%;
        background: rgba(255, 255, 255, 0.78) !important;
        color: #333333 !important;
        border: 1px solid #f0e4cf !important;
        border-radius: 14px !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
    }

    .stButton > button:hover {
        background: #ff922b !important;
        color: white !important;
        border-color: #ff922b !important;
    }

    .chat-shell {
        background: rgba(255, 255, 255, 0.58);
        backdrop-filter: blur(10px);
        border: 1px solid #f0e4cf;
        border-radius: 24px;
        padding: 20px 20px 6px 20px;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.04);
    }

    .message-row {
        display: flex;
        margin: 14px 0;
        width: 100%;
    }

    .message-row.assistant {
        justify-content: flex-start;
    }

    .message-row.user {
        justify-content: flex-end;
    }

    .message-wrap {
        display: flex;
        gap: 10px;
        align-items: flex-end;
        max-width: 78%;
    }

    .message-row.user .message-wrap {
        flex-direction: row-reverse;
    }

    .avatar-bot, .avatar-user {
        width: 34px;
        height: 34px;
        min-width: 34px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 0.92rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.10);
    }

    .avatar-bot {
        background: #ff922b;
        color: white;
    }

    .avatar-user {
        background: #1f2937;
        color: white;
    }

    .bubble {
        padding: 14px 16px;
        border-radius: 18px;
        font-size: 0.98rem;
        line-height: 1.65;
        word-break: break-word;
        box-shadow: 0 4px 14px rgba(0,0,0,0.04);
    }

    .bubble.assistant {
        background: #fff8ec;
        border: 1px solid #f0e4cf;
        color: #2f2f2f;
        border-bottom-left-radius: 6px;
    }

    .bubble.user {
        background: #ff922b;
        border: 1px solid #ff922b;
        color: white;
        border-bottom-right-radius: 6px;
    }

    div[data-testid="stChatInput"] {
        margin-top: 18px;
    }

    div[data-testid="stChatInput"] > div {
        background: #1f2230 !important;
        border-radius: 18px !important;
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
    row_class = "assistant" if role == "assistant" else "user"
    avatar_class = "avatar-bot" if role == "assistant" else "avatar-user"
    avatar_text = "A" if role == "assistant" else "U"
    safe_content = content.replace("\n", "<br>")

    st.markdown(
        f"""
        <div class="message-row {row_class}">
            <div class="message-wrap">
                <div class="{avatar_class}">{avatar_text}</div>
                <div class="bubble {row_class}">{safe_content}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


initialize_state()

with st.sidebar:
    st.markdown(
        '<div class="sidebar-title">Session Info</div>',
        unsafe_allow_html=True
    )

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

left, center, right = st.columns([0.7, 3.8, 0.7])

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

    st.markdown('<div class="chat-shell">', unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        render_message(msg["role"], msg["content"])
    st.markdown('</div>', unsafe_allow_html=True)

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