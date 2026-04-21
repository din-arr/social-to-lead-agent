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
            radial-gradient(circle at 12% 18%, rgba(255, 179, 71, 0.20) 0%, transparent 18%),
            radial-gradient(circle at 86% 22%, rgba(255, 140, 42, 0.14) 0%, transparent 20%),
            radial-gradient(circle at 52% 82%, rgba(255, 214, 140, 0.15) 0%, transparent 18%),
            linear-gradient(180deg, #fffdf8 0%, #fff6e8 100%);
        color: #2c2c2c;
    }

    header[data-testid="stHeader"] {
        background: rgba(255,255,255,0.88) !important;
        backdrop-filter: blur(12px);
        border-bottom: 1px solid rgba(234, 217, 187, 0.75) !important;
        box-shadow: 0 8px 18px rgba(0,0,0,0.04);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fff7ea 0%, #fff1dc 100%) !important;
        border-right: 1px solid #ead9bb !important;
        box-shadow:
            inset -8px 0 16px rgba(255,255,255,0.55),
            10px 0 24px rgba(0,0,0,0.03);
    }

    section[data-testid="stSidebar"] * {
        color: #2c2c2c !important;
    }

    .sidebar-title {
        font-size: 1.7rem;
        font-weight: 800;
        color: #1f2937;
        margin-bottom: 16px;
        letter-spacing: -0.02em;
        text-shadow: 0 1px 0 rgba(255,255,255,0.85);
    }

    .hero-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.95), rgba(255,247,234,0.95));
        border: 1px solid rgba(234, 217, 187, 0.95);
        border-radius: 30px;
        padding: 34px;
        margin-bottom: 26px;
        box-shadow:
            0 32px 60px rgba(38, 25, 4, 0.09),
            0 10px 18px rgba(255,255,255,0.92) inset,
            0 -10px 20px rgba(232, 196, 132, 0.12) inset;
        transform: perspective(1400px) rotateX(1.2deg);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }

    .hero-card:hover {
        transform: perspective(1400px) rotateX(0deg) translateY(-4px);
        box-shadow:
            0 40px 80px rgba(38, 25, 4, 0.12),
            0 10px 18px rgba(255,255,255,0.92) inset,
            0 -10px 20px rgba(232, 196, 132, 0.12) inset;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        color: #262626;
        margin-bottom: 8px;
        line-height: 1.05;
        letter-spacing: -0.03em;
        text-shadow: 0 2px 0 rgba(255,255,255,0.7);
    }

    .hero-subtitle {
        color: #6f6f6f;
        font-size: 1.05rem;
    }

    .section-label {
        font-weight: 800;
        color: #3a3227;
        margin: 10px 0 10px 0;
        font-size: 1.08rem;
    }

    .info-card {
        background: linear-gradient(145deg, #ffffff, #fff7ea);
        border: 1px solid #ead9bb;
        border-radius: 20px;
        padding: 16px 18px;
        margin-bottom: 14px;
        color: #3f3f3f;
        box-shadow:
            0 14px 28px rgba(0,0,0,0.05),
            0 2px 0 rgba(255,255,255,0.88) inset;
        transform: translateY(0) scale(1);
        transition: transform 0.22s ease, box-shadow 0.22s ease;
    }

    .info-card:hover {
        transform: translateY(-8px) scale(1.01);
        box-shadow:
            0 24px 44px rgba(0,0,0,0.08),
            0 2px 0 rgba(255,255,255,0.88) inset;
    }

    .info-card b {
        font-size: 1.08rem;
        font-weight: 700;
        color: #111827;
    }

    .quick-note {
        color: #777777;
        font-size: 0.95rem;
        margin-bottom: 14px;
    }

    .stButton > button {
        width: 100%;
        background: linear-gradient(145deg, #ffffff, #fff2df) !important;
        color: #333333 !important;
        border: 1px solid #ead9bb !important;
        border-radius: 16px !important;
        font-weight: 700 !important;
        box-shadow:
            0 10px 18px rgba(0,0,0,0.05),
            0 2px 0 rgba(255,255,255,0.92) inset !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        background: linear-gradient(145deg, #ffb14a, #ff922b) !important;
        color: white !important;
        border-color: #ff922b !important;
        transform: translateY(-6px) scale(1.02);
        box-shadow:
            0 22px 30px rgba(255, 146, 43, 0.25),
            0 2px 0 rgba(255,255,255,0.18) inset !important;
    }

    .chat-shell {
        background: linear-gradient(145deg, rgba(255,255,255,0.84), rgba(255,246,231,0.80));
        border: 1px solid rgba(234, 217, 187, 0.95);
        border-radius: 30px;
        padding: 22px 22px 8px 22px;
        box-shadow:
            0 28px 50px rgba(0,0,0,0.05),
            0 10px 16px rgba(255,255,255,0.88) inset;
    }

    .message-row {
        display: flex;
        margin: 16px 0;
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
        gap: 12px;
        align-items: flex-end;
        max-width: 78%;
    }

    .message-row.user .message-wrap {
        flex-direction: row-reverse;
    }

    .avatar-bot, .avatar-user {
        width: 40px;
        height: 40px;
        min-width: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 0.95rem;
        box-shadow:
            0 12px 20px rgba(0,0,0,0.14),
            0 2px 0 rgba(255,255,255,0.35) inset;
        transition: transform 0.2s ease;
    }

    .avatar-bot:hover, .avatar-user:hover {
        transform: translateY(-3px) scale(1.05);
    }

    .avatar-bot {
        background: linear-gradient(145deg, #ffb14a, #ff922b);
        color: white;
    }

    .avatar-user {
        background: linear-gradient(145deg, #333949, #1f2230);
        color: white;
    }

    .bubble {
        padding: 15px 18px;
        border-radius: 22px;
        font-size: 0.99rem;
        line-height: 1.65;
        word-break: break-word;
        transform: translateY(0);
        transition: transform 0.22s ease, box-shadow 0.22s ease;
    }

    .bubble:hover {
        transform: translateY(-6px) scale(1.01);
    }

    .bubble.assistant {
        background: linear-gradient(145deg, #fffaf1, #fff1dd);
        border: 1px solid #ecdcbc;
        color: #2f2f2f;
        border-bottom-left-radius: 8px;
        box-shadow:
            0 14px 24px rgba(0,0,0,0.05),
            0 2px 0 rgba(255,255,255,0.72) inset;
    }

    .bubble.user {
        background: linear-gradient(145deg, #ffad45, #ff922b);
        border: 1px solid #ff922b;
        color: white;
        border-bottom-right-radius: 8px;
        box-shadow:
            0 18px 30px rgba(255, 146, 43, 0.26),
            0 2px 0 rgba(255,255,255,0.15) inset;
    }

    div[data-testid="stChatInput"] {
        margin-top: 18px;
    }

    div[data-testid="stChatInput"] > div {
        background: linear-gradient(145deg, #2b3040, #1f2230) !important;
        border-radius: 22px !important;
        padding: 14px !important;
        border: none !important;
        box-shadow:
            0 18px 32px rgba(0,0,0,0.18),
            0 2px 0 rgba(255,255,255,0.04) inset !important;
    }

    div[data-testid="stChatInput"] textarea {
        background: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #e6d7bf !important;
        border-radius: 14px !important;
        opacity: 1 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) inset;
    }

    div[data-testid="stChatInput"] textarea::placeholder {
        color: #8c8c8c !important;
        opacity: 1 !important;
    }

    div[data-testid="stChatInput"] button {
        background: linear-gradient(145deg, #ffb14a, #ff922b) !important;
        color: #ffffff !important;
        border-radius: 14px !important;
        border: none !important;
        box-shadow:
            0 12px 20px rgba(255, 146, 43, 0.28),
            0 2px 0 rgba(255,255,255,0.18) inset !important;
        transition: transform 0.2s ease !important;
    }

    div[data-testid="stChatInput"] button:hover {
        background: linear-gradient(145deg, #ff9d31, #e97e13) !important;
        color: #ffffff !important;
        transform: translateY(-2px) scale(1.03);
    }

    .stSuccess {
        background: #eefbf0 !important;
        color: #216b2f !important;
        border: 1px solid #cce8d2 !important;
        border-radius: 14px !important;
    }

    .stAlert {
        border-radius: 14px !important;
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

        try:
            response = process_message(st.session_state.agent_state, user_input)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            st.session_state.chat_history.append({"role": "assistant", "content": error_message})
            st.rerun()