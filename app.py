import streamlit as st
from agent.graph import process_message

st.set_page_config(
    page_title="AutoStream AI Agent",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background:
            radial-gradient(circle at 15% 20%, rgba(173, 216, 255, 0.22) 0%, transparent 18%),
            radial-gradient(circle at 85% 25%, rgba(124, 167, 255, 0.16) 0%, transparent 18%),
            radial-gradient(circle at 55% 80%, rgba(220, 235, 255, 0.32) 0%, transparent 20%),
            linear-gradient(180deg, #f7fbff 0%, #eef5fb 100%);
        color: #1e293b;
    }

    header[data-testid="stHeader"] {
        background: rgba(248, 252, 255, 0.92) !important;
        border-bottom: 1px solid #d8e5f2 !important;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #edf5fc 0%, #e5eff8 100%) !important;
        border-right: 1px solid #d5e2ef !important;
    }

    section[data-testid="stSidebar"] * {
        color: #1f2937 !important;
    }

    .sidebar-title {
        font-size: 1.65rem;
        font-weight: 800;
        color: #10243e;
        margin-bottom: 16px;
    }

    .hero-card {
        text-align: center;
        padding: 28px;
        background: rgba(255, 255, 255, 0.92);
        border-radius: 24px;
        border: 1px solid #d6e4f2;
        margin-bottom: 22px;
        box-shadow: 0 18px 35px rgba(15, 23, 42, 0.06);
    }

    .hero-title {
        margin: 0;
        font-size: 2.8rem;
        font-weight: 800;
        color: #10243e;
    }

    .hero-subtitle {
        margin-top: 8px;
        color: #64748b;
        font-size: 1rem;
    }

    .info-card {
        background: rgba(255, 255, 255, 0.90);
        border-radius: 16px;
        padding: 14px 16px;
        margin-bottom: 12px;
        border: 1px solid #d6e4f2;
        box-shadow: 0 8px 18px rgba(15, 23, 42, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        font-size: 0.96rem;
    }

    .info-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 14px 26px rgba(15, 23, 42, 0.09);
    }

    .info-card b {
        font-size: 1.02rem;
        color: #10243e;
    }

    .section-title {
        font-size: 1.08rem;
        font-weight: 800;
        color: #17365d;
        margin: 10px 0;
    }

    .quick-note {
        color: #60758f;
        font-size: 0.95rem;
        margin-bottom: 14px;
    }

    .stButton > button {
        width: 100%;
        background: linear-gradient(145deg, #ffffff, #eef5fb) !important;
        color: #17365d !important;
        border: 1px solid #d6e4f2 !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        box-shadow: 0 8px 18px rgba(15, 23, 42, 0.05) !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        background: linear-gradient(145deg, #4c88d9, #1f3b64) !important;
        color: white !important;
        border-color: #3b6dad !important;
        transform: translateY(-3px);
        box-shadow: 0 16px 26px rgba(31, 59, 100, 0.20) !important;
    }

    .chat-shell {
        background: rgba(255, 255, 255, 0.78);
        border: 1px solid #d9e5f1;
        border-radius: 28px;
        padding: 22px;
        box-shadow: 0 20px 38px rgba(15, 23, 42, 0.05);
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
        box-shadow: 0 10px 18px rgba(15, 23, 42, 0.12);
    }

    .avatar-bot {
        background: linear-gradient(145deg, #7db8ff, #3f6ca8);
        color: white;
    }

    .avatar-user {
        background: linear-gradient(145deg, #243b5a, #0f172a);
        color: white;
    }

    .bubble {
        padding: 15px 18px;
        border-radius: 22px;
        font-size: 0.99rem;
        line-height: 1.65;
        word-break: break-word;
        transition: transform 0.2s ease;
    }

    .bubble:hover {
        transform: translateY(-3px);
    }

    .bubble.assistant {
        background: linear-gradient(145deg, #fafdff, #ecf4fb);
        border: 1px solid #d8e5f1;
        color: #243447;
        border-bottom-left-radius: 8px;
        box-shadow: 0 12px 22px rgba(15, 23, 42, 0.04);
    }

    .bubble.user {
        background: linear-gradient(145deg, #4c88d9, #1f3b64);
        border: 1px solid #2e578d;
        color: white;
        border-bottom-right-radius: 8px;
        box-shadow: 0 16px 28px rgba(31, 59, 100, 0.22);
    }

    div[data-testid="stChatInput"] {
        margin-top: 18px;
    }

    div[data-testid="stChatInput"] > div {
        background: linear-gradient(145deg, #e9f2fa, #dce8f4) !important;
        border-radius: 24px !important;
        padding: 14px !important;
        border: 1px solid #cfdeec !important;
        box-shadow: 0 16px 28px rgba(15, 23, 42, 0.08) !important;
    }

    div[data-testid="stChatInput"] textarea {
        background: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cdddeb !important;
        border-radius: 14px !important;
        opacity: 1 !important;
    }

    div[data-testid="stChatInput"] textarea::placeholder {
        color: #7a8da5 !important;
        opacity: 1 !important;
    }

    div[data-testid="stChatInput"] button {
        background: linear-gradient(145deg, #7db8ff, #31598d) !important;
        color: #ffffff !important;
        border-radius: 14px !important;
        border: none !important;
        box-shadow: 0 10px 18px rgba(49, 89, 141, 0.24) !important;
    }

    div[data-testid="stChatInput"] button:hover {
        background: linear-gradient(145deg, #659fde, #203f66) !important;
        color: #ffffff !important;
    }

    .stSuccess {
        background: #eef7ff !important;
        color: #1e4e85 !important;
        border: 1px solid #cfe1f3 !important;
        border-radius: 14px !important;
    }

    .stAlert {
        border-radius: 14px !important;
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

    state = st.session_state.agent_state

    st.markdown(
        f'<div class="info-card"><b>Intent:</b><br>{state.get("intent", "") or "Not detected yet"}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="info-card"><b>Name:</b><br>{state.get("name", "") or "Not provided"}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="info-card"><b>Email:</b><br>{state.get("email", "") or "Not provided"}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="info-card"><b>Platform:</b><br>{state.get("platform", "") or "Not provided"}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="info-card"><b>Lead Stage:</b><br>{state.get("lead_stage", "") or "Not started"}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="info-card"><b>Lead:</b><br>{"Captured ✅" if state.get("lead_captured", False) else "Not yet"}</div>',
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

    st.markdown('<div class="section-title">Quick Actions</div>', unsafe_allow_html=True)

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

st.markdown(
    """
    <script>
        const scrollToBottom = () => {
            const parent = window.parent.document;
            const chatContainer = parent.querySelector('[data-testid="stChatInput"]');
            if (chatContainer) {
                chatContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        };
        setTimeout(scrollToBottom, 200);
    </script>
    """,
    unsafe_allow_html=True
)